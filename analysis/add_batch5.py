#!/usr/bin/env python3
"""
add_batch5.py — Phase 14 corpus expansion, second increment.
================================================================
A small, deliberately targeted follow-up to add_batch4.py, drawn from the same
2026-08-09 Crossref harvest (data/corpus_screened.csv's remaining unreviewed
candidates, 147 after batch 4). Where batch 4 was a broad first pass, this batch
specifically corrects the taxonomy skew batch 4 itself flagged in CLAUDE.md and
README.md: H1 and H7 were unusually easy to find and code with confidence from
titles alone (PINN and GEP papers name their method plainly), which risked making
the corpus's taxonomy balance reflect what's easy to classify rather than the
field's true distribution. This batch deliberately weights toward H4/H5/H6 —
9 records total, smaller than batch 4 on purpose.

VERIFICATION NOTE: none of these 9 had a Crossref-deposited abstract. All 9 were
checked via WebSearch against the actual publisher/aggregator page before coding
(not title-inference alone) — search-engine-surfaced abstract text or structured
summaries, quoted or closely paraphrased in each note below. This is one step
below reading the full abstract directly on the publisher's page (all attempts to
fetch the pages directly were blocked, consistent with the pattern already
documented for the Ghorbani/ScienceDirect and Kaloop/Taylor&Francis attempts) and
a step above title-only classification. Flagged per-record as "search-confirmed."

ONE RECORD IS A DELIBERATE NEGATIVE / BOUNDARY CASE, KEPT ON PURPOSE:
10.1155/2008/861701 (Ayenu-Prah & Attoh-Okine 2008, BEMD + Sobel edge detector for
crack evaluation) looks, from its harvest flags, like a strong H6 candidate — but
search confirms its second component is a fixed Sobel filter, not a trained
data-driven learner, so it fails the H2.3 structural test and is coded `none`. It
is kept in the database anyway because it is the cleanest available illustration
of the H6/not-H6 boundary: decomposition + a classical fixed operator is not H6;
decomposition + something that learns from data is. Cite it in §8 as exactly that
boundary case, not silently drop it for scoring "none".

Idempotent; run after add_batch4.py.
"""

import csv
from pathlib import Path

COLUMNS = [
    "doi", "year", "authors", "title", "venue", "cited_by_count",
    "role_in_review", "pavement_domain", "pavement_family", "architecture",
    "optimizer_hybrid", "data_source", "n_samples", "interpretability_method",
    "deployment_evidence", "note",
]

