# 五庫初始化驗收紀錄｜2026-09-27

## 已交付

五個既有公開倉庫已實際寫入，沒有建立同名重複倉庫，沒有改動 GlimmerTown 系列。

| 倉庫 | 本次已核對的研究／框架 commit | 問題卡 | 遠端 CI |
|---|---|---:|---|
| [FrontierLab-Governance](https://github.com/lijiabao1998/FrontierLab-Governance) | `07d2b13051b83215182e411e1612f92f1912d8fb` | 共用治理 | [Research records 通過](https://github.com/lijiabao1998/FrontierLab-Governance/actions/runs/36329898391) |
| [FrontierMath](https://github.com/lijiabao1998/FrontierMath) | `cd1e4eadc177920b95332ebe08c2498e52c3ce56` | 10 | [紀錄通過](https://github.com/lijiabao1998/FrontierMath/actions/runs/36331328933)、[Lean／公理審計通過](https://github.com/lijiabao1998/FrontierMath/actions/runs/36331328580) |
| [FrontierPhysics](https://github.com/lijiabao1998/FrontierPhysics) | `bca6b6c16efc5d2e04ff95cdfda5bea522160371` | 10 | [Research records 通過](https://github.com/lijiabao1998/FrontierPhysics/actions/runs/36330636815) |
| [FrontierBiology](https://github.com/lijiabao1998/FrontierBiology) | `e0c162b2705760eee8cc22c1400da2370984fac4` | 10 | [Research records 通過](https://github.com/lijiabao1998/FrontierBiology/actions/runs/36330838725) |
| [FrontierChemistry](https://github.com/lijiabao1998/FrontierChemistry) | `6edd379003c880e5c3e5b1ade556dff21e9a7591` | 10 | [Research records 通過](https://github.com/lijiabao1998/FrontierChemistry/actions/runs/36331066907) |

本驗收文件的提交是後續文件提交；上表固定的是實際已跑過檢查的框架／題卡版本。四科繼續鎖定治理 `07d2b130...`，不因新增本報告而浮動升級依賴。

## 框架內容

- 共用研究協議、來源與證據政策、完成狀態、公開資料與安全／算力邊界。
- 各科 README 的明確主線、10張 `problems/<ID>/problem.json`、AGENTS／CLAUDE 入口、STATUS、PR模板、CODEOWNERS、固定治理 lock 及紀錄 CI。
- 物理／生物／化學另有學科 VALIDATION 契約；數學另有固定 Lean toolchain、Lake工程、manifest、claims清單、公理審計與實際 Lean CI。
- 每題包含：問題範圍、已知結果、缺口、最小任務、驗證方式、不能推出什麼、完成條件、初始檢索字串、來源及閱讀限制。

## 每輪開始前的機制

`start` 只生成 DRAFT；研究者必須真正完成本輪的廣域、學科、解答及反證／更正四路檢索並閱讀原文，填寫 `round.json`，再由 `admit` 檢查。

入場記錄要求本輪開始後的新鮮搜尋、來源、精確範圍比較、驗收凍結與預算。已確認同範圍外部解答則寫 `COMPLETED_EXTERNAL`，輪次 `CLOSED_EXTERNAL`，停止重複探索並提狀態更新 PR；未核實解答聲稱先暫停。特例、下界或某benchmark進步不能關閉一般父問題。

15個本機 unittest 測試方法通過，遠端共用CI也執行這批測試。測試包括缺檢查項、舊搜尋、重複來源、缺primary、main分支、無支持完成、子題误關父題及外部完成狀態寫入。這是軟體行為驗證，不是驗證搜尋內容誠實或科學問題確實未解。

## Lean 失敗與修復

第一次數學 Lean CI：run `36330192158`，job `108650517971`，失敗原因為 `No lake-manifest.json found. Run lake update to generate manifest`。Lean工具鏈成功安裝，但尚未進入build，公理審計被跳過。因此不能把第一輪報成證明通過。

修復 commit `cd1e4eadc177920b95332ebe08c2498e52c3ce56` 加入無外部依賴的明確Lake manifest。重跑 run `36331328580`／job `108653711679` 後，Lean Action 與 `Audit declared proof axioms` 都顯示 success。

目前被驗證的是 `FrontierMath.bootstrap_add_zero`，只用來確認工具鏈可用，不是前沿数学成果。mathlib尚未加入；正式採用時要選匹配的Lean與固定mathlib revision／manifest。具名公理審計只涵蓋claims清單；新增正式定理需註冊、匯入並另審自然語言目標是否一致。

## 下一輪主線

| 學科 | 首輪目標 |
|---|---|
| 數學 | MATH-001：小n、已知構造、精確determinant驗證及故意共線負例 |
| 物理 | PHYS-001：凍結可負擔模型，驗證能量平衡與結構函數基線 |
| 生物 | BIO-001：公開資料授權、跨donor／cell-context留出與簡單基線 |
| 化學 | CHEM-004：良性中性分子小資料集的單位、標準態與參照核對 |

每科先跑一條閉環，其餘排隊。首輪仍須重新查文獻，不因題卡在今日建立就省略。

## 未做及能力邊界

1. 原創研究輪次仍為0；沒有宣稱任何一題已由本庫解決。40題的專用 evaluator／完整重現尚未實作。
2. 初始來源篩查不是完整文獻審計；部分只讀到摘要，題卡已標示。本次沒有宣稱全網所有來源均已讀完。
3. CI驗記錄及已配置的Lean目標，不會自行全網搜尋或判定自然界真相。聯網檢索由正在工作的agent執行；審核者要核實來源與解答範圍。
4. 沒有設定常駐agent、定時研究、付費API、GPU、濕實驗或新的資料存取權限。對話結束後不會自動持續跑研究。
5. CODEOWNERS和文件已寫，GitHub伺服器端required reviews/checks與分支保護尚未設定，不能把治理約定誤當已啟用技術鎖。
6. 本機嘗試clone五庫時遇到DNS無法解析github.com，沒有完成本機全庫回讀；交付驗收依據是GitHub連接器的提交讀取、遠端CI與job結果。治理腳本本機單元測試是在先前已建立的本機檔案上執行。
