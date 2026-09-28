# Gate 契約：治理 pin、受保護題目規格與研究路徑

本文件定義 `tools/frontier.py` 的機器檢查範圍，屬 protocol 2.0.0（breaking，見 [PROTOCOL_VERSIONS.md](PROTOCOL_VERSIONS.md)）。它檢查紀錄、欄位與路徑，**不檢查科學真偽**，也不驗證搜尋內容是否誠實。每條守衛在 `tests/` 都至少有一個 GREEN、一個故意違規的 RED 和一個邊界案例；測試不會紅的守衛不算守衛。

生效範圍：研究庫 CI 執行的是 `GOVERNANCE.lock.json` 固定的治理 commit。本契約只在某研究庫把 pin 升到包含本契約的治理 commit 之後，才會在該庫 CI 生效；升 pin 需業主批准，逐庫進行。

| 指令 | 何時跑 | 本契約內容 |
|---|---|---|
| `validate <repo>` | 每次 push／PR | §1 pin 一致性、§3.2 整庫路徑歸屬、決策紀錄格式 |
| `check-diff <repo> <base> <head>` | PR | §2 受保護題目規格、§3.3 本次變更的路徑歸屬 |
| `check-pins <repo>` | 手動 | 只跑 §1 |
| `decide <repo> <ID> …` | 手動 | 產生 §2 的決策紀錄骨架（低摩擦路徑） |

## 1. Governance pin 契約

唯一依據是 `GOVERNANCE.lock.json`：`repository` 必須是 `lijiabao1998/FrontierLab-Governance`，`commit` 必須是 40 位小寫 hex。

只有下列位置算「治理 pin 宣告」，其他 SHA（資料集版本、其他 repo、`actions/checkout@<sha>` 等）一律不讀，避免誤判：

| 檔案 | 宣告位置 | 規則 |
|---|---|---|
| `.github/workflows/research.yml` | `uses: <owner>/FrontierLab-Governance/.github/workflows/<file>@<ref>` | 至少一處；`<owner>/FrontierLab-Governance` 必須等於 lock 的 `repository`；`<ref>` 必須完整等於 lock `commit`（`main`、tag、短 SHA 都是 RED） |
| 同上 | `governance_ref: <ref>` | 至少一處；完整等於 lock `commit` |
| `README.md`、`AGENTS.md` | 網址 `https://github.com/lijiabao1998/FrontierLab-Governance/{tree,blob,commit}/<ref>` | 每一處都完整等於 lock `commit` |
| 同上 | 顯式標記 `<!-- governance-pin: <40 hex> -->` | 完整等於 lock `commit` |
| 同上 | 文字「治理」或 `governance`（不分大小寫），可接 `commit`／`pin`／`ref`／`版本`，再接空白、冒號或反引號，緊跟 7–40 位 hex | 必須是 lock `commit` 的前綴 |

`README.md` 與 `AGENTS.md` 各自至少要有一處宣告。缺宣告與宣告不一致都是 RED：onboarding 文件必須把 agent 指向 CI 實際使用的治理版本。

## 2. 受保護題目規格

### 2.1 欄位分級

| 級別 | 欄位 | 可由什麼授權修改 |
|---|---|---|
| IMMUTABLE | `id`、`domain` | 無。題目不能改名或換學科；要換就新開卡。 |
| SPEC（定義題目與成敗） | `title`、`statement`、`evaluator`、`completion_criterion`、`validation_limits`，以及任何未列名的新欄位 | `spec-change` 決策；小幅 `editorial` 決策 |
| KNOWLEDGE（文獻現況） | `known_result`、`open_gap` | 同題、非 DRAFT、通過 preflight、verdict 不是 BLOCKED 的輪次；`spec-change`；`editorial` |
| PLAN | `first_task` | 同上述輪次（記錄下一個最小動作）；`spec-change`；`editorial` |
| PLAN | `priority` | `hygiene`；`spec-change`（排序是業主的資源決策，不由研究輪次改） |
| PROVENANCE | `sources`、`screening_queries`、`screening_note` | 同上述輪次；`hygiene`；`spec-change`（`screening_note` 也可 `editorial`） |
| FRESHNESS | `checked_on` | **只能**由同題輪次授權，且新日期與該輪 `preflight.checked_at` 的 UTC 日期相差不超過 1 天（容許本地時區） |
| STATUS | `status`、`resolution` | 見 §2.3 |

`first_task` 不決定題目算不算解，所以研究輪次可以更新它；`completion_criterion`、`evaluator`、`statement` 會決定成敗，研究輪次不能順手改。

### 2.2 授權紀錄

