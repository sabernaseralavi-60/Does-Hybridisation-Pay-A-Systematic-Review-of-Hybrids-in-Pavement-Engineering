# Project brief for Claude Code — read this first

You are picking up a Q1 review-paper project from a prior Claude session that ran in a
chat sandbox with **no direct internet access to academic APIs** (OpenAlex, Crossref,
Semantic Scholar all returned `403 host_not_allowed`). That session built this entire
repository — manuscript, database, figures, build pipeline — using a third-party
literature-search connector one query at a time, which was slow and is why the project
has moved to you. **You almost certainly have real internet access.** That changes what
"the next step" should look like — see "What actually changed" below before you do
anything else.

Read this file fully before touching anything. Then read `README.md` for the file-by-file
map. Then read `docs/01_SCOPE_AND_TAXONOMY.md` for the actual argument of the paper — it
is the single most important document for understanding *why* the review is shaped the
way it is, not just what's in it.

## What this project is

A systematic review titled **"Does Hybridisation Pay? A Systematic Review of
Metaheuristic Optimisation and Machine Learning Hybrids in Pavement Engineering
(2005–2026)"**, targeting *Automation in Construction* (Elsevier), written in Quarto
(`manuscript.qmd`) so it builds to PDF, Word, and HTML from one source. The authors are
Dr. Seyed Saber Naseralavi (Shahid Bahonar University of Kerman) and Dr. Ali Reza
Ghanizadeh (Sirjan University of Technology) — the human principals of this project, not
you or the prior Claude session.

**The paper's core claim:** the pavement-engineering literature routinely couples a
metaheuristic optimiser to a machine-learning base learner and reports the coupling as
its contribution ("hybrid model"), almost never comparing against the same base learner
properly tuned by conventional means under a comparable search budget. Where that fair
comparison exists in the literature (rare), the hybrid's advantage shrinks or disappears.
The review calls this the **hybridisation premium** and audits how often it's even
measurable. A companion finding, documented with unusual rigor, is that at least 8+
papers by one overlapping author team (Alnaqbi/Zeiada/Al-Khateeb) reuse the same ~33-
section LTPP substrate across single-target papers, and full-text verification of two of
them confirmed ungrouped, leakage-prone cross-validation.

## What actually changed — and what you should do differently

The prior session hand-searched and hand-verified everything through a connector because
it had no other option. **Before you replicate that pattern, check whether you can do
better:**

1. **Try the real harvest first.** `analysis/harvest_openalex.py` is a fully-written,
   documented, 261-query PRISMA search script against the OpenAlex API. It was never
   successfully run — only tested for syntax. If you have outbound internet access, run:
   ```bash
   pip install requests
   python analysis/harvest_openalex.py --email <a real email — OpenAlex politeness pool>
   ```
   This should return several thousand raw records in `corpus_raw.csv` in one run,
   which is the entire remaining "collect candidates" problem solved in one command
   instead of ~15 more manual chat rounds. If it works, your job shifts from *searching*
   to *screening and coding*, which is a completely different (and much faster) workflow.
   If OpenAlex rate-limits or blocks you too, fall back to whatever academic search
   access you do have (web search + fetch, a connected Scopus/WoS tool, etc.) — but try
   the real API first, because it is categorically faster than anything else available.

2. **If you have general web browsing** (which the prior session did have, just not for
   bulk API calls), you can fetch full text directly for verification — this worked
   repeatedly and is documented below under "Full-text verification protocol." Prefer
   this over re-deriving conclusions from abstracts.

## Non-negotiable integrity rules — read before writing anything

These aren't style preferences. They are why this review is trustworthy, and violating
them silently would be a serious failure, not a minor one.

1. **Every citation in `manuscript.qmd` must resolve against `references.bib`, and every
   row in `references.bib` is generated from `data/seed_bibliography.csv` by
   `analysis/make_bib.py` — never hand-edit `references.bib`.** Adding a citation means:
   verify the DOI is real (search or fetch it, don't recall it from training data) → add
   a row to the CSV with that DOI → re-run `make_bib.py` → cite the generated key. A
   citation key that doesn't exist in the bib fails the render loudly (undefined
   reference), which is the intended safety net — don't work around it by inventing a
   bib entry by hand.

