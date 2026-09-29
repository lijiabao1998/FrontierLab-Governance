# 研究契約版本

`protocol_version` 表示某個治理 commit 實作的研究契約版本：規則文件（AGENTS、RESEARCH_PROTOCOL、EVIDENCE_POLICY、SAFETY）加上 `tools/frontier.py` 的 gate 行為。

- 治理庫 `lab.json` 的 `protocol_version`，以及 `tools/frontier.py` 的 `PROTOCOL_VERSION`，都是**本 commit** 實作的版本。兩者由 `validate` 與單元測試互相核對。
- 研究庫 `GOVERNANCE.lock.json` 的 `protocol_version`，是它固定的那個治理 commit 的版本。研究庫 CI 用 lock 的 commit 執行 `validate`，所以兩者不一致就是 RED；本機誤用別的治理版本跑 `validate` 也會 RED，並提示 checkout lock 的 commit。
- 版本號採語意版本：修補錯字或說明為 patch；向後相容地擴充（例如新增題號命名空間）為 minor；讓既有合規紀錄變成不合規的規則改變為 major 或須業主另行決定。

| 版本 | 引入 commit | 內容 | 目前固定此版本的研究庫 |
|---|---|---|---|
| 1.0.0 | `07d2b13051b83215182e411e1612f92f1912d8fb` | bootstrap：每輪四路檢索 gate、證據與安全政策、MATH/PHYS/BIO/CHEM 題號 | FrontierMath、FrontierPhysics、FrontierBiology、FrontierChemistry |
| 1.1.0 | `091d6a26a4af8522683711483f2b97afd90efa7f`（有缺陷）→ 修正於 `f40beb161b6c87201d8082ecbc29c7e0b3eaa402` | 向後相容擴充：新增 CS/STAT/MAT/ASTRO/EARTH/NEURO/ECON/ENG/MED/SOC/META 題號；`checked_on` 容許 UTC 前方一日。規則文件未改。 | 其餘 11 個研究庫（固定 `f40beb16`） |
| 1.2.0 | `1c577661890e52e9e34197ba8f86d076ad2d3b06`（PR #1 合併） | 向後相容擴充：時間戳缺漏改為乾淨的 `BLOCKED:`；`start --topic` 產生 `<agent>/<ID>-<topic>-<UTC>` 分支；`admit` 對新輪次要求此分支契約，舊版工具已登記的輪次沿用原規則；`validate` 要求 lock 的 `protocol_version` 等於執行中治理版本。 | 無（升 pin 時一併把 lock 改為 1.2.0） |
| 2.0.0 | `claude/governance-gate-hardening`（PR #5）合併後的 main commit（合併時補登） | **Breaking**（見 [GATE_CONTRACT.md](GATE_CONTRACT.md)）：規則文件包含 PR #3（`9af72f82553d337271d2b13bc8abcfd00770d199`）把 RESEARCH_PROTOCOL §5 的完成界線推廣到所有經驗、計算與應用學科；lock、workflow、README、AGENTS 的治理 pin 必須一致且 README/AGENTS 必須宣告；題卡欄位分級，改動需同題輪次或決策紀錄；研究路徑採 allowlist，未登記路徑 RED；輪次紀錄不可刪除、已合併輪次的身分與檢索不可改寫，決策紀錄不可刪改；已完成的題不再收新輪次與研究產物；repo 可在 `lab.json` 登記額外研究根路徑。既有合規的 repo 升 pin 後可能變 RED，例如 README 沒有治理 pin 宣告、有未登記路徑。 | 無。業主決定：先升 11 個新研究庫；原始四庫等現有研究 PR 收束後再升 |

## 升到 2.0.0 的檢查清單

1. 同一個 PR 內改 `GOVERNANCE.lock.json`（`commit` 與 `protocol_version: 2.0.0`）、workflow 的 `uses:…@<commit>` 與 `governance_ref`，以及 README.md、AGENTS.md 的治理 pin 宣告。
2. 用新治理版本跑 `validate`：README/AGENTS 缺宣告、未登記路徑、沒有同題輪次的研究產物都會 RED，先處理再升。
3. 需要額外研究根路徑的 repo（例如 FrontierMath 的 Lean 模組），先用單獨的 PR 在 `lab.json` 登記 `artifact_roots`，合併後再交研究產物。
4. FrontierMath 另建議在 `lakefile.toml` 的 lean_lib 設定 `globs = ["FrontierMath.+"]`，讓 root 下沒被 import 的模組也會被 `lake build --wfail` 編譯；否則未 import 的檔案（包括含 `sorry` 的）不會被 build。

## 1.1.0 的釐清紀錄（2026-09-28）

擴充時，11 個新研究庫的 lock 已寫 `1.1.0`，但治理庫 `lab.json` 仍停在 bootstrap 的 `1.0.0`，治理庫本身從未宣告 1.1.0。查證結果：

- `lab.json` 自 `07d2b130` 建立後未改。
- 新研究庫的 lock 在建立時（固定 `091d6a26`）與改 pin 後（固定 `f40beb16`）都寫 `1.1.0`。
- `07d2b130` 與 `f40beb16` 之間，規則文件沒有改動，gate 只做向後相容擴充；1.0.0 的研究庫在 1.1.0 工具下仍然合規。

因此擴充時有意宣告的是 1.1.0（minor），錯的是治理庫 `lab.json` 沒有跟著升。原始四庫的 `1.0.0` 與其 pin `07d2b130` 一致，**不改**。

同一個 PR 又向後相容地加入新的 gate 行為，依上面的語義再升一個 minor：治理庫 `lab.json` 直接從 `1.0.0` 改為 `1.2.0`，並加上 `lab.json`、`PROTOCOL_VERSION` 與研究庫 lock 的一致性檢查。分支契約只套用在新輪次，舊紀錄不會因升級而變成不合規；若改成對歷史紀錄也強制，就屬於 major。

`091d6a26` 雖屬 1.1.0，但 `problem_path` 仍只接受四個舊題號，新題號會被拒絕；任何研究庫都不應固定在它。
