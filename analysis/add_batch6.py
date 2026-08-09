#!/usr/bin/env python3
"""
add_batch6.py — Phase 17 corpus expansion, third increment.
==============================================================
A further, deliberately modest pass from the same 2026-08-09 Crossref harvest's
remaining structural candidates (data/corpus_screened.csv), drawn following an
external pre-submission read that asked whether 147 records is a sufficient
reference base for a Q1 submission. 13 records added here, verified at the same
disclosed depth as batches 4-5 (search-confirmed where a real abstract or summary
was found, title-level otherwise, marked per record).

ONE RECORD EXTENDS AN ALREADY-DOCUMENTED PATTERN CENTRAL TO SECTION 7:
10.1007/s42947-026-00761-2 (Alnaqbi, Al-Khateeb, Zeiada -- SVR-PSO for
longitudinal cracking in rigid pavement, 2026) is by the same overlapping author
team already documented in Section 7 as reusing a single ~33-section CRCP LTPP
substrate across at least eight prior single-target papers. This is very likely
a ninth. Section 7's prose is updated accordingly in the same commit as this
script.

Idempotent; run after add_batch5.py.
"""

import csv
from pathlib import Path

COLUMNS = [
    "doi", "year", "authors", "title", "venue", "cited_by_count",
    "role_in_review", "pavement_domain", "pavement_family", "architecture",
    "optimizer_hybrid", "data_source", "n_samples", "interpretability_method",
    "deployment_evidence", "note",
]

TITLE_LEVEL = ("Title-level classification from the 2026-08-09 Crossref harvest -- "
               "no Crossref abstract deposited, publisher page not fetched. "
               "Architecture inferred from the title; not full-text verified.")

