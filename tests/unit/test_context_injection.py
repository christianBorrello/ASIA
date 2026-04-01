"""Unit tests for patient context injection pure function.

Tests the build_patient_context pure function which formats
patient data into the LLM prompt template.

Test Budget: 2 behaviors x 2 = 4 max unit tests.
Behaviors: (1) full context formatting, (2) empty field omission.
"""
from __future__ import annotations

import pytest

from asia.domain.context_injection import build_patient_context


@pytest.mark.parametrize(
    "patient_data,expected_fragments,unexpected_fragments",
    [
        pytest.param(
            {
                "patient_name": "Luna",
                "breed": "Golden Retriever",
                "age": "7 anni",
                "diagnosis": "Linfoma multicentrico B-cell",
                "stage": "IIIa",
                "immunophenotype": "B-cell",
                "notes": "Buone condizioni",
                "query": "Qual e il protocollo migliore?",
            },
            [
                "PAZIENTE:",
                "Nome: Luna",
                "Razza: Golden Retriever",
                "Diagnosi: Linfoma multicentrico B-cell",
                "Stadio: IIIa",
                "DOMANDA: Qual e il protocollo migliore?",
            ],
            [],
            id="full-context-includes-all-fields",
        ),
        pytest.param(
            {
                "patient_name": "Rex",
                "diagnosis": "Linfoma multicentrico",
                "query": "Protocollo raccomandato?",
            },
            [
                "PAZIENTE:",
                "Nome: Rex",
                "Diagnosi: Linfoma multicentrico",
                "DOMANDA: Protocollo raccomandato?",
            ],
            ["Razza:", "Stadio:", "Immunofenotipo:", "Note:"],
            id="minimal-context-omits-empty-fields",
        ),
    ],
)
def test_build_patient_context(patient_data, expected_fragments, unexpected_fragments):
    """Context template includes populated fields and omits empty ones."""
    result = build_patient_context(**patient_data)

    for fragment in expected_fragments:
        assert fragment in result, f"Expected '{fragment}' in context"

    for fragment in unexpected_fragments:
        assert fragment not in result, f"Did not expect '{fragment}' in context"
