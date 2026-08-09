#!/usr/bin/env python3
"""
fig_year_trend.py
==================
Figure 3: publication-year distribution of the seed corpus's primary (hybrid-type-
coded, non-review) studies.

Same honesty constraint as fig_taxonomy_distribution.py: this is a seed-corpus
snapshot assembled through targeted searches during protocol and taxonomy
development, not a random or exhaustive sample of the literature. A seed corpus
built by targeted search is expected to skew toward whatever years those targeted
queries happened to surface, and does NOT support a claim about the field's true
publication trajectory. The manuscript caption must say so; this docstring is the
reminder for whoever (human or model) regenerates this figure later not to quietly
drop that caveat once real bibliometric data (from the completed harvest) exists to
replace it.
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

years = [int(r["year"]) for r in primary if r["year"]]
counts = collections.Counter(years)
y_min, y_max = min(years), max(years)
all_years = list(range(y_min, y_max + 1))
values = [counts.get(y, 0) for y in all_years]

fig, ax = plt.subplots(figsize=(11, 4.8))
colors = ["#1f4e79" if y >= 2020 else "#9ec6e0" for y in all_years]
ax.bar(all_years, values, color=colors, width=0.7)
ax.set_xticks(all_years)
ax.set_xticklabels(all_years, rotation=45, ha="right", fontsize=8.5)
ax.set_ylabel("Primary studies in seed corpus")
for x, v in zip(all_years, values):
    if v:
        ax.text(x, v + 0.1, str(v), ha="center", fontsize=8.5)

for s in ["top", "right"]:
    ax.spines[s].set_visible(False)

ax.set_title("Publication years of primary studies in the seed corpus (n = %d)\n"
              "Seed corpus from targeted search during protocol development —\n"
              "NOT a claim about the field's true publication trajectory"
              % len(primary), fontsize=10.5, pad=10)

plt.tight_layout()
plt.savefig(ROOT / "figures" / "fig03_seed_corpus_years.png", dpi=300,
            bbox_inches="tight", facecolor="white")
plt.savefig(ROOT / "figures" / "fig03_seed_corpus_years.pdf",
            bbox_inches="tight", facecolor="white")
print("year distribution:", dict(sorted(counts.items())))
print(f"median year: {sorted(years)[len(years)//2]}")
print(f"share 2023+: {sum(1 for y in years if y>=2023)/len(years):.0%}")
print("wrote fig03_seed_corpus_years.png / .pdf")