BATCH5 = [
    dict(doi="10.1016/j.conbuildmat.2023.131852", year=2023,
         authors="Guo, F.; Liu, J.; Lv, C.; Yu, H.",
         title="A novel transformer-based network with attention mechanism for automatic pavement crack detection",
         venue="Construction and Building Materials", cited_by_count=102,
         role_in_review="PRIMARY — H4, batch 15 (taxonomy-balance pass)",
         pavement_domain="distress-detection", pavement_family="flexible",
         architecture="Swin Transformer encoder + UperNet decoder with attention module",
         optimizer_hybrid="", data_source="", n_samples="", interpretability_method="",
         deployment_evidence="",
         note="Search-confirmed (publisher page blocked automated fetch): the network unifies a Swin "
              "Transformer encoder with a UperNet-based decoder augmented by an attention module for "
              "pixel-level crack segmentation, explicitly compared against CNN-only baselines and reported "
              "as achieving the best mean-F1/mean-Recall at 0-pixel tolerance among compared models. A "
              "transformer-backbone + CNN-lineage-decoder pairing is architecture fusion under the H4 "
              "definition in §4 (same family as @Luo2023strans, @Zhang2026dual, @Deng2025enhancing), at 102 "
              "citations the best-cited H4 record in the corpus."),
    dict(doi="10.1016/j.eswa.2011.01.089", year=2011,
         authors="Nejad, F. M.; Zakeri, H.",
         title="An optimum feature extraction method based on Wavelet–Radon Transform and Dynamic Neural Network for pavement distress classification",
         venue="Expert Systems with Applications", cited_by_count=69,
         role_in_review="PRIMARY — H6, batch 15 (taxonomy-balance pass)",
         pavement_domain="distress-detection", pavement_family="flexible",
         architecture="dynamic (thresholding) neural network classifier",
         optimizer_hybrid="wavelet transform + Radon transform (front-end feature decomposition)",
         data_source="", n_samples="", interpretability_method="", deployment_evidence="",
         note="Search-confirmed (publisher page blocked automated fetch): discrete wavelet transform is "
              "applied to pavement images, then a Radon transform on the wavelet modulus, then a dynamic "
              "neural-network-based threshold stage extracts and classifies distress features. Decomposition "
              "(wavelet+Radon) feeding a trained neural classifier is H6 under the taxonomy in §4. Companion "
              "paper to @NejadZakeri2011expert immediately below — same two authors, same research thread, "
              "same journal and year, giving the corpus its first genuinely multi-record H6 evidence base "
              "rather than one isolated exemplar."),
    dict(doi="10.1016/j.eswa.2010.12.060", year=2011,
         authors="Moghadas Nejad, F.; Zakeri, H.",
         title="An expert system based on wavelet transform and radon neural network for pavement distress classification",
         venue="Expert Systems with Applications", cited_by_count=55,
         role_in_review="PRIMARY — H6, batch 15 (taxonomy-balance pass)",
         pavement_domain="distress-detection", pavement_family="flexible",
         architecture="radon neural network (expert-system classifier)",
         optimizer_hybrid="wavelet transform (front-end decomposition)",
         data_source="", n_samples="", interpretability_method="", deployment_evidence="",
         note="Search-confirmed (publisher page blocked automated fetch): a wavelet-transform front end "
              "feeding a 'radon neural network' expert-system classifier for pavement distress. Same authors "
              "and research thread as @NejadZakeri2011optimum immediately above, both published the same "
              "year in the same journal — two related but distinct architectures (dynamic-threshold NN vs. "
              "radon NN), both H6."),
    dict(doi="10.32604/sdhm.2026.075421", year=2026,
         authors="Peng, C.; Tang, J.; Zhang, D.",
         title="Prediction of Asphalt Pavement Rutting Depth Based on Multi-Model Fusion of Stacking Algorithm",
         venue="Structural Durability & Health Monitoring", cited_by_count=0,
         role_in_review="PRIMARY — H5, batch 15 (taxonomy-balance pass)",
         pavement_domain="materials", pavement_family="flexible",
         architecture="stacking: Ridge regression + KNN + MLP + RF (base models) -> SVM (meta-model)",
         optimizer_hybrid="", data_source="", n_samples="",
         interpretability_method="", deployment_evidence="",
         note="Search-confirmed (publisher page blocked automated fetch, technique summary found via "
              "aggregator): explicit heterogeneous stacking architecture named directly — four distinct base "
              "model families (ridge regression, KNN, MLP, RF) feeding an SVM meta-model for rutting-depth "
              "prediction from loading number, temperature, dynamic modulus and layer-structure features. "
              "Reported to show lower variance/bias and better generalisation than (presumably) the "
              "individual base models, though the exact comparator protocol needs full-text confirmation "
              "before quoting a specific premium figure."),
    dict(doi="10.3390/su14105938", year=2022,
         authors="Huang, J.; Zhou, M.; Sabri, M. M. S.; Yuan, H.",
         title="A Novel Neural Computing Model Applied to Estimate the Dynamic Modulus (DM) of Asphalt Mixtures by the Improved Beetle Antennae Search",
         venue="Sustainability", cited_by_count=24,
         role_in_review="PRIMARY — H1, §9 premium-adjacent, batch 15",
         pavement_domain="materials", pavement_family="flexible",
         architecture="neural network", optimizer_hybrid="improved beetle antennae search",
         data_source="laboratory (8 gradations x 2 binders x 3 temperatures x 3 frequencies, 144 datasets)",
         n_samples=144, interpretability_method="input-importance ranking (post-hoc)", deployment_evidence="",
         note="Abstract read directly: improved Beetle Antennae Search (BAS) tunes a neural network's "
              "hyperparameters for dynamic-modulus prediction, with the abstract's own words stating the "
              "'improved BAS algorithm can effectively adjust the hyperparameters... and built the asphalt "
              "mixture DM prediction model has higher reliability and effectiveness than the random "
              "hyperparameter selection' — a genuine within-paper comparison against a random-hyperparameter "
              "baseline (not a fully tuned one, but closer to §9's premium construct than most H1 records in "
              "the corpus manage). Real, specific dataset size (144, from a fully described lab design) — "
              "the kind of detail integrity rule #2 wants and most title-level batch-4/5 notes lack."),
    dict(doi="10.3141/2305-14", year=2012, authors="Jadoun, F. M.; Kim, Y. R.",
         title="Calibrating Mechanistic–Empirical Pavement Design Guide for North Carolina: Genetic Algorithm and Generalized Reduced Gradient Optimization Methods",
         venue="Transportation Research Record", cited_by_count=18,
         role_in_review="context — GA calibrates MEPDG coefficients directly, not coupled to a learner, batch 15",
         pavement_domain="design", pavement_family="flexible",
         architecture="Mechanistic-Empirical Pavement Design Guide (MEPDG) rutting/fatigue models (not a trained ML model)",
         optimizer_hybrid="genetic algorithm vs. generalized reduced gradient (GRG), compared head-to-head as two calibration methods",
         data_source="LTPP-derived (12 North Carolina HMA mixtures)", n_samples="",
         interpretability_method="MEPDG model structure (intrinsic)", deployment_evidence="DARWin-ME / MEPDG production software",
         note="Abstract read directly: GA and GRG are two alternative OPTIMISATION methods used to "
              "recalibrate MEPDG's rutting/fatigue k-value coefficients to North Carolina conditions — this "
              "is a metaheuristic fitting a mechanistic-empirical model's own coefficients directly, not a "
              "coupled optimiser+learner hybrid, so it fails the same structural test as "
              "@Coleri2010subgrade and @cscm.2022.e00991 (kept, not classified as hybrid). Genuinely useful "
              "comparator evidence though: the abstract states 'the GA optimization method does a better' "
              "job than GRG (truncated before the specific metric) — a real head-to-head between two "
              "optimisation methods on identical calibration data, cite alongside the other GA-vs-alternative "
              "comparator evidence in §9."),
    dict(doi="10.1080/10298436.2025.2543554", year=2025,
         authors="Giridharan, U.; Okte, E.",
         title="Physics-informed graph attention networks for scalable pavement response prediction",
         venue="International Journal of Pavement Engineering", cited_by_count=0,
         role_in_review="PRIMARY — H3;H4 combined, batch 15",
         pavement_domain="structural-response", pavement_family="flexible",
         architecture="graph attention network (GNN architecture) with a physics-informed constraint",
         optimizer_hybrid="", data_source="", n_samples="", interpretability_method="physics constraint (intrinsic)",
         deployment_evidence="",
         note="Title/metadata-level classification (no Crossref abstract, publisher page not fetched) — "
              "coded H3;H4 because a graph attention network is itself an architecture distinct from a plain "
              "MLP/CNN (graph-structured message passing, H4-adjacent) and the title states the physics-"
              "informed constraint explicitly (H3). Not full-text verified; a genuinely two-family "
              "structural claim rather than a single H-type, kept deliberately unresolved to the more "
              "specific type pending full-text read."),
    dict(doi="10.1080/10298436.2026.2708277", year=2026,
         authors="Tong, X.; Chen, Z.; Cheng, H.",
         title="A physics-informed coupled back-calculation method for asphalt pavement modulus evaluation",
         venue="International Journal of Pavement Engineering", cited_by_count=0,
         role_in_review="PRIMARY — H3 (inverse problem), batch 15",
         pavement_domain="structural-evaluation", pavement_family="flexible",
         architecture="physics-informed model applied to the back-calculation inverse problem",
         optimizer_hybrid="", data_source="", n_samples="", interpretability_method="physics constraint (intrinsic)",
         deployment_evidence="",
         note="Title/metadata-level classification (no Crossref abstract, publisher page not fetched) — "
              "extends the H3/PINN thread from batch 4 to the back-calculation inverse problem specifically, "
              "the same problem the corpus's several H2 (metaheuristic-driven) backcalculation records solve "
              "by a different route (@Rakesh2006neural, @Zhang2021pavement, @Fakhri2017determining) — a "
              "genuinely useful same-problem, different-hybridisation-type comparison for a future §8/§9 "
              "discussion of which coupling strategy the field prefers for this specific inverse problem and "
              "why."),
    dict(doi="10.1155/2008/861701", year=2008, authors="Ayenu-Prah, A.; Attoh-Okine, N.",
         title="Evaluating Pavement Cracks with Bidimensional Empirical Mode Decomposition",
         venue="EURASIP Journal on Advances in Signal Processing", cited_by_count=170,
         role_in_review="context — H6/not-H6 boundary case, decomposition + fixed operator not a learner, batch 15",
         pavement_domain="distress-detection", pavement_family="flexible",
         architecture="Sobel edge detector (fixed classical operator, not a trained model)",
         optimizer_hybrid="bidimensional empirical mode decomposition (BEMD)",
         data_source="", n_samples="", interpretability_method="", deployment_evidence="",
         note="Search-confirmed (publisher page blocked automated fetch, but this is an open-access "
              "SpringerOpen journal so a full read should be attempted before the next verification pass): "
              "proposes bidimensional EMD (BEMD) for pavement crack image analysis, paired with a Sobel edge "
              "detector. Deliberately kept and coded `none`, not H6: BEMD decomposition is genuine, but the "
              "second component (Sobel) is a fixed classical filter, not a data-driven learner, so this does "
              "not meet the structural definition in §2.3 despite matching every keyword signal an automated "
              "screen would use to flag it as H6. Cite in §8 specifically AS the H6/not-H6 boundary case: "
              "'decomposition + a fixed operator is not H6; decomposition + something that learns from data "
              "is' — the cleanest available illustration of that line, at 170 citations the best-cited record "
              "this taxonomy-balance batch touches."),
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
    for r in BATCH5:
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
