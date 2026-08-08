# Section 2 — Review methodology

*Manuscript draft, Phase 2. Target length 1,200 words; current draft ≈ 1,240.
English as it will appear in submission. Numbers marked `[N]` are placeholders to be
replaced by the figures the harvest actually produces — none of them is invented here.*

---

## 2.1 Scope and framing question

This review is organised around a question that differs from the one earlier surveys asked. Where
Yang et al. [ref] catalogued *where* neural networks had been applied across the pavement
lifecycle, and where subsequent surveys refined that catalogue for particular distresses or
indices [refs], we ask a narrower and, we think, more urgent question: **how much of the
performance this literature reports would survive an independent test?**

The distinction matters because the two questions have different answers. A field can grow
rapidly, converge on impressive metrics, and still be accumulating results that do not transfer —
and pavement engineering has structural features that make this failure mode unusually easy to
fall into. Datasets are small relative to the number of candidate predictors. Records are rarely
independent: repeated measurements come from the same specimen, the same section, the same
kilometre of road. A single public database, the Long-Term Pavement Performance programme, sits
underneath a large share of the tabular literature, so that apparent replication across papers
is sometimes re-analysis of overlapping data. And the vision literature evaluates on benchmarks
whose partitions and annotation conventions differ from one another, which makes the reported
gains difficult to compare even in principle.

None of this is hidden. Several recent reviews name pieces of it — Tamagusko and Ferreira [ref]
identify standardisation, interpretability and replicability as open problems in roughness
prediction; M'harzi Alaoui et al. [ref] describe a lab-to-field gap and an "interpretability
paradox" in soil-stabilisation modelling. What has not been done is to convert these observations
into per-study evidence. That conversion is the contribution of this review, and this section
describes how it was carried out.

## 2.2 Protocol and reporting

The review follows PRISMA 2020 for identification, screening and reporting [ref]. The protocol —
search strings, inclusion criteria, coding rubric and reliability procedure — was fixed before
screening began and is provided in full as supplementary material, together with the coded
database. We did not register the protocol on PROSPERO, which does not accept engineering
reviews; the frozen protocol document serves the equivalent function and carries a version date.

Two features of the protocol depart from common practice in engineering reviews and should be
stated plainly at the outset. First, coding treats **silence as absence**: where a study does not
report that a procedure was followed, it is coded as not followed, rather than as unclear. This
is the convention adopted in clinical-prediction appraisal [refs] and it is the only one that
cannot be accused of charitable reading. It will understate compliance in cases where authors
did the right thing without saying so, and we return to that bias in §11.4. Second, the coding
rubric was frozen before the full-text pass and every subsequent amendment was logged and applied
retrospectively.

## 2.3 Information sources and search

Records were identified from OpenAlex, Scopus, Web of Science Core Collection and Semantic
Scholar, with backward and forward snowballing from the [N] prior reviews in this domain. The
window is 1 January 2005 to 30 June 2026, giving the two decades over which neural methods moved
from occasional to routine in this field. A small set of earlier landmark studies is retained for
the historical account in §3 but excluded from the audit, since appraising 1990s work against
2020s reporting norms would be neither fair nor informative.

The search combines three term blocks — method, domain and task — applied to title, abstract and
keywords. Rather than issuing a single Boolean expression, we ran each method-by-domain pair as a
separate query and recorded its yield, which preserves recall on terms that behave differently
across databases and gives a per-query audit trail. The complete term list and per-query yields
appear in Table 1; the harvesting script is released with the supplementary material so that the
identification stage can be re-executed.

## 2.4 Eligibility

Studies were included when they trained or evaluated at least one neural or deep architecture on
a pavement-engineering task and reported quantitative performance. Peer-reviewed journal articles
and full conference papers were eligible; abstracts, posters and theses were not. Preprints were
excluded unless a peer-reviewed version was traced, and the [N] retained as grey literature are
flagged as such wherever cited.

Three exclusions deserve comment because they shaped the corpus. Studies using non-neural machine
learning without a neural comparator were held in a separate context set rather than the main
corpus; they inform the discussion in §4 and §8 — particularly the recurring finding that
gradient-boosted ensembles outperform neural architectures on small tabular pavement data — but
they are not audited, since the audit is framed around neural methods. Studies where pavement
enters only as an exogenous input, such as vehicle-dynamics work using roughness as a forcing
term, were excluded. And where the same team reported the same model on the same dataset in more
than one venue, the fullest report was retained and the others recorded as duplicates, since
counting them separately would inflate both the corpus and any conclusion drawn from it.

## 2.5 Screening and selection

Identification returned [N] records, reduced to [N] after deduplication. Title and abstract
screening removed [N], leaving [N] for full-text assessment, of which [N] met all criteria. The
flow is given in Figure 1.

Of the included studies, [N] were carried forward to full rigour coding. These were selected to
span the six pavement domains, the full period, and the range of citation impact — deliberately
including highly cited work, since a methodological weakness in a paper cited three hundred times
propagates further than the same weakness in one cited three times.

## 2.6 Data extraction and appraisal

Each fully coded study yields a record with [24] fields covering bibliographic detail, pavement
domain, data provenance, architecture, optimisation, partitioning, validation, interpretation,
metrics and deployment evidence. The appraisal fields — leakage risk, external validation,
baseline strength, hyperparameter reporting, uncertainty quantification and deployment level —
are governed by explicit decision rules with worked examples, reproduced in the supplementary
material.

Two constructs carry most of the analytical weight and are defined restrictively. **External
validation** requires evaluation on data from a different source: a different agency, region,
laboratory, test track or acquisition campaign. A random hold-out from a single pool, however
large and however described in the source paper, does not qualify. **Baseline strength** is rated
strong only where the study compares against both a tuned conventional learner and the
established domain model for the target, where one exists — the Witczak or Hirsch relationships
for dynamic modulus, the MEPDG transfer functions for roughness, rutting and faulting,
layered-elastic solutions for structural response. Comparisons drawn from other papers' published
numbers on different data are rated weak, since they establish nothing about the study at hand.

## 2.7 Reliability

A random 15% of coded studies (n = [N]) was independently coded by two reviewers. Cohen's κ is
reported field by field in Table [N]. Fields falling below κ = 0.60 had their decision rule
rewritten and were recoded in full rather than reported with a caveat. Remaining disagreements
were resolved by discussion, with a third reader breaking ties.

## 2.8 Limitations of the method

Four limitations bound what follows. The audit assesses *reporting*, and reporting is an
imperfect proxy for conduct; some studies coded as non-compliant will have followed sound
practice silently, and §11.4 estimates the size of this bias from the subset where authors
responded to correspondence. English-language restriction excludes a Chinese-language literature
that is substantial in this field. Coding of a study's *substance* — whether an architecture
suits its task, whether an attribution is mechanically plausible — is expert judgement and cannot
be made fully mechanical, though the double-coded subsample bounds the disagreement. Finally,
appraisal criteria that are conventional in 2026 were not conventional in 2008, so temporal trends
in the audit partly track changing norms rather than changing quality; we therefore report all
audit results stratified by period, and read levels only within periods.
