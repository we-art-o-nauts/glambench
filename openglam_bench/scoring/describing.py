"""Describing: generate catalogue metadata for a cultural object.

Expected model output: a JSON-ish dict or KEY: VALUE lines with the same keys
as gold["gold_fields"] (e.g. creator, date, material, title).
Metrics: field-level precision / recall / F1 over exact normalised matches,
and an abstention-aware "unsupported" flag if the model refuses.
"""

from __future__ import annotations

import json
import re

from ..textnorm import normalize_text

ABSTAIN_MARKERS = ("insufficient evidence", "no answer", "unsupported", "unknown")


def parse_fields(prediction: str) -> dict[str, str]:
    text = prediction.strip()
    if not text:
        return {}
    if text.startswith("{"):
        try:
            obj = json.loads(text)
            return {normalize_text(str(k)): normalize_text(str(v)) for k, v in obj.items()}
        except json.JSONDecodeError:
            return {}
    fields: dict[str, str] = {}
    for line in text.splitlines():
        m = re.match(r"^\s*([A-Za-z_][\w\- ]*)\s*[:=]\s*(.+?)\s*$", line)
        if m:
            fields[normalize_text(m.group(1))] = normalize_text(m.group(2))
    return fields


def is_abstention(prediction: str) -> bool:
    norm = normalize_text(prediction)
    return any(marker in norm for marker in ABSTAIN_MARKERS)


def score(prediction: str, gold: dict) -> dict:
    gold_fields = {normalize_text(str(k)): normalize_text(str(v)) for k, v in gold["gold_fields"].items()}
    if is_abstention(prediction):
        # Abstaining is correct only when the gold itself marks the field as unsupported.
        if gold.get("gold_status") == "insufficient_evidence":
            return {"field_precision": 1.0, "field_recall": 1.0, "field_f1": 1.0, "abstained": 1.0}
        return {"field_precision": 0.0, "field_recall": 0.0, "field_f1": 0.0, "abstained": 1.0}

    pred_fields = parse_fields(prediction)
    if not gold_fields:
        return {"field_precision": 0.0, "field_recall": 0.0, "field_f1": 0.0, "abstained": 0.0}

    hits = sum(1 for k, v in pred_fields.items() if k in gold_fields and gold_fields[k] == v)
    precision = hits / len(pred_fields) if pred_fields else 0.0
    recall = hits / len(gold_fields)
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "field_precision": round(precision, 4),
        "field_recall": round(recall, 4),
        "field_f1": round(f1, 4),
        "abstained": 0.0,
    }
