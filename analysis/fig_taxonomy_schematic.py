#!/usr/bin/env python3
"""
fig_taxonomy_schematic.py
===========================
Figure 3 (inserted after @tbl-taxonomy): a visual schematic of the seven
hybridisation architectures (H1-H7), complementing the text table with a
diagram a reader can parse at a glance. Each panel uses a minimal, consistent
box-and-arrow visual language so the seven types are directly comparable:
optimiser/search components in the accent colour, learner/model components in
the neutral-fill box style, data/physics elements in the secondary accent.

This is a schematic of the GENERAL architecture each type names (matching the
formal notation in the "Formal structure of each type" subsection of Sec4), not
a diagram of any one specific paper's implementation.
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch, Circle

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
LEARNER_FILL = "#eaf1fb"
LEARNER_BORDER = "#2a78d6"      # categorical slot 1 (blue) -- the learner/model
SEARCH_FILL = "#fdece3"
SEARCH_BORDER = "#eb6834"       # categorical slot 2 (orange) -- optimiser/search
DATA_FILL = "#e8f5ee"
DATA_BORDER = "#1baf7a"         # categorical slot 3 (aqua) -- data/physics/decomposition
NEUTRAL_FILL = "#f4f3f0"
NEUTRAL_BORDER = "#c3c2b7"


def panel(ax, title):
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.text(5, 9.4, title, ha="center", va="top", fontsize=10.5, weight="bold", color=INK)


def box(ax, cx, cy, w, h, text, fill, border, fontsize=7.6, color=INK):
    b = FancyBboxPatch((cx - w / 2, cy - h / 2), w, h,
                        boxstyle="round,pad=0.08,rounding_size=0.12",
                        facecolor=fill, edgecolor=border, linewidth=1.3, zorder=2)
    ax.add_patch(b)
    ax.text(cx, cy, text, ha="center", va="center", fontsize=fontsize, color=color,
             weight="medium", linespacing=1.25, zorder=3)


def arrow(ax, p1, p2, color=INK_SECONDARY, style="-|>", lw=1.1, ls="-"):
    ax.add_patch(FancyArrowPatch(p1, p2, arrowstyle=style, mutation_scale=11,
                                  color=color, linewidth=lw, linestyle=ls, zorder=1))


fig, axes = plt.subplots(2, 4, figsize=(11.5, 6.4))
axes = axes.flatten()

# --- H1: metaheuristic -> hyperparameters ---
ax = axes[0]
panel(ax, "H1  Metaheuristic → hyperparameters")
box(ax, 2.2, 6.3, 3.0, 1.8, "Metaheuristic\nsearch", SEARCH_FILL, SEARCH_BORDER)
box(ax, 7.4, 6.3, 3.0, 1.8, "Base learner\n$f_\\theta$", LEARNER_FILL, LEARNER_BORDER)
arrow(ax, (3.7, 6.3), (5.9, 6.3))
ax.text(4.8, 6.85, "tunes $\\phi$", ha="center", fontsize=7.6, style="italic", color=INK_SECONDARY)
arrow(ax, (7.4, 5.4), (7.4, 3.6), style="-", lw=0.9, ls=(0, (2, 2)))
ax.text(7.4, 3.05, "$\\theta$ fit by\ngradient descent", ha="center", fontsize=6.3, color=INK_SECONDARY)

# --- H2: metaheuristic -> weights ---
ax = axes[1]
panel(ax, "H2  Metaheuristic → weights")
box(ax, 2.2, 6.3, 3.0, 1.8, "Metaheuristic\nsearch", SEARCH_FILL, SEARCH_BORDER)
box(ax, 7.4, 6.3, 3.0, 1.8, "Base learner\n$f_\\theta$", LEARNER_FILL, LEARNER_BORDER)
arrow(ax, (3.7, 6.3), (5.9, 6.3))
ax.text(4.8, 6.85, "sets $\\theta$", ha="center", fontsize=7.6, style="italic", color=INK_SECONDARY)
ax.text(4.8, 3.9, "no gradient step:\n$\\mathcal{M}$ replaces backprop entirely",
        ha="center", fontsize=6.3, color=INK_SECONDARY)

# --- H3: physics + data ---
ax = axes[2]
panel(ax, "H3  Physics + data")
box(ax, 5, 6.4, 4.4, 1.7, "$f_\\theta(x)$", LEARNER_FILL, LEARNER_BORDER)
box(ax, 2.6, 3.2, 2.6, 1.6, "Data loss\n$\\mathcal{L}_{data}$", NEUTRAL_FILL, NEUTRAL_BORDER, fontsize=7.0)
box(ax, 7.4, 3.2, 2.6, 1.6, "Physics residual\n$\\mathcal{N}[f_\\theta]$", DATA_FILL, DATA_BORDER, fontsize=7.0)
arrow(ax, (4.2, 5.5), (2.9, 4.05))
arrow(ax, (5.8, 5.5), (7.1, 4.05))
ax.text(5, 1.3, "$\\mathcal{L}_{total} = \\mathcal{L}_{data} + \\lambda\\,\\mathcal{L}_{phys}$",
        ha="center", fontsize=7.6)

# --- H4: architecture fusion ---
ax = axes[3]
panel(ax, "H4  Architecture fusion")
box(ax, 2.6, 6.2, 3.2, 1.8, "Encoder $h_1$\n(e.g. CNN)", LEARNER_FILL, LEARNER_BORDER, fontsize=7.2)
box(ax, 7.4, 6.2, 3.2, 1.8, "Encoder $h_2$\n(e.g. transformer)", LEARNER_FILL, LEARNER_BORDER, fontsize=7.2)
box(ax, 5, 2.8, 3.6, 1.7, "Fusion $g(h_1,h_2)$", DATA_FILL, DATA_BORDER, fontsize=7.4)
arrow(ax, (2.9, 5.3), (4.4, 3.55))
arrow(ax, (7.1, 5.3), (5.6, 3.55))

# --- H5: heterogeneous stacking ---
ax = axes[4]
panel(ax, "H5  Heterogeneous stacking")
xs = [1.8, 4.0, 6.2, 8.4]
labels = ["$f_1$", "$f_2$", "$\\cdots$", "$f_k$"]
for x, lab in zip(xs, labels):
    box(ax, x, 6.6, 1.7, 1.5, lab, LEARNER_FILL, LEARNER_BORDER, fontsize=8.5)
box(ax, 5, 2.9, 4.2, 1.8, "Meta-learner\n$g_{meta}$", DATA_FILL, DATA_BORDER, fontsize=7.4)
for x in xs:
    arrow(ax, (x, 5.85), (5 + (x - 5) * 0.25, 3.85))
ax.text(5, 1.2, "on out-of-fold predictions, not in-fold", ha="center",
        fontsize=6.6, color=INK_SECONDARY, style="italic")

# --- H6: decomposition then learn ---
ax = axes[5]
panel(ax, "H6  Decomposition then learn")
box(ax, 5, 7.2, 4.2, 1.5, "$x(t)$", NEUTRAL_FILL, NEUTRAL_BORDER, fontsize=8)
xs6 = [1.9, 3.75, 6.25, 8.1]
labels6 = ["$c_1$", "$c_2$", "$\\cdots$", "$c_n$"]
for x, lab in zip(xs6, labels6):
    box(ax, x, 4.6, 1.6, 1.4, lab, DATA_FILL, DATA_BORDER, fontsize=8)
    arrow(ax, (5 + (x - 5) * 0.3, 6.45), (x, 5.3))
box(ax, 5, 1.9, 4.4, 1.6, "$f_\\theta(c_1,\\ldots,c_n)$", LEARNER_FILL, LEARNER_BORDER, fontsize=7.4)
for x in xs6:
    arrow(ax, (x, 3.9), (5 + (x - 5) * 0.35, 2.7))

# --- H7: symbolic-numeric ---
ax = axes[6]
panel(ax, "H7  Symbolic–numeric")
box(ax, 2.3, 6.3, 3.0, 1.9, "Genetic /\ngrammatical search", SEARCH_FILL, SEARCH_BORDER, fontsize=7.2)
box(ax, 7.5, 6.1, 3.2, 2.6, "expr($x$; $c$)\n\ne.g. $a{\\cdot}x_1 + \\frac{x_2}{b}$", DATA_FILL, DATA_BORDER, fontsize=7.2)
arrow(ax, (3.85, 6.3), (5.85, 6.3))
ax.text(4.85, 4.55, "evolves both structure\nand coefficients $c$", ha="center", fontsize=6.3, color=INK_SECONDARY)

# --- legend panel ---
ax = axes[7]
ax.set_xlim(0, 10); ax.set_ylim(0, 10); ax.axis("off")
ax.text(5, 9.4, "Legend", ha="center", va="top", fontsize=10.5, weight="bold", color=INK)
box(ax, 5, 7.3, 6.5, 1.3, "Base learner / model component", LEARNER_FILL, LEARNER_BORDER, fontsize=7.8)
box(ax, 5, 5.3, 6.5, 1.3, "Metaheuristic / search component", SEARCH_FILL, SEARCH_BORDER, fontsize=7.8)
box(ax, 5, 3.3, 6.5, 1.3, "Data, physics or decomposition component", DATA_FILL, DATA_BORDER, fontsize=7.6)
box(ax, 5, 1.3, 6.5, 1.3, "Non-learned intermediate quantity", NEUTRAL_FILL, NEUTRAL_BORDER, fontsize=7.8)

fig.suptitle("Schematic architecture of the seven hybridisation types (H1–H7)",
             fontsize=13, weight="bold", y=1.015)
fig.text(0.5, 0.975,
          "General couplings each type names (§4.1); not one specific paper's implementation.",
          ha="center", fontsize=8.3, style="italic", color=INK_SECONDARY)

plt.tight_layout(rect=[0, 0, 1, 0.95])
plt.savefig("fig_taxonomy_schematic.png", dpi=300, bbox_inches="tight", facecolor="white")
plt.savefig("fig_taxonomy_schematic.pdf", bbox_inches="tight", facecolor="white")
print("wrote fig_taxonomy_schematic.png / .pdf")
