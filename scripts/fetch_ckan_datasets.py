#!/usr/bin/env python3
"""Fetch the OpenGLAM dataset list from opendata.swiss (CKAN) and recommend
datasets for the GLAMbench benchmark, based on file types, access patterns,
licences and metadata richness. Snapshot is saved for reproducibility;
recommendations are written to Markdown + JSON for review by curators.

Usage:
  python scripts/fetch_ckan_datasets.py                 # fetch + analyse + report
  python scripts/fetch_ckan_datasets.py --offline       # analyse existing latest.json
  python scripts/fetch_ckan_datasets.py --json-only     # skip Markdown report

Nothing is downloaded beyond dataset *metadata* (CKAN package records).
No collection data files are fetched — that decision stays with curators.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.request
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
CKAN_DIR = REPO_ROOT / "data" / "ckan"
API = "https://opendata.swiss/api/3/action/package_search"
USER_AGENT = "GLAMbench-research/0.1 (OpenGLAM-Bench; opendata.ch hackathon 2026-11-14)"

# Formats that indicate direct image/scan payloads (reading task candidates).
IMAGE_FORMATS = {"TIFF", "TIF", "JPEG", "JPG", "PNG", "JP2", "IIIF", "IMAGE"}
# Structured export formats (describing task candidates).
STRUCTURED_FORMATS = {"CSV", "XML", "JSON", "XLS", "XLSX", "TSV", "RDF", "JSON-LD", "PARQUET", "SQL", "DB", "SQLITE"}
# Service-style access (linking / interoperability candidates).
SERVICE_FORMATS = {"SERVICE", "SPARQL", "API", "OAI-PMH", "WEBSERVICE"}
ARCHIVE_FORMATS = {"ZIP", "TAR", "GZ", "7Z"}
DOC_FORMATS = {"PDF"}
OPEN_LICENSE_RE = re.compile(r"(cc0|cc-by|cc-by-sa|odc-by|pddl|public|terms_by|terms-by|by-1\.0|cc-by-1\.0)", re.I)
KEYWORD_HINTS = {
    "reading": ["manuscript", "e-manuscripta", "prints", "drucke", "briefe", "letters", "handschrift", "volltext", "fulltext", "digitized", "faksimile", "scan", "photograph", "dia", "slide", "plakat", "poster"],
    "describing": ["csv", "export", "katalog", "catalog", "inventar", "inventory", "metadaten", "metadata", "datastore", "tabelle", "table"],
    "linking": ["sparql", "linked open data", "linked data", "linked art", "iiif", "wikidata", "rdf", "endpoint", "loh", "authority", "sameas"],
    "translating": ["mehrsprachig", "multilingual", "fr", "it", "de", "romansh", "sursilv", "lo reno"],
    "faithfulness": ["provenance", "provenienz", "rights", "recht", "inventar", "attribution", "zuschreibung", "lizenz", "license", "herkunft", "restitution"],
}


def fetch_all(org: str, rows: int = 100) -> list[dict]:
    results, start = [], 0
    while True:
        url = f"{API}?fq=organization:{org}&rows={rows}&start={start}"
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            payload = json.load(resp)
        batch = payload["result"]["results"]
        results.extend(batch)
        if len(results) >= payload["result"]["count"] or not batch:
            break
        start += len(batch)
    return results


def first_lang(value) -> str:
    if isinstance(value, dict):
        for lang in ("en", "de", "fr", "it", "gsw", "rm"):
            if value.get(lang):
                return str(value[lang])
        return str(next(iter(value.values()), ""))
    return str(value or "")


def merged_keywords(ds: dict) -> set[str]:
    kw = ds.get("keywords") or {}
    merged: set[str] = set()
    if isinstance(kw, dict):
        for lang_vals in kw.values():
            merged.update(str(k).lower() for k in (lang_vals or []))
    elif isinstance(kw, list):
        merged.update(str(k).lower() for k in kw)
    return merged


def resource_info(ds: dict) -> dict:
    formats, urls, licences, has_datastore = [], 0, [], False
    for res in ds.get("resources", []):
        fmt = (res.get("format") or "UNKNOWN").upper().strip()
        formats.append(fmt)
        if res.get("url") or res.get("download_url"):
            urls += 1
        lic = res.get("license") or ""
        if lic:
            licences.append(lic)
        if res.get("datastore_active"):
            has_datastore = True
    return {"formats": formats, "urls": urls, "resource_licenses": licences, "datastore_active": has_datastore}


def licence_flag(ds: dict, rinfo: dict) -> str:
    lic = ds.get("license_id") or ""
    haystacks = [lic, ds.get("license_title", "")] + rinfo["resource_licenses"]
    for h in haystacks:
        if h and OPEN_LICENSE_RE.search(str(h).lower()):
            return "open-ish"
    return "unknown/not-stated"


def score_dataset(ds: dict) -> dict:
    rinfo = resource_info(ds)
    formats = set(rinfo["formats"])
    kw = merged_keywords(ds)
    kw_blob = " ".join(sorted(kw))
    languages = {l for l in (ds.get("language") or []) if l}
    reasons: dict[str, list[str]] = {t: [] for t in KEYWORD_HINTS}
    scores = {t: 0 for t in KEYWORD_HINTS}

    def add(task, pts, reason):
        scores[task] += pts
        reasons[task].append(reason)

    # File-type signals.
    if formats & IMAGE_FORMATS:
        add("reading", 3, f"image/scan formats: {sorted(formats & IMAGE_FORMATS)}")
    if formats & DOC_FORMATS:
        add("reading", 2, "PDF resources (scanned documents possible)")
    if formats & STRUCTURED_FORMATS:
        add("describing", 3, f"structured formats: {sorted(formats & STRUCTURED_FORMATS)}")
    if formats & SERVICE_FORMATS:
        add("linking", 3, f"service/linked-data access: {sorted(formats & SERVICE_FORMATS)}")
        add("faithfulness", 1, "machine-readable service endpoint (evidence traceability)")
    if formats & ARCHIVE_FORMATS:
        add("reading", 1, "archive bundles (bulk scans possible — needs curator review)")
        add("describing", 1, "archive bundles may hold structured exports")
    if rinfo["datastore_active"]:
        add("describing", 2, "CKAN datastore active (queryable structured records)")

    # Keyword signals.
    for task, hints in KEYWORD_HINTS.items():
        hits = [h for h in hints if h in kw_blob]
        if hits:
            add(task, min(3, len(hits)), f"keywords matched: {hits}")

    # Language signals: TRULY multilingual collections help translation testing.
    if len(languages) >= 2:
        add("translating", 3, f"multilingual dataset languages: {sorted(languages)}")
    elif languages:
        add("translating", 1, f"single declared language: {sorted(languages)}")

    # Licence transparency helps rights-aware tasks.
    lic = licence_flag(ds, rinfo)
    if lic == "open-ish":
        add("faithfulness", 1, "explicit licence statement on dataset/resources")

    return {
        "name": ds.get("name"),
        "title": first_lang(ds.get("title")),
        "organization": first_lang((ds.get("organization") or {}).get("title") if isinstance(ds.get("organization"), dict) else ds.get("organization")),
        "languages": sorted(languages),
        "formats": sorted(formats),
        "n_resources": len(ds.get("resources", [])),
        "n_linked_urls": rinfo["urls"],
        "license": lic,
        "url": f"https://opendata.swiss/en/dataset/{ds.get('name')}",
        "scores": scores,
        "reasons": reasons,
    }


def render_markdown(entries: list[dict], total: int) -> str:
    tasks = ["reading", "describing", "linking", "translating", "faithfulness"]
    lines = [
        "# OpenGLAM-Bench Dataset Recommendations (opendata.swiss CKAN)",
        "",
        f"Generated from the organization `openglam` CKAN package list — **{total} datasets**, snapshot for {date.today().isoformat()}.",
        "Only dataset *metadata* was retrieved; no collection files were downloaded. All candidates require curator/individual-institution sign-off and licence review before use.",
        "",
        "Scoring is a heuristic triage, not a judgement of quality or openness. A dataset with no score may still be excellent; check the task datasheets for what each task needs.",
        "",
    ]
    for task in tasks:
        ranked = sorted(entries, key=lambda e: e["scores"][task], reverse=True)
        ranked = [e for e in ranked if e["scores"][task] > 0]
        lines += [f"## {task.capitalize()}", ""]
        if not ranked:
            lines += ["_No candidate matched the file-type/keyword heuristics._", ""]
            continue
        lines += ["| Score | Dataset | Licence | Formats | Why |", "|---|---|---|---|---|"]
        for e in ranked[:15]:
            why = "; ".join(e["reasons"][task]) or "—"
            why = why.replace("|", "\\|")
            lines.append(f"| {e['scores'][task]} | [{e['title']}]({e['url']}) | {e['license']} | {', '.join(e['formats']) or '—'} | {why} |")
        lines.append("")
    lines += [
        "## Method notes",
        "",
        "- Scores combine file-type formats (max 3), keyword hints (max 3), language multiplicity (max 3) and licence transparency (max 1).",
        "- `SERVICE`/`SPARQL`/`API` endpoints score for linking; `CSV`/`XML`/`JSON`/datastore score for describing; `TIFF`/scans/`PDF` score for reading.",
        "- Datasets without declared licences are flagged `unknown/not-stated` — they are not excluded, but must not be used until rights are confirmed.",
        "- Re-run this script after CKAN updates to refresh the snapshot; compare `data/ckan/latest.json` between releases to track changes.",
    ]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--organization", default="openglam")
    parser.add_argument("--offline", action="store_true", help="Analyse data/ckan/latest.json instead of fetching")
    parser.add_argument("--json-only", action="store_true", help="Skip the Markdown report")
    args = parser.parse_args()

    CKAN_DIR.mkdir(parents=True, exist_ok=True)
    latest = CKAN_DIR / "latest.json"

    if args.offline:
        dataset_list = json.loads(latest.read_text(encoding="utf-8"))
    else:
        dataset_list = fetch_all(args.organization)
        snapshot = CKAN_DIR / f"openglam_datasets_{date.today().isoformat()}.json"
        snapshot.write_text(json.dumps(dataset_list, ensure_ascii=False, indent=2), encoding="utf-8")
        latest.write_text(json.dumps(dataset_list, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"Fetched {len(dataset_list)} datasets -> {snapshot}")

    entries = [score_dataset(ds) for ds in dataset_list]
    (CKAN_DIR / "recommendations.json").write_text(json.dumps(entries, ensure_ascii=False, indent=2), encoding="utf-8")
    if not args.json_only:
        report = render_markdown(entries, len(entries))
        (CKAN_DIR / "recommendations.md").write_text(report, encoding="utf-8")
        print(f"Wrote {CKAN_DIR/'recommendations.md'} and recommendations.json")


if __name__ == "__main__":
    main()
