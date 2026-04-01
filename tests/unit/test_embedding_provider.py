"""Unit tests for SentenceTransformerEmbedder adapter.

Test Budget: 2 behaviors (embed_text dimensions, embed_batch consistency) x 2 = 4 max
Actual: 2 tests
"""
import pytest


def test_embed_text_returns_384_dimensions():
    """EmbeddingProvider.embed_text produces a 384-dimensional vector."""
    from asia.adapters.sentence_transformer_embedder import SentenceTransformerEmbedder

    embedder = SentenceTransformerEmbedder()
    result = embedder.embed_text("CHOP protocol for canine lymphoma")

    assert isinstance(result, list)
    assert len(result) == 384
    assert all(isinstance(v, float) for v in result)


def test_embed_batch_returns_consistent_dimensions():
    """EmbeddingProvider.embed_batch produces vectors of equal length for all inputs."""
    from asia.adapters.sentence_transformer_embedder import SentenceTransformerEmbedder

    embedder = SentenceTransformerEmbedder()
    texts = [
        "CHOP protocol for B-cell lymphoma",
        "Doxorubicin dose adjustment for neutropenia",
        "T-cell vs B-cell prognosis in canine lymphoma",
    ]
    results = embedder.embed_batch(texts)

    assert len(results) == 3
    for vec in results:
        assert len(vec) == 384
