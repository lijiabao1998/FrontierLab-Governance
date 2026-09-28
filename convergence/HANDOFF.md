# HANDOFF｜Convergence-2 session（durable, committed to GitHub）

## 現況（live truth 2026-09-28）
- FM PR#4 `beaf8427`：AWAITING_REVIEW（head findings 0）
- PHYS PR#2 `81c7c372`：FIXING（3 P2：W3 幾何網格 / raw rows 未存 / bands 精度）
- CHEM PR#1 `6b7cf14d`：AWAITING_REVIEW（head findings 0；owner 要求 scaffold/preregistration 審計）
- BIO PR#1 `500ecfa6`：FIXING（2 P1 + 4 P2：E2 同測試集、4/4→1 preregistered、newline/hash、GEO .gz manifest、withdrawn metrics、donor summary）
- Gov PR#2 `2cc70438`：FIXING（1 P2：renderer 字串 queries 逐字元）

## 修復 SOP
checkout branch → 修根因 → targeted test → full regression → verifier → manifest（最後生成）→ commit → push → 更新本目錄 ledger → @codex review → 重抓 threads → 迭代。

## 規則
READY 僅在：head 已 review + P1=0 + P2=0 + CI 綠 + manifest 綠 + 無 stale claims + 無 post-hoc 冒充 preregistered。
僅 reviewer 未返回 = AWAITING_REVIEW（不是 READY）。禁止自行 merge / force push main。

## Session 規則（owner override）
持續施工至 context 實際耗盡；每完成一事件即更新 ledger 並 push；FAIL/負結果照存；最後狀態以本目錄 GitHub 版為準。
