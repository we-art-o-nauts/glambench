#!/usr/bin/env python3
"""Build the leaderboard CSV + HTML from a results directory.

Usage: python scripts/make_leaderboard.py --results ../results --out ../leaderboard
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from openglam_bench.leaderboard import load_results, rank_models, write_csv, write_html


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--results", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    args.out.mkdir(parents=True, exist_ok=True)
    results = load_results(args.results)
    rows = rank_models(results)
    write_csv(rows, args.out / "leaderboard.csv")
    write_html(rows, args.out / "index.html")
    print(f"Wrote {args.out/'leaderboard.csv'} and {args.out/'index.html'} ({len(rows)} models)")


if __name__ == "__main__":
    main()
