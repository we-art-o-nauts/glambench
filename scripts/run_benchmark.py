#!/usr/bin/env python3
"""Run OpenGLAM-Bench against a model and write results JSON.

Usage:
  python scripts/run_benchmark.py --model dummy --output ../results/dummy.json
  python scripts/run_benchmark.py --model openai-compatible --base-url http://localhost:8000/v1 \
      --name my-apertus --output ../results/apertus.json [--limit N] [--tasks reading,linking]
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from openglam_bench.dotenv import load_dotenv
from openglam_bench.models.dummy import DummyModel
from openglam_bench.models.openai_compatible import OpenAICompatibleModel
from openglam_bench.runner import run_all

# Fill os.environ from .env (shell wins). Never commit .env.
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", choices=["dummy", "openai-compatible"], required=True)
    parser.add_argument("--base-url", default=os.environ.get("OPENAI_BASE_URL", "http://localhost:8000/v1"))
    parser.add_argument("--name", default=os.environ.get("OPENAI_MODEL", "openai-compatible"), help="Model name/id for openai-compatible mode (env: OPENAI_MODEL)")
    parser.add_argument("--api-key-env", default=os.environ.get("OPENAI_API_KEY_ENV", "OPENAI_API_KEY"), help="Environment variable holding the API key (default: OPENAI_API_KEY)")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--tasks", default=None, help="Comma-separated subset, e.g. reading,linking")
    parser.add_argument("--quiet", action="store_true", help="Suppress per-item progress output")
    args = parser.parse_args()

    if args.model == "dummy":
        model = DummyModel()
    else:
        model = OpenAICompatibleModel(name=args.name, base_url=args.base_url, api_key_env=args.api_key_env)

    tasks = [t.strip() for t in args.tasks.split(",")] if args.tasks else None
    results = run_all(model, tasks=tasks, limit=args.limit, verbose=not args.quiet)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
