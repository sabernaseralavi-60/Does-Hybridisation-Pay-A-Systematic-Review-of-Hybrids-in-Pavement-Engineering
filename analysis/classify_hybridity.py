#!/usr/bin/env python3
"""
classify_hybridity.py
======================
Adds a `hybrid_type` column to seed_bibliography.csv, hand-verified per record
against the structural definition in docs/01_SCOPE_AND_TAXONOMY.md §2 (not a
keyword heuristic — a heuristic pass was run first and every label below was
checked against the record's architecture/optimizer/note fields by hand).

Values: H1-H7 (may be multiple, semicolon-separated), or:
  "none"          — not a hybrid under the structural definition (single-family
                    model, or a metaheuristic-named paper that runs the two
                    components as separate competing models rather than coupled)
  "context"       — landmark/comparator/survey paper kept in the database for
                    citation context, not a hybridity data point
  "not-yet-coded" — primary study not yet classified (full-text needed)

This is the file Figure 2 (taxonomy distribution) and Table (premium candidates)
are built from. Re-run whenever new records are added to the CSV.
"""

import csv
from pathlib import Path

# doi -> (hybrid_type, reasoning)  — reasoning is for the audit trail, not written to CSV
CLASSIFICATION = {
    # --- H1: metaheuristic/statistical search over hyperparameters ---
    "10.1177/03611981241245991": ("H3", "PINN with Optuna hyperparameter search; H3 dominates, Optuna use is incidental"),
    "10.28991/cej-2025-011-01-06": ("none", "per-algorithm tuning, no metaheuristic coupling — this IS the tuned-baseline exemplar, not a hybrid"),
    "10.1186/s44147-025-00706-9": ("H1", "PSO tunes SVR hyperparameters"),
    "10.3390/ma18122913": ("H5", "heterogeneous stacking with CV-leakage-aware meta-learner; Bayesian opt is base-model tuning only"),
    "10.1016/j.jtte.2016.09.007": ("H7", "GEP output feeds an ANN refinement stage — symbolic-numeric coupling"),
    "10.1016/j.conbuildmat.2025.143050": ("H2", "metaheuristic drives the back-calculation search itself, not just hyperparameters"),
    "10.1038/s41598-024-81311-3": ("H1", "black-winged kite algorithm tunes XGBoost hyperparameters"),
    "10.3390/app9163221": ("H1", "PSO tunes ELM; paper also reports PSO-ANN and kernel-ELM as internal comparators"),
    "10.1038/s41598-022-17429-z": ("H1", "six swarm optimisers each tune LSSVM hyperparameters"),
    "10.32604/cmes.2023.046025": ("H1", "modified beetle antennae search tunes random forest / selects features"),
    "10.3390/su13168831": ("none", "Bayesian-regularised shallow NN, no metaheuristic coupling"),
    "10.1080/19942060.2018.1563829": ("H1", "particle filter optimises SVR"),
    "10.3390/su15129617": ("none", "plain tree ensembles + SHAP, no optimiser coupling"),
    "10.3390/app132312862": ("H1", "TPE tunes CatBoost hyperparameters; Boruta is feature selection, not the hybrid coupling itself"),
    "10.1016/j.sandf.2020.02.010": ("H2", "GA both fits a symbolic equation (H7-adjacent) AND drives ANN-GA weights (H2); coded primarily H2 for the direct head-to-head with the H7 variant"),
    "10.3390/infrastructures8080125": ("H2", "PSO drives WNN weights"),
    "10.3390/ai7020037": ("H1", "Fennec Fox Optimization tunes the ensemble stack"),
    "10.1038/s41598-024-61313-x": ("H7", "TLBO-optimised EPR/MGGP — symbolic-numeric with metaheuristic-fitted coefficients"),
    "10.1155/2020/7534970": ("none", "grey relation analysis is a feature-ranking step, not a coupled optimiser-learner hybrid"),
    "10.1016/j.cscm.2022.e00991": ("none", "GA and ANN run as separate competing models, not coupled — vocabulary trap, see note field"),
    "10.1109/tits.2022.3161689": ("context", "reinforcement learning M&R policy — architecturally distinct from the H1-H7 predictive-model taxonomy; kept for Section 9/11"),
    "10.1111/mice.13234": ("context", "multi-agent RL — same reason as above"),
    "10.1016/j.ijtst.2021.05.006": ("context", "supervised ML + Q-learning coupling — borderline H-taxonomy case; flag for full-text read"),
    "10.1016/j.eswa.2023.120851": ("context", "insufficient detail in abstract to classify; full-text needed"),
    "10.48550/arxiv.2112.12589": ("context", "preprint; DNN environment + DQN/PPO — kept for Section 9 only"),
    "10.1155/2020/8824135": ("H5", "heterogeneous stacking of XGBoost+ANN+RF+ridge+SVR"),

    # --- context / landmark / non-hybrid single-architecture studies ---
    "10.3390/infrastructures6020028": ("context", "error-propagation simulation, not a predictive model — keystone citation for Section 11"),
    "10.1111/mice.70102": ("none", "gradient boosting + random forest with grid search — tuned baseline, not a coupled hybrid"),
    "10.3390/inventions11030060": ("context", "graph operator network on synthetic FEM data — architecture-fusion adjacent (H4-like) but not metaheuristic/ML coupling; flag for taxonomy edge-case discussion"),
    "10.1111/mice.12263": ("none", "single-architecture CNN, landmark citation only"),
    "10.1007/s41062-020-00312-z": ("none", "single ANN with post-hoc Garson/connection-weight sensitivity — interpretability, not hybridity"),
    "10.3390/su15108831".replace("8831","0060"): ("skip", "placeholder guard, not a real key"),
    "10.1016/j.ijprt.2017.09.002": ("none", "single ANN, FFT is a signal-processing input step not a coupled learner"),
    "10.1155/2014/515467": ("H7", "ANN and MARS reported together as parallel symbolic/numeric comparators"),
    "10.1016/j.infrastructures9020033.replace".replace(".replace",""): ("skip", "guard"),
    "10.3390/infrastructures9020033": ("context", "mechanistic-empirical only, no ML — kept as the mechanistic-reference citation"),
    "10.1038/s41598-024-79588-5": ("none", "single LSTM, no coupling — architecture/task-mismatch critique case"),
    "10.3390/su13158298": ("H5", "stacking XGBoost/RF/CART/M5 — building energy context paper, not pavement"),
    "10.1016/j.ijprt.2016.11.006": ("none", "single ANN forward model"),
    "10.1139/cjce-2017-0570": ("none", "single ANN back-calculation"),
    "10.1139/cjce-2017-0132": ("none", "single ANN — the external-validation positive exemplar"),
    "10.3390/ma15207303": ("none", "single ANN"),
    "10.3390/ma15134386": ("H7", "ANN and GEP reported as parallel symbolic/numeric comparators"),
    "10.1016/j.conbuildmat.2018.08.011": ("none", "CNN vs. tuned classical edge detectors — the baseline-honesty exemplar, not a hybrid"),
    "10.1186/s40537-023-00727-2": ("context", "cross-domain methods survey"),
    "10.1016/j.autcon.2022.104440": ("context", "cross-domain construction-AI survey, Section 1 framing citation"),
    "10.1186/s40537-024-00981-y": ("none", "single U-Net-variant segmentation model"),
    "10.3390/app14114709": ("none", "single transformer segmentation model"),
    "10.3390/s23073772": ("H4", "dual Swin-Transformer + ResNet backbone fusion"),
    "10.1145/3594806.3596560": ("none", "single SegFormer model"),
    "10.3390/s23177395": ("H4", "YOLOv5 + transformer tracking fusion"),
    "10.1111/mice.13344": ("H4", "FCN + HRNet backbone fusion with geometric post-processing"),
    "10.1155/2023/3301106": ("H4", "HRNet + dynamic feature-fusion edge branch"),
    "10.28991/cej-2025-011-01-06b": ("skip", "guard"),
    "10.3390/app14083177": ("none", "tuned tree ensembles, no metaheuristic coupling"),
    "10.3390/infrastructures9050078": ("none", "Bayesian-optimised ensemble trees — tuning, not a coupled hybrid under our definition; borderline, flag"),
    "10.1007/s44290-024-00128-1": ("none", "GPR/SVM comparators, no coupling"),
    "10.1007/s44285-025-00061-4": ("H1", "PSO tunes GBM hyperparameters"),
    "10.1007/s42947-022-00213-7": ("none", "ML ensemble + SHAP, no metaheuristic/architecture coupling"),
    "10.1109/access.2020.2991968": ("H1;H4", "multi-objective salp swarm feature selection (H1) over fused hand-crafted+CNN features (H4)"),
    "10.1111/mice.70169": ("H4", "PaveGNet: graph + temporal architecture fusion, no metaheuristic coupling"),
    "10.3390/su152316337": ("none", "SVM vs CatBoost comparison, no metaheuristic/architecture coupling"),
    "10.1109/access.2022.3196660": ("H1", "adaptive mutation dipper-throated optimization tunes/selects features for random forest — the vocabulary-trap exemplar"),
    "10.3390/infrastructures11040127": ("context", "mechanistic-only (NCHRP 1-37A vs locally calibrated model), no ML — kept for Section 11 decision-consequence discussion"),
    "10.32604/cmc.2023.042183": ("H1", "whale optimization algorithm selects deep (ResNet-18) features for random forest classification"),
    "10.1007/s41062-025-02249-7": ("H1", "PSO tunes GBM hyperparameters"),
    "10.1007/s43995-025-00214-0": ("H1", "GA tunes SVR hyperparameters"),
    "10.1186/s44147-025-00623-x": ("H1", "PSO tunes GBM hyperparameters"),
    "10.1007/s41024-025-00667-9": ("H1", "GA tunes GBM hyperparameters"),
    "10.1007/s41024-024-00499-z": ("H1", "GA tunes SVR hyperparameters"),
    "10.3390/constrmater6010006": ("H1", "GA tunes GBM hyperparameters"),
    "10.1007/s44290-025-00381-y": ("H1", "GA tunes SVR hyperparameters"),
    "10.1016/j.conbuildmat.2023.133523": ("none", "tuned XGBoost, no metaheuristic coupling described in available summary"),
    "10.1016/j.cscm.2022.e01774": ("H7", "MEP produces closed-form equations; compared against ANN/ANFIS/DT-Bagging, no coupling"),
    "10.3390/eng6080183": ("H7", "GEP closed-form equation, no metaheuristic coupling"),
    "10.20944/preprints202004.0029.v1": ("H2", "genetic algorithm drives random forest structure (RF-GA) -- superseded, see coatings10111100"),
    "10.1038/s41598-024-65547-7": ("H1", "four separate metaheuristics (PSO/GWO/SMA/MPA) tune ANN"),
    "10.3390/infrastructures6090129": ("H1", "four separate metaheuristics (PSO/FF/GA/GWO) tune ANFIS"),
    "10.1155/2023/1827117": ("H7", "GEP/MEP closed-form equations, no metaheuristic coupling"),
    "10.3390/coatings10111100": ("H2", "genetic algorithm drives random forest structure (RF-GA), published version"),
    "10.1155/2022/9193511": ("H1", "salp swarm algorithm optimizes multiclass SVM"),
    "10.3390/app9153172": ("H1", "GA and PSO separately tune ANFIS (GA-ANFIS, PSO-ANFIS), compared against plain SVM"),

    # --- batch 4 (2026-08-09 Crossref harvest) ---
    # H1
    "10.1016/j.conbuildmat.2023.131564": ("H1", "Bayesian optimization tunes RF+XGBoost for GPR density prediction"),
    "10.1016/j.conbuildmat.2024.136675": ("H1", "Bayesian optimization tunes XGBoost for moisture-damage recognition"),
    "10.3390/app112411867": ("H1", "PSO tunes SVM for fatigue life prediction"),
    "10.1088/2631-8695/ae894f": ("H1", "WOA tunes XGBoost hyperparameters; abstract-confirmed +2.8pp over plain XGBoost"),
    "10.1177/00368504261450035": ("H1", "PSO tunes SVM (c, gamma); abstract-confirmed 70/30 + 5-fold CV protocol"),
    # H1;H5
    "10.3390/s25082616": ("H1;H5", "Bayesian optimization tunes hyperparameters AND fusion coefficients over a Stacking meta-learner"),
    "10.1038/s41598-025-26364-8": ("H1;H5", "APO+GGO tune XGBoost/LightGBM combined via Voting+Stacking"),
    # H2
    "10.1080/10298436.2021.2005056": ("H2", "grey wolf optimizer drives ANN weights for dynamic modulus"),
    "10.1016/j.conbuildmat.2021.123026": ("H2", "GA drives ANN for moduli back-calculation (inverse problem)"),
    "10.1080/10298430500495113": ("H2", "GA drives ANN for moduli back-calculation, 2006"),
    "10.1080/10298430500195432": ("H2", "GA drives ANN for pavement maintenance management, 2005"),
    "10.1139/cjce-2017-0124": ("H2", "GA used AS the ANN training algorithm (not just hyperparameter search), abstract-confirmed"),
    "10.1007/s00521-018-3426-0": ("H2", "symbiotic organisms search drives least-squares SVR"),
    # H2;H4
    "10.1016/j.conbuildmat.2024.139540": ("H2;H4", "CPO tunes a CNN-LSTM fused architecture"),
    # H3
    "10.1016/j.trgeo.2024.101409": ("H3", "PINN for subgrade settlement from shield tunnelling"),
    "10.1016/j.autcon.2025.105983": ("H3", "PINN with fuzzy PDE constraint, published in the review's own target journal"),
    "10.1016/j.conbuildmat.2025.142179": ("H3", "PINN for asphalt pavement temperature field"),
    "10.1016/j.conbuildmat.2024.135070": ("H3", "PINN-AFP: PINN for fatigue C-S curve estimation"),
    "10.1016/j.conbuildmat.2026.146164": ("H3", "PINN for airport pavement thermal property inversion"),
    "10.1177/03611981251372087": ("H3", "PINN vs conventional ANN on LTPP cracking, abstract-confirmed comparison"),
    "10.1016/j.neunet.2026.108803": ("H3", "PINN for viscoelastic constitutive modeling of asphalt mechanics"),
    "10.1016/j.cacaie.2026.100171": ("H3", "DM-PINN-FP for fatigue prediction with cracking preference index"),
    "10.1080/14680629.2024.2315073": ("H3", "PINN pretrained on suspension response, fine-tuned to IRI -- confirmed primary research via search, not the near-identically-titled 2026 ACME review"),
    # H3;H6
    "10.1016/j.ymssp.2026.114232": ("H3;H6", "Wave-PINN: wavelet decomposition front-end feeding a physics-informed network"),
    # H4
    "10.3390/app13031999": ("H4", "STrans-YOLOX: CNN(YOLOX)+Swin Transformer fusion, abstract-confirmed"),
    "10.3390/s26113286": ("H4", "dual-path CNN+Transformer fusion for crack segmentation, abstract-confirmed"),
    "10.1177/03611981251329046": ("H4", "parallel CNN+Transformer branches for crack detection, abstract-confirmed"),
    # H5
    "10.1016/j.conbuildmat.2025.140001": ("H5", "stacking ensemble for flow number prediction"),
    "10.1016/j.conbuildmat.2025.142704": ("H5", "stacking ensemble for elastic modulus back-calculation"),
    "10.1080/10298436.2026.2641497": ("H1;H5", "multi-model optimized stacking ensemble framework"),
    "10.1007/s42947-026-00866-8": ("H5", "stacked ensemble with SHAP-prioritized intervention ranking"),
    # H6 -- the taxonomically consequential pair; see add_batch4.py docstring
    "10.1080/10298436.2020.1776281": ("H6", "wavelet decomposition integrated with OP-ELM, abstract-confirmed; CONFIRMS H6 is not empty, overturning the two-sweep 'H6=0' finding"),
    "10.1016/j.ymssp.2025.112468": ("H6", "EEMD+K-means IMF selection feeding a downstream predictor (downstream model not named in the retrievable snippet -- provisional, top full-text-verification priority)"),
    # H7
    "10.1016/j.conbuildmat.2020.120543": ("H7", "GEP for rutting depth prediction"),
    "10.1080/10298436.2016.1138113": ("H7", "GEP for dynamic modulus prediction"),
    "10.1016/j.trgeo.2021.100520": ("H7", "GEP (+ANN comparator) for subgrade resilient modulus under freeze-thaw"),
    "10.1016/j.conbuildmat.2019.03.225": ("H7", "GEP for aggregate angularity effects on permanent deformation"),
    "10.1007/s41062-021-00504-1": ("H7", "GEP for PCI from IRI"),
    "10.1371/journal.pone.0301075": ("H7", "GP+EPR vs ANN/RSM for soil-lime UCS; abstract-confirmed GP underperforms ANN (66% vs 85% accuracy) -- §9 hybrid-underperforms evidence"),
    "10.1080/14680629.2022.2126383": ("H7", "MEP+GEP for bituminous mixture stiffness modulus"),
    "10.1016/j.jreng.2022.08.002": ("H7", "multi-gene GP explicitly extending AASHTO M-E design procedure"),
    "10.1016/j.rineng.2023.101242": ("H7", "GEP for theoretical maximum specific gravity"),
    "10.1061/jpeodx.pveng-1834": ("H7", "GEP for dynamic modulus and phase angle"),
    # none -- metaheuristic present but not coupled to a data-driven learner
    "10.3141/2170-08": ("none", "GA fits a semi-empirical curve-shift model directly; ANN run as a separate uncoupled comparator, same exclusion logic as cscm.2022.e00991"),

    # --- batch 5 (2026-08-09 harvest, taxonomy-balance follow-up) ---
    "10.1016/j.conbuildmat.2023.131852": ("H4", "Swin Transformer encoder + UperNet decoder w/ attention, search-confirmed"),
    "10.1016/j.eswa.2011.01.089": ("H6", "wavelet+Radon decomposition feeding a dynamic-threshold neural network classifier, search-confirmed"),
    "10.1016/j.eswa.2010.12.060": ("H6", "wavelet decomposition feeding a radon neural network expert system, search-confirmed; companion to eswa.2011.01.089"),
    "10.32604/sdhm.2026.075421": ("H5", "explicit stacking: Ridge+KNN+MLP+RF base models -> SVM meta-model, search-confirmed"),
    "10.3390/su14105938": ("H1", "improved beetle antennae search tunes NN hyperparameters; abstract-confirmed vs random-hyperparameter comparison"),
    "10.3141/2305-14": ("none", "GA calibrates MEPDG k-value coefficients directly, not coupled to a learner -- same exclusion as 2170-08"),
    "10.1080/10298436.2025.2543554": ("H3;H4", "physics-informed graph attention network -- GNN architecture (H4-adjacent) + physics constraint (H3), title-level"),
    "10.1080/10298436.2026.2708277": ("H3", "physics-informed back-calculation method, title-level"),
    "10.1155/2008/861701": ("none", "BEMD decomposition + Sobel edge detector (fixed classical operator, not a trained learner) -- deliberate H6/not-H6 boundary case, search-confirmed"),

    # --- batch 6 (2026-08-09 harvest, third increment) ---
    "10.1016/j.conbuildmat.2022.128955": ("H1", "Bayesian optimization tunes SVR for icing prediction"),
    "10.3390/asi6050093": ("H7", "ANN+GEP hybrid; GEP produces the final closed-form equation, abstract-confirmed"),
    "10.1016/j.istruc.2024.106837": ("H7", "GEP vs MEP for subgrade resilient modulus"),
    "10.1007/s00521-022-07305-2": ("H7", "GEP for Idaho pavement distress models"),
    "10.3389/fbuil.2022.895210": ("H7", "ANN+GEP for PCI/IRI, Jordan road network, search-confirmed"),
    "10.1080/10298436.2022.2147672": ("none", "WOA optimises the downstream M&R schedule, not the RF prediction model itself -- same category as RL M&R policy papers coded context"),
    "10.1016/j.conbuildmat.2025.143170": ("H1;H3", "Bayesian optimization tunes a physics-informed network for density prediction"),
    "10.1186/s40703-021-00149-0": ("none", "DEA + Taguchi are classical statistical/OR methods, not a metaheuristic-learner coupling"),
    "10.3390/ma18245635": ("H1", "GA hyperparameter optimization for ML road-performance model"),
    "10.1051/matecconf/202439605016": ("H1", "Bayesian optimization tunes SVR for resilient modulus"),
    "10.1007/s42947-026-00761-2": ("H1", "PSO tunes SVR; same Alnaqbi/Al-Khateeb/Zeiada author team as the documented CRCP same-substrate series, likely a 9th entry"),
    "10.1155/adce/8657453": ("H7", "GEP rutting prediction model, LTPP data"),
}


