#!/usr/bin/env python3
"""
fig_domain_optimizer.py
=========================
Figure 5 (Sec3, Bibliometric landscape): two real, corpus-derived panels that
were previously missing from the section -- (a) which pavement sub-domain the
corpus's hybridisation activity concentrates in, and (b) which optimiser
families recur most often. Both are read directly from
data/seed_bibliography.csv (the `pavement_domain` field, 100% populated across
143 primary studies, and `optimizer_hybrid`, populated for 70 of them where an
optimiser applies at all) -- nothing here is estimated, sampled, or drawn from
an external bibliometric tool.

Panel (b) applies light, disclosed text normalisation (merging "PSO" and
"particle swarm optimization" as one bucket, for example) since the field is
free text describing what a batch script's author observed in each paper's
title/abstract, not a controlled vocabulary; the normalisation map is defined
in this script and is the complete, auditable record of what was merged.
"""

import csv
import re
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["DejaVu Sans", "Arial", "Helvetica"]

INK = "#0b0b0b"
INK_SECONDARY = "#52514e"
BAR_COLOR_1 = "#2a78d6"   # categorical slot 1 (blue)
BAR_COLOR_2 = "#eb6834"   # categorical slot 2 (orange)
GRID_COLOR = "#e1e0d9"

ROOT = Path(__file__).parent.parent
DB = ROOT / "data" / "seed_bibliography.csv"

DOMAIN_LABELS = {
    "performance-prediction": "Performance prediction",
    "materials": "Materials",
    "distress-detection": "Distress detection",
    "M&R-and-PMS": "M&R / PMS",
    "structural-evaluation": "Structural evaluation",
    "geotechnical (subgrade-adjacent)": "Geotechnical (subgrade)",
    "materials/test-simulation": "Materials / test-simulation",
    "structural-response": "Structural response",
    "design": "Design",
    "geotechnical (adjacent)": "Geotechnical (adjacent)",
    "cross-domain": "Cross-domain",
    "materials/performance-prediction": "Materials / performance",
}

# Disclosed normalisation: free-text optimizer_hybrid values -> a canonical family
# name. Anything not matched here is dropped from panel (b), not miscounted into
# an unrelated bucket -- see the printed "unmatched" list when this script runs.
OPTIMIZER_PATTERNS = [
    (r"particle swarm|\bpso\b", "PSO"),
    (r"genetic algorithm|\bga\b(?!p)", "Genetic algorithm"),
    (r"bayesian optim", "Bayesian optimisation"),
    (r"grey wolf|\bgwo\b", "Grey wolf optimizer"),
    (r"whale optim|\bwoa\b", "Whale optimization"),
    (r"gene expression programming|\bgep\b", "GEP (symbolic search)"),
    (r"salp swarm", "Salp swarm optimization"),
    (r"symbiotic organisms", "Symbiotic organisms search"),
    (r"beetle antennae", "Beetle antennae search"),
    (r"wavelet|empirical mode decomposition|\bemd\b|\bvmd\b", "Signal decomposition (H6 front-end)"),
]


def normalize_optimizer(raw: str):
    low = raw.lower()
    for pattern, label in OPTIMIZER_PATTERNS:
        if re.search(pattern, low):
            return label
    return None


def main():
    with DB.open(encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    primary = [r for r in rows if "prior review" not in r["role_in_review"]]

    # Panel (a): domain distribution
    domain_counts = Counter(r["pavement_domain"].strip() for r in primary if r["pavement_domain"].strip())
    domain_items = sorted(domain_counts.items(), key=lambda kv: kv[1])
    domain_labels = [DOMAIN_LABELS.get(k, k) for k, _ in domain_items]
    domain_values = [v for _, v in domain_items]

    # Panel (b): optimizer family frequency (normalised, disclosed)
    unmatched = []
    opt_counter = Counter()
    for r in primary:
        raw = r["optimizer_hybrid"].strip()
        if not raw or raw.lower().startswith("none"):
            continue
        label = normalize_optimizer(raw)
        if label:
            opt_counter[label] += 1
        else:
            unmatched.append(raw)
    opt_items = sorted(opt_counter.items(), key=lambda kv: kv[1])
    opt_labels = [k for k, _ in opt_items]
    opt_values = [v for _, v in opt_items]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(11.5, 5.2))

    ax1.barh(domain_labels, domain_values, color=BAR_COLOR_1, height=0.62, zorder=3)
    ax1.set_title("(a) Pavement sub-domain\n(143 primary studies)", fontsize=10.5, weight="bold", pad=10)
    ax1.set_xlabel("Primary studies", fontsize=9, color=INK_SECONDARY)
    ax1.tick_params(axis="y", labelsize=8.6)
    ax1.tick_params(axis="x", labelsize=8)
    ax1.grid(axis="x", color=GRID_COLOR, linewidth=0.8, zorder=0)
    ax1.set_axisbelow(True)
    for spine in ("top", "right"):
        ax1.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax1.spines[spine].set_color(GRID_COLOR)
    for y, v in enumerate(domain_values):
        ax1.text(v + 0.6, y, str(v), va="center", fontsize=8, color=INK_SECONDARY)

    ax2.barh(opt_labels, opt_values, color=BAR_COLOR_2, height=0.62, zorder=3)
    ax2.set_title(f"(b) Named optimiser family\n({sum(opt_values)} of 143 studies where one applies)",
                  fontsize=10.5, weight="bold", pad=10)
    ax2.set_xlabel("Primary studies", fontsize=9, color=INK_SECONDARY)
    ax2.tick_params(axis="y", labelsize=8.6)
    ax2.tick_params(axis="x", labelsize=8)
    ax2.grid(axis="x", color=GRID_COLOR, linewidth=0.8, zorder=0)
    ax2.set_axisbelow(True)
    for spine in ("top", "right"):
        ax2.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax2.spines[spine].set_color(GRID_COLOR)
    for y, v in enumerate(opt_values):
        ax2.text(v + 0.15, y, str(v), va="center", fontsize=8, color=INK_SECONDARY)

    fig.suptitle("Where the corpus's hybridisation activity concentrates",
                  fontsize=13, weight="bold", y=1.04)
    fig.text(0.5, 0.985,
              "Both panels are tabulated directly from data/seed_bibliography.csv, not estimated.",
              ha="center", fontsize=8.2, style="italic", color=INK_SECONDARY)

    plt.tight_layout(rect=[0, 0, 1, 0.93])
    plt.savefig("fig_domain_optimizer.png", dpi=300, bbox_inches="tight", facecolor="white")
    plt.savefig("fig_domain_optimizer.pdf", bbox_inches="tight", facecolor="white")
    print("wrote fig_domain_optimizer.png / .pdf")
    print(f"\ndomain panel: {dict(domain_items)}")
    print(f"optimizer panel: {dict(opt_items)}")
    if unmatched:
        print(f"\n{len(unmatched)} optimizer_hybrid values not matched by any pattern (excluded from panel b):")
        for u in unmatched:
            print(f"  - {u[:80]}")


if __name__ == "__main__":
    main()
