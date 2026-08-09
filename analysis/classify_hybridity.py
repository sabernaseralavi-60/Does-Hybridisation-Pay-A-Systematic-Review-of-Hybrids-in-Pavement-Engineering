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
}


def main() -> None:
    path = Path(__file__).with_name("seed_bibliography.csv")
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
        else:
            r["hybrid_type"] = "not-yet-coded"

    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    uncoded = [r["title"][:60] for r in rows
               if r["hybrid_type"] == "not-yet-coded"]
    print(f"classified {coded} primary studies")
    if uncoded:
        print(f"{len(uncoded)} still not-yet-coded:")
        for t in uncoded:
            print("  -", t)


if __name__ == "__main__":
    main()
