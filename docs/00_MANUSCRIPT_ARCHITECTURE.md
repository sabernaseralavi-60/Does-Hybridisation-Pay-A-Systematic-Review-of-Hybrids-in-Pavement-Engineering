# ANN & Deep Learning in Pavement Engineering — Manuscript Architecture (v1)

**Status:** Stage 1 deliverable — positioning, scope, structure, corpus protocol.
**Prepared for:** S. S. Naseralavi (Shahid Bahonar University of Kerman) & A. R. Ghanizadeh (Sirjan University of Technology).
**Date:** August 2026.

---

## 1. The positioning problem (read this first)

The working title — *"Application of Artificial Neural Network and Deep Learning Methods in
Pavement Engineering: A Review"* — collides almost word-for-word with an existing, well-cited
paper:

> Yang, X., Guan, J., Ding, L., et al. (2021). *Research and applications of artificial neural
> network in pavement engineering: A state-of-the-art review.* **Journal of Traffic and
> Transportation Engineering (English Edition)**, 8(6), 1000–1021.
> DOI: 10.1016/j.jtte.2021.03.005 — 683 papers retrieved, 143 reviewed in depth; ~111 citations
> and still accumulating ~26/yr.

Adjacent territory is also occupied:

| Existing review | Year | Territory it owns |
|---|---|---|
| Gopalakrishnan, *Data* 3(3):28 (10.3390/data3030028) | 2018 | DL for pavement image analysis / distress detection |
| Cao, Liu & He, *IEEE Access* 8 (10.1109/access.2020.2966881) | 2020 | Pavement defect detection: image processing → ML → DL → 3D |
| Hou et al., *Engineering* 6(12) (10.1016/j.eng.2020.07.030) | 2020 | Intrusive sensing + image processing + ML in pavement monitoring |
| Rasol et al., *Constr. Build. Mater.* 324 (10.1016/j.conbuildmat.2022.126686) | 2022 | GPR + ML for road infrastructure |
| Cavalli et al., *J. Road Eng.* (10.1016/j.jreng.2023.12.001) | 2023 | Advanced road materials/structures/detection (39-author omnibus) |
| Zagvozda et al., *ACAE* (10.13167/2026.32.7) | 2026 | AI for distress detection on lower-ranking roads (bibliometric + systematic) |
| Hariri Asli et al., *J. Infrastruct. Preserv. Resil.* (10.1186/s43065-026-00178-y) | 2026 | AI for IRI prediction, rigid & composite pavements |

**Consequence.** A Q1 editor running the same duplication check we just ran will reject a
generic "ANN/DL in pavement engineering" survey at desk, or a reviewer will ask the fatal
question: *what does this add over Yang et al. (2021)?* Novelty in a review is not the topic —
it is the **analytical frame**. We need a frame nobody has occupied.

---

## 2. Proposed repositioning

### 2.1 Recommended title (primary)

> **From Accuracy to Evidence: A Critical Appraisal of Neural and Deep Learning Models in
> Pavement Engineering (2005–2026) — Methodological Rigour, Interpretability, and the
> Deployment Gap**

Shorter variant for journals with title-length limits:

> **Neural and Deep Learning Models in Pavement Engineering: A Critical Appraisal of
> Methodological Rigour, Interpretability and Deployment (2005–2026)**

### 2.2 What makes it defensibly new

Four claims, each of which is *empirically testable against the corpus* rather than rhetorical:

1. **Rigour audit (the core contribution).** No existing review in this domain has systematically
   scored the primary literature against a validity rubric. We do: for every included study we
   code data-leakage risk, presence/absence of an *external* (independent-source) test set,
   split protocol, hyperparameter-search reporting, baseline strength, uncertainty
   quantification, and data/code availability. The result is a quantitative statement about how
   much of the field's reported skill is trustworthy — a finding, not a summary.
2. **The 2021–2026 methodological wave.** Yang et al. stop essentially at MLP/CNN/RNN. The
   period since is dominated by (i) metaheuristic-hybridised learners, (ii) gradient-boosted
   ensembles displacing shallow ANNs on tabular pavement data, (iii) explainable AI (SHAP, PDP,
   NCA, connection-weight and Garson decomposition), (iv) physics-informed and mechanics-
   constrained networks, (v) transformer/attention and vision-foundation models, (vi) graph
   neural networks for network-level PMS, (vii) synthetic-data and transfer-learning responses
   to data scarcity. This wave is uncovered.
3. **The tabular-vs-vision split.** The field behaves as two literatures that do not read each
   other: a *materials/mechanics* stream (small tabular datasets, R² competitions) and a
   *vision/monitoring* stream (large image datasets, benchmark-driven). We quantify the split
   and argue their methodological pathologies are opposite and mutually instructive.
