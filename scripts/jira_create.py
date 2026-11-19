#!/usr/bin/env python3
"""Create a Jira issue (Server/Data Center REST API v2, personal access token) and find users.

Dry run unless --apply: prints the request it would send. Host and token come from
atlassian_config.py (flag, environment, or a profile in ~/.config/wiki-kit/atlassian.json;
token from JIRA_TOKEN or the Keychain). No host is built in.

  jira_create.py user "Surname"                      # name (use it for --assignee), display name, e-mail
  jira_create.py create --project KEY --summary "..." --description-file desc.txt \\
      [--type Task] [--priority Medium] [--label L ...] [--assignee NAME] [--relates KEY-1 ...] [--apply]

The description file is Jira wiki markup. A custom User-Agent is always sent: some hosts sit
behind Cloudflare, which refuses the default Python-urllib one with HTTP 403.
"""
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import atlassian_config  # noqa: E402

UA = "wiki-kit-jira/1.0"


def call(cfg, method, path, body=None, **params):
    url = atlassian_config.require(cfg, "jira_url") + path
    if params:
        url += "?" + urllib.parse.urlencode(params)
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {atlassian_config.token('jira', cfg)}",
        "Accept": "application/json", "Content-Type": "application/json", "User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:500]
        sys.exit(f"HTTP {e.code} {method} {path}: {detail}")


def users(cfg, query):
    found = call(cfg, "GET", "/rest/api/2/user/search", username=query, maxResults=20)
    for u in found:
        print(f"{u.get('name')}\t{u.get('displayName')}\t{u.get('emailAddress', '')}")
    if not found:
        print("no users found", file=sys.stderr)
        return 1
    return 0


def create(cfg, a):
    with open(a.description_file, encoding="utf-8") as f:
        description = f.read().strip()
    fields = {"project": {"key": a.project}, "issuetype": {"name": a.type}, "summary": a.summary,
              "description": description, "priority": {"name": a.priority}}
    if a.label:
        fields["labels"] = a.label
    if a.assignee:
        fields["assignee"] = {"name": a.assignee}
    if not a.apply:
        print(json.dumps({"fields": fields}, ensure_ascii=False, indent=2))
        for k in a.relates:
            print(f"then link: Relates {k}")
        print("dry run: nothing created; add --apply")
        return 0
    issue = call(cfg, "POST", "/rest/api/2/issue", {"fields": fields})
    key = issue["key"]
    for k in a.relates:
        call(cfg, "POST", "/rest/api/2/issueLink",
             {"type": {"name": "Relates"}, "inwardIssue": {"key": key}, "outwardIssue": {"key": k}})
    print(f"{key}\t{cfg['jira_url']}/browse/{key}")
    return 0


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--profile")
    p.add_argument("--jira-url")
    sub = p.add_subparsers(dest="cmd", required=True)
    u = sub.add_parser("user", help="find users by name or e-mail")
    u.add_argument("query")
    c = sub.add_parser("create", help="create an issue (dry run unless --apply)")
    c.add_argument("--project", required=True)
    c.add_argument("--summary", required=True)
    c.add_argument("--description-file", required=True)
    c.add_argument("--type", default="Task")
    c.add_argument("--priority", default="Medium")
    c.add_argument("--label", action="append", default=[])
    c.add_argument("--assignee", help="Jira user name (see the user command)")
    c.add_argument("--relates", action="append", default=[], help="issue key to link with Relates")
    c.add_argument("--apply", action="store_true")
    a = p.parse_args()
    cfg = atlassian_config.settings(a.profile, jira_url=a.jira_url)
    return users(cfg, a.query) if a.cmd == "user" else create(cfg, a)


if __name__ == "__main__":
    sys.exit(main())
