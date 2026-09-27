# Frontier Audit v2｜2026-09-28｜glm scout sweep（Codex review 修訂版）

**Scope（依 Codex P2-1 修正）**：涵蓋 registry 全部 **15 個 repo 的 primary problems**——原四庫（MATH-001、PHYS-001、BIO-001、CHEM-004，另有完整 LITERATURE_MAP 於各 repo）＋擴充 11 庫之 primary（CS-001、STAT-001、MAT-003、ASTRO-003、EARTH-003、NEURO-001、ECON-001、ENG-004、MED-001、SOC-008、META-001；來源：`EXPANSION-2026-09-28.md`）。
**搜尋狀態**：四路完成＝MATH-001、PHYS-001、BIO-001、CHEM-004（完整輪次）、CS-001、STAT-001、META-001；**BLOCKED（四路檢索待做，不發佈結論）**＝MAT-003、ASTRO-003、EARTH-003、NEURO-001、ECON-001、ENG-004、MED-001、SOC-008。原 12 題 priority-A 掃描中 8 題僅 1-2 query——其結論降級為 screening-level，四路補齊列為待辦（Codex P2-2）。
**不修改任何題卡狀態**；本次掃描無 candidate_for_resolution_review 觸發。

## 15 primaries 逐題（含完整檢索紀錄者標 ✎）

### ✎ CS-001｜Repository-scale 軟體形式驗證（FrontierComputerScience）
- 檢索（2026-09-28T19:5xZ，zcode-websearch）：general=`repository-scale formal verification large Lean codebase proof automation 2026`；discipline=`arXiv 2602.18307 proof obligations dependencies`；solution=`VeriSoftBench Lean repository proof automation solved status limitations criticism`；criticism=`automated proof engineering repository scale unsolved challenges erratum retraction 2026`。
- 來源：primary＝arXiv:2602.18307（VeriSoftBench，Xin/Chen/Durrett/Dillig，COLM 2026；經 COLM2026 HF dataset 引用核實）；secondary＝utopia-group/VeriSoftBench GitHub、APE-Bench (OpenReview)、Vero。
- 判讀：open——repo 規模驗證對前沿模型仍未解（VeriSoftBench pass rate 遠低於 Mathlib-backed 基準之 ~90%）；無 erratum。批評線：數學 Lean 基準表現不能外推到真實 repo。
- evaluator maturity：無（benchmark 已存在，題卡 evaluator 待建）。next-smallest-action：以 VeriSoftBench 子集建立本庫基線 pass-rate 重現。
- priority：維持 primary。

### ✎ STAT-001｜Distribution shift 下的 conformal coverage（FrontierStatistics）
- 檢索：general=`conformal prediction distribution shift coverage guarantee 2026 open problems`；discipline=`arXiv 2403.15025 covariate shift calibration`；solution=`conformal prediction shift robust methods comparison weighted quantile 2025 2026`；criticism=`conformal prediction shift miscalibration empirical failure overconfident`。
- 來源：primary＝arXiv:2403.15025（Robust CP via Physics-Informed SCM，實證存在）；secondary＝arXiv:2602.14913（pseudo-calibrated CP）、Tibshirani et al. NeurIPS 2019（WCP，1200+ 引用）、Gibbs & Candès JMLR 2024（ACI）、ICML 2026 domain-shift-aware CP、arXiv 2601.00908（診斷 CP 失效）。
- 判讀：open——shift 下 coverage 恢復為活躍未解方向；批評線：marginal≠conditional coverage、density-ratio 估計脆弱、long-tail 類內失衡。
- next-smallest-action：WCP/ACI/split conformal 三基線在標準 covariate-shift 模擬之重現（stdlib 可行）。
- priority：維持 primary。

### ✎ META-001｜Agent-based experiment reproduction 的 execution bottleneck（FrontierMetaScience）
- 檢索：general=`AI agent paper reproduction benchmark success rate environment setup execution failures 2026`；discipline=`arXiv 2609.11117`；solution=`PaperBench FIRE-Bench MLAgentBench RE-Bench approaches`；criticism=`agent benchmarks broken gameable flawed evaluation critique`。
- 來源：primary＝arXiv:2609.11117（NLPCC 2026 Shared Task 11 overview；AgentActionBench，150 papers，**execution 為主要 bottleneck**——摘要層級）；secondary＝PaperBench（OpenAI, arXiv:2504.01848）、FIRE-Bench、「AI Agent Benchmarks are Broken」（Kang）、SWE-bench 污染批評線。
- 判讀：open——執行/環境 setup 為公認主要失敗點；批評線：agent benchmark 本身有 gamability/contamination 問題（本庫 evaluator 設計須預防）。
- next-smallest-action：以 AgentActionBench 公開子集做失敗階段分類重現（stdlib 可行部分：literature/metric matching 階段）。
- priority：維持 primary。

### BLOCKED 題（8）——僅列卡片元資料，不發佈結論
| ID | repo | title | card source（未讀全文） | search_status |
|---|---|---|---|---|
| MAT-003 | FrontierMaterials | 虛擬穩定性到可合成性的落差 | nature.com s44160-026-01027-2 | BLOCKED |
| ASTRO-003 | FrontierAstronomy | Little Red Dots 的物理本質 | nature.com s41550-026-02934-2 | BLOCKED |
| EARTH-003 | FrontierEarth | 地震 forecast 與 early warning 校準 | nature.com collections/bfjaccgaaj | BLOCKED |
| NEURO-001 | FrontierNeuroscience | 模型分歧設計可區分腦計算假說刺激 | nature.com s41583-026-01070-0 | BLOCKED |
| ECON-001 | FrontierEconomics | AI 的 firm-level 因果生產力效果 | nber.org/papers/w34984 | BLOCKED |
| ENG-004 | FrontierEngineering | Non-smooth hybrid systems 的 uncertainty transport | nature.com s41598-026-53809-5 | BLOCKED |
| MED-001 | FrontierMedicine | 醫療 AI 跨機構 external validation | nature.com s41591-025-04184-7 | BLOCKED |
| SOC-008 | FrontierSocialScience | Observational causal-claim validity | nature.com s41562-026-02553-x | BLOCKED |
- BLOCKED 原因：本波 context/預算不足以對每題完成四路＋≥2 來源（含 primary）閱讀；依 RESEARCH_PROTOCOL 不在檢索不足下發佈結論。解除：下一波逐題四路（每題約 4 query＋primary 閱讀）。

## 原四庫 A 題（12）——狀態更新
- 四 primary（MATH-001/PHYS-001/BIO-001/CHEM-004）：完整 LITERATURE_MAP 見各 repo runs/*；本次 Remediation wave 修正後數字以各 repo REMEDIATION.md 為準。
- 其餘 8 題（MATH-004/006/010、PHYS-003、BIO-002/010、CHEM-003/010）：**search_status=screening_level（1-2 query）**；前版「low open-status uncertainty／no erratum」結論降級為「篩查層級觀察」，四路補齊前排程在 META-001 之後。逐題觀察與 next-smallest-action 詳見 v1 audit（本 repo 同目錄 json）。

## 方法與限制
- 所有 query 原字串、引擎、來源 URL/DOI、時間、kind、supports 已記錄於 `frontier_audit_2026-09-28.json`（v2）。
- 檢索為有界；「無結果」非未解證明；摘要層級閱讀不等於全文審讀。
