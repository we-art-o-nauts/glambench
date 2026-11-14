"""Translating: historical text translation preserving meaning and key terms.

Expected model output: the translated text.
Gold fields: gold_translation, key_terms (list of terms that must survive,
already in the target language).
Metrics: token-F1 against the reference, key-term retention, length ratio sanity.

Note (documented in ETHICS.md): overlap metrics are a proxy for meaning
preservation. Native-speaker review remains the arbiter for release decisions.
"""

from __future__ import annotations

from ..textnorm import normalize_text, token_f1


def score(prediction: str, gold: dict) -> dict:
    prediction = prediction or ""
    reference = gold["gold_translation"]
    tf1 = token_f1(prediction, reference)

    key_terms = [normalize_text(str(t)) for t in gold.get("key_terms", [])]
    norm_pred = normalize_text(prediction)
    if key_terms:
        retained = sum(1 for t in key_terms if t and t in norm_pred)
        term_retention = retained / len(key_terms)
    else:
        term_retention = 1.0

    ref_len, pred_len = len(reference.split()), len(prediction.split())
    length_ratio = (min(ref_len, pred_len) / max(ref_len, pred_len)) if max(ref_len, pred_len) else 1.0

    return {
        "token_f1": round(tf1, 4),
        "key_term_retention": round(term_retention, 4),
        "length_ratio": round(length_ratio, 4),
    }
