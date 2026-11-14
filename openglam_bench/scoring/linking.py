"""Linking: resolve a person / place / work to a Wikidata QID.

Expected model output: either a QID ("Q90"), "no answer", or a sentence from
which the first QID-like token is extracted.
Gold fields: gold_qid (string, or null) — null means "no answer exists".
Metrics: hits@1, MRR (rank of gold among candidates, exact-match case),
abstention correctness for no-answer cases.
"""

from __future__ import annotations

import re

from ..textnorm import normalize_text

QID_RE = re.compile(r"Q\d+", re.IGNORECASE)
NO_ANSWER_MARKERS = ("no answer", "insufficient", "unsupported", "unknown", "abstain")


def extract_qid(prediction: str):
    norm = normalize_text(prediction)
    if any(m in norm for m in NO_ANSWER_MARKERS):
        return None
    match = QID_RE.search(prediction.upper().replace(" ", ""))
    return match.group(0).upper() if match else None


def score(prediction: str, gold: dict) -> dict:
    gold_qid = gold.get("gold_qid")
    gold_qid = gold_qid.upper() if isinstance(gold_qid, str) else None
    pred_qid = extract_qid(prediction or "")
    candidates = [str(c.get("qid", "")).upper() for c in gold.get("candidates", [])]

    if gold_qid is None:
        # No answer exists: reward abstention.
        correct = 1.0 if pred_qid is None else 0.0
        return {"hits_at_1": correct, "mrr": correct, "abstention_correct": correct, "answered": 0.0 if pred_qid is None else 1.0}

    hit = 1.0 if pred_qid == gold_qid else 0.0
    if pred_qid is None:
        mrr = 0.0
    elif gold_qid in candidates:
        # Candidate list defines the possibility space; MRR over candidate rank.
        rank = candidates.index(gold_qid) + 1
        mrr = 1.0 / rank if pred_qid == gold_qid else 0.0
    else:
        mrr = hit
    return {"hits_at_1": hit, "mrr": round(mrr, 4), "abstention_correct": 0.0, "answered": 1.0}
