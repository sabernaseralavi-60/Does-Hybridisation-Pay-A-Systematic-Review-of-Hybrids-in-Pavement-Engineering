#!/usr/bin/env python3
"""
harvest_openalex.py  (v2 — algorithm-driven)
============================================
Corpus harvesting for:
  "Does Hybridisation Pay? A Systematic Review of Metaheuristic Optimisation and
   Machine Learning Hybrids in Pavement Engineering (2005-2026)"

WHY v2 EXISTS
-------------
v1 searched on method labels ("hybrid", "deep learning", "artificial neural network").
That misses a large share of qualifying studies, because many hybrid pipelines never
call themselves hybrid — they say "optimized", "improved", "novel X-Y", or just name
the two algorithms. A label-driven search misses, for example, Alhussan et al. (2022,
10.1109/access.2022.3196660): dipper-throated optimisation coupled to a random forest
for pothole classification, 106 citations, no prominent use of the word "hybrid".

v2 therefore searches on ALGORITHM NAMES crossed with pavement terms, in three lanes:

  Lane A  optimiser x pavement          — catches H1/H2 regardless of self-description
  Lane B  learner x pavement            — the tabular and vision base literature
  Lane C  label x pavement              — legacy label lane, kept for recall and for
                                          measuring how often the label is actually used

A test sweep showed that optimiser vocabulary drifts hard into concrete, mining,
geopolymer and energy work, so the pavement block is mandatory in every query and is
re-applied as a hard post-filter on title+abstract. Inclusion is then decided on
STRUCTURE, not on the label (see 01_SCOPE_AND_TAXONOMY.md §2).

USAGE
-----
    pip install requests
    python harvest_openalex.py --email you@uk.ac.ir --out corpus_raw.csv

Expect roughly 2,000-4,000 unique records before screening. Nothing here is
fabricated: every row traces to a live OpenAlex work ID.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import time
from typing import Dict, List, Optional

import requests

OPENALEX = "https://api.openalex.org/works"
YEAR_FROM, YEAR_TO = 2005, 2026

# ---------------------------------------------------------------------------
# Lane A — optimisers and search strategies (the vocabulary that finds unlabelled hybrids)
# ---------------------------------------------------------------------------
OPTIMISERS = [
    # classical evolutionary / swarm
    "genetic algorithm", "particle swarm optimization", "differential evolution",
    "simulated annealing", "ant colony optimization", "artificial bee colony",
    "harmony search", "imperialist competitive algorithm", "cuckoo search",
    "firefly algorithm", "bat algorithm", "biogeography-based optimization",
    # 2014+ named metaheuristics that dominate this literature
    "grey wolf optimizer", "whale optimization algorithm", "salp swarm algorithm",
    "grasshopper optimization algorithm", "harris hawks optimization",
    "slime mould algorithm", "symbiotic organisms search", "sine cosine algorithm",
    "teaching-learning-based optimization", "jaya algorithm",
    "beetle antennae search", "marine predators algorithm", "arithmetic optimization",
    "equilibrium optimizer", "political optimizer", "coot optimization",
    "dipper throated optimization", "black-winged kite algorithm",
    "fennec fox optimization", "dingo optimization algorithm",
    "forensic-based investigation optimization", "gravitational search algorithm",
    # surrogate / statistical hyperparameter search
    "bayesian optimization", "tree-structured parzen estimator", "optuna",
    "hyperparameter optimization",
    # generic bait
    "metaheuristic optimization", "nature-inspired algorithm", "swarm intelligence",
    "evolutionary optimization",
]

# ---------------------------------------------------------------------------
# Lane B — base learners
# ---------------------------------------------------------------------------
LEARNERS = [
    "artificial neural network", "multilayer perceptron", "deep learning",
    "convolutional neural network", "long short-term memory", "recurrent neural network",
    "transformer network", "graph neural network", "physics-informed neural network",
    "adaptive neuro-fuzzy inference system", "extreme learning machine",
    "wavelet neural network", "radial basis function network",
    "support vector regression", "least squares support vector machine",
    "random forest", "gradient boosting", "extreme gradient boosting",
    "categorical boosting", "light gradient boosting", "gaussian process regression",
    "group method of data handling", "gene expression programming",
    "multi-gene genetic programming", "evolutionary polynomial regression",
    "multivariate adaptive regression splines", "stacking ensemble",
    "variational mode decomposition", "empirical mode decomposition",
]

# ---------------------------------------------------------------------------
# Lane C — legacy label lane
# ---------------------------------------------------------------------------
LABELS = [
    "hybrid model", "hybrid machine learning", "hybrid intelligent model",
    "optimized machine learning", "soft computing", "data-driven model",
    "surrogate model", "explainable machine learning",
]

# ---------------------------------------------------------------------------
# Mandatory pavement block — used in every query AND as a hard post-filter
# ---------------------------------------------------------------------------
PAVEMENT_TERMS = [
    "pavement", "asphalt", "flexible pavement", "rigid pavement", "subgrade",
    "subbase", "unbound granular", "hot mix asphalt", "bituminous mixture",
    "road surface", "airport pavement", "pavement management",
    "resilient modulus", "dynamic modulus", "international roughness index",
    "pavement condition index", "rutting", "pavement cracking", "pothole",
    "falling weight deflectometer", "backcalculation",
]

# Terms whose presence WITHOUT any pavement term marks off-domain drift.
DRIFT_MARKERS = [
    "geopolymer", "rock burst", "rockburst", "flyrock", "blasting", "slope stability",
    "tunnel", "landslide", "groundwater", "runoff", "streamflow", "wind speed",
    "photovoltaic", "battery", "lithium", "reservoir", "crude oil", "stock price",
    "air quality", "building energy", "3d printing",
]

PAVEMENT_RE = re.compile("|".join(re.escape(t) for t in PAVEMENT_TERMS), re.I)
DRIFT_RE = re.compile("|".join(re.escape(t) for t in DRIFT_MARKERS), re.I)

# Anchors: the pavement terms crossed with every optimiser/learner. Kept short so the
# Cartesian product stays inside a sane query count.
CORE_ANCHORS = [
    "pavement", "asphalt pavement", "subgrade soil", "asphalt mixture",
    "pavement performance", "pavement distress",
]


def deinvert(inv: Optional[Dict[str, List[int]]]) -> str:
    if not inv:
        return ""
    pos: Dict[int, str] = {}
    for word, idxs in inv.items():
        for i in idxs:
            pos[i] = word
    return " ".join(pos[i] for i in sorted(pos)) if pos else ""


def fetch(search: str, email: str, per_page: int = 200, max_pages: int = 15,
          sleep: float = 0.35) -> List[dict]:
    out, cursor, pages = [], "*", 0
    while cursor and pages < max_pages:
        params = {
            "search": search,
            "filter": (f"from_publication_date:{YEAR_FROM}-01-01,"
                       f"to_publication_date:{YEAR_TO}-12-31,"
                       "type:article|review|preprint"),
            "per-page": per_page, "cursor": cursor, "mailto": email,
        }
        try:
            r = requests.get(OPENALEX, params=params, timeout=60)
            r.raise_for_status()
        except requests.RequestException as exc:
            print(f"    ! {exc}; backing off", file=sys.stderr)
            time.sleep(5)
            pages += 1
            continue
        payload = r.json()
        results = payload.get("results", [])
        out.extend(results)
        cursor = payload.get("meta", {}).get("next_cursor")
        pages += 1
        if not results:
            break
        time.sleep(sleep)
    return out


SCREEN_COLS = [
    "screen_ti_ab", "screen_fulltext", "exclusion_reason",
    "hybridisation_type",          # H1..H7, multiple allowed, blank if not hybrid
    "self_describes_as_hybrid",    # yes/no — feeds the vocabulary finding in Section 3
    "optimiser", "base_learner",
    "pavement_domain", "pavement_family", "data_source", "n_samples", "n_inputs",
    "split_protocol", "external_validation", "leakage_risk",
    "hyperparam_reporting", "baseline_strength",
    "premium_computable", "premium_value", "budget_parity_reported",
    "optimiser_novelty_claim", "repeated_runs_reported",
    "uncertainty_quantified", "interpretability_method",
    "metrics_reported", "best_reported_R2", "best_reported_F1",
    "code_available", "data_available", "deployment_evidence", "critique_note",
]


def flatten(work: dict, label: str) -> dict:
    auths = [a.get("author", {}).get("display_name", "") for a in work.get("authorships", [])]
    src = (work.get("primary_location") or {}).get("source") or {}
    oa = work.get("open_access") or {}
    abstract = deinvert(work.get("abstract_inverted_index"))
    title = work.get("title") or ""
    blob = f"{title} {abstract}"
    row = {
        "openalex_id": (work.get("id") or "").split("/")[-1],
        "doi": (work.get("doi") or "").replace("https://doi.org/", ""),
        "year": work.get("publication_year"),
        "type": work.get("type"),
        "title": title,
        "authors": "; ".join(a for a in auths if a),
        "venue": src.get("display_name") or "",
        "cited_by_count": work.get("cited_by_count", 0),
        "is_oa": oa.get("is_oa", False),
        "oa_url": oa.get("oa_url") or "",
        "abstract": abstract,
        "found_by": label,
        "pavement_hit": bool(PAVEMENT_RE.search(blob)),
        "drift_hit": bool(DRIFT_RE.search(blob)),
        "label_hybrid": bool(re.search(r"hybrid", blob, re.I)),
    }
    for c in SCREEN_COLS:
        row[c] = ""
    return row


COLUMNS = list(flatten({}, "").keys())


def harvest(email: str) -> tuple[List[dict], List[dict]]:
    queries: List[tuple[str, str]] = []
    for opt in OPTIMISERS:
        for anchor in CORE_ANCHORS[:3]:
            queries.append(("A", f"{opt} {anchor}"))
    for lrn in LEARNERS:
        for anchor in CORE_ANCHORS[:3]:
            queries.append(("B", f"{lrn} {anchor}"))
    for lab in LABELS:
        for anchor in CORE_ANCHORS:
            queries.append(("C", f"{lab} {anchor}"))

    seen: Dict[str, dict] = {}
    log: List[dict] = []

    for i, (lane, q) in enumerate(queries, 1):
        print(f"[{i}/{len(queries)}] ({lane}) {q}")
        works = fetch(q, email)
        new = kept = 0
        for w in works:
            row = flatten(w, f"{lane}:{q}")
            key = row["doi"].lower() or row["openalex_id"]
            if key in seen:
                seen[key]["found_by"] += f" | {lane}:{q}"
                continue
            # hard domain gate: must mention pavement vocabulary somewhere
            if not row["pavement_hit"]:
                continue
            seen[key] = row
            new += 1
            kept += 1
        log.append({"lane": lane, "query": q, "returned": len(works), "new_unique": new})
        print(f"    returned {len(works)}, kept {kept}")

    rows = sorted(seen.values(), key=lambda r: (-(r["cited_by_count"] or 0), -(r["year"] or 0)))
    return rows, log


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--email", required=True, help="OpenAlex polite-pool contact address")
    ap.add_argument("--out", default="corpus_raw.csv")
    ap.add_argument("--prisma", default="prisma_query_log.csv")
    args = ap.parse_args()

    rows, log = harvest(args.email)

    with open(args.out, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    with open(args.prisma, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["lane", "query", "returned", "new_unique"])
        w.writeheader()
        w.writerows(log)

    labelled = sum(1 for r in rows if r["label_hybrid"])
    drift = sum(1 for r in rows if r["drift_hit"])
    print("\n--- PRISMA identification ---")
    print(f"queries run                          : {len(log)}")
    print(f"records returned                     : {sum(l['returned'] for l in log)}")
    print(f"unique, pavement-gated               : {len(rows)}")
    print(f"  of which contain the word 'hybrid' : {labelled} "
          f"({100*labelled/max(len(rows),1):.1f}%)")
    print(f"  flagged for possible domain drift  : {drift}")
    print(f"written to                           : {args.out}")
    print("\nThe 'hybrid' percentage above is itself a reportable result: it quantifies")
    print("how much of this literature a label-driven search would have missed.")


if __name__ == "__main__":
    main()
