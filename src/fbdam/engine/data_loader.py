"""Utilities to materialize the optimization domain from CSV datasets.

This module is responsible for reading the tabular inputs referenced by a
scenario configuration (already validated/normalized by ``io.py``) and
returning domain objects ready to be consumed by the model builder.

The loader is intentionally light-weight and only depends on the standard
library in order to keep import times small and to avoid introducing optional
dependencies (pandas, etc.).
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Tuple
import csv

from fbdam.engine.domain import (
    AllocationBounds,
    DomainIndex,
    Household,
    Item,
    ItemNutrient,
    Nutrient,
    Requirement,
)


class DataLoaderError(RuntimeError):
    """Raised when a dataset cannot be parsed into the domain model."""


@dataclass(frozen=True)
class DataBundle:
    """Container returned by :func:`load_domain_and_params`."""

    domain: DomainIndex
    model_params: Dict[str, Any]


def load_domain_and_params(
    data_paths: Mapping[str, Path],
    model_section: Mapping[str, Any],
) -> DataBundle:
    """Read CSV datasets and scenario parameters into domain objects.

    Args:
        data_paths: Mapping of logical dataset names to *absolute* file paths.
        model_section: Raw ``model`` section from the scenario YAML. Only the
            scalar parameters (dials, budget, etc.) are consumed here; the
            constraint/objective catalogs remain untouched.

    Returns:
        :class:`DataBundle` with an assembled :class:`DomainIndex` and a
        dictionary of model parameters.
    """

    required_keys = {
        "items_csv",
        "nutrients_csv",
        "households_csv",
        "requirements_csv",
        "item_nutrients_csv",
        "household_item_bounds_csv",
    }
    missing = sorted(k for k in required_keys if k not in data_paths)
    if missing:
        raise DataLoaderError(f"Missing dataset paths: {', '.join(missing)}")

    items = _read_items(Path(data_paths["items_csv"]))
    nutrients = _read_nutrients(Path(data_paths["nutrients_csv"]))
    households = _read_households(Path(data_paths["households_csv"]))
    requirements = _read_requirements(Path(data_paths["requirements_csv"]))
    item_nutrients = _read_item_nutrients(Path(data_paths["item_nutrients_csv"]))
    bounds = _read_bounds(Path(data_paths["household_item_bounds_csv"]))

    domain = DomainIndex(
        items=items,
        nutrients=nutrients,
        households=households,
        item_nutrients=item_nutrients,
        requirements=requirements,
        bounds=bounds,
    )

    model_params = _extract_model_params(model_section)

    return DataBundle(domain=domain, model_params=model_params)


# ---------------------------------------------------------------------------
# CSV readers
# ---------------------------------------------------------------------------


def _read_items(path: Path) -> Dict[str, Item]:
    rows = _read_csv(path, required_columns={"item_id", "name", "stock"})
    items: Dict[str, Item] = {}
    for row in rows:
        item_id = row["item_id"].strip()
        unit = row.get("unit") or None
        metadata = _extract_metadata(row, {"item_id", "name", "unit", "stock", "cost"})
        items[item_id] = Item(
            item_id=item_id,
            name=row["name"].strip(),
            stock=_to_float(row["stock"], field="stock", context=f"item '{item_id}'"),
            cost=_to_float(row.get("cost", 0.0) or 0.0, field="cost", context=f"item '{item_id}'"),
            unit=unit.strip() if isinstance(unit, str) and unit.strip() else None,
            metadata=metadata or None,
        )
    return items


def _read_nutrients(path: Path) -> Dict[str, Nutrient]:
    rows = _read_csv(path, required_columns={"nutrient_id", "name"})
    nutrients: Dict[str, Nutrient] = {}
    for row in rows:
        nutrient_id = row["nutrient_id"].strip()
        unit = row.get("unit") or None
        metadata = _extract_metadata(row, {"nutrient_id", "name", "unit"})
        nutrients[nutrient_id] = Nutrient(
            nutrient_id=nutrient_id,
            name=row["name"].strip(),
            unit=unit.strip() if isinstance(unit, str) and unit.strip() else None,
            metadata=metadata or None,
        )
    return nutrients


def _read_households(path: Path) -> Dict[str, Household]:
    rows = _read_csv(path, required_columns={"household_id", "name"})
    households: Dict[str, Household] = {}
    for row in rows:
        household_id = row["household_id"].strip()
        fairshare_weight_value = (
            row.get("fairshare_weight")
            or row.get("gamma")
            or row.get("weight")
            or row.get("fairshare")
            or 1.0
        )
        metadata = _extract_metadata(
            row,
            {"household_id", "name", "gamma", "fairshare_weight", "weight", "fairshare"},
        )
        households[household_id] = Household(
            household_id=household_id,
            name=row["name"].strip(),
            fairshare_weight=_to_float(
                fairshare_weight_value,
                field="fairshare_weight",
                context=f"household '{household_id}'",
            ),
            group=row.get("group") or None,
            metadata=metadata or None,
        )
    return households


def _read_requirements(path: Path) -> Dict[Tuple[str, str], Requirement]:
    rows = _read_csv(
        path,
        required_columns={"household_id", "nutrient_id"},
        numeric_columns={"requirement", "amount"},
    )
    requirements: Dict[Tuple[str, str], Requirement] = {}
    for row in rows:
        household_id = row["household_id"].strip()
        nutrient_id = row["nutrient_id"].strip()
        amount = row.get("requirement", row.get("amount", 0.0))
        requirements[(household_id, nutrient_id)] = Requirement(
            household_id=household_id,
            nutrient_id=nutrient_id,
            amount=_to_float(
                amount,
                field="requirement",
                context=f"requirement ({household_id}, {nutrient_id})",
            ),
        )
    return requirements


def _read_item_nutrients(path: Path) -> Dict[Tuple[str, str], ItemNutrient]:
    rows = _read_csv(
        path,
        required_columns={"item_id", "nutrient_id", "qty_per_unit"},
    )
    contents: Dict[Tuple[str, str], ItemNutrient] = {}
    for row in rows:
        item_id = row["item_id"].strip()
        nutrient_id = row["nutrient_id"].strip()
        qty = _to_float(
            row["qty_per_unit"],
            field="qty_per_unit",
            context=f"item nutrient ({item_id}, {nutrient_id})",
        )
        contents[(item_id, nutrient_id)] = ItemNutrient(
            item_id=item_id,
            nutrient_id=nutrient_id,
            qty_per_unit=qty,
        )
    return contents


def _read_bounds(path: Path) -> Dict[Tuple[str, str], AllocationBounds]:
    rows = _read_csv(path, required_columns={"household_id", "item_id"})
    bounds: Dict[Tuple[str, str], AllocationBounds] = {}
    for row in rows:
        household_id = row["household_id"].strip()
        item_id = row["item_id"].strip()
        lower = _optional_float(row.get("lower"), default=0.0)
        upper = _optional_float(row.get("upper"), default=None)
        bounds[(item_id, household_id)] = AllocationBounds(
            item_id=item_id,
            household_id=household_id,
            lower=lower,
            upper=upper,
        )
    return bounds


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _extract_model_params(model_section: Mapping[str, Any]) -> Dict[str, Any]:
    if not isinstance(model_section, Mapping):
        model_section = {}

    params: Dict[str, Any] = {}

    dials = model_section.get("dials", {}) if model_section else {}
    if dials:
        if not isinstance(dials, Mapping):
            raise DataLoaderError("model.dials must be a mapping")
        params["dials"] = {k: _to_float(v, field=k, context="model.dials") for k, v in dials.items()}
    else:
        params["dials"] = {}

    if "budget" in model_section:
        params["budget"] = _to_float(
            model_section.get("budget", 0.0),
            field="budget",
            context="model",
        )

    for key in ("lambda", "lambda_", "lam" ):
        if key in model_section:
            params[key] = _to_float(model_section[key], field=key, context="model")

    return params


def _read_csv(
    path: Path,
    *,
    required_columns: Iterable[str],
    numeric_columns: Iterable[str] | None = None,
) -> Iterable[Dict[str, Any]]:
    if not path.is_file():
        raise DataLoaderError(f"Dataset not found: {path}")

    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        header = set(reader.fieldnames or [])
        missing = sorted(set(required_columns) - header)
        if missing:
            raise DataLoaderError(
                f"CSV {path.name} missing required columns: {', '.join(missing)}"
            )

        numeric_columns = set(numeric_columns or [])

        rows = []
        for row in reader:
            # Normalize numeric columns eagerly if present
            for col in numeric_columns:
                if col in row and row[col] == "":
                    row[col] = None
            rows.append(row)
    return rows


def _extract_metadata(row: Mapping[str, Any], known_columns: Iterable[str]) -> Dict[str, Any]:
    known = set(known_columns)
    metadata = {
        key: value
        for key, value in row.items()
        if key not in known and value not in (None, "")
    }
    return metadata


def _to_float(value: Any, *, field: str, context: str) -> float:
    try:
        if value is None or value == "":
            return 0.0
        return float(value)
    except (TypeError, ValueError) as exc:
        raise DataLoaderError(
            f"Cannot parse field '{field}' in {context} as float (value={value!r})."
        ) from exc


def _optional_float(value: Any, *, default: float | None) -> float | None:
    if value in (None, ""):
        return default
    return _to_float(value, field="value", context="bounds")

