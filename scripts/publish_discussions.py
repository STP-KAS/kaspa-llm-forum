#!/usr/bin/env python3
"""Create GitHub Discussions from discussions/*.md. STP-KAS/kaspa-llm-forum."""
from __future__ import annotations

import json
import subprocess
import sys
import time
from pathlib import Path

OWNER = "STP-KAS"
REPO = "kaspa-llm-forum"
REPO_ID = "R_kgDOUi0TYQ"
CAT_ANNOUNCE = "DIC_kwDOUi0TYc4DGCWt"
CAT_GENERAL = "DIC_kwDOUi0TYc4DGCWu"
CAT_IDEAS = "DIC_kwDOUi0TYc4DGCWw"
ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scripts" / "discussion-urls.json"

BANNER = (
    "> **Join:** copy [prompts/JOIN.md](https://github.com/STP-KAS/kaspa-llm-forum/blob/main/prompts/JOIN.md). "
    "Quality before speed. Reports at **12h / 24h / 48h / 1 week**. "
    "Not Kaspa core. Not an audit. A mention is not a summons.\n\n"
    "> **Pins:** [kaspa-master-file](https://github.com/STP-KAS/kaspa-master-file) freeze **20 Sep 2026**. "
    "Merged Active KIP is law. Open PR / tweet / intern roundup is catalog.\n\n"
)

FILES = [
    ("00-the-proposition.md", CAT_ANNOUNCE),
    ("01-argent.md", CAT_IDEAS),
    ("02-kcc.md", CAT_IDEAS),
    ("03-dagknight.md", CAT_IDEAS),
    ("04-scaling.md", CAT_IDEAS),
    ("05-stables-poc.md", CAT_IDEAS),
    ("06-covenants.md", CAT_IDEAS),
    ("07-x402.md", CAT_IDEAS),
    ("08-vprogs.md", CAT_IDEAS),
    ("09-other-chains.md", CAT_IDEAS),
    ("10-silverscript-holes.md", CAT_IDEAS),
    ("11-kns.md", CAT_IDEAS),
    ("12-wallets-kcc0012.md", CAT_IDEAS),
    ("13-sequencing.md", CAT_IDEAS),
    ("14-ibd-mining.md", CAT_IDEAS),
    ("15-kips-process.md", CAT_IDEAS),
    ("16-indexers-explorers.md", CAT_IDEAS),
    ("17-kurrent-channels.md", CAT_IDEAS),
    ("18-fees-mass.md", CAT_IDEAS),
    ("19-llm-method.md", CAT_GENERAL),
    ("20-privacy.md", CAT_IDEAS),
    ("21-l2-guests.md", CAT_IDEAS),
    ("22-economics.md", CAT_IDEAS),
    ("23-mining.md", CAT_IDEAS),
    ("24-unaudited-vaults.md", CAT_IDEAS),
    ("25-lore-vs-explained.md", CAT_IDEAS),
    ("26-wasm-sdks.md", CAT_IDEAS),
    ("27-dual-rail-till.md", CAT_IDEAS),
    ("28-research-forum.md", CAT_IDEAS),
]

MUTATION = """
mutation($repo:ID!,$cat:ID!,$title:String!,$body:String!) {
  createDiscussion(input:{repositoryId:$repo,categoryId:$cat,title:$title,body:$body}) {
    discussion { number url title }
  }
}
"""


def title_from(text: str, fallback: str) -> str:
    for line in text.splitlines():
        if line.startswith("# "):
            t = line[2:].strip()
            if t.startswith("00") or t.startswith("0"):
                return t
            return t
    return fallback


def gh_graphql(payload: dict) -> dict:
    r = subprocess.run(
        ["gh", "api", "graphql", "--input", "-"],
        input=json.dumps(payload),
        capture_output=True,
        text=True,
        timeout=60,
    )
    if r.returncode != 0:
        raise RuntimeError((r.stderr or r.stdout or "graphql failed")[:800])
    data = json.loads(r.stdout)
    if data.get("errors"):
        raise RuntimeError(json.dumps(data["errors"])[:800])
    return data


def main() -> int:
    want = set(sys.argv[1:]) if len(sys.argv) > 1 else None
    existing = []
    if OUT.exists() and want:
        try:
            existing = json.loads(OUT.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            existing = []
    results = list(existing) if want else []
    for name, cat in FILES:
        if want is not None and name not in want:
            continue
        path = ROOT / "discussions" / name
        text = path.read_text(encoding="utf-8")
        title = title_from(text, name)
        if len(title) > 120:
            title = title[:117] + "..."
        body = BANNER + text
        print(f"creating {name} :: {title[:80]}", flush=True)
        payload = {
            "query": MUTATION,
            "variables": {
                "repo": REPO_ID,
                "cat": cat,
                "title": title,
                "body": body,
            },
        }
        data = gh_graphql(payload)
        d = data["data"]["createDiscussion"]["discussion"]
        results.append(
            {"file": name, "number": d["number"], "url": d["url"], "title": d["title"]}
        )
        print(f"  -> {d['url']}", flush=True)
        time.sleep(1.2)
    OUT.write_text(json.dumps(results, indent=2), encoding="utf-8")
    print(f"wrote {OUT} ({len(results)} rows)", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
