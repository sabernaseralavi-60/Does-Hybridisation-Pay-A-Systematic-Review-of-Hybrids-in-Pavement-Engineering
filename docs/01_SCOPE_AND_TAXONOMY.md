# Scope, taxonomy and operational definitions — hybrid models review (v1)

Supersedes §1–§3 of `00_MANUSCRIPT_ARCHITECTURE.md`. The section plan below replaces the
14-section plan in that document; §2 as drafted in `02_MANUSCRIPT_S2_methodology.md` transfers
almost unchanged, and `03_PAVE-ML_instrument.md` gains one new item block (§4.4 here).

---

## 1. The vocabulary problem — and why it changes the search design

The observation that many qualifying studies never use the word *hybrid* is correct, and it is
the single most dangerous recall failure available to us. A test query built from algorithm names
alone confirmed it in two directions at once:

- **False negatives avoided.** Alhussan et al. (2022, 10.1109/access.2022.3196660, 106 citations)
  couple an adaptive-mutation dipper-throated optimiser to a random forest for pothole
  classification, benchmark it against WOA+RF, GWO+RF and PSO+RF, and lead with the word
  *optimization*, not *hybrid*. A label-driven search misses it. An algorithm-name search finds it
  immediately.
- **False positives introduced.** The same query pulled back geopolymer concrete, rock-burst
  prediction, flyrock from surface blasting, iron-ore price forecasting and residential energy
  load. Metaheuristic-plus-learner vocabulary is generic across all of civil and mining
  engineering, so the pavement block must be mandatory and strict, not a soft filter.

The design consequence is that **the search runs on algorithm names, and inclusion runs on
structure — never on the authors' label.**

### Alternative self-descriptions observed in the corpus so far

`hybrid` · `hybridised/hybridized` · `optimised/optimized X` · `improved X` · `enhanced X` ·
`novel X–Y` · `X-based Y` · `coupled` · `integrated` · `combined` · `X-assisted` ·
`X-tuned` · `evolutionary X` · `nature-inspired X` · `swarm-optimised X` · `stacked` ·
`ensemble of` · `decomposition-based` · `neuro-fuzzy` · `physics-informed` · `knowledge-guided`

None of these is treated as a criterion. They are treated as *search bait*.

---

## 2. Operational definition of hybridity (structural, not lexical)

> **A study is in scope if its predictive pipeline couples two or more components drawn from
> different methodological families, where at least one component is a learned data-driven model
> and the coupling is claimed or demonstrated to affect predictive performance.**

Three clarifications that will decide most borderline cases:

- **Hyperparameter search counts only when the searcher is a metaheuristic or a
  surrogate-based optimiser** (PSO, GA, GWO, TLBO, Bayesian optimisation, TPE/Optuna). Manual
  tuning and exhaustive grid search do **not** make a model hybrid — but they are recorded,
  because they are the baseline against which the hybridisation premium (§4) is measured.
- **An ensemble of one family is not a hybrid.** Random forest is not a hybrid; a stacked
  RF→XGBoost meta-learner is (H5).
- **Self-description is irrelevant in both directions.** A paper calling itself hybrid because it
  "combines statistics and engineering judgement" is out; a paper calling itself nothing while
  running GWO over an LSSVM is in.

---

## 3. Taxonomy of hybridisation (H1–H7)

No prior review distinguishes these. They are lumped under one label, which is precisely why the
field cannot say which kinds of hybridisation earn their complexity. Each type has a distinct
justification and a distinct failure mode — the second column is the review's analytical spine.

