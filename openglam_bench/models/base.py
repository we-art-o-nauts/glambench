"""Adapter protocol: every model is a callable that takes (task, prompt) and
returns the raw string output. Kept intentionally minimal so institutions can
plug in retrieval pipelines, rerankers, or containerised systems later.
"""

from __future__ import annotations

from typing import Protocol


class ModelAdapter(Protocol):
    name: str

    def generate(self, task: str, prompt: str) -> str: ...
