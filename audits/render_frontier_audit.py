#!/usr/bin/env python3
"""Render audits/frontier_audit_2026-09-28.md from the JSON truth source.

The markdown is GENERATED — hand edits will be overwritten and CI treats a
dirty diff after rendering as a failure. Run from repo root:
    python3 audits/render_frontier_audit.py
    git diff --exit-code audits/frontier_audit_2026-09-28.md
"""
from __future__ import annotations
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
JSON_PATH = HERE / "frontier_audit_2026-09-28.json"
MD_PATH = HERE / "frontier_audit_2026-09-28.md"


def render(a: dict) -> str:
    L = []
    L.append("# Frontier Audit v3｜2026-09-28｜glm scout sweep（Codex convergence 修訂）")
    L.append("")
    L.append("**單一真相源**：`frontier_audit_2026-09-28.json`；本檔由 "
             "`audits/render_frontier_audit.py` 自動生成——**請勿手改**，"
             "CI 以 render 後 `git diff --exit-code` 防 drift。")
    L.append("")
    L.append(f"- 條目數：{len(a['problems'])}（15 個 repo primaries＋8 個 priority-A screening 題）")
    L.append(f"- 時間戳政策：{a['timestamp_policy']}")
    L.append(f"- 狀態：{a['status_note']}")
    L.append(f"- 四路完成定義：general/discipline/solution/criticism＋≥2 來源（含 ≥1 primary）；"
             "「no resolution found」僅出現在 FOUR_WAY_COMPLETE 條目。")
    L.append("")
    L.append("## 覆蓋總表")
    L.append("")
    L.append("| problem_id | repo | search_status | claims_published | conclusion_scope |")
    L.append("|---|---|---|---|---|")
    for p in a["problems"]:
        scope = p.get("conclusion_scope", "")[:90]
        L.append(f"| {p['problem_id']} | {p['repo']} | {p['search_status']} "
                 f"| {p.get('claims_published')} | {scope} |")
    L.append("")
    for p in a["problems"]:
        L.append(f"### {p['problem_id']}｜{p['repo']}｜{p['search_status']}")
        L.append("")
        if p["search_status"] == "BLOCKED":
            L.append(f"- reason：{p.get('reason')}")
            L.append("- 本條**不發佈任何結論**（claims_published=false）；"
                     "卡片來源 URL 已登記待四路檢索。")
            L.append("")
            continue
        if p["search_status"] == "SCREENING_ONLY":
            L.append(f"- 篩查觀察（非結論）：{p.get('screening_note')}")
            L.append(f"- next-smallest-action：{p.get('next_smallest_action')}")
            L.append("")
            continue
        L.append(f"- checked：{p.get('checked_date')}（{p.get('timestamp_status')}）；"
                 f"engine：{p.get('engine')}")
        L.append("")
        L.append("#### queries")
        L.append("")
        L.append("| category | query | engine | started_at | completed_at | outcome |")
        L.append("|---|---|---|---|---|---|")
        for qq in p.get("queries", []):
            if isinstance(qq, dict) and "category" in qq:
                L.append(f"| {qq['category']} | `{qq['query']}` | {qq['engine']} "
                         f"| {qq.get('started_at')} | {qq.get('completed_at')} "
                         f"| {qq['outcome']} |")
            else:
                # string-form record (e.g. the four original primaries whose
                # per-round query records live in their repo LITERATURE_MAPs):
                # render ONE reference row, never character-iterate (Codex P2)
                L.append(f"| (repo-recorded) | {qq} | (see repo) | | | per-round records in repo LITERATURE_MAP |")
        L.append("")
        L.append("#### sources")
        L.append("")
        L.append("| kind | title | url/doi | year | version | read_mode | supports |")
        L.append("|---|---|---|---|---|---|---|")
        for ss in p.get("sources", []):
            loc = ss.get("url") or ss.get("doi") or "null"
            L.append(f"| {ss.get('kind')} | {ss.get('title')} | {loc} "
                     f"| {ss.get('year')} | {ss.get('version')} "
                     f"| {ss.get('read_mode')} | {ss.get('supports')} |")
        L.append("")
        if p.get("conclusion_scope"):
            L.append(f"- conclusion_scope：{p['conclusion_scope']}")
        if p.get("next_smallest_action"):
            L.append(f"- next-smallest-action：{p['next_smallest_action']}")
        if p.get("extra"):
            for k, v in p["extra"].items():
                if v:
                    L.append(f"- {k}：{v}")
        L.append("")
    L.append("## 方法與限制")
    L.append("")
    L.append("- 有界檢索；「無結果」非未解證明；摘要層級閱讀不等於全文審讀。")
    L.append("- 舊版搜尋之精確時戳不可恢復者記 timestamp_status=UNKNOWN，不猜測。")
    return "\n".join(L) + "\n"


if __name__ == "__main__":
    audit = json.loads(JSON_PATH.read_text(encoding="utf-8"))
    MD_PATH.write_text(render(audit), encoding="utf-8")
    print(f"rendered {MD_PATH.name} from {JSON_PATH.name} "
          f"({len(audit['problems'])} entries)")
