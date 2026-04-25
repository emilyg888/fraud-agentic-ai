from __future__ import annotations

import json
from dataclasses import dataclass
from urllib import request

from airlab_fraud_agentic_ai.config import get_settings


@dataclass
class FakeLLM:
    provider: str = "fake"

    def invoke(self, prompt: str) -> str:
        return f"[fake-llm] {prompt}"


@dataclass
class OllamaLLM:
    model: str
    host: str
    provider: str = "ollama"

    def invoke(self, prompt: str) -> str:
        payload = json.dumps(
            {
                "model": self.model,
                "prompt": prompt,
                "stream": False,
            }
        ).encode("utf-8")
        http_request = request.Request(
            f"{self.host}/api/generate",
            data=payload,
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with request.urlopen(http_request, timeout=120) as response:
            body = json.loads(response.read().decode("utf-8"))
        return body["response"]


def get_llm(provider: str | None = None) -> FakeLLM | OllamaLLM:
    settings = get_settings()
    selected_provider = provider or settings.llm_provider
    if selected_provider == "ollama":
        return OllamaLLM(model=settings.model_name, host=settings.ollama_host)
    return FakeLLM(provider=selected_provider)
