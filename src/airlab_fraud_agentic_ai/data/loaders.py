from __future__ import annotations

from functools import lru_cache
from pathlib import Path

import pandas as pd
import yaml

from airlab_fraud_agentic_ai.config import get_settings


class DataRepository:
    def __init__(self, mapping_path: Path | None = None) -> None:
        settings = get_settings()
        self.root_dir = settings.root_dir
        self.mapping_path = mapping_path or settings.data_dir / "bb_dataset_mapping.yaml"
        self.mapping = self._load_mapping()

    def _load_mapping(self) -> dict:
        with self.mapping_path.open("r", encoding="utf-8") as handle:
            return yaml.safe_load(handle)

    @lru_cache(maxsize=None)
    def load(self, dataset_name: str) -> pd.DataFrame:
        dataset = self.mapping[dataset_name]
        path = self.root_dir / dataset["path"]
        return pd.read_csv(path)


def get_repository() -> DataRepository:
    return DataRepository()
