from __future__ import annotations

from airlab_fraud_agentic_ai.rag.retriever import KnowledgeRetriever


def test_retriever_returns_relevant_typology() -> None:
    retriever = KnowledgeRetriever()
    results = retriever.retrieve("device change new payee account takeover", category="fraud_typologies", limit=2)
    paths = [item["path"] for item in results]
    assert any("account_takeover.md" in path for path in paths)
