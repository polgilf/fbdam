"""
data_loader.py — CSV to DomainIndex loader
------------------------------------------
Responsibility:
- Read CSV files and convert them into typed domain dataclasses.
- Load model parameters (dials, budget, etc.) from YAML or defaults.
- Return a DataBundle ready for model building.

Design notes:
- Uses stdlib csv module (no pandas dependency for data loading).
- Streaming API for memory efficiency.
- Strong validation at load time.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Iterable, Mapping, Tuple

from fbdam.engine.domain import (
    DomainIndex,
    Item,
    ItemId,
    Nutrient,
    NutrientId,
    Household,
    HouseholdId,
    Requirement,
    ItemNutrient,
    AllocationBounds,
)


# ----------------------------- Exceptions ------------------------------------


class DataLoaderError(RuntimeError):
    """Raised when CSV loading or validation fails."""


# ----------------------------- Data structures -------------------------------


@dataclass(frozen=True)
class DataBundle:
    """
    Container returned by :func:`load_domain_and_params`.
    
    Attributes:
        domain: Fully populated DomainIndex (items, households, nutrients, etc.)
        model_params: Model configuration parameters (dials, budget, epsilon, etc.)
    """
    domain: DomainIndex
    model_params: Dict[str, Any]


# ----------------------------- Public API ------------------------------------


def load_domain_and_params(
    data_paths: Mapping[str, Path],
    model_section: Mapping[str, Any],
) -> DataBundle:
    """
    Load domain entities from CSVs and extract model parameters.
    
    Args:
        data_paths: Dict with keys:
                    - items (required)
                    - nutrients (required)
                    - households (required)
                    - requirements (required)
                    - item_nutrients (required)
                    - bounds (optional)
                    - params (optional) ← YAML with dials/budget
        
        model_section: Model config from scenario YAML (constraints, objectives)
    
    Returns:
        DataBundle: Domain + model parameters ready for build_model()
        
    Raises:
        DataLoaderError: If CSVs are malformed or missing required columns
    """
    
    # 1. Load domain entities from CSVs
    items = _load_items(data_paths.get("items"))
    nutrients = _load_nutrients(data_paths.get("nutrients"))
    households = _load_households(data_paths.get("households"))
    item_nutrients = _load_item_nutrients(data_paths.get("item_nutrients"))
    requirements = _load_requirements(data_paths.get("requirements"))
    bounds = _load_bounds(data_paths.get("bounds"))
    
    # 2. Validate referential integrity
    _validate_references(items, nutrients, households, item_nutrients, requirements, bounds)
    
    domain = DomainIndex(
        items=items,
        nutrients=nutrients,
        households=households,
        item_nutrients=item_nutrients,
        requirements=requirements,
        bounds=bounds,
    )
    
    # 3. Load model parameters (dials, budget, etc.)
    model_params = _load_model_params(data_paths.get("params"), model_section)
    
    return DataBundle(domain=domain, model_params=model_params)


# ----------------------------- CSV reading utilities -------------------------


def _read_csv(
    path: Path,
    *,
    required_columns: Iterable[str],
    numeric_columns: Iterable[str] | None = None,
) -> Iterable[Dict[str, Any]]:
    """
    Read CSV file and yield rows as dicts with basic validation and type coercion.
    
    Args:
        path: Path to CSV file
        required_columns: Columns that must exist (raises if missing)
        numeric_columns: Columns to coerce to float (optional)
    
    Yields:
        Dict[str, Any]: Row with string keys and coerced values
        
    Raises:
        DataLoaderError: If file not found or columns missing
    """
    if not path.is_file():
        raise DataLoaderError(f"Dataset not found: {path}")
    
    numeric_cols = set(numeric_columns or [])
    required_cols = set(required_columns)
    
    with path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        
        # Validate header
        if reader.fieldnames is None:
            raise DataLoaderError(f"{path.name}: Empty or malformed CSV (no header)")
        
        found_cols = set(reader.fieldnames)
        missing = required_cols - found_cols
        if missing:
            raise DataLoaderError(
                f"{path.name}: Missing required columns: {missing}. "
                f"Found: {found_cols}"
            )
        
        # Yield rows with type coercion
        for row_num, row in enumerate(reader, start=2):  # start=2 (header is row 1)
            # Coerce numeric columns
            for col in numeric_cols:
                if col in row and row[col]:
                    try:
                        row[col] = float(row[col])
                    except ValueError as e:
                        raise DataLoaderError(
                            f"{path.name}:{row_num}: Cannot convert '{col}'='{row[col]}' to float"
                        ) from e
            yield row


# ----------------------------- Loaders per entity ----------------------------


def _load_items(path: Path | None) -> Dict[ItemId, Item]:
    """Load items from CSV."""
    if not path:
        raise DataLoaderError("Missing 'items' path in data_paths")
    
    items = {}
    for row in _read_csv(
        path,
        required_columns=["item_id", "name", "stock"],
        numeric_columns=["stock", "cost"],
    ):
        item_id = str(row["item_id"])
        items[item_id] = Item(
            item_id=item_id,
            name=str(row["name"]),
            stock=float(row["stock"]),
            cost=float(row.get("cost") or 0.0),
            unit=str(row.get("unit") or "") or None,
        )
    
    return items


def _load_nutrients(path: Path | None) -> Dict[NutrientId, Nutrient]:
    """Load nutrients from CSV."""
    if not path:
        raise DataLoaderError("Missing 'nutrients' path in data_paths")
    
    nutrients = {}
    for row in _read_csv(
        path,
        required_columns=["nutrient_id", "name"],
        numeric_columns=[],
    ):
        nutrient_id = str(row["nutrient_id"])
        nutrients[nutrient_id] = Nutrient(
            nutrient_id=nutrient_id,
            name=str(row["name"]),
            unit=str(row.get("unit") or "") or None,
        )
    
    return nutrients


def _load_households(path: Path | None) -> Dict[HouseholdId, Household]:
    """Load households from CSV."""
    if not path:
        raise DataLoaderError("Missing 'households' path in data_paths")
    
    households = {}
    for row in _read_csv(
        path,
        required_columns=["household_id", "name"],
        numeric_columns=["fairshare_weight"],
    ):
        household_id = str(row["household_id"])
        households[household_id] = Household(
            household_id=household_id,
            name=str(row["name"]),
            fairshare_weight=float(row.get("fairshare_weight") or 1.0),
        )
    
    return households


def _load_item_nutrients(path: Path | None) -> Dict[Tuple[ItemId, NutrientId], ItemNutrient]:
    """Load item-nutrient content matrix from CSV."""
    if not path:
        raise DataLoaderError("Missing 'item_nutrients' path in data_paths")
    
    item_nutrients = {}
    for row in _read_csv(
        path,
        required_columns=["item_id", "nutrient_id", "qty_per_unit"],
        numeric_columns=["qty_per_unit"],
    ):
        key = (str(row["item_id"]), str(row["nutrient_id"]))
        item_nutrients[key] = ItemNutrient(
            item_id=str(row["item_id"]),
            nutrient_id=str(row["nutrient_id"]),
            qty_per_unit=float(row["qty_per_unit"]),
        )
    
    return item_nutrients


def _load_requirements(path: Path | None) -> Dict[Tuple[HouseholdId, NutrientId], Requirement]:
    """Load household-nutrient requirements from CSV."""
    if not path:
        raise DataLoaderError("Missing 'requirements' path in data_paths")
    
    requirements = {}
    for row in _read_csv(
        path,
        required_columns=["household_id", "nutrient_id", "requirement"],
        numeric_columns=["requirement"],
    ):
        key = (str(row["household_id"]), str(row["nutrient_id"]))
        requirements[key] = Requirement(
            household_id=str(row["household_id"]),
            nutrient_id=str(row["nutrient_id"]),
            amount=float(row["requirement"]),
        )
    
    return requirements


def _load_bounds(path: Path | None) -> Dict[Tuple[ItemId, HouseholdId], AllocationBounds]:
    """Load allocation bounds from CSV (optional)."""
    if not path or not path.exists():
        return {}
    
    bounds = {}
    for row in _read_csv(
        path,
        required_columns=["item_id", "household_id"],
        numeric_columns=["lower", "upper"],
    ):
        key = (str(row["item_id"]), str(row["household_id"]))
        
        # Handle optional upper bound
        upper_val = row.get("upper")
        upper = float(upper_val) if upper_val not in (None, "", "None") else None
        
        bounds[key] = AllocationBounds(
            item_id=str(row["item_id"]),
            household_id=str(row["household_id"]),
            lb=float(row.get("lower") or 0.0),
            ub=upper,
        )
    
    return bounds


# ----------------------------- Model parameters ------------------------------


def _load_model_params(params_path: Path | None, model_section: Mapping[str, Any]) -> Dict[str, Any]:
    """
    Load model parameters (dials, budget, etc.) from optional YAML file.
    
    Priority:
    1. params.yaml (if exists)
    2. Defaults from model_section (constraints params)
    3. Hard-coded defaults
    
    Returns:
        Dict with keys: budget, lambda_penalty, alpha, beta, gamma, kappa, rho, omega
    """
    import yaml
    
    # Start with defaults
    params = {
        "budget": None,               # No budget constraint by default
        "lambda_penalty": 0.0,        # No epsilon penalty by default
        "alpha": 0.5,                 # Item-level deviation cap
        "beta": 0.5,                  # Household-level deviation cap
        "gamma": 0.8,                 # Per-nutrient floor
        "kappa": 0.8,                 # Per-pair floor
        "rho": 0.5,                   # Per-pair deviation cap
        "omega": 0.8,                 # Per-household floor (aggregate over nutrients)
    }
    
    # Load from params.yaml if exists
    if params_path and params_path.exists():
        with open(params_path, "r") as f:
            file_params = yaml.safe_load(f) or {}
        params.update(file_params)
    
    # Override with constraint-level params from model_section
    for c in model_section.get("constraints", []):
        if "params" in c:
            params.update(c["params"])
    
    return params


# ----------------------------- Validation ------------------------------------


def _validate_references(
    items: Dict[ItemId, Item],
    nutrients: Dict[NutrientId, Nutrient],
    households: Dict[HouseholdId, Household],
    item_nutrients: Dict[Tuple[ItemId, NutrientId], ItemNutrient],
    requirements: Dict[Tuple[HouseholdId, NutrientId], Requirement],
    bounds: Dict[Tuple[ItemId, HouseholdId], AllocationBounds],
) -> None:
    """
    Validate referential integrity across loaded entities.
    """
    
    # Check item_nutrients
    for (item_id, nutrient_id), _ in item_nutrients.items():
        if item_id not in items:
            raise DataLoaderError(
                f"item_nutrients references unknown item_id='{item_id}'"
            )
        if nutrient_id not in nutrients:
            raise DataLoaderError(
                f"item_nutrients references unknown nutrient_id='{nutrient_id}'"
            )
    
    # Check requirements
    for (household_id, nutrient_id), _ in requirements.items():
        if household_id not in households:
            raise DataLoaderError(
                f"requirements references unknown household_id='{household_id}'"
            )
        if nutrient_id not in nutrients:
            raise DataLoaderError(
                f"requirements references unknown nutrient_id='{nutrient_id}'"
            )
    
    # Check bounds
    for (item_id, household_id), _ in bounds.items():
        if item_id not in items:
            raise DataLoaderError(
                f"bounds references unknown item_id='{item_id}'"
            )
        if household_id not in households:
            raise DataLoaderError(
                f"bounds references unknown household_id='{household_id}'"
            )