**輪次紀錄** `runs/<round_id>/round.json`：必須在本次變更中新增或修改；`round_id` 等於目錄名；`problem_id` 等於被改的題；`state` 不是 `DRAFT`；通過 `validate_preflight`。空白或 DRAFT 輪次不授權任何東西；別題輪次不能掩護本題。

**決策紀錄** `decisions/<decision_id>/decision.json`：必須在本次變更中**新增**；已合併的決策紀錄不可修改或刪除。格式：

```json
{
  "decision_id": "與目錄同名",
  "problem_id": "MED-001",
  "kind": "spec-change | editorial | hygiene | status-change | new-problem",
  "fields": ["實際改動的欄位，一個不多一個不少"],
  "author": "agent 或人",
  "created_at": "含時區的 ISO 8601",
  "base_sha": "40 位 hex",
  "rationale": "為什麼改"
}
```

- `spec-change` 另需 `impact`：`narrows`／`broadens`／`rescopes`／`clarifies` 之一，強迫明說是否弱化或改寫題目。
- `status-change` 另需 `from`、`to`；目標 `COMPLETED_INTERNAL` 還需 `rounds`（已存在的同題 `FINISHED` 輪次）與 `verifier`（不得是任何這些輪次的 agent）。
- `fields` 列了沒改的欄位是 RED（避免預先寫好萬用紀錄）；決策對應的題卡本次沒有改動也是 RED。
- 可附 `sources`，格式同題卡來源。

**低摩擦路徑**：錯字、來源網址修正、查詢字串補登、優先序調整，不需要假裝做研究：

```bash
python3 tools/frontier.py decide ../FrontierMedicine MED-001 --kind editorial --fields statement --agent claude --rationale "修正錯字：隨機"
python3 tools/frontier.py decide ../FrontierMedicine MED-001 --kind hygiene --fields sources --agent claude --rationale "原網址改為 DOI"
```

- `editorial`：只限文字欄位，每欄改動不超過 12 個字元（`difflib` 計算）。超過就改用 `spec-change`。小改動仍可能翻轉語意（例如加一個「不」），所以 CI 會把 SPEC 欄位的前後文字印在 log，審核者必須看。
- `hygiene`：只限 `sources`、`screening_queries`、`screening_note`、`priority`；不能動 `checked_on`，不能用來宣稱做過新檢索。

### 2.3 狀態轉移

| 新狀態 | 必要依據 |
|---|---|
| `COMPLETED_EXTERNAL` | 本次變更中同題輪次：verdict `RESOLVED_EXTERNAL`、state `CLOSED_EXTERNAL`，且題卡 `resolution` 與該輪 `preflight.resolution` 完全相同（`admit` 自動寫出的就是這個）。決策紀錄不能宣告外部完成。 |
| `CLAIMED_RESOLVED` | 同題輪次 verdict `CLAIMED_RESOLVED` |
| `PARTIAL` | 同題輪次 verdict `PARTIAL_PROGRESS`，或 `status-change` 決策 |
| `OPEN`、`PAUSED`、`RETRACTED` | `status-change` 決策，`from`／`to` 必須等於實際舊／新狀態 |
| `COMPLETED_INTERNAL` | `status-change` 決策 + 已存在的同題 `FINISHED` 輪次 + 不同於作者的 `verifier` + 題卡 `resolution` 通過 `validate_resolution` |

只改 `resolution` 不改 `status` 也要同樣的依據。

### 2.4 不可混合

- 同一次變更中，同一題的 SPEC 欄位改動不能和該題研究產物（`problems/<ID>/{experiments,proofs,results}/` 或該題輪次的附件）一起出現：先改規格、另開 PR 交結果。
- 同一次變更中，同一題不能同時改 SPEC 欄位和 `status`：不能邊改題目邊宣告解完。
- 新增題卡需要 `new-problem` 決策，且初始狀態必須是 `OPEN`；刪除題卡一律 RED，退場用 `PAUSED`／`RETRACTED`。

## 3. 研究路徑歸屬

### 3.1 路徑分類（allowlist，未列入者一律 unregistered）

