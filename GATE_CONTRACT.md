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
| `README.md`、`AGENTS.md` | 網址 `https://github.com/lijiabao1998/FrontierLab-Governance/{tree,blob,commit,commits,raw}/<ref>` 或 `https://raw.githubusercontent.com/lijiabao1998/FrontierLab-Governance/<ref>/…`（不分大小寫） | 每一處都完整等於 lock `commit` |
| 同上 | 顯式標記 `<!-- governance-pin: <40 hex> -->`（不分大小寫） | 完整等於 lock `commit` |
| 同上 | 文字「治理」或 `governance`，可接 `commit`／`pin`／`ref`／`版本`，再接空白、冒號或反引號，緊跟 7–40 位 hex（關鍵字與 hex 都不分大小寫） | 必須是 lock `commit` 的前綴 |

workflow 逐行解析：`#` 之後的 YAML 註解不算宣告；key 與值可加引號。block scalar（例如 `run: |`、`key: >-`、帶 tag／anchor 的 `run: !!str |`、沒有 key 的 `- |`）的內容是資料，不算宣告，內容以縮排超過該 key（或 `-`）所在欄位為準；內容若提到 `FrontierLab-Governance` 或 `governance_ref` 一律 RED。任何其他非註解行若提到這兩者，卻不是上述兩種寫法（例如 flow mapping），也一律 RED，不跳過。

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

輪次一旦以非 DRAFT 狀態合併，`round_id`、`problem_id`、`agent`、`branch`、`base_sha`、`started_at`、`admitted_at`、`acceptance`、`budget`、`preflight` 就固定；之後的 PR 只能改 `state` 與結果類欄位（例如 `result`、`artifacts`、`not_done`）。這避免把舊輪次改寫成別題或別的 verdict，再當作新的授權。合併時已是 `FINISHED`、`PAUSED` 或 `CLOSED_EXTERNAL` 的輪次已經結束：`state` 也不能再改，之後也不再授權任何新的產物、附件或題卡欄位；要做新工作就開新輪次。merge base 上仍是 DRAFT（或不存在）的輪次，在本次變更中算新輪次。已完成（`COMPLETED_EXTERNAL`／`COMPLETED_INTERNAL`）的題不能新增輪次（包括把先前合併的 DRAFT 補成非 DRAFT），也不能新增研究產物或輪次附件，它的既有輪次也不再授權任何新內容，與 `admit` 一致；要重做就開 replication 題，或先以決策退回狀態。

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
- `status-change` 另需 `from`、`to`，且必須等於題卡實際的舊／新狀態；同一次變更中任何一筆 `from`／`to` 不符的 `status-change` 都是 RED，即使狀態轉移另有輪次依據。狀態有改變時 `fields` 必須包含 `status`；只修正 `resolution` 時，`fields` 只列 `resolution`，`from` 與 `to` 都填目前狀態；`CLAIMED_RESOLVED` 題卡也用這條路徑更正 `resolution`（決策不能把狀態改成 `CLAIMED_RESOLVED`）。目標 `COMPLETED_INTERNAL` 還需 `rounds` 與 `verifier`：`rounds` 必須是 merge base 上已以非 DRAFT 狀態存在（先前 PR 已審）、head 為 `FINISHED`、verdict 為 `NO_RESOLUTION_FOUND` 或 `PARTIAL_PROGRESS` 的同題輪次；`verifier` 不得是這些輪次的 agent，也不得是決策的 `author`。
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
| `CLAIMED_RESOLVED` | 同題輪次 verdict `CLAIMED_RESOLVED`；輪次不改 `resolution` |
| `PARTIAL` | 同題輪次 verdict `PARTIAL_PROGRESS`，或 `status-change` 決策 |
| `OPEN`、`PAUSED`、`RETRACTED` | `status-change` 決策，`from`／`to` 必須等於實際舊／新狀態 |
| `COMPLETED_INTERNAL` | `status-change` 決策 + 已合併的同題 `FINISHED` 研究輪次 + 不同於輪次 agent 與決策作者的 `verifier` + 題卡 `resolution` 通過 `validate_resolution` |

只改 `resolution` 不改 `status` 也要同樣的依據。離開已完成狀態（`COMPLETED_EXTERNAL`／`COMPLETED_INTERNAL` 改成別的狀態）只能靠 `status-change` 決策，不能靠輪次 verdict。`COMPLETED_EXTERNAL` 題卡的 `resolution` 在本契約下不能直接更正（新輪次會被拒）；需要時先以決策退回狀態，再重新走外部完成。

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
- 某題有研究產物，repo 中至少要有一個同題、非 DRAFT、通過 preflight、verdict 為 `NO_RESOLUTION_FOUND` 或 `PARTIAL_PROGRESS` 的輪次（與 `check-diff` 相同；BLOCKED／CLAIMED_RESOLVED 輪次不授權產物）。
- 有附件的 `runs/<round_id>/` 必須有非 DRAFT 的 `round.json`。

這讓直接 push（沒有 PR diff）時也擋得住「產物放錯地方」和「沒有輪次的產物」。

### 3.3 變更檢查（`check-diff`）

`lab.json` 的 `domain` 決定套用哪一份契約，所以不可改動：merge base 與 head 的 domain 不同即 RED（例如研究庫改成 `governance` 以跳過檢查）。`validate` 與 `check-diff` 另外都直接檢查樹本身：含 `problems/` 或 `GOVERNANCE.lock.json` 的 repo 宣告 domain 為 `governance` 即 RED，merge base 沒有 `lab.json` 時也一樣。

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
- merge base 的 root 宣告若不符合目前 gate（例如升 pin 後規則變嚴），`check-diff` 視為沒有任何 root（其下檔案算 unregistered），並在 log 印出 `REVIEW`，而不是讓所有 PR 都跑不動。head 的宣告仍必須合法：修正 `lab.json` 的 PR 可以通過，其他 PR 在修正前仍是 RED。

## 4. 已知限制（需要業主或人工處理）

1. **CI 設定本身在 PR 控制下**：PR 可以刪改自己的 workflow，讓檢查根本不跑。只有伺服器端 branch protection 的 required status checks 能擋，需業主在 GitHub 設定。
2. **直接 push 到 main** 不跑 `check-diff`，只跑 `validate`。
3. **決策紀錄的 `author`、`verifier` 沒有身分驗證**；誰批准了什麼，仍靠 PR 審核與 CODEOWNERS。
4. **小幅 editorial 可能改變語意**；CI 只保證改動量小，並把前後文字印出來。
5. **文件內容（例如 `STATUS.md`）仍可能寫入過度宣稱**；路徑檢查不讀語意。
6. **workflow 只做逐行解析，不是完整的 YAML／Actions 語意**：例如 `if: false` 停用的 job、用 shell 拼接出來的 repo 名稱，都無法可靠判斷；仍需人工審 `.github/` 改動（見 1）。
7. **文件 pin 只讀 §1 列出的寫法**；其他寫法（例如只寫在連結文字裡、沒有「治理／governance」字樣的短 SHA）不算宣告，也不被檢查。
8. **`check-diff` 以 merge base 判斷，`validate` 看不到歷史**：兩個從同一 base 分出的 PR 可以各自通過（例如一個宣告外部完成、另一個在同題交新結果），合併後 `validate` 也無從分辨產物是在完成前還是完成後加入。要關掉這個競態，需要伺服器端要求 PR 合併前先跟上最新 main（#4 提案的 `strict_required_status_checks_policy`），讓 `check-diff` 對最新 base 重跑。
