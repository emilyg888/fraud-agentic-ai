from __future__ import annotations

import argparse
import csv
import itertools
import re
import subprocess
import time
from pathlib import Path


TPS_RE = re.compile(
    r"\[\s*Prompt:\s*(?P<prompt_tps>[0-9.]+)\s+t/s\s+\|\s+Generation:\s*(?P<generation_tps>[0-9.]+)\s+t/s\s*\]"
)
ERROR_RE = re.compile(r"(Compute error|Insufficient Memory|failed to decode|error:)", re.IGNORECASE)


def parse_csv_ints(value: str) -> list[int]:
    return [int(part.strip()) for part in value.split(",") if part.strip()]


def parse_csv_strings(value: str) -> list[str]:
    return [part.strip() for part in value.split(",") if part.strip()]


def parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parent
    default_binary = project_root.parent / "llama.cpp" / "build" / "bin" / "llama-cli"
    default_model = (
        project_root.parent
        / "llama-models"
        / "hf-cache"
        / "hub"
        / "models--lmstudio-community--Qwen3.6-35B-A3B-GGUF"
        / "snapshots"
        / "68a34855558af61cbef0324d31f411be8a506b08"
        / "Qwen3.6-35B-A3B-Q4_K_M.gguf"
    )

    parser = argparse.ArgumentParser(description="Sweep llama.cpp runtime settings and write TPS results to CSV.")
    parser.add_argument("--binary", type=Path, default=default_binary, help="Path to llama-cli binary.")
    parser.add_argument("--model", type=Path, default=default_model, help="Path to GGUF model.")
    parser.add_argument("--output", type=Path, default=project_root / "results.csv", help="Output CSV path.")
    parser.add_argument("--batches", default="8,16,32,64", help="Comma-separated batch sizes.")
    parser.add_argument("--ctxs", default="2048,4096,8192,16384", help="Comma-separated context sizes.")
    parser.add_argument("--kvs", default="q8_0,q6_K,q4_0", help="Comma-separated KV cache types.")
    parser.add_argument("--threads", type=int, default=8, help="llama.cpp thread count.")
    parser.add_argument("--ngl", default="999", help="GPU layer setting passed to -ngl.")
    parser.add_argument("--ncmoe", type=int, default=1, help="Value passed to -ncmoe.")
    parser.add_argument("--n-predict", type=int, default=64, help="Tokens to generate for each run.")
    parser.add_argument("--prompt", default="Say hello in one sentence.", help="Benchmark prompt.")
    parser.add_argument("--timeout", type=int, default=900, help="Per-run timeout in seconds.")
    parser.add_argument(
        "--extra-args",
        nargs="*",
        default=[],
        help="Additional llama-cli args appended after the standard benchmark flags.",
    )
    return parser.parse_args()


def build_command(
    args: argparse.Namespace,
    batch: int,
    ctx: int,
    kv: str,
) -> list[str]:
    return [
        str(args.binary),
        "-m",
        str(args.model),
        "-ngl",
        str(args.ngl),
        "-ncmoe",
        str(args.ncmoe),
        "-t",
        str(args.threads),
        "-c",
        str(ctx),
        "-b",
        str(batch),
        "-ub",
        str(batch),
        "-ctk",
        kv,
        "-ctv",
        kv,
        "--mlock",
        "--mmap",
        "--reasoning",
        "off",
        "--simple-io",
        "-st",
        "-n",
        str(args.n_predict),
        "-p",
        args.prompt,
        *args.extra_args,
    ]


def run_case(command: list[str], timeout: int) -> tuple[str, int | None, float]:
    started = time.perf_counter()
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
        combined = f"{completed.stdout}\n{completed.stderr}"
        return combined, completed.returncode, time.perf_counter() - started
    except subprocess.TimeoutExpired as exc:
        stdout = exc.stdout or ""
        stderr = exc.stderr or ""
        combined = f"{stdout}\n{stderr}\nTIMEOUT"
        return combined, None, time.perf_counter() - started


def parse_status(output: str, returncode: int | None) -> str:
    if returncode is None:
        return "timeout"
    if ERROR_RE.search(output):
        return "error"
    if "Exiting..." in output and "Generation:" in output:
        return "ok"
    if returncode == 0 and "Generation:" in output:
        return "ok"
    return "unknown"


def parse_tps(output: str) -> tuple[float | None, float | None]:
    matches = TPS_RE.findall(output)
    if not matches:
        return None, None
    prompt_tps, generation_tps = matches[-1]
    return float(prompt_tps), float(generation_tps)


def main() -> int:
    args = parse_args()
    batches = parse_csv_ints(args.batches)
    ctxs = parse_csv_ints(args.ctxs)
    kvs = parse_csv_strings(args.kvs)

    args.output.parent.mkdir(parents=True, exist_ok=True)

    with args.output.open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "batch",
                "ctx",
                "kv",
                "prompt_tps",
                "generation_tps",
                "status",
                "elapsed_s",
                "returncode",
                "ncmoe",
                "threads",
                "ngl",
            ]
        )

        for batch, ctx, kv in itertools.product(batches, ctxs, kvs):
            command = build_command(args, batch=batch, ctx=ctx, kv=kv)
            print(f"Running batch={batch} ctx={ctx} kv={kv}")
            output, returncode, elapsed_s = run_case(command, timeout=args.timeout)
            prompt_tps, generation_tps = parse_tps(output)
            status = parse_status(output, returncode)
            writer.writerow(
                [
                    batch,
                    ctx,
                    kv,
                    prompt_tps,
                    generation_tps,
                    status,
                    f"{elapsed_s:.2f}",
                    returncode,
                    args.ncmoe,
                    args.threads,
                    args.ngl,
                ]
            )
            handle.flush()

    print(f"Wrote results to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
