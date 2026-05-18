from __future__ import annotations

from airlab_fraud_agentic_ai import cli


def test_cli_investigate_reports_local_llm_runtime_errors_without_traceback(monkeypatch, capsys) -> None:
    def fail_run(*args, **kwargs):
        raise RuntimeError("Local Ollama model call failed. Rerun with --llm-backend fake.")

    monkeypatch.setattr(cli, "run_investigation", fail_run)

    exit_code = cli.main(["investigate", "--case-id", "A-1001"])

    captured = capsys.readouterr()
    assert exit_code == 1
    assert "Rerun with --llm-backend fake" in captured.err
    assert "Traceback" not in captured.err
