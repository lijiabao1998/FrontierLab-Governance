# FRONTIER MAP｜2026-09-28｜convergence-2 session

## 已確立（ Replicated / Reviewed ）
- MATH-001：2n 構造 n≤74 除 75 外全解（文獻+glm 獨立重驗 431,008 檔中 71-76 五筆全過 verifier）；36,912/1997 檔全量重驗。n=75 唯一 0 筆（最小未解）。
- MATH-001：n≤5 CNF encoding 正確性（triples+Sinz 雙編碼、窮舉 UNSAT 證書）。
- PHYS-001：K41 合成基線（S2≈2/3、頻譜 5/3 與 3、能量收支機器精度）＋兩段式帶規則（須含絕對下限——cycle-1 零寬帶負結果）。
- BIO-001：Norman metadata 審計（111,445 cells；105 singles/41,759 duals/11,855 controls）；同-T 洩漏示範方法論。
- CHEM-004：FreeSolv v0.52 核對＋GAFF 錨點 MAE 1.114 kcal/mol。

## 負結果（不可刪）
- BIO E2：sibling-free CLEAN 不可構造（train=0）→ E2 INCONCLUSIVE；改以 MODEL_ABLATION（gap 0.8776）另輪記錄，僅宣稱 group 結構訊號。
- BIO donor POST_HOC gap：estimator 敏感（獨立 0.905 vs 主 0.1616）→ contested，不得單獨引用。
- CHEM C4：真 Murcko 下無 scaffold-holdout 劣化（2.647<2.883）→ +0.635/+0.656 宣稱撤回。
- PHYS cycle-1：±4σ 零寬帶退化 → FAIL（負結果保存；cycle-2 floor 規則為修復）。
- PHYS β=3 斜率：窗依賴統計量（非 clean exponent）——dsk 審計，已採納。

## 爭議/未收斂
- PHYS donor/estimator 差異類問題：任何 POST_HOC gap 需聲明 estimator variant。
- CHEM C4 正式結論：需新 admitted round 凍結 RDKit Murcko key。

## 高價值未挖區（依 information gain × 可驗證性排序）
1. MATH-001 n=75 SAT 實戰（bench 已就緒，~20M clauses seq 編碼）
2. MATH-004：r₃(F₃ⁿ) 小 n 精確重現＋多項式方法文獻圖譜（零成本驗證器）
3. PHYS-001 Sabra shell model（三 guards 已規格）
4. BIO-001 真實表達矩陣（numpy in-repo 解除 BLOCKED 後 frozen-vs-random 實測）
5. MATH-006 union-closed 小全集族窮舉＋Gilmer 熵重現
6. CHEM-003 液相障壁基準集授權/單位審計（複用 CHEM-004 模板）
7. 跨 repo：晶體預測假陽性（CHEM-010）×Materials MAT-003 可合成性——同一 problem 兩種切入
