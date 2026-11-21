// Two-track capture for Kit Voice (docs/voice-design.md, layer 1):
// "them" = a Core Audio process tap on the call apps (or on all output except Kit Voice itself),
// "me"   = the default microphone through AVAudioEngine.
// Both tracks are converted to 16 kHz mono Float32 and kept in memory only.
import AVFoundation
import AudioToolbox
import CoreAudio
import Foundation

let kRate = 16_000.0
let kMono = AVAudioFormat(commonFormat: .pcmFormatFloat32, sampleRate: kRate, channels: 1, interleaved: false)!

struct KVError: Error, CustomStringConvertible {
    let description: String
}

@discardableResult
func check(_ status: OSStatus, _ what: String) throws -> OSStatus {
    guard status == noErr else { throw KVError(description: "\(what) failed (OSStatus \(status))") }
    return status
}

/// One track: samples at 16 kHz in RAM, appended from any input format.
final class Track {
    let name: String
    private var samples: [Float] = []
    private let lock = NSLock()
    private var converter: AVAudioConverter?
    private var source: AVAudioFormat?
    private(set) var firstHostTime: UInt64 = 0

    init(name: String, reserveSeconds: Double = 600) {
        self.name = name
        samples.reserveCapacity(Int(kRate * reserveSeconds))
    }

    func append(_ buf: AVAudioPCMBuffer, hostTime: UInt64) {
        if source == nil || source! != buf.format {
            source = buf.format
            converter = AVAudioConverter(from: buf.format, to: kMono)
            converter?.downmix = true
        }
        guard let conv = converter, buf.frameLength > 0 else { return }
        let cap = AVAudioFrameCount(Double(buf.frameLength) * kRate / buf.format.sampleRate + 64)
        guard let out = AVAudioPCMBuffer(pcmFormat: kMono, frameCapacity: cap) else { return }
        var fed = false
        var err: NSError?
        conv.convert(to: out, error: &err) { _, status in
            if fed { status.pointee = .noDataNow; return nil }
            fed = true
            status.pointee = .haveData
            return buf
        }
        guard err == nil, let ch = out.floatChannelData, out.frameLength > 0 else { return }
        lock.lock()
        if firstHostTime == 0 { firstHostTime = hostTime }
        samples.append(contentsOf: UnsafeBufferPointer(start: ch[0], count: Int(out.frameLength)))
        lock.unlock()
    }

    var count: Int { lock.lock(); defer { lock.unlock() }; return samples.count }

    func snapshot() -> [Float] { lock.lock(); defer { lock.unlock() }; return samples }

    /// RMS level in dBFS of the last `seconds` of audio.
    func level(lastSeconds seconds: Double) -> Float {
        lock.lock(); defer { lock.unlock() }
        let n = min(samples.count, Int(kRate * seconds))
        guard n > 0 else { return -120 }
        var sum: Float = 0
        for x in samples[(samples.count - n)...] { sum += x * x }
        return 10 * log10(max(sum / Float(n), 1e-12))
    }

    /// Overwrite and drop the samples (stop and purge).
    func wipe() {
        lock.lock()
        for i in samples.indices { samples[i] = 0 }
        samples.removeAll(keepingCapacity: false)
        lock.unlock()
    }
}

// MARK: - Core Audio helpers

func propAddress(_ selector: AudioObjectPropertySelector,
                 _ scope: AudioObjectPropertyScope = kAudioObjectPropertyScopeGlobal) -> AudioObjectPropertyAddress {
    AudioObjectPropertyAddress(mSelector: selector, mScope: scope, mElement: kAudioObjectPropertyElementMain)
}

func getUInt32(_ obj: AudioObjectID, _ selector: AudioObjectPropertySelector) -> UInt32? {
    var addr = propAddress(selector)
    var value: UInt32 = 0
    var size = UInt32(MemoryLayout<UInt32>.size)
    return AudioObjectGetPropertyData(obj, &addr, 0, nil, &size, &value) == noErr ? value : nil
}

func getString(_ obj: AudioObjectID, _ selector: AudioObjectPropertySelector) -> String? {
    var addr = propAddress(selector)
    var value: Unmanaged<CFString>?
    var size = UInt32(MemoryLayout<Unmanaged<CFString>?>.size)
    guard AudioObjectGetPropertyData(obj, &addr, 0, nil, &size, &value) == noErr, let v = value else { return nil }
    return v.takeRetainedValue() as String
}

func defaultDevice(_ selector: AudioObjectPropertySelector) -> AudioObjectID? {
    var addr = propAddress(selector)
    var id = AudioObjectID(kAudioObjectUnknown)
    var size = UInt32(MemoryLayout<AudioObjectID>.size)
    let st = AudioObjectGetPropertyData(AudioObjectID(kAudioObjectSystemObject), &addr, 0, nil, &size, &id)
    return st == noErr && id != kAudioObjectUnknown ? id : nil
}

func processObject(pid: pid_t) -> AudioObjectID? {
    var addr = propAddress(kAudioHardwarePropertyTranslatePIDToProcessObject)
    var pidVar = pid
    var obj = AudioObjectID(kAudioObjectUnknown)
    var size = UInt32(MemoryLayout<AudioObjectID>.size)
    let st = AudioObjectGetPropertyData(AudioObjectID(kAudioObjectSystemObject), &addr,
                                        UInt32(MemoryLayout<pid_t>.size), &pidVar, &size, &obj)
    return st == noErr && obj != kAudioObjectUnknown ? obj : nil
}

struct AudioProcess {
    let object: AudioObjectID
    let pid: pid_t
    let bundleID: String
    let runningOutput: Bool
}

