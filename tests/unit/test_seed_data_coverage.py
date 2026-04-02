"""Unit tests for seed data topic coverage.

Verifies that the curated seed papers cover all critical query topics
for both lymphoma and carcinoma corpora.

Test Budget: 5 behaviors x 2 = 10 max
  1. Lymphoma topic coverage (parametrized)
  2. Carcinoma topic coverage (parametrized)
  3. Total paper count meets minimum
  4. Carcinoma queries present in pre-loaded queries
  5. Seed runner script exists
Actual: 5 tests (3 parametrized + 2 simple)
"""
import importlib
import sys
from pathlib import Path

import pytest

# Ensure backend is importable
_backend_path = str(Path(__file__).resolve().parents[2] / "backend")
if _backend_path not in sys.path:
    sys.path.insert(0, _backend_path)


# ---------------------------------------------------------------------------
# Lymphoma topics (existing)
# ---------------------------------------------------------------------------
LYMPHOMA_QUERY_TOPICS = [
    ("first_line_chop", ["CHOP", "first-line", "B-cell"]),
    ("chop_19_vs_25", ["CHOP-19", "CHOP-25", "19-week", "25-week"]),
    ("rescue_protocols", ["rescue", "Tanovea", "LOPP", "DMAC", "LAP"]),
    ("t_cell_vs_b_cell", ["T-cell", "B-cell", "immunophenotype", "prognosis"]),
    ("doxorubicin_dose", ["doxorubicin", "dose", "neutropenia"]),
]


@pytest.mark.parametrize("topic_name,keywords", LYMPHOMA_QUERY_TOPICS)
def test_seed_papers_cover_lymphoma_topic(topic_name, keywords):
    """Each lymphoma query topic has at least one paper with relevant content."""
    from db.seeds.seed_papers import SEED_PAPERS

    all_text = " ".join(
        f"{p['title']} {p.get('abstract', '')}" for p in SEED_PAPERS
    )
    matched = any(kw.lower() in all_text.lower() for kw in keywords)
    assert matched, f"No seed paper covers lymphoma topic '{topic_name}' (keywords: {keywords})"


# ---------------------------------------------------------------------------
# Carcinoma topics (new)
# ---------------------------------------------------------------------------
CARCINOMA_QUERY_TOPICS = [
    ("mediastinal_tumors", ["thymoma", "thymic carcinoma", "mediastinal"]),
    ("hypercalcemia", ["hypercalcemia", "PTHrP", "paraneoplastic"]),
    ("treatment", ["toceranib", "carboplatin", "radiation", "surgery"]),
    ("prognosis", ["thyroidectomy", "thyroid carcinoma", "staging"]),
    ("differential_diagnosis", ["flow cytometry", "cytokeratin", "vimentin", "differential"]),
]


@pytest.mark.parametrize("topic_name,keywords", CARCINOMA_QUERY_TOPICS)
def test_seed_papers_cover_carcinoma_topic(topic_name, keywords):
    """Each carcinoma query topic has at least one paper with relevant content."""
    from db.seeds.seed_papers import SEED_PAPERS

    all_text = " ".join(
        f"{p['title']} {p.get('abstract', '')}" for p in SEED_PAPERS
    )
    matched = any(kw.lower() in all_text.lower() for kw in keywords)
    assert matched, f"No seed paper covers carcinoma topic '{topic_name}' (keywords: {keywords})"


# ---------------------------------------------------------------------------
# Paper count and structural checks
# ---------------------------------------------------------------------------
def test_seed_papers_total_count_meets_minimum():
    """Seed corpus has at least 40 papers (24 lymphoma + carcinoma)."""
    from db.seeds.seed_papers import SEED_PAPERS

    assert len(SEED_PAPERS) >= 40, (
        f"Expected >= 40 total seed papers, got {len(SEED_PAPERS)}"
    )


def test_pre_loaded_queries_include_carcinoma():
    """Pre-loaded queries include at least 2 carcinoma-related queries."""
    from asia.config.pre_loaded_queries import PRE_LOADED_QUERIES

    carcinoma_keywords = ["carcinoma", "timoma", "ipercalcemia", "massa mediastinica"]
    carcinoma_queries = [
        q for q in PRE_LOADED_QUERIES
        if any(kw.lower() in q["text"].lower() for kw in carcinoma_keywords)
    ]
    assert len(carcinoma_queries) >= 2, (
        f"Expected >= 2 carcinoma queries, got {len(carcinoma_queries)}: "
        f"{[q['text'][:50] for q in carcinoma_queries]}"
    )


def test_seed_runner_script_exists():
    """A seed runner script exists and is importable."""
    run_seed = importlib.import_module("db.seeds.run_seed")
    assert hasattr(run_seed, "main"), "run_seed.py must have a main() function"
