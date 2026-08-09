#!/usr/bin/env python3
"""
add_batch4.py — Phase 14 corpus expansion (first real-harvest batch).
=======================================================================
Adds 44 records selected from the first successful bulk harvest this project has run
(analysis/harvest_crossref.py, 2026-08-09; OpenAlex itself was rate-limited into a
~7.7h wall from this environment's shared egress IP, see CLAUDE.md and the harvest log
-- Crossref was the working fallback). The harvest returned 2,332 unique pavement-gated
records from 261 queries; analysis/screen_corpus.py's structural filter narrowed that
to 97 title/abstract-level candidates; this batch is the 44 of those judged, by hand,
to be genuine structural hybrids under docs/01_SCOPE_AND_TAXONOMY.md §2 -- not simply
records that matched the search vocabulary.

VERIFICATION DEPTH -- read this before trusting any single note field
-----------------------------------------------------------------------
~12 of these 44 were checked against a real Crossref-deposited abstract (Elsevier does
not deposit abstracts to Crossref for most of its journals, so most Elsevier-published
records here are NOT in that dozen). Those notes quote or closely paraphrase the actual
abstract. The rest are coded at TITLE level only -- defensible for hybrid_type in this
specific literature, where titles are unusually literal about method ("GEP model for
X", "PINN for Y"), but NOT a substitute for full-text verification before any specific
metric (R^2, n, leakage protocol) is asserted about them. None of these notes states a
number that was not actually read in an abstract or full text.

THE ONE RECORD THAT MATTERS MOST: 10.1080/10298436.2020.1776281 (Kaloop et al. 2020,
"hybrid wavelet-optimally-pruned extreme learning machine... international roughness
index of rigid pavements") is, on its own abstract's word, a genuine H6 case -- wavelet
decomposition integrated with OP-ELM, benchmarked against plain OP-ELM/ANN/regression on
LTPP JPCP data. The manuscript's H6=0 finding ("confirmed absent after two independent
search sweeps") was reported honestly based on what two prior sweeps actually found --
this is not that finding turning out to be false, it is the corpus growing past what
those sweeps covered. Section 3/9 prose needs updating to reflect H6>=1, not silently
left as before. Full-text access to this record itself was attempted and BLOCKED
(Taylor & Francis returned 403 to an automated fetch, the same failure mode already
recorded for the Ghorbani ScienceDirect attempt) -- so leakage_risk on this specific
record stays coded as unknown/unread, not inferred.

Idempotent; run after add_batch3.py (or any state -- it dedupes by DOI like the others).
"""

import csv
from pathlib import Path

COLUMNS = [
    "doi", "year", "authors", "title", "venue", "cited_by_count",
    "role_in_review", "pavement_domain", "pavement_family", "architecture",
    "optimizer_hybrid", "data_source", "n_samples", "interpretability_method",
    "deployment_evidence", "note",
]

TITLE_LEVEL = ("Title/metadata-level classification from the 2026-08-09 Crossref "
               "harvest -- no Crossref abstract was deposited for this record (common "
               "for this publisher) and full text has not yet been read. Architecture "
               "is inferred from the title, which in this literature is typically "
               "literal about method. Not full-text verified; no specific metric below "
               "is asserted beyond what the title itself states.")

