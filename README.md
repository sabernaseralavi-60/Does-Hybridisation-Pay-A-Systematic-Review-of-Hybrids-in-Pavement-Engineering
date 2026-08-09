# Does Hybridisation Pay?

### A Systematic Review of Metaheuristic Optimisation and Machine Learning Hybrids in Pavement Engineering (2005–2026)

**Seyed Saber Naseralavi**¹ · **Ali Reza Ghanizadeh**²
¹ Shahid Bahonar University of Kerman · ² Sirjan University of Technology

---

## Summary

Pavement engineering has, over the past decade, adopted a recurring rhetorical move: an
optimisation algorithm is coupled to a machine-learning model, the coupling out-predicts
some comparator, and the coupling itself is offered as the contribution. This review asks a
narrower, checkable question: how often does that reported gain survive a comparison against
the *same* base learner, properly tuned by conventional means, under a comparable search
budget? Reading the literature this way — on the structure of what was actually compared,
not on whether a paper calls itself "hybrid" — surfaces three findings.

**The comparison the field would need to answer its own question is usually missing, not
unfavourable.** Across the studies coded closely enough to test this, the dominant pattern is
not that hybrids lose a fair fight — it is that the fair fight was never staged. Where a
tuned, apples-to-apples baseline *is* reported, the hybrid or deep-architecture advantage
narrows and can reverse outright.

**"Hybrid" currently flattens at least seven structurally distinct couplings into one label**
— a metaheuristic tuning hyperparameters is a different engineering claim from one tuning
network weights, which is different again from a physics-constrained loss term, a
heterogeneous stacking ensemble, a decomposition front-end, or a symbolic-regression
component. Each has its own theoretical justification and its own characteristic failure
mode; collapsing them under one word is precisely what has kept those failure modes
undiscussed.

**A specific, identifiable pattern of data reuse is worth naming plainly.** At least nine
papers by one overlapping author team report single-target models — international roughness
index, rutting, cracking, faulting, friction — each as its own publication, all apparently
drawn from the same ~33-section, ~395-observation LTPP substrate. Full-text verification of
two of these confirms an ungrouped, observation-level cross-validation split on that shared
substrate — a leakage mechanism the paper traces mechanically, not by inference from the
abstract.

The review contributes a structural taxonomy (H1–H7) for classifying what a "hybrid" pavement
model actually couples, an operational **hybridisation premium** construct for measuring
whether that coupling earns its complexity, and **PAVE-ML**, a 24-item reporting and appraisal
checklist that can be applied to any future study in this space at no added experimental
cost — every item asks for something most studies already have, just doesn't currently
report.

---

## Repository contents

| Path | Contents |
|---|---|
| `manuscript.qmd` | The paper. Builds to PDF, DOCX and HTML from one Quarto source. |
| `references.bib` | Generated from `data/seed_bibliography.csv` — never hand-edited. |
| `data/seed_bibliography.csv` | The coded review database: every included record, its DOI, its H1–H7 classification, and the evidence basis for that classification. |
| `docs/01_SCOPE_AND_TAXONOMY.md` | The structural definition of hybridity and the H1–H7 taxonomy in full. |
| `docs/03_PAVE-ML_instrument.md` | The 24-item appraisal checklist and its coding rules. |
| `analysis/` | The full identification → screening → classification → figure/table-generation pipeline (see below). |
| `figures/`, `output/` | Generated figures and the built manuscript in all three formats. |

### The pipeline, in the order it runs

```
harvest_crossref.py  →  screen_corpus.py  →  add_batchN.py  →  classify_hybridity.py  →  make_bib.py  →  fig_*.py  →  quarto render
   (identify)             (structural          (verify &          (H1–H7 coding)        (bibliography)   (figures)     (manuscript)
                            pre-filter)          add records)
```

`analysis/harvest_crossref.py` runs a 261-query algorithmic search — optimiser names ×
learner names × legacy hybrid-labelled vocabulary, each crossed against a mandatory
pavement-terminology filter — against the Crossref API. `screen_corpus.py` applies a
structural (not lexical) proxy filter to the results. Records that pass are hand-verified
against the definition in `docs/01_SCOPE_AND_TAXONOMY.md` §2 before being added to the
database by an `add_batchN.py` script, each carrying a per-record note disclosing how deeply
it was verified (full-text, abstract-confirmed, search-confirmed, or title-level). See
`CLAUDE.md` for the full technical development record, including diagnostics for issues
found and fixed along the way.

### Building

```bash
quarto add quarto-journals/elsevier --no-prompt   # once
pip install jupyter matplotlib numpy requests pillow
python analysis/make_bib.py
cd figures && for f in ../analysis/fig_*.py; do python "$f"; done && cd ..
quarto render manuscript.qmd
```

Requires Quarto ≥ 1.5, Python ≥ 3.10, and a TeX distribution (`lmodern` must be available).

---

## Reproducibility and data availability

Every citation in the manuscript resolves against `references.bib`; every entry in
`references.bib` traces to a verified DOI in `data/seed_bibliography.csv`. A citation with no
corresponding database row fails the render rather than appearing as a plausible but
unverified reference — this is enforced structurally, not by convention. The full analysis
pipeline that produced every figure and table is included in this repository and runs from
the committed data with no external dependencies beyond the packages listed above.

During the preparation of this work, the authors used Claude (Anthropic) to assist with
literature identification and screening, database construction and verification, and
manuscript drafting; all output was reviewed and edited by the authors, who take full
responsibility for the content. See the manuscript's own Declaration of Generative AI
section for the disclosure as it appears in the submitted paper.

---

## Citation

A citation entry will be added once the manuscript is assigned a DOI. In the interim, please
cite the target venue and manuscript title above.
