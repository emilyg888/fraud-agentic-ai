from __future__ import annotations

from pathlib import Path

from airlab_fraud_agentic_ai.config import get_settings
from airlab_fraud_agentic_ai.rag.vector_store import RetrievedDocument, SimpleVectorStore


def build_knowledge_store(base_dir: Path | None = None) -> SimpleVectorStore:
    settings = get_settings()
    root = base_dir or settings.knowledge_dir
    documents: list[RetrievedDocument] = []
    for path in sorted(root.rglob("*.md")):
        relative_parts = path.relative_to(root).parts
        category = relative_parts[0]
        content = path.read_text(encoding="utf-8")
        documents.append(
            RetrievedDocument(
                path=str(path.relative_to(settings.root_dir)),
                category=category,
                title=path.stem.replace("_", " ").title(),
                content=content,
            )
        )
    return SimpleVectorStore(documents)
