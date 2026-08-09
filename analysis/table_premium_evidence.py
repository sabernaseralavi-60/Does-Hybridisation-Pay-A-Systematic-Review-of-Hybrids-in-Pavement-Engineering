#!/usr/bin/env python3
"""
table_premium_evidence.py
==========================
Builds the illustrative hybridisation-premium evidence table (Table X, Section 9)
from within-paper comparisons already present in the seed corpus — cases where a
single paper reports BOTH a hybrid/optimised variant AND a same-data, same-metric
comparator, so a premium is directly readable from the published numbers without
any re-analysis on our part.

This is NOT the full systematic premium audit (that needs the completed harvest
and full-text coding per PAVE-ML items 12a-12d). It is the evidence already in
hand, and it is what Section 9 opens with.

Every number below is copied from the abstract/reported results of the cited
paper — nothing is computed or estimated by us. Source DOI is given for each row
so every figure is checkable against references.bib.
"""

import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (doi, comparison, metric, comparator_value, hybrid_value, premium, note)
ROWS = [
    ("10.3390/app9153172",
     "Plain SVM vs. GA-ANFIS vs. PSO-ANFIS, all reported within one paper, 1000-run Monte Carlo",
     "RMSE / MAE / R (Marshall Stability)",
     "plain SVM (best of three by converged statistical criteria)",
     "GA-ANFIS and PSO-ANFIS (both hybrids)",
     "negative — plain SVM outperforms both hybrids",
     "Rare in this literature: a statistically robust (1000-simulation Monte Carlo) same-paper comparison where a plain, non-hybrid learner beats two separate metaheuristic-hybrid variants. Directly supports the review's central claim rather than merely gesturing at a missing baseline."),
    ("10.1038/s41598-022-17429-z",
     "LSSVM (best single-kernel setting reported) vs. best of 6 swarm-optimised LSSVM variants",
     "R2 / RMSE (MPa)",
     "not reported as a standalone tuned baseline",
     "0.942 / 6.72 (best of six, SOS)",
     "not computable — no tuned non-hybrid baseline reported",
     "The paper compares six hybrids to each other, never to a conventionally tuned LSSVM. This is the missing-baseline pattern Section 9 quantifies."),
    ("10.28991/cej-2025-011-01-06",
     "Eight individually-tuned learners (ANN, RNN, CNN among them) vs. Witczak/Hirsch mechanistic baselines",
     "R2 (dynamic modulus)",
     "Witczak 1-40D / Hirsch (mechanistic)",
     "bagging ensemble, individually tuned (highest of eight)",
     "positive but modest — mechanistic models remain competitive; deep architectures do NOT win",
     "The field's clearest example of tuning parity: every learner gets its own search budget, and the winner is a tuned ensemble tree, not a hybrid or a deep net."),
    ("10.1016/j.sandf.2020.02.010",
     "GA-fitted symbolic equation (H7-adjacent) vs. ANN-GA (GA on ANN weights, H2)",
     "R2 (resilient modulus)",
     "GA-only symbolic model",
     "ANN-GA hybrid",
     "ANN-GA reported higher R2, but adds a black-box layer over an already-competitive symbolic model",
     "Rare true head-to-head between two hybrid types on identical data — flagged for full-text extraction of exact R2 values."),
    ("10.3390/app9163221",
     "PSO-ANN vs. PSO-ELM vs. kernel-ELM, all reported within one paper",
     "RMSE / R2",
     "PSO-ANN (same optimiser, different base learner)",
     "PSO-ELM (best reported)",
     "small, same-optimiser architecture comparison — isolates base-learner choice, not optimiser value",
     "Useful for a different question than the premium: it holds the optimiser constant and varies the learner, the mirror image of what Section 9 needs."),
    ("10.3390/ma18122913",
     "Single ML models (KNN, Bayesian ridge, decision tree) vs. stacking ensemble",
     "R2 (G* and phase angle)",
     "best single model",
     "stacking (R2 = 0.973 / 0.999)",
     "positive, and the ONLY row in this table where leakage is explicitly controlled by design",
     "Cross-validated meta-features stated as a deliberate leakage-avoidance choice — the paper we cite as the positive PAVE-ML exemplar."),
]


def main() -> None:
    out = ROOT / "docs" / "table_premium_evidence.md"
    lines = [
        "# Table — within-corpus evidence for the hybridisation premium (illustrative)\n",
        "*Every figure below is copied verbatim from the source paper's own reported*",
        "*results; nothing is computed or estimated. This is the evidence already*",
        "*in hand from the seed corpus, not the completed systematic premium audit*",
        "*(PAVE-ML items 12a-12d), which requires the full harvest and full-text coding.*\n",
        "| Source | Comparison | Metric | Non-hybrid value | Hybrid value | Premium | Note |",
        "|---|---|---|---|---|---|---|",
    ]
    for doi, comp, metric, base, hyb, prem, note in ROWS:
        lines.append(f"| `{doi}` | {comp} | {metric} | {base} | {hyb} | {prem} | {note} |")
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out.relative_to(ROOT)} with {len(ROWS)} rows")


if __name__ == "__main__":
    main()
