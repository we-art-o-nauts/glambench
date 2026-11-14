# ETHICS.md — GLAMbench Ethical Code

Created at the **Opendata.ch Open Cultural Data Hackathon, Winterthur, Switzerland — 2026-11-14**.
Governance: the GLAMhack community via the **Opendata.ch association**, with participating Swiss GLAM institutions.

This code adapts the **Apertus Charter** (Swiss AI Initiative, v1.0, August 2025, formerly the Swiss AI Charter; 11 articles, 68 principles) to the evaluation of AI systems on cultural heritage work. The Apertus Charter is rooted in Switzerland's constitutional values — neutrality, consensus, federalism, multilingualism, subsidiarity — and this code carries those values into GLAM benchmarking.

Where the charter and this code appear to conflict, the charter wins. This is a benchmark document, not legal advice and not institutional policy.

---

## 1. Truth and Evidence Over Fluency

*Charter: Art. 1 (Response Quality), Art. 2 (Knowledge and Reasoning Standards)*

- **2.5 — Say "unknown" rather than guess.** The benchmark rewards models that refuse when records do not support a claim. An abstention backed by evidence is a correct answer, not a failure.
- **2.1 / 2.2 — Evidence, and separating fact from speculation.** Every evaluated output should cite the source field, image region, record identifier, or provenance note it rests on. Model claims are scored against verified source truth, not against plausibility.
- **2.4 — Uncertainty is stated, never hidden.** Tasks must preserve ambiguity: contested attributions, missing rights statements, and conflicting dates are test cases, not noise to be cleaned up.
- **1.2 — Correctness above style.** Scores never reward fluent-sounding but unverifiable prose.
- **2.6 — Dated claims.** Tasks that involve dates or revisions must state the vintage of the data; an answer that ignores when a record was valid is unfaithful.

## 2. No Fabricated Heritage

*Charter: Art. 2, Art. 4 (Preventing Harm)*

- The benchmark contains **negative cases with no answer** (missing maker, unresolved attribution, absent rights statement, no image). Fabricating a creator, date, provenance chain, or license is the benchmark's central failure mode and is scored as an error, never as a bold guess.
- Hallucinated rights or access statements are scored worst of all, because they cause real-world reuse harm (4.5, 4.6 applied to cultural records).
- Ground truth annotations must be verified by domain experts before release (**Accurate ground truth**, per community consensus on multilingual benchmarking; cf. asta.txt, "Gaps").

## 3. Rights, Licenses, and Reuse

*Charter: Art. 4, Art. 8 (Autonomy and Personal Boundaries), Art. 9 (Long-term Orientation)*

- Every test case carries rights metadata (CC-BY / CC0 / public domain / restricted / unknown). Models are evaluated on respecting these — including **refusing to claim reuse when rights are unknown**.
- Benchmark data is drawn from openly licensed or openly accessible sources; terms of access are recorded per item in the datasheets (`tasks/*/datasheet.md`, `data/source_info.yaml`).
- No sensitive or restricted cultural material is ingested into the benchmark without the holder's permission. Provenance and community permissions outrank coverage.
- Rights conditions can change over time (expiry, revision). Where records show dated rights states, the benchmark prefers the state valid at the stated date (2.6).

## 4. Linguistic and Cultural Respect

*Charter: Art. 3 (Respectful Communication), especially 3.1, 3.3, 3.5, 3.9; Art. 7 (Collective Decision-Making), especially 7.5, 7.7*

- Tasks are built **from original Swiss collection contexts** (German, French, Italian, Swiss German dialects; Kurrent/Fraktur scripts where applicable) — **never by translating an English benchmark after the fact**. Localized benchmarks align with local judgment; translated ones do not.
- No language is privileged as "default". Multilingual parity is reported per language and per script, not aggregated into one number.
- Local terminology and spelling (e.g. `Zürich`) are preserved; normalization happens only when the source itself normalized, and is documented.
- Disputed or contested cultural descriptions are represented as disputes, not silently resolved (3.9 — compromises preserve dignity of all parties; 7.7 — multiple viewpoints integrated fairly).
- Minority and regional languages are first-class test subjects, not optional extensions.

## 5. Human Agency and Subsidiarity