def main() -> None:
    # NOTE: seed_bibliography.csv lives in data/, not analysis/ -- it was moved there
    # at some point and this script's path was never updated (found 2026-08-09 while
    # adding batch 4; make_bib.py had already been fixed, this one and the historical
    # add_batch2.py/add_batch3.py/build_seed_db.py were not). Hardcoded rather than
    # re-using the stale with_name() pattern so this can't silently regress again.
    path = Path(__file__).parent.parent / "data" / "seed_bibliography.csv"
    rows = list(csv.DictReader(path.open(encoding="utf-8-sig")))
    fieldnames = list(rows[0].keys())
    if "hybrid_type" not in fieldnames:
        fieldnames.append("hybrid_type")

    coded = 0
    for r in rows:
        doi = r["doi"].strip()
        if "prior review" in r["role_in_review"]:
            r["hybrid_type"] = "review"
            continue
        entry = CLASSIFICATION.get(doi)
        if entry and entry[0] != "skip":
            r["hybrid_type"] = entry[0]
            coded += 1
        elif r.get("hybrid_type") and r["hybrid_type"] not in ("", "not-yet-coded"):
            # Already classified by a prior run/manual edit and not (yet) present
            # in CLASSIFICATION above -- preserve it rather than silently reset to
            # not-yet-coded. Whoever adds a record's hybrid_type by hand should
            # still backfill CLASSIFICATION at the next convenient edit so the
            # reasoning trail stays in one place.
            coded += 1
        else:
            r["hybrid_type"] = "not-yet-coded"

    tmp = path.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    tmp.replace(path)  # atomic swap -- never leaves the real file truncated mid-write

    uncoded = [r["title"][:60] for r in rows
               if r["hybrid_type"] == "not-yet-coded"]
    print(f"classified {coded} primary studies")
    if uncoded:
        print(f"{len(uncoded)} still not-yet-coded:")
        for t in uncoded:
            print("  -", t)


if __name__ == "__main__":
    main()
