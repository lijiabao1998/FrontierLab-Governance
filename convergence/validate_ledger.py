#!/usr/bin/env python3
"""Validate SESSION_LEDGER evidence locators: each referenced path must exist
at the referenced commit in its repo's local clone. Exit != 0 on any failure."""
import json, subprocess, sys
from pathlib import Path
WS = Path(__file__).resolve().parent.parent.parent  # workspace root
ledger = json.loads((Path(__file__).resolve().parent / "SESSION_LEDGER.json")
                    .read_text(encoding="utf-8"))
fail = False
for e in ledger["entries"]:
    repo = e["repo"]
    clone = WS / repo
    # Codex P2: missing clones are validation FAILURES, not skips — a clean
    # checkout or CI run must not report an unverified ledger as validated
    if not (clone / ".git").exists():
        print(f"FAIL {repo}: sibling clone missing (git clone "
              f"https://github.com/lijiabao1998/{repo}.git {clone})")
        fail = True
        continue
    for loc in e.get("evidence_paths", []):
        sha, path = loc["commit_sha"], loc["path"]
        if sha == "THIS_COMMIT":
            sha = "HEAD"
        if sha == "BRANCH_HEAD":
            # Codex P2: resolve from the ledger's recorded immutable
            # current_head_sha — never from whatever branch the local clone
            # happens to be on
            sha = e.get("current_head_sha") or sha
        r = subprocess.run(["git", "-C", str(clone), "cat-file", "-e",
                            f"{sha}:{path}"], capture_output=True, text=True)
        ok = r.returncode == 0
        print(f"{'OK ' if ok else 'FAIL'} {repo} {sha[:8]}:{path}")
        if not ok:
            fail = True
sys.exit(1 if fail else 0)
