#!/usr/bin/env python3
"""
fig_leakage_diagram.py
=======================
Figure 4: conceptual diagram contrasting a random (ungrouped) split against a
section-grouped split for the same 33-section CRCP substrate documented in
Section 7 -- the mechanism, not just the claim, made visible.

This is not illustrative-only: the "random split" panel reproduces the actual
partitioning described in @Alnaqbi2025learning's own methods section (5 folds,
observation-level, no section grouping), full-text confirmed (see Section 7 and
the CSV note field for doi 10.1186/s44147-025-00706-9). The "correct" panel shows
the section-grouped alternative the paper did not use. Both panels use the same
33-section, ~12-observations-per-section structure the real substrate has.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

rng = np.random.default_rng(7)

N_SECTIONS = 33
OBS_PER_SECTION = 12
N_OBS = N_SECTIONS * OBS_PER_SECTION  # 396, matches the ~395 in the real substrate
K_FOLDS = 5

# assign each observation to its section
section_of_obs = np.repeat(np.arange(N_SECTIONS), OBS_PER_SECTION)

# --- Panel A: random (ungrouped) split -- what the paper actually did ---
obs_order_random = rng.permutation(N_OBS)
fold_random = np.empty(N_OBS, dtype=int)
fold_random[obs_order_random] = np.arange(N_OBS) % K_FOLDS

# --- Panel B: section-grouped split -- the alternative that avoids leakage ---
section_order = rng.permutation(N_SECTIONS)
fold_of_section = np.empty(N_SECTIONS, dtype=int)
fold_of_section[section_order] = np.arange(N_SECTIONS) % K_FOLDS
fold_grouped = fold_of_section[section_of_obs]

FOLD_COLORS = ["#1f4e79", "#c00000", "#2e7d32", "#e08e00", "#6a1b9a"]


def draw_panel(ax, fold_assignment, title, subtitle, highlight_contam=False):
    # layout: 33 rows (sections) x 12 cols (observations within section)
    grid = fold_assignment.reshape(N_SECTIONS, OBS_PER_SECTION)
    img = np.zeros((N_SECTIONS, OBS_PER_SECTION, 3))
    cmap = [tuple(int(c[i:i+2], 16) / 255 for i in (1, 3, 5)) for c in FOLD_COLORS]
    for f in range(K_FOLDS):
        mask = grid == f
        img[mask] = cmap[f]
    ax.imshow(img, aspect="auto", interpolation="none")
    ax.set_xticks([])
    ax.set_yticks(np.arange(0, N_SECTIONS, 4))
    ax.set_yticklabels([f"Sec {i+1}" for i in range(0, N_SECTIONS, 4)], fontsize=7.5)
    ax.set_title(title, fontsize=11, fontweight="bold", pad=8)
    ax.text(0.5, -0.055, subtitle, transform=ax.transAxes, ha="center",
             fontsize=8.7, style="italic", color="#333333")

    if highlight_contam:
        # circle a couple of sections split across multiple folds to make the
        # contamination visually obvious
        for sec_idx in [4, 15, 26]:
            row = grid[sec_idx]
            if len(set(row)) > 1:
                rect = mpatches.Rectangle((-0.5, sec_idx - 0.5), OBS_PER_SECTION, 1,
                                           fill=False, edgecolor="black", linewidth=1.6,
                                           linestyle="--", zorder=5)
                ax.add_patch(rect)
    else:
        for sec_idx in [4, 15, 26]:
            rect = mpatches.Rectangle((-0.5, sec_idx - 0.5), OBS_PER_SECTION, 1,
                                       fill=False, edgecolor="#2e7d32", linewidth=1.6,
                                       zorder=5)
            ax.add_patch(rect)


fig, axes = plt.subplots(1, 2, figsize=(11.5, 8.6))

draw_panel(
    axes[0], fold_random,
    "A. Random 5-fold split (observation level)",
    "As reported: \u201cthe dataset was split into 5 subsets...\u201d\n"
    "(Alnaqbi et al., full-text confirmed)  \u2014  dashed boxes: one section, multiple folds",
    highlight_contam=True,
)
draw_panel(
    axes[1], fold_grouped,
    "B. Section-grouped 5-fold split",
    "Alternative not used in the reviewed papers\n"
    "solid boxes: one section stays entirely within one fold",
    highlight_contam=False,
)

handles = [mpatches.Patch(color=FOLD_COLORS[i], label=f"Fold {i+1}") for i in range(K_FOLDS)]
fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False,
           bbox_to_anchor=(0.5, -0.01), fontsize=9.5)

fig.suptitle(
    "Why an ungrouped split inflates reported accuracy on section-structured pavement data\n"
    "(33 sections \u00d7 ~12 observations, matching the CRCP substrate audited in Section 7)",
    fontsize=12, y=0.995,
)
fig.text(0.5, 0.895,
          "In Panel A, a model can see 10\u201311 of a section's 12 observations in training and be\n"
          "\u201ctested\u201d on the 12th \u2014 near-duplicate, spatially correlated records leak across the\n"
          "train/test boundary. In Panel B, an entire section is held out together, so the test\n"
          "fold contains no information the model could have seen during training.",
          ha="center", fontsize=9.3, color="#333333")

plt.tight_layout(rect=[0, 0.035, 1, 0.83])
plt.savefig("fig04_leakage_diagram.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.savefig("fig04_leakage_diagram.pdf", bbox_inches="tight", facecolor="white")
print("wrote fig04_leakage_diagram.png / .pdf")
