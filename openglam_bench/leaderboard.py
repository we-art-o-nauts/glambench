"""Leaderboard: aggregate per-model result JSON files into a ranking table.

Multi-metric by design (see ETHICS.md): every metric is reported separately,
plus a mean rank across tasks. No single blended score is produced.
Higher is better except cer/wer (lower is better), which are inverted on input.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

HIGHER_BETTER = {
    "reading": ["char_accuracy", "word_accuracy"],
    "describing": ["field_precision", "field_recall", "field_f1"],
    "linking": ["hits_at_1", "mrr", "abstention_correct"],
    "translating": ["token_f1", "key_term_retention", "length_ratio"],
    "faithfulness": ["accuracy", "hallucination_f1", "error_type_accuracy"],
}


def load_results(results_dir: Path) -> list[dict]:
    out = []
    for path in sorted(results_dir.glob("*.json")):
        with path.open(encoding="utf-8") as fh:
            out.append(json.load(fh))
    return out


def rank_models(results: list[dict]) -> list[dict]:
    rows = []
    for result in results:
        model = result.get("model", "unknown")
        row = {"model": model}
        for task, metric_keys in HIGHER_BETTER.items():
            task_summary = result.get(task, {}).get("summary", {})
            for key in metric_keys:
                row[f"{task}.{key}"] = task_summary.get(key)
        rows.append(row)

    # Mean rank per metric column (1 = best).
    metric_cols = [c for c in rows[0] if c != "model"] if rows else []
    rank_sums = {i: 0.0 for i in range(len(rows))}
    for col in metric_cols:
        values = [r[col] for r in rows]
        present = [(i, v) for i, v in enumerate(values) if v is not None]
        if not present:
            continue
        for rank, (i, _) in enumerate(sorted(present, key=lambda iv: iv[1], reverse=True), 1):
            rank_sums[i] += rank
    for i, row in enumerate(rows):
        row["mean_rank"] = round(rank_sums[i] / max(len(metric_cols), 1), 3)
    return sorted(rows, key=lambda r: r["mean_rank"])


def write_csv(rows: list[dict], path: Path) -> None:
    if not rows:
        return
    fieldnames = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_html(rows: list[dict], path: Path) -> None:
    if not rows:
        path.write_text("<p>No results yet.</p>", encoding="utf-8")
        return
    cols = list(rows[0].keys())
    thead = "".join(f"<th>{c}</th>" for c in cols)
    trs = []
    for row in rows:
        cells = "".join(f"<td>{row[c] if row[c] is not None else '—'}</td>" for c in cols)
        trs.append(f"<tr>{cells}</tr>")
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>OpenGLAM-Bench Leaderboard</title>
<style>body{{font-family:system-ui,sans-serif;margin:2rem}}table{{border-collapse:collapse}}
th,td{{border:1px solid #ccc;padding:.4rem .8rem;font-size:.9rem}}th{{background:#f2efe9}}
tr:nth-child(even){{background:#fafafa}}</style></head>
<body><h1>OpenGLAM-Bench Leaderboard</h1>
<p>Created at the Opendata.ch Open Cultural Data Hackathon, Winterthur, 2026-11-14.
Multi-metric reporting — see ETHICS.md. Scores are meaningful only for the dated test-set version.</p>
<table><thead><tr>{thead}</tr></thead><tbody>{''.join(trs)}</tbody></table>
</body></html>"""
    path.write_text(html, encoding="utf-8")