func audioProcesses() -> [AudioProcess] {
    var addr = propAddress(kAudioHardwarePropertyProcessObjectList)
    var size: UInt32 = 0
    let sys = AudioObjectID(kAudioObjectSystemObject)
    guard AudioObjectGetPropertyDataSize(sys, &addr, 0, nil, &size) == noErr else { return [] }
    var ids = [AudioObjectID](repeating: 0, count: Int(size) / MemoryLayout<AudioObjectID>.size)
    guard AudioObjectGetPropertyData(sys, &addr, 0, nil, &size, &ids) == noErr else { return [] }
    return ids.map { id in
        var pidAddr = propAddress(kAudioProcessPropertyPID)
        var pid: pid_t = 0
        var psize = UInt32(MemoryLayout<pid_t>.size)
        _ = AudioObjectGetPropertyData(id, &pidAddr, 0, nil, &psize, &pid)
        return AudioProcess(object: id, pid: pid,
                            bundleID: getString(id, kAudioProcessPropertyBundleID) ?? "",
                            runningOutput: (getUInt32(id, kAudioProcessPropertyIsRunningOutput) ?? 0) != 0)
    }
}

// MARK: - "them": process tap

final class SystemTap {
    private var tapID = AudioObjectID(kAudioObjectUnknown)
    private var aggregateID = AudioObjectID(kAudioObjectUnknown)
    private var procID: AudioDeviceIOProcID?
    private let queue = DispatchQueue(label: "kitvoice.tap", qos: .userInitiated)
    private(set) var describe = ""

    /// Tap the given processes, or every process except `exclude` when `processes` is empty.
    func start(processes: [AudioObjectID], exclude: [AudioObjectID], into track: Track) throws {
        let desc: CATapDescription
        if processes.isEmpty {
            desc = CATapDescription(stereoGlobalTapButExcludeProcesses: exclude)
            describe = "all output except Kit Voice"
        } else {
            desc = CATapDescription(stereoMixdownOfProcesses: processes)
            describe = "\(processes.count) call-app process(es)"
        }
        desc.uuid = UUID()
        desc.name = "Kit Voice them"
        desc.isPrivate = true
        desc.muteBehavior = .unmuted
        try check(AudioHardwareCreateProcessTap(desc, &tapID), "create process tap")

        let aggregate: [String: Any] = [
            kAudioAggregateDeviceNameKey: "Kit Voice tap",
            kAudioAggregateDeviceUIDKey: "local.wiki-kit.voice.tap." + UUID().uuidString,
            kAudioAggregateDeviceIsPrivateKey: true,
            kAudioAggregateDeviceIsStackedKey: false,
            kAudioAggregateDeviceTapAutoStartKey: true,
            kAudioAggregateDeviceSubDeviceListKey: [] as [Any],
            kAudioAggregateDeviceTapListKey: [[kAudioSubTapDriftCompensationKey: true,
                                               kAudioSubTapUIDKey: desc.uuid.uuidString]],
        ]
        try check(AudioHardwareCreateAggregateDevice(aggregate as CFDictionary, &aggregateID), "create aggregate device")

        var asbd = AudioStreamBasicDescription()
        var size = UInt32(MemoryLayout<AudioStreamBasicDescription>.size)
        var addr = propAddress(kAudioTapPropertyFormat)
        try check(AudioObjectGetPropertyData(tapID, &addr, 0, nil, &size, &asbd), "read tap format")
        guard let format = AVAudioFormat(streamDescription: &asbd) else { throw KVError(description: "tap format not usable") }
        describe += String(format: ", %.0f Hz, %d ch", format.sampleRate, format.channelCount)

        try check(AudioDeviceCreateIOProcIDWithBlock(&procID, aggregateID, queue) { _, input, inTime, _, _ in
            guard let buf = AVAudioPCMBuffer(pcmFormat: format, bufferListNoCopy: input, deallocator: nil) else { return }
            track.append(buf, hostTime: inTime.pointee.mHostTime)
        }, "create IO proc")
        try check(AudioDeviceStart(aggregateID, procID), "start tap device")
    }

    func stop() {
        if aggregateID != kAudioObjectUnknown {
            if let p = procID { AudioDeviceStop(aggregateID, p); AudioDeviceDestroyIOProcID(aggregateID, p) }
            AudioHardwareDestroyAggregateDevice(aggregateID)
        }
        if tapID != kAudioObjectUnknown { AudioHardwareDestroyProcessTap(tapID) }
        procID = nil; aggregateID = AudioObjectID(kAudioObjectUnknown); tapID = AudioObjectID(kAudioObjectUnknown)
    }
}

// MARK: - "me": microphone

final class Microphone {
    private let engine = AVAudioEngine()
    private(set) var describe = ""

    func start(into track: Track) throws {
        guard defaultDevice(kAudioHardwarePropertyDefaultInputDevice) != nil else {
            throw KVError(description: "no input device: connect a headset or a microphone")
        }
        let input = engine.inputNode
        let format = input.outputFormat(forBus: 0)
        guard format.sampleRate > 0, format.channelCount > 0 else { throw KVError(description: "microphone format not usable") }
        let name = defaultDevice(kAudioHardwarePropertyDefaultInputDevice).flatMap { getString($0, kAudioObjectPropertyName) } ?? "default input"
        describe = String(format: "%@, %.0f Hz, %d ch", name, format.sampleRate, format.channelCount)
        input.installTap(onBus: 0, bufferSize: 4096, format: format) { buf, when in
            track.append(buf, hostTime: when.hostTime)
        }
        try engine.start()
    }

    func stop() {
        engine.inputNode.removeTap(onBus: 0)
        engine.stop()
    }
}