| Type | Coupling | Theoretical justification | Characteristic failure mode |
|---|---|---|---|
| **H1** | Metaheuristic → hyperparameters | Non-convex, discrete hyperparameter space that gradient methods cannot search | Compared against an *untuned* base learner, so the reported gain is the tuning, not the metaheuristic |
| **H2** | Metaheuristic → weights / structure | Escapes local minima of backpropagation; enables non-differentiable objectives | Vastly more function evaluations than the baseline gets; no compute-parity reporting |
| **H3** | Physics + data (PINN, mechanistic residual, transfer function as loss) | Constrains the solution to a mechanically admissible manifold; helps under data scarcity | Physics term weight tuned on the test set; constraint too weak to bind |
| **H4** | Architecture fusion (CNN+transformer, two-stream, CNN+classical operator) | Complementary inductive biases: local texture plus long-range context | Gains confounded with parameter count and training budget |
| **H5** | Heterogeneous stacking / blending | Decorrelated errors across model families | Meta-learner trained on in-fold predictions; leakage through the stacking layer |
| **H6** | Signal decomposition then learn (VMD, EMD, CEEMDAN, EWT, wavelet) | Separates scales the learner would otherwise have to disentangle | Decomposition fitted on the full series before the temporal split — the most common severe leakage in this family |
| **H7** | Symbolic–numeric (GEP, MGGP, EPR + a numeric optimiser) | Yields a closed-form, inspectable expression | Expression complexity uncontrolled; equation overfits and is then quoted as if it were physics |

Ghanizadeh's corpus spans H1, H2, H3-adjacent and H7 — which is why this scope makes his work
central without any strain: EPR-TLBO for asphalt air voids (H7), WNN-PSO for liquefaction (H2),
XGBoost-FFO for stabilised tailings (H1), METABACKCAL for moduli back-calculation (H2 applied to
an inverse problem), and the ANN back-calculation work with Garson and connection-weight
decomposition that sits at the origin of the interpretability thread.

---

## 4. The hybridisation premium — the paper's headline construct

### 4.1 Definition

For a study reporting a hybrid model *M*<sub>hyb</sub> = optimiser ⊕ base learner *M*<sub>base</sub>
on a held-out partition, the **hybridisation premium** is

> Δ = *performance*(*M*<sub>hyb</sub>) − *performance*(*M*<sub>base</sub><sup>tuned</sup>)

where *M*<sub>base</sub><sup>tuned</sup> is the same base learner tuned by a conventional
procedure under a **comparable evaluation budget**, evaluated on the **same** partition with the
**same** metric.

The three constraints are the whole point. A premium computed against an untuned default-setting
baseline is not a premium; it is a measurement of default settings.

### 4.2 What we can measure, and what we will report

Most studies will not permit Δ to be computed. That is the finding. We report, over the coded
corpus:

- **`premium_computable`** — yes / no. Requires a same-partition, same-metric tuned baseline.
- **`premium_value`** — where computable, in the study's own metric plus a standardised form.
- **`budget_parity_reported`** — whether function evaluations, wall-clock time or search-budget
  equivalence is stated for hybrid and baseline. Expect this to be near zero.
- **`optimiser_novelty_claim`** — whether the study's novelty rests on the optimiser being new,
  and whether it is compared against established optimisers on the same problem.

### 4.3 The evidence already in hand

Three records in `seed_bibliography.csv` make the case before any further coding:

- **Azam et al. (2022, 10.1038/s41598-022-17429-z)** run six swarm optimisers over one LSSVM. The
  top three land at RMSE 6.72 / 6.78 / 6.79 MPa and R² 0.942 / 0.940 / 0.940. Those separations
  are well inside what a different random seed would produce, yet they are reported as a ranking
  and a recommendation.
- **Duan (2024, 10.1038/s41598-024-81311-3)** reports BKA-XGBoost at R² = 0.995 against nine
  comparators, with no statement that the comparators received equivalent tuning effort.
- **Zeiada et al. (2025, 10.28991/cej-2025-011-01-06)** individually optimise eight algorithms
  and benchmark against Witczak and Hirsch. With tuning parity enforced, the winner is a bagged
  ensemble — not a deep or hybrid architecture.

