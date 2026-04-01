"""Query type classification -- pure domain functions."""
from __future__ import annotations

import re

_COMPARISON_PATTERNS: list[re.Pattern[str]] = [
    re.compile(r"\bvs\.?\b", re.IGNORECASE),
    re.compile(r"\bversus\b", re.IGNORECASE),
    re.compile(r"\bdifferenz[aei]\b", re.IGNORECASE),
    re.compile(r"\bconfronto\b", re.IGNORECASE),
    re.compile(r"\bconfrontare\b", re.IGNORECASE),
    re.compile(r"\brispetto\s+a\b", re.IGNORECASE),
    re.compile(r"\bcomparazione\b", re.IGNORECASE),
    re.compile(r"\bmeglio\s+tra\b", re.IGNORECASE),
]


def is_comparison_query(query_text: str) -> bool:
    """Detect whether a query is asking for a protocol comparison.

    Checks for Italian comparison keywords: vs, versus, differenze,
    confronto, confrontare, rispetto a, comparazione, meglio tra.
    """
    return any(pattern.search(query_text) for pattern in _COMPARISON_PATTERNS)
