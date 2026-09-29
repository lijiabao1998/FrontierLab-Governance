# Branch protection ruleset 提案（未啟用）

狀態：**提案，未套用到任何 repo**。啟用與否、何時啟用由業主決定；啟用前請以 GitHub 當下的 Rulesets 文件核對欄位名稱。

## 先講限制：所有 agent 共用 `lijiabao1998` 身分

目前人類業主與所有 agent（GPT、Claude、Codex、GLM 等）在 GitHub 上都是同一個帳號。因此伺服器端規則**只能保證硬規則**，**無法區分「業主合併」與「agent 合併」**：

| 能保證 | 不能保證 |
|---|---|
| main 只能透過 PR 更新，不能直接 push | 誰按下 merge：業主與 agent 是同一個身分 |
| 必要 CI check 綠燈才能合併 | 人類核准：GitHub 不允許 PR 作者核准自己的 PR，而所有 PR 的作者都是 `lijiabao1998`，所以「至少 1 個核准」會擋住全部合併 |
| 禁止 force push、禁止刪除 main | CODEOWNERS 審查：code owner 也是同一個帳號 |
| 合併前 review 對話必須 resolved | PR 修改自己的 workflow 讓同名 check 假綠：workflow 檔本身在 PR 控制下，必須人工審 `.github/` 的改動 |
| 分支必須跟上最新 main 才能合併（check-diff 對最新 base 跑） | 有 admin 權限的 token 可以修改或停用 ruleset 本身 |

## 建議 ruleset

套用對象：16 個 repo 的預設分支（`~DEFAULT_BRANCH`，即 `main`）。沒有 bypass actor：業主也走 PR，緊急時由業主在 Settings 暫停 ruleset（會留下稽核紀錄）。

必要 check 名稱取自實際 CI：

| Repo | 必要 check |
|---|---|
| FrontierLab-Governance | `records` |
| 15 個研究庫 | `records / records`（呼叫治理庫 reusable workflow 的 job） |
| FrontierMath（另加） | `lean`（Lean kernel and axioms） |

研究庫範本（REST：`POST /repos/lijiabao1998/<repo>/rulesets`，或在 Settings → Rules → Rulesets 匯入 JSON）：

```json
{
  "name": "main: PR + records CI",
  "target": "branch",
  "enforcement": "active",
  "bypass_actors": [],
  "conditions": { "ref_name": { "include": ["~DEFAULT_BRANCH"], "exclude": [] } },
  "rules": [
    { "type": "deletion" },
    { "type": "non_fast_forward" },
    {
      "type": "pull_request",
      "parameters": {
        "required_approving_review_count": 0,
        "dismiss_stale_reviews_on_push": true,
        "require_code_owner_review": false,
        "require_last_push_approval": false,
        "required_review_thread_resolution": true
      }
    },
    {
      "type": "required_status_checks",
      "parameters": {
        "strict_required_status_checks_policy": true,
        "required_status_checks": [
          { "context": "records / records", "integration_id": 15368 }
        ]
      }
    }
  ]
}
```

- 治理庫：`context` 改為 `records`。
- FrontierMath：`required_status_checks` 再加 `{ "context": "lean", "integration_id": 15368 }`。
- `integration_id` 15368 是 GitHub Actions 的 app id，用來要求 check 必須來自 GitHub Actions；啟用前請核對。
- `required_approving_review_count` 與 `require_code_owner_review` 在共用身分下必須是 0／false，否則沒有任何 PR 能合併。
- `strict_required_status_checks_policy: true` 讓 PR 在合併前必須跟上最新 main，`check-diff` 因此對最新 base 執行。代價是每合併一個 PR，其他 PR 要先更新分支。

## 共用身分下仍可做的補強

1. 給 agent 用的 token 只開 `Contents` 與 `Pull requests` 的寫入，不開 `Administration`。這樣 agent 不能修改或停用 ruleset；但仍能合併 PR，因為合併不需要 admin。
2. 人工審查 `.github/`、`GOVERNANCE.lock.json`、`lab.json` 的改動：這些決定了 CI 跑什麼、跑哪個治理版本。
3. 各 agent 依 AGENTS.md 的分支契約 `<agent>/<problem-id>-<topic>-<round>` 開分支，讓每個 PR 看得出是哪個 agent、哪一題、哪一輪；但這只是紀錄，不是身分驗證。

## 要真正區分業主與 agent，需要分開身分

讓 agent 使用獨立身分（machine user 或 GitHub App），業主保留 `lijiabao1998`。之後可以改成：

- `required_approving_review_count: 1`、`require_code_owner_review: true`，CODEOWNERS 維持 `* @lijiabao1998`：agent 開的 PR 必須業主核准才能合併。
- agent 身分不給 admin，也不列為 bypass actor。

這需要業主建立帳號或 App 並重新發 token，本提案不代為執行。
