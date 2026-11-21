#!/bin/bash
# Run Kit Voice through `open`, so the app (not the terminal) holds the permissions.
# Output goes to this terminal, or to $KITVOICE_LOG when set. Examples:
#   voice/run.sh list
#   voice/run.sh capture --consent --seconds 60
#   voice/run.sh capture --consent --apps us.zoom.xos,com.microsoft.teams2 --debug-wav /tmp/kv
set -euo pipefail
cd "$(dirname "$0")"
OUT="${KITVOICE_LOG:-$(tty 2>/dev/null || echo /dev/null)}"
exec open -W -n --stdout "$OUT" --stderr "$OUT" build/KitVoice.app --args "$@"
