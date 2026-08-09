#!/usr/bin/env python3
"""
fig_review_flow.py
====================
Figure 5: the review's identification/screening/inclusion process, styled after
the PRISMA 2020 flow-diagram convention (two identification streams merging into
one screening/inclusion path, with excluded/pending counts as labelled side
branches) rather than as a generic box-and-arrow chart. Every count is read
directly from data/corpus_raw.csv, data/corpus_screened.csv and
data/seed_bibliography.csv -- recompute and update if the corpus changes.

Deliberately NOT presented as a completed PRISMA 2020 diagram: screening of the
2026 algorithmic harvest is ongoing (126 structural candidates remain
unreviewed), and the caption says so. See manuscript.qmd Sec2.2 for why this
distinction is stated explicitly rather than left implicit.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

# -- palette (validated categorical set; used sparingly -- one accent, one muted) --
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
BORDER = "#c3c2b7"
SURFACE = "#ffffff"
ACCENT_FILL = "#eaf1fb"     # light tint of categorical slot 1 (blue #2a78d6)
ACCENT_BORDER = "#2a78d6"
NEUTRAL_FILL = "#f4f3f0"    # light neutral for side/exclusion boxes
FINAL_FILL = "#e8f5ee"      # light tint of aqua/green slot for the terminal box
FINAL_BORDER = "#1baf7a"

fig, ax = plt.subplots(figsize=(7.2, 9.6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 15.6)
ax.axis("off")

MAIN_W = 5.7
SIDE_W = 3.4


def box(cx, cy, w, h, text, fill=SURFACE, border=INK, lw=1.1, fontsize=8.6,
        weight="normal", color=INK, style="normal"):
    b = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                        boxstyle="round,pad=0.10,rounding_size=0.09",
                        facecolor=fill, edgecolor=border, linewidth=lw, zorder=2)
    ax.add_patch(b)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fontsize,
             weight=weight, color=color, style=style, linespacing=1.4, zorder=3,
             wrap=True)
    return (cx, cy, w, h)


def down_arrow(b, gap=0.62, color=INK_SECONDARY):
    cx, cy, w, h = b
    y0, y1 = cy - h / 2, cy - h / 2 - gap
    ax.add_patch(FancyArrowPatch((cx, y0), (cx, y1), arrowstyle="-|>",
                                  mutation_scale=11, color=color, linewidth=1.0, zorder=1))


def side_arrow(b_from, cx_to, cy_to, color=INK_MUTED):
    cx, cy, w, h = b_from
    start = (cx + w / 2, cy)
    end = (cx_to - 0.05, cy_to)
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=10,
                                  color=color, linewidth=0.9, linestyle=(0, (3, 2)),
                                  zorder=1))


def stage_label(y, text):
    ax.text(0.15, y, text, ha="left", va="center", fontsize=8.3, weight="bold",
             color=INK_SECONDARY, rotation=90, rotation_mode="anchor")


CX_MANUAL = 2.85
CX_HARVEST = 6.95

# ---------------------------------------------------------------- IDENTIFICATION
y = 14.9
b_manual0 = box(CX_MANUAL, y, MAIN_W * 0.62, 0.95,
                "Manual literature search\n(2024–2026, phases 1–13)",
                fontsize=8.4)
b_harvest0 = box(CX_HARVEST, y, MAIN_W * 0.62, 0.95,
                 "Algorithmic harvest\n(analysis/harvest_crossref.py, 261 queries)",
                 fontsize=8.4)

y -= 1.55
b_manual1 = box(CX_MANUAL, y, MAIN_W * 0.62, 0.85,
                "94 records identified\nand verified",
                fontsize=8.4)
down_arrow(b_manual0, gap=1.55 - 0.475 - 0.425)

b_harvest1 = box(CX_HARVEST, y, MAIN_W * 0.62, 0.85,
                 "25,750 records returned\n(with duplication across queries)",
                 fontsize=8.4)
down_arrow(b_harvest0, gap=1.55 - 0.475 - 0.425)

y -= 1.35
b_harvest2 = box(CX_HARVEST, y, MAIN_W * 0.62, 0.85,
                 "2,332 unique records\n(deduplicated, pavement-term gated)",
                 fontsize=8.4)
down_arrow(b_harvest1, gap=1.35 - 0.425 - 0.425)

y -= 1.55

# --------------------------------------------------------------------- SCREENING
b_screen = box(CX_HARVEST, y, MAIN_W * 0.62, 1.05,
               "2,307 new records screened\n(25 already in the database)",
               fontsize=8.4)
down_arrow(b_harvest2, gap=1.55 - 0.425 - 0.525)

y -= 1.55
b_flagged = box(CX_HARVEST, y, MAIN_W * 0.62, 0.85,
                "191 flagged as structural\nhybridisation candidates",
                fontsize=8.4)
down_arrow(b_screen, gap=1.55 - 0.525 - 0.425)
side_excl1 = box(SIDE_W / 2 + 0.25, y + 0.85, SIDE_W, 0.85,
                  "2,116 records did not match the\nstructural-candidate proxy filter",
                  fill=NEUTRAL_FILL, border=BORDER, color=INK_SECONDARY, fontsize=7.9)
side_arrow(b_screen, side_excl1[0] + SIDE_W / 2 - SIDE_W, side_excl1[1])

y -= 1.55
b_verified = box(CX_HARVEST, y, MAIN_W * 0.62, 1.05,
                 "65 candidates hand-verified against the\nstructural definition (§2.3) and added",
                 fill=ACCENT_FILL, border=ACCENT_BORDER, fontsize=8.4, weight="bold")
down_arrow(b_flagged, gap=1.55 - 0.425 - 0.525)
side_excl2 = box(SIDE_W / 2 + 0.25, y + 0.05, SIDE_W, 0.85,
                  "126 flagged candidates remain\nunreviewed (next screening pass)",
                  fill=NEUTRAL_FILL, border=BORDER, color=INK_SECONDARY, fontsize=7.9)
side_arrow(b_flagged, side_excl2[0] + SIDE_W / 2 - SIDE_W, side_excl2[1])

# ----------------------------------------------------------------------- MERGE
y -= 1.7
merge_y = y
b_merge = box(4.9, merge_y, 7.0, 0.85, "Combined review database",
              fill=NEUTRAL_FILL, border=INK, fontsize=8.8, weight="bold")
down_arrow(b_manual1, gap=(b_manual1[1] - merge_y) - b_manual1[3] / 2 - b_merge[3] / 2)
down_arrow(b_verified, gap=(b_verified[1] - merge_y) - b_verified[3] / 2 - b_merge[3] / 2)

# ------------------------------------------------------------------------ INCLUDED
y = merge_y - 1.7
b_final = box(4.9, y, 7.6, 1.55,
              "159 records\n143 primary studies + 16 prior reviews (§1)\n"
              "103 of the primary studies structurally coded H1–H7,\n"
              "29 coded ‘none’, 11 coded ‘context’",
              fill=FINAL_FILL, border=FINAL_BORDER, fontsize=8.9, weight="bold")
down_arrow(b_merge, gap=1.7 - 0.425 - 0.775)

y -= 1.55
b_target = box(4.9, y, 6.6, 0.85,
               "Target for the completed audit: 150–500 records\n"
               "(screening continues from the 126 candidates above)",
               fill=SURFACE, border=BORDER, color=INK_SECONDARY, fontsize=8.0,
               style="italic")
down_arrow(b_final, gap=1.55 - 0.775 - 0.425)

# ---- stage labels (PRISMA convention: vertical labels along the left margin) ----
stage_label((14.9 + 12.0) / 2, "Identification")
stage_label((10.65 + 7.55) / 2, "Screening")
stage_label((5.55 + 1.6) / 2, "Included")

fig.text(0.5, 0.985, "Review process, 2026–08–09", ha="center",
          fontsize=12.5, weight="bold", color=INK)
fig.text(0.5, 0.965,
          "Reported as the process currently stands, not as a completed PRISMA 2020 "
          "flow diagram — every count traces to the harvest logs and working database.",
          ha="center", fontsize=8.0, style="italic", color=INK_SECONDARY)

plt.tight_layout(rect=[0.02, 0.0, 1, 0.955])
plt.savefig("fig05_review_flow.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.savefig("fig05_review_flow.pdf", bbox_inches="tight", facecolor="white")
print("wrote fig05_review_flow.png / .pdf")
