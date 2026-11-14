Benchmark for Cultural Preservation i'th'Age of AI

# OpenGLAM-Bench

<small>GLAMhack 2026 · O Lavrovsky M Mazourik</small>

---

## The Challenge

**Can we build an open benchmark that tests whether AI can *responsibly* work with cultural collections?**

---

![Screenshot From 2026-11-14 17-12-42](https://hackmd.io/_uploads/Sklq_WLRGl.png)

---

![Screenshot From 2026-11-14 16-04-38](https://hackmd.io/_uploads/SkGWBWICfe.png)

---

- Existing AI benchmarks test narrow tasks: raw accuracy, no provenance, no rights reasoning.
- Cultural records are uneven: images, catalogues, rights, provenance, multiple languages, revisions over time.
- Hallucinated creators, dates or licences cause real harm — and are hard to detect.
- Switzerland's [67+ OpenGLAM datasets](https://opendata.swiss/en/organization/openglam) are waiting to be used!

---

**OpenGLAM-Bench** 

An open benchmark for Swiss GLAM collections

- Not a one-off test set: an **open evaluation system** — extensible like Lighteval, multi-metric, community-reviewed
- **Five tasks**, mirroring real collection work:

---

| Task | What it tests |
|---|---|
| Reading | Transcribe historical documents (Kurrent, Fraktur, archaic spelling) |
| Describing | Generate catalogue metadata, judged against institution records |
| Linking | Match people/places/works to Wikidata — or abstain |
| Translating | Historical DE/FR/IT texts, meaning + key terms preserved |
| Faithfulness | Catch invented creators, dates, provenance, rights claims |

---

## Design principles

- **Abstention is rewarded** — negative/no-answer cases are part of every task
- **Insufficient evidence** - always beats hallucination
- **Evidence-grounded outputs** — answers must cite source fields; no source, no credit
- **Localized multilingual data**, translated benchmarks (de / fr / it / en)
- **Difficulty-stratified**, contamination-aware, refreshable

---

![Screenshot From 2026-11-14 16-59-44](https://hackmd.io/_uploads/SkkcHWLAGx.png)

---

### Leaderboard :trophy: 

| model | ccuracy |  halluc | rank |
| --- | --- | --- | --- |
| Apertus-v1.5-70B | 0.9984 | 0.9004 | 1.286 |
| Apertus-v1.5-8B | 0.9984 | 0.9042 | 1.714 |

---

## CKAN utility

Pulled metadata for all **67 OpenGLAM datasets** on opendata.swiss and ranked candidates per task (scans → Reading, CSVs/datastores → Describing, SPARQL/API/RDF → Linking, multilingual → Translating, licence-transparent → Faithfulness)

---

## Best candidates:

**SKKG Digital Collection**, e-manuscripta, Zentral- & Universitätsbibliotheken rare prints/manuscripts, Swiss Fotografie-Metadaten, Diplomatic Documents

---

### No dataset without rights review

`ETHICS.md`, adapted from the **Apertus Charter** (Swiss AI Initiative), governs: truth over accuracy, abstention, rights & licences, human agency

---


- ✅ Harness + all 5 scorers implemented, 7/7 tests pass
- ✅ `.env`-configured, runs any OpenAI-compatible endpoint — **Apertus 1.5 8B via PublicAI already smoke-tested**
- ✅ Leaderboard (multi-metric, no blended score) + static site with embedded CKAN dataset catalogue
- ✅ Lighteval integration scaffolded for HF's evals platform
- ⏳ Curated GLAM pairs + rights review needed to turn this into real model comparisons

---

![Screenshot 2026-11-14 at 17-02-40](https://hackmd.io/_uploads/ryfEUbU0fe.png)

Thanks for an awesome GLAMhack!


