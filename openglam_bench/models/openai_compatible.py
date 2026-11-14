"""OpenAI-compatible chat completions adapter (works with any /v1/chat/completions
endpoint: OpenAI, vLLM, OpenRouter, self-hosted Apertus, etc.).

Uses stdlib urllib — no third-party dependencies. Reads credentials from the
environment. Never hard-code keys.
"""

from __future__ import annotations

import json
import os
import time
import urllib.error
import urllib.request

# Server-side / transient conditions worth retrying; 4xx client errors are fatal immediately.
RETRIABLE_HTTP = {408, 409, 425, 429} | set(range(500, 600))


class OpenAICompatibleModel:
    def __init__(self, name: str, base_url: str, api_key_env: str = "OPENAI_API_KEY",
                 temperature: float = 0.0, timeout: int = 120, max_attempts: int = 3,
                 user_agent: str = "GLAMbench/0.1 (OpenGLAM-Bench; opendata.ch)"):
        self.name = name
        self.base_url = base_url.rstrip("/")
        self.api_key_env = api_key_env
        self.temperature = temperature
        self.timeout = timeout
        self.max_attempts = max_attempts
        self.user_agent = user_agent

    def _request_once(self, payload: dict) -> str:
        api_key = os.environ.get(self.api_key_env, "")
        req = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                # WAFs (e.g. PublicAI's Cloudflare) 403 the default Python-urllib UA.
                "User-Agent": self.user_agent,
                **({"Authorization": f"Bearer {api_key}"} if api_key else {}),
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            body = json.loads(resp.read().decode("utf-8"))
        return body["choices"][0]["message"]["content"]

    def generate(self, task: str, prompt: str) -> str:
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
        last_error = ""
        for attempt in range(1, self.max_attempts + 1):
            try:
                return self._request_once(payload)
            except urllib.error.HTTPError as e:
                detail = e.read().decode("utf-8", errors="replace")[:300]
                if e.code not in RETRIABLE_HTTP:
                    raise RuntimeError(f"LLM endpoint returned HTTP {e.code} for {self.name} "
                                       f"(not retrying — client error): {detail}") from e
                last_error = f"HTTP {e.code}: {detail}"
            except (TimeoutError, urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
                # Timeouts, connection failures, and malformed/partial responses are transient.
                last_error = f"{type(e).__name__}: {e}"
            if attempt < self.max_attempts:
                wait = 2 ** attempt
                print(f"      request failed for {self.name} ({last_error}) — "
                      f"retrying {attempt}/{self.max_attempts - 1} in {wait}s", flush=True)
                time.sleep(wait)
        raise RuntimeError(f"LLM endpoint failed {self.max_attempts} times in a row for {self.name}: {last_error}")
