from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from airlab_fraud_agentic_ai.data.loaders import DataRepository, get_repository


@dataclass
class BBDatasetAdapter:
    repository: DataRepository

    @classmethod
    def create(cls) -> "BBDatasetAdapter":
        return cls(repository=get_repository())

    def alerts(self) -> pd.DataFrame:
        return self.repository.load("alerts")

    def customers(self) -> pd.DataFrame:
        return self.repository.load("customers")

    def accounts(self) -> pd.DataFrame:
        return self.repository.load("accounts")

    def transactions(self) -> pd.DataFrame:
        return self.repository.load("transactions")

    def behavioural_events(self) -> pd.DataFrame:
        return self.repository.load("behavioural_events")

    def features(self) -> pd.DataFrame:
        return self.repository.load("features")

    def historical_cases(self) -> pd.DataFrame:
        return self.repository.load("historical_cases")

    def data_quality(self) -> pd.DataFrame:
        return self.repository.load("data_quality")

    def lineage(self) -> pd.DataFrame:
        return self.repository.load("lineage")
