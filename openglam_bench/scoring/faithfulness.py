"""Faithfulness: judge whether a claim about a cultural object is supported by the record.

Expected model output: "supported" or "unsupported" (optionally with an error
type such as invented_date / false_provenance / invented_creator / rights_misstatement),
plus ideally the citation to the record field.

Per-item metrics (0/1):
  accuracy            — verdict matches gold
  abstained           — model refused to judge
  unsupported_caught  — gold is unsupported and model caught it
  unsupported_missed  — gold is unsupported and model missed it
  false_alarm         — gold is supported and model flagged it anyway
  error_type_accuracy — exact error_type match (only when both are unsupported)

Corpus-level hallucination-detection F1 is computed in aggregate(), not per item.
"""

from __future__ import annotations

from ..textnorm import normalize_text

SUPPORTED_MARKERS = ("supported", "correct", "accurate")
UNSUPPORTED_MARKERS = ("unsupported", "not supported", "invented", "false", "fabricat")
ABSTAIN_MARKERS = ("insufficient evidence", "not enough", "no answer", "cannot determine", "abstain")
ERROR_TYPES = ("invented_date", "invented_creator", "false_provenance", "rights_misstatement", "invented_place", "other")


def classify(prediction: str):
    norm = normalize_text(prediction or "")
    if any(m in norm for m in ABSTAIN_MARKERS):
        supported = None
    elif any(m in norm for m in UNSUPPORTED_MARKERS):
        supported = False
    elif any(m in norm for m in SUPPORTED_MARKERS):
        supported = True
    else:
        supported = None
    lowered = (prediction or "").lower()
    error_type = next((et for et in ERROR_TYPES if et.replace("_", " ") in lowered or et in lowered), None)
    return supported, error_type


def score(prediction: str, gold: dict) -> dict:
    gold_supported = bool(gold["supported"])
    gold_error = str(gold.get("error_type", "correct" if gold_supported else "other"))

    pred_supported, pred_error = classify(prediction)

    abstained = 1.0 if pred_supported is None else 0.0
    if pred_supported is None:
        return {"accuracy": 0.0, "abstained": 1.0, "unsupported_caught": 0.0,
                "unsupported_missed": 0.0 if gold_supported else 1.0,
                "false_alarm": 0.0, "error_type_accuracy": 0.0}

    accuracy = 1.0 if pred_supported == gold_supported else 0.0
    unsupported_caught = 1.0 if (not gold_supported) and (not pred_supported) else 0.0
    unsupported_missed = 1.0 if (not gold_supported) and pred_supported else 0.0
    false_alarm = 1.0 if gold_supported and not pred_supported else 0.0
    error_type_accuracy = 0.0
    if not gold_supported and not pred_supported:
        error_type_accuracy = 1.0 if pred_error == gold_error else 0.0

    return {
        "accuracy": accuracy,
        "abstained": abstained,
        "unsupported_caught": unsupported_caught,
        "unsupported_missed": unsupported_missed,
        "false_alarm": false_alarm,
        "error_type_accuracy": round(error_type_accuracy, 4),
    }


def aggregate(records: list[dict]) -> dict:
    tp = sum(r["unsupported_caught"] for r in records)
    fn = sum(r["unsupported_missed"] for r in records)
    fp = sum(r["false_alarm"] for r in records)
    precision = tp / (tp + fp) if (tp + fp) else 0.0
    recall = tp / (tp + fn) if (tp + fn) else 0.0
    f1 = 2 * precision * recall / (precision + recall) if (precision + recall) else 0.0
    return {"hallucination_precision": round(precision, 4),
            "hallucination_recall": round(recall, 4),
            "hallucination_f1": round(f1, 4)}
