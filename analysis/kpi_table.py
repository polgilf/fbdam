"""Utilities to assemble KPI comparison tables across datasets and configs."""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import pandas as pd
import yaml


@dataclass(frozen=True)
class KpiDefinition:
    """Lightweight representation of a KPI entry from ``kpis.yaml``."""

    id: str
    label: str | None = None

    @property
    def path(self) -> tuple[str, ...]:
        """Return the hierarchical path for the KPI (e.g. ``("basic", "items")``)."""

        return tuple(part for part in self.id.split(".") if part)

    @property
    def display_name(self) -> str:
        """Return a human-friendly name for the KPI."""

        return self.label or self.id


def load_kpi_catalog(catalog_path: Path) -> list[KpiDefinition]:
    """Load KPI definitions from a YAML file.

    The YAML structure can either be a mapping with a ``kpis`` key or a list where each
    entry is either a string (``section.metric``) or a mapping with ``id`` and optional
    ``label`` keys.
    """

    if not catalog_path.exists():
        msg = f"KPI catalog not found: {catalog_path}"
        raise FileNotFoundError(msg)

    raw_data = yaml.safe_load(catalog_path.read_text(encoding="utf-8"))
    if raw_data is None:
        return []

    if isinstance(raw_data, Mapping):
        entries = raw_data.get("kpis")
        if entries is None:
            msg = "KPI catalog mapping must contain a 'kpis' key"
            raise ValueError(msg)
    elif isinstance(raw_data, Sequence) and not isinstance(raw_data, (str, bytes)):
        entries = raw_data
    else:
        msg = "Unsupported KPI catalog format"
        raise TypeError(msg)

    definitions: list[KpiDefinition] = []
    for entry in entries:
        if isinstance(entry, str):
            definitions.append(KpiDefinition(id=entry))
        elif isinstance(entry, Mapping):
            identifier = entry.get("id")
            if not identifier:
                msg = "Each KPI mapping must include an 'id'"
                raise ValueError(msg)
            definitions.append(
                KpiDefinition(
                    id=str(identifier),
                    label=str(entry.get("label")) if entry.get("label") else None,
                )
            )
        else:
            msg = f"Unsupported KPI entry type: {type(entry)!r}"
            raise TypeError(msg)

    return definitions


def extract_nested_value(data: Mapping[str, Any], path: Iterable[str]) -> Any:
    """Return a nested value from ``data`` following ``path``; ``None`` if missing."""

    current: Any = data
    for segment in path:
        if not isinstance(current, Mapping):
            return None
        current = current.get(segment)
        if current is None:
            return None
    return current


def load_latest_kpis(
    dataset_id: str,
    config_id: str,
    runs_root: Path,
) -> Mapping[str, Any]:
    """Load KPI metrics from the most recent run for ``dataset_id``/``config_id``.

    Parameters
    ----------
    dataset_id:
        Dataset identifier (matches the ``runs/{dataset_id}`` folder).
    config_id:
        Configuration identifier (matches ``runs/{dataset_id}/{config_id}``).
    runs_root:
        Base directory that stores run outputs.
    """

    base_dir = runs_root / dataset_id / config_id
    if not base_dir.exists():
        return {}

    run_dirs = [path for path in base_dir.iterdir() if path.is_dir()]
    if not run_dirs:
        return {}

    latest_dir = max(run_dirs, key=lambda path: path.name)
    kpi_path = latest_dir / "kpis.json"
    if not kpi_path.exists():
        return {}

    with kpi_path.open(encoding="utf-8") as f:
        payload = json.load(f)

    kpi_section = payload.get("kpi")
    return kpi_section if isinstance(kpi_section, Mapping) else {}


def build_kpi_dataframe(
    dataset_ids: Sequence[str],
    config_ids: Sequence[str],
    runs_root: Path | None = None,
    catalog_path: Path | None = None,
) -> pd.DataFrame:
    """Assemble a KPI DataFrame indexed by KPI definitions.

    Parameters
    ----------
    dataset_ids:
        Ordered list of dataset identifiers to include as column groups.
    config_ids:
        Ordered list of configuration identifiers to include within each dataset.
    runs_root:
        Directory that stores run outputs; defaults to ``runs`` in the project root.
    catalog_path:
        Path to the ``kpis.yaml`` catalog.
    """

    runs_root = runs_root or Path("runs")
    catalog_path = catalog_path or Path("analysis") / "kpis.yaml"

    definitions = load_kpi_catalog(catalog_path)
    index = pd.Index([definition.display_name for definition in definitions], name="kpi")
    columns = pd.MultiIndex.from_product(
        [dataset_ids, config_ids], names=["dataset_id", "config_id"]
    )
    frame = pd.DataFrame(index=index, columns=columns, dtype="object")

    for dataset_id in dataset_ids:
        for config_id in config_ids:
            metrics = load_latest_kpis(dataset_id, config_id, runs_root)
            for definition in definitions:
                value = extract_nested_value(metrics, definition.path)
                frame.loc[definition.display_name, (dataset_id, config_id)] = value

    return frame


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a KPI table for the given datasets and configs."
    )
    parser.add_argument(
        "--datasets",
        nargs="+",
        required=True,
        help="Dataset identifiers to include (e.g. ds-a ds-b).",
    )
    parser.add_argument(
        "--configs",
        nargs="+",
        required=True,
        help="Configuration identifiers to include (e.g. dials-balanced).",
    )
    parser.add_argument(
        "--runs-dir",
        type=Path,
        default=Path("runs"),
        help="Root directory that contains run outputs (defaults to ./runs).",
    )
    parser.add_argument(
        "--catalog",
        type=Path,
        default=Path("analysis") / "kpis.yaml",
        help="Path to the KPI catalog (defaults to analysis/kpis.yaml).",
    )
    return parser.parse_args()


def main() -> None:
    args = _parse_args()
    dataframe = build_kpi_dataframe(
        dataset_ids=args.datasets,
        config_ids=args.configs,
        runs_root=args.runs_dir,
        catalog_path=args.catalog,
    )
    with pd.option_context("display.max_rows", None, "display.max_columns", None):
        print(dataframe)


if __name__ == "__main__":
    main()
