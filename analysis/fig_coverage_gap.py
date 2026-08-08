#!/usr/bin/env python3
"""
fig_coverage_gap.py  (v2 — Phase 2)
===================================
Figure 1: coverage of the prior review literature, and the band left open.

v2 adds four reviews found in the second search sweep and RE-SCORES the matrix
honestly. Two of them — Tamagusko & Ferreira (2023) and M'harzi Alaoui et al.
(2026) — reach into territory the v1 figure showed as empty. Scoring them
generously to ourselves would be the first thing a reviewer caught, so they are
scored on what they actually do:

  * Tamagusko & Ferreira (2023) quantify input-variable prevalence across IRI
    studies and name standardisation, interpretability and replicability as open
    problems. That is partial coverage of comparability and of the audit idea,
    restricted to IRI on flexible pavements.
  * M'harzi Alaoui et al. (2026) name the lab-to-field gap and the
    "interpretability paradox" across 180 soil-stabilisation studies. Same
    diagnosis as our Section 11, in one sub-domain, without a per-study rubric.

The differentiation therefore is NOT "nobody has noticed the problem". It is:
whole-of-pavement scope, a per-study coding rubric applied consistently, the
audit reported as quantified findings, and a released instrument (PAVE-ML).
That is a defensible claim; "we are first to notice" is not.

Scoring: 2 = substantive dedicated treatment, 1 = touched in passing, 0 = absent.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

REVIEWS = [
    ("Gopalakrishnan", 2018), ("Cao et al.", 2020), ("Hou et al.", 2020),
    ("Abambres &\nFerreira", 2020), ("Yang et al.", 2021), ("Rasol et al.", 2022),
    ("Tamagusko &\nFerreira", 2023), ("Cavalli et al.", 2023),
    ("Safyari et al.", 2024), ("Yuan et al.", 2024),
    ("Zagvozda et al.", 2026), ("Hariri Asli\net al.", 2026),
    ("M'harzi Alaoui\net al.", 2026), ("THIS REVIEW", None),
]

TOPICS = [
    "Material & mix property modelling",
    "Structural response & inverse analysis",
    "Surface distress detection (vision)",
    "Performance / deterioration prediction",
    "Network-level M&R and PMS decisions",
    "Hybrid metaheuristic-optimised learners",
    "Explainable AI (SHAP / PDP / symbolic)",
    "Uncertainty quantification",
    "Physics-informed & mechanics-constrained",
    "Transformers / foundation models / GNN",
    "Benchmark & split-protocol comparability",
    "Per-study leakage & external-validation audit",
    "Deployment into agency workflow",
    "Reporting checklist / appraisal instrument",
]

#     Gop Cao Hou Aba Yan Ras Tam Cav Saf Yua Zag Har Alo | OURS
M = np.array([
    [0,  0,  1,  2,  2,  0,  0,  2,  0,  0,  0,  0,  2,    2],
    [0,  0,  2,  2,  2,  2,  0,  2,  0,  0,  0,  0,  0,    2],
    [2,  2,  2,  1,  2,  1,  0,  1,  2,  2,  2,  0,  0,    2],
    [0,  0,  1,  1,  2,  0,  2,  1,  0,  0,  0,  2,  0,    2],
    [0,  0,  0,  1,  1,  0,  1,  1,  0,  0,  0,  0,  0,    2],
    [0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  1,  1,    2],
    [0,  0,  0,  0,  0,  0,  1,  0,  0,  0,  0,  1,  2,    2],
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,    2],
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,    2],
    [0,  0,  0,  0,  0,  0,  0,  0,  1,  1,  1,  0,  0,    2],
    [1,  1,  0,  0,  0,  0,  1,  0,  1,  1,  1,  1,  1,    2],
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  1,    2],
    [0,  0,  0,  0,  1,  0,  0,  1,  0,  0,  0,  0,  1,    2],
    [0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,  0,    2],
])

assert M.shape == (len(TOPICS), len(REVIEWS)), M.shape

labels = [f"{n}\n{y}" if y else f"{n}\n(proposed)" for n, y in REVIEWS]
cmap = ListedColormap(["#f2f2f2", "#9ec6e0", "#1f4e79"])

fig, ax = plt.subplots(figsize=(13.5, 7.0))
ax.imshow(M, cmap=cmap, vmin=0, vmax=2, aspect="auto")

ax.set_xticks(np.arange(len(REVIEWS)))
ax.set_xticklabels(labels, fontsize=7.6)
ax.set_yticks(np.arange(len(TOPICS)))
ax.set_yticklabels(TOPICS, fontsize=9)

ax.add_patch(plt.Rectangle((len(REVIEWS) - 1.5, -0.5), 1.0, len(TOPICS),
                           fill=False, edgecolor="#c00000", linewidth=2.2, zorder=3))

ax.set_xticks(np.arange(-0.5, len(REVIEWS), 1), minor=True)
ax.set_yticks(np.arange(-0.5, len(TOPICS), 1), minor=True)
ax.grid(which="minor", color="white", linewidth=1.5)
ax.tick_params(which="minor", length=0)
for s in ax.spines.values():
    s.set_visible(False)

handles = [plt.Rectangle((0, 0), 1, 1, color=c) for c in cmap.colors]
ax.legend(handles, ["not covered", "touched in passing", "substantive treatment"],
          loc="upper center", bbox_to_anchor=(0.5, -0.16), ncol=3,
          frameon=False, fontsize=9)

ax.set_title("Coverage of the prior review literature on AI methods in pavement engineering",
             fontsize=12, pad=12)

plt.tight_layout()
plt.savefig("fig01_coverage_gap.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.savefig("fig01_coverage_gap.pdf", bbox_inches="tight", facecolor="white")

prior = M[:, :-1]
zero = [TOPICS[i] for i in range(len(TOPICS)) if prior[i].max() == 0]
partial = [TOPICS[i] for i in range(len(TOPICS)) if prior[i].max() == 1]
print("Zero prior coverage:")
for t in zero:
    print("  -", t)
print("\nPartial only (max = 'touched in passing'):")
for t in partial:
    print("  -", t)
print(f"\nmean prior coverage score = {prior.mean():.2f} / 2.00")
print("wrote fig01_coverage_gap.png / .pdf")
