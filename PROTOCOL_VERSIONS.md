# 研究契約版本

`protocol_version` 表示某個治理 commit 實作的研究契約版本：規則文件（AGENTS、RESEARCH_PROTOCOL、EVIDENCE_POLICY、SAFETY）加上 `tools/frontier.py` 的 gate 行為。

- 治理庫 `lab.json` 的 `protocol_version`，以及 `tools/frontier.py` 的 `PROTOCOL_VERSION`，都是**本 commit** 實作的版本。兩者由 `validate` 與單元測試互相核對。
- 研究庫 `GOVERNANCE.lock.json` 的 `protocol_version`，是它固定的那個治理 commit 的版本。研究庫 CI 用 lock 的 commit 執行 `validate`，所以兩者不一致就是 RED；本機誤用別的治理版本跑 `validate` 也會 RED，並提示 checkout lock 的 commit。
- 版本號採語意版本：修補錯字或說明為 patch；向後相容地擴充（例如新增題號命名空間）為 minor；讓既有合規紀錄變成不合規的規則改變為 major 或須業主另行決定。

| 版本 | 引入 commit | 內容 | 目前固定此版本的研究庫 |
|---|---|---|---|
| 1.0.0 | `07d2b13051b83215182e411e1612f92f1912d8fb` | bootstrap：每輪四路檢索 gate、證據與安全政策、MATH/PHYS/BIO/CHEM 題號 | FrontierMath、FrontierPhysics、FrontierBiology、FrontierChemistry |
| 1.1.0 | `091d6a26a4af8522683711483f2b97afd90efa7f`（有缺陷）→ 修正於 `f40beb161b6c87201d8082ecbc29c7e0b3eaa402` | 向後相容擴充：新增 CS/STAT/MAT/ASTRO/EARTH/NEURO/ECON/ENG/MED/SOC/META 題號；`checked_on` 容許 UTC 前方一日。規則文件未改。 | 其餘 11 個研究庫（固定 `f40beb16`） |
| 1.2.0 | `claude/governance-hygiene` 合併後的 main commit（合併時補登） | 向後相容擴充：時間戳缺漏改為乾淨的 `BLOCKED:`；`start --topic` 產生 `<agent>/<ID>-<topic>-<UTC>` 分支；`admit` 對新輪次要求此分支契約，舊版工具已登記的輪次沿用原規則；`validate` 要求 lock 的 `protocol_version` 等於執行中治理版本。 | 無（升 pin 時一併把 lock 改為 1.2.0） |

## 1.1.0 的釐清紀錄（2026-09-28）

擴充時，11 個新研究庫的 lock 已寫 `1.1.0`，但治理庫 `lab.json` 仍停在 bootstrap 的 `1.0.0`，治理庫本身從未宣告 1.1.0。查證結果：

- `lab.json` 自 `07d2b130` 建立後未改。
- 新研究庫的 lock 在建立時（固定 `091d6a26`）與改 pin 後（固定 `f40beb16`）都寫 `1.1.0`。
- `07d2b130` 與 `f40beb16` 之間，規則文件沒有改動，gate 只做向後相容擴充；1.0.0 的研究庫在 1.1.0 工具下仍然合規。

因此擴充時有意宣告的是 1.1.0（minor），錯的是治理庫 `lab.json` 沒有跟著升。原始四庫的 `1.0.0` 與其 pin `07d2b130` 一致，**不改**。

同一個 PR 又向後相容地加入新的 gate 行為，依上面的語義再升一個 minor：治理庫 `lab.json` 直接從 `1.0.0` 改為 `1.2.0`，並加上 `lab.json`、`PROTOCOL_VERSION` 與研究庫 lock 的一致性檢查。分支契約只套用在新輪次，舊紀錄不會因升級而變成不合規；若改成對歷史紀錄也強制，就屬於 major。

`091d6a26` 雖屬 1.1.0，但 `problem_path` 仍只接受四個舊題號，新題號會被拒絕；任何研究庫都不應固定在它。
