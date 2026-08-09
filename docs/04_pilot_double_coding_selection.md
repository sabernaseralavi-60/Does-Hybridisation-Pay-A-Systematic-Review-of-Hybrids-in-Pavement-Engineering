# Pilot double-coding — selection record

**Sent to:** Dr. Ali Reza Ghanizadeh, as an independent blind coder
**Sent:** 2026-08-09
**Files sent:** `PAVE-ML_Coding_Instructions.docx`, `PAVE-ML_pilot_coding_sheet.xlsx`,
`PAVE-ML_full_instrument_reference.pdf` (a clean PDF export of `03_PAVE-ML_instrument.md`)

This is the permanent record of exactly which 14 papers were selected and in what
(randomised, seed=42) order they were presented to him — so that when his completed
sheet comes back, it can be matched to the correct existing codes without ambiguity.
**Do not regenerate this selection** — use this list, so the comparison is apples-to-apples.

## Selection method

Stratified across hybrid_type to stress-test the rubric on every category rather than
the most common one: H1×3 (incl. 2 already full-text-verified, as an embedded validity
check), H2×1, H3×1 (the only H3 in the corpus), H4×2, H5×2 (incl. 1 full-text-verified
positive exemplar), H7×2, and 2 boundary cases coded `none` (one a vocabulary-trap case,
one a genuine tuned-baseline exemplar) — a natural, non-cherry-picked spread resulted.

## The 14 papers, in the order presented to the blind coder

| # in sheet | DOI | Existing `hybrid_type` (NOT shown to coder) | Title |
|---|---|---|---|
| 1 | `10.3390/ma18122913` | H5 | Predicting rheological properties of asphalt modified with mineral pow |
| 2 | `10.1016/j.cscm.2022.e00991` | none | Introducing mathematical modeling to estimate pavement quality index o |
| 3 | `10.1111/mice.70169` | H4 | A spatiotemporal prediction method for the evolution of pavement distr |
| 4 | `10.3390/s23073772` | H4 | Automatic pavement crack detection transformer based on convolutional  |
| 5 | `10.28991/cej-2025-011-01-06` | none | Benchmarking classical and deep machine learning models for predicting |
| 6 | `10.1155/2023/1827117` | H7 | Indirect estimation of swelling pressure of expansive soil: GEP versus |
| 7 | `10.1177/03611981241245991` | H3 | Roughness prediction of jointed plain concrete pavement using physics  |
| 8 | `10.1038/s41598-024-81311-3` | H1 | Assessment of resilient modulus of soil using hybrid extreme gradient  |
| 9 | `10.1155/2020/8824135` | H5 | Prediction of highway tunnel pavement performance based on digital twi |
| 10 | `10.1007/s41062-020-00312-z` | none | Artificial neural network back-calculation of flexible pavements with  |
| 11 | `10.1016/j.sandf.2020.02.010` | H2 | Development of genetic-based models for predicting the resilient modul |
| 12 | `10.1186/s44147-025-00706-9` | H1 | A hybrid machine learning method of support vector regression with par |
| 13 | `10.3390/app132312862` | H1 | Optimizing faulting prediction for rigid pavements using a hybrid SHAP |
| 14 | `10.1038/s41598-024-61313-x` | H7 | A formulation for asphalt concrete air void during service life by ado |

## When results come back

1. Do NOT just eyeball agreement — compute it field by field (hybrid_type, leakage_risk,
   external_validation, baseline_strength, hyperparam_reporting, uncertainty_quantified,
   interpretability_method, deployment_evidence). A simple percent-agreement is a start;
   Cohen's κ (which corrects for chance agreement) is what the manuscript promises.
2. For the 3 embedded full-text-verified papers (rows corresponding to
   `10.1186/s44147-025-00706-9`, `10.3390/app132312862`, `10.3390/ma18122913`), check
   whether Dr. Ghanizadeh's independent judgement matches what full-text reading already
   confirmed — this is a stronger validity check than agreement with the first-pass coder,
   since it's checking against verified ground truth, not just coder-to-coder consistency.
3. Any field below roughly κ = 0.60 needs its decision rule reviewed and tightened (see
   `03_PAVE-ML_instrument.md` Part C) — a low κ is informative, not just a problem to bury.
4. Disagreements get discussed and reconciled together, not silently resolved by one side.
5. Report the actual κ values in the manuscript's methodology section (§2.7) and the
   PAVE-ML reliability paragraph (§12) — replacing the current placeholder language that
   promises this procedure without yet showing its result.