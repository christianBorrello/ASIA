"""Evidence scoring -- pure domain function.

Computes evidence level (ALTO/MODERATO/BASSO) from cited paper metadata.

Formula:
  study_type_score = max score among cited papers' study types
  count_bonus = min(paper_count * 3, 12)
  sample_size_bonus = min(log2(total_sample_size), 8) if total > 0 else 0
  total_score = study_type_score + count_bonus + sample_size_bonus

Thresholds: ALTO >= 40, MODERATO >= 20, BASSO < 20
"""
from __future__ import annotations

import math

from asia.domain.models import EvidenceLevel, Paper

STUDY_TYPE_SCORES: dict[str, int] = {
    "meta_analysis": 20,
    "randomized_controlled_trial": 15,
    "rct": 15,
    "prospective": 12,
    "clinical_trial": 12,
    "retrospective": 8,
    "case_series": 5,
    "case_report": 2,
    "review": 5,
    "pharmacokinetic": 8,
}

ALTO_THRESHOLD = 40
MODERATO_THRESHOLD = 20


def compute_evidence_level(papers: list[Paper]) -> tuple[EvidenceLevel, float]:
    """Compute evidence level from a list of cited papers.

    Returns a tuple of (EvidenceLevel, numeric_score).
    """
    if not papers:
        return EvidenceLevel.BASSO, 0.0

    study_type_score = max(
        STUDY_TYPE_SCORES.get(p.study_type or "", 0) for p in papers
    )

    count_bonus = min(len(papers) * 3, 12)

    total_sample_size = sum(p.sample_size or 0 for p in papers)
    sample_size_bonus = 0.0
    if total_sample_size > 0:
        sample_size_bonus = min(math.log2(total_sample_size), 8.0)

    total_score = study_type_score + count_bonus + sample_size_bonus

    if total_score >= ALTO_THRESHOLD:
        level = EvidenceLevel.ALTO
    elif total_score >= MODERATO_THRESHOLD:
        level = EvidenceLevel.MODERATO
    else:
        level = EvidenceLevel.BASSO

    return level, total_score
