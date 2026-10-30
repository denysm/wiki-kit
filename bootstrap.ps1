# Install wiki-kit on Windows 10 or 11: Git, Python and Claude Code if missing
# (asks first), the llm-wiki plugin, an empty hub, the specialists and the front
# desk, then a self-check. Safe to run again: it only adds what is missing and
# never overwrites your files. Windows PowerShell 5.1 or PowerShell 7.
#
# Run (PowerShell blocks downloaded scripts by default, hence the bypass):
#   powershell -ExecutionPolicy Bypass -File $HOME\Projects\wiki-kit\bootstrap.ps1
# Options:
#   -Hub DIR    where your wiki lives (default: hub_path from
#               ~\.config\llm-wiki\config.json, else ~\wiki)
#   -Lang ru    language of the hub rules and of the chat (en, ru or uk; default:
#               the Windows display language)
#   -NoPlugin   skip the Claude Code plugin step
#   -Yes        install missing tools without asking
# Environment: WIKI_KIT_DIR (where to clone the kit, default ~\Projects\wiki-kit),
# WIKI_KIT_REPO (the kit's git address; needed only when this file runs outside a kit).
# A full log goes to %TEMP%\wiki-kit-bootstrap.log: send it if something fails.
param(
  [string]$Hub = "",
  [string]$Lang = "",
  [switch]$NoPlugin,
  [switch]$Yes
)
$ErrorActionPreference = "Continue"
$PluginRepo = "https://github.com/nvk/llm-wiki.git#v0.25.1"
$PluginId = "wiki@llm-wiki"
$Log = Join-Path $env:TEMP "wiki-kit-bootstrap.log"
try { Start-Transcript -Path $Log -Append | Out-Null } catch {}

$script:ok = 0; $script:warn = 0; $script:fail = 0
function Say($t)  { Write-Host $t }
function Good($t) { $script:ok++;   Write-Host "  ok    $t" }
function Note($t) { $script:warn++; Write-Host "  note  $t" -ForegroundColor Yellow }
function Bad($t)  { $script:fail++; Write-Host "  FAIL  $t" -ForegroundColor Red }
function Finish($code) { try { Stop-Transcript | Out-Null } catch {}; exit $code }

function Write-Utf8($path, $text) {
  # UTF-8 without BOM: Windows PowerShell 5.1 adds a BOM, and Python's json.load refuses it
  [System.IO.File]::WriteAllText($path, $text, (New-Object System.Text.UTF8Encoding $false))
}
function Refresh-Path {
  # add what an installer just put in the registry; keep what this session already has
  $parts = @($env:Path -split ";" | Where-Object { $_ })
  $saved = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
  foreach ($p in ($saved -split ";")) { if ($p -and ($parts -notcontains $p)) { $parts += $p } }
  $env:Path = $parts -join ";"
  $local = Join-Path $HOME ".local\bin"
  if ((Test-Path $local) -and ($env:Path -notlike "*$local*")) { $env:Path = "$local;$env:Path" }
}
function Ask($question) {
  if ($Yes) { return $true }
  $a = Read-Host "$question [Y/n]"
  return ($a -eq "" -or $a -match "^[Yy]")
}
# programs only: a function or alias of the same name must not count
function Has($cmd) { return [bool](Get-Command $cmd -CommandType Application, ExternalScript -ErrorAction SilentlyContinue) }
function Install-Winget($id, $what, $extra) {
  if (-not (Has "winget")) { Bad "$what is missing and winget is not available: install $what by hand, then run this again"; return $false }
  if (-not (Ask "  $what is missing. Install it now with winget?")) { Bad "$what is missing"; return $false }
  $wargs = @("install", "--id", $id, "-e", "--source", "winget", "--accept-package-agreements", "--accept-source-agreements") + $extra
  & winget @wargs
  Refresh-Path
  return ($LASTEXITCODE -eq 0)
}

# Python: the py launcher or python; python3 on Windows is often a Microsoft Store stub.
$script:PyExe = $null; $script:PyArgs = @()
function Find-Python {
  foreach ($c in @("py -3", "python", "python3")) {
    $parts = $c -split " "
    if (-not (Has $parts[0])) { continue }
    $rest = @($parts | Select-Object -Skip 1)
    & $parts[0] @rest -c "import sys; sys.exit(sys.version_info < (3, 9))" 2>&1 | Out-Null
    if ($LASTEXITCODE -eq 0) { $script:PyExe = $parts[0]; $script:PyArgs = $rest; return $true }
  }
  return $false
}
# stderr merged here as plain text: Windows PowerShell 5.1 turns a native program's
# stderr into error records, which print as red errors (or stop a strict caller)
function Invoke-Py { & $script:PyExe @script:PyArgs -I @args 2>&1 | ForEach-Object { "$_" } }

