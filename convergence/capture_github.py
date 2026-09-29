#!/usr/bin/env python3
"""Read GitHub into an append-only acquisition directory and render current status.

No repository writes, comments, review requests or merges are sent to GitHub.
Missing current-head review always remains REVIEW_REQUIRED. Historic unresolved
threads are reported separately, because line anchoring can move after a push.
"""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
import re
import subprocess

HERE = Path(__file__).resolve().parent
REPOS = ["Frontier" + x for x in (
    "Math", "Physics", "Biology", "Chemistry", "Lab-Governance", "ComputerScience",
    "Statistics", "Materials", "Astronomy", "Earth", "Neuroscience", "Economics",
    "Engineering", "Medicine", "SocialScience", "MetaScience")]
QUERY = '''query($name:String!){repository(owner:"lijiabao1998",name:$name){
 name defaultBranchRef{name target{oid}}
 pullRequests(first:50,states:[OPEN,CLOSED,MERGED],orderBy:{field:UPDATED_AT,direction:DESC}){
 pageInfo{hasNextPage} nodes{
 number title url state isDraft headRefName headRefOid baseRefName mergedAt
 mergeCommit{oid} updatedAt reviewDecision
 commits(last:1){nodes{commit{statusCheckRollup{state contexts(first:100){pageInfo{hasNextPage}
 nodes{... on CheckRun{name status conclusion detailsUrl} ... on StatusContext{context state targetUrl}}}}}}}
 reviews(last:50){pageInfo{hasPreviousPage} nodes{id state submittedAt url body commit{oid} author{login}}}
 reviewThreads(first:100){pageInfo{hasNextPage} nodes{isResolved isOutdated
 comments(first:1){nodes{url body createdAt pullRequestReview{id commit{oid}}}}}}
 }}}}'''


def now():
    return datetime.now(timezone.utc).isoformat()


def capture(repo):
    started = now()
    result = subprocess.run(["gh", "api", "graphql", "-f", "query=" + QUERY,
                             "-f", "name=" + repo], capture_output=True, text=True,
                            encoding="utf-8", timeout=90)
    if result.returncode:
        raise RuntimeError(f"{repo}: GitHub request failed: {result.stderr}")
    body = json.loads(result.stdout)
    if body.get("errors"):
        raise RuntimeError(f"{repo}: GraphQL errors: {body['errors']}")
    return {"acquired_started_at": started, "acquired_completed_at": now(),
            "repository": repo, "response": body}


def summarise(raw):
    repo = raw["repository"]
    data = raw["response"]["data"]["repository"]
    if not data or data["pullRequests"]["pageInfo"]["hasNextPage"]:
        raise ValueError(f"{repo}: incomplete repository/PR inventory")
    rows = []
    for pr in data["pullRequests"]["nodes"]:
        head = pr["headRefOid"]
        reviews = pr["reviews"]["nodes"]
        current = [r for r in reviews if r.get("commit", {}).get("oid") == head]
        counts = {"P1": 0, "P2": 0}
        historic = 0
        findings = []
        for thread in pr["reviewThreads"]["nodes"]:
            if thread["isResolved"]:
                continue
            for c in thread["comments"]["nodes"]:
                review_sha = ((c.get("pullRequestReview") or {}).get("commit") or {}).get("oid")
                match = re.search(r"\b(P[12]) Badge\b", c["body"])
                if review_sha == head and match:
                    counts[match[1]] += 1
                    findings.append({"priority": match[1], "url": c["url"],
                                     "text": c["body"], "is_outdated": thread["isOutdated"]})
                elif not thread["isOutdated"]:
                    historic += 1
        commits = pr["commits"]["nodes"]
        checks = commits[-1]["commit"].get("statusCheckRollup") if commits else None
        complete = not (pr["reviews"]["pageInfo"]["hasPreviousPage"]
                        or pr["reviewThreads"]["pageInfo"]["hasNextPage"]
                        or (checks and checks["contexts"]["pageInfo"]["hasNextPage"]))
        verdict = (pr["state"] if pr["state"] != "OPEN" else
                   "DRAFT" if pr["isDraft"] else
                   "HOLD_INCOMPLETE_API" if not complete else
                   "HOLD_FINDINGS" if counts["P1"] or counts["P2"] else "REVIEW_REQUIRED")
        rows.append({"repo": repo, "pr": pr["number"], "url": pr["url"],
                     "head_sha": head, "base_branch": pr["baseRefName"], "state": pr["state"],
                     "merge_sha": (pr.get("mergeCommit") or {}).get("oid"),
                     "merged_at": pr["mergedAt"], "ci": checks["state"] if checks else "UNKNOWN",
                     "current_head_reviews": [r["url"] for r in current],
                     "current_head_P1": counts["P1"], "current_head_P2": counts["P2"],
                     "historical_unresolved_nonoutdated_threads": historic,
                     "findings": findings, "api_complete": complete, "verdict": verdict})
    return rows


def main():
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    acquired = list(ThreadPoolExecutor(max_workers=4).map(capture, REPOS))
    rows = [row for raw in acquired for row in summarise(raw)]
    destination = HERE / "snapshots" / stamp
    destination.mkdir(parents=True, exist_ok=False)
    for raw in acquired:
        (destination / (raw["repository"] + ".json")).write_text(
            json.dumps(raw, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    status = {"acquired_at": now(), "evidence_directory": f"snapshots/{stamp}",
              "method": "read-only GitHub API; review findings matched by original review commit, not mutable comment anchor; no automatic READY promotion",
              "prs": rows}
    (HERE / "CURRENT_STATUS.json").write_text(json.dumps(status, ensure_ascii=False, indent=2)
                                             + "\n", encoding="utf-8", newline="\n")
    lines = ["# Current GitHub status", "", f"Acquired: {status['acquired_at']}", "",
             f"Raw evidence: `{status['evidence_directory']}`.", "",
             "Snapshot only. REVIEW_REQUIRED is not a merge approval. Checks verify their configured scope only.", "",
             "| Repository / PR | Head | CI | Head review | P1 / P2 | Decision |",
             "|---|---|---|---|---|---|"]
    for row in rows:
        if row["state"] == "OPEN":
            lines.append(f"| [{row['repo']} #{row['pr']}]({row['url']}) | `{row['head_sha'][:12]}` | "
                         f"{row['ci']} | {len(row['current_head_reviews'])} | "
                         f"{row['current_head_P1']} / {row['current_head_P2']} | {row['verdict']} |")
    lines += ["", "Merge decisions and independent verification are recorded separately in MERGE_DECISIONS.md.", ""]
    (HERE / "CURRENT_STATUS.md").write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(f"Captured {len(acquired)} repositories, {len(rows)} PRs at {destination.name}")


if __name__ == "__main__":
    main()