Read together: **when the baseline is tuned, the hybrid advantage shrinks or reverses.** That is
a publishable claim, and the audit is what turns it from an anecdote into a finding.

### 4.4 New PAVE-ML items (append to `03_PAVE-ML_instrument.md`, domain D3)

| # | Item |
|---|---|
| 12a | The base learner is reported both with and without the hybridising component, on the same partition and metric. |
| 12b | Search budget is stated for both hybrid and baseline — function evaluations, iterations × population, or wall-clock time — so that parity can be assessed. |
| 12c | Stochastic optimisers are run more than once and the spread across runs is reported, not the best run. |
| 12d | Where a newly named optimiser is proposed, it is compared against at least two established optimisers on the same problem, and the No-Free-Lunch implication is acknowledged. |

---

## 5. Title

Both requirements are met: the words *review*, *metaheuristic optimisation* and *machine
learning* are in the title, which matters for retrieval and for later citation.

**Recommended (16 words):**

> **Does Hybridisation Pay? A Systematic Review of Metaheuristic Optimisation and Machine
> Learning Hybrids in Pavement Engineering (2005–2026)**

**Broader alternative (19 words) — if we keep H3–H7 at full weight:**

> **Does Hybridisation Pay? A Systematic Review and Critical Appraisal of Hybrid Data-Driven
> Models — Metaheuristic, Physics-Informed and Ensemble — in Pavement Engineering (2005–2026)**

**Conservative alternative, if a reviewer objects to a question-form title:**

> **Hybrid Metaheuristic–Machine Learning Models in Pavement Engineering: A Systematic Review and
> Critical Appraisal of Reported Performance Gains (2005–2026)**

A note worth acting on: question-form titles are retrieved and shared more, but a minority of
engineering editors dislike them. Put the recommended form in the submission and keep the
conservative form ready for a revision request — it is a one-line change and not worth arguing
over.

**Scope consequence to decide.** The recommended title centres H1–H2 and treats H3–H7 as
surveyed context. The broader alternative gives all seven equal weight, which roughly doubles the
corpus and pulls the vision literature (H4) back in. My advice is the recommended form: a
narrower corpus audited properly beats a wider one summarised. H3–H7 still get a full taxonomy
section and a research-agenda entry.

---

## 6. Revised section plan (≈17,500 words)

| § | Title | Words |
|---|---|---|
| 1 | Introduction: hybridisation as the field's dominant novelty claim | 1,100 |
| 2 | Review methodology (PRISMA, algorithm-driven search, structural inclusion rule) | 1,300 |
| 3 | Bibliometric landscape: the optimiser-naming explosion, 2005–2026 | 1,300 |
| 4 | **Taxonomy of hybridisation (H1–H7)** with justification and failure mode | 1,800 |
| 5 | H1/H2 in material and mix modelling | 1,900 |
| 6 | H1/H2 in structural evaluation and inverse analysis | 1,600 |
| 7 | H1/H2 in performance prediction and deterioration | 1,700 |
| 8 | H3–H7 in pavement engineering: physics-informed, fusion, stacking, decomposition, symbolic | 1,800 |
| 9 | **The hybridisation premium: how much of the reported gain survives a tuned baseline** | 2,300 |
| 10 | Interpretability and uncertainty in hybrid pipelines | 1,400 |
| 11 | From premium to decision: does the gain change any engineering decision? | 1,200 |
| 12 | PAVE-ML: reporting and appraisal checklist for hybrid pavement models | 1,000 |
| 13 | Research agenda | 1,100 |
| 14 | Conclusions | 700 |

§11 is new and is the strongest single addition. Hosseini and Smadi (2021,
10.3390/infrastructures6020028) priced the cost consequence of prediction error over a 20-year
horizon; against that curve, a premium of ΔR² = 0.004 can be shown to move no decision at all.
Stating that plainly, with their numbers, is the sentence the paper will be cited for.
