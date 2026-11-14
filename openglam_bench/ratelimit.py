"""Simple rolling-window rate limiter for API calls.

Default: 15 requests per minute (e.g. PublicAI free-tier chat endpoint).
Set to 0 to disable. Override per run with --rate-limit
"""

from __future__ import annotations

import time


class RateLimiter:
    def __init__(self, per_minute: int = 15, window_seconds: float = 60.0):
        self.per_minute = per_minute
        self.window = window_seconds
        self._calls: list[float] = []

    def wait(self) -> None:
        if self.per_minute <= 0:
            return
        while True:
            now = time.monotonic()
            self._calls = [t for t in self._calls if now - t < self.window]
            if len(self._calls) < self.per_minute:
                self._calls.append(time.monotonic())
                return
            sleep_for = self.window - (now - self._calls[0]) + 0.05
            time.sleep(max(sleep_for, 0.05))
