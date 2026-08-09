# PAVE-ML — appraisal and reporting instrument, with operational coding rules

**Manuscript role:** Reproduced as Table 4 in the main text (`manuscript.qmd` §12,
`@tbl-paveml`); this document supplies the operational decision rules, worked
examples, and reliability procedure that make the table's coding reproducible
rather than a matter of reader judgement — see §2 (Review methodology) for how
this connects to the review's overall protocol.
**Version:** 1.0 — includes the 4 hybrid-specific items (12a–12d), added to keep
this file in sync with the manuscript table after they were introduced during
taxonomy design; previously these existed only in `01_SCOPE_AND_TAXONOMY.md` and
the manuscript itself, which was a real (now-fixed) inconsistency, not a
hypothetical one — see `CLAUDE.md` if you're wondering why this note is here.

---

## Why the coding rules come first

The audit in §12 (with supporting evidence in §7 and §9) is the paper's central claim. Its credibility rests entirely on whether two
people reading the same paper assign the same codes. Vague criteria produce a κ around 0.4 and
a reviewer who asks, fairly, whether the audit measures the literature or the auditors. So the
rules below are written to be applied mechanically, and each has an explicit *default when the
paper is silent*. Silence is the most common condition in this literature, and how it is treated
determines the headline numbers — so it must be stated in the manuscript, not buried.

**Governing convention: silence is recorded as absence, never as compliance.** If a paper does
not report that it held out an independent test set, the code is `no`, not `unclear`. This is
the convention used in clinical-prediction appraisal (TRIPOD, PROBAST) and it is the only one
that resists the charge of charitable coding. It will produce uncomfortable numbers. That is the
point of an audit.

---

## Part A — the 24-item PAVE-ML checklist (20 general + 4 hybrid-specific)

Items are grouped in five domains. Each is answered **Yes / No / Not applicable**, with a
required source (page, section, or figure) for every Yes.

### D1. Data provenance and structure

| # | Item |
|---|---|
| 1 | The origin of every record is stated (laboratory programme, named field project, named public database, or simulation), together with the acquisition period. |
| 2 | The unit of observation is defined, and the paper states whether records are independent — in particular, whether multiple records derive from the same specimen, section, image, or site. |
| 3 | Sample size is reported for each split, and the ratio of records to fitted parameters (or of records to candidate input variables) can be computed from the text. |
| 4 | The range of every input and of the target is given, and the paper states explicitly that predictions outside those ranges are not supported. |

### D2. Preprocessing and partitioning

| # | Item |
|---|---|
| 5 | The split is described precisely enough to reproduce: mechanism (random, stratified, temporal, spatial/section-blocked, source-held-out), proportions, and random seed or its absence. |
| 6 | Every fitted preprocessing step — scaling, imputation, resampling, feature selection, outlier removal, augmentation — is stated to have been fitted **inside** the training partition only. |
| 7 | If records are non-independent (item 2), the split respects the grouping, so that no specimen, section, image, or site appears in more than one partition. |
| 8 | Class imbalance, censoring, or target skew is reported and its treatment described. |

### D3. Modelling and comparison

| # | Item |
|---|---|
| 9 | The architecture is fully specified: layers, widths, activations, regularisation, and, for ensembles, base learner and count. |
| 10 | The hyperparameter search is described — space, method, budget — and the partition used to select hyperparameters is named and is not the reported test partition. |
| 11 | At least one baseline is a *tuned* conventional model, and, where a domain model exists for the target (e.g. Witczak or Hirsch for dynamic modulus, the MEPDG transfer functions for IRI, rutting or faulting, layered-elastic solutions for pavement response), it is included as a comparator. |
| 12 | Where a metaheuristic is used, it is stated whether it optimises hyperparameters or model weights, and the comparison against a conventionally tuned version of the same learner is reported. |
| 12a *(hybrid-specific)* | The base learner is reported both with and without the hybridising component, on the same partition and metric. |
| 12b *(hybrid-specific)* | Search budget is stated for both hybrid and baseline — function evaluations, iterations × population, or wall-clock time — so that parity can be assessed. |
| 12c *(hybrid-specific)* | Stochastic optimisers are run more than once and the spread across runs is reported, not the best run. |
| 12d *(hybrid-specific)* | Where a newly named optimiser is proposed, it is compared against at least two established optimisers on the same problem, and the No-Free-Lunch implication is acknowledged. |

### D4. Evaluation, uncertainty and interpretation

| # | Item |
|---|---|
| 13 | Metrics suit the task: for imbalanced segmentation, IoU or F1 with the positive class defined, never bare pixel accuracy; for regression, an absolute-error metric in engineering units alongside R². |
| 14 | Performance is reported for training **and** held-out partitions, with dispersion (fold standard deviation, confidence interval, or repeated-run range), not a single point estimate. |
| 15 | Predictive uncertainty is quantified for individual predictions — conformal intervals, deep ensembles, MC dropout, Gaussian-process variance, or quantile regression — or the omission is acknowledged. |
| 16 | Any interpretation output (SHAP, PDP, Garson, connection weights, NCA, attention) is accompanied by a statement of the validation status of the model it explains, and by a check of whether the attributions are consistent with established mechanics. |

### D5. Generalisation, transparency and use

