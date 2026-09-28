#!/usr/bin/env python3
"""Build audit JSON v3 (schema-first single truth source). Run once; the
markdown is then rendered by render_frontier_audit.py. Not part of CI."""
import json

def q(cat, query, engine, outcome):
    return {"category": cat, "query": query, "engine": engine,
            "started_at": None, "completed_at": None,
            "timestamp_status": "UNKNOWN", "outcome": outcome}

def src(url, doi, title, authors, year, version, kind, supports, license_=None):
    return {"url": url, "doi": doi, "title": title, "authors": authors,
            "year": year, "version": version, "kind": kind,
            "accessed_at": None, "accessed_on_date": "2026-09-27",
            "timestamp_status": "DATE_ONLY_KNOWN", "read_mode": "abstract-level",
            "revision_status": "unverified", "supports": supports,
            "license_if_relevant": license_}

problems = []

for pid, repo, pm, extra in [
    ("MATH-001", "FrontierMath",
     "arXiv:2602.07751 (Prellberg 2026, v1); Flammenkamp record page 2026-09-11",
     {"newest_bound": "2n for all n<=74 except 75; record n=76; smallest open n=75",
      "note": "full four-way maps in repo runs/*/LITERATURE_MAP.md; BLOCKED-on-frontier-configs retracted after dsk evidence: n=71-76 public configs available (431,008-file verified by glm), n=75 unique zero"}),
    ("PHYS-001", "FrontierPhysics", "arXiv:2607.26896 (Mukherjee & Mukherjee 2026, v1)",
     {"newest_bound": "K41 synthetic baseline calibrated (two-stage); triadic-suppression 2026-03 mechanism study",
      "note": "beta=3 slope is a window-dependent statistic, not a clean exponent (dsk audit)"}),
    ("BIO-001", "FrontierBiology", "Wei et al. Nat Methods 2025; PerturbVAE leakage-aware benchmark",
     {"newest_bound": "leakage gap quantified (PerturbVAE 0.522->0.257; glm synthetic 0.878)", "note": ""}),
    ("CHEM-004", "FrontierChemistry", "Moore et al. JACS 2026 (abstract-level); FreeSolv v0.52",
     {"newest_bound": "GAFF calc-vs-exp MAE 1.114 kcal/mol reproduced; C4 passes under true Murcko split",
      "note": "FreeSolv CC BY 4.0 reviewed"})]:
    problems.append({
        "problem_id": pid, "repo": repo, "search_status": "FOUR_WAY_COMPLETE",
        "checked_at": None, "checked_date": "2026-09-27",
        "timestamp_status": "DATE_ONLY_KNOWN",
        "engine": "zcode-websearch(web_search_prime)/zcode-webfetch/curl",
        "queries": "see repo LITERATURE_MAP (4 categories, >=4 distinct queries, recorded per round)",
        "sources": [{"url": None, "doi": None, "title": pm, "authors": None,
                     "year": 2026, "version": None, "kind": "primary",
                     "accessed_at": None, "accessed_on_date": "2026-09-27",
                     "read_mode": "abstract-level+round-evidence",
                     "revision_status": "checked v1-only (MATH/PHYS)",
                     "supports": "primary of the problem",
                     "license_if_relevant": None}],
        "conclusion_scope": "no resolution found for the problem scope (four-way supported); details in repo LITERATURE_MAP + REMEDIATION",
        "claims_published": True, "extra": extra})

cs = {"problem_id": "CS-001", "repo": "FrontierComputerScience",
      "search_status": "FOUR_WAY_COMPLETE", "checked_at": None,
      "checked_date": "2026-09-27", "timestamp_status": "UNKNOWN",
      "engine": "zcode-websearch(web_search_prime)",
      "queries": [
        q("general", "repository-scale formal verification large Lean codebase proof automation 2026", "zcode-websearch", "located VeriSoftBench/APE-Bench line of work"),
        q("discipline", "arXiv 2602.18307 proof obligations dependencies", "zcode-websearch", "primary confirmed: VeriSoftBench 500 obligations/23 repos (COLM 2026)"),
        q("solution", "VeriSoftBench Lean repository proof automation solved status limitations criticism", "zcode-websearch", "frontier models solve far fewer than mathlib-backed benchmarks; repo-scale unsolved"),
        q("criticism", "automated proof engineering repository scale unsolved challenges erratum retraction 2026", "zcode-websearch", "no erratum/retraction found")],
      "sources": [
        src("https://arxiv.org/abs/2602.18307", "10.48550/arXiv.2602.18307", "VeriSoftBench: Repository-Scale Formal Verification Benchmarks for Lean", "Yutong Xin; Qiaochu Chen; Greg Durrett; Isil Dillig", 2026, "v1", "primary", "benchmark existence/scale/unsolved pass rates"),
        src("https://github.com/utopia-group/VeriSoftBench", None, "VeriSoftBench GitHub", None, 2026, None, "secondary", "dataset detail")],
      "conclusion_scope": "FOUR_WAY_COMPLETE: no same-scope resolution or erratum found; repo-scale verification unsolved for frontier models",
      "claims_published": True, "evaluator_maturity": "none",
      "next_smallest_action": "baseline pass-rate reproduction on VeriSoftBench subset"}
