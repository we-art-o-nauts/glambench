from openglam_bench import TASK_NAMES
from openglam_bench.runner import load_test_data
from openglam_bench.scoring import SCORERS


def test_five_tasks_registered():
    assert TASK_NAMES == ["reading", "describing", "linking", "translating", "faithfulness"]
    assert set(SCORERS) == set(TASK_NAMES)


def test_every_task_has_nonempty_test_data():
    for task in TASK_NAMES:
        items = load_test_data(task)
        assert items, task
        for item in items:
            assert item.get("id"), task
            assert item.get("license"), task
            assert str(item.get("source_uri", "")).startswith(("synthetic://", "cc", "open", "https")), task


def test_reading_scoring_bounds():
    from openglam_bench.scoring.reading import score
    item = {"gold_text": "Das ist ein Test."}
    perfect = score("Das ist ein Test.", item)
    assert perfect["char_accuracy"] == 1.0
    garbage = score("xyzzy", item)
    assert 0.0 <= garbage["char_accuracy"] < 1.0


def test_linking_abstain_on_no_answer():
    from openglam_bench.scoring.linking import score
    item = {"gold_qid": None, "candidates": []}
    assert score("no answer", item)["abstention_correct"] == 1.0
    assert score("Q39", item)["abstention_correct"] == 0.0


def test_linking_hits():
    from openglam_bench.scoring.linking import score
    item = {"gold_qid": "Q39", "candidates": [{"qid": "Q39"}, {"qid": "Q38"}]}
    assert score("Q39", item)["hits_at_1"] == 1.0
    assert score("Q38", item)["hits_at_1"] == 0.0


def test_faithfulness_abstain_zero_accuracy():
    from openglam_bench.scoring.faithfulness import score
    item = {"supported": False, "error_type": "invented_date"}
    assert score("insufficient evidence", item)["abstained"] == 1.0


def test_describing_insufficient_evidence_case():
    from openglam_bench.scoring.describing import score
    item = {"gold_fields": {}, "gold_status": "insufficient_evidence"}
    assert score("insufficient evidence", item)["field_f1"] == 1.0
