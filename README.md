# OpenGLAM-Bench

A living, open benchmark for AI in cultural heritage collections, built around what GLAM institutions actually need: truthful description, source-cited claims, respect for rights and licences, and the ability to say *"insufficient evidence"* instead of inventing heritage.

Created at **GLAMhack 2026** (Swiss Open Cultural Data Hackathon, 12–14 Nov 2026, Winterthur) run by the **Opendata.ch** association. See [`ETHICS.md`](../ETHICS.md) at the repository root for the ethical code adapted from the **Apertus Charter**.

_**Tech stack:** OpenCode, Apertus 1.5 70B (initial spec), Inkling 2 Small (scaffold), NeoVim (human-in-the-loop), Python, Manjaro Linux_

## Overview

Five tasks, built from real collection work rather than toy prompts:

| Task | Input | Output | Core metrics |
|---|---|---|---|
| `reading` | Historical document (text proxy until images are curated) | Transcription | CER/WER accuracy |
| `describing` | Object record fragment | Catalogue fields (KEY: VALUE / JSON) | Field-level precision/recall/F1 |
| `linking` | Mention + candidate Wikidata IDs | QID or *"no answer"* | Hits@1, MRR, abstention correctness |
| `translating` | Historical text (de/fr/it/de-ch) | Translation preserving meaning | Token-F1, key-term retention |
| `faithfulness` | Record + claim | *"supported"* / *"unsupported"* + error type | Accuracy, hallucination-detection F1 |

Design principles: evidence-grounded outputs, abstention is rewarded over guessing, localized multilingual data over translated English, multi-metric reporting (never one score), contamination awareness, community governance.

## Repository layout

```
openglam_bench/
├── openglam_bench/          # the benchmark package (stdlib only)
│   ├── scoring/             # reading, describing, linking, translating, faithfulness
│   ├── models/              # dummy adapter + OpenAI-compatible adapter
│   ├── runner.py            # load test data → prompt model → score → JSON
│   ├── leaderboard.py       # multi-metric ranking (mean rank, no blended score)
│   ├── textnorm.py          # CER/WER/token-F1/Levenshtein from scratch
│   └── dotenv.py            # minimal .env loader (shell env wins)
├── tasks/<task>/            # datasheet.md + test_data/test.jsonl per task
├── data/ckan/               # CKAN snapshot + recommendations (metadata only)
├── scripts/
│   ├── run_benchmark.py     # evaluate a model
│   ├── make_leaderboard.py  # build CSV + HTML leaderboard
│   └── fetch_ckan_datasets.py  # refresh OpenGLAM dataset list + recommendations
├── tests/                   # smoke/unit tests (pytest)
└── results/                 # per-model result JSON (gitignored)
```

## Requirements

- Python ≥ 3.10. The benchmark itself has **zero third-party dependencies** (HTTP via `urllib`; metrics implemented from scratch).
- [`uv`](https://docs.astral.sh/uv/) (optional, for tests) — or any environment with `pytest`.

## Quickstart (offline, no API key)

```bash
cd openglam_bench
python3 scripts/run_benchmark.py --model dummy --output results/dummy.json
python3 scripts/make_leaderboard.py --results results --out leaderboard
uv run --with pytest python -m pytest tests/ -q   # or: python -m pytest tests/
```

## Running against an LLM API

### 1. Configure `.env`

```bash
cp .env.template .env
# edit .env
```

`.env` is gitignored. Existing shell variables win over `.env` values. **Never commit `.env` or paste keys into issues/logs.**

| Variable | Meaning | Example |
|---|---|---|
| `OPENAI_BASE_URL` | OpenAI-compatible `/v1` endpoint | `http://localhost:8000/v1` (self-hosted), `https://api.openai.com/v1`, `https://openrouter.ai/api/v1` |
| `OPENAI_MODEL` | Model id exactly as the endpoint expects | `swiss-ai/Apertus-8B-Instruct-2509` (local vLLM), `gpt-4.1-mini` |
| `OPENAI_API_KEY` | Key for that endpoint | leave empty for unauthenticated local servers |
| `OPENAI_API_KEY_ENV` | *(optional)* read the key from a different variable instead | `MY_PROVIDER_KEY` |
| `GLAMBENCH_RATE_LIMIT` | Max LLM API requests per minute, default `15`; `0` disables (rolling window; retries count too) | `60` |

Works with **any** OpenAI-compatible `/v1/chat/completions` server: self-hosted open-weight models (including **Apertus** served via vLLM/sglang at `localhost:8000/v1`), OpenRouter, OpenAI, or gateway proxies.

### 2. Run the benchmark

```bash
python3 scripts/run_benchmark.py --model openai-compatible --output results/my-model.json
# subset of tasks / quick smoke:
python3 scripts/run_benchmark.py --model openai-compatible --tasks reading,linking --limit 10 --output results/smoke.json
```

`--base-url`, `--name`, `--api-key-env` override the `.env` values; `--tasks` takes a comma-separated subset; `--limit N` runs the first N items per task; `--rate-limit N` overrides `GLAMBENCH_RATE_LIMIT` (default 15 req/min, `0` to disable). Each output JSON contains per-item outputs + metrics and a per-task summary.

### 3. Update the leaderboard

```bash
python3 scripts/make_leaderboard.py --results results --out leaderboard
# then regenerate the website's embedded pages:
python3 ../site/build.py
```

Multi-metric by design: CER/WER accuracy, field F1, Hits@1/MRR, token-F1/key-term retention, hallucination F1, plus `mean_rank`. No single blended score.

## Test data and licences

- `tasks/*/test_data/test.jsonl` ships **synthetic CC0 placeholders** (clearly marked `synthetic://`). They exist to pin the harness, not to measure models.
- Real records will be added per institution after rights review — see `ETHICS.md` (rights first: no dataset enters the benchmark until its licence is verified) and `scripts/fetch_ckan_datasets.py`, which fetches the OpenGLAM dataset list from https://opendata.swiss (metadata only, never payloads) and ranks candidates per task.

## Contributing

- Tasks, ground truth, scoring, and leaderboard changes all require **domain-expert + community review** (GLAMhack / Opendata.ch). Technical and ethical changes are reviewed separately.
- Before opening anything, read `ETHICS.md` — abstention scoring, evidence-citation, and contamination rules are load-bearing, not decoration.
- Site development: `python3 site/build.py` regenerates the embedded leaderboard/dataset pages.
