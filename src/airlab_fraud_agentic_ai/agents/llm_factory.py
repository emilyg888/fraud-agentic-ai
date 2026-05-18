from __future__ import annotations

import json
from dataclasses import dataclass
from urllib import error, request

from airlab_fraud_agentic_ai.config import get_settings


@dataclass
class FakeLLM:
    backend: str = "fake"

    @property
    def provider(self) -> str:
        return self.backend

    def invoke(self, prompt: str) -> str:
        return f"[fake-llm] {prompt}"


@dataclass
class OllamaLLM:
    model: str
    host: str
    backend: str = "ollama"

    @property
    def provider(self) -> str:
        return self.backend

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
        try:
            with request.urlopen(http_request, timeout=120) as response:
                body = json.loads(response.read().decode("utf-8"))
        except error.URLError as exc:
            raise RuntimeError(
                f"Local Ollama model call failed for {self.model} at {self.host}. "
                "Start Ollama and confirm the model is available, or rerun with --llm-backend fake."
            ) from exc
        return body["response"]


def get_llm(provider: str | None = None, backend: str | None = None) -> FakeLLM | OllamaLLM:
    settings = get_settings()
    selected_backend = backend or provider or settings.llm_backend
    if selected_backend == "ollama":
        return OllamaLLM(model=settings.model_name, host=settings.ollama_host)
    return FakeLLM(backend=selected_backend)
