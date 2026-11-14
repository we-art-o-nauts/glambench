"""Benchmark runner: loads task test data, prompts the model, scores outputs,
and writes a per-model JSON result file.
"""

from __future__ import annotations

import json
from pathlib import Path

from .scoring import SCORERS, faithfulness

REPO_ROOT = Path(__file__).resolve().parent.parent
TASKS_DIR = REPO_ROOT / "tasks"


def load_test_data(task: str) -> list[dict]:
    path = TASKS_DIR / task / "test_data" / "test.jsonl"
    items = []
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                items.append(json.loads(line))
    return items


def build_prompt(task: str, item: dict) -> str:
    if task == "reading":
        return item.get("prompt") or (
            f"Transcribe this historical document exactly as written (language: {item.get('language')}, "
            f"script: {item.get('script')}). Do not modernise spelling. Document image/text reference: "
            f"{item.get('image_path')}")
    if task == "describing":
        return ("Given the following fields from a cultural object record, produce the complete catalogue "
                f"description as KEY: VALUE lines or JSON. If a field is not supported by the record, mark it "
                f"insufficient_evidence.\nRecord:\n{item['record']}")
    if task == "linking":
        cand = "\n".join(f"- {c['qid']}: {c.get('label', '')}" for c in item.get("candidates", []))
        return (f"Which Wikidata entity does this refer to? Answer with a QID only, or say 'no answer' if none "
                f"fits.\nMention: {item['mention']}\nRecord context: {item.get('context', '')}\n"
                f"Candidates:\n{cand}")
    if task == "translating":
        return (f"Translate the following {item.get('source_lang')} historical text into {item.get('target_lang')}. "
                f"Preserve historical meaning, proper nouns, and cultural references; do not modernise register.\n\n"
                f"{item['source_text']}")
    if task == "faithfulness":
        return ("Is the following claim about this cultural object supported by the record? Answer 'supported' or "
                f"'unsupported', and name the error type if unsupported (invented_date, invented_creator, "
                f"false_provenance, rights_misstatement, invented_place, other).\n"
                f"Record:\n{item['record']}\nClaim:\n{item['claim']}")
    raise ValueError(f"Unknown task: {task}")


def run_task(model, task: str, limit: int | None = None) -> dict:
    items = load_test_data(task)
    if limit:
        items = items[:limit]
    scorer = SCORERS[task]
    per_item = []
    for item in items:
        prompt = build_prompt(task, item)
        output = model.generate(task, prompt)
        metrics = scorer(output, item)
        per_item.append({"id": item.get("id"), "output": output, "metrics": metrics})

    summary: dict[str, float] = {}
    if per_item:
        keys = per_item[0]["metrics"].keys()
        for key in keys:
            summary[key] = round(sum(r["metrics"][key] for r in per_item) / len(per_item), 4)
    if task == "faithfulness":
        summary.update(faithfulness.aggregate([r["metrics"] for r in per_item]))

    return {"task": task, "model": getattr(model, "name", str(model)),
            "n_items": len(per_item), "summary": summary, "items": per_item}


def run_all(model, tasks: list[str] | None = None, limit: int | None = None) -> dict:
    from . import TASK_NAMES
    tasks = tasks or TASK_NAMES
    results = {task: run_task(model, task, limit) for task in tasks}
    results["model"] = getattr(model, "name", str(model))
    return results
