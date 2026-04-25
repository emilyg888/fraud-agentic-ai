from __future__ import annotations

from dataclasses import dataclass

from airlab_fraud_agentic_ai.rag.ingest import build_knowledge_store
from airlab_fraud_agentic_ai.rag.vector_store import RetrievedDocument


@dataclass
class KnowledgeRetriever:
    store = build_knowledge_store()

    def retrieve(self, query: str, category: str | None = None, limit: int = 3) -> list[dict]:
        results: list[RetrievedDocument] = self.store.search(query=query, limit=limit, category=category)
        return [
            {
                "path": document.path,
                "category": document.category,
                "title": document.title,
                "excerpt": document.content.strip().splitlines()[0:3],
            }
            for document in results
        ]