2. **Never state a specific finding (an R², a sample size, a methods detail) about a
   paper you have not actually read the abstract or full text of.** The database has a
   `note` field precisely so every claim about a paper traces to something actually
   read. If you're not sure whether a detail is real, say so in the note ("full-text
   verification needed") rather than asserting it.

3. **Run the pre-flight citation check before every render** — it's cheap and catches
   mistakes before a 5-minute LaTeX build fails:
   ```bash
   python3 -c "
   import re
   qmd = open('manuscript.qmd', encoding='utf-8').read()
   cites = set(re.findall(r'@([A-Za-z][A-Za-z0-9]+)', qmd)) - {'fig','tbl','uk','sec'}
   bib = open('references.bib', encoding='utf-8').read()
   keys = set(re.findall(r'@article\{([^,]+),', bib))
   missing = cites - keys
   print('missing:', missing if missing else 'NONE')"
   ```

4. **`analysis/classify_hybridity.py` preserves hand-set `hybrid_type` values not yet in
   its `CLASSIFICATION` dict** (this was a real bug, fixed once already — don't
   reintroduce it). Still, the correct habit is: whenever you set `hybrid_type` by hand
   in the CSV, also add the same DOI → (type, reasoning) entry to `CLASSIFICATION` in
   that script, so the reasoning trail stays in one place and a future re-run can't
   silently diverge from what you intended.

5. **No raw LaTeX macros in `manuscript.qmd` prose** (`\textendash`, `\textrightarrow`,
   etc.) — they render fine in PDF but break HTML/Word silently. Use literal Unicode
   (–, →) instead. This was a real bug, fixed once already.

6. **Author names: verify, don't infer.** One correction was already needed this
   project (a first author's given-name/surname were transposed from a secondary
   source: "Wei, X." was actually "Xiao, W."). When a name looks uncertain, check the
   publisher page directly rather than trusting a citation aggregator's parsing.

## Current state (as of handoff)

- **90 records** in `data/seed_bibliography.csv`: 75 primary studies (all hand-classified
  against the H1–H7 taxonomy), 15 prior reviews used for positioning (§1).
- **H1–H7 distribution among classified primaries:** H1=20 (+1 joint H1;H4), H2=4, H3=1,
  H4=5, H5=2, H6=0 (confirmed absent after two independent search sweeps — a reported
  finding, not an oversight), H7=7; 24 coded `none` (not hybrid under the structural
  test), 11 coded `context` (kept for citation but outside the taxonomy).
- **Four records are full-text verified** (fetched and read in full, not just abstract):
  `10.1186/s44147-025-00706-9`, `10.1186/s44147-025-00623-x` (both confirm identical
  leakage mechanism — ungrouped 5-fold CV — in the Alnaqbi CRCP series), `10.3390/app132312862`
  (confirms a *different* leakage mechanism — pre-split Boruta feature selection),
  `10.3390/ma18122913` (confirms a genuine *positive* exemplar — leakage-safe stacking
  design, with an honest caveat that the same paper still lacks external validation).
  These four are the template for how the remaining ~70 should eventually be verified —
  see the protocol below.
- **All 14 manuscript sections have real, cited prose** — none are empty placeholders —
  but Sections 5–8 (domain deep-dives) and the bibliometric analysis (§3) are thin
  relative to what a finished 200-record corpus would support, and figures 2–3 are
  explicitly captioned as seed-corpus snapshots, not final bibliometric claims.
- **The abstract is deliberately still a placeholder.** Do not write it until the
  findings it would summarize are actually final — this is intentional, not an oversight.
- **Builds clean**: `quarto render manuscript.qmd` → 26-page PDF, DOCX, HTML, zero
  citation warnings, zero LaTeX errors, as of the last commit.

## Full-text verification protocol (the pattern that worked four times)

