import argparse
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import yaml


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plot KPI visuals from a generated CSV table."
    )
    parser.add_argument(
        "csv_path",
        nargs="?",
        default="analysis/tables/kpis.csv",
        help="Path to the KPI CSV file (default: analysis/tables/kpis.csv).",
    )
    parser.add_argument(
        "--catalog",
        default="analysis/kpis.yaml",
        help="Optional KPI catalog to map display labels to canonical ids.",
    )
    return parser.parse_args()


def load_label_mapping(catalog_path: Path) -> dict[str, str]:
    if not catalog_path.exists():
        return {}

    raw = yaml.safe_load(catalog_path.read_text(encoding="utf-8")) or {}
    entries = raw.get("kpis", raw)
    mapping: dict[str, str] = {}

    def canonical_name(identifier: str) -> str:
        return identifier.split(".")[-1]

    if isinstance(entries, list):
        for entry in entries:
            if isinstance(entry, str):
                identifier = entry
                label = entry.split(".")[-1].replace("_", " ").title()
            elif isinstance(entry, dict):
                identifier = str(entry.get("id", "")).strip()
                label = str(entry.get("label", "")).strip() or identifier
            else:
                continue

            if not identifier:
                continue

            canonical = canonical_name(identifier)
            if label:
                mapping[label] = canonical
            mapping[identifier] = canonical

    return mapping


def to_snake_case(value: str) -> str:
    cleaned = value.strip().lower().replace("/", " ")
    return "_".join(segment for segment in cleaned.split() if segment)


def load_kpi_wide_table(csv_path: Path, catalog_path: Path) -> pd.DataFrame:
    table = pd.read_csv(csv_path, header=[0, 1], index_col=0)

    label_mapping = load_label_mapping(catalog_path)
    table.index = [
        label_mapping.get(label, to_snake_case(label)) for label in table.index
    ]
    table.index.name = "kpi_id"

    tidy = table.stack(["dataset_id", "config_id"]).rename("value").reset_index()
    tidy["scenario"] = tidy["dataset_id"] + " :: " + tidy["config_id"]

    wide = tidy.pivot_table(
        index="scenario", columns="kpi_id", values="value", aggfunc="first"
    )
    wide = wide.reset_index()

    numeric_columns = wide.columns.difference(["scenario"])
    wide[numeric_columns] = wide[numeric_columns].apply(pd.to_numeric, errors="coerce")
    return wide


def make_plots(df: pd.DataFrame, source_path: Path) -> None:
    required_columns = {
        "global_mean_deviation_from_fair_share",
        "global_mean_utility",
        "min_mean_utility_per_nutrient",
        "min_overall_utility",
        "max_mean_deviation_from_fair_share_per_household",
    }
    missing = required_columns - set(df.columns)
    if missing:
        missing_cols = ", ".join(sorted(missing))
        raise ValueError(
            f"Missing required KPI columns in {source_path}: {missing_cols}. "
            "Ensure the catalog and CSV are up to date."
        )

    # 1. Global trade-off
    sns.scatterplot(
        data=df,
        x="global_mean_deviation_from_fair_share",
        y="global_mean_utility",
        hue="scenario",
    )
    plt.xlabel("Mean deviation from fair share (lower = better)")
    plt.ylabel("Mean utility (higher = better)")
    plt.title("Equity–Efficiency Trade-off Map")
    plt.tight_layout()
    plt.show()

    # 2. Nutritional adequacy breakdown
    nutr_candidates = [
        "min_mean_utility_per_nutrient",
        "global_mean_utility",
        "min_overall_utility",
    ]
    nutr_cols = [col for col in nutr_candidates if col in df.columns]
    if nutr_cols:
        df.set_index("scenario")[nutr_cols].T.plot(kind="bar")
        plt.title("Nutritional Adequacy Overview")
        plt.ylabel("Utility (0–1)")
        plt.tight_layout()
        plt.show()

    # 3. Household fairness breakdown
    if "max_mean_deviation_from_fair_share_per_household" in df.columns:
        sns.barplot(
            data=df,
            x="scenario",
            y="max_mean_deviation_from_fair_share_per_household",
            palette="viridis"
        )
        plt.title("Household Fairness Deviation")
        plt.ylabel("Deviation from fair share")
        plt.xlabel("Scenario")
        plt.tight_layout()
        plt.show()

    # 4. KPI heatmap
    kpi_cols = [
        col
        for col in df.columns
        if col not in {"scenario"} and df[col].dtype != object
    ]
    if kpi_cols:
        corr = df[kpi_cols].corr()
        sns.heatmap(corr, annot=True, cmap="coolwarm")
        plt.title("KPI Correlation Map")
        plt.tight_layout()
        plt.show()


def main() -> None:
    args = parse_args()
    df_path = Path(args.csv_path)
    catalog_path = Path(args.catalog)

    if not df_path.exists():
        raise FileNotFoundError(f"KPI CSV not found at: {df_path}")

    df = load_kpi_wide_table(df_path, catalog_path)
    make_plots(df, df_path)


if __name__ == "__main__":
    main()
