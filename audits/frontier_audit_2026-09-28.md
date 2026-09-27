# Frontier Audit｜2026-09-28｜glm scout sweep

範圍：全部 priority A + 各庫 primary problems（12 題）。方法：每題 1-2 條有界檢索（引擎 zcode-websearch）＋本波四輪研究之 LITERATURE_MAP。**不修改任何題卡狀態**；「可能已解」一律只標 `candidate_for_resolution_review`（本次掃描無任何題目觸發此標記）。機器可讀版：`audits/frontier_audit_2026-09-28.json`。

## 跨題總覽

| 題 | 域 | 狀態 | 最新 primary / 錨點 | evaluator 成熟度 | 建議 |
|---|---|---|---|---|---|
| MATH-001 | math | OPEN | Flammenkamp 頁 2026-09-11；Prellberg arXiv:2602.07751 v1 | **高**（r1 整數 verifier×2＋SAT bench r2） | 維持 A；下一輪 n=75 DIMACS 串流求解 |
| MATH-002 | math | OPEN | 未掃（priority B，本輪範圍外） | 無 | — |
| MATH-004 | math | OPEN | Ellenberg–Gijswijt 2.756ⁿ＋Jiang √n（2021）；Tyrrell 下界 2023 | 無 | 維持 A；F3 向量驗證器可立即建 |
| MATH-006 | math | OPEN | Gilmer 0.38（2022）；Alweiss–Huang–Sellke 2024 改進 | 無 | 維持 A；小全集族窮舉+閉包檢查可立即建 |
| MATH-010 | math | OPEN | Θ(C₇)∈[3.2596, 3.3177]；α(C₇⁵)=368 | 無 | 維持 A；α(C₇⁶) 精確計算為攻擊面（重算力，B 級排程考量） |
| PHYS-001 | phys | OPEN | arXiv:2607.26896 v1（再核查無 erratum） | **高**（r1/r2：K41 校準帶） | 維持 A；Sabra 三 guards 已規格 |
| PHYS-002..010 | phys | OPEN | PHYS-003 已掃；其餘本輪範圍外 | 無 | — |
| PHYS-003 | phys | OPEN | DQ²MC（arXiv 2026-08）；sign-problem-free 原理（2026-07） | 無 | 維持 A；小 Hamiltonian 方差/成本對照可建 |
| BIO-001 | bio | OPEN | Wei et al. Nat Methods 2025；PerturbVAE leakage-aware | **高**（r1 split/leak evaluator） | 維持 A；表達矩陣 numpy in-repo 解除 tractability-BLOCKED |
| BIO-002 | bio | OPEN | Dai 2025（latent confounders）；CausalGRN 2025-12 | 無 | 維持 A；合成真值+擾動分離驗證器可立即建 |
| BIO-010 | bio | OPEN | Koldasbayeva 2025 spatio-temporal CV | 無 | 維持 A；空間區塊留出基線可立即建 |
| CHEM-003 | chem | OPEN | RSC PCCP 液相 Δ‡G 基準集；MiFEA 2025 | 無 | 維持 A；反應族/溶劑留出對照可立即建 |
| CHEM-004 | chem | OPEN | Moore 2026 JACS（摘要層級）；FreeSolv v0.52 | **高**（r1 validator+split+負控） | 維持 A；RDKit in-repo 後真 Murcko split |
| CHEM-010 | chem | OPEN | uMLIP 評測 2025（Loew npj）；假陽性率 ~7% 即 DFT 亦然（Jakob 2025） | 無 | 維持 A；hull 參照+固定切分可立即建 |

## 逐題要點（僅列本輪新掃描之 8 題；四 primary 題詳見各 repo 之 LITERATURE_MAP）

### MATH-004（Cap set 漸近增長率）
- open status uncertainty：低——EG 界 2.756ⁿ 穩固，無 2025-26 新指數改進之宣稱。
- claimed resolution / erratum：無。
- newest bound：上界 cⁿ√n（Jiang 2021）；下界 Tyrrell 2023。
- evaluator maturity：無——**第一輪可建**：F3 向量加法與無三項 AP 結構驗證（小 n 窮舉＋確定性驗證器，stdlib 可行）。
- data availability：不需要外部資料。tractability：驗證器容易；漸近改善屬理論突破（低機率高價值）。
- next-smallest-action：n≤6 之 r₃(F₃ⁿ) 精確值重現＋行列式/多項式方法文獻圖譜。
- priority change：維持 A。