4. **The deployment gap.** We trace how many published models reach an agency workflow (PMS
   integration, MEPDG/AASHTOWare input, specification, deployed GUI/API). Preliminary reading
   suggests the number is very small relative to publication volume — a headline finding.

### 2.3 Deliverable artefact (this is what gets the paper accepted)

**PAVE-ML** — a reporting and appraisal checklist for data-driven pavement models
(≈20 items across Data, Modelling, Validation, Interpretation, Deployment), derived *from* the
audit rather than asserted. Reviews that hand the community a usable instrument are cited and
accepted; reviews that hand it a taxonomy are not.

### 2.4 How Ghanizadeh's corpus is served — legitimately

His published work sits directly on four of our sections, so citation is substantive rather than
ornamental:

| Section | Natural anchor in his corpus |
|---|---|
| §5 Structural evaluation & inverse problems | ANN back-calculation with Garson / connection-weight sensitivity (10.1007/s41062-020-00312-z); METABACKCAL metaheuristic back-calculation (Constr. Build. Mater. 492, 2025) |
| §4 Material & mix modelling | Asphalt air-void evolution via EPR-TLBO / MGGP (10.1038/s41598-024-61313-x); hydraulic conductivity of coarse-grained road materials (Transp. Geotech. 54, 2025) |
| §6 Loading, response & test simulation | Equivalent-frequency prediction by FFT+ANN for quasi-static analysis (10.1016/j.ijprt.2017.09.002); fatigue-test loading frequency via MARS & ANN (10.1155/2014/515467) |
| §7 Hybrid metaheuristics + §8 Interpretability + §10 Deployment | WNN-PSO with NCA sensitivity (10.3390/infrastructures8080125); XGBoost-FFO with dual interpretation and GUI (10.3390/ai7020037) |

**Editorial caution.** Self-citation is expected and unremarkable up to roughly 8–12% of the
reference list in an author-team review. Beyond that, Elsevier/Springer editors flag it and it
becomes a rejection reason in its own right. With a 250–350-item reference list, **18–30
Ghanizadeh citations is the safe, defensible ceiling** — which comfortably covers his relevant
output. Padding past that damages the paper.

---

## 3. Corpus protocol (PRISMA 2020)

### 3.1 Sources
OpenAlex (primary, API-harvestable), Scopus, Web of Science Core Collection, Semantic Scholar;
backward/forward snowballing from the seven reviews in §1.

### 3.2 Window
2005-01-01 → 2026-06-30 (the requested 20-year span), with a small set of pre-2005 landmarks
retained for the historical section only (Meier & Rix 1994/1995 FWD back-calculation ANNs;
Ceylan/Gopalakrishnan/Guclu ANN work at Iowa State; Attoh-Okine 1994 pavement ANN).

### 3.3 Query blocks (Boolean, applied to title/abstract/keywords)

```
A (method):  "artificial neural network" OR ANN OR "deep learning" OR "convolutional neural
             network" OR CNN OR "recurrent neural network" OR LSTM OR GRU OR transformer OR
             "graph neural network" OR autoencoder OR "generative adversarial" OR
             "physics-informed neural" OR ANFIS OR "extreme learning machine" OR
             "radial basis function network" OR "multilayer perceptron" OR "wavelet neural"

B (domain):  pavement OR asphalt OR "flexible pavement" OR "rigid pavement" OR subgrade OR
             subbase OR "unbound granular" OR "hot mix asphalt" OR "warm mix asphalt" OR
             bitumen OR "road surface" OR "highway pavement" OR "airport pavement" OR
             "pavement management"

C (task):    prediction OR "back-calculation" OR backcalculation OR detection OR segmentation
             OR classification OR "condition assessment" OR rutting OR fatigue OR cracking OR
             IRI OR roughness OR "resilient modulus" OR "dynamic modulus" OR skid OR
             deterioration OR "remaining service life" OR "maintenance and rehabilitation"

Final:  A AND B AND (C OR review)
```

### 3.4 Inclusion / exclusion

**Include** — peer-reviewed journal articles and full conference papers that (a) train or
evaluate at least one neural or deep architecture, (b) on a pavement-engineering task, (c) with
reported quantitative performance, (d) in English.

**Exclude** — abstracts only; non-neural ML with no neural comparator (kept separately as a
context set); papers where pavement is incidental (e.g. vehicle-dynamics studies using road
roughness only as an input); duplicate reports of the same dataset+model by the same team;
predatory-venue output failing the DOAJ / Master Journal List check.

