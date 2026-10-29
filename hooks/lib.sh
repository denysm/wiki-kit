# Sourced by the hooks. Sets $py to a Python >= 3.9 command: python3 on macOS
# and Linux; python or the py launcher on Windows (Git Bash), where python3 is
# often a Microsoft Store stub. Empty when none works.
py=""
for c in python3 python "py -3"; do
  # shellcheck disable=SC2086
  if $c -c 'import sys; sys.exit(sys.version_info < (3, 9))' >/dev/null 2>&1; then py="$c"; break; fi
done