BATCH4 = [
    # --- H1: optimiser tunes hyperparameters ---
    dict(doi="10.1016/j.conbuildmat.2023.131564", year=2023,
         authors="Chen, Y.; Li, F.; Zhou, S.; Zhang, X.; Zhang, S.; Zhang, Q.; Su, Y.",
         title="Bayesian optimization based random forest and extreme gradient boosting for the pavement density prediction in GPR detection",
         venue="Construction and Building Materials", cited_by_count=72,
         role_in_review="PRIMARY — H1, batch 14", pavement_domain="materials",
         pavement_family="flexible", architecture="RF + XGBoost", optimizer_hybrid="Bayesian optimisation",
         data_source="GPR field survey", n_samples="", interpretability_method="", deployment_evidence="",
         note=TITLE_LEVEL),
    dict(doi="10.1016/j.conbuildmat.2024.136675", year=2024,
         authors="Li, H.; Zhang, J.; Yang, X.; Ye, M.; Jiang, W.; Gong, J.; Tian, Y.; Zhao, L.; Wang, W.; Xu, Z.",
         title="Bayesian optimization based extreme gradient boosting and GPR time-frequency features for the recognition of moisture damage in asphalt pavement",
         venue="Construction and Building Materials", cited_by_count=26,
         role_in_review="PRIMARY — H1, batch 14", pavement_domain="materials",
         pavement_family="flexible", architecture="XGBoost", optimizer_hybrid="Bayesian optimisation",
         data_source="GPR field survey", n_samples="", interpretability_method="", deployment_evidence="",
         note=TITLE_LEVEL),
    dict(doi="10.3390/app112411867", year=2021, authors="Sun, Y.; He, D.; Li, J.",
         title="Research on the Fatigue Life Prediction for a New Modified Asphalt Mixture of a Support Vector Machine Based on Particle Swarm Optimization",
         venue="Applied Sciences", cited_by_count=18,
         role_in_review="PRIMARY — H1, batch 14", pavement_domain="materials",
         pavement_family="flexible", architecture="SVM (SVR)", optimizer_hybrid="particle swarm optimization",
         data_source="laboratory (SCB fatigue test)", n_samples="", interpretability_method="", deployment_evidence="",
         note="Abstract confirms PSO-SVM fatigue-life model for SMCSBS composite-modified asphalt, trained on SCB test data (SMC content, asphalt-aggregate ratio, stress ratio, loading frequency as inputs); abstract text was truncated before it stated the RMSE/R2 values, so no specific metric is recorded here."),
    dict(doi="10.1088/2631-8695/ae894f", year=2026, authors="Zhang, L.; Li, Y.; Guang, C.",
         title="Smartphone-based pavement distress classification using WOA-Optimized XGBoost",
         venue="Engineering Research Express", cited_by_count=0,
         role_in_review="PRIMARY — H1, §9 premium evidence, batch 14", pavement_domain="distress-detection",
         pavement_family="general", architecture="XGBoost", optimizer_hybrid="whale optimization algorithm",
         data_source="field (2280 smartphone-collected samples)", n_samples=2280,
         interpretability_method="", deployment_evidence="smartphone deployment, real road sections",
         note="Abstract read directly: WOA tunes XGBoost max-depth/n-estimators/learning-rate for 4-class distress classification (intact/manhole/pothole/network-cracking). WOA-XGBoost reaches 94.6% test accuracy, stated as +2.8% over plain (presumably default-hyperparameter) XGBoost, +4.1% over RF, +5.7% over SVM — a genuinely modest, believable premium figure, unlike several inflated claims elsewhere in the corpus. Good concrete number for §9's premium table once the +2.8%-vs-plain-XGBoost baseline's tuning protocol is confirmed."),
    dict(doi="10.1177/00368504261450035", year=2026, authors="Xu, W.; Yang, Z.; Ji, Y.; Huang, P.",
         title="Pavement condition prediction under small-sample conditions using a particle swarm optimization-based support vector machine",
         venue="Science Progress", cited_by_count=0,
         role_in_review="PRIMARY — H1, §9 premium evidence, batch 14", pavement_domain="performance-prediction",
         pavement_family="general", architecture="SVM (SVR)", optimizer_hybrid="particle swarm optimization",
         data_source="field (two Chinese roads, one ordinary + one expressway)", n_samples="",
         interpretability_method="random forest feature importance (post-hoc, on inputs not model)",
         deployment_evidence="",
         note="Abstract read directly: PSO tunes SVM hyperparameters c and gamma; compared against baseline SVM and BPNN. Explicitly states evaluation used a 70/30 hold-out split PLUS 5-fold cross-validation 'to mitigate partition bias in a small-sample context' — a rare case where a small-sample study actively names and addresses partition bias rather than ignoring it. Worth citing in §12 (PAVE-ML) as a positive small-sample-reporting exemplar even though the H1 premium magnitude itself isn't quoted in the truncated abstract."),

    # --- H1;H5 combined ---
    dict(doi="10.3390/s25082616", year=2025, authors="Hao, J.; Sun, Z.; Xing, Z.; Pei, L.; Feng, X.",
         title="Dual-Layer Fusion Model Using Bayesian Optimization for Asphalt Pavement Condition Index Prediction",
         venue="Sensors", cited_by_count=6,
         role_in_review="PRIMARY — H1;H5 combined, batch 14", pavement_domain="performance-prediction",
         pavement_family="flexible", architecture="LCE ensemble + TCN-Transformer (lower layer) -> Stacking w/ logistic-regression meta-learner (upper layer)",
         optimizer_hybrid="Bayesian optimisation (tunes network hyperparameters AND fusion coefficients jointly)",
         data_source="multi-modal field sensors (strain, temp/humidity, WIM) + distress + maintenance records, 8-year observation window",
         n_samples="", interpretability_method="", deployment_evidence="embedded sensor network",
         note="Abstract read directly: a genuinely multi-family hybrid — BO-DLFF couples Bayesian-optimised hyperparameter tuning (H1) with a Stacking meta-learner (H5) over an LCE+TCN-Transformer base layer. Reports R2 = 0.9292 on an 8-year multi-source dataset. Coded H1;H5 as the two taxonomy-defining couplings; the TCN-Transformer fusion is a third coupling this taxonomy doesn't have a clean single label for — flag as a research-agenda note (multi-type composite hybrids are becoming more common and may need an H8/'composite' bucket in a future taxonomy revision)."),
    dict(doi="10.1038/s41598-025-26364-8", year=2025,
         authors="Khiavi, A. J.; Naeim, B.; Soleimanzadeh, M.",
         title="Development of a novel ensemble learning model for predicting asphalt volumetric properties using experimental data for pavement performance assessment",
         venue="Scientific Reports", cited_by_count=7,
         role_in_review="PRIMARY — H1;H5 combined, §9, batch 14", pavement_domain="materials",
         pavement_family="flexible", architecture="XGBoost + LightGBM, Voting + Stacking ensemble",
         optimizer_hybrid="Artificial Protozoa Optimizer (APO) + Greylag Goose Optimization (GGO), hyperparameter tuning",
         data_source="laboratory (~200 road-surface samples, Ardabil, Iran)", n_samples=200,
         interpretability_method="sensitivity analysis (post feature selection)", deployment_evidence="",
         note="Abstract read directly: predicts three volumetric outputs (AVP, PVFB, PVMS) from 11 input features; base learners XGBoost/LightGBM, combined via Voting and Stacking, hyperparameters tuned by two very recently proposed metaheuristics (APO, GGO — both 2024-era). Abstract states XGBoost gives 'excellent R2 and RMSE' but was truncated before the actual values. Relevant to §9's optimiser_novelty_claim item: APO and GGO are newly-named optimisers: full text needs checking for whether they're benchmarked against established optimisers on this problem, per PAVE-ML item 12d."),

    # --- H2: optimiser drives weights/structure ---
    dict(doi="10.1080/10298436.2021.2005056", year=2021,
         authors="Mohammadi Golafshani, E.; Behnood, A.; Karimi, M. M.",
         title="Predicting the dynamic modulus of asphalt mixture using hybridized artificial neural network and grey wolf optimizer",
         venue="International Journal of Pavement Engineering", cited_by_count=12,
         role_in_review="PRIMARY — H2, batch 14", pavement_domain="materials",
         pavement_family="flexible", architecture="ANN", optimizer_hybrid="grey wolf optimizer",
         data_source="", n_samples="", interpretability_method="", deployment_evidence="", note=TITLE_LEVEL),
    dict(doi="10.1016/j.conbuildmat.2021.123026", year=2021,
         authors="Zhang, X.; Otto, F.; Oeser, M.",
         title="Pavement moduli back-calculation using artificial neural network and genetic algorithms",
         venue="Construction and Building Materials", cited_by_count=31,
         role_in_review="PRIMARY — H2 (inverse problem), batch 14", pavement_domain="structural-evaluation",
         pavement_family="flexible/rigid/composite", architecture="ANN", optimizer_hybrid="genetic algorithm",
         data_source="", n_samples="", interpretability_method="", deployment_evidence="",
         note=TITLE_LEVEL + " Same ANN-GA-backcalculation pattern as the two 2005/2006 records below, 15+ years later — useful for showing the pattern's persistence over time in §3's bibliometric narrative."),
    dict(doi="10.1080/10298430500495113", year=2006,
         authors="Rakesh, N.; Jain, A. K.; Reddy, M. A.; Reddy, K. S.",
         title="Artificial neural networks—genetic algorithm based model for backcalculation of pavement layer moduli",
         venue="International Journal of Pavement Engineering", cited_by_count=62,
         role_in_review="PRIMARY — H2 (inverse problem), batch 14", pavement_domain="structural-evaluation",
         pavement_family="flexible/rigid/composite", architecture="ANN", optimizer_hybrid="genetic algorithm",
         data_source="", n_samples="", interpretability_method="", deployment_evidence="",
         note=TITLE_LEVEL + " One of the earliest H2 records in the corpus (2006); useful for the year-trend figure's early tail."),
    dict(doi="10.1080/10298430500195432", year=2005, authors="Bosurgi, G.; Trifirò, F.",
         title="A model based on artificial neural networks and genetic algorithms for pavement maintenance management",
         venue="International Journal of Pavement Engineering", cited_by_count=47,
         role_in_review="PRIMARY — H2, earliest year in corpus, batch 14", pavement_domain="M&R-and-PMS",
         pavement_family="general", architecture="ANN", optimizer_hybrid="genetic algorithm",
         data_source="", n_samples="", interpretability_method="", deployment_evidence="",
         note=TITLE_LEVEL + " 2005 — the earliest possible year under this review's own 2005-2026 scope; anchors the year-trend figure's start point with a real record rather than an empty first year."),
    dict(doi="10.1139/cjce-2017-0124", year=2017,
         authors="Fakhri, M.; Amoosoltani, E.; Farhani, M.; Ahmadi, A.",
         title="Determining optimal combination of roller compacted concrete pavement mixture containing recycled asphalt pavement and crumb rubber using hybrid artificial neural network–genetic algorithm method considering energy absorbency approach",
         venue="Canadian Journal of Civil Engineering", cited_by_count=18,
         role_in_review="PRIMARY — H2, batch 14", pavement_domain="materials",
         pavement_family="rigid", architecture="feed-forward ANN", optimizer_hybrid="genetic algorithm (real-coded, used AS the training algorithm)",
         data_source="laboratory (RCC mix design)", n_samples="",
         interpretability_method="", deployment_evidence="",
         note="Abstract read directly: GA is used as the actual training algorithm for the feed-forward ANN (not just hyperparameter search) — 'a real coded GA was implemented as training algorithm of feed forward neural network'; Nash-Sutcliffe efficiency used as GA's fitness function. Clean H2 case (metaheuristic -> weights)."),
    dict(doi="10.1007/s00521-018-3426-0", year=2018,
         authors="Cheng, M.-Y.; Prayogo, D.; Wu, Y.-W.",
         title="Prediction of permanent deformation in asphalt pavements using a novel symbiotic organisms search–least squares support vector regression",
         venue="Neural Computing and Applications", cited_by_count=50,
         role_in_review="PRIMARY — H2, batch 14", pavement_domain="materials",
         pavement_family="flexible", architecture="least-squares SVR", optimizer_hybrid="symbiotic organisms search",
         data_source="", n_samples="", interpretability_method="", deployment_evidence="", note=TITLE_LEVEL),

    # --- H2;H4 combined ---
    dict(doi="10.1016/j.conbuildmat.2024.139540", year=2025,
         authors="Chen, S.; Cao, J.; Wan, Y.; Huang, W.; Abdel-Aty, M.",
         title="A novel CPO-CNN-LSTM based deep learning approach for multi-time scale deflection basin area prediction in asphalt pavement",
         venue="Construction and Building Materials", cited_by_count=22,
         role_in_review="PRIMARY — H2;H4 combined, batch 14", pavement_domain="structural-evaluation",
         pavement_family="flexible", architecture="CNN-LSTM (architecture fusion)",
         optimizer_hybrid="crested porcupine optimizer (CPO)",
         data_source="", n_samples="", interpretability_method="", deployment_evidence="",
         note=TITLE_LEVEL + " Two couplings at once: CNN+LSTM is architecture fusion (H4) and CPO tuning that fused network is metaheuristic-driven (H2/H1-adjacent, coded H2 since CPO's target — hyperparameters vs. structure — isn't stated in the title alone). Coded H2;H4."),

    # --- H3: physics-informed neural networks (note the 2024-2026 surge in this batch) ---
    dict(doi="10.1016/j.trgeo.2024.101409", year=2024,
         authors="Wang, G.; Shan, Y.; Detmann, B.; Lin, W.",
         title="Physics-Informed Neural Network (PINN) model for predicting subgrade settlement induced by shield tunnelling beneath an existing railway subgrade",
         venue="Transportation Geotechnics", cited_by_count=37,
         role_in_review="PRIMARY — H3, batch 14", pavement_domain="geotechnical (subgrade-adjacent)",
         pavement_family="subgrade", architecture="PINN", optimizer_hybrid="",
         data_source="", n_samples="", interpretability_method="physics constraint (intrinsic)", deployment_evidence="",
         note=TITLE_LEVEL),
    dict(doi="10.1016/j.autcon.2025.105983", year=2025,
         authors="Li, J.; Zhang, S.; Wang, X.",
         title="Physics-informed neural network with fuzzy partial differential equation for pavement performance prediction",
         venue="Automation in Construction", cited_by_count=30,
         role_in_review="PRIMARY — H3, THIS REVIEW'S TARGET JOURNAL, batch 14", pavement_domain="performance-prediction",
         pavement_family="flexible", architecture="PINN (fuzzy PDE constraint)", optimizer_hybrid="",
         data_source="", n_samples="", interpretability_method="physics constraint (intrinsic)", deployment_evidence="",
         note=TITLE_LEVEL + " Published in Automation in Construction (this review's current submission target) — evidence the venue actively publishes exactly this kind of methodology paper, worth a line in the journal-targeting rationale."),
    dict(doi="10.1016/j.conbuildmat.2025.142179", year=2025,
         authors="Quan, W.; Ma, X.; Shang, Z.; Zhao, K.; Su, M.; Dong, Z.; Zhao, Z.",
         title="Hybrid physics-data-driven model for temperature field prediction of asphalt pavement based on physics-informed neural network",
         venue="Construction and Building Materials", cited_by_count=30,
         role_in_review="PRIMARY — H3, batch 14", pavement_domain="materials/test-simulation",
         pavement_family="flexible", architecture="PINN", optimizer_hybrid="",
         data_source="", n_samples="", interpretability_method="physics constraint (intrinsic)", deployment_evidence="",
         note=TITLE_LEVEL),
    dict(doi="10.1016/j.conbuildmat.2024.135070", year=2024,
         authors="Han, C.; Zhang, J.; Tu, Z.; Ma, T.",
         title="PINN-AFP: A novel C-S curve estimation method for asphalt mixtures fatigue prediction based on physics-informed neural network",
         venue="Construction and Building Materials", cited_by_count=27,
         role_in_review="PRIMARY — H3, batch 14", pavement_domain="materials",
         pavement_family="flexible", architecture="PINN", optimizer_hybrid="",
         data_source="", n_samples="", interpretability_method="physics constraint (intrinsic)", deployment_evidence="",
         note=TITLE_LEVEL),
    dict(doi="10.1016/j.conbuildmat.2026.146164", year=2026,
         authors="Xing, X.; Ling, J.; Liu, S.; Tao, Z.",
         title="Physics-informed neural network for thermal property inversion of airport pavement multilayer materials under icing conditions",
         venue="Construction and Building Materials", cited_by_count=11,
         role_in_review="PRIMARY — H3, airfield domain, batch 14", pavement_domain="materials/test-simulation",
         pavement_family="airfield", architecture="PINN", optimizer_hybrid="",
         data_source="", n_samples="", interpretability_method="physics constraint (intrinsic)", deployment_evidence="",
         note=TITLE_LEVEL + " One of very few airfield-domain records in the corpus — useful for domain-coverage diversity."),
    dict(doi="10.1177/03611981251372087", year=2025,
         authors="Taheri, A.; Sobanjo, J.; Elwardany, M.",
         title="Pavement Cracking Prediction Models Based on Deep Learning Physics-Informed Neural Network",
         venue="Transportation Research Record", cited_by_count=3,
         role_in_review="PRIMARY — H3, §9 premium-adjacent, batch 14", pavement_domain="performance-prediction",
         pavement_family="flexible", architecture="PINN", optimizer_hybrid="",
         data_source="LTPP", n_samples="", interpretability_method="physics constraint (intrinsic)", deployment_evidence="",
         note="Abstract read directly: PINN for wheel-path cracking on LTPP data; explicitly compares against a conventional ANN and reports improved accuracy/generalisation from enforcing a physically-expected sign constraint (positive correlation of age vs. cracking). This is a genuine PINN-vs-plain-ANN comparison — a candidate for the §9 premium table once the exact R2/MAE gap is read from the full text (abstract was truncated before the numbers)."),
    dict(doi="10.1016/j.neunet.2026.108803", year=2026,
         authors="Luo, X.; Huang, J.; Shen, L.; Wang, H.; Shi, Z.",
         title="Physics-informed neural networks for constitutive modeling and multiphysics coupling in viscoelastic materials: Applications to asphalt pavement mechanics",
         venue="Neural Networks", cited_by_count=2,
         role_in_review="PRIMARY — H3, batch 14", pavement_domain="materials",
         pavement_family="flexible", architecture="PINN", optimizer_hybrid="",
         data_source="", n_samples="", interpretability_method="physics constraint (intrinsic)", deployment_evidence="",
         note=TITLE_LEVEL),
    dict(doi="10.1016/j.cacaie.2026.100171", year=2026,
         authors="Liu, Q.; Li, H.; Gao, Y.; Zhang, H.; Li, Y.; Lee, D.; Wu, J.",
         title="A Physics-Informed Neural Network (DM-PINN-FP): Incorporating Cracking Preference Index for Asphalt Mixture Fatigue Prediction",
         venue="Computer-Aided Civil and Infrastructure Engineering", cited_by_count=0,
         role_in_review="PRIMARY — H3, CACAIE (shortlisted alt. venue), batch 14", pavement_domain="materials",
         pavement_family="flexible", architecture="PINN", optimizer_hybrid="",
         data_source="", n_samples="", interpretability_method="physics constraint (intrinsic)", deployment_evidence="",
         note=TITLE_LEVEL + " Published in Computer-Aided Civil and Infrastructure Engineering — the Wiley journal flagged in CLAUDE.md as the strongest non-Elsevier alternative venue; another data point for that venue's fit."),
    dict(doi="10.1080/14680629.2024.2315073", year=2024,
         authors="Kargah-Ostadi, N.; Vasylevskyi, K.; Ablets, A.; Drach, A.",
         title="Physics-informed neural networks to advance pavement engineering and management",
         venue="Road Materials and Pavement Design", cited_by_count=14,
         role_in_review="PRIMARY — H3 (confirmed primary, not a review), batch 14", pavement_domain="performance-prediction",
         pavement_family="flexible", architecture="PINN (pretrained on suspension-response simulation, fine-tuned to IRI)",
         optimizer_hybrid="", data_source="", n_samples="",
         interpretability_method="physics constraint (intrinsic)", deployment_evidence="",
         note="Confirmed via search (title alone reads review-like, so this was checked before inclusion): this is primary research, not a survey. A PINN is pretrained to approximate vehicle-suspension response to road profile, then its outer layers are fine-tuned to match measured IRI while the physics-informed inner layers are kept frozen — a genuine physics+data coupling, not a literature review. Worth noting: a true review with an almost identical title exists (Springer ACME, 2026, 'Physics-Informed Neural Networks in Civil, Transportation, and Pavement Engineering: Cross-Domain Review') — different DOI, not added here, flagged for a future batch's §1 prior-review sweep."),

    # --- H3;H6 combined ---
    dict(doi="10.1016/j.ymssp.2026.114232", year=2026,
         authors="Fu, D.; Deng, Y.; Wang, H.; Shi, X.; Zhang, Y.; Yu, J.",
         title="Wave-PINN: a wavelet-based physics-informed neural network for continuous pavement roughness evaluation from vehicle dynamics",
         venue="Mechanical Systems and Signal Processing", cited_by_count=2,
         role_in_review="PRIMARY — H3;H6 combined, batch 14", pavement_domain="performance-prediction",
         pavement_family="flexible", architecture="PINN + wavelet decomposition front-end",
         optimizer_hybrid="", data_source="vehicle dynamics response", n_samples="",
         interpretability_method="physics constraint (intrinsic)", deployment_evidence="",
         note=TITLE_LEVEL + " Title names both couplings explicitly (wavelet decomposition front-end feeding a physics-informed network) — coded H3;H6, a rare combined case worth a callout in §8's taxonomy-combinations discussion."),

    # --- H4: architecture fusion (vision domain) ---
    dict(doi="10.3390/app13031999", year=2023,
         authors="Luo, H.; Li, J.; Cai, L.; Wu, M.",
         title="STrans-YOLOX: Fusing Swin Transformer and YOLOX for Automatic Pavement Crack Detection",
         venue="Applied Sciences", cited_by_count=24,
         role_in_review="PRIMARY — H4, batch 14", pavement_domain="distress-detection",
         pavement_family="flexible", architecture="CNN (YOLOX) + Swin Transformer, feature-pyramid fusion",
         optimizer_hybrid="", data_source="", n_samples="",
         interpretability_method="", deployment_evidence="",
         note="Abstract read directly: CNN backbone (YOLOX) for local features + Swin Transformer for long-range dependency via self-attention, fused through a global attention guidance module in the feature pyramid network. Textbook H4 (CNN+transformer fusion, matches the taxonomy doc's own H4 example exactly). Reports 63.37% mAP, stated to surpass compared state-of-the-art models on the cited crack dataset."),
    dict(doi="10.3390/s26113286", year=2026,
         authors="Zhang, J.; Sun, S.; Song, W.; Li, Y.; Teng, Q.",
         title="A Dual-Path CNN and Transformer Network for Continuous Pavement Crack Detection",
         venue="Sensors", cited_by_count=0,
         role_in_review="PRIMARY — H4, batch 14", pavement_domain="distress-detection",
         pavement_family="flexible", architecture="CNN (dynamic multi-branch conv) + Transformer (lightweight DCNv4), dual-path fusion",
         optimizer_hybrid="", data_source="4 public crack datasets (CFD, DeepCrack537, Gaps384, Crack500)", n_samples="",
         interpretability_method="", deployment_evidence="",
         note="Abstract read directly: parallel CNN + Transformer branches with a multi-path fusion module; ablation studies reported. Clean H4 case, 2026 — shows the CNN+transformer fusion pattern is still active three years after the STrans-YOLOX paper above."),
    dict(doi="10.1177/03611981251329046", year=2025,
         authors="Deng, Y.; Yu, H.; Niu, P.; Guo, F.",
         title="Enhancing Pavement Crack Detection Using a Hybrid Convolutional Neural Network-Transformer Architecture",
         venue="Transportation Research Record", cited_by_count=1,
         role_in_review="PRIMARY — H4, batch 14", pavement_domain="distress-detection",
         pavement_family="flexible", architecture="CNN + Transformer, parallel-branch fusion with boundary heatmap head",
         optimizer_hybrid="", data_source="", n_samples="",
         interpretability_method="boundary heatmap (post-hoc, spatial)", deployment_evidence="",
         note="Abstract read directly: CNN branch generates boundary heatmaps for regional interaction, Transformer branch handles long-range context via multi-head self-attention; a contextual-attention module fuses both. F1 = 76.36% on public datasets stated. Third independent CNN+Transformer H4 example in this batch (with the two above) — together they support a §3/§8 claim that architecture fusion is now a recurring, not isolated, pattern in the crack-detection sub-literature."),

    # --- H5: heterogeneous stacking ---
    dict(doi="10.1016/j.conbuildmat.2025.140001", year=2025,
         authors="Guan, Y.; Zhang, B.; Li, Z.; Zhang, D.",
         title="Enhanced flow number prediction of asphalt mixtures using stacking ensemble-based machine learning model and grey relational analysis",
         venue="Construction and Building Materials", cited_by_count=19,
         role_in_review="PRIMARY — H5, batch 14", pavement_domain="materials",
         pavement_family="flexible", architecture="stacking ensemble (base learners unspecified in title)",
         optimizer_hybrid="grey relational analysis (feature ranking)", data_source="", n_samples="",
         interpretability_method="", deployment_evidence="", note=TITLE_LEVEL),
    dict(doi="10.1016/j.conbuildmat.2025.142704", year=2025,
         authors="Wang, Y.; Zhao, Y.; Sun, Q.; Wang, R.",
         title="Intelligent back-calculation of elastic modulus for asphalt pavement structures with bedrock using a stacking ensemble learning model",
         venue="Construction and Building Materials", cited_by_count=6,
         role_in_review="PRIMARY — H5 (inverse problem), batch 14", pavement_domain="structural-evaluation",
         pavement_family="flexible/rigid/composite", architecture="stacking ensemble (base learners unspecified in title)",
         optimizer_hybrid="", data_source="", n_samples="", interpretability_method="", deployment_evidence="",
         note=TITLE_LEVEL),
    dict(doi="10.1080/10298436.2026.2641497", year=2026,
         authors="Khan, A.; Zhang, W.; Chang, H.; Wang, C.; Liu, S.; Liu, H.; Geng, D.",
         title="Multi-model optimized stacking ensemble framework for pavement performance: predicting key indicators and the Pavement Maintenance Quality Index",
         venue="International Journal of Pavement Engineering", cited_by_count=2,
         role_in_review="PRIMARY — H1;H5 combined, batch 14", pavement_domain="M&R-and-PMS",
         pavement_family="general", architecture="stacking ensemble (multi-model)",
         optimizer_hybrid="optimisation-tuned base models (method unspecified in title)", data_source="", n_samples="",
         interpretability_method="", deployment_evidence="", note=TITLE_LEVEL),
    dict(doi="10.1007/s42947-026-00866-8", year=2026, authors="Gupta, A.; Kumar, P.",
         title="Stacked Ensemble Learning with SHAP-Prioritized Intervention Ranking for Pavement Maintenance Automation",
         venue="International Journal of Pavement Research and Technology", cited_by_count=0,
         role_in_review="PRIMARY — H5, §10/§12 interpretability angle, batch 14", pavement_domain="M&R-and-PMS",
         pavement_family="general", architecture="stacked ensemble (base learners unspecified in title)",
         optimizer_hybrid="", data_source="", n_samples="",
         interpretability_method="SHAP", deployment_evidence="maintenance intervention ranking",
         note=TITLE_LEVEL + " SHAP-based ranking used directly to prioritise maintenance interventions (not just post-hoc explanation) — a genuine interpretability-to-decision link, relevant to §10/§11's argument about whether interpretability actually changes decisions."),

    # --- H6: decomposition then learn (the taxonomically consequential pair) ---
    dict(doi="10.1080/10298436.2020.1776281", year=2020,
         authors="Kaloop, M. R.; El-Badawy, S. M.; Ahn, J.; Sim, H.-B.; Hu, J. W.; Abd El-Hakim, R. T.",
         title="A hybrid wavelet-optimally-pruned extreme learning machine model for the estimation of international roughness index of rigid pavements",
         venue="International Journal of Pavement Engineering", cited_by_count=47,
         role_in_review="PRIMARY — H6 CONFIRMED (overturns prior H6=0 finding), §3/§9, batch 14",
         pavement_domain="performance-prediction", pavement_family="rigid (JPCP)",
         architecture="Optimally Pruned Extreme Learning Machine (OP-ELM)",
         optimizer_hybrid="wavelet decomposition (front-end signal processing, not a metaheuristic — this is the H6 coupling itself)",
         data_source="LTPP (JPCP sections, USA)", n_samples="",
         interpretability_method="", deployment_evidence="",
         note="Abstract obtained via web search after Taylor & Francis blocked automated full-text fetch (403 — same failure mode as the Ghorbani/ScienceDirect attempt already on record, honestly logged rather than silently skipped). Abstract states directly: 'Optimally Pruned Extreme Learning Machine (OP-ELM) and Wavelet analysis are integrated... novel hybrid Wavelet-OPELM (WOPELM) model', benchmarked against plain OP-ELM, conventional feed-forward ANN, and a regression model on LTPP JPCP data. This is a genuine, abstract-confirmed H6 case — the manuscript's prior claim that H6 was 'confirmed absent after two independent search sweeps' was an honest report of what those two sweeps actually covered, not a false claim; the corpus has now grown past that coverage and Section 3/9 prose needs a one-line update reflecting H6>=1. leakage_risk on this specific record is UNKNOWN — full text (needed to check whether the wavelet transform was fitted before or after the train/test split, the exact H6 failure mode the taxonomy names) was not obtainable; do not infer either way."),
    dict(doi="10.1016/j.ymssp.2025.112468", year=2025,
         authors="Zhang, C.; Shen, S.; Huang, H.; Yu, S.",
         title="An integrated data processing strategy for pavement modulus prediction using empirical mode decomposition techniques",
         venue="Mechanical Systems and Signal Processing", cited_by_count=6,
         role_in_review="PRIMARY — H6 plausible (abstract-snippet confirmed, full text blocked), batch 14",
         pavement_domain="structural-evaluation", pavement_family="flexible",
         architecture="downstream predictive model not named in the retrievable snippet",
         optimizer_hybrid="ensemble empirical mode decomposition (EEMD) + K-means clustering for IMF selection",
         data_source="embedded wireless sensors (field)", n_samples="",
         interpretability_method="", deployment_evidence="embedded sensor network",
         note="Publisher page (Elsevier) and a university repository mirror (Penn State PURE) both returned 403 to automated fetch; what's recorded here comes from a search-engine snippet of the abstract only, not a full read. That snippet describes EEMD decomposition of sensor signals, MNCC/SNR-guided K-means selection of effective IMFs, and states the approach 'expand[s] data dimensionality' and yields 'enhanced prediction accuracy' for pavement modulus — strongly implying a downstream trained predictor consumes the decomposed features, which is what would make this H6, but the snippet does not name that downstream model explicitly. Coded H6 provisionally; flag as the top-priority full-text verification target in the next batch, specifically to confirm the downstream learner and check decomposition-before-split leakage risk (the same question flagged on the Kaloop record above)."),

    # --- H7: symbolic-numeric (gene expression / multi-expression programming) ---
    dict(doi="10.1016/j.conbuildmat.2020.120543", year=2021,
         authors="Majidifard, H.; Jahangiri, B.; Rath, P.; Urra Contreras, L.; Buttlar, W. G.; Alavi, A. H.",
         title="Developing a prediction model for rutting depth of asphalt mixtures using gene expression programming",
         venue="Construction and Building Materials", cited_by_count=60,
         role_in_review="PRIMARY — H7, batch 14", pavement_domain="performance-prediction",
         pavement_family="flexible", architecture="gene expression programming", optimizer_hybrid="",
         data_source="", n_samples="", interpretability_method="closed-form GEP equation (intrinsic)",
         deployment_evidence="", note=TITLE_LEVEL),
    dict(doi="10.1080/10298436.2016.1138113", year=2016,
         authors="Liu, J.; Yan, K.; You, L.; Liu, P.",
         title="Prediction models of mixtures' dynamic modulus using gene expression programming",
         venue="International Journal of Pavement Engineering", cited_by_count=54,
         role_in_review="PRIMARY — H7, batch 14", pavement_domain="materials",
         pavement_family="flexible", architecture="gene expression programming", optimizer_hybrid="",
         data_source="", n_samples="", interpretability_method="closed-form GEP equation (intrinsic)",
         deployment_evidence="", note=TITLE_LEVEL),
    dict(doi="10.1016/j.trgeo.2021.100520", year=2021,
         authors="Zou, W.-l.; Han, Z.; Ding, L.-q.; Wang, X.-q.",
         title="Predicting resilient modulus of compacted subgrade soils under influences of freeze–thaw cycles and moisture using gene expression programming and artificial neural network approaches",
         venue="Transportation Geotechnics", cited_by_count=52,
         role_in_review="PRIMARY — H7 (GEP component; ANN run as comparator), batch 14",
         pavement_domain="geotechnical (subgrade-adjacent)", pavement_family="subgrade",
         architecture="gene expression programming (+ ANN comparator)", optimizer_hybrid="",
         data_source="", n_samples="", interpretability_method="closed-form GEP equation (intrinsic)",
         deployment_evidence="", note=TITLE_LEVEL),
    dict(doi="10.1016/j.conbuildmat.2019.03.225", year=2019, authors="Leon, L. P.; Gay, D.",
         title="Gene expression programming for evaluation of aggregate angularity effects on permanent deformation of asphalt mixtures",
         venue="Construction and Building Materials", cited_by_count=31,
         role_in_review="PRIMARY — H7, batch 14", pavement_domain="materials",
         pavement_family="flexible", architecture="gene expression programming", optimizer_hybrid="",
         data_source="", n_samples="", interpretability_method="closed-form GEP equation (intrinsic)",
         deployment_evidence="", note=TITLE_LEVEL),
    dict(doi="10.1007/s41062-021-00504-1", year=2021,
         authors="Imam, R.; Murad, Y.; Asi, I.; Shatnawi, A.",
         title="Predicting Pavement Condition Index from International Roughness Index using Gene Expression Programming",
         venue="Innovative Infrastructure Solutions", cited_by_count=27,
         role_in_review="PRIMARY — H7, batch 14", pavement_domain="M&R-and-PMS",
         pavement_family="general", architecture="gene expression programming", optimizer_hybrid="",
         data_source="", n_samples="", interpretability_method="closed-form GEP equation (intrinsic)",
         deployment_evidence="", note=TITLE_LEVEL),
    dict(doi="10.1371/journal.pone.0301075", year=2024,
         authors="Guo, X.; Garcia, C.; Andrade Valle, A. I.; Onyelowe, K.; Zarate Villacres, A. N.; Ebid, A. M.; Hanandeh, S.",
         title="Modeling the influence of lime on the unconfined compressive strength of reconstituted graded soil using advanced machine learning approaches for subgrade and liner applications",
         venue="PLOS ONE", cited_by_count=18,
         role_in_review="PRIMARY — H7 (GP/EPR components), §9 hybrid-underperforms evidence, batch 14",
         pavement_domain="geotechnical (subgrade-adjacent)", pavement_family="subgrade",
         architecture="Genetic Programming (GP) + Evolutionary Polynomial Regression (EPR), vs. ANN and Response Surface Methodology comparators",
         optimizer_hybrid="", data_source="laboratory (soil-lime UCS, 7- and 28-day curing)", n_samples="",
         interpretability_method="closed-form GP/EPR equation (intrinsic)", deployment_evidence="",
         note="Abstract read directly: four methods head-to-head on the same UCS prediction task — ANN and EPR reach similar 7-day accuracy (85% and 82%, R2 = 0.947 and 0.923 respectively), while GP is explicitly reported LOWER (66.0% accuracy). This is a real, abstract-confirmed case of a symbolic/GP model underperforming a plain ANN on the same data and split — directly strengthens §9's evidence that hybrid/symbolic complexity does not reliably beat simpler baselines, alongside the existing Nguyen (2019) Monte Carlo case."),
    dict(doi="10.1080/14680629.2022.2126383", year=2022,
         authors="Leon, L. P.; Azamathulla, H.; Felix, P.; Prasad, C. V. S. R.",
         title="Prediction of stiffness modulus of bituminous mixtures using the applications of multi-expression programming and gene expression programming",
         venue="Road Materials and Pavement Design", cited_by_count=15,
         role_in_review="PRIMARY — H7, batch 14", pavement_domain="materials",
         pavement_family="flexible", architecture="multi-expression programming + gene expression programming",
         optimizer_hybrid="", data_source="", n_samples="",
         interpretability_method="closed-form MEP/GEP equation (intrinsic)", deployment_evidence="",
         note=TITLE_LEVEL),
    dict(doi="10.1016/j.jreng.2022.08.002", year=2022, authors="Li, H.; Khazanovich, L.",
         title="Multi-gene genetic programming extension of AASHTO M-E for design of low-volume concrete pavements",
         venue="Journal of Road Engineering", cited_by_count=8,
         role_in_review="PRIMARY — H7 (symbolic model literally extends a physics-based design method), batch 14",
         pavement_domain="design", pavement_family="low-volume",
         architecture="multi-gene genetic programming, extending the AASHTO Mechanistic-Empirical design procedure",
         optimizer_hybrid="", data_source="", n_samples="",
         interpretability_method="closed-form MGGP equation (intrinsic)", deployment_evidence="",
         note=TITLE_LEVEL + " Unusual and citable case: the symbolic model is framed as an explicit EXTENSION of an established mechanistic-empirical design procedure (AASHTO M-E) rather than a standalone black-box competitor — relevant to §8's discussion of where H3/H7 boundary cases sit."),
    dict(doi="10.1016/j.rineng.2023.101242", year=2023, authors="Jweihan, Y. S.",
         title="Predictive model of asphalt mixes' theoretical maximum specific gravity using gene expression programming",
         venue="Results in Engineering", cited_by_count=12,
         role_in_review="PRIMARY — H7, batch 14", pavement_domain="materials",
         pavement_family="flexible", architecture="gene expression programming", optimizer_hybrid="",
         data_source="", n_samples="", interpretability_method="closed-form GEP equation (intrinsic)",
         deployment_evidence="", note=TITLE_LEVEL),
    dict(doi="10.1061/jpeodx.pveng-1834", year=2025,
         authors="Jukte, N. R.; Swamy, A. K.",
         title="Efficient Gene Expression Programming–Based Predictive Models for Dynamic Modulus and Phase Angle of Asphalt Mixtures",
         venue="Journal of Transportation Engineering, Part B: Pavements", cited_by_count=0,
         role_in_review="PRIMARY — H7, batch 14", pavement_domain="materials",
         pavement_family="flexible", architecture="gene expression programming", optimizer_hybrid="",
         data_source="", n_samples="", interpretability_method="closed-form GEP equation (intrinsic)",
         deployment_evidence="", note=TITLE_LEVEL),

    # --- none: metaheuristic used, but not coupled to a learner (structural exclusion) ---
    dict(doi="10.3141/2170-08", year=2010,
         authors="Coleri, E.; Guler, M.; Gungor, A. G.; Harvey, J. T.",
         title="Prediction of Subgrade Resilient Modulus Using Genetic Algorithm and Curve-Shifting Methodology",
         venue="Transportation Research Record", cited_by_count=17,
         role_in_review="context — GA-fitted curve-shift method, ANN run as a separate uncoupled comparator, batch 14",
         pavement_domain="geotechnical (subgrade-adjacent)", pavement_family="subgrade",
         architecture="curve-shifting methodology (semi-empirical, not a trained ML model)",
         optimizer_hybrid="genetic algorithm (fits shift-factor curve parameters directly, not coupled to a learner)",
         data_source="laboratory (triaxial resilient modulus tests)", n_samples="",
         interpretability_method="closed-form shift-factor curve (intrinsic)", deployment_evidence="",
         note="Abstract read directly: GA horizontally shifts laboratory stress-strain curves to fit a gamma-distribution model — this is a genetically-fitted semi-empirical curve, not a coupled optimiser+learner hybrid, so it does not meet the H1-H7 structural test (same exclusion logic as the existing 10.1016/j.cscm.2022.e00991 record: 'GA and ANN run as separate competing models, not coupled'). Kept as context because the abstract states the GA-curve-shift approach beat the Uzan constitutive model by a coefficient-of-determination 14% higher, and was separately compared against ANN predictions — real, quotable comparator evidence for a future premium-adjacent discussion, just not itself a hybrid data point."),
]


def main() -> None:
    # seed_bibliography.csv lives in data/, not analysis/ (see the same fix + note in
    # classify_hybridity.py, discovered while writing this script).
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

    # Existing rows may already carry a hybrid_type column (added by a prior
    # classify_hybridity.py run) that COLUMNS above doesn't list -- write out the
    # union so DictWriter doesn't choke, same as add_batch2.py/add_batch3.py's
    # implicit assumption before that column existed.
    fieldnames = existing_fieldnames + [c for c in COLUMNS if c not in existing_fieldnames]

    added = 0
    for r in BATCH4:
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
    tmp.replace(path)  # atomic swap -- never leaves the real file truncated mid-write

    print(f"added {added} records; database now holds {len(existing)}")


if __name__ == "__main__":
    main()
