# Faithfulness Task Datasheet — OpenGLAM-Bench

## Purpose
Judge whether a claim is supported by the record: 'supported' or 'unsupported' (+ error type). 24 items, 12/12 balanced. Includes partial-truth traps (right creator wrong date; right century wrong precision), absence-as-fact items ('the record does not state...'), logical entailments (a range implies its superset), disputed-provenance cases, and rights misstatements.

## Source
Synthetic placeholder seed data (CC0). Replace with curated records from partner GLAMs before any public release; track replacements in data/source_info.yaml.

## Licence & Rights
See ETHICS.md. Placeholder items are CC0 synthetic. Real items must record per-item licences.

## Difficulty Strata
Items carry an informal difficulty via note: script archaic / contested / etc. Stratify when curating.

## Known Gaps
Replace placeholders; add provenance chain fields; expand languages beyond de/fr/it placeholders.

## Evaluation
See task_spec.md and openglam_bench/scoring/faithfulness.py.
