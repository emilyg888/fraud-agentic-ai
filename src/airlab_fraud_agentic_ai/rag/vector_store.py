from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class RetrievedDocument:
    path: str
    category: str
    title: str
    content: str


class SimpleVectorStore:
    def __init__(self, documents: list[RetrievedDocument]) -> None:
        self.documents = documents

    @staticmethod
    def _score(query: str, content: str) -> int:
        query_terms = {token for token in re.split(r"[^a-zA-Z0-9]+", query.lower()) if token}
        content_terms = {token for token in re.split(r"[^a-zA-Z0-9]+", content.lower()) if token}
        return sum(1 for token in query_terms if token and token in content_terms)

    def search(self, query: str, limit: int = 5, category: str | None = None) -> list[RetrievedDocument]:
        candidates = [
            document
            for document in self.documents
            if category is None or document.category == category
        ]
        ranked = sorted(
            candidates,
            key=lambda document: self._score(query=query, content=document.content),
            reverse=True,
        )
        return [document for document in ranked[:limit] if self._score(query, document.content) > 0]
