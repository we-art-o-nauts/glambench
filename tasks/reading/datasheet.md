# Reading Task Datasheet — OpenGLAM-Bench

## Purpose
OCR post-correction of historical documents: given raw OCR output (with long-s, ligature, encoding and misread-character errors typical of Fraktur/Kurrent/print), the model must reconstruct the intended historical transcription exactly — no modernising, no translating, nothing added or dropped. Text-proxy stand-in until document images are curated.

Difficulty strata via the `difficulty` field: easy (encoding artifacts), medium, hard (heavy corruption or long documents).

## Source
Synthetic placeholder seed data (CC0). Replace with curated records from partner GLAMs before any public release; track replacements in data/source_info.yaml.

## Licence & Rights
See ETHICS.md. Placeholder items are CC0 synthetic. Real items must record per-item licences.

## Difficulty Strata
Items carry an informal difficulty via note: script archaic / contested / etc. Stratify when curating.

## Known Gaps
Replace placeholders; add provenance chain fields; expand languages beyond de/fr/it placeholders.

## Evaluation
See task_spec.md and openglam_bench/scoring/reading.py.
