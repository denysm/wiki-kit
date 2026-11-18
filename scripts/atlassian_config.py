"""Hosts and credentials for atlassian_export.py and confluence_publish.py (Confluence and Jira
Server/Data Center REST API with personal access tokens). No host is built in.

Each setting comes from, first match wins: a command-line flag, an environment variable, a
profile in ~/.config/wiki-kit/atlassian.json (outside every repository; hosts and Keychain item
names only, never tokens; WIKI_KIT_ATLASSIAN_CONFIG names another file):

  {"default": "work",
   "profiles": {"work": {"confluence_url": "https://kb.example.com",
                         "jira_url": "https://issues.example.com",
                         "confluence_keychain": "work-confluence",
                         "jira_keychain": "work-jira",
                         "confluence_title_suffix": " (Example wiki)"}}}

Environment: ATLASSIAN_PROFILE picks the profile; CONFLUENCE_URL, JIRA_URL, CONFLUENCE_KEYCHAIN,
JIRA_KEYCHAIN and CONFLUENCE_TITLE_SUFFIX override its fields. confluence_title_suffix is
appended to exported page titles (default: none).

Tokens: CONFLUENCE_TOKEN / JIRA_TOKEN when set, otherwise the macOS Keychain item named by
confluence_keychain / jira_keychain (default "confluence" / "jira"), added once with
  security add-generic-password -s <item> -a "$USER" -w     # paste the token
"""
import json, os, subprocess, sys

KEYS = ("confluence_url", "jira_url", "confluence_keychain", "jira_keychain", "confluence_title_suffix")
DEFAULTS = {"confluence_keychain": "confluence", "jira_keychain": "jira", "confluence_title_suffix": ""}
PATH = os.environ.get("WIKI_KIT_ATLASSIAN_CONFIG") or os.path.expanduser("~/.config/wiki-kit/atlassian.json")
_TOKENS = {}


def settings(profile=None, **flags):
    """Merge flags, environment and the profile; flags with value None are ignored."""
    cfg = {}
    if os.path.exists(PATH):
        with open(PATH, encoding="utf-8") as f:
            cfg = json.load(f)
    profiles = cfg.get("profiles", {})
    name = profile or os.environ.get("ATLASSIAN_PROFILE") or cfg.get("default")
    if not name and len(profiles) == 1:
        name = next(iter(profiles))
    if name and name not in profiles:
        sys.exit(f"no profile '{name}' in {PATH}")
    prof = profiles.get(name, {}) if name else {}
    out = {}
    for k in KEYS:
        v = flags.get(k)
        if v is None:
            v = os.environ.get(k.upper())
        if v is None:
            v = prof.get(k, DEFAULTS.get(k, ""))
        out[k] = v.rstrip("/") if k.endswith("_url") else v
    return out


def require(cfg, key):
    if not cfg.get(key):
        sys.exit(f"no {key}: pass --{key.replace('_', '-')}, set {key.upper()} or add it to a profile in {PATH}")
    return cfg[key]


def token(system, cfg):
    """Personal access token for 'confluence' or 'jira': environment first, then the Keychain."""
    if system not in _TOKENS:
        env = os.environ.get(f"{system.upper()}_TOKEN")
        if env:
            _TOKENS[system] = env
        else:
            item = cfg[f"{system}_keychain"]
            try:
                _TOKENS[system] = subprocess.run(["security", "find-generic-password", "-s", item, "-w"],
                                                 capture_output=True, text=True, check=True).stdout.strip()
            except (OSError, subprocess.CalledProcessError):
                sys.exit(f"no {system.upper()}_TOKEN and no Keychain item '{item}'; add it with: "
                         f"security add-generic-password -s {item} -a \"$USER\" -w")
    return _TOKENS[system]


def inside_wiki(path):
    """True when path (existing or not) lies in a wiki: a hub (wikis.json), a repository with
    .wiki/, a .wiki/ folder or a topic root (raw/ next to wiki/)."""
    d = os.path.realpath(os.path.expanduser(path))
    while True:
        if (os.path.basename(d) == ".wiki" or os.path.exists(os.path.join(d, "wikis.json"))
                or os.path.isdir(os.path.join(d, ".wiki"))
                or (os.path.isdir(os.path.join(d, "raw")) and os.path.isdir(os.path.join(d, "wiki")))):
            return True
        parent = os.path.dirname(d)
        if parent == d:
            return False
        d = parent
