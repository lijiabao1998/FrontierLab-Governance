# 狀態

## 目前（2026-09-29）
- 架構：1 個治理庫 + 15 個研究庫；每個研究庫 10 張初始題卡，共 150 張。
- 治理庫 main 實作 protocol 2.0.0（引入 commit `9c3ae2dbaa1c814f3ef451c041dedfe3b77d926f`；gate 契約見 [GATE_CONTRACT.md](GATE_CONTRACT.md)）。
- 研究庫固定的治理版本以各庫 `GOVERNANCE.lock.json` 為準：原始四庫（Math、Physics、Biology、Chemistry）固定 `07d2b130`（protocol 1.0.0）；其餘 11 庫固定 `9c3ae2db`（protocol 2.0.0）。版本語義見 [PROTOCOL_VERSIONS.md](PROTOCOL_VERSIONS.md)。
- 原始四庫升到 2.0.0 前要處理：Physics、Biology、Chemistry 的 README 沒有治理 pin 宣告；部分研究分支在 2.0.0 下 `check-diff` 為 RED；FrontierMath 建議在 `lakefile.toml` 設 `globs = ["FrontierMath.+"]`（見 PROTOCOL_VERSIONS.md 的檢查清單）。
- 治理 gate 的測試：以 `python3 -m unittest discover -s tests -v` 的實際輸出與遠端 CI 為準；本文件不寫死測試數量。
- 研究輪次：以各研究庫 main 上的 `runs/` 為準；本文件不代記其他分支或未合併 PR 的研究狀態。
- 尚未配置：常駐 agent、API key、付費計算、GitHub 分支保護與 required status checks（[BRANCH_PROTECTION_PROPOSAL.md](BRANCH_PROTECTION_PROPOSAL.md) 只是提案，未啟用）。文件與 CODEOWNERS 不是伺服器端安全鎖。

## 歷史紀錄
以下保留當時原文，不回改；其中的數字與「下一步」是當時的狀態。

### 2026-09-27 bootstrap（當時共五庫：本治理庫與四個研究庫）

主線：治理與可重現基線先行，各科 10 題；先一科一題跑通，再擴並行。

- 已建立：研究協議、角色與 PR 流程、來源與完成狀態政策、Python per-round gate、反向測試、共用 CI。
- 本機已執行：15 個 unittest 測試方法通過，含每項漏填檢查、舊搜尋、缺 primary、重複來源、無支持完成、子題誤關父題等拒絕案例。
- 尚未由此紀錄宣稱：GitHub 遠端 CI 通過、Lean 通過、任何問題被本庫解決、資料集實際重現。
- 尚未配置：常駐 agent、API key、付費計算、GitHub 分支保護。文件與 CODEOWNERS 不是伺服器端安全鎖。

下一步：四個研究倉庫固定本治理 commit，跑 schema／gate CI；首輪各選 README 的基線任務，先做新的文獻檢索，不直接進發現模式。


### 2026-09-28 擴充
研究線由4科擴充到15個學科／元科學repo；目標初始問題卡總數150。治理工具新增 CS、STAT、MAT、ASTRO、EARTH、NEURO、ECON、ENG、MED、SOC、META 問題ID支援。新增repo仍須各自固定本治理commit並先通過CI，不能因框架存在就宣稱任何研究問題已解。


### 2026-09-28 十一庫初始化完成
新增 11 個研究 repo 已各寫入 10 張初始題卡（共 110），與原四科 40 題合計 150 張。新增 repo 全部固定治理 `f40beb161b6c87201d8082ecbc29c7e0b3eaa402`，遠端 research-records CI 已逐庫通過。這只驗題卡／治理結構；原創研究輪次仍為 0，題目是否仍未解必須在每一輪開始前重新聯網核對。


### 2026-09-28 狀態（2026-09-29 由上方「目前」取代）
- 研究庫固定的治理版本：原始四庫固定 `07d2b130`（protocol 1.0.0），其餘 11 庫固定 `f40beb16`（protocol 1.1.0）。