problems.append(cs)

stat = json.loads(json.dumps(cs))
stat.update({"problem_id": "STAT-001", "repo": "FrontierStatistics",
  "queries": [
    q("general", "conformal prediction distribution shift coverage guarantee 2026 open problems", "zcode-websearch", "active open area; 2602.14913 pseudo-calibrated CP"),
    q("discipline", "arXiv 2403.15025 conformal prediction covariate shift calibration", "zcode-websearch", "primary confirmed: Robust CP via Physics-Informed SCM"),
    q("solution", "conformal prediction shift robust methods comparison weighted quantile 2025 2026", "zcode-websearch", "canonical baselines: Tibshirani WCP 2019, Gibbs-Candes ACI"),
    q("criticism", "conformal prediction shift miscalibration empirical failure overconfident", "zcode-websearch", "marginal!=conditional; density-ratio fragility; long-tail imbalance")],
  "sources": [
    src("https://arxiv.org/abs/2403.15025", "10.48550/arXiv.2403.15025", "Robust Conformal Prediction under Distribution Shift via Physics-Informed SCM", None, 2024, "v1", "primary", "card primary exists; SCM-robust CP"),
    src("https://arxiv.org/abs/1904.06019", "10.48550/arXiv.1904.06019", "Conformal Prediction Under Covariate Shift", "RJ Tibshirani; R Barber; E Candes; A Ramdas", 2019, None, "secondary", "canonical WCP baseline")],
  "conclusion_scope": "FOUR_WAY_COMPLETE: no same-scope resolution; shift-robust coverage open with known criticism lines",
  "next_smallest_action": "WCP/ACI/split-conformal reproduction on standard covariate-shift simulation"})
problems.append(stat)

meta = json.loads(json.dumps(cs))
meta.update({"problem_id": "META-001", "repo": "FrontierMetaScience",
  "queries": [
    q("general", "AI agent paper reproduction benchmark success rate environment setup execution failures 2026", "zcode-websearch", "PaperBench/FIRE-Bench landscape; low replication scores"),
    q("discipline", "arXiv 2609.11117 agent-based experiment reproduction bottleneck", "zcode-websearch", "primary confirmed: AgentActionBench 150 papers; execution primary bottleneck"),
    q("solution", "PaperBench FIRE-Bench MLAgentBench RE-Bench approaches", "zcode-websearch", "existing approaches and their scopes"),
    q("criticism", "agent benchmarks broken gameable flawed evaluation critique", "zcode-websearch", "contamination/gamability critiques; SWE-bench issues")],
  "sources": [
    src("https://arxiv.org/abs/2609.11117", "10.48550/arXiv.2609.11117", "Overview of the NLPCC 2026 Shared Task 11: Agent-Based Experiment Reproduction", "Hanhua Hong et al.", 2026, "v1", "primary", "AgentActionBench; execution primary bottleneck"),
    src("https://arxiv.org/abs/2504.01848", "10.48550/arXiv.2504.01848", "PaperBench: Evaluating AI's Ability to Replicate AI Research", "OpenAI", 2025, None, "secondary", "low replication scores for top agents")],
  "conclusion_scope": "FOUR_WAY_COMPLETE: no same-scope resolution; execution bottleneck acknowledged; benchmark-gamability critiques constrain evaluator design",
  "next_smallest_action": "failure-stage classification reproduction on public AgentActionBench subset"})
problems.append(meta)