BATCH6 = [
    dict(doi="10.1016/j.conbuildmat.2022.128955", year=2022,
         authors="Yang, E.; Yang, Q.; Li, J.; Zhang, H.; Di, H.; Qiu, Y.",
         title="Establishment of icing prediction model of asphalt pavement based on support vector regression algorithm and Bayesian optimization",
         venue="Construction and Building Materials", cited_by_count=46,
         role_in_review="PRIMARY — H1, batch 17", pavement_domain="performance-prediction",
         pavement_family="flexible", architecture="SVR", optimizer_hybrid="Bayesian optimisation",
         data_source="", n_samples="", interpretability_method="", deployment_evidence="",
         note=TITLE_LEVEL),
    dict(doi="10.3390/asi6050093", year=2023,
         authors="Jweihan, Y. S.; Al-Kheetan, M. J.; Rabi, M.",
         title="Empirical Model for the Retained Stability Index of Asphalt Mixtures Using Hybrid Machine Learning Approach",
         venue="Applied System Innovation", cited_by_count=26,
         role_in_review="PRIMARY — H7, batch 17", pavement_domain="materials",
         pavement_family="flexible", architecture="ANN + gene expression programming",
         optimizer_hybrid="", data_source="laboratory", n_samples="",
         interpretability_method="closed-form GEP equation (intrinsic)", deployment_evidence="",
         note="Abstract read directly: predicts the Retained Stability Index (moisture "
              "susceptibility) from an ANN+GEP hybrid, with GEP producing the final "
              "closed-form equation from four input variables (filler %, aggregate water "
              "absorption, asphalt content, air void content); asphalt content ranked most "
              "influential via relative-importance analysis. Coded H7 on the GEP component."),
    dict(doi="10.1016/j.istruc.2024.106837", year=2024,
         authors="Khawaja, L.; Javed, M. F.; Asif, U.; Alkhattabi, L.",
         title="Indirect estimation of resilient modulus (Mr) of subgrade soil: Gene expression programming vs multi expression programming",
         venue="Structures", cited_by_count=25,
         role_in_review="PRIMARY — H7, batch 17", pavement_domain="geotechnical (subgrade-adjacent)",
         pavement_family="subgrade", architecture="gene expression programming + multi-expression programming",
         optimizer_hybrid="", data_source="", n_samples="", interpretability_method="closed-form equation (intrinsic)",
         deployment_evidence="", note=TITLE_LEVEL),
    dict(doi="10.1007/s00521-022-07305-2", year=2022, authors="Deng, Y.; Shi, X.",
         title="Development of predictive models of asphalt pavement distresses in Idaho through gene expression programming",
         venue="Neural Computing and Applications", cited_by_count=18,
         role_in_review="PRIMARY — H7, batch 17", pavement_domain="performance-prediction",
         pavement_family="flexible", architecture="gene expression programming", optimizer_hybrid="",
         data_source="Idaho agency pavement management data", n_samples="",
         interpretability_method="closed-form GEP equation (intrinsic)", deployment_evidence="",
         note=TITLE_LEVEL),
    dict(doi="10.3389/fbuil.2022.895210", year=2022,
         authors="Hanandeh, S.; Hanandeh, A.; Alhiary, M.; Al Twaiqat, M.",
         title="Application of Soft Computing for Estimation of Pavement Condition Indicators and Predictive Modeling",
         venue="Frontiers in Built Environment", cited_by_count=10,
         role_in_review="PRIMARY — H7, batch 17", pavement_domain="M&R-and-PMS",
         pavement_family="general", architecture="ANN + gene expression programming",
         optimizer_hybrid="genetic algorithm (GEP is itself evolutionary)", data_source="field (Jordan road network)",
         n_samples="", interpretability_method="closed-form GEP equation (intrinsic)", deployment_evidence="",
         note="Search-confirmed: models PCI and IRI for a Jordanian road network using ANN "
              "and GEP; described as combining genetic-algorithm-family and AI methods. Coded "
              "H7 on the GEP component, consistent with how the corpus treats other ANN+GEP pairs."),
    dict(doi="10.1080/10298436.2022.2147672", year=2022,
         authors="Naseri, H.; Jahanbakhsh, H.; Foomajd, A.; Galustanian, N.",
         title="A newly developed hybrid method on pavement maintenance and rehabilitation optimization applying Whale Optimization Algorithm and random forest regression",
         venue="International Journal of Pavement Engineering", cited_by_count=42,
         role_in_review="context — WOA optimises the M&R schedule, not the RF prediction model itself, batch 17",
         pavement_domain="M&R-and-PMS", pavement_family="general",
         architecture="random forest (IRI prediction) + Whale Optimization Algorithm (M&R schedule optimisation)",
         optimizer_hybrid="", data_source="", n_samples="", interpretability_method="", deployment_evidence="",
         note="Search-confirmed: random forest regression predicts IRI; WOA then searches for "
              "the optimal maintenance-and-rehabilitation schedule using those predictions as an "
              "input. The metaheuristic optimises a downstream decision problem, not the "
              "predictive model's own hyperparameters or weights, so this does not meet the H1/H2 "
              "structural test in §2.3 — same architectural category as the reinforcement-learning "
              "M&R policy papers already coded context (e.g. @Yao2022large)."),
    dict(doi="10.1016/j.conbuildmat.2025.143170", year=2025,
         authors="Yao, K.; Chen, X.; Lu, Y.; Shi, B.; Hu, X.; Dong, Q.",
         title="A novel model for asphalt mixture density prediction based on physics-informed neural network with Bayesian optimization",
         venue="Construction and Building Materials", cited_by_count=9,
         role_in_review="PRIMARY — H1;H3 combined, batch 17", pavement_domain="materials",
         pavement_family="flexible", architecture="PINN", optimizer_hybrid="Bayesian optimisation",
         data_source="", n_samples="", interpretability_method="physics constraint (intrinsic)",
         deployment_evidence="", note=TITLE_LEVEL + " Coded H1;H3: Bayesian optimisation (H1) tunes a physics-informed network (H3) — two couplings named directly in the title."),
    dict(doi="10.1186/s40703-021-00149-0", year=2021,
         authors="Ikeagwuani, C. C.; Nwonu, D. C.",
         title="Variable returns to scale DEA–Taguchi approach for ternary additives optimization in expansive soil subgrade enhancement",
         venue="Journal of Engineering and Applied Science", cited_by_count=8,
         role_in_review="none — DEA and Taguchi are classical statistical/OR methods, not a metaheuristic-learner coupling, batch 17",
         pavement_domain="geotechnical (subgrade-adjacent)", pavement_family="subgrade",
         architecture="data envelopment analysis + Taguchi design of experiments (neither a trained ML model)",
         optimizer_hybrid="", data_source="laboratory", n_samples="", interpretability_method="", deployment_evidence="",
         note="Title-level: DEA (efficiency-frontier analysis) and Taguchi (classical design-of-"
              "experiments) are both statistical/operations-research techniques, not a "
              "metaheuristic or a trained data-driven learner under the definition in §2.3. Kept "
              "for completeness of the harvest record; not coded as a structural hybrid."),
    dict(doi="10.3390/ma18245635", year=2025,
         authors="Wu, Z.; Li, S.; Wang, D.; Qiu, M.; Fang, C.",
         title="Machine Learning Prediction of Road Performance of Cold Recycled Mix Asphalt with Genetic Algorithm Hyperparameter Optimization",
         venue="Materials", cited_by_count=2,
         role_in_review="PRIMARY — H1, batch 17", pavement_domain="materials",
         pavement_family="flexible", architecture="ML model (base learner unspecified in title)",
         optimizer_hybrid="genetic algorithm", data_source="", n_samples="",
         interpretability_method="", deployment_evidence="", note=TITLE_LEVEL),
    dict(doi="10.1051/matecconf/202439605016", year=2024,
         authors="Sandjak, K.; Ouanani, M.",
         title="Bayesian optimization algorithm based support vector regression analysis for estimation of resilient modulus of crushed rock materials for pavement design",
         venue="MATEC Web of Conferences", cited_by_count=1,
         role_in_review="PRIMARY — H1, batch 17", pavement_domain="materials",
         pavement_family="general", architecture="SVR", optimizer_hybrid="Bayesian optimisation",
         data_source="", n_samples="", interpretability_method="", deployment_evidence="",
         note=TITLE_LEVEL),
    dict(doi="10.1007/s42947-026-00761-2", year=2026,
         authors="Alnaqbi, A.; Al-Khateeb, G. G.; Zeiada, W.",
         title="A Hybrid Approach of Support Vector Regression with Particle Swarm Optimization for Predicting Longitudinal Cracking in Rigid Pavement",
         venue="International Journal of Pavement Research and Technology", cited_by_count=1,
         role_in_review="PRIMARY — H1, §7 same-substrate series (likely 9 of 9+), batch 17",
         pavement_domain="performance-prediction", pavement_family="rigid (CRCP)",
         architecture="SVR", optimizer_hybrid="particle swarm optimization",
         data_source="LTPP (likely the same CRCP substrate as the rest of the series)", n_samples="",
         interpretability_method="", deployment_evidence="",
         note="Same overlapping author team (Alnaqbi, Al-Khateeb, Zeiada) already documented in "
              "§7 as reusing a single ~33-section CRCP LTPP substrate across at least eight prior "
              "single-target papers (rutting, IRI, faulting, transverse and longitudinal cracking "
              "each spun out as its own publication). This record's target — longitudinal cracking "
              "in rigid pavement, via a new SVR-PSO coupling — is fully consistent with that "
              "pattern and, title and topic alone, is very likely a ninth entry in the same "
              "series; not confirmed by full-text reading of the data section, which would be "
              "needed to verify the substrate match with certainty rather than high plausibility."),
    dict(doi="10.1155/adce/8657453", year=2026,
         authors="Rind, T. A.; Khan, M. A.; Ahmed, S.; Javed, M.",
         title="Development of Gene Expression Programming–Based Rutting Prediction Model for Smart Pavement Management Using LTPP Data",
         venue="Advances in Civil Engineering", cited_by_count=0,
         role_in_review="PRIMARY — H7, batch 17", pavement_domain="performance-prediction",
         pavement_family="flexible", architecture="gene expression programming", optimizer_hybrid="",
         data_source="LTPP", n_samples="", interpretability_method="closed-form GEP equation (intrinsic)",
         deployment_evidence="", note=TITLE_LEVEL),
]


def main() -> None:
    path = Path(__file__).parent.parent / "data" / "seed_bibliography.csv"
    if not path.exists():
        raise SystemExit(f"! {path} does not exist -- refusing to create it from scratch")

    with path.open(encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        existing_fieldnames = list(reader.fieldnames)
        existing = list(reader)
    if not existing:
        raise SystemExit(f"! {path} read as empty -- refusing to write, investigate first")
    seen = {row["doi"].strip().lower() for row in existing}

    fieldnames = existing_fieldnames + [c for c in COLUMNS if c not in existing_fieldnames]

    added = 0
    for r in BATCH6:
        if r["doi"].strip().lower() in seen:
            continue
        existing.append({c: r.get(c, "") for c in fieldnames})
        seen.add(r["doi"].strip().lower())
        added += 1

    existing.sort(key=lambda r: (r.get("role_in_review", ""), -int(r.get("year") or 0)))

    tmp = path.with_suffix(".csv.tmp")
    with tmp.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(existing)
    tmp.replace(path)

    print(f"added {added} records; database now holds {len(existing)}")


if __name__ == "__main__":
    main()
