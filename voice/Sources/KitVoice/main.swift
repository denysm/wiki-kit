// Kit Voice prototype: two-track capture ("me" = microphone, "them" = call apps) into memory.
// Phase 1 of docs/voice-design.md, first step. Usage:
//   KitVoice list                         audio processes (pid, bundle id, whether they play sound now)
//   KitVoice capture --consent [--apps id1,id2] [--seconds N] [--debug-wav DIR] [--no-mic]
// --consent   required: you told everyone in the call and nobody objected (stub of the consent gate)
// --apps      tap only processes whose bundle id starts with one of these (default: all output except Kit Voice)
// --debug-wav TEST ONLY, with recording consent: write me.wav and them.wav (16 kHz) into DIR at the end
// Stop with Ctrl-C (SIGINT) or SIGTERM, or after --seconds. Without --debug-wav nothing is written to disk
// except one line in the audit log (~/Library/Application Support/KitVoice/audit.log).
import AVFoundation
import CoreAudio
import Foundation

setvbuf(stdout, nil, _IOLBF, 0)

func arg(_ name: String) -> String? {
    let a = CommandLine.arguments
    guard let i = a.firstIndex(of: name), i + 1 < a.count else { return nil }
    return a[i + 1]
}
func flag(_ name: String) -> Bool { CommandLine.arguments.contains(name) }

func audit(_ line: String) {
    let dir = FileManager.default.homeDirectoryForCurrentUser.appendingPathComponent("Library/Application Support/KitVoice")
    try? FileManager.default.createDirectory(at: dir, withIntermediateDirectories: true)
    let url = dir.appendingPathComponent("audit.log")
    let text = ISO8601DateFormatter().string(from: Date()) + " " + line + "\n"
    if let h = try? FileHandle(forWritingTo: url) {
        h.seekToEndOfFile(); h.write(text.data(using: .utf8)!); try? h.close()
    } else {
        try? text.write(to: url, atomically: true, encoding: .utf8)
    }
}

func bar(_ db: Float) -> String {
    let n = max(0, min(20, Int((db + 60) / 3)))
    return String(repeating: "█", count: n) + String(repeating: "·", count: 20 - n)
}

/// 100 ms energy envelope in dB.
func envelope(_ x: [Float]) -> [Float] {
    let w = Int(kRate / 10)
    return stride(from: 0, to: max(0, x.count - w + 1), by: w).map { i in
        var s: Float = 0
        for v in x[i..<(i + w)] { s += v * v }
        return 10 * log10(max(s / Float(w), 1e-12))
    }
}

func pearson(_ a: [Float], _ b: [Float]) -> Float? {
    let n = min(a.count, b.count)
    guard n > 10 else { return nil }
    let x = Array(a.prefix(n)), y = Array(b.prefix(n))
    let mx = x.reduce(0, +) / Float(n), my = y.reduce(0, +) / Float(n)
    var sxy: Float = 0, sxx: Float = 0, syy: Float = 0
    for i in 0..<n { let dx = x[i] - mx, dy = y[i] - my; sxy += dx * dy; sxx += dx * dx; syy += dy * dy }
    return sxx > 0 && syy > 0 ? sxy / (sxx.squareRoot() * syy.squareRoot()) : nil
}

func writeWav(_ samples: [Float], to url: URL) throws {
    let settings: [String: Any] = [AVFormatIDKey: kAudioFormatLinearPCM, AVSampleRateKey: kRate,
                                   AVNumberOfChannelsKey: 1, AVLinearPCMBitDepthKey: 16,
                                   AVLinearPCMIsFloatKey: false, AVLinearPCMIsBigEndianKey: false]
    let file = try AVAudioFile(forWriting: url, settings: settings, commonFormat: .pcmFormatFloat32, interleaved: false)
    let chunk = 16_000
    var i = 0
    while i < samples.count {
        let n = min(chunk, samples.count - i)
        let buf = AVAudioPCMBuffer(pcmFormat: kMono, frameCapacity: AVAudioFrameCount(n))!
        buf.frameLength = AVAudioFrameCount(n)
        samples[i..<(i + n)].withUnsafeBufferPointer { buf.floatChannelData![0].update(from: $0.baseAddress!, count: n) }
        try file.write(from: buf)
        i += n
    }
}

func list() {
    print("pid      plays  bundle id")
    for p in audioProcesses().sorted(by: { $0.bundleID < $1.bundleID }) {
        print(String(format: "%-8d %@  %@", p.pid, p.runningOutput ? "yes " : "    ", p.bundleID.isEmpty ? "(none)" : p.bundleID))
    }
}