blocked = [
 ("MAT-003", "FrontierMaterials", "https://www.nature.com/articles/s44160-026-01027-2", "virtual stability to synthesizability gap"),
 ("ASTRO-003", "FrontierAstronomy", "https://www.nature.com/articles/s41550-026-02934-2", "JWST Little Red Dots physical nature"),
 ("EARTH-003", "FrontierEarth", "https://www.nature.com/collections/bfjaccgaaj", "earthquake forecast/early-warning calibration"),
 ("NEURO-001", "FrontierNeuroscience", "https://www.nature.com/articles/s41583-026-01070-0", "model-disagreement stimulus design"),
 ("ECON-001", "FrontierEconomics", "https://www.nber.org/papers/w34984", "AI firm-level causal productivity effects"),
 ("ENG-004", "FrontierEngineering", "https://www.nature.com/articles/s41598-026-53809-5", "uncertainty transport in non-smooth hybrid systems"),
 ("MED-001", "FrontierMedicine", "https://www.nature.com/articles/s41591-025-04184-7", "medical AI external validation"),
 ("SOC-008", "FrontierSocialScience", "https://www.nature.com/articles/s41562-026-02553-x", "causal-claim validity in observational social science")]
for pid, repo, url, title in blocked:
    problems.append({"problem_id": pid, "repo": repo, "search_status": "BLOCKED",
        "checked_at": None, "checked_date": "2026-09-27",
        "timestamp_status": "DATE_ONLY_KNOWN",
        "engine": None, "queries": [],
        "sources": [{"url": url, "doi": None, "title": title, "authors": None,
                     "year": 2026, "version": None, "kind": None,
                     "accessed_at": None, "accessed_on_date": None,
                     "timestamp_status": "UNKNOWN", "read_mode": "card-metadata-only",
                     "revision_status": None, "supports": None,
                     "license_if_relevant": None}],
        "conclusion_scope": "NO CONCLUSIONS PUBLISHED",
        "reason": "four-way search + >=2 sources incl. primary not completed this wave (context budget)",
        "claims_published": False,
        "next_smallest_action": "full four-way search per RESEARCH_PROTOCOL"})

screen = [
 ("MATH-004", "FrontierMath", "cap set asymptotics; EG 2.756^n + Jiang sqrt(n) stand; no 2025-26 exponential improvement found"),
 ("MATH-006", "FrontierMath", "Frankl union-closed; Gilmer 0.38 -> AHS 2024; 1/2 open"),
 ("MATH-010", "FrontierMath", "Theta(C7) in [3.2596, 3.3177]; alpha(C7^5)=368"),
 ("PHYS-003", "FrontierPhysics", "sign problem open; DQ2MC 2026-08; no generic unbiased sampler"),
 ("BIO-002", "FrontierBiology", "GRN causal identifiability open (latent confounders/cycles/soft interventions)"),
 ("BIO-010", "FrontierBiology", "random CV overoptimistic for SDM transfer; spatio-temporal CV (Koldasbayeva 2025)"),
 ("CHEM-003", "FrontierChemistry", "liquid-phase barrier extrapolation: no consensus cross-condition evaluation"),
 ("CHEM-010", "FrontierChemistry", "uMLIP false positives + DFT ~7%; prospective-validation gap")]
for pid, repo, note in screen:
    problems.append({"problem_id": pid, "repo": repo,
        "search_status": "SCREENING_ONLY", "checked_at": None,
        "checked_date": "2026-09-27", "timestamp_status": "DATE_ONLY_KNOWN",
        "engine": "zcode-websearch(web_search_prime)", "queries": [], "sources": [],
        "conclusion_scope": "SCREENING OBSERVATIONS ONLY (1-2 queries; four-way pending; no erratum/resolution claims are supported at this level)",
        "screening_note": note, "claims_published": False,
        "next_smallest_action": "complete four-way search per RESEARCH_PROTOCOL"})

audit = {"version": 3, "generated_by": "glm",
         "wave": "scout-sweep (convergence revision)",
         "single_truth_source": "audits/frontier_audit_2026-09-28.json (markdown is RENDERED, do not hand-edit)",
         "renderer": "audits/render_frontier_audit.py",
         "timestamp_policy": "timezone-qualified timestamps where recorded; UNKNOWN where not recoverable; date-only marked DATE_ONLY_KNOWN",
         "status_note": "no problem status modified; no candidate_for_resolution_review flags; 'no resolution found' appears ONLY on FOUR_WAY_COMPLETE entries",
         "problems": problems}
json.dump(audit, open("audits/frontier_audit_2026-09-28.json", "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("json v3:", len(problems), "entries")
