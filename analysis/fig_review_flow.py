#!/usr/bin/env python3
"""
fig_review_flow.py
====================
Figure 5: the review's identification/screening/inclusion process, styled after
the PRISMA 2020 flow-diagram convention. A single main lane carries the
algorithmic Crossref harvest through its stages (source -> raw returns ->
deduplicated -> screened -> flagged -> hand-verified), with excluded/pending
counts as labelled side branches consistently on the right. The manually
identified, already individually-verified records join as a short tributary at
the merge point rather than running a second full-height parallel lane:
unlike the algorithmic harvest, that stream never went through deduplication or
proxy screening, so giving it the same number of stacked stages would visually
claim a process it did not go through, and it previously left a long, empty
connector line beside the dense harvest column. Every count is read directly
from data/corpus_raw.csv, data/corpus_screened.csv and
data/seed_bibliography.csv -- recompute and update if the corpus changes.

Deliberately NOT presented as a completed PRISMA 2020 diagram: screening of the
2026 algorithmic harvest is ongoing (126 structural candidates remain
unreviewed), and the caption says so. See manuscript.qmd Sec2.2 for why this
distinction is stated explicitly rather than left implicit.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

# -- palette (validated categorical set; used sparingly -- two accents, one muted) --
INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
INK_MUTED = "#898781"
BORDER = "#c3c2b7"
SURFACE = "#ffffff"
ACCENT_FILL = "#eaf1fb"     # light tint of categorical slot 1 (blue #2a78d6) -- harvest verification
ACCENT_BORDER = "#2a78d6"
TRIB_FILL = "#fdece3"       # light tint of categorical slot 2 (orange #eb6834) -- manual tributary
TRIB_BORDER = "#eb6834"
NEUTRAL_FILL = "#f4f3f0"    # light neutral for side/exclusion boxes and the merge box
FINAL_FILL = "#e8f5ee"      # light tint of aqua/green slot for the terminal box
FINAL_BORDER = "#1baf7a"

CX_MAIN = 5.35
MAIN_W = 4.9
CX_EXCL = 9.75
EXCL_W = 3.4
CX_TRIB = 1.95
TRIB_W = 2.95
GAP = 0.60

fig, ax = plt.subplots(figsize=(8.8, 10.6))
ax.set_xlim(0, 11.9)
ax.set_ylim(-0.7, 15.9)
ax.axis("off")


def box(cx, cy, w, h, text, fill=SURFACE, border=INK, lw=1.1, fontsize=8.5,
        weight="normal", color=INK, style="normal"):
    b = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                        boxstyle="round,pad=0.10,rounding_size=0.09",
                        facecolor=fill, edgecolor=border, linewidth=lw, zorder=2)
    ax.add_patch(b)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fontsize,
             weight=weight, color=color, style=style, linespacing=1.4, zorder=3,
             wrap=True)
    return (cx, cy, w, h)


def below(y_prev, h_prev, h_curr, gap=GAP):
    """Centre-y of a box placed directly below the previous one, edge-to-edge gap `gap`."""
    return y_prev - h_prev / 2 - gap - h_curr / 2


def down_arrow(b, gap=GAP, color=INK_SECONDARY):
    cx, cy, w, h = b
    ax.add_patch(FancyArrowPatch((cx, cy - h / 2), (cx, cy - h / 2 - gap), arrowstyle="-|>",
                                  mutation_scale=11, color=color, linewidth=1.1, zorder=1))


def side_arrow(b_from, b_to, color=INK_MUTED):
    cx, cy, w, h = b_from
    tx, ty, tw, th = b_to
    start = (cx + w / 2, cy)
    end = (tx - tw / 2, ty)
    ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=10,
                                  color=color, linewidth=0.95, linestyle=(0, (3, 2)), zorder=1))


def merge_in_arrow(b_from, target_xy, color=INK_SECONDARY):
    """Diagonal connector for the manual tributary joining the merge box's top-left corner."""
    cx, cy, w, h = b_from
    ax.add_patch(FancyArrowPatch((cx, cy - h / 2), target_xy, arrowstyle="-|>",
                                  mutation_scale=11, color=color, linewidth=1.15, zorder=1))


def stage_label(y0, y1, text):
    ax.text(0.55, (y0 + y1) / 2, text, ha="center", va="center", fontsize=8.7,
             weight="bold", color=INK_SECONDARY, rotation=90, rotation_mode="anchor")
    ax.plot([0.2, 0.2], [y0, y1], color=BORDER, linewidth=1.2, zorder=0, solid_capstyle="round")


# ---------------------------------------------------------------- IDENTIFICATION
y = 15.15
b_source = box(CX_MAIN, y, MAIN_W, 0.95,
               "Automated harvest — Crossref API\n"
               "261 queries: optimiser × learner × pavement vocabulary\n"
               "(analysis/harvest_crossref.py)",
               fontsize=8.4)
id_top = y + 0.475 + 0.18

y = below(y, 0.95, 0.85)
b_raw = box(CX_MAIN, y, MAIN_W, 0.85, "25,750 records returned\n(duplication across queries)", fontsize=8.5)
down_arrow(b_source)