Say "== 1/7 Tools on this computer"
if (-not (Has "git")) { [void](Install-Winget "Git.Git" "Git" @()) }
if (-not (Has "git")) { Bad "Git is still not found: install it from https://git-scm.com/download/win, reopen PowerShell, run this again"; Finish 1 }
Good ("git " + ((git --version) -replace "git version ", ""))
if (-not (Find-Python)) {
  [void](Install-Winget "Python.Python.3.13" "Python 3" @("--override", "/quiet InstallAllUsers=0 PrependPath=1 Include_launcher=1 Include_test=0"))
  [void](Find-Python)
}
if (-not $script:PyExe) { Bad "Python 3.9+ is still not found: install it from https://www.python.org/downloads/ (tick 'Add python.exe to PATH'), reopen PowerShell, run this again"; Finish 1 }
Good ("python " + (& $script:PyExe @script:PyArgs -c "import platform; print(platform.python_version())") + " (as '" + (($script:PyExe + " " + ($script:PyArgs -join " ")).Trim()) + "')")
Refresh-Path
if (-not (Has "claude")) {
  if (Ask "  Claude Code is missing. Install it now (official installer from claude.ai)?") {
    # in a child scope: the installer sets $ErrorActionPreference = 'Stop', which would
    # otherwise stay in this script and turn any later warning into a fatal error
    & { Invoke-RestMethod https://claude.ai/install.ps1 | Invoke-Expression }
    $ErrorActionPreference = "Continue"
    Refresh-Path
  }
}
$HasClaude = Has "claude"
# The Claude Code installer leaves ~\.local\bin out of PATH and asks you to add it by hand
$local = Join-Path $HOME ".local\bin"
if (Test-Path (Join-Path $local "claude.exe")) {
  $userPath = [Environment]::GetEnvironmentVariable("Path", "User")
  if (-not $userPath) { $userPath = "" }
  if (($userPath -split ";") -notcontains $local) {
    [Environment]::SetEnvironmentVariable("Path", (($userPath.TrimEnd(";") + ";" + $local).TrimStart(";")), "User")
    Good "added $local to your PATH (takes effect in new windows)"
  }
}
if ($HasClaude) { Good ("Claude Code " + ((claude --version 2>&1 | Out-String).Trim() -split " ")[0]) }
else { Note "Claude Code not found: install it with  irm https://claude.ai/install.ps1 | iex  then reopen PowerShell and run this again for the plugin step" }

Say "== 2/7 The kit"
if ($PSScriptRoot -and (Test-Path (Join-Path $PSScriptRoot "scripts\leak_check.py"))) {
  $Kit = $PSScriptRoot; Good "using the kit at $Kit"
} else {
  $Kit = $env:WIKI_KIT_DIR; if (-not $Kit) { $Kit = Join-Path $HOME "Projects\wiki-kit" }
  if (Test-Path (Join-Path $Kit ".git")) { git -C $Kit pull -q --ff-only; Good "updated $Kit" }
  elseif (-not $env:WIKI_KIT_REPO) { Bad "no kit here: clone it first (git clone <address you were sent> $HOME\Projects\wiki-kit) or set WIKI_KIT_REPO"; Finish 1 }
  else {
    New-Item -ItemType Directory -Force -Path (Split-Path $Kit) | Out-Null
    git clone -q $env:WIKI_KIT_REPO $Kit
    if ($LASTEXITCODE -ne 0) { Bad "git clone failed"; Finish 1 }
    Good "cloned into $Kit"
  }
}
git -C $Kit config core.hooksPath hooks
if ($LASTEXITCODE -eq 0) { Good "kit hooks on (leak check before push, specialists re-sync)" }

Say "== 3/7 The llm-wiki plugin ($PluginId, pinned to v0.25.1)"
if ($NoPlugin -or -not $HasClaude) { Note "skipped" }
elseif ((claude plugin list --json 2>&1 | Out-String) -match [regex]::Escape("`"$PluginId`"")) { Good "already installed" }
else {
  if ((claude plugin marketplace list 2>&1 | Out-String) -notmatch "llm-wiki") { claude plugin marketplace add $PluginRepo 2>&1 | Out-Null }
  claude plugin install $PluginId 2>&1 | Out-Null
  if ($LASTEXITCODE -eq 0) { Good "installed" } else { Bad "plugin install failed: run 'claude plugin install $PluginId' and read the message" }
}

Say "== 4/7 Your hub (the folder with your wikis)"
$Config = Join-Path $HOME ".config\llm-wiki\config.json"
if (-not $Hub -and (Test-Path $Config)) {
  try { $Hub = (Get-Content $Config -Raw | ConvertFrom-Json).hub_path } catch { $Hub = "" }
}
$HubSetting = $Hub
if (-not $Hub) { $Hub = "~/wiki"; $HubSetting = "~/wiki" }
if ($Hub.StartsWith("~")) { $Hub = Join-Path $HOME $Hub.Substring(1).TrimStart("/", "\") }
$Hub = [System.IO.Path]::GetFullPath($Hub)
if (-not (Test-Path $Config)) {
  New-Item -ItemType Directory -Force -Path (Split-Path $Config) | Out-Null
  if (-not $HubSetting.StartsWith("~")) { $HubSetting = $Hub -replace "\\", "/" }
  Write-Utf8 $Config ('{"hub_path": "' + $HubSetting + '"}')
  Good "hub path saved in $Config"
}
if (-not $Lang) { $Lang = (Get-UICulture).TwoLetterISOLanguageName }
if ($Lang -eq "ru") { $Language = "Russian" } elseif ($Lang -eq "uk") { $Language = "Ukrainian" } else { $Language = "English" }
$today = Get-Date -Format "yyyy-MM-dd"
if (Test-Path (Join-Path $Hub "_index.md")) {
  Good "hub exists at $Hub (left as it is)"
} else {
  New-Item -ItemType Directory -Force -Path (Join-Path $Hub "topics") | Out-Null
  $f = Join-Path $Hub "wikis.json"
  if (-not (Test-Path $f)) { Write-Utf8 $f "{`n  `"default`": `"<HUB>`",`n  `"wikis`": {`n    `"hub`": {`"path`": `"<HUB>`", `"description`": `"Personal knowledge hub`"}`n  },`n  `"local_wikis`": []`n}`n" }
  Write-Utf8 (Join-Path $Hub "_index.md") ("# Wiki Hub`n`n> Personal knowledge base. Content lives in topic wikis.`n`nLast updated: $today`n`n## Topic Wikis`n`n" +
    "| Topic | Description | Sources | Articles |`n|-------|-------------|---------|----------|`n`n## Recent Changes`n`n- ${today}: Hub initialized (wiki-kit bootstrap.ps1)`n")
  $f = Join-Path $Hub "log.md"
  if (-not (Test-Path $f)) { Write-Utf8 $f "# Wiki Activity Log`n`n## [$today] init | Hub initialized by wiki-kit bootstrap.ps1`n" }
  $f = Join-Path $Hub "CLAUDE.md"
  if (-not (Test-Path $f)) {
    $t = [System.IO.File]::ReadAllText((Join-Path $Kit "templates\hub-CLAUDE.md"))
    Write-Utf8 $f ($t.Replace("{HUB_NAME}", "My wiki").Replace("{WIKI_LANGUAGE}", $Language).Replace("{CHAT_LANGUAGE}", $Language))
  }
  $f = Join-Path $Hub "README.md"
  if (-not (Test-Path $f)) { Write-Utf8 $f "# State and plan`n`nUpdated: $today. Empty hub created by wiki-kit bootstrap.ps1. Next: create the first topic with ``/wiki init <topic>``.`n" }
  $f = Join-Path $Hub ".gitignore"
  if (-not (Test-Path $f)) { Write-Utf8 $f (".DS_Store`n# files that must not leave this computer`n*.local.md`n.sessions/`ninbox/.processed/`n" +
    "# kit specialists in .skills/ are a cache of wiki-kit (sync_specialists.py);`n# only your own tuning (*.local.md) is history of this hub`n" +
    ".skills/*/SKILL.md`n.skills/*/references/*`n!.skills/*/references/*.local.md`n") }
  Good "empty hub created at $Hub (rules in $Language)"
}
if (-not (Test-Path (Join-Path $Hub ".git"))) {
  git -C $Hub init -q
  if ($LASTEXITCODE -eq 0) { Good "hub is a git repository (local only, no remote; the first commit comes with your first topic)" }
}

