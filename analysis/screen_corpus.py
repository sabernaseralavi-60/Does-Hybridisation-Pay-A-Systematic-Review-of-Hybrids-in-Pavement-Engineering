#!/usr/bin/env python3
"""
screen_corpus.py
=================
Automated FIRST-PASS PRISMA screening of data/corpus_raw.csv (the Crossref harvest)
against the STRUCTURAL definition of hybridity in docs/01_SCOPE_AND_TAXONOMY.md §2 —
"couples two or more components drawn from different methodological families, at
least one of which is a learned data-driven model."

This script does NOT decide final inclusion. It is a title/abstract-level triage that:
  1. drops records already present in data/seed_bibliography.csv (by DOI)
  2. drops records whose title+abstract never mentions any pavement-family term a
     second time beyond the query anchor itself would be redundant -- already gated
     at harvest time, kept here as a defensive re-check
  3. flags each remaining record with which structural families it plausibly touches:
       has_optimizer, has_learner, has_physics, has_decomposition, has_symbolic,
       has_stacking_signal, has_fusion_signal
  4. a record is a "structural_candidate" if it shows a genuine cross-family coupling
     signal (optimizer+learner, or one of the H3/H5/H6/H7-specific patterns) --- NOT
     just because it contains the word "hybrid" (that's the exact lexical trap this
     review's own search design exists to avoid, see docs/01_SCOPE_AND_TAXONOMY.md §1)

Every flag here is a proxy computed from title/abstract text alone. It is NOT a
substitute for reading the abstract before coding a record into the taxonomy, and
it is absolutely not a substitute for full-text verification before asserting any
specific finding about a paper (CLAUDE.md integrity rule #2). Treat the output
(corpus_screened.csv) as a ranked candidate list for human/AI title+abstract review,
not as a final included set.

USAGE
-----
    python screen_corpus.py
"""

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from harvest_openalex import OPTIMISERS, LEARNERS  # noqa: E402

ROOT = Path(__file__).parent.parent
RAW = ROOT / "data" / "corpus_raw.csv"
SEED = ROOT / "data" / "seed_bibliography.csv"
OUT = ROOT / "data" / "corpus_screened.csv"

# Sub-vocabularies for the H3/H5/H6/H7-specific structural signals that a plain
# optimizer+learner co-occurrence check would miss.
PHYSICS_TERMS = ["physics-informed", "physics informed", "mechanistic", "governing equation",
                  "constitutive model", "MEPDG", "loss term"]
DECOMPOSITION_TERMS = ["variational mode decomposition", "empirical mode decomposition",
                        "wavelet", "VMD", "EMD", "CEEMDAN", "signal decomposition",
                        "empirical wavelet"]
SYMBOLIC_TERMS = ["gene expression programming", "genetic programming", "symbolic regression",
                   "evolutionary polynomial regression", "multi-gene"]
STACKING_TERMS = ["stacking", "stacked ensemble", "blending", "meta-learner", "super learner",
                   "heterogeneous ensemble"]
FUSION_TERMS = ["two-stream", "fusion network", "multimodal", "cross-attention",
                 "CNN-transformer", "CNN-LSTM", "attention mechanism"]

OPT_RE = re.compile("|".join(re.escape(t) for t in OPTIMISERS), re.I)
LRN_RE = re.compile("|".join(re.escape(t) for t in LEARNERS), re.I)
PHYS_RE = re.compile("|".join(re.escape(t) for t in PHYSICS_TERMS), re.I)
DECOMP_RE = re.compile("|".join(re.escape(t) for t in DECOMPOSITION_TERMS), re.I)
SYMB_RE = re.compile("|".join(re.escape(t) for t in SYMBOLIC_TERMS), re.I)
STACK_RE = re.compile("|".join(re.escape(t) for t in STACKING_TERMS), re.I)
FUSION_RE = re.compile("|".join(re.escape(t) for t in FUSION_TERMS), re.I)


def norm_doi(doi: str) -> str:
    return (doi or "").strip().lower().replace("https://doi.org/", "")


def load_existing_dois() -> set:
    with open(SEED, encoding="utf-8-sig") as f:
        return {norm_doi(r["doi"]) for r in csv.DictReader(f)}


def main() -> None:
    if not RAW.exists():
        print(f"! {RAW} does not exist yet -- run the harvest first", file=sys.stderr)
        sys.exit(1)

    existing = load_existing_dois()
    with open(RAW, encoding="utf-8-sig") as f:
        raw_rows = list(csv.DictReader(f))

    out_rows = []
    n_dup = 0
    for r in raw_rows:
        doi = norm_doi(r.get("doi", ""))
        if doi and doi in existing:
            n_dup += 1
            continue
        blob = f"{r.get('title','')} {r.get('abstract','')}"
        has_opt = bool(OPT_RE.search(blob))
        has_lrn = bool(LRN_RE.search(blob))
        has_phys = bool(PHYS_RE.search(blob))
        has_decomp = bool(DECOMP_RE.search(blob))
        has_symb = bool(SYMB_RE.search(blob))
        has_stack = bool(STACK_RE.search(blob))
        has_fusion = bool(FUSION_RE.search(blob))
        structural_candidate = (
            (has_opt and has_lrn) or has_phys or has_decomp or has_symb
            or has_stack or has_fusion or (has_opt and has_symb)
        )
        row = dict(r)
        row["has_optimizer_term"] = has_opt
        row["has_learner_term"] = has_lrn
        row["has_physics_signal"] = has_phys
        row["has_decomposition_signal"] = has_decomp
        row["has_symbolic_signal"] = has_symb
        row["has_stacking_signal"] = has_stack
        row["has_fusion_signal"] = has_fusion
        row["structural_candidate"] = structural_candidate
        out_rows.append(row)

    out_rows.sort(key=lambda r: (not r["structural_candidate"],
                                  -(int(r["cited_by_count"]) if r["cited_by_count"] else 0)))

    fieldnames = list(out_rows[0].keys()) if out_rows else []
    with open(OUT, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(out_rows)

    n_cand = sum(1 for r in out_rows if r["structural_candidate"])
    print("--- screening summary ---")
    print(f"raw records                       : {len(raw_rows)}")
    print(f"already in seed_bibliography.csv  : {n_dup}")
    print(f"new, not yet in database          : {len(out_rows)}")
    print(f"  of which structural candidates  : {n_cand}")
    print(f"written to                        : {OUT}")


if __name__ == "__main__":
    main()
