#!/bin/bash
# Build Kit Voice as a small app bundle (voice/build/KitVoice.app), so macOS asks for microphone and
# system-audio permission for the app itself. Works with the Command Line Tools; Xcode is not needed.
# Signing: ad-hoc by default; set KITVOICE_SIGN to a code-signing identity to keep permissions across rebuilds.
set -euo pipefail
cd "$(dirname "$0")"
swift build -c release --product KitVoice
APP=build/KitVoice.app
rm -rf "$APP"; mkdir -p "$APP/Contents/MacOS"
cp .build/release/KitVoice "$APP/Contents/MacOS/KitVoice"
cp Resources/Info.plist "$APP/Contents/Info.plist"
codesign --force --sign "${KITVOICE_SIGN:--}" --identifier local.wiki-kit.voice "$APP"
echo "built $(pwd)/$APP"
