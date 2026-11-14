# Lighteval integration (planned)

Wrap OpenGLAM-Bench as [lighteval](https://github.com/huggingface/lighteval) custom tasks so it can run on Hugging Face's evaluation platform next to the Open LLM Leaderboard.

**Status: scaffold only — not installed, not verified.** API details below are from the lighteval docs as of 2026-11-14 and must be checked against the installed version before use.

- Docs: <https://huggingface.co/docs/lighteval/en/adding-a-custom-task>
- Task config reference: <https://huggingface.co/docs/lighteval/en/package_reference/tasks>
- Metric docs: <https://huggingface.co/docs/lighteval/en/adding-a-new-metric>

## General idea

One `custom_tasks.py` exposing `TASKS_TABLE` with one `LightevalTaskConfig` per GLAMbench task (`reading`, `describing`, `linking`, `translating`, `faithfulness`), reusing as much as possible of the benchmark itself rather than reimplementing it:

- **Prompt functions** reuse the prompt builders in `openglam_bench/runner.py` (`build_prompt`), so lighteval and the standalone runner evaluate the same inputs.
- **Metrics** are thin `SampleLevelMetric` wrappers around the existing scorers in `openglam_bench/scoring/` (e.g. `reading` → `char_accuracy`/`word_accuracy`, `describing` → `field_f1`, `linking` → `hits_at_1`, `translating` → `token_f1`, `faithfulness` → `accuracy` + corpus-level `hallucination_f1` via `faithfulness.aggregate`). `corpus_level_fn=np.mean` where metrics are sample-decomposable.
- **Scoring semantics are unchanged**: abstention is rewarded, no blended single score, per-language/per-type breakdowns stay available in the benchmark's own JSON outputs.
- **Dataset**: `hf_repo`/`hf_subset` pointing at a hub dataset built from `tasks/*/test_data/test.jsonl` (synthetic CC0 placeholders today). Open question: ship a tiny hub dataset now (clearly marked synthetic) or wire a local JSONL loader once the exact local-file mechanism is confirmed — `datasets.load_dataset("json", data_files=...)` works, but whether `LightevalTaskConfig.hf_repo` accepts that pattern needs a smoke test.
- **Task naming**: `openglambench:reading`, `openglambench:describing`, … selectable via `--custom-tasks lighteval/custom_tasks.py`.

## Sketch

```python
from lighteval.metrics.utils.metric_utils import SampleLevelMetric
from lighteval.tasks.lighteval_task import LightevalTaskConfig
from lighteval.tasks.requests import Doc
import numpy as np

from openglam_bench.scoring.reading import score as score_reading   # etc.

def reading_prompt(line: dict, task_name: str) -> Doc:
    return Doc(task_name=task_name, query=line["prompt"], choices=None, gold_index=None)

reading_acc = SampleLevelMetric(
    metric_name="char_accuracy", higher_is_better=True, category="accuracy",
    sample_level_fn=lambda item: score_reading(item.prediction, item)["char_accuracy"],
    corpus_level_fn=np.mean,
)

TASKS_TABLE = [
    LightevalTaskConfig(
        name="openglambench:reading",
        prompt_function=reading_prompt,
        hf_repo="openglam/openglam-bench",   # to create; synthetic until curation
        hf_subset="reading",
        hf_avail_splits=["test"],
        evaluation_splits=["test"],
        metrics=[reading_acc],
        generation_size=512,
        stop_sequence=["\n\n"],
        version=0,
    ),
    # … one config per task
]
```

Run (once implemented):

```bash
pip install -r lighteval/requirements.txt   # lighteval + numpy
lighteval accelerate \
    "model_name=<your-model>" \
    "openglambench:reading|0" \
    --custom-tasks lighteval/custom_tasks.py
```

## Caveats / TODO

- Verify the `Doc` contract for **free-form generation** (loglikelihood tasks want `choices`/`gold_index`; generative metrics read the raw prediction) against the installed lighteval version.
- Verify `SampleLevelMetric.sample_level_fn` receives what the example above assumes (items with `.prediction` vs. raw strings).
- `faithfulness`'s `hallucination_f1` is corpus-level; don't fake it as a per-sample metric — either restructure `faithfulness.aggregate` or report it via benchmark runner alongside lighteval.
- `requirements.txt`: pin `lighteval` (and `datasets` if local loading is used) — lighteval's API has changed across releases.
- Data remains **synthetic placeholders** until GLAM institutions contribute curated, rights-cleared records (see `../ETHICS.md`); no real-model conclusions until then.

## Why lighteval

Hub-native datasets and models, one CLI for local (`accelerate`) and endpoint evaluation, and direct comparability with other HF evaluations — useful for GLAM partners that already run open models.