| 類別 | 路徑 | 規則 |
|---|---|---|
| 文件與 CI | `README.md`、`AGENTS.md`、`CLAUDE.md`、`STATUS.md`、`VALIDATION.md`、`LICENSE`、`LICENSE.md`、`CONTRIBUTING.md`、`CITATION.cff`、`.gitignore`、`.gitattributes`、`lab.json`、`GOVERNANCE.lock.json`、`runs/README.md`、`decisions/README.md`、`.github/**` | 不需輪次 |
| 學科基礎設施 | math：`lakefile.toml`、`lean-toolchain`、`lake-manifest.json`、`FrontierMath.lean`、`FrontierMath/Smoke.lean`、`claims.json`、`tools/audit_lean.py` | 不需輪次；只對該學科有效 |
| 題卡 | `problems/<ID>/problem.json` | §2 |
| 研究產物 | `problems/<ID>/{experiments,proofs,results}/**` | 本次變更需有同題輪次，verdict 為 `NO_RESOLUTION_FOUND` 或 `PARTIAL_PROGRESS` |
| 輪次紀錄 | `runs/<round_id>/round.json` | 只增改，不刪 |
| 輪次附件 | `runs/<round_id>/` 下其他檔案 | 本次變更必須同時新增或修改該輪 `round.json`，且非 DRAFT；只增改，不刪 |
| 決策紀錄 | `decisions/<decision_id>/decision.json` | 只增，不改不刪 |
| 登記的額外根路徑 | `lab.json` `artifact_roots` 的每個 `path` 之下（§3.4） | 等同該題研究產物 |
| unregistered | 其他所有路徑，例如 `misc/`、`notes/`、`analysis/`、`problems/<ID>/analysis/`、`problems/<ID>/results.txt`、`Problems/…`、學科外的 `*.lean` | 新增或修改即 RED；刪除允許（清理舊檔） |

分類只看路徑，不看副檔名：把結果改名成 `.md` 或搬到別的資料夾，只會變成「研究產物仍需輪次」或「unregistered」。README、文件修字與 CI 調整屬於第一類，不會被當成研究成果。

### 3.2 整庫檢查（`validate`）

- 每個 git 追蹤檔都必須能歸類；unregistered 即 RED。
- 某題有研究產物，repo 中至少要有一個同題、非 DRAFT、通過 preflight 的輪次。
- 有附件的 `runs/<round_id>/` 必須有非 DRAFT 的 `round.json`。

這讓直接 push（沒有 PR diff）時也擋得住「產物放錯地方」和「沒有輪次的產物」。

### 3.3 變更檢查（`check-diff`）

以 `git diff --name-status --no-renames <base>...<head>` 逐檔分類。改名視為「刪舊路徑 + 加新路徑」，兩端都要合規。新舊內容一律從 merge-base 與 head commit 讀取，不讀工作目錄。治理庫本身（`lab.json` domain 為 `governance`）跳過研究路徑檢查，改由 unit tests 把關。

### 3.4 Repo 登記的額外研究根路徑（artifact roots）

預設研究路徑是 `problems/<ID>/{experiments,proofs,results}/`。有些工具鏈要求程式放在特定位置，例如 Lake 只能 import 屬於 lib 命名空間的模組，`problems/MATH-001/proofs/` 不是合法的 Lean 模組路徑。這時 repo 可以在 `lab.json` 明確登記額外根路徑：

```json
"artifact_roots": [
  {"path": "FrontierMath/Research/MATH001/", "problem_id": "MATH-001", "kind": "proofs"}
]
```

- 每個 root 只對應一題、一種 artifact kind（`experiments`／`proofs`／`results`）。root 下的檔案一律視為該題的研究產物，受 §3.1 同一條輪次規則管理：本次變更需有同題、verdict 為 `NO_RESOLUTION_FOUND` 或 `PARTIAL_PROGRESS` 的輪次；整庫檢查時 repo 中要有同題已 admit 的輪次。
- `path` 必須是相對目錄、以 `/` 結尾；每段以英數字或底線開頭（不接受 `..`、隱藏目錄、絕對路徑）；不得位於 `problems/`、`runs/`、`decisions/`、`.github/` 之下；不得包含任何基礎設施檔（例如 math 的 `FrontierMath/` 會包住 `FrontierMath/Smoke.lean`，所以不行）；root 之間不得互相巢狀。`problem_id` 必須是本庫存在的題。
- `check-diff` 用 **merge base** 的 `lab.json` 決定 root。所以登記 root 與在 root 下交研究產物必須分成兩個 PR：同一個 PR 內新登記的 root，其下檔案仍算 unregistered（RED）。`lab.json` 的 root 改動會在 CI log 印出 `REVIEW lab.json artifact_roots`。
- 移除 root 時，root 下仍被追蹤的檔案會在 `validate` 變成 unregistered（RED）。

## 4. 已知限制（需要業主或人工處理）

1. **CI 設定本身在 PR 控制下**：PR 可以刪改自己的 workflow，讓檢查根本不跑。只有伺服器端 branch protection 的 required status checks 能擋，需業主在 GitHub 設定。
2. **直接 push 到 main** 不跑 `check-diff`，只跑 `validate`。
3. **決策紀錄的 `author`、`verifier` 沒有身分驗證**；誰批准了什麼，仍靠 PR 審核與 CODEOWNERS。
4. **小幅 editorial 可能改變語意**；CI 只保證改動量小，並把前後文字印出來。
5. **文件內容（例如 `STATUS.md`）仍可能寫入過度宣稱**；路徑檢查不讀語意。
