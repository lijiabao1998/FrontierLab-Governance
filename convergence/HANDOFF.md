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


## Convergence-2 最終 checkpoint｜2026-09-28T16:43:53+00:00

| repo | PR | head | CI | P1 | P2 | state |
|---|---|---|---|---|---|---|
| FrontierMath | 4 | beaf8427 | GREEN | 0 | 0 | AWAITING_REVIEW |
| FrontierPhysics | 2 | 7219b6ab | GREEN | 0 | 0 | AWAITING_REVIEW |
| FrontierChemistry | 1 | bdca6622 | GREEN | 0 | 0 | AWAITING_REVIEW |
| FrontierBiology | 1 | 4fdac610 | GREEN | 2 | 1 | FIXING |
| FrontierLab-Governance | 2 | bba67544 | GREEN | 0 | 1 | FIXING |

本 session 完成之修復：
- PHYS：W3 真幾何網格、raw rows 全座標、bands 全精度+persisted judging、commands provenance、雙 manifest（renormalize 根治 EOL 漂移）、amplitude guard 有牙。重跑 PASS。
- BIO：E2 同 cohort（770 列）＋CLEAN 退化如實記錄、headline 僅 E2、verifier v3 6/6、manifest 含 .gz、撤回數字清除。
- Gov：renderer 字串 queries 正規化（4 reference rows）、drift check 乾淨。
- CHEM：SCAFFOLD_AUDIT.md（preregistration 誠實記錄：C4 FAIL 為 post-hoc key 下結果）、graceful RDKit。
- FM：無 findings；tests/manifest 全綠。

殘餘：各 PR 等 Codex 對最新 head 的 re-review；若返回新 findings，依 SOP 繼續。禁止自行 merge。


## Convergence-3 checkpoint｜2026-09-28T17:35:22+00:00
- READY_FOR_OWNER_REVIEW：FM PR#4（beaf842，三審 0 findings）、CHEM PR#1（bdca662，三審 0 findings）
- AWAITING_REVIEW：PHYS PR#2（88c316c：environment.txt runtime P1 修復）、BIO PR#1（9590a99：E2 FAILED/INCONCLUSIVE 誠實記錄＋MODEL_ABLATION 新 admitted round PASS＋verifier v4）、Gov PR#2（ledger locator 化＋validate_ledger.py 11/11 exit 0）
- E2 負結果已保存：CLEAN train=0、verdict=E2_INCONCLUSIVE_SIBLING_FREE_CLEAN_NOT_CONSTRUCTIBLE——未調切分救 PASS
- 殘餘：等 Codex 對最新 heads 的 re-review；BIO donor-gap estimator 差異（0.905 vs 0.1616）已列 documented discrepancy


## DISCOVERY MODE checkpoint｜2026-09-29T15:52:49+00:00
- 新 admitted round 完成：MATH-004 r1（PR #9）——第一個 evaluator、窮舉 D(1)=2/D(2)=4、greedy LB 8/18/35/72、對抗式發現並修正 unwrapped-AP 定義 bug
- exploration/ 目錄建置：FRONTIER_MAP、HYPOTHESIS_QUEUE（7 項排序）、NEGATIVE_RESULTS（10 項）、CROSS_REPO_LINKS（6 條）、EXPLORATION_LEDGER
- 下一 session 建議：H-MATH-004 n=3 精確窮舉（含對稱剪枝）→ H-MATH-006 enum → PHYS Sabra → BIO 真資料
