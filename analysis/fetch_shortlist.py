#!/usr/bin/env python3
"""One-off helper: fetch full Crossref records (incl. abstract if deposited) for a
shortlist of DOIs, one at a time via the single-work endpoint, and print them for
manual review before hand-coding into seed_bibliography.csv. Not part of the
regular pipeline -- a scratch tool for this expansion pass."""
import re
import sys
import time
import json
import requests

EMAIL = "saber.naseralavi@gmail.com"
HEADERS = {"User-Agent": f"pavement-hybrid-review/1.0 (mailto:{EMAIL})"}


def get(doi):
    url = f"https://api.crossref.org/works/{doi}"
    for attempt in range(4):
        r = requests.get(url, headers=HEADERS, timeout=30)
        if r.status_code == 429:
            time.sleep(3 * (attempt + 1))
            continue
        r.raise_for_status()
        return r.json()["message"]
    return None


def main():
    dois = [l.strip() for l in open(sys.argv[1], encoding="utf-8") if l.strip()]
    results = []
    for i, doi in enumerate(dois, 1):
        try:
            m = get(doi)
        except Exception as exc:
            print(f"[{i}/{len(dois)}] ERROR {doi}: {exc}", file=sys.stderr)
            results.append({"doi": doi, "error": str(exc)})
            time.sleep(0.4)
            continue
        title = "; ".join(m.get("title") or [])
        abstract = re.sub(r"<[^>]+>", " ", m.get("abstract") or "").strip()
        container = "; ".join(m.get("container-title") or [])
        year = None
        for k in ("published", "published-print", "published-online", "issued"):
            dp = (m.get(k) or {}).get("date-parts")
            if dp and dp[0] and dp[0][0]:
                year = dp[0][0]
                break
        authors = "; ".join(
            f"{a.get('family','')}, {a.get('given','')}".strip(", ")
            for a in m.get("author", []) or [] if a.get("family")
        )
        cited = m.get("is-referenced-by-count", 0)
        results.append({
            "doi": doi, "title": title, "abstract": abstract, "venue": container,
            "year": year, "authors": authors, "cited_by_count": cited,
        })
        print(f"[{i}/{len(dois)}] {doi} :: {title[:80]} (abs: {len(abstract)} chars)", flush=True)
        time.sleep(0.4)
    with open(sys.argv[2], "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=1)
    print(f"\nwrote {len(results)} records to {sys.argv[2]}")


if __name__ == "__main__":
    main()
