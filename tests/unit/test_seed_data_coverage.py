"""Unit tests for seed data topic coverage.

Verifies that the curated seed papers cover all 5 critical query topics.

Test Budget: 1 behavior (topic coverage) x 2 = 2 max
Actual: 1 parametrized test
"""
import pytest


CRITICAL_QUERY_TOPICS = [
    ("first_line_chop", ["CHOP", "first-line", "B-cell"]),
    ("chop_19_vs_25", ["CHOP-19", "CHOP-25", "19-week", "25-week"]),
    ("rescue_protocols", ["rescue", "Tanovea", "LOPP", "DMAC", "LAP"]),
    ("t_cell_vs_b_cell", ["T-cell", "B-cell", "immunophenotype", "prognosis"]),
    ("doxorubicin_dose", ["doxorubicin", "dose", "neutropenia"]),
]


@pytest.mark.parametrize("topic_name,keywords", CRITICAL_QUERY_TOPICS)
def test_seed_papers_cover_query_topic(topic_name, keywords):
    """Each critical query topic has at least one paper with relevant content."""
    import sys
    sys.path.insert(0, str(__import__("pathlib").Path(__file__).resolve().parents[2] / "backend"))
    from db.seeds.seed_papers import SEED_PAPERS

    all_text = " ".join(
        f"{p['title']} {p.get('abstract', '')}" for p in SEED_PAPERS
    )
    matched = any(kw.lower() in all_text.lower() for kw in keywords)
    assert matched, f"No seed paper covers topic '{topic_name}' (keywords: {keywords})"
