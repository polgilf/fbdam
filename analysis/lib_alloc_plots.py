
from pathlib import Path
import os
import pandas as pd
import matplotlib.pyplot as plt
from typing import Optional, Dict, List

DEFAULT_COLUMN_ALIASES = {
    "household_id": ["household_id", "household", "h", "hh_id"],
    "item_id": ["item_id", "item", "i", "product_id"],
    "quantity": ["quantity", "qty", "x", "alloc", "amount", "value"],
}

def _resolve_columns(df: pd.DataFrame, overrides: Optional[Dict[str, str]] = None) -> Dict[str, str]:
    overrides = overrides or {}
    resolved = {}
    for logical, aliases in DEFAULT_COLUMN_ALIASES.items():
        if logical in overrides:
            if overrides[logical] not in df.columns:
                raise KeyError(f"Override '{overrides[logical]}' not found in CSV columns: {list(df.columns)}")
            resolved[logical] = overrides[logical]
            continue
        for a in aliases:
            if a in df.columns:
                resolved[logical] = a
                break
        if logical not in resolved:
            raise KeyError(
                f"Required column for '{logical}' not found. "
                f"Looked for {aliases}. Available: {list(df.columns)}"
            )
    return resolved

def aggregate_allocations_per_household(csv_path: Path, column_overrides: Optional[Dict[str, str]] = None) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    cols = _resolve_columns(df, column_overrides)
    g = df.groupby(df[cols["household_id"]], as_index=False)[cols["quantity"]].sum()
    g.columns = ["household_id", "quantity"]
    g = g.sort_values("household_id").reset_index(drop=True)
    return g

def plot_allocated_food_bar(
    per_household_df: pd.DataFrame,
    output_png: Path,
    *,
    ylabel: str = "Total allocated quantity (sum of units)",
    title: str = "Allocated Food per Household",
    ymax: Optional[float] = None,
) -> Path:
    plt.figure(figsize=(8,5))
    plt.bar(per_household_df["household_id"], per_household_df["quantity"])
    plt.xlabel("Household")
    plt.ylabel(ylabel)
    plt.title(title)
    if ymax is not None:
        plt.ylim(top=ymax)
    for x, y in zip(per_household_df["household_id"], per_household_df["quantity"]):
        plt.text(x, y, f"{y:.1f}", ha="center", va="bottom")
    plt.tight_layout()
    output_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(output_png, dpi=150)
    plt.close()
    return output_png

def find_solution_csv(solution_dir: Path, candidates: Optional[List[str]] = None) -> Path:
    solution_dir = Path(solution_dir)
    candidates = candidates or ["solution.csv"]
    for name in candidates:
        p = solution_dir / name
        if p.exists():
            return p
    for root, _, files in os.walk(solution_dir):
        for name in candidates:
            if name in files:
                return Path(root) / name
    root_csvs = list(solution_dir.glob("*.csv"))
    if root_csvs:
        return root_csvs[0]
    for p in solution_dir.rglob("*.csv"):
        return p
    raise FileNotFoundError(f"No CSV found under {solution_dir}")
