"""OpenAI-compatible chat completions adapter (works with any /v1/chat/completions
endpoint: OpenAI, vLLM, OpenRouter, self-hosted Apertus, etc.).

Uses stdlib urllib — no third-party dependencies. Reads credentials from the
environment. Never hard-code keys.
"""

from __future__ import annotations

import json
import os
import urllib.request


class OpenAICompatibleModel:
    def __init__(self, name: str, base_url: str, api_key_env: str = "OPENAI_API_KEY",
                 temperature: float = 0.0, timeout: int = 120):
        self.name = name
        self.base_url = base_url.rstrip("/")
        self.api_key_env = api_key_env
        self.temperature = temperature
        self.timeout = timeout

    def generate(self, task: str, prompt: str) -> str:
        api_key = os.environ.get(self.api_key_env, "")
        payload = {
            "model": self.name.split(":", 1)[-1],
            "messages": [
                {"role": "system", "content": (
                    "You are being evaluated on cultural-heritage collection work. "
                    "Answer strictly from the provided record. If the record does not "
                    "support a claim, say so instead of guessing.")},
                {"role": "user", "content": prompt},
            ],
            "temperature": self.temperature,
        }
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                **({"Authorization": f"Bearer {api_key}"} if api_key else {}),
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        return body["choices"][0]["message"]["content"]
