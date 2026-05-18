from __future__ import annotations

from urllib import error

import pytest

from airlab_fraud_agentic_ai.agents import llm_factory
from airlab_fraud_agentic_ai.agents.llm_factory import FakeLLM, OllamaLLM, get_llm


def test_get_llm_defaults_to_ollama_settings(monkeypatch) -> None:
    monkeypatch.setenv("LOCAL_LLM_BACKEND", "ollama")
    monkeypatch.setenv("MODEL_NAME", "qwen3.6:35b-a3b")
    llm = get_llm()
    assert isinstance(llm, OllamaLLM)
    assert llm.model == "qwen3.6:35b-a3b"


def test_get_llm_can_return_fake_backend() -> None:
    llm = get_llm(backend="fake")
    assert isinstance(llm, FakeLLM)
    assert llm.backend == "fake"
    assert llm.invoke("hello").startswith("[fake-llm]")


def test_ollama_llm_raises_actionable_error_when_server_is_unavailable(monkeypatch) -> None:
    def raise_url_error(*args, **kwargs):
        raise error.URLError("connection refused")

    monkeypatch.setattr(llm_factory.request, "urlopen", raise_url_error)
    llm = OllamaLLM(model="qwen3.6:35b-a3b", host="http://127.0.0.1:11434")

    with pytest.raises(RuntimeError, match="rerun with --llm-backend fake"):
        llm.invoke("hello")
