#!/usr/bin/env python3
"""Show or change who an issue notifies: reporter and watchers.

    jira_people.py --profile PROFILE show KEY-1 KEY-2
    jira_people.py --profile PROFILE set KEY-1 KEY-2 --reporter jdoe \
        --add-watcher jdoe --remove-watcher me [--apply]

Without --apply it prints the plan only. With --apply it writes, then reads
each issue back and prints the result. Host and token come from
atlassian_config.py, as in jira_create.py. Changing the reporter needs the
Modify Reporter permission in the project. Standard library only.
"""
import argparse
import sys

from jira_create import call
import atlassian_config


def state(cfg, key):
    f = call(cfg, "GET", f"/rest/api/2/issue/{key}", fields="reporter,assignee,summary")["fields"]
    w = call(cfg, "GET", f"/rest/api/2/issue/{key}/watchers").get("watchers", [])
    name = lambda u: u.get("name") if u else "-"
    return {"reporter": name(f.get("reporter")), "assignee": name(f.get("assignee")),
            "watchers": sorted(u.get("name") for u in w), "summary": f.get("summary", "")}


def show(cfg, key):
    s = state(cfg, key)
    print(f"{key}\treporter={s['reporter']}\tassignee={s['assignee']}\t"
          f"watchers={','.join(s['watchers']) or '-'}\t{s['summary'][:60]}")
    return s


def apply_one(cfg, key, a):
    if a.reporter:
        call(cfg, "PUT", f"/rest/api/2/issue/{key}", {"fields": {"reporter": {"name": a.reporter}}})
    for u in a.add_watcher:
        call(cfg, "POST", f"/rest/api/2/issue/{key}/watchers", u)
    for u in a.remove_watcher:
        call(cfg, "DELETE", f"/rest/api/2/issue/{key}/watchers", username=u)


def main():
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--profile")
    p.add_argument("--jira-url")
    sub = p.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("show")
    s.add_argument("keys", nargs="+")
    c = sub.add_parser("set")
    c.add_argument("keys", nargs="+")
    c.add_argument("--reporter")
    c.add_argument("--add-watcher", action="append", default=[])
    c.add_argument("--remove-watcher", action="append", default=[])
    c.add_argument("--apply", action="store_true")
    a = p.parse_args()
    cfg = atlassian_config.settings(a.profile, jira_url=a.jira_url)
    for key in a.keys:
        if a.cmd == "show":
            show(cfg, key)
            continue
        before = show(cfg, key)
        print(f"  plan: reporter {before['reporter']} -> {a.reporter or 'unchanged'}; "
              f"add {a.add_watcher or '-'}; remove {a.remove_watcher or '-'}")
        if a.apply:
            apply_one(cfg, key, a)
            print("  after:", end=" ")
            show(cfg, key)
    if a.cmd == "set" and not a.apply:
        print("dry run: nothing written; add --apply")
    return 0


if __name__ == "__main__":
    sys.exit(main())
