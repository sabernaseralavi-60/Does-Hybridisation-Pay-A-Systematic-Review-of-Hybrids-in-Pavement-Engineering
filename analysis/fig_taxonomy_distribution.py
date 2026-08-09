#!/usr/bin/env python3
"""
fig_taxonomy_distribution.py
=============================
Figure 2: distribution of hybridisation types (H1-H7) among the primary studies
coded so far, plus the non-hybrid and context categories that make up the rest
of the seed corpus.

IMPORTANT — what this figure is and is not:
This is drawn from the 55 primary studies hand-classified in the seed corpus
(data/seed_bibliography.csv), NOT from the completed systematic harvest, which
is still in progress via analysis/harvest_openalex.py. The manuscript must
present this as an illustrative distribution from the seed corpus, and replace
it with the full-corpus distribution once screening is complete. The caption
below states this explicitly and the same caption text must be used in the
manuscript to avoid overstating what has been coded.
"""

import csv
import collections
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
rows = list(csv.DictReader((ROOT / "data" / "seed_bibliography.csv").open(encoding="utf-8-sig")))
primary = [r for r in rows if r["hybrid_type"] != "review"]

LABELS = {
    "H1": "H1 — metaheuristic\n\u2192 hyperparameters",
    "H2": "H2 — metaheuristic\n\u2192 weights/structure",
    "H3": "H3 — physics +\ndata (PINN etc.)",
    "H4": "H4 — architecture\nfusion",
    "H5": "H5 — heterogeneous\nstacking",
    "H6": "H6 — decomposition\nthen learn",
    "H7": "H7 — symbolic\u2013numeric",
    "none": "Not hybrid under\nour definition",
    "context": "Context / landmark\n(not classified)",
}
ORDER = ["H1", "H2", "H3", "H4", "H5", "H6", "H7", "none", "context"]
counts = collections.Counter(r["hybrid_type"] for r in primary)
values = [counts.get(k, 0) for k in ORDER]
colors = ["#1f4e79"] * 7 + ["#b0b0b0", "#e0a458"]

fig, ax = plt.subplots(figsize=(13, 6))
bars = ax.bar(range(len(ORDER)), values, color=colors, edgecolor="white", width=0.62)
ax.set_xticks(range(len(ORDER)))
ax.set_xticklabels([LABELS[k].replace("\n", " ") for k in ORDER],
                    fontsize=9, rotation=20, ha="right")
ax.set_ylabel("Number of primary studies (seed corpus)")
for i, v in enumerate(values):
    if v:
        ax.text(i, v + 0.15, str(v), ha="center", fontsize=9.5, fontweight="bold")

ax.axvline(6.5, color="black", linewidth=0.8, linestyle=":")
top = max(values)
ax.set_ylim(0, top * 1.28)
ax.text(3, top * 1.10, "in scope (H1\u2013H7)", ha="center", fontsize=9,
        style="italic", color="#1f4e79")
ax.text(7.5, top * 1.10, "out of scope", ha="center", fontsize=9,
        style="italic", color="#666666")

for s in ["top", "right"]:
    ax.spines[s].set_visible(False)

ax.set_title("Hybridisation types among primary studies coded so far\n"
              "(seed corpus, n = %d; full-corpus harvest in progress)" % len(primary),
              fontsize=11.5, pad=14)

plt.tight_layout()
plt.savefig(ROOT / "figures" / "fig02_taxonomy_distribution.png", dpi=300,
            bbox_inches="tight", facecolor="white")
plt.savefig(ROOT / "figures" / "fig02_taxonomy_distribution.pdf",
            bbox_inches="tight", facecolor="white")
print("counts:", dict(counts))
print("wrote fig02_taxonomy_distribution.png / .pdf")
