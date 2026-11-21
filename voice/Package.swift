// swift-tools-version: 5.10
import PackageDescription

let package = Package(
    name: "KitVoice",
    platforms: [.macOS("14.4")],
    targets: [
        .executableTarget(name: "KitVoice", path: "Sources/KitVoice")
    ]
)