Say "== 5/7 Private lists (outside every repository)"
$Cfg = Join-Path $HOME ".config\wiki-kit"
New-Item -ItemType Directory -Force -Path $Cfg | Out-Null
$f = Join-Path $Cfg "private-names.txt"
if (-not (Test-Path $f)) { Write-Utf8 $f "# Names that must never reach the kit: your family, employer, clients.`n# One case-insensitive regex per line, for example: Acme Corp`n" }
$f = Join-Path $Cfg "internal-domains.txt"
if (-not (Test-Path $f)) { Write-Utf8 $f "# Internal host suffixes of your employer or clients, one per line, for example: corp.example.com`n" }
Good "$Cfg (fill private-names.txt before your first push to the kit)"

Say "== 6/7 Specialists and the front desk"
$LlmWiki = Get-ChildItem -Path (Join-Path $HOME ".claude\plugins\cache\llm-wiki\wiki\*\bin\llm-wiki") -ErrorAction SilentlyContinue |
  Sort-Object FullName | Select-Object -Last 1
function Lw { Invoke-Py $LlmWiki.FullName specialist --hub $Hub @args 2>&1 | Out-Null; return ($LASTEXITCODE -eq 0) }
if ($LlmWiki) {
  if (-not (Test-Path (Join-Path $Hub ".skills"))) { [void](Lw init) }
  $out = Invoke-Py (Join-Path $Kit "scripts\sync_specialists.py") $Hub 2>&1 | Select-Object -Last 1
  if ($LASTEXITCODE -eq 0) { Good "specialists: $out" } else { Bad "specialists: $out" }
  [void](Lw refresh)
} else { Note "specialists wait for the plugin: run this again after step 3 succeeds" }
$Skills = Join-Path $HOME ".claude\skills"
New-Item -ItemType Directory -Force -Path $Skills | Out-Null
$Desk = Join-Path $Skills "department"
if (Test-Path $Desk) { Good "front desk skill already present" }
else {
  # a junction needs no administrator rights, unlike a symbolic link
  New-Item -ItemType Junction -Path $Desk -Target (Join-Path $Kit "skills\department") | Out-Null
  if (Test-Path (Join-Path $Desk "SKILL.md")) { Good "front desk skill linked (say 'coach' or 'help me decide' in any folder)" }
  else { Bad "could not link $Desk to the kit's skills\department" }
}

