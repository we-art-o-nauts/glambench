"""Lightweight edit distance and text normalisation used by the scorers.

Implemented from scratch (pure stdlib) so the benchmark runs offline with no
third-party dependencies.
"""

from __future__ import annotations

import re
import unicodedata


def levenshtein(a: str, b: str) -> int:
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        curr = [i]
        for j, cb in enumerate(b, 1):
            curr.append(min(curr[-1] + 1, prev[j] + 1, prev[j - 1] + (ca != cb)))
        prev = curr
    return prev[-1]


def normalize_text(text: str, *, casefold: bool = True, strip_accents: bool = True) -> str:
    text = unicodedata.normalize("NFC", text)
    if strip_accents:
        text = "".join(
            ch for ch in unicodedata.normalize("NFD", text) if unicodedata.category(ch) != "Mn"
        )
    if casefold:
        text = text.casefold()
    text = re.sub(r"\s+", " ", text).strip()
    return text


def char_error_rate(hypothesis: str, reference: str) -> float:
    if not reference:
        return 0.0 if not hypothesis else 1.0
    return levenshtein(hypothesis, reference) / len(reference)


def word_error_rate(hypothesis: str, reference: str) -> float:
    hyp_words = hypothesis.split()
    ref_words = reference.split()
    if not ref_words:
        return 0.0 if not hyp_words else 1.0
    return _word_lev(hyp_words, ref_words) / len(ref_words)


def _word_lev(a: list[str], b: list[str]) -> int:
    if not a:
        return len(b)
    prev = list(range(len(b) + 1))
    for i, wa in enumerate(a, 1):
        curr = [i]
        for j, wb in enumerate(b, 1):
            curr.append(min(curr[-1] + 1, prev[j] + 1, prev[j - 1] + (wa != wb)))
        prev = curr
    return prev[-1]


def token_f1(hypothesis: str, reference: str) -> float:
    hyp = normalize_text(hypothesis).split()
    ref = normalize_text(reference).split()
    if not hyp and not ref:
        return 1.0
    if not hyp or not ref:
        return 0.0
    ref_counts: dict[str, int] = {}
    for tok in ref:
        ref_counts[tok] = ref_counts.get(tok, 0) + 1
    common = 0
    for tok in hyp:
        if ref_counts.get(tok, 0) > 0:
            common += 1
            ref_counts[tok] -= 1
    if common == 0:
        return 0.0
    precision = common / len(hyp)
    recall = common / len(ref)
    return 2 * precision * recall / (precision + recall)
