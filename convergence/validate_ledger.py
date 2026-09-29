#!/usr/bin/env python3
"""Check evidence files at immutable commits; missing repositories fail closed.

This validates provenance locations, not scientific content or review freshness.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys

SHA = re.compile(r"[0-9a-f]{40}\Z")
REPO = re.compile(r"Frontier[A-Za-z]+(?:-Governance)?\Z")


def validate(data: dict, workspace: Path) -> list[str]:
    errors = []
    entries = data.get("entries")
    if not isinstance(entries, list) or not entries:
        return ["ledger must contain nonempty entries"]
    for entry in entries:
        repo = entry.get("repo", "")
        if not isinstance(repo, str) or not REPO.fullmatch(repo):
            errors.append(f"invalid repository: {repo!r}")
            continue
        head = entry.get("current_head_sha", "")
        if not isinstance(head, str) or not SHA.fullmatch(head):
            errors.append(f"{repo}: current_head_sha must be a full immutable SHA")
            continue
        if entry.get("work_status") == "READY_FOR_OWNER_REVIEW":
            if (entry.get("last_reviewed_sha") != head
                    or entry.get("live_P1") != 0 or entry.get("live_P2") != 0
                    or entry.get("ci_state") != "GREEN"):
                errors.append(f"{repo}: READY requires current-head review, zero P1/P2 and green CI")
        clone = workspace / repo
        probe = subprocess.run(["git", "-c", "core.quotepath=false", "-C", str(clone),
                                "rev-parse", "--show-toplevel"],
                               capture_output=True, text=True, encoding="utf-8")
        if probe.returncode or Path(probe.stdout.strip()).resolve() != clone.resolve():
            errors.append(f"{repo}: missing local repository (validation incomplete)")
            continue
        locations = entry.get("evidence_paths")
        if not isinstance(locations, list) or not locations:
            errors.append(f"{repo}: no evidence locators")
            continue
        for loc in locations:
            source = loc.get("repo", "")
            sha = loc.get("commit_sha", "")
            if sha == "BRANCH_HEAD":
                sha = head
            path = loc.get("path", "")
            if (source not in (repo, f"lijiabao1998/{repo}")
                    or not isinstance(sha, str) or not SHA.fullmatch(sha)
                    or not isinstance(path, str) or not path
                    or PurePosixPath(path).is_absolute()
                    or ".." in PurePosixPath(path).parts or "\\" in path or ":" in path):
                errors.append(f"{repo}: invalid immutable locator {loc!r}")
                continue
            result = subprocess.run(["git", "-C", str(clone), "cat-file", "-t", f"{sha}:{path}"],
                                    capture_output=True, text=True, encoding="utf-8")
            if result.returncode or result.stdout.strip() != "blob":
                errors.append(f"{repo}: missing file at {sha}:{path}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--ledger", type=Path,
                        default=Path(__file__).with_name("SESSION_LEDGER.json"))
    args = parser.parse_args()
    try:
        errors = validate(json.loads(args.ledger.read_text(encoding="utf-8")), args.workspace)
    except (OSError, ValueError, TypeError, AttributeError) as exc:
        errors = [f"invalid/unreadable ledger: {exc}"]
    for error in errors:
        print(f"FAIL {error}")
    if not errors:
        print("PASS: evidence files exist at immutable commits; content not verified")
    return int(bool(errors))


if __name__ == "__main__":
    sys.exit(main())
