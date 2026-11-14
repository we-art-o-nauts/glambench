"""Reading: transcribe a historical document image (or its text proxy).

Expected model output: the transcription as plain text.
Gold fields: gold_text, language, script.
Metrics: character error rate (inverted), word error rate (inverted).
"""

from __future__ import annotations

from ..textnorm import char_error_rate, word_error_rate, normalize_text


def score(prediction: str, gold: dict) -> dict:
    reference = gold["gold_text"]
    # Tolerate the model echoing nothing at all.
    prediction = prediction if prediction is not None else ""
    cer = char_error_rate(normalize_text(prediction), normalize_text(reference))
    wer = word_error_rate(normalize_text(prediction), normalize_text(reference))
    return {
        "cer": round(cer, 4),
        "wer": round(wer, 4),
        "char_accuracy": round(max(0.0, 1.0 - cer), 4),
        "word_accuracy": round(max(0.0, 1.0 - wer), 4),
    }
