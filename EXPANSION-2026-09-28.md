# 2026-09-28 十一研究庫擴充驗收

## 範圍

在原有 FrontierMath / Physics / Biology / Chemistry 之外，完成 11 個新研究 repo 的第一版 bootstrap。每庫 10 張 scoped frontier problem cards，共新增 110 張；15 個學科／元科學 repo 合計 150 張初始題卡。中央治理仍是 FrontierLab-Governance。

新增庫：

| Repo | Primary | 驗收 commit | Remote CI |
|---|---|---|---|
| FrontierComputerScience | CS-001 | `02c84fa77c3cee2e4b90c37d4c089ed67eff4c13` | success |
| FrontierStatistics | STAT-001 | `d81eaadfa16134d0f744ea0256db756a557e3769` | success |
| FrontierMaterials | MAT-003 | `4b1a99ca87c33b1c0fc5281ab068b800a325b293` | success |
| FrontierAstronomy | ASTRO-003 | `796d97763a4957a1124cc0ed997a75eb5d6d1571` | success |
| FrontierEarth | EARTH-003 | `39ade8c1dbb507aed17ef9b29f8537d09fe08b6a` | success |
| FrontierNeuroscience | NEURO-001 | `1d8b2d6ce7a35797a3949f8258cc4eae31aacfba` | success |
| FrontierEconomics | ECON-001 | `7f333f502d2fe83967a8a600369bc15d2c35cf96` | success |
| FrontierEngineering | ENG-004 | `6ee2083b403070d2a5942d735684117c7548c50c` | success |
| FrontierMedicine | MED-001 | `5b693a6bc4baa2647530833d046a1f0528dab90c` | success |
| FrontierSocialScience | SOC-008 | `f2a2c8fc70aaa409fd18092ad5628df432ed766f` | success |
| FrontierMetaScience | META-001 | `5d3455dd9a3e223b5e3240575c204ff71507af76` | success |

所有新增庫固定治理 commit：

`f40beb161b6c87201d8082ecbc29c7e0b3eaa402`

該治理 commit 自身 remote CI success。

## 每庫都有

- README：主線、10題索引、第一輪入口與「OPEN 不是未解證明」。
- AGENTS / CLAUDE：branch + PR、多agent角色與禁止自合。
- STATUS：明確目前原創研究輪次為0。
- VALIDATION：該學科專用 evidence/evaluator contract。
- `lab.json` 與 `GOVERNANCE.lock.json`。
- 固定治理 commit 的 reusable GitHub Actions workflow。
- CODEOWNERS、PR template、runs/README、gitignore。
- `problems/<ID>/problem.json` × 10；每張含 statement、known result、open gap、first task、evaluator、validation limits、completion criterion、initial source/query。

## CI 紅燈與修復

第一批 11 庫首次執行全部紅燈。原因不是題卡科學內容，而是治理工具雖新增 prefix constant 與 unit test，`problem_path` / `check_diff` 仍殘留舊的四科 hard-coded regex；另外題卡用台灣本地 2026-09-28 日期時，GitHub runner 尚是 UTC 2026-09-27。

修復治理：
- 統一 problem ID 支援：MATH / PHYS / BIO / CHEM / CS / STAT / MAT / ASTRO / EARTH / NEURO / ECON / ENG / MED / SOC / META。
- `problem_path` 與 research-diff gate 改用完整 prefix set。
- date-only `checked_on` 允許 UTC 前方時區的一日日期差。
- extended-prefix negative/unit tests 實際通過。

修復後 11 庫全部重新 pin 並觸發 remote CI，均為 success。失敗沒有刪除或改寫成第一次就通過。

## 證據邊界

150 張題卡是研究 registry，不是「150 個已確認永久未解問題」。初始題卡基於 2026-09-28 的有界文獻篩查，有些題是精確 open problem，有些是清楚限定的 frontier research gap。每次 agent 真正開一輪之前，仍必須重新做 general / discipline / solution / criticism 四路檢索、閱讀原始來源、比較 scope。

若已確認同範圍外部解答：
1. 標 `COMPLETED_EXTERNAL`；
2. 記原作者、來源與獨立核查；
3. 停止把原題當新發現目標；
4. 以 PR 更新 registry。

局部 benchmark、特例、有限 n、單一資料集或一組模擬成功，不關閉廣泛父問題。

## 尚未做

- 110 題的專用 evaluator / baseline reproduction 尚未逐題施工。
- 原創 research rounds 仍為 0。
- 沒有常駐 agent、自動研究排程、付費 GPU/API、濕實驗或臨床執行。
- CODEOWNERS / repo instructions 不是 GitHub server-side branch protection；硬門禁仍需另設。
- 初始 source screening 不替代每輪 fresh search，也不等於完整讀完每篇全文。