1. Web-search the exact title + a distinctive methods term (e.g. "cross-validation",
   "Boruta", author names) to find the publisher's landing page.
2. Fetch the landing page directly (Springer/MDPI open-access pages render full text
   in-page; this worked every time so far without needing a separate PDF fetch).
3. Read the **Methods** section for the actual partitioning procedure — don't rely on
   the abstract's description, which is often vague or silent on exactly this point.
4. Read the **Limitations / Future Work** section — authors surprisingly often self-admit
   the absence of external validation in their own words, which is stronger evidence
   than inferring it from silence.
5. Write what you found into the CSV `note` field with the DOI, a verbatim or
   near-verbatim quote of the load-bearing sentence, and an explicit
   `leakage_risk: HIGH (confirmed)` / `external_validation: NO (author-confirmed)` style
   tag so a future reader doesn't have to re-derive your reasoning.
6. Update `role_in_review` to flag it as full-text verified (grep the CSV for
   `"FULL-TEXT VERIFIED"` to see the existing four as examples of the phrasing).
7. If the finding changes what a manuscript section claims, update that section's prose
   too — don't let the database and the manuscript drift apart.

## Suggested priority order

1. **Try the real OpenAlex harvest** (see above). This is the highest-leverage single
   action available — it could turn ~15 rounds of manual searching into one run.
2. **Screen the harvest output** against the eligibility criteria in `manuscript.qmd`
   §2.3 / `docs/01_SCOPE_AND_TAXONOMY.md` §2 (structural hybridity test, not lexical).
   Target a final included corpus in the 150–250 range per the original brief.
3. **Classify each included study** against H1–H7 using `analysis/classify_hybridity.py`
   as the running record — extend `CLASSIFICATION`, don't hand-edit the CSV's
   `hybrid_type` column without also updating the script.
4. **Full-text verify a meaningful stratified sample** — not necessarily every record,
   but enough per domain/hybridisation-type to make Section 9's premium analysis and
   Section 7's leakage findings statistically meaningful rather than anecdotal. Twenty to
   thirty full verifications, chosen to span H1/H2/H7 and all six pavement domains, would
   be a defensible sample even short of full coverage.
5. **Only then** flesh out Sections 5–8 and rewrite §3's bibliometric figures from the
   completed corpus rather than the seed-corpus snapshot.
6. **Double-coding reliability** (§2's κ commitment) needs a second independent human
   coder — this is not something you can satisfy alone regardless of how much you read;
   flag it to the human authors as an open task for them specifically.
7. **Write the abstract last**, from the finished Sections 9 and 11.

## Build commands

```bash
quarto add quarto-journals/elsevier --no-prompt   # once, if not already present
pip install jupyter matplotlib numpy requests
python3 analysis/make_bib.py                      # regenerate references.bib from the CSV
cd figures && python3 ../analysis/fig_coverage_gap.py && python3 ../analysis/fig_taxonomy_distribution.py && python3 ../analysis/fig_year_trend.py && cd ..
quarto render manuscript.qmd                      # all three formats
quarto render manuscript.qmd --to elsevier-pdf     # PDF only, faster iteration
```

Needs a TeX distribution with `lmodern` available (`apt-get install lmodern
texlive-fonts-recommended` on Debian/Ubuntu if PDF rendering fails with a `lmodern.sty
not found` error — this happened once already in the sandbox environment and may or may
not reproduce on your machine).

## Git

The repo has 16 commits, each a real, documented increment — `git log --oneline` reads
as an audit trail of the project's actual progress and is worth preserving that way
going forward: commit at meaningful checkpoints with a message that says what changed
and why, not just "update files."

## Journal targeting — still provisional

Current target is *Automation in Construction* (Elsevier), chosen over publishing where
most primary-study sources are concentrated (MDPI journals) specifically because a
methodological rigour audit is better received by a venue with a thinner, more critical
reviewer pool than by the high-volume venues it is partly auditing. Revisit this once the
corpus is closer to final — see `README.md` "Journal targeting" section for the full
reasoning and alternatives.
