"""Patient context injection for case-aware queries.

Pure function that builds the patient context template
for prepending to LLM prompts.
"""
from __future__ import annotations


def build_patient_context(
    patient_name: str,
    diagnosis: str,
    query: str,
    breed: str | None = None,
    age: str | None = None,
    stage: str | None = None,
    immunophenotype: str | None = None,
    notes: str | None = None,
) -> str:
    """Build patient context string for LLM prompt injection.

    Omits fields that are None or empty.
    """
    lines = ["PAZIENTE:"]

    field_map = [
        ("Nome", patient_name),
        ("Razza", breed),
        ("Et\u00e0", age),
        ("Diagnosi", diagnosis),
        ("Stadio", stage),
        ("Immunofenotipo", immunophenotype),
        ("Note", notes),
    ]

    for label, value in field_map:
        if value:
            lines.append(f"- {label}: {value}")

    lines.append("")
    lines.append(f"DOMANDA: {query}")

    return "\n".join(lines)