**Target after screening:** 380–450 included studies, of which ~120 undergo full rigour coding.
(Both numbers get reported in the PRISMA diagram and must match the database exactly.)

### 3.5 Coding rubric (the novel instrument)

Each fully-coded study receives a record with these fields — this is also the database schema
in `seed_bibliography.csv`:

| Field | Values |
|---|---|
| `id`, `doi`, `year`, `authors`, `title`, `venue` | bibliographic |
| `pavement_domain` | design / materials / structural-evaluation / distress-detection / performance-prediction / M&R-and-PMS / construction-QC / other |
| `pavement_family` | flexible / rigid / composite / airfield / unpaved / general |
| `architecture` | MLP, CNN, RNN-LSTM/GRU, ANFIS, RBF, ELM, WNN, GNN, Transformer, GAN, AE, PINN, hybrid-metaheuristic, ensemble-tree (context), other |
| `optimizer_hybrid` | none / GA / PSO / GWO / TLBO / FFO / SOS / HHO / BAS / other |
| `data_source` | laboratory / field-project / LTPP / agency-PMS / public-image-benchmark / simulated-FEM / mixed |
| `n_samples` | integer (records or images) |
| `n_inputs` | integer |
| `split_protocol` | random-holdout / k-fold / nested-CV / temporal / spatial-blocked / external-set / unclear |
| `external_validation` | yes / no |
| `leakage_risk` | low / moderate / high / cannot-assess *(high = scaling or feature selection before split, duplicated records across splits, or per-image patches split at patch level)* |
| `hyperparam_reporting` | full / partial / none |
| `baseline_strength` | strong (tuned classical + mechanistic) / moderate / weak (untuned or none) |
| `uncertainty_quantified` | yes / no |
| `interpretability_method` | none / sensitivity / Garson / connection-weights / NCA / PDP / SHAP / LIME / attention / symbolic-equation |
| `metrics_reported` | R2, RMSE, MAE, MAPE, accuracy, precision/recall, F1, IoU, mAP … |
| `best_reported_R2` / `best_reported_F1` | float |
| `code_available` / `data_available` | yes / no |
| `deployment_evidence` | none / GUI / API / equation-in-spec / PMS-integration / field-trial |
| `critique_note` | free text — the reviewer's own reading, one or two sentences |

---

## 4. Section plan (target ≈ 19,000 words excluding references)

