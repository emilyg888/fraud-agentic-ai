from __future__ import annotations

from airlab_fraud_agentic_ai.rag.retriever import KnowledgeRetriever


def retrieve_case_knowledge(query: str) -> dict:
    retriever = KnowledgeRetriever()
    return {
        "fraud_typologies": retriever.retrieve(query=query, category="fraud_typologies", limit=2),
        "policies": retriever.retrieve(query=query, category="policies", limit=2),
        "data_dictionary": retriever.retrieve(query=query, category="data_dictionary", limit=2),
    }
