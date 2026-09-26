"""Watch STP-KAS/kaspa-llm-forum issues + discussions for new comments.

Silent unless a new non-own comment needs a Grok Build auto-reply.
Prints ACTION_REQUIRED so the Grok Build monitor can wake and reply.
Replies MUST start with: Auto-reply from Grok Build
"""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

OWNER = "STP-KAS"
REPO = "kaspa-llm-forum"
POLL = 30
DIR = Path.home() / ".grok" / "long-running-background-tasks"
LOG = DIR / "watch_kaspa_llm_forum.log"
STATE = DIR / "watch_kaspa_llm_forum.state"
OWN_USERS = {"STP-KAS"}
OWN_MARKERS = (
    "Auto-reply from Grok Build",
    "Grok Build here (Windows desk)",
    "Independent **Grok Build** check",
    "Grok Build (Windows desk)",
)


def dbg(msg: str) -> None:
    DIR.mkdir(parents=True, exist_ok=True)
    line = time.strftime("%Y-%m-%dT%H:%M:%S ") + msg
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")


def gh_json(path: str):
    r = subprocess.run(
        ["gh", "api", path],
        capture_output=True,
        text=True,
        timeout=45,
    )
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout or "gh api failed").strip()[:400])
    return json.loads(r.stdout)


def gh_graphql(query: str, variables: dict | None = None):
    payload = {"query": query, "variables": variables or {}}
    r = subprocess.run(
        ["gh", "api", "graphql", "--input", "-"],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=45,
    )
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout or "graphql failed").strip()[:400])
    return json.loads(r.stdout)


def load_state() -> dict:
    if STATE.exists():
        try:
            return json.loads(STATE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            pass
    return {
        "issue_comments": {},
        "discussion_comments": {},
        "known_discussions": [],
        "known_issues": [],
    }


def save_state(st: dict) -> None:
    STATE.write_text(json.dumps(st, indent=2), encoding="utf-8")


def is_own(body: str, user: str) -> bool:
    if user in OWN_USERS:
        return True
    return any(m in (body or "") for m in OWN_MARKERS)


def oneline(s: str, n: int = 180) -> str:
    t = " ".join((s or "").split())
    return t if len(t) <= n else t[: n - 1] + "…"


ISSUE_LIST = f"repos/{OWNER}/{REPO}/issues?state=open&per_page=50"
ISSUE_COMMENTS = "repos/{owner}/{repo}/issues/{n}/comments?per_page=100"

GQL_DISCUSSIONS = """
query($owner: String!, $repo: String!) {
  repository(owner: $owner, name: $repo) {
    discussions(first: 50) {
      nodes { number title url }
    }
  }
}
"""

GQL_D_COMMENTS = """
query($owner: String!, $repo: String!, $n: Int!) {
  repository(owner: $owner, name: $repo) {
    discussion(number: $n) {
      comments(first: 50) {
        nodes { id databaseId author { login } body url createdAt }
      }
    }
  }
}
"""


def main() -> int:
    st = load_state()
    fails = 0
    dbg("watch start")
    while True:
        try:
            issues = gh_json(ISSUE_LIST)
            d = gh_graphql(GQL_DISCUSSIONS, {"owner": OWNER, "repo": REPO})
            discs = (
                (((d.get("data") or {}).get("repository") or {}).get("discussions") or {}).get(
                    "nodes"
                )
                or []
            )
            fails = 0
        except Exception as e:
            fails += 1
            dbg(f"poll error {fails}: {e}")
            if fails >= 8:
                print(f"FAILED: cannot read {OWNER}/{REPO}: {e}")
                return 1
            time.sleep(min(120, POLL * fails))
            continue

        for iss in issues:
            if iss.get("pull_request"):
                continue
            n = int(iss["number"])
            nkey = str(n)
            last = int(st["issue_comments"].get(nkey, 0))
            try:
                comments = gh_json(
                    ISSUE_COMMENTS.format(owner=OWNER, repo=REPO, n=n)
                )
            except Exception as e:
                dbg(f"issue {n} comments error: {e}")
                continue
            new = [c for c in comments if int(c.get("id") or 0) > last]
            new.sort(key=lambda c: int(c.get("id") or 0))
            if not new and nkey not in st["issue_comments"]:
                # first sight: do not replay history
                ids = [int(c.get("id") or 0) for c in comments]
                st["issue_comments"][nkey] = max(ids) if ids else 0
                save_state(st)
                continue
            for c in new:
                cid = int(c["id"])
                st["issue_comments"][nkey] = cid
                save_state(st)
                body = c.get("body") or ""
                user = (c.get("user") or {}).get("login") or "?"
                if is_own(body, user):
                    dbg(f"skip own issue {n} {cid}")
                    continue
                url = c.get("html_url") or ""
                print(
                    "ACTION_REQUIRED: "
                    f"issue {n} comment {cid} by {user} {url} :: {oneline(body)}"
                )
                dbg(f"wake issue {n} {cid} {user}")

        for disc in discs:
            n = int(disc["number"])
            nkey = str(n)
            last = int(st["discussion_comments"].get(nkey, 0))
            try:
                raw = gh_graphql(
                    GQL_D_COMMENTS, {"owner": OWNER, "repo": REPO, "n": n}
                )
            except Exception as e:
                dbg(f"discussion {n} comments error: {e}")
                continue
            nodes = (
                ((((raw.get("data") or {}).get("repository") or {}).get("discussion") or {}).get(
                    "comments"
                )
                or {}).get("nodes")
                or []
            )
            new = [c for c in nodes if int(c.get("databaseId") or 0) > last]
            new.sort(key=lambda c: int(c.get("databaseId") or 0))
            if not new and nkey not in st["discussion_comments"]:
                ids = [int(c.get("databaseId") or 0) for c in nodes]
                st["discussion_comments"][nkey] = max(ids) if ids else 0
                save_state(st)
                continue
            for c in new:
                cid = int(c.get("databaseId") or 0)
                st["discussion_comments"][nkey] = cid
                save_state(st)
                body = c.get("body") or ""
                user = ((c.get("author") or {}).get("login")) or "?"
                if is_own(body, user):
                    dbg(f"skip own disc {n} {cid}")
                    continue
                url = c.get("url") or ""
                print(
                    "ACTION_REQUIRED: "
                    f"discussion {n} comment {cid} by {user} {url} :: {oneline(body)}"
                )
                dbg(f"wake disc {n} {cid} {user}")

        time.sleep(POLL)


if __name__ == "__main__":
    sys.exit(main())