func capture() {
    guard flag("--consent") else {
        print("Refusing to capture: pass --consent after telling everyone in the call and hearing no objection.")
        exit(2)
    }
    let me = Track(name: "me"), them = Track(name: "them")
    let tap = SystemTap(), mic = Microphone()
    let prefixes = (arg("--apps") ?? "").split(separator: ",").map { String($0) }.filter { !$0.isEmpty }
    let procs = prefixes.isEmpty ? [] :
        audioProcesses().filter { p in prefixes.contains { p.bundleID.hasPrefix($0) } }.map(\.object)
    if !prefixes.isEmpty && procs.isEmpty {
        print("none of \(prefixes) has an audio process yet; tapping all output except Kit Voice instead")
    }
    let own = processObject(pid: getpid()).map { [$0] } ?? []
    do {
        try tap.start(processes: procs, exclude: own, into: them)
        print("them: \(tap.describe)")
    } catch {
        print("them: \(error)"); exit(1)
    }
    if flag("--no-mic") {
        print("me:   off (--no-mic)")
    } else {
        do { try mic.start(into: me); print("me:   \(mic.describe)") } catch { print("me:   \(error)") }
    }
    let debugDir = arg("--debug-wav")
    audit("capture start: them=\(tap.describe); me=\(flag("--no-mic") ? "off" : mic.describe); apps=\(prefixes.joined(separator: ",")); debug-wav=\(debugDir != nil)")
    let started = Date()

    let meter = DispatchSource.makeTimerSource(queue: .main)
    meter.schedule(deadline: .now() + 0.5, repeating: 0.5)
    meter.setEventHandler {
        let a = me.level(lastSeconds: 0.5), b = them.level(lastSeconds: 0.5)
        print(String(format: "%6.1fs  me %@ %6.1f dB   them %@ %6.1f dB", Date().timeIntervalSince(started), bar(a), a, bar(b), b))
    }
    meter.resume()

    var finished = false
    func finish(_ why: String) {
        guard !finished else { return }
        finished = true
        meter.cancel(); tap.stop(); mic.stop()
        let m = me.snapshot(), t = them.snapshot()
        let em = envelope(m), et = envelope(t)
        let speech = { (e: [Float]) in Double(e.filter { $0 > -45 }.count) / 10 }
        print(String(format: "\nstopped (%@) after %.1f s", why, Date().timeIntervalSince(started)))
        print(String(format: "me:   %.1f s in RAM, speech above -45 dB: %.1f s", Double(m.count) / kRate, speech(em)))
        print(String(format: "them: %.1f s in RAM, speech above -45 dB: %.1f s", Double(t.count) / kRate, speech(et)))
        let both = zip(em, et).filter { $0.0 > -45 && $0.1 > -45 }.count
        print(String(format: "both tracks loud at once: %.1f s", Double(both) / 10))
        if let r = pearson(em, et) {
            print(String(format: "envelope correlation me/them: %.2f (high values mean the microphone hears the call: use a headset)", r))
        }
        if let dir = debugDir {
            let url = URL(fileURLWithPath: (dir as NSString).expandingTildeInPath, isDirectory: true)
            do {
                try FileManager.default.createDirectory(at: url, withIntermediateDirectories: true)
                if !m.isEmpty { try writeWav(m, to: url.appendingPathComponent("me.wav")) }
                if !t.isEmpty { try writeWav(t, to: url.appendingPathComponent("them.wav")) }
                print("TEST ONLY: wrote me.wav and them.wav to \(url.path); delete them after the test")
            } catch { print("debug wav: \(error)") }
        }
        me.wipe(); them.wipe()
        audit("capture stop: \(why); me=\(String(format: "%.1f", Double(m.count) / kRate))s them=\(String(format: "%.1f", Double(t.count) / kRate))s; debug-wav=\(debugDir != nil)")
        exit(0)
    }

    signal(SIGINT, SIG_IGN); signal(SIGTERM, SIG_IGN)
    let sigs = [SIGINT, SIGTERM].map { s -> DispatchSourceSignal in
        let src = DispatchSource.makeSignalSource(signal: s, queue: .main)
        src.setEventHandler { finish(s == SIGINT ? "Ctrl-C" : "SIGTERM") }
        src.resume()
        return src
    }
    _ = sigs
    if let s = arg("--seconds").flatMap(Double.init) {
        DispatchQueue.main.asyncAfter(deadline: .now() + s) { finish("time limit") }
    }
    withExtendedLifetime(sigs) { dispatchMain() }
}

switch CommandLine.arguments.dropFirst().first {
case "list": list()
case "capture": capture()
default:
    print("usage: KitVoice list | KitVoice capture --consent [--apps id1,id2] [--seconds N] [--debug-wav DIR] [--no-mic]")
    exit(2)
}