| § | Title | Words | Core content | Figures / Tables |
|---|---|---|---|---|
| 1 | Introduction | 1,000 | Why pavement is a hard modelling domain: heterogeneous, ageing, stochastic loading, expensive labels. Why neural methods took hold. What this review does that prior reviews do not (explicit, named). Contributions list. | — |
| 2 | Review methodology | 1,200 | PRISMA 2020 flow, query blocks, screening, inter-coder agreement (report Cohen's κ on a 15% double-coded subsample), rubric definition, limitations of the protocol. | **F1** PRISMA diagram; **T1** query blocks & yields |
| 3 | Bibliometric landscape | 1,300 | Publication trajectory 2005–2026; architecture share over time (the MLP→CNN→ensemble/hybrid→transformer succession); country & institution networks; venue concentration; keyword co-occurrence; citation-burst detection. | **F2** stacked-area architectures × year; **F3** country co-authorship map; **F4** keyword co-occurrence; **F5** venue treemap |
| 4 | Materials and mix modelling | 2,000 | Dynamic modulus, Marshall/volumetric properties, air-void evolution, rutting & fatigue of mixes, modified/recycled binders, stabilised soils UCS, resilient modulus of subgrade & bases. Critical point: extreme R² homogeneity (0.95–0.99) across incomparable datasets is a red flag, not a success story. | **T2** material-property models: data, inputs, architecture, reported skill, validity flags; **F6** reported R² vs. sample size (the "small-n high-R²" cloud) |
| 5 | Structural response, inverse analysis & NDT | 1,800 | Forward surrogates for layered-elastic/viscoelastic/FEM response; FWD/HWD/TSD back-calculation; GPR interpretation; layer-thickness and bonding-condition inference; seismic/dispersion methods. Critical point: inverse problems are where neural surrogates are genuinely well-posed — and where synthetic-training/field-testing mismatch is systematically underreported. | **T3** back-calculation studies; **F7** synthetic-vs-field validation status |
| 6 | Loading, response spectra & test simulation | 900 | Equivalent-frequency prediction, load-pulse shape, speed and temperature effects, laboratory-test simulation. Compact but distinct; anchors the mechanistic-empirical link. | **T4** |
| 7 | Surface distress detection and segmentation | 2,400 | The vision literature: classification → detection (YOLO family, Faster R-CNN) → semantic/instance segmentation (U-Net, DeepLab, SegFormer) → 3D and multimodal (LiDAR, UAV, sensor fusion). Benchmark datasets (CFD, CRACK500, GAPs, RDD2020/2022, DeepCrack) and the comparability crisis: incompatible IoU definitions, tolerance bands, and train/test partitions make reported gains largely unverifiable across papers. | **T5** benchmark datasets: size, annotation type, licence, splits; **T6** reported segmentation performance with protocol flags; **F8** benchmark fragmentation graph |
| 8 | Performance prediction and deterioration modelling | 1,900 | IRI, PCI, rutting depth, cracking extent, faulting, skid resistance, remaining service life; LTPP as the field's dominant tabular substrate and its consequences (shared-substrate overfitting, near-duplicate publications). Sequence models for time-series condition. | **T7**; **F9** LTPP dependency over time |
| 9 | Network-level decisions: PMS, M&R optimisation, cost & LCA | 1,400 | Budget allocation, treatment selection, RL/approximate DP for maintenance policy, GNN for network topology, coupling prediction models to optimisation. Critical point: the prediction literature and the decision literature barely cite each other. | **T8**; **F10** citation bridge (or lack of it) between §8 and §9 clusters |
| 10 | Interpretability, uncertainty and physics consistency | 1,700 | Sensitivity → Garson/connection-weights → NCA → PDP/ICE → SHAP → attention; symbolic regression (GEP, MGGP, EPR) as intrinsically interpretable alternatives; conformal prediction, deep ensembles, MC-dropout, Bayesian NN; monotonicity and mechanics-consistency constraints; PINNs. Critical point: "interpretability" in this field is overwhelmingly *post-hoc feature ranking on an unvalidated model*, which ranks the artefacts of overfitting. | **T9** interpretability methods & what each can/cannot license; **F11** uptake curve |
| 11 | **Cross-cutting rigour audit** *(the paper's spine)* | 2,200 | Quantified results of the rubric: % with external validation, % with high leakage risk, % reporting hyperparameter search, % with uncertainty, % with code, % with any deployment evidence; stratified by domain and by period. Formal discussion of the small-n/high-R² pathology, weak-baseline inflation, publication bias toward "our model won", and the near-absence of negative results. | **F12** rigour heatmap (criterion × domain); **F13** trend in external validation 2005→2026; **T10** the ten most-cited claims that do not survive the audit |
| 12 | PAVE-ML: a reporting and appraisal checklist | 1,000 | The instrument, item by item, with a worked example applying it to one exemplary and one deficient study. Explicit guidance for authors, reviewers and agencies. | **T11** the checklist |
| 13 | Research agenda | 1,300 | Ten prioritised directions, each stated as a testable question with the data and method that would settle it: benchmark standardisation with fixed splits; leakage-proof protocols for spatially autocorrelated pavement data; foundation models and transfer to low-resource agencies; physics-constrained surrogates for MEPDG acceleration; multimodal fusion (imagery + FWD + GPR + traffic + climate); uncertainty-aware M&R optimisation; digital-twin coupling; federated learning across agencies; equity and transferability to developing-country networks; reproducibility infrastructure. | **T12** agenda × required data × feasibility |
| 14 | Conclusions | 700 | Findings, not a summary. Six numbered conclusions traceable to §11. | — |

**Front matter:** structured abstract (~280 words), 6–8 keywords, highlights (5 × ≤85 chars),
nomenclature table, CRediT statement, data-availability statement, declaration of AI use
(see §6 below), funding, conflicts.

---

## 5. Target journals — ranked shortlist

| Rank | Journal | Publisher | 2-yr mean citedness (OpenAlex) | Why | Risk |
|---|---|---|---|---|---|
| 1 | **Archives of Computational Methods in Engineering** | Springer | 10.3 (h=149) | Review-only journal; a methodological-audit review is exactly its remit; APC ~USD 3,990 but subscription route available | Slower review; wants genuine computational-methods depth |
| 2 | **Automation in Construction** | Elsevier | 11.9 (h=240) | Highest-impact realistic home; publishes critical reviews with instruments | Wants a construction-automation angle foregrounded |
| 3 | **Computer-Aided Civil and Infrastructure Engineering** | Wiley | very high | Prestige; publishes the field's landmark ML papers | Reviews are rare there — check with the editor first |
| 4 | **Journal of Road Engineering** | Elsevier/Chang'an | rising fast | Explicitly commissions state-of-the-art reviews; strong pavement identity | Newer, indexation still maturing |
| 5 | **Transportation Geotechnics** | Elsevier | high | Natural fit for the materials/subgrade half; Ghanizadeh already publishes there | Narrower than our scope |
| 6 | **Engineering Applications of Artificial Intelligence** | Elsevier | high | Method-first framing welcomed | Weaker pavement readership |
| 7 | **International Journal of Pavement Engineering** | Taylor & Francis | moderate | Core domain audience | Lower impact than 1–4 |

*Avoid* the Journal of Traffic and Transportation Engineering (English Ed.) as first choice —
it published Yang et al. (2021) and will read our paper as competing with its own asset.
(Counter-argument: it may also want the successor. Worth a pre-submission enquiry, not a blind
submission.)

**Action:** send a 200-word pre-submission enquiry to editors of #1 and #2 before writing the
full draft. This costs a week and can save a four-month desk rejection.

---

## 6. Integrity constraints — how they are actually met

**Similarity below 10%.** Achieved by construction, not by post-hoc rewriting:
- Every study is read and re-expressed from its *quantitative record* (task, data, n, architecture,
  metric, flaw) in the database, never from its sentences. Prose is written from the table, not
  from the abstract. This is the single most effective anti-similarity method.
- No block quotation. Method names, metric names, standard designations (AASHTO T 307,
  ASTM D6931, MEPDG), and architecture names are technical terms and stay verbatim —
  Turnitin/iThenticate exclusion filters handle these, and altering them would be a scientific
  error. The instruction to preserve specialist vocabulary is correct and will be followed.
- Reference lists, standard equations and the nomenclature table are excluded from the
  similarity computation by the journal's own settings.
- Realistic expectation: a well-written review of this type lands at **4–9%** with the
  bibliography excluded. Sections with heavy standard-designation density will show local
  spikes; that is normal and editors know it.

**Writing quality and AI-detection.** Two things must be said plainly:
1. AI-text classifiers are unreliable in both directions. They flag human-written technical
   English at high rates — formulaic, low-burstiness academic prose is exactly their false-
   positive zone — and they can be fooled by text that is genuinely machine-generated. Nobody
   can promise you a specific score from any tool, and any service that does is selling you
   something.
2. More importantly, **Elsevier, Springer Nature, Wiley, Taylor & Francis and COPE all now
   require disclosure of generative-AI assistance in manuscript preparation.** Disclosed use is
   permitted and routine; *undisclosed* use that is later established is a retraction-grade
   finding. Concealment is the risk here, not the tool. The correct move is a one-line statement
   in the Declaration of Generative AI section — it costs nothing and removes the entire
   exposure.

   So: I will write prose that is specific, argumentative, uneven in rhythm, opinionated where
   the evidence supports an opinion, and dense with the actual numbers from our database —
   which is what good academic writing is, and what generic AI output is not. What I will not do
   is dress the manuscript to defeat a detector while you tell the journal nothing.

3. What genuinely makes the text read as yours: you and Dr Ghanizadeh write §11 and §13 in
   first draft from your own reading, and revise everything else. A review whose critical
   sections carry the authors' actual judgements is unmistakable, and it is also the version
   reviewers accept.

**Acceptance.** No one can guarantee acceptance. What is controllable: a defensible novelty
claim (§2), a real instrument (§12), a verifiable corpus (§3), findings rather than summary
(§11), and a journal that wants this kind of paper (§5). That combination is what moves a
review from "another survey" to "cited for a decade".

---

## 7. Work plan

| Stage | Output | Who |
|---|---|---|
| **1 (done)** | Positioning, architecture, protocol, seed database, harvest script | — |
| 2 | Run `harvest_openalex.py` → raw corpus (expect 1,500–2,500 hits), deduplicate, title/abstract screen to ~600 | Claude drafts screening decisions; you adjudicate borderline cases |
| 3 | Full-text screening → 380–450 included; rigour-code ~120 | Split: Claude codes, Ghanizadeh double-codes 15% for κ |
| 4 | Bibliometric analysis + all 13 figures | Claude (matplotlib/VOSviewer-compatible exports) |
| 5 | Section drafting §3–§10, one section per pass, each fully cited from the database | Claude drafts → you revise |
| 6 | §11, §12, §13 — the argumentative core | You & Ghanizadeh lead; Claude supports with the audit statistics |
| 7 | Assembly, reference formatting (target journal style), Word/LaTeX build, similarity self-check, cover letter, response-to-reviewer templates | Claude |

**Rule for every stage: no citation enters the manuscript unless it exists in the database with a
verified DOI.** Fabricated or mis-attributed references are the fastest route to rejection and
the one error that is unforgivable in a review paper. Nothing gets written from memory.
