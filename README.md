# Does Hybridisation Pay?

A systematic review of metaheuristic optimisation and machine learning hybrids in pavement
engineering (2005–2026).

**Authors:** S. S. Naseralavi (Shahid Bahonar University of Kerman) · A. R. Ghanizadeh (Sirjan
University of Technology)
**Target journal:** *Automation in Construction* (Elsevier) — see [Journal targeting](#journal-targeting)
**Status:** manuscript renders clean to PDF/Word/HTML (32 pages). All 14 sections now have
real, cited content — including Section 10 (Interpretability), which an external review
caught as a silently-empty placeholder despite being cross-referenced 13 times elsewhere
under the wrong section number; both the content and every cross-reference are now fixed.
The full 24-item PAVE-ML checklist is reproduced as a table in the main text (not just
described), and Figure 4 now shows the leakage mechanism (random vs. section-grouped
cross-validation) as a concrete diagram rather than only prose. Database: 90 records, 75
classified primary studies. See `CLAUDE.md` for the full external-review tracking and the
project handoff for continuing in Claude Code / Cowork. What remains: expanding the corpus from 90
to the 300–500
records a full systematic review of this kind needs, full-text coding (vs. abstract-level) of
every PAVE-ML field, the double-coding reliability pass, and the abstract (deliberately still a
placeholder — it should not be written before the findings it summarises exist).

---

## What's left before this is submittable

Being direct about this, since it matters more than any file listing below:

- **Corpus size.** 90 verified records is a solid seed, not a completed systematic review.
  A defensible Q1 review in this space needs several hundred screened records. The bottleneck
  is literature-search-connector throughput (~10–20 records per targeted query), not analysis
  time — expanding this is mechanical repetition of what `add_batch2.py` / `add_batch3.py`
  already demonstrate, across more queries.
- **Full-text coding.** Almost every PAVE-ML field (leakage risk, external validation, baseline
  strength, etc.) is still coded from abstracts, but this is now demonstrated to be tractable,
  not just designed-for: five records were fetched and read in full. Two (`10.1186/s44147-025-00706-9`
  and `10.1186/s44147-025-00623-x`, the first two papers in the Alnaqbi same-substrate series
  discussed in Section 7) independently confirmed the identical leakage mechanism — an ungrouped
  5-fold split at the observation level, plus a self-admitted absence of external validation in
  each paper's own Limitations/Future Directions section. The third (`10.3390/app132312862`,
  Xiao et al.'s TPE-CatBoost faulting model) confirmed a **structurally different** leakage
  mechanism on an unrelated substrate: Boruta feature selection performed on the full dataset
  in the paper's own "Data Preparation" section, before the train/test split appears in "Model
  Construction" — and the paper's own conclusion attributes part of its headline accuracy gain
  directly to that contaminated step. The fourth (`10.3390/ma18122913`, Huang et al.'s stacking
  ensemble) is a balancing case: full-text confirmed as a genuine **positive** exemplar, with
  a leakage-safe stacking design stated explicitly in its own methods section rather than
  inferred from the abstract — while also honestly coding `external_validation: no` on the same
  paper, since a study can get one PAVE-ML dimension right while another stays open. The fifth
  (`10.1038/s41598-024-81311-3`, Duan's BKA-XGBoost model) is the most nuanced case yet: confirms
  a genuine repeated-run reliability check (10 dataset reassemblies, matching PAVE-ML item 12c)
  and an author-acknowledged cross-study comparability caveat, alongside an unconfirmed comparator
  tuning budget and no mechanistic baseline — a single paper landing on both sides of the ledger.
  One verification attempt (`10.1016/j.sandf.2020.02.010`, Ghorbani's GA-vs-ANN-GA comparison)
  failed outright — ScienceDirect blocks automated fetching — and is recorded as a failed attempt
  in the CSV rather than left ambiguous, so it isn't silently re-attempted the same way. Five
  confirmations, two risk mechanisms, one verified positive case, one nuanced mixed case, one
  honestly-recorded failure is the current full-text
  record. The first verification also surfaced a second overlapping-author cluster
  (Wang/Xiao/Liu) publishing on a related substrate, found only by following the first paper's
  own reference list. Scaling this from 5 records to the ~60 that need it is the
  highest-value remaining task, and the method is now proven five times over, not
  hypothetical.
- **Double-coding reliability.** Section 2 commits to an independent 15% double-coded sample
  with Cohen's κ reported per field. This requires a second coder — a role this assistant
  cannot fill on its own, since the entire point of double-coding is a second, independent
  judgement.
- **The abstract.** Deliberately still a placeholder. Writing it now, before the audit that
  it summarises is complete, would mean writing conclusions before the evidence for them
  exists.

All fourteen numbered sections currently have real, cited, grounded prose — not
placeholders — and are a reasonable draft of the paper's argument and structure. The domain
sections (5–8) are thinner than the final version will be once the corpus is larger, but each
is now anchored on at least one concrete, verifiable finding rather than general description.
Everything below this point in the README is unchanged in spirit from before: you do
not need to run anything.

Everything in `analysis/` runs on the drafting side and its outputs are committed to this
repository. The scripts are here because reviewers and journals increasingly ask for the
pipeline behind a systematic review, and because a review whose own analysis is not reproducible
would be a poor advertisement for a paper about methodological rigour.

The one thing that needs you is pushing to GitHub, which needs your credentials
(see [Publishing this repository](#publishing-this-repository)).

---

## What each file is, and what it is for

### The manuscript

| Path | What it is |
|---|---|
| `manuscript.qmd` | **The paper.** Single source for all three output formats. Sections marked `PLACEHOLDER` are not yet written. |
| `_quarto.yml` | Build configuration. Changing the target journal is a one-line change here. |
| `references.bib` | **Generated — never edit by hand.** Produced from `data/seed_bibliography.csv`. |
| `assets/manuscript-reference.docx` | Word styling template for the `.docx` output. |
| `output/manuscript.pdf` · `.docx` · `.html` | Built outputs. Regenerated by `make render`. |

### The evidence base

| Path | What it is |
|---|---|
| `data/seed_bibliography.csv` | **The database everything else derives from.** 90 verified records (75 primary studies, 15 prior reviews) so far, every row hand-classified against the H1–H7 taxonomy; every row carries a live DOI. Grows as the harvest proceeds. |
| `docs/00_MANUSCRIPT_ARCHITECTURE.md` | Original positioning analysis and journal shortlist. Partly superseded by `01`. |
| `docs/01_SCOPE_AND_TAXONOMY.md` | **Current scope document.** Structural definition of hybridity, the H1–H7 taxonomy, the hybridisation-premium metric, section plan. Read this one first. |
| `docs/02_MANUSCRIPT_S2_methodology.md` | Full draft of Section 2, transferred into `manuscript.qmd` piece by piece. |
| `docs/03_PAVE-ML_instrument.md` | The 24-item appraisal checklist and the operational coding rules for the audit. |
| `docs/table_premium_evidence.md` | Generated — source data for the Section 9 evidence table; regenerate via `analysis/table_premium_evidence.py`, don't hand-edit. |

### The pipeline

| Path | What it does | Runs where |
|---|---|---|
| `analysis/make_bib.py` | Regenerates `references.bib` from the CSV. | drafting side |
| `analysis/build_seed_db.py` · `add_batch2.py` · `add_batch3.py` | Build and extend the verified database, in the order they were run. | drafting side |
| `analysis/classify_hybridity.py` | Hand-verified H1–H7 classification of every primary study (not a keyword guess — checked against the structural definition in `docs/01_SCOPE_AND_TAXONOMY.md` §2). Re-run after adding records. | drafting side |
| `analysis/fig_coverage_gap.py` | Produces Figure 1 (review-landscape coverage matrix). | drafting side |
| `analysis/fig_taxonomy_distribution.py` | Produces Figure 2 (H1–H7 distribution in the seed corpus). | drafting side |
| `analysis/table_premium_evidence.py` | Produces the within-corpus hybridisation-premium evidence table (Section 9) — every figure copied verbatim from source papers, nothing estimated. | drafting side |
| `analysis/harvest_openalex.py` | **Reproducibility artifact for supplementary material.** The full 261-query PRISMA search, documented so a third party can re-execute the identification stage. It is not part of the drafting workflow — this environment's network cannot reach api.openalex.org directly (`403 host_not_allowed`); the actual corpus is being built via a literature-search connector instead. | third-party replication |

---

## The guard against fabricated references

The manuscript may only cite keys present in `references.bib`, and `references.bib` is generated
from the CSV, where every row carries a DOI verified against OpenAlex or Semantic Scholar. A
citation key that is not in the database produces an undefined-reference warning at render time
rather than a plausible-looking entry in the reference list.

Adding a reference therefore means: verify the DOI → add the row to the CSV → re-run
`make_bib.py`. There is no other route in.

---

## Building

```bash
make render        # all three formats
make pdf           # Elsevier PDF only
make bib           # regenerate references.bib from the CSV
make figures       # regenerate all figures
make clean
```

Requires Quarto ≥ 1.5, Python ≥ 3.10, a TeX installation with `lmodern`, and
`pip install jupyter matplotlib numpy`. Install the Elsevier template once with
`quarto add quarto-journals/elsevier`.

---

## Journal targeting

Venue distribution of the 48 primary studies in the database so far:

| Publisher | Count |
|---|---|
| MDPI (Infrastructures, Applied Sciences, Materials, Sensors, Sustainability, AI) | 16 |
| Springer Nature (mostly *Scientific Reports*) | 5 |
| Wiley (*Computer-Aided Civil and Infrastructure Engineering*) | 4 |
| Elsevier | 2 |
| Various | 21 |

"Publish where the sources are" is a reasonable tiebreaker, but it should not decide this case,
for a specific reason: this paper audits the methodological conventions of a literature that is
heavily concentrated in fast-turnaround, high-volume venues. Submitting the audit to one of those
venues invites the obvious objection, and the reviewer pool for a methodological appraisal is
thinner there. The MDPI concentration is best used a different way — it tells us who the
*audience* is, which shapes how the paper is written, not where it is sent.

The current target is **Automation in Construction** (Elsevier; 2-year mean citedness 11.9,
h-index 240), which publishes critical reviews that deliver a usable instrument. Retargeting to
any other Elsevier title — *Construction and Building Materials*, *Transportation Geotechnics*,
*Journal of Road Engineering*, or *Transportation Research Part C: Emerging Technologies* — is a
one-line change in `_quarto.yml`, because they share the `elsarticle` class. **Computer-Aided
Civil and Infrastructure Engineering** (Wiley, IF ~9.6) is the strongest non-Elsevier alternative
specifically for AI-in-infrastructure methodology papers, but needs a different Quarto extension.

**This decision should be revisited once the harvest is complete** and the venue distribution
rests on 400+ records rather than 48.

---

## Publishing this repository

The repository is complete and committed locally. Pushing needs your GitHub credentials, which
are yours alone:

```bash
gh repo create pavement-hybrid-review --private --source=. --push
# or, without the GitHub CLI:
git remote add origin https://github.com/<your-username>/pavement-hybrid-review.git
git branch -M main && git push -u origin main
```

Keep it private until submission; make it public at acceptance and put the URL in the
Data Availability statement, which currently reads `[REPOSITORY URL]`.

---

## Integrity notes

- **Similarity.** Prose is written from the quantitative record of each study in the database,
  not from its sentences. Technical terms, standard designations and architecture names stay
  verbatim; altering them would be a scientific error.
- **Generative AI.** Elsevier, Springer Nature, Wiley, Taylor & Francis and COPE all require
  disclosure of generative-AI assistance in manuscript preparation. Disclosed use is permitted
  and routine. The manuscript carries a placeholder Declaration section to be completed in the
  journal's own wording before submission.
- **Self-citation.** With a 250–350-item reference list, 18–30 citations to the author team's own
  work is the defensible ceiling. The database currently holds 8 such records.
