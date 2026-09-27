# 狀態｜2026-09-27 bootstrap

主線：治理與可重現基線先行，各科 10 題；先一科一題跑通，再擴並行。

- 已建立：研究協議、角色與 PR 流程、來源與完成狀態政策、Python per-round gate、反向測試、共用 CI。
- 本機已執行：15 個 unittest 測試方法通過，含每項漏填檢查、舊搜尋、缺 primary、重複來源、無支持完成、子題誤關父題等拒絕案例。
- 尚未由此紀錄宣稱：GitHub 遠端 CI 通過、Lean 通過、任何問題被本庫解決、資料集實際重現。
- 尚未配置：常駐 agent、API key、付費計算、GitHub 分支保護。文件與 CODEOWNERS 不是伺服器端安全鎖。

下一步：四個研究倉庫固定本治理 commit，跑 schema／gate CI；首輪各選 README 的基線任務，先做新的文獻檢索，不直接進發現模式。


## 2026-09-28 擴充
研究線由4科擴充到15個學科／元科學repo；目標初始問題卡總數150。治理工具新增 CS、STAT、MAT、ASTRO、EARTH、NEURO、ECON、ENG、MED、SOC、META 問題ID支援。新增repo仍須各自固定本治理commit並先通過CI，不能因框架存在就宣稱任何研究問題已解。
