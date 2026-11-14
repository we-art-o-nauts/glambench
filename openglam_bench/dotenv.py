"""Minimal .env loader (stdlib only).

Shell environment wins over .env values — matching the CulturalRiddles convention.
Comments (#), blank lines, and `export KEY=value` prefixes are supported.
Never commit .env. Never print loaded values.
"""

from __future__ import annotations

import os
from pathlib import Path


def load_dotenv(path: Path) -> int:
    if not path.exists():
        return 0
    loaded = 0
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("export "):
            line = line[len("export "):].lstrip()
        key, sep, value = line.partition("=")
        if not sep:
            continue
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        if key and key not in os.environ:
            os.environ[key] = value
            loaded += 1
    return loaded