Say "== 7/7 Self-check"
$broken = Invoke-Py -c "import sys`nfor f in sys.argv[1:]:`n    try: compile(open(f, encoding='utf-8').read(), f, 'exec')`n    except SyntaxError: print(f.replace(chr(92), '/').rsplit('/', 1)[-1], end=' ')" (Get-ChildItem (Join-Path $Kit "scripts\*.py") | ForEach-Object { $_.FullName })
if (-not $broken) { Good "all scripts compile on this Python" } else { Bad "scripts that need a newer Python: $broken" }
$sh = Join-Path (Split-Path (Split-Path (Get-Command git).Source)) "bin\sh.exe"
if (Test-Path $sh) {
  $found = & $sh -c ". '$($Kit -replace '\\', '/')/hooks/lib.sh'; echo `$py"
  if ($found) { Good "git hooks find Python ('$found')" } else { Bad "git hooks cannot find Python: reinstall Python with 'Add python.exe to PATH' ticked" }
} else { Note "Git's sh.exe not found next to git: hooks not checked" }
if (Test-Path (Join-Path $Hub ".skills")) {
  Invoke-Py (Join-Path $Kit "scripts\sync_specialists.py") $Hub --check 2>&1 | Out-Null
  if ($LASTEXITCODE -eq 0) { Good "hub specialists match the kit" } else { Bad "hub specialists differ from the kit" }
  if (Lw validate) { Good "specialists pass the plugin validator" } else { Bad "plugin validator failed: run  $($script:PyExe) $($script:PyArgs -join ' ') -I `"$($LlmWiki.FullName)`" specialist --hub `"$Hub`" validate" }
}
Invoke-Py (Join-Path $Kit "scripts\leak_check.py") --repo $Kit 2>&1 | Out-Null
if ($LASTEXITCODE -eq 0) { Good "kit passes the leak check" } else { Bad "kit fails the leak check: run  py -3 -I $Kit\scripts\leak_check.py --repo $Kit" }

Say ""
Say "Done: $($script:ok) ok, $($script:warn) note(s), $($script:fail) failure(s). Hub: $Hub"
Say "Next: open the hub folder in VS Code, start Claude Code, sign in, and type:  /wiki init personal"
Say "Guide: $Kit\docs\QUICKSTART.md (English), $Kit\docs\QUICKSTART.ru.md (Russian), $Kit\docs\QUICKSTART.uk.md (Ukrainian). Log: $Log"
if ($script:fail -eq 0) { Finish 0 } else { Finish 1 }
