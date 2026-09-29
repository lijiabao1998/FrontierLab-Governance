# Frontier Audit v3｜2026-09-28｜glm scout sweep（Codex convergence 修訂）

**單一真相源**：`frontier_audit_2026-09-28.json`；本檔由 `audits/render_frontier_audit.py` 自動生成——**請勿手改**，CI 以 render 後 `git diff --exit-code` 防 drift。

- 條目數：23（15 個 repo primaries＋8 個 priority-A screening 題）
- 時間戳政策：timezone-qualified timestamps where recorded; UNKNOWN where not recoverable; date-only marked DATE_ONLY_KNOWN
- 狀態：no problem status modified; no candidate_for_resolution_review flags; 'no resolution found' appears ONLY on FOUR_WAY_COMPLETE entries
- 四路完成定義：general/discipline/solution/criticism＋≥2 來源（含 ≥1 primary）；「no resolution found」僅出現在 FOUR_WAY_COMPLETE 條目。

## 覆蓋總表

| problem_id | repo | search_status | claims_published | conclusion_scope |
|---|---|---|---|---|
| MATH-001 | FrontierMath | FOUR_WAY_COMPLETE | True | no resolution found for the problem scope (four-way supported); details in repo LITERATURE |
| PHYS-001 | FrontierPhysics | FOUR_WAY_COMPLETE | True | no resolution found for the problem scope (four-way supported); details in repo LITERATURE |
| BIO-001 | FrontierBiology | FOUR_WAY_COMPLETE | True | no resolution found for the problem scope (four-way supported); details in repo LITERATURE |
| CHEM-004 | FrontierChemistry | FOUR_WAY_COMPLETE | True | no resolution found for the problem scope (four-way supported); details in repo LITERATURE |
| CS-001 | FrontierComputerScience | FOUR_WAY_COMPLETE | True | FOUR_WAY_COMPLETE: no same-scope resolution or erratum found; repo-scale verification unso |
| STAT-001 | FrontierStatistics | FOUR_WAY_COMPLETE | True | FOUR_WAY_COMPLETE: no same-scope resolution; shift-robust coverage open with known critici |
| META-001 | FrontierMetaScience | FOUR_WAY_COMPLETE | True | FOUR_WAY_COMPLETE: no same-scope resolution; execution bottleneck acknowledged; benchmark- |
| MAT-003 | FrontierMaterials | BLOCKED | False | NO CONCLUSIONS PUBLISHED |
| ASTRO-003 | FrontierAstronomy | BLOCKED | False | NO CONCLUSIONS PUBLISHED |
| EARTH-003 | FrontierEarth | BLOCKED | False | NO CONCLUSIONS PUBLISHED |
| NEURO-001 | FrontierNeuroscience | BLOCKED | False | NO CONCLUSIONS PUBLISHED |
| ECON-001 | FrontierEconomics | BLOCKED | False | NO CONCLUSIONS PUBLISHED |
| ENG-004 | FrontierEngineering | BLOCKED | False | NO CONCLUSIONS PUBLISHED |
| MED-001 | FrontierMedicine | BLOCKED | False | NO CONCLUSIONS PUBLISHED |
| SOC-008 | FrontierSocialScience | BLOCKED | False | NO CONCLUSIONS PUBLISHED |
| MATH-004 | FrontierMath | SCREENING_ONLY | False | SCREENING OBSERVATIONS ONLY (1-2 queries; four-way pending; no erratum/resolution claims a |
| MATH-006 | FrontierMath | SCREENING_ONLY | False | SCREENING OBSERVATIONS ONLY (1-2 queries; four-way pending; no erratum/resolution claims a |
| MATH-010 | FrontierMath | SCREENING_ONLY | False | SCREENING OBSERVATIONS ONLY (1-2 queries; four-way pending; no erratum/resolution claims a |
| PHYS-003 | FrontierPhysics | SCREENING_ONLY | False | SCREENING OBSERVATIONS ONLY (1-2 queries; four-way pending; no erratum/resolution claims a |
| BIO-002 | FrontierBiology | SCREENING_ONLY | False | SCREENING OBSERVATIONS ONLY (1-2 queries; four-way pending; no erratum/resolution claims a |
| BIO-010 | FrontierBiology | SCREENING_ONLY | False | SCREENING OBSERVATIONS ONLY (1-2 queries; four-way pending; no erratum/resolution claims a |
| CHEM-003 | FrontierChemistry | SCREENING_ONLY | False | SCREENING OBSERVATIONS ONLY (1-2 queries; four-way pending; no erratum/resolution claims a |
| CHEM-010 | FrontierChemistry | SCREENING_ONLY | False | SCREENING OBSERVATIONS ONLY (1-2 queries; four-way pending; no erratum/resolution claims a |

### MATH-001｜FrontierMath｜FOUR_WAY_COMPLETE

- checked：2026-09-27（DATE_ONLY_KNOWN）；engine：zcode-websearch(web_search_prime)/zcode-webfetch/curl

#### queries

| category | query | engine | started_at | completed_at | outcome |
|---|---|---|---|---|---|
| (repo-recorded) | see repo LITERATURE_MAP (4 categories, >=4 distinct queries, recorded per round) | (see repo) | | | per-round records in repo LITERATURE_MAP |

#### sources

| kind | title | url/doi | year | version | read_mode | supports |
|---|---|---|---|---|---|---|
| primary | arXiv:2602.07751 (Prellberg 2026, v1); Flammenkamp record page 2026-09-11 | null | 2026 | None | abstract-level+round-evidence | primary of the problem |

- conclusion_scope：no resolution found for the problem scope (four-way supported); details in repo LITERATURE_MAP + REMEDIATION
- newest_bound：2n for all n<=74 except 75; record n=76; smallest open n=75
- note：full four-way maps in repo runs/*/LITERATURE_MAP.md; BLOCKED-on-frontier-configs retracted after dsk evidence: n=71-76 public configs available (431,008-file verified by glm), n=75 unique zero

### PHYS-001｜FrontierPhysics｜FOUR_WAY_COMPLETE

- checked：2026-09-27（DATE_ONLY_KNOWN）；engine：zcode-websearch(web_search_prime)/zcode-webfetch/curl

#### queries

| category | query | engine | started_at | completed_at | outcome |
|---|---|---|---|---|---|
| (repo-recorded) | see repo LITERATURE_MAP (4 categories, >=4 distinct queries, recorded per round) | (see repo) | | | per-round records in repo LITERATURE_MAP |

#### sources

| kind | title | url/doi | year | version | read_mode | supports |
|---|---|---|---|---|---|---|
| primary | arXiv:2607.26896 (Mukherjee & Mukherjee 2026, v1) | null | 2026 | None | abstract-level+round-evidence | primary of the problem |

- conclusion_scope：no resolution found for the problem scope (four-way supported); details in repo LITERATURE_MAP + REMEDIATION
- newest_bound：K41 synthetic baseline calibrated (two-stage); triadic-suppression 2026-03 mechanism study
- note：beta=3 slope is a window-dependent statistic, not a clean exponent (dsk audit)

### BIO-001｜FrontierBiology｜FOUR_WAY_COMPLETE

- checked：2026-09-27（DATE_ONLY_KNOWN）；engine：zcode-websearch(web_search_prime)/zcode-webfetch/curl

#### queries

| category | query | engine | started_at | completed_at | outcome |
|---|---|---|---|---|---|
| (repo-recorded) | see repo LITERATURE_MAP (4 categories, >=4 distinct queries, recorded per round) | (see repo) | | | per-round records in repo LITERATURE_MAP |

#### sources

| kind | title | url/doi | year | version | read_mode | supports |
|---|---|---|---|---|---|---|
| primary | Wei et al. Nat Methods 2025 (published 2025); PerturbVAE 2026 | null | 2025 | None | abstract-level+round-evidence | primary of the problem |

- conclusion_scope：no resolution found for the problem scope (four-way supported); details in repo LITERATURE_MAP + REMEDIATION
- newest_bound：leakage gap quantified (PerturbVAE 0.522->0.257; glm synthetic 0.878)

### CHEM-004｜FrontierChemistry｜FOUR_WAY_COMPLETE

- checked：2026-09-27（DATE_ONLY_KNOWN）；engine：zcode-websearch(web_search_prime)/zcode-webfetch/curl

#### queries

| category | query | engine | started_at | completed_at | outcome |
|---|---|---|---|---|---|
| (repo-recorded) | see repo LITERATURE_MAP (4 categories, >=4 distinct queries, recorded per round) | (see repo) | | | per-round records in repo LITERATURE_MAP |

#### sources

| kind | title | url/doi | year | version | read_mode | supports |
|---|---|---|---|---|---|---|
| primary | Moore et al. JACS 2026 (abstract-level); FreeSolv v0.52 | null | 2026 | None | abstract-level+round-evidence | primary of the problem |

- conclusion_scope：no resolution found for the problem scope (four-way supported); details in repo LITERATURE_MAP + REMEDIATION
- newest_bound：GAFF calc-vs-exp MAE 1.114 kcal/mol reproduced; C4 passes under true Murcko split
- note：FreeSolv CC BY 4.0 reviewed

### CS-001｜FrontierComputerScience｜FOUR_WAY_COMPLETE

- checked：2026-09-27（UNKNOWN）；engine：zcode-websearch(web_search_prime)

#### queries

| category | query | engine | started_at | completed_at | outcome |
|---|---|---|---|---|---|
| general | `repository-scale formal verification large Lean codebase proof automation 2026` | zcode-websearch | None | None | located VeriSoftBench/APE-Bench line of work |
| discipline | `arXiv 2602.18307 proof obligations dependencies` | zcode-websearch | None | None | primary confirmed: VeriSoftBench 500 obligations/23 repos (COLM 2026) |
| solution | `VeriSoftBench Lean repository proof automation solved status limitations criticism` | zcode-websearch | None | None | frontier models solve far fewer than mathlib-backed benchmarks; repo-scale unsolved |
| criticism | `automated proof engineering repository scale unsolved challenges erratum retraction 2026` | zcode-websearch | None | None | no erratum/retraction found |

#### sources

| kind | title | url/doi | year | version | read_mode | supports |
|---|---|---|---|---|---|---|
| primary | VeriSoftBench: Repository-Scale Formal Verification Benchmarks for Lean | https://arxiv.org/abs/2602.18307 | 2026 | v1 | abstract-level | benchmark existence/scale/unsolved pass rates |
| secondary | VeriSoftBench GitHub | https://github.com/utopia-group/VeriSoftBench | 2026 | None | abstract-level | dataset detail |

- conclusion_scope：FOUR_WAY_COMPLETE: no same-scope resolution or erratum found; repo-scale verification unsolved for frontier models
- next-smallest-action：baseline pass-rate reproduction on VeriSoftBench subset

### STAT-001｜FrontierStatistics｜FOUR_WAY_COMPLETE

- checked：2026-09-27（UNKNOWN）；engine：zcode-websearch(web_search_prime)

#### queries

| category | query | engine | started_at | completed_at | outcome |
|---|---|---|---|---|---|
| general | `conformal prediction distribution shift coverage guarantee 2026 open problems` | zcode-websearch | None | None | active open area; 2602.14913 pseudo-calibrated CP |
| discipline | `arXiv 2403.15025 conformal prediction covariate shift calibration` | zcode-websearch | None | None | primary confirmed: Robust CP via Physics-Informed SCM |
| solution | `conformal prediction shift robust methods comparison weighted quantile 2025 2026` | zcode-websearch | None | None | canonical baselines: Tibshirani WCP 2019, Gibbs-Candes ACI |
| criticism | `conformal prediction shift miscalibration empirical failure overconfident` | zcode-websearch | None | None | marginal!=conditional; density-ratio fragility; long-tail imbalance |

#### sources

| kind | title | url/doi | year | version | read_mode | supports |
|---|---|---|---|---|---|---|
| primary | Robust Conformal Prediction under Distribution Shift via Physics-Informed SCM | https://arxiv.org/abs/2403.15025 | 2024 | v1 | abstract-level | card primary exists; SCM-robust CP |
| secondary | Conformal Prediction Under Covariate Shift | https://arxiv.org/abs/1904.06019 | 2019 | None | abstract-level | canonical WCP baseline |

- conclusion_scope：FOUR_WAY_COMPLETE: no same-scope resolution; shift-robust coverage open with known criticism lines
- next-smallest-action：WCP/ACI/split-conformal reproduction on standard covariate-shift simulation

### META-001｜FrontierMetaScience｜FOUR_WAY_COMPLETE

- checked：2026-09-27（UNKNOWN）；engine：zcode-websearch(web_search_prime)

#### queries

| category | query | engine | started_at | completed_at | outcome |
|---|---|---|---|---|---|
| general | `AI agent paper reproduction benchmark success rate environment setup execution failures 2026` | zcode-websearch | None | None | PaperBench/FIRE-Bench landscape; low replication scores |
| discipline | `arXiv 2609.11117 agent-based experiment reproduction bottleneck` | zcode-websearch | None | None | primary confirmed: AgentActionBench 150 papers; execution primary bottleneck |
| solution | `PaperBench FIRE-Bench MLAgentBench RE-Bench approaches` | zcode-websearch | None | None | existing approaches and their scopes |
| criticism | `agent benchmarks broken gameable flawed evaluation critique` | zcode-websearch | None | None | contamination/gamability critiques; SWE-bench issues |

#### sources

| kind | title | url/doi | year | version | read_mode | supports |
|---|---|---|---|---|---|---|
| primary | Overview of the NLPCC 2026 Shared Task 11: Agent-Based Experiment Reproduction | https://arxiv.org/abs/2609.11117 | 2026 | v1 | abstract-level | AgentActionBench; execution primary bottleneck |
| secondary | PaperBench: Evaluating AI's Ability to Replicate AI Research | https://arxiv.org/abs/2504.01848 | 2025 | None | abstract-level | low replication scores for top agents |

- conclusion_scope：FOUR_WAY_COMPLETE: no same-scope resolution; execution bottleneck acknowledged; benchmark-gamability critiques constrain evaluator design
- next-smallest-action：failure-stage classification reproduction on public AgentActionBench subset

### MAT-003｜FrontierMaterials｜BLOCKED

- reason：four-way search + >=2 sources incl. primary not completed this wave (context budget)
- 本條**不發佈任何結論**（claims_published=false）；卡片來源 URL 已登記待四路檢索。

### ASTRO-003｜FrontierAstronomy｜BLOCKED

- reason：four-way search + >=2 sources incl. primary not completed this wave (context budget)
- 本條**不發佈任何結論**（claims_published=false）；卡片來源 URL 已登記待四路檢索。

### EARTH-003｜FrontierEarth｜BLOCKED

- reason：four-way search + >=2 sources incl. primary not completed this wave (context budget)
- 本條**不發佈任何結論**（claims_published=false）；卡片來源 URL 已登記待四路檢索。

### NEURO-001｜FrontierNeuroscience｜BLOCKED

- reason：four-way search + >=2 sources incl. primary not completed this wave (context budget)
- 本條**不發佈任何結論**（claims_published=false）；卡片來源 URL 已登記待四路檢索。

### ECON-001｜FrontierEconomics｜BLOCKED

- reason：four-way search + >=2 sources incl. primary not completed this wave (context budget)
- 本條**不發佈任何結論**（claims_published=false）；卡片來源 URL 已登記待四路檢索。

### ENG-004｜FrontierEngineering｜BLOCKED

- reason：four-way search + >=2 sources incl. primary not completed this wave (context budget)
- 本條**不發佈任何結論**（claims_published=false）；卡片來源 URL 已登記待四路檢索。

### MED-001｜FrontierMedicine｜BLOCKED

- reason：four-way search + >=2 sources incl. primary not completed this wave (context budget)
- 本條**不發佈任何結論**（claims_published=false）；卡片來源 URL 已登記待四路檢索。

### SOC-008｜FrontierSocialScience｜BLOCKED

- reason：four-way search + >=2 sources incl. primary not completed this wave (context budget)
- 本條**不發佈任何結論**（claims_published=false）；卡片來源 URL 已登記待四路檢索。

### MATH-004｜FrontierMath｜SCREENING_ONLY

- 篩查觀察（非結論）：cap set asymptotics; EG 2.756^n + Jiang sqrt(n) stand; no 2025-26 exponential improvement found
- next-smallest-action：complete four-way search per RESEARCH_PROTOCOL

### MATH-006｜FrontierMath｜SCREENING_ONLY

- 篩查觀察（非結論）：Frankl union-closed; Gilmer 0.38 -> AHS 2024; 1/2 open
- next-smallest-action：complete four-way search per RESEARCH_PROTOCOL

### MATH-010｜FrontierMath｜SCREENING_ONLY

- 篩查觀察（非結論）：Theta(C7) in [3.2596, 3.3177]; alpha(C7^5)=368
- next-smallest-action：complete four-way search per RESEARCH_PROTOCOL

### PHYS-003｜FrontierPhysics｜SCREENING_ONLY

- 篩查觀察（非結論）：sign problem open; DQ2MC 2026-08; no generic unbiased sampler
- next-smallest-action：complete four-way search per RESEARCH_PROTOCOL

### BIO-002｜FrontierBiology｜SCREENING_ONLY

- 篩查觀察（非結論）：GRN causal identifiability open (latent confounders/cycles/soft interventions)
- next-smallest-action：complete four-way search per RESEARCH_PROTOCOL

### BIO-010｜FrontierBiology｜SCREENING_ONLY

- 篩查觀察（非結論）：random CV overoptimistic for SDM transfer; spatio-temporal CV (Koldasbayeva 2025)
- next-smallest-action：complete four-way search per RESEARCH_PROTOCOL

### CHEM-003｜FrontierChemistry｜SCREENING_ONLY

- 篩查觀察（非結論）：liquid-phase barrier extrapolation: no consensus cross-condition evaluation
- next-smallest-action：complete four-way search per RESEARCH_PROTOCOL

### CHEM-010｜FrontierChemistry｜SCREENING_ONLY

- 篩查觀察（非結論）：uMLIP false positives + DFT ~7%; prospective-validation gap
- next-smallest-action：complete four-way search per RESEARCH_PROTOCOL

## 方法與限制

- 有界檢索；「無結果」非未解證明；摘要層級閱讀不等於全文審讀。
- 舊版搜尋之精確時戳不可恢復者記 timestamp_status=UNKNOWN，不猜測。
