"""Offline dummy model for smoke tests and CI. Not a benchmark candidate."""

from __future__ import annotations


class DummyModel:
    name = "dummy:local"

    def generate(self, task: str, prompt: str) -> str:
        # Deliberately mediocre, deterministic output. Faithfulness/linking
        # cases mostly abstain, which the scorers reward.
        if task == "describing":
            return "title: unknown\n"
        if task == "linking":
            return "no answer"
        if task == "faithfulness":
            return "insufficient evidence"
        if task == "translating":
            return "[untranslated] " + prompt[:200]
        return prompt[:200]  # reading: echo the prompt (usually wrong)
