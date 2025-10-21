import argparse
import json
import sys
from pathlib import Path

import pandas as pd
from lib_alloc_plots import (
    aggregate_allocations_per_household,
    plot_allocated_food_bar,
    find_solution_csv,
)

def _find_households_csv(solution_dir: Path) -> Path:
    config_snapshot = solution_dir / "config_snapshot.json"
    if config_snapshot.exists():
        with config_snapshot.open("r", encoding="utf-8") as f:
            config = json.load(f)
        data_section = config.get("data", {})
        for key in ("households_csv", "households"):
            path_str = data_section.get(key)
            if path_str:
                path = Path(path_str)
                if path.exists():
                    return path
        dataset_section = config.get("dataset", {})
        dataset_path = dataset_section.get("path")
        if dataset_path:
            candidate = Path(dataset_path) / "households.csv"
            if candidate.exists():
                return candidate
        dataset_id = dataset_section.get("id")
        if dataset_id:
            repo_root = Path(__file__).resolve().parents[1]
            candidate = repo_root / "data" / dataset_id / "households.csv"
            if candidate.exists():
                return candidate

    repo_root = Path(__file__).resolve().parents[1]
    data_dir = repo_root / "data"
    if data_dir.exists():
        solution_str = str(solution_dir)
        for dataset_dir in data_dir.iterdir():
            if dataset_dir.is_dir() and dataset_dir.name in solution_str:
                candidate = dataset_dir / "households.csv"
                if candidate.exists():
                    return candidate
        tokens = {token for part in solution_dir.parts for token in part.split("_")}
        for dataset_dir in data_dir.iterdir():
            if dataset_dir.is_dir() and dataset_dir.name in tokens:
                candidate = dataset_dir / "households.csv"
                if candidate.exists():
                    return candidate

    raise FileNotFoundError(
        f"Could not locate households.csv for solution directory '{solution_dir}'."
    )


def _parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Plot per-member food allocation from a solution directory."
    )
    parser.add_argument("solution_dir", type=Path, help="Directory containing a solution CSV.")
    parser.add_argument(
        "output_png",
        type=Path,
        nargs="?",
        help="Path to save the output plot PNG (defaults inside the solution directory).",
    )
    parser.add_argument(
        "--ymax",
        type=float,
        default=None,
        help="Upper limit for the y-axis (per-member allocation). Auto when omitted.",
    )
    return parser.parse_args(argv[1:])

def main(argv):
    args = _parse_args(argv)
    solution_dir = args.solution_dir
    output_png = args.output_png or solution_dir / "allocated_food_by_household.png"

    csv_path = find_solution_csv(solution_dir)
    per_hh = aggregate_allocations_per_household(csv_path)
    households_csv = _find_households_csv(solution_dir)
    households = pd.read_csv(households_csv, usecols=["household_id", "members"])
    per_hh = per_hh.merge(households, on="household_id", how="left")
    if per_hh["members"].isnull().any():
        missing = per_hh.loc[per_hh["members"].isnull(), "household_id"].tolist()
        raise ValueError(
            f"Missing 'members' count for households {missing} in {households_csv}"
        )
    if (per_hh["members"] <= 0).any():
        zero_or_negative = per_hh.loc[per_hh["members"] <= 0, "household_id"].tolist()
        raise ValueError(
            "Household member count must be positive to compute per-member allocation. "
            f"Problem households: {zero_or_negative} from {households_csv}"
        )

    per_hh["quantity"] = per_hh["quantity"] / per_hh["members"]
    per_hh = per_hh.sort_values("household_id").reset_index(drop=True)

    plot_allocated_food_bar(
        per_hh,
        output_png,
        ylabel="Allocated quantity per member (units/person)",
        title="Allocated Food per Household (per member)",
        ymax=args.ymax,
    )
    print(f"CSV: {csv_path}")
    print(f"Households: {households_csv}")
    print(f"Plot saved to: {output_png}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