| # | Item |
|---|---|
| 17 | The model is evaluated on at least one dataset from an **independent source** — different agency, region, laboratory, test track, or acquisition campaign — or the absence of external validation is stated as a limitation in the conclusions, not only in a mid-paper aside. |
| 18 | Code and trained weights are available at a persistent identifier; data are available or the barrier to release is named. |
| 19 | Computational cost is reported: training time, inference time per record or image, and hardware. |
| 20 | The intended decision context is stated — which engineering decision the output would inform, at what level (project or network), and what accuracy that decision actually requires. |

---

## Part B — operational coding rules (the fields cited throughout the review's analysis sections)

These map the checklist onto the database fields defined in `00_MANUSCRIPT_ARCHITECTURE.md` §3.5.

### `leakage_risk`

- **high** — any one of: (a) scaling, imputation, feature selection, or outlier removal
  described before the split or over the full dataset; (b) synthetic augmentation or
  oversampling applied before the split; (c) non-independent records (repeated specimens,
  multiple records per pavement section, patches from one image) split at record level rather
  than group level; (d) the reported test partition also used for hyperparameter selection.
- **moderate** — none of the above is visible, but the preprocessing order is not stated and the
  design makes the error plausible (e.g. a tabular dataset compiled from literature with likely
  duplicate mixes).
- **low** — the paper states the split precedes all fitted preprocessing and, where records are
  grouped, that the split is grouped.
- **cannot-assess** — reserved for papers where the modelling section is too thin to place in any
  of the above. Report this count separately; a large one is itself a finding.

> Worked case. Xiao et al. (2023, 10.3390/app132312862) apply Boruta feature selection to 17
> candidate variables over 160 LTPP observations and then report R² = 0.906. Unless the full text
> establishes that Boruta ran inside each training fold, this codes **high**. The paper is a good
> paper by the field's conventions; that is precisely why it belongs in the audit rather than in
> a list of bad actors. The audit sections must be about a systemic convention, not about individuals.

### `external_validation`

- **yes** — evaluated on data whose *source* differs from the training data: a different agency,
  region, laboratory, test track, or campaign. A random hold-out from the same pool is not
  external validation, however large.
- **no** — everything else, including "validation sets" that are random splits of one pool.

> Worked case. Elbagalati et al. (2017, 10.1139/cjce-2017-0132) train on a Louisiana deflection
> programme and evaluate on an independent Minnesota programme; R² falls from 0.73 to 0.72. This
> codes **yes**, and the near-absence of degradation is the interesting result. It is also the
> benchmark against which the field's typical 0.99-on-random-holdout should be read.

### `baseline_strength`

- **strong** — at least one tuned conventional learner **and** the relevant domain/mechanistic
  model.
- **moderate** — tuned conventional learners only, or a domain model without tuned ML
  comparators.
- **weak** — untuned comparators, default-setting comparators, comparisons drawn from other
  papers' published numbers on different data, or no comparator at all.

> Worked case. Zeiada et al. (2025, 10.28991/cej-2025-011-01-06) individually optimise eight
> algorithms and compare against Witczak NCHRP 1-37A, 1-40D and Hirsch. **strong** — and the
> outcome, that bagged ensembles beat the deep architectures, is what a strong baseline is for.

### `uncertainty_quantified`

**yes** only for interval or distributional output on individual predictions. Cross-validation
fold spread is dispersion of the *estimate*, not of the *prediction*, and codes **no** — though
it is recorded separately under item 14, because a field that reports neither is in a different
condition from one that reports only the former.

### `interpretability_method` — with a validity qualifier

Record the method, and additionally record whether the explained model met the external-validation
criterion. The §10 argument turns on this pairing: an attribution computed on a model that has
never been tested outside its own data ranks the structure of that dataset, not the physics of
the pavement. We expect this pairing to be rare, and if it is, that is the finding to report.

### `deployment_evidence`

Ordered ladder — record the highest rung reached:

`none` → `equation` (closed-form model a practitioner could apply) → `GUI/software` →
`named released tool` → `specification or design-guide input` → `integrated into an agency PMS`
→ `field trial or documented agency adoption`

> The distribution across this ladder is Figure 12 and, in our reading of the corpus so far, is
> likely to be the most quotable number in the paper.

---

## Part C — reliability procedure

1. Freeze this document before coding begins. Any later change is logged with a date and applied
   retrospectively to all coded records.
2. Both coders independently code a random 15% of the included studies (target n ≈ 60).
3. Report Cohen's κ per field. Fields below κ = 0.60 get their rule rewritten and that field is
   recoded in full — do not paper over a weak κ with a footnote.
4. Disagreements on the remaining records resolved by discussion; a third reader breaks ties.
5. Publish the coded database as supplementary material with DOIs. A rigour audit that does not
   release its own data would be self-refuting.

---

## Part D — how to present this without antagonising the field

The audit will show that a large share of a literature many reviewers have contributed to does
not meet criteria that were not conventional when the work was done. Two rules keep this
constructive, and they are also what keeps the paper publishable:

- **Judge the convention, not the authors.** Report distributions and trends. Name individual
  papers only as *positive* exemplars, or where a specific methodological point cannot be made
  without the example — and then frame it as a widespread pattern that the paper happens to
  illustrate clearly.
- **Audit ourselves first.** Ghanizadeh et al. (2023, 10.3390/infrastructures8080125) reports
  99.09% accuracy on n = 109. Under our own rules that is a small-n, high-skill result without
  external validation. Saying so, in our own voice, about our own co-author's work, does more for
  the paper's credibility than any amount of hedging — and it removes the obvious reviewer attack
  before it is made.
