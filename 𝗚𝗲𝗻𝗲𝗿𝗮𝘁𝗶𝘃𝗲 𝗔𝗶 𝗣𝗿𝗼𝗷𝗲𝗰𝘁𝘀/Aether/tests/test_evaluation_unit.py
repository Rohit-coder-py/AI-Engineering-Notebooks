"""
Functional unit tests for Aether's evaluation harness logic.

Everything here runs on the local sample PDF and the locally cached
embedding model - no LLM, no network-dependent logic required.

How to run:  pytest tests/ -v
"""

import json
import sys
from pathlib import Path

import pytest

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "evaluation"))

import evaluate  # noqa: E402  (evaluation/evaluate.py)


@pytest.fixture(scope="module")
def index():
    """The FAISS index over the sample handbook (built once per test run)."""
    # Heavy inference dependencies: skip the whole fixture if not installed.
    for _dep in ("faiss", "pypdf", "langchain_community",
                 "langchain_huggingface", "sentence_transformers"):
        pytest.importorskip(_dep)
    require_samples()
    return evaluate.build_index(evaluate.PDF_PATH)


def _require_module_dependency(name):
    try:
        __import__(name)
    except ImportError:
        pytest.skip(f"{name} not installed in this environment")


def require_samples():
    if not evaluate.PDF_PATH.exists():
        pytest.skip("sample PDF not generated in this workspace")


# ----------------------------------------------------------------------
# Golden-QA integrity: the test set itself must be well-formed
# ----------------------------------------------------------------------
def test_golden_qa_is_wellformed():
    for item in evaluate.GOLDEN_QA:
        assert item["id"] and item["question"]
        if item["type"] == "must_refuse":
            assert not item["keywords"], "refusal items must not have keywords"
        else:
            assert item["keywords"], f"{item['id']} has no keywords to match"
        assert item["type"] in {"fact_lookup", "config_lookup", "policy",
                                "composition", "must_refuse"}


def test_golden_qa_ids_unique():
    ids = [item["id"] for item in evaluate.GOLDEN_QA]
    assert len(ids) == len(set(ids))


# ----------------------------------------------------------------------
# Retrieval behaviour on the real sample index
# ----------------------------------------------------------------------
def test_retrieval_finds_config_facts(index):
    db, stats = index
    assert stats["vectors"] >= 11, "sample PDF should produce a meaningful corpus"

    def chunks_for(question, k=4):
        return " ".join(d.page_content for d in
                        db.similarity_search(question, k=k)).lower()

    assert "1000" in chunks_for("What chunk size does the splitter use?")
    assert "150" in chunks_for("What chunk size does the splitter use?")
    assert "0.7" in chunks_for("What temperature is the planner?")
    assert "384" in chunks_for("What is the embedding dimension of MiniLM?")


def test_retrieval_metrics_are_sane(index):
    db, _ = index
    summary, per_item = evaluate.evaluate_retrieval(db, evaluate.GOLDEN_QA)

    assert summary["n_items"] == 14          # 14 answerable questions
    assert 0.0 <= summary["hit@1"] <= 1.0
    assert 0.0 <= summary["mrr"] <= 1.0
    # every non-refusal item must appear in the details
    assert len(per_item) == 14
    for row in per_item:
        assert row["id"].startswith(("q", "r"))


def test_index_metadata_keeps_page_numbers(index):
    """Page provenance is what lets the Writer cite sources - it must survive."""
    db, _ = index
    docs = db.similarity_search("What chunk size and overlap are used?", k=4)
    for doc in docs:
        assert "page" in doc.metadata and doc.metadata["page"] >= 1


# ----------------------------------------------------------------------
# Report generation (deterministic, no LLM)
# ----------------------------------------------------------------------
def test_write_reports_produces_consistent_files(tmp_path, monkeypatch):
    monkeypatch.setattr(evaluate, "PROJECT_ROOT", tmp_path)
    retrieval = {"hit@1": 0.5, "hit@2": 0.7, "hit@4": 0.9, "mrr": 0.6, "n_items": 10}
    evaluate.write_reports(retrieval, None, None, {"pages": 6, "chunks": 11, "vectors": 11},
                           llm_used=False)

    payload = json.loads((tmp_path / "evaluation" / "results.json").read_text(encoding="utf-8"))
    assert payload["retrieval"]["hit@1"] == 0.5
    assert payload["llm_evaluation_run"] is False
    md = (tmp_path / "evaluation" / "RESULTS.md").read_text(encoding="utf-8")
    assert "**0.5**" in md and "MRR" in md