*Charter: Art. 7 (Collective Decision-Making, especially 7.3, 7.5, 7.6), Art. 10 (Human Agency), Art. 6 (Professional Competence Boundaries)*

- **Humans decide.** The benchmark measures assistance to GLAM work, not replacement of it. Curators and archivists define "correct"; the scoring code encodes their decisions, and deviations are documented and reversible.
- **Subsidiarity (7.5).** Task design is delegated to the level with the relevant expertise: rights questions → rights officers; transcription conventions → conservators/linguists; schema questions → data wranglers. The technical team does not overrule domain experts.
- **Local and decentralized (7.5, 7.6).** Governance lives in the Opendata.ch community: public review, steady releases, no abrupt breaking changes to tasks or scores.
- **Assistance, not authority (6.3, 10.1).** The benchmark never certifies a model as safe for unsupervised cataloguing, provenance determination, or rights clearance. Results support professional judgment; they do not waive it.

## 6. Identity, Honesty, and Limits

*Charter: Art. 11 (AI Identity and Limits), Art. 1*

- Leaderboard entries always show: model name/version, date of evaluation, task-set version, and known model limits (knowledge cutoff, reasoning limits) where disclosed by the provider.
- Benchmark documentation (benchmark cards + datasheets) states goals, methods, data sources, metrics, contamination risks, and known weaknesses before any result is published (cf. Geoffrey Arnold's FactSheets / BenchmarkCards, see `priorart.md`).
- No score shall be presented as a general verdict on a model's competence — only as performance on this dated, this-version test set.
- Failure modes found during evaluation are published with the results.

## 7. Openness and Community Governance

*Charter: Art. 5 (Resolving Value Conflicts), Art. 7, Art. 9*

- The benchmark is open infrastructure: datasets, tasks, and scorers are public, machine-readable, and versioned; results are reproducible locally via offline scoring scripts before any leaderboard publication.
- Changes to tasks, ground truth, licenses, or scoring require **domain-expert review plus community review** (GLAMhack / Opendata.ch) before merge. Technical changes and ethical changes are reviewed separately.
- Value conflicts (e.g. openness vs. community restriction; coverage vs. accuracy) are documented openly: which values were weighed, which were preserved, and why (5.1, 5.2, 5.8).
- The benchmark assumes long-term stewardship (Art. 9): dated tasks, versioned data, deprecation paths, and explicit contamination monitoring — public collection records may already sit in training corpora, and cross-lingual contamination is treated as a real risk, not a theoretical one.

## 8. Abstention Is a Feature

*Charter: Art. 2.5, Art. 8 (8.1, 8.3)*

- Models may answer `Unsupported by the record` or `Insufficient evidence` and are rewarded for doing so correctly.
- The benchmark reports an **abstention profile** per model: correct refusals, wrong refusals, and overclaims. A high-accuracy model that never abstains is flagged, not celebrated.
- Evidence-grounded outputs are required wherever feasible: an answer without a pointer to its supporting source is treated as unverifiable.

## 9. Scoring and Reporting Commitments

- **Multiple metrics, never one number.** Task success, evidence quality, abstention quality, per-language parity, and error analysis are all reported (see `asta.txt`: "Multi-metric evaluation, not one score").
- **Negative and no-answer cases are part of every task.**
- **Difficulty-stratified reporting** (easy / medium / hard) prevents masking failures behind easy wins.
- **Contamination controls.** Test sets are versioned and refreshed; known-public records in likely training corpora are labelled; methodology for contamination checking is documented.
- **Transparent revision.** If strong evidence shows a ground-truth error, the revision and its justification are published with the changelog (2.8).

## 10. What This Benchmark Is Not

- Not a certification, license approval, or provenance authority.
- Not a substitute for consultation with source communities or rights holders.
- Not a claim that models evaluated here may autonomously describe, link, translate, or clear rights on cultural objects.
- Not permanent: tasks, thresholds, and language coverage will be revised as collections, standards, and models evolve (Art. 9).

---

*Provenance of this document: drafted 2026-11-14 at the Open Cultural Data Hackathon, Winterthur, from the preceding benchmark methodology research (`priorart.md`), the Apertus Charter v1.0, and the OpenGLAM-Bench task design. Licence: CC0 — adopt, adapt, critique.*
