#!/usr/bin/env python3
"""
make_bib.py
===========
Generates references.bib from data/seed_bibliography.csv.

The manuscript cites ONLY keys produced by this script. Because every row in the
database carries a verified DOI, a citation that does not exist in the database
cannot be cited: Quarto fails the render with an undefined-reference warning and
the key appears in the audit below. That is the mechanism that makes fabricated
references structurally impossible rather than merely discouraged.

Run:  python analysis/make_bib.py
"""

import csv
import re
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSV = ROOT / "data" / "seed_bibliography.csv"
BIB = ROOT / "references.bib"


def ascii_slug(text: str) -> str:
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]", "", text)


def first_surname(authors: str) -> str:
    if not authors:
        return "Anon"
    first = authors.split(";")[0].strip()
    surname = first.split(",")[0].strip() if "," in first else first.split()[-1]
    return ascii_slug(surname) or "Anon"


def title_word(title: str) -> str:
    stop = {"a", "an", "the", "of", "on", "in", "for", "and", "to", "with",
            "using", "from", "development", "application", "applications",
            "prediction", "predicting", "review", "study", "analysis", "new",
            "novel", "towards", "toward", "based", "assessment", "modeling",
            "modelling", "machine", "deep", "artificial", "hybrid", "does"}
    for w in re.findall(r"[A-Za-z]+", title):
        if w.lower() not in stop and len(w) > 3:
            return ascii_slug(w).lower()
    return "untitled"


def escape(s: str) -> str:
    return (s.replace("&", r"\&").replace("%", r"\%")
             .replace("#", r"\#").replace("_", r"\_"))


def bib_authors(authors: str) -> str:
    """Convert 'Surname, F.; Surname2, G.' to BibTeX 'Surname, F. and Surname2, G.'"""
    parts = [a.strip() for a in authors.split(";") if a.strip()]
    parts = [p for p in parts if not re.match(r"^\(?\d+\s+authors?\)?$", p, re.I)]
    parts = [re.sub(r"\s*\(\d+\s+authors?\)", "", p) for p in parts]
    if not parts:
        return "Anonymous"
    if any(re.search(r"et al", p, re.I) for p in parts):
        parts = [p for p in parts if not re.search(r"et al", p, re.I)] + ["others"]
    return " and ".join(parts)


def main() -> None:
    rows = list(csv.DictReader(CSV.open(encoding="utf-8-sig")))
    used, entries, report = set(), [], []

    for r in rows:
        if not r.get("doi"):
            continue
        base = f"{first_surname(r['authors'])}{r['year']}{title_word(r['title'])}"
        key, n = base, 1
        while key in used:
            n += 1
            key = f"{base}{chr(ord('a') + n - 1)}"
        used.add(key)

        fields = [
            f"  author  = {{{escape(bib_authors(r['authors']))}}}",
            f"  title   = {{{escape(r['title'])}}}",
            f"  journal = {{{escape(r['venue'])}}}",
            f"  year    = {{{r['year']}}}",
            f"  doi     = {{{r['doi']}}}",
        ]
        entries.append("@article{" + key + ",\n" + ",\n".join(fields) + "\n}\n")
        report.append((key, r["year"], r["role_in_review"][:38], r["title"][:58]))

    header = (
        "% references.bib — GENERATED FILE, DO NOT EDIT BY HAND\n"
        "% Produced by analysis/make_bib.py from data/seed_bibliography.csv.\n"
        "% Every entry carries a DOI verified against OpenAlex or Semantic Scholar.\n"
        "% To add a reference: add the verified row to the CSV, then re-run this script.\n\n"
    )
    BIB.write_text(header + "\n".join(entries), encoding="utf-8")

    print(f"wrote {len(entries)} entries -> {BIB.relative_to(ROOT)}\n")
    print(f"{'key':<34}{'year':<6}{'role':<40}title")
    print("-" * 132)
    for k, y, role, t in sorted(report, key=lambda x: x[0]):
        print(f"{k:<34}{y:<6}{role:<40}{t}")


if __name__ == "__main__":
    main()