y = below(y, 0.85, 0.85)
b_unique = box(CX_MAIN, y, MAIN_W, 0.85, "2,332 unique records\n(deduplicated, pavement-term gated)", fontsize=8.5)
down_arrow(b_raw)
id_bottom = y - 0.425 - 0.18

# --------------------------------------------------------------------- SCREENING
y = below(y, 0.85, 1.0)
b_screen = box(CX_MAIN, y, MAIN_W, 1.0, "2,307 new records screened\n(25 already in the database)", fontsize=8.5)
down_arrow(b_unique)
screen_top = y + 0.5 + 0.18

y = below(y, 1.0, 0.85)
b_flagged = box(CX_MAIN, y, MAIN_W, 0.85, "191 flagged as structural\nhybridisation candidates", fontsize=8.5)
down_arrow(b_screen)
side_excl1 = box(CX_EXCL, y, EXCL_W, 0.95,
                  "2,116 records did not match the\nstructural-candidate proxy filter — excluded",
                  fill=NEUTRAL_FILL, border=BORDER, color=INK_SECONDARY, fontsize=7.8)
side_arrow(b_flagged, side_excl1)

y = below(y, 0.85, 1.05)
b_verified = box(CX_MAIN, y, MAIN_W, 1.05,
                  "65 candidates hand-verified against the\nstructural definition (§2.3) and added",
                  fill=ACCENT_FILL, border=ACCENT_BORDER, fontsize=8.5, weight="bold")
down_arrow(b_flagged)
side_excl2 = box(CX_EXCL, y, EXCL_W, 0.95,
                  "126 flagged candidates remain\nunreviewed — next screening pass, not excluded",
                  fill=NEUTRAL_FILL, border=BORDER, color=INK_SECONDARY, fontsize=7.8)
side_arrow(b_verified, side_excl2)
screen_bottom = y - 0.525 - 0.18

# --------------------------------------------------------- MANUAL TRIBUTARY + MERGE
# The tributary gets its own row (below b_verified, above the merge box) so it can
# never overlap either neighbour, however wide its box is drawn -- `below()` reasons
# in y only, so the horizontal offset of the tributary from the main lane is free.
row_trib_y = below(y, 1.05, 1.7, gap=0.75)
b_manual = box(CX_TRIB, row_trib_y, TRIB_W, 1.7,
               "Manual / connector-assisted\nliterature search\n"
               "94 records identified and\nindividually verified\n"
               "(2024–2026, ahead of and\nseparate from the harvest above)",
               fill=TRIB_FILL, border=TRIB_BORDER, fontsize=7.5)

merge_y = below(row_trib_y, 1.7, 0.85, gap=0.55)
b_merge = box(CX_MAIN, merge_y, 6.0, 0.85, "Combined review database",
              fill=NEUTRAL_FILL, border=INK, fontsize=8.8, weight="bold")
# a single long connector carries the main lane past the tributary's row, unbroken
down_arrow(b_verified, gap=(y - 0.525) - (merge_y + 0.425))
merge_in_arrow(b_manual, (CX_MAIN - 6.0 / 2 + 0.4, merge_y + 0.22))

# ------------------------------------------------------------------------ INCLUDED
included_top = merge_y + 0.425 + 0.18
y = below(merge_y, 0.85, 1.55)
b_final = box(CX_MAIN, y, 8.4, 1.55,
              "159 records\n143 primary studies + 16 prior reviews (§1)\n"
              "103 of the primary studies structurally coded H1–H7,\n"
              "29 coded ‘none’, 11 coded ‘context’",
              fill=FINAL_FILL, border=FINAL_BORDER, fontsize=8.8, weight="bold")
down_arrow(b_merge)

y = below(y, 1.55, 0.85)
b_target = box(CX_MAIN, y, 7.2, 0.85,
               "Target for the completed audit: 150–500 records\n"
               "(screening continues from the 126 candidates above)",
               fill=SURFACE, border=BORDER, color=INK_SECONDARY, fontsize=8.0,
               style="italic")
down_arrow(b_final)
included_bottom = y - 0.425 - 0.18

# ---- stage labels (PRISMA convention: vertical labels along the left margin) ----
stage_label(id_top, id_bottom, "Identification")
stage_label(screen_top, screen_bottom, "Screening")
stage_label(included_top, included_bottom, "Included")

fig.text(0.5, 0.986, "Review identification and screening process", ha="center",
          fontsize=12.5, weight="bold", color=INK)
fig.text(0.5, 0.968,
          "Reported as the process currently stands, not as a completed PRISMA 2020 "
          "flow diagram — every count traces to the harvest logs and working database.",
          ha="center", fontsize=8.1, style="italic", color=INK_SECONDARY)

plt.tight_layout(rect=[0.02, 0.0, 1, 0.955])
plt.savefig("fig05_review_flow.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.savefig("fig05_review_flow.pdf", bbox_inches="tight", facecolor="white")
print("wrote fig05_review_flow.png / .pdf")