### MATH-006（Frankl union-closed）
- open status uncertainty：低——½ 猜想 open；常數下界 ~0.38-0.40（Gilmer→AHS 2024）。
- claimed resolution / erratum：無（2025-26 有 cross-union 特例證明，非全解）。
- evaluator maturity：無——第一輪：小全集族窮舉＋閉包檢查＋頻率統計（stdlib 可行）。
- next-smallest-action：m≤12 全 union-closed 族之 enumerative 基線＋Gilmer 熵方法之數值重現。
- priority change：維持 A。

### MATH-010（C7 Shannon capacity）
- open status uncertainty：低——[3.2596, 3.3177] 區間穩定多年。
- evaluator maturity：無——α(C₇⁵)=368 可作獨立重現目標（強積圖獨立數，精確整數）；α(C₇⁶) 計算重算力大（B 級排程考量）。
- next-smallest-action：重現 α(C₇⁵)=368（獨立整數驗證）＋Lovász theta 上界之 SDP 重現（需 SDP 工具，stdlib 外）。
- priority change：維持 A（重現部分）／實際推界建議降 B（算力）。

### PHYS-003（符號問題與無偏取樣）
- open status uncertainty：低——通用解不存在；2026 有量子混合（DQ²MC）與 sign-problem-free 原理之進展線。
- evaluator maturity：無——第一輪：固定小 Hamiltonian（如 4×4 Hubbard），比較行列式 QMC 方差 vs 能量/粒子數守恆檢查（stdlib 可行，精度注意）。
- next-smallest-action：小模型符號方差增長曲線重現（文獻已知）＋無偏估計器基線。
- priority change：維持 A。

### BIO-002（GRN 因果可識別性）
- open status uncertainty：低——latent confounders/迴路/soft intervention 為公認未解（Dai 2025 等）。
- evaluator maturity：無——第一輪：合成真值（已知 DAG+干預）之可識別性驗證器＋公開擾動資料分離（stdlib 可行）。
- data availability：合成自足；真實資料同 BIO-001 之 GEO 管道。
- next-smallest-action：合成 DAG 可識別性 testbed（engine 依賴圖＋噪聲條件掃描）。
- priority change：維持 A。

### BIO-010（物種分布時空外推）
- open status uncertainty：低——random CV 過樂觀已定量化（Koldasbayeva 2025）。
- evaluator maturity：無——第一輪：空間區塊留出 vs random CV 之對照（合成或小型公開 GBIF 子集）。
- data availability：GBIF 公開（license 逐資料集審計）。
- next-smallest-action：區塊留出模板＋偏差/校準基線。
- priority change：維持 A。

### CHEM-003（液相自由能障壁條件外推）
- open status uncertainty：中——反應基準集存在（RSC PCCP）但跨條件外推無共識評估。
- evaluator maturity：無——第一輪：反應族/溶劑留出對照（用公開基準集之子集）。
- next-smallest-action：資料集授權/單位審計（沿用 CHEM-004 模板）。
- priority change：維持 A。

### CHEM-010（晶體穩定性→前瞻發現）
- open status uncertainty：中——uMLIP 假陽性問題已量化（DFT 本身 ~7%），前瞻驗證缺口明確（Shiryaev 2026 綜述）。
- evaluator maturity：無——第一輪：固定資料切分＋hull 參照一致性檢查（需 Materials Project 授權審計）。
- next-smallest-action：MP 授權審計＋公開 hull 資料之切分驗證器。
- priority change：維持 A。

## 方法與限制
- 每題 1-2 query 有界檢索＋摘要層級閱讀；本波四輪（MATH-001/PHYS-001/BIO-001/CHEM-004）另有完整 LITERATURE_MAP。
- 搜尋引擎首次批次逾時，重試後完成——覆蓋非窮盡；「無結果」非未解證明。
- 無任何題目發現同範圍解答宣稱或 erratum；無 candidate_for_resolution_review 標記。
