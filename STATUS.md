# 狀態

## 目前（2026-09-28）
- 架構：1 個治理庫 + 15 個研究庫；每個研究庫 10 張初始題卡，共 150 張。
- 研究庫固定的治理版本以各庫 `GOVERNANCE.lock.json` 為準：原始四庫（Math、Physics、Biology、Chemistry）固定 `07d2b130`（protocol 1.0.0），其餘 11 庫固定 `f40beb16`（protocol 1.1.0）。版本語義見 [PROTOCOL_VERSIONS.md](PROTOCOL_VERSIONS.md)。
- 治理 gate 的測試：以 `python3 -m unittest discover -s tests -v` 的實際輸出與遠端 CI 為準；本文件不寫死測試數量。
- 研究輪次：以各研究庫 main 上的 `runs/` 為準；本文件不代記其他分支或未合併 PR 的研究狀態。
- 尚未配置：常駐 agent、API key、付費計算、GitHub 分支保護與 required status checks。文件與 CODEOWNERS 不是伺服器端安全鎖。

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
