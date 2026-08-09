#!/usr/bin/env python3
"""
fig_review_flow.py
====================
Figure 5: the review's identification/screening/inclusion process as it
actually stands on 2026-08-09 -- not a completed PRISMA 2020 flow diagram.

WHY THIS IS LABELLED "interim status", NOT "PRISMA flow diagram"
-------------------------------------------------------------------
A real PRISMA 2020 flow diagram reports final identification, screening and
exclusion counts for a COMPLETED review. This review's screening is not
complete: 138 structural candidates from the 2026-08-09 Crossref harvest are
still unreviewed (see analysis/screen_corpus.py's output,
data/corpus_screened.csv), and the raw pool itself (2,332 records) has only
had an automated structural PROXY filter applied, not full title/abstract
screening against the eligibility criteria in Sec2.3. Labelling this a PRISMA
diagram would overstate how far the identification/screening process has
actually gotten. What CAN be reported honestly, and is reported here, is the
real, counted state of the pipeline as it stands right now -- every number
below is read directly from data/corpus_raw.csv, data/corpus_screened.csv and
data/seed_bibliography.csv, none is estimated or projected forward.

Numbers (recompute and update if the corpus changes):
  261 queries -> 25,750 records returned (with duplication across queries)
  -> 2,332 unique, pavement-gated records (dedup + hard pavement-term gate)
  -> 25 already in the pre-existing database; 2,307 new
  -> 191 flagged as structural candidates by the automated proxy filter
     (screen_corpus.py); 2,116 did not match the proxy (may include missed
     true positives -- the proxy is a recall aid, not a ground truth)
  -> 53 hand-reviewed against the structural definition in Sec2.3 and added
     (batch 4: 44, batch 5: 9); 138 structural candidates remain unreviewed
  -> corpus as of this run: 147 total records (131 primary + 16 prior
     reviews), of which 93 primary studies are coded H1-H7, 27 `none`
     (fail the structural test), 11 `context` (kept for citation only)

Plus the pre-2026-08-09 manual-search phases that built the original 94-record
seed corpus, shown as a separate parallel input feeding the same final box.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

fig, ax = plt.subplots(figsize=(9, 11))
ax.set_xlim(0, 10)
ax.set_ylim(0, 15)
ax.axis("off")

BOX = dict(boxstyle="round,pad=0.35,rounding_size=0.12", linewidth=1.2)
COL_MANUAL = "#e8eef7"
COL_HARVEST = "#eaf3e8"
COL_MERGE = "#f7f0e3"
COL_FINAL = "#f2e6ea"
EDGE = "#444444"


def box(x, y, w, h, text, color, fontsize=9.2, weight="normal"):
    b = FancyBboxPatch((x - w / 2, y - h / 2), w, h, facecolor=color,
                        edgecolor=EDGE, **BOX)
    ax.add_patch(b)
    ax.text(x, y, text, ha="center", va="center", fontsize=fontsize,
             weight=weight, linespacing=1.35)
    return (x, y, w, h)


def arrow(b1, b2, label=None, label_dx=0.35):
    x1, y1, w1, h1 = b1
    x2, y2, w2, h2 = b2
    start = (x1, y1 - h1 / 2) if y1 > y2 else (x1, y1 + h1 / 2)
    end = (x2, y2 + h2 / 2) if y1 > y2 else (x2, y2 - h2 / 2)
    a = FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=14,
                         color=EDGE, linewidth=1.1, shrinkA=2, shrinkB=2)
    ax.add_patch(a)
    if label:
        midx, midy = (start[0] + end[0]) / 2, (start[1] + end[1]) / 2
        ax.text(midx + label_dx, midy, label, fontsize=8.2, color="#333333",
                 ha="left", va="center", style="italic")


# --- Left column: pre-2026 manual search phases (phases 1-13) ---
b_manual1 = box(2.4, 13.6, 4.2, 1.05,
                "Manual search, phases 1–13\n"
                "(pre-2026-08-09)\nOpenAlex / Scopus / WoS / Semantic\n"
                "Scholar connector, one query at a time",
                COL_MANUAL)
b_manual2 = box(2.4, 11.7, 4.2, 0.95,
                "94 records verified and\nhand-classified\n"
                "(the pre-existing seed corpus)",
                COL_MANUAL)
arrow(b_manual1, b_manual2)

# --- Right column: 2026-08-09 algorithmic harvest ---
b_h1 = box(7.3, 13.6, 4.4, 1.05,
           "analysis/harvest_crossref.py\n2026-08-09\n"
           "261 queries (optimiser × learner ×\n"
           "label vocabulary, Sec2.3)",
           COL_HARVEST)
b_h2 = box(7.3, 12.1, 4.4, 0.85,
           "25,750 records returned\n(with duplication across queries)",
           COL_HARVEST)
arrow(b_h1, b_h2)
b_h3 = box(7.3, 10.7, 4.4, 0.95,
           "2,332 unique, pavement-gated\nrecords (dedup + hard\npavement-term filter)",
           COL_HARVEST)
arrow(b_h2, b_h3)
b_h4 = box(7.3, 9.15, 4.4, 1.05,
           "2,307 new (25 already in the\nexisting database)\n→ 191 flagged as structural\ncandidates (automated proxy)",
           COL_HARVEST)
arrow(b_h3, b_h4)
b_h5 = box(7.3, 7.55, 4.4, 0.95,
           "53 hand-verified against Sec2.3\nand added (batch 4: 44, batch 5: 9)",
           COL_HARVEST, weight="bold")
arrow(b_h4, b_h5, label="138 structural candidates\nstill unreviewed →", label_dx=-4.7)

# --- Merge point ---
b_merge = box(4.85, 5.9, 7.2, 0.85,
              "Combined database: data/seed_bibliography.csv",
              COL_MERGE, weight="bold")
arrow(b_manual2, b_merge, label=None)
arrow(b_h5, b_merge, label=None)

# --- Final breakdown ---
b_final = box(4.85, 3.9, 8.0, 1.55,
              "147 records total\n"
              "131 primary studies + 16 prior reviews (§1)\n"
              "Of the primary studies: 93 coded H1–H7 (an actual\n"
              "structural hybrid), 27 `none` (fail the Sec2.3 test),\n"
              "11 `context` (kept for citation, outside the taxonomy)",
              COL_FINAL, weight="bold", fontsize=9.5)
arrow(b_merge, b_final)

b_target = box(4.85, 1.7, 6.4, 0.95,
               "Target: 150–500 records for a completed\nsystematic audit — not yet reached;\nscreening continues from the 138 candidates above",
               "#ffffff", fontsize=8.8)
arrow(b_final, b_target)

# dashed border around the whole diagram + status label
fig.text(0.5, 0.985,
          "Review process status — 2026-08-09 (interim, not a completed PRISMA 2020 flow diagram)",
          ha="center", fontsize=11.5, weight="bold")
fig.text(0.5, 0.965,
          "Every count is read directly from data/corpus_raw.csv, data/corpus_screened.csv and data/seed_bibliography.csv — none is projected or estimated.",
          ha="center", fontsize=8.3, style="italic", color="#333333")

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("fig05_review_flow.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.savefig("fig05_review_flow.pdf", bbox_inches="tight", facecolor="white")
print("wrote fig05_review_flow.png / .pdf")
