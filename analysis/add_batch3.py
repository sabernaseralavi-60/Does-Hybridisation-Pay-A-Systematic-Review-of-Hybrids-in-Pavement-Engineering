#!/usr/bin/env python3
"""
add_batch3.py — Phase 3 corpus expansion.
Adds records verified in the third search sweep: pavement-specific H1/H2 studies
(metaheuristic-tuned learners), one additional prior review found only now, and two
H5 (stacking) exemplars — one a clean leakage-avoidance case, one a leakage-risk case.
Idempotent; run after add_batch2.py.
"""

import csv
from pathlib import Path

COLUMNS = [
    "doi", "year", "authors", "title", "venue", "cited_by_count",
    "role_in_review", "pavement_domain", "pavement_family", "architecture",
    "optimizer_hybrid", "data_source", "n_samples", "interpretability_method",
    "deployment_evidence", "note",
]

BATCH3 = [
    dict(doi="10.1186/s43065-023-00082-9", year=2023, authors="Deng, Y.; Shi, X.",
         title="Modeling the rutting performance of asphalt pavements: a review",
         venue="J. Infrastruct. Preserv. Resil.", cited_by_count=41,
         role_in_review="prior review — §7 (rutting slice) + agency-practitioner survey",
         pavement_domain="performance-prediction", pavement_family="flexible",
         architecture="mechanical/empirical/ML (survey)", optimizer_hybrid="",
         data_source="literature + practitioner survey", n_samples="",
         interpretability_method="", deployment_evidence="",
         note="Includes a practitioner survey of which rutting models agencies actually use — a rare deployment-side data point, cite in §11/§9."),
    dict(doi="10.1016/j.jtte.2016.09.007", year=2016,
         authors="Mazari, M.; Rodriguez, D. D.",
         title="Prediction of pavement roughness using a hybrid gene expression programming-neural network technique",
         venue="J. Traffic Transp. Eng. (Engl. Ed.)", cited_by_count=159,
         role_in_review="PRIMARY — H7 exemplar, §8", pavement_domain="performance-prediction",
         pavement_family="flexible", architecture="GEP + ANN", optimizer_hybrid="none",
         data_source="LTPP", n_samples="", interpretability_method="GEP equation (intrinsic)",
         deployment_evidence="none",
         note="Early (2016), heavily cited (159) H7 case: symbolic GEP feeds a neural refinement stage. Good anchor for the symbolic-numeric taxonomy entry."),
    dict(doi="10.1016/j.sandf.2020.02.010", year=2020,
         authors="Ghorbani, B.; Arulrajah, A.; Narsilio, G. A.; et al.",
         title="Development of genetic-based models for predicting the resilient modulus of cohesive pavement subgrade soils",
         venue="Soils and Foundations", cited_by_count=93,
         role_in_review="PRIMARY — H2 exemplar, §4 & §9", pavement_domain="materials",
         pavement_family="general", architecture="ANN-GA (GA on weights) vs. GA symbolic",
         optimizer_hybrid="genetic algorithm", data_source="laboratory (RLT tests)",
         n_samples="", interpretability_method="closed-form GA equation (intrinsic)",
         deployment_evidence="equation",
         note="Directly compares a symbolic GA-only model against an ANN-GA hybrid on the SAME data — one of the few true head-to-head H2-vs-H7 comparisons in the corpus. Central to the premium analysis."),
    dict(doi="10.1155/2020/7534970", year=2020,
         authors="Wang, X.; Zhao, J.; Li, Q.; et al.",
         title="A hybrid model for prediction in asphalt pavement performance based on support vector machine and grey relation analysis",
         venue="J. Adv. Transp.", cited_by_count=68,
         role_in_review="§8 & §9", pavement_domain="performance-prediction",
         pavement_family="flexible", architecture="SVR", optimizer_hybrid="grey relation analysis (feature selection)",
         data_source="field (Guangyun Expressway weather station)", n_samples="",
         interpretability_method="GRA ranking", deployment_evidence="none",
         note="GRA used for feature selection before SVR — check whether selection precedes or follows the split; a leakage-risk candidate."),
    dict(doi="10.1016/j.cscm.2022.e00991", year=2022, authors="Hanandeh, S.",
         title="Introducing mathematical modeling to estimate pavement quality index of flexible pavements based on genetic algorithm and artificial neural networks",
         venue="Case Stud. Constr. Mater.", cited_by_count=40,
         role_in_review="§8 & §9", pavement_domain="performance-prediction",
         pavement_family="flexible", architecture="ANN vs. GA (compared, not combined)",
         optimizer_hybrid="genetic algorithm (independent model, not a hybrid coupling)",
         data_source="field (500 Amman sections)", n_samples="500 sections",
         interpretability_method="regression + GA equation", deployment_evidence="equation",
         note="Titled as GA+ANN but the two are run as SEPARATE competing models, not coupled — an example of the vocabulary trap in reverse (label suggests hybrid, structure does not qualify under our H1-H7 definition). Useful negative case for §2 methodology discussion."),
    dict(doi="10.3390/app9163221", year=2019,
         authors="Kaloop, M. R.; Kumar, D.; Samui, P.; et al.",
         title="Particle Swarm Optimization Algorithm-Extreme Learning Machine (PSO-ELM) model for predicting resilient modulus of stabilized aggregate bases",
         venue="Applied Sciences", cited_by_count=83,
         role_in_review="H1 exemplar — §4 (duplicate-checked against seed batch 1)",
         pavement_domain="materials", pavement_family="general", architecture="ELM",
         optimizer_hybrid="PSO", data_source="laboratory", n_samples="",
         interpretability_method="none", deployment_evidence="none",
         note="Also compares PSO-ELM against PSO-ANN and kernel ELM on the same task — within-paper optimiser ablation, useful for the premium analysis."),
    dict(doi="10.1186/s44147-025-00706-9", year=2025,
         authors="Alnaqbi, A.; Zeiada, W.; Al-Khateeb, G. G.",
         title="A hybrid machine learning method of support vector regression with particle swarm optimization for predicting IRI in continuously reinforced concrete pavement",
         venue="J. Eng. Appl. Sci.", cited_by_count=18,
         role_in_review="PRIMARY — H1 exemplar & §11 leakage case", pavement_domain="performance-prediction",
         pavement_family="rigid (CRCP)", architecture="SVR", optimizer_hybrid="PSO",
         data_source="LTPP (395 observations, 33 sections)", n_samples="395 obs / 33 sections",
         interpretability_method="variable importance; 3D interaction plots", deployment_evidence="none",
         note="Same 33-CRCP-section LTPP substrate as Alnaqbi 2026 GBM-PSO paper already in the database — a second report from an overlapping data source. R2=0.991 under 5-fold CV; unless section-blocked, a leakage-risk case identical in structure to the earlier one. Flag both for the §8/§11 near-duplicate-substrate discussion."),
    dict(doi="10.3390/ma18122913", year=2025,
         authors="Huang, H.; Xu, Z.; Li, X.; et al.",
         title="Predicting rheological properties of asphalt modified with mineral powder: bagging, boosting, and stacking vs. single machine learning models",
         venue="Materials", cited_by_count=2,
         role_in_review="PRIMARY — H5 positive exemplar, §8 & §12", pavement_domain="materials",
         pavement_family="flexible", architecture="stacking (KNN+DT+RF+XGBoost -> Bayesian ridge meta-learner)",
         optimizer_hybrid="Bayesian optimisation", data_source="laboratory (DSR tests)",
         n_samples="", interpretability_method="SHAP",
         deployment_evidence="none",
         note="States explicitly that the stacking framework uses CROSS-VALIDATED base-model predictions as meta-learner input specifically to reduce information leakage. This is the clearest positive H5 exemplar in the corpus and becomes the worked 'good practice' case in PAVE-ML item 12a-with-stacking (§10)."),
    dict(doi="10.1155/2020/8824135", year=2020,
         authors="Yu, G.; Zhang, S.; Hu, M.; et al.",
         title="Prediction of highway tunnel pavement performance based on digital twin and multiple time series stacking",
         venue="Adv. Civ. Eng.", cited_by_count=100,
         role_in_review="§8 & §9", pavement_domain="performance-prediction",
         pavement_family="general (tunnel)", architecture="stacking (XGBoost+ANN+RF+ridge+SVR)",
         optimizer_hybrid="grid search + k-fold CV", data_source="field (2010-2019, Shanghai)",
         n_samples="", interpretability_method="none",
         deployment_evidence="digital twin integration",
         note="Digital-twin framing gives it one of the strongest deployment-evidence codes in the corpus, though the stacking-leakage question (was CV used to select meta-features fairly?) needs full-text verification."),
]


def main() -> None:
    path = Path(__file__).with_name("seed_bibliography.csv")
    existing, seen = [], set()
    if path.exists():
        with path.open(encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                existing.append(row)
                seen.add(row["doi"].strip().lower())

    added = 0
    for r in BATCH3:
        if r["doi"].strip().lower() in seen:
            continue
        existing.append({c: r.get(c, "") for c in COLUMNS})
        seen.add(r["doi"].strip().lower())
        added += 1

    existing.sort(key=lambda r: (r.get("role_in_review", ""), -int(r.get("year") or 0)))

    with path.open("w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(existing)

    print(f"added {added} records; database now holds {len(existing)}")


if __name__ == "__main__":
    main()