### 2026-09-29 治理 1.2.0／2.0.0 合併與 11 庫升級（Claude；業主授權自主驗證後合併）
每個 PR 合併前都重查遠端 head 與該 head 上的 CI，並以 `expectedHeadSha` 合併；科學結論不因這些合併而改變。

| PR | 合併的 head | 合併 commit | 合併前驗證 |
|---|---|---|---|
| 治理 #1（hygiene，protocol 1.2.0） | `491631c` | `1c57766` | 40 tests；15 個研究庫與 12 條研究分支在 1.2.0 下 validate PASS |
| 治理 #3（RESEARCH_PROTOCOL §5 推廣） | `48dc5ff` | `9af72f8` | 只改 §5；交叉引用存在；合到 main 後 tests PASS |
| 治理 #4（分支保護 ruleset 提案，未啟用） | `a61a614` | `bdd4efa` | 只新增提案文件；JSON 可解析；check 名稱與實際 CI 相符 |
| 治理 #5（gate hardening，protocol 2.0.0） | `c7baf35` | `9c3ae2d` | Codex review 3 項＋三輪獨立 code review 共 20 項，逐項先重現再修正；168 tests；mutation 29/29；原始四庫 18 條研究分支的 check-diff 輸出與審查前相同 |
| FrontierComputerScience #2（升到 2.0.0） | `e421f95` | `1688c47` | 只改 lock、workflow、README、AGENTS 的治理 commit；validate／check-diff／check-pins PASS；`records / records` 綠 |
| FrontierStatistics #2（升到 2.0.0） | `4b23056` | `3e9a457` | 只改 lock、workflow、README、AGENTS 的治理 commit；validate／check-diff／check-pins PASS；`records / records` 綠 |
| FrontierMedicine #2（升到 2.0.0） | `ae0e7fd` | `3db7921` | 只改 lock、workflow、README、AGENTS 的治理 commit；validate／check-diff／check-pins PASS；`records / records` 綠 |
| FrontierEngineering #2（升到 2.0.0） | `b4ae80d` | `79594b5` | 只改 lock、workflow、README、AGENTS 的治理 commit；validate／check-diff／check-pins PASS；`records / records` 綠 |
| FrontierEconomics #2（升到 2.0.0） | `bbd44a3` | `92c11fc` | 只改 lock、workflow、README、AGENTS 的治理 commit；validate／check-diff／check-pins PASS；`records / records` 綠 |
| FrontierNeuroscience #2（升到 2.0.0） | `8b88e62` | `e257e97` | 只改 lock、workflow、README、AGENTS 的治理 commit；validate／check-diff／check-pins PASS；`records / records` 綠 |
| FrontierEarth #2（升到 2.0.0） | `1cc80df` | `10124d0` | 只改 lock、workflow、README、AGENTS 的治理 commit；validate／check-diff／check-pins PASS；`records / records` 綠 |
| FrontierAstronomy #2（升到 2.0.0） | `6752555` | `56af914` | 只改 lock、workflow、README、AGENTS 的治理 commit；validate／check-diff／check-pins PASS；`records / records` 綠 |
| FrontierMaterials #2（升到 2.0.0） | `4eb81ec` | `5941570` | 只改 lock、workflow、README、AGENTS 的治理 commit；validate／check-diff／check-pins PASS；`records / records` 綠 |
| FrontierSocialScience #2（升到 2.0.0） | `ca14b07` | `f36d188` | 只改 lock、workflow、README、AGENTS 的治理 commit；validate／check-diff／check-pins PASS；`records / records` 綠 |
| FrontierMetaScience #2（升到 2.0.0） | `5e00903` | `bf071d8` | 只改 lock、workflow、README、AGENTS 的治理 commit；validate／check-diff／check-pins PASS；`records / records` 綠 |

11 個研究庫的升級在 FrontierMedicine 的副本上做過反向檢查：未登記檔、沒有輪次的研究產物、改 `completion_criterion`、README 留舊 pin 都 RED。合併後 11 庫 main 的 `records / records`（呼叫 `@9c3ae2db`）與治理庫 main 的 `records` 都是綠的。原始四庫仍固定 `07d2b130`（1.0.0），依業主決定等現有研究 PR 收束後再升。
