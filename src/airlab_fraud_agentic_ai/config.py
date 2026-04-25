from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    root_dir: Path
    data_dir: Path
    docs_dir: Path
    knowledge_dir: Path
    reports_dir: Path
    runs_dir: Path
    registry_dir: Path
    llm_provider: str
    model_name: str
    ollama_host: str


def get_settings() -> Settings:
    root_dir = Path(os.getenv("AIRLAB_ROOT_DIR", Path(__file__).resolve().parents[2]))
    return Settings(
        root_dir=root_dir,
        data_dir=Path(os.getenv("AIRLAB_DATA_DIR", root_dir / "data")),
        docs_dir=Path(os.getenv("AIRLAB_DOCS_DIR", root_dir / "docs")),
        knowledge_dir=Path(os.getenv("AIRLAB_KNOWLEDGE_DIR", root_dir / "knowledge")),
        reports_dir=Path(os.getenv("AIRLAB_REPORTS_DIR", root_dir / "reports")),
        runs_dir=Path(os.getenv("AIRLAB_RUNS_DIR", root_dir / "runs")),
        registry_dir=Path(os.getenv("AIRLAB_REGISTRY_DIR", root_dir / "signal_registry")),
        llm_provider=os.getenv("LOCAL_LLM_PROVIDER", "ollama"),
        model_name=os.getenv("MODEL_NAME", "qwen3.6:35b-a3b"),
        ollama_host=os.getenv("OLLAMA_HOST", "http://127.0.0.1:11434"),
    )
