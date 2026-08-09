#!/usr/bin/env python3
"""
harvest_crossref.py
====================
Fallback corpus harvester for the same project as harvest_openalex.py, using the
Crossref REST API instead of OpenAlex.

WHY THIS EXISTS
---------------
The first real attempt to run harvest_openalex.py from this environment (2026-08-09)
found that OpenAlex now meters its API behind a credits system, and the shared egress
IP this environment sits behind had already exhausted its one-time free credit balance
before we made a single successful call: every request returned HTTP 429 with
`X-RateLimit-Remaining-USD: 0` and `Retry-After: ~27,763s` (~7.7 hours) --- not a
per-second throttle we could back off from, a hard multi-hour wall. Semantic Scholar's
API returned 429 from the same IP for the same reason. Crossref's API, tested the same
way, returned clean 200s under its normal polite-pool limits (3 req/s). This script
therefore reuses harvest_openalex.py's exact query vocabulary (imported, not copied) and
re-implements only the transport layer against Crossref.

TRADE-OFF vs OpenAlex
----------------------
Crossref covers effectively the same DOI universe but:
  - very few records carry an abstract (most publishers don't deposit one), so
    downstream screening here leans harder on title + venue + the query that found it
    than the OpenAlex version could.
  - citation counts (`is-referenced-by-count`) are usually lower than OpenAlex's
    `cited_by_count` for the same DOI (different indexing coverage) --- treat as
    directional, not authoritative for ranking.
  - no boolean full-text search; `query.bibliographic` is Crossref's closest analogue
    and is used here.
Every row still carries a real, live DOI resolved by Crossref itself --- nothing here
is fabricated or inferred.

USAGE
-----
    pip install requests
    python harvest_crossref.py --email you@example.org --out corpus_raw.csv
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
import time
from pathlib import Path
from typing import Dict, List, Optional

import requests

sys.path.insert(0, str(Path(__file__).parent))
from harvest_openalex import (  # noqa: E402  (reuse the vocabulary, not the transport)
    OPTIMISERS, LEARNERS, LABELS, CORE_ANCHORS, PAVEMENT_RE, DRIFT_RE,
)

CROSSREF = "https://api.crossref.org/works"
YEAR_FROM, YEAR_TO = 2005, 2026

SCREEN_COLS = [
    "screen_ti_ab", "screen_fulltext", "exclusion_reason",
    "hybridisation_type", "self_describes_as_hybrid",
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


def fetch(query: str, email: str, rows: int = 50, max_pages: int = 2,
          sleep: float = 0.4) -> List[dict]:
    """Cursor-paginate api.crossref.org/works, with exponential backoff on 429/5xx."""
    out: List[dict] = []
    cursor = "*"
    headers = {"User-Agent": f"pavement-hybrid-review/1.0 (mailto:{email})"}
    pages = 0
    backoff = 2.0
    while cursor and pages < max_pages:
        params = {
            "query.bibliographic": query,
            "filter": (f"from-pub-date:{YEAR_FROM}-01-01,"
                       f"until-pub-date:{YEAR_TO}-12-31,type:journal-article"),
            "rows": rows, "cursor": cursor, "mailto": email,
            "select": "DOI,title,container-title,type,published,author,"
                      "is-referenced-by-count,abstract",
        }
        try:
            r = requests.get(CROSSREF, params=params, headers=headers, timeout=60)
            if r.status_code == 429:
                wait = float(r.headers.get("Retry-After", backoff))
                wait = min(wait, 30.0)  # a multi-hour Retry-After means give up, not stall
                print(f"    ! 429; backing off {wait:.0f}s", file=sys.stderr)
                time.sleep(wait)
                backoff = min(backoff * 2, 30.0)
                pages += 1
                continue
            r.raise_for_status()
        except requests.RequestException as exc:
            print(f"    ! {exc}; backing off", file=sys.stderr)
            time.sleep(5)
            pages += 1
            continue
        payload = r.json().get("message", {})
        items = payload.get("items", [])
        out.extend(items)
        cursor = payload.get("next-cursor")
        pages += 1
        if not items or len(items) < rows:
            break
        time.sleep(sleep)
    return out


def pub_year(item: dict) -> Optional[int]:
    for key in ("published", "published-print", "published-online", "issued"):
        dp = (item.get(key) or {}).get("date-parts")
        if dp and dp[0] and dp[0][0]:
            return dp[0][0]
    return None


def flatten(item: dict, label: str) -> dict:
    title = "; ".join(item.get("title") or [])
    container = "; ".join(item.get("container-title") or [])
    authors = "; ".join(
        f"{a.get('family', '')}, {a.get('given', '')}".strip(", ")
        for a in item.get("author", []) or []
        if a.get("family")
    )
    abstract = re.sub(r"<[^>]+>", " ", item.get("abstract") or "").strip()
    blob = f"{title} {abstract}"
    row = {
        "doi": (item.get("DOI") or "").lower(),
        "year": pub_year(item),
        "type": item.get("type"),
        "title": title,
        "authors": authors,
        "venue": container,
        "cited_by_count": item.get("is-referenced-by-count", 0),
        "is_oa": "",
        "oa_url": "",
        "abstract": abstract,
        "found_by": label,
        "pavement_hit": bool(PAVEMENT_RE.search(blob)),
        "drift_hit": bool(DRIFT_RE.search(blob)),
        "label_hybrid": bool(re.search(r"hybrid", blob, re.I)),
    }
    for c in SCREEN_COLS:
        row[c] = ""
    return row


COLUMNS = list(flatten({"title": [], "author": []}, "").keys())


def harvest(email: str, limit_queries: Optional[int] = None) -> tuple[List[dict], List[dict]]:
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
    if limit_queries:
        queries = queries[:limit_queries]

    seen: Dict[str, dict] = {}
    log: List[dict] = []

    for i, (lane, q) in enumerate(queries, 1):
        print(f"[{i}/{len(queries)}] ({lane}) {q}", flush=True)
        items = fetch(q, email)
        new = kept = 0
        for it in items:
            row = flatten(it, f"{lane}:{q}")
            key = row["doi"] or row["title"].lower()
            if not key:
                continue
            if key in seen:
                seen[key]["found_by"] += f" | {lane}:{q}"
                continue
            if not row["pavement_hit"]:
                continue
            seen[key] = row
            new += 1
            kept += 1
        log.append({"lane": lane, "query": q, "returned": len(items), "new_unique": new})
        print(f"    returned {len(items)}, kept {kept}", flush=True)

    rows = sorted(seen.values(), key=lambda r: (-(r["cited_by_count"] or 0), -(r["year"] or 0)))
    return rows, log


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--email", required=True, help="Crossref polite-pool contact address")
    ap.add_argument("--out", default="corpus_raw.csv")
    ap.add_argument("--prisma", default="prisma_query_log.csv")
    ap.add_argument("--limit-queries", type=int, default=None,
                     help="debug: only run the first N queries")
    args = ap.parse_args()

    rows, log = harvest(args.email, args.limit_queries)

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
    print("\n--- PRISMA identification (Crossref) ---")
    print(f"queries run                          : {len(log)}")
    print(f"records returned                     : {sum(l['returned'] for l in log)}")
    print(f"unique, pavement-gated               : {len(rows)}")
    print(f"  of which contain the word 'hybrid' : {labelled} "
          f"({100*labelled/max(len(rows),1):.1f}%)")
    print(f"  flagged for possible domain drift  : {drift}")
    print(f"written to                           : {args.out}")


if __name__ == "__main__":
    main()
