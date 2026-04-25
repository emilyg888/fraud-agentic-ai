from __future__ import annotations

import argparse
import glob
from pathlib import Path

import pandas as pd


def parse_args() -> argparse.Namespace:
    project_root = Path(__file__).resolve().parent
    parser = argparse.ArgumentParser(
        description="Merge llama.cpp benchmark CSVs and render 3D scatter/surface plots."
    )
    parser.add_argument(
        "inputs",
        nargs="+",
        help="Input CSV files, globs, or directories containing benchmark CSVs.",
    )
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=project_root / "benchmark_plots",
        help="Directory for merged CSV and plot images.",
    )
    parser.add_argument(
        "--metric",
        choices=["generation_tps", "prompt_tps"],
        default="generation_tps",
        help="Metric to plot on the Z axis.",
    )
    parser.add_argument(
        "--status",
        default="ok",
        help="Only plot rows with this status. Use 'all' to keep every row.",
    )
    parser.add_argument(
        "--plot",
        choices=["scatter", "surface", "both"],
        default="both",
        help="Plot type to render.",
    )
    return parser.parse_args()


def resolve_inputs(inputs: list[str]) -> list[Path]:
    resolved: list[Path] = []

    for raw in inputs:
        matches = [Path(match) for match in glob.glob(raw)]
        if matches:
            for match in matches:
                if match.is_dir():
                    resolved.extend(sorted(match.glob("*.csv")))
                else:
                    resolved.append(match)
            continue

        candidate = Path(raw)
        if candidate.is_dir():
            resolved.extend(sorted(candidate.glob("*.csv")))
        else:
            resolved.append(candidate)

    unique: list[Path] = []
    seen: set[str] = set()
    for path in resolved:
        key = str(path.resolve()) if path.exists() else str(path)
        if key in seen:
            continue
        seen.add(key)
        unique.append(path)
    return unique


def load_results(paths: list[Path], status: str) -> pd.DataFrame:
    frames: list[pd.DataFrame] = []
    for path in paths:
        frame = pd.read_csv(path)
        frame["source_file"] = path.name
        frames.append(frame)

    merged = pd.concat(frames, ignore_index=True)
    if status != "all":
        merged = merged[merged["status"] == status].copy()

    merged["batch"] = pd.to_numeric(merged["batch"], errors="coerce")
    merged["ctx"] = pd.to_numeric(merged["ctx"], errors="coerce")
    merged["prompt_tps"] = pd.to_numeric(merged["prompt_tps"], errors="coerce")
    merged["generation_tps"] = pd.to_numeric(merged["generation_tps"], errors="coerce")
    merged = merged.dropna(subset=["batch", "ctx", "kv"])
    return merged


def render_scatter(data: pd.DataFrame, metric: str, output_path: Path) -> None:
    import matplotlib.pyplot as plt

    fig = plt.figure(figsize=(11, 8))
    ax = fig.add_subplot(111, projection="3d")

    for kv, frame in sorted(data.groupby("kv")):
        ax.scatter(
            frame["ctx"],
            frame["batch"],
            frame[metric],
            label=kv,
            s=70,
            alpha=0.85,
        )

    ax.set_xlabel("Context")
    ax.set_ylabel("Batch")
    ax.set_zlabel(metric.replace("_", " "))
    ax.set_title(f"llama.cpp benchmark scatter ({metric})")
    ax.legend(title="KV")
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def render_surfaces(data: pd.DataFrame, metric: str, output_path: Path) -> None:
    import matplotlib.pyplot as plt
    import numpy as np

    kv_groups = sorted(data.groupby("kv"))
    if not kv_groups:
        raise ValueError("No data available for surface plot.")

    fig = plt.figure(figsize=(6 * len(kv_groups), 6))

    for index, (kv, frame) in enumerate(kv_groups, start=1):
        ax = fig.add_subplot(1, len(kv_groups), index, projection="3d")
        pivot = (
            frame.pivot_table(index="batch", columns="ctx", values=metric, aggfunc="mean")
            .sort_index()
            .sort_index(axis=1)
        )
        x_vals = pivot.columns.to_numpy(dtype=float)
        y_vals = pivot.index.to_numpy(dtype=float)
        xx, yy = np.meshgrid(x_vals, y_vals)
        zz = pivot.to_numpy(dtype=float)

        mask = ~np.isnan(zz)
        if mask.any():
            ax.plot_surface(
                xx,
                yy,
                np.where(mask, zz, np.nan),
                cmap="viridis",
                linewidth=0,
                antialiased=True,
                alpha=0.9,
            )

        ax.set_title(f"{kv}")
        ax.set_xlabel("Context")
        ax.set_ylabel("Batch")
        ax.set_zlabel(metric.replace("_", " "))

    fig.suptitle(f"llama.cpp benchmark surfaces ({metric})", y=0.98)
    fig.tight_layout()
    fig.savefig(output_path, dpi=180)
    plt.close(fig)


def main() -> int:
    args = parse_args()
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    input_paths = resolve_inputs(args.inputs)
    if not input_paths:
        raise SystemExit("No input CSV files matched.")

    merged = load_results(input_paths, status=args.status)
    if merged.empty:
        raise SystemExit("No rows matched the requested filters.")

    merged_csv = output_dir / "merged_results.csv"
    merged.to_csv(merged_csv, index=False)

    if args.plot in {"scatter", "both"}:
        render_scatter(merged, metric=args.metric, output_path=output_dir / f"scatter_{args.metric}.png")

    if args.plot in {"surface", "both"}:
        render_surfaces(merged, metric=args.metric, output_path=output_dir / f"surface_{args.metric}.png")

    print(f"Merged CSV: {merged_csv}")
    if args.plot in {"scatter", "both"}:
        print(f"Scatter plot: {output_dir / f'scatter_{args.metric}.png'}")
    if args.plot in {"surface", "both"}:
        print(f"Surface plot: {output_dir / f'surface_{args.metric}.png'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
