from __future__ import annotations

from airlab_fraud_agentic_ai.agents.llm_factory import FakeLLM, OllamaLLM, get_llm


def test_get_llm_defaults_to_ollama_settings(monkeypatch) -> None:
    monkeypatch.setenv("LOCAL_LLM_PROVIDER", "ollama")
    monkeypatch.setenv("MODEL_NAME", "qwen3.6:35b-a3b")
    llm = get_llm()
    assert isinstance(llm, OllamaLLM)
    assert llm.model == "qwen3.6:35b-a3b"


def test_get_llm_can_return_fake_provider() -> None:
    llm = get_llm(provider="fake")
    assert isinstance(llm, FakeLLM)
    assert llm.invoke("hello").startswith("[fake-llm]")
