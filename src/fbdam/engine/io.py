"""
io.py — Data and configuration loader
-------------------------------------
Responsibility:
- Load and validate YAML scenario files.
- Load built-in catalogs (constraints/objectives) packaged under `fbdam.config`.
- Resolve catalog references (`ref`) with optional parameter overrides.
- Normalize file paths and perform light validation (existence checks).
- Return a structured, builder-ready configuration dict.

Design notes:
- This module performs *structural* validation and normalization only.
  Semantic/business validation (e.g., shapes, value ranges beyond simple checks)
  should live in a dedicated validation layer or Pydantic models if/when added.
- Catalog files are shipped as package data and accessed via importlib.resources.
- CSVs (datasets) are *not* read here; we only normalize and validate paths.
"""

from __future__ import annotations

from dataclasses import dataclass
from importlib import resources
from pathlib import Path
from typing import Any, Dict, List, Mapping, Optional, Tuple, Union

import yaml

from fbdam.engine.data_loader import DataLoaderError, load_domain_and_params
from fbdam.engine.domain import DomainIndex


# ----------------------------- Exceptions ------------------------------------


class IOConfigError(RuntimeError):
    """Raised when the scenario or catalogs are structurally invalid."""


# ----------------------------- Data shapes -----------------------------------


@dataclass(frozen=True)
class MaterializedConstraint:
    """A fully specified constraint block ready for the model builder."""
    id: str                # catalog id / registry key
    params: Dict[str, Any] # concrete parameters (after overrides applied)


@dataclass(frozen=True)
class MaterializedObjective:
    """A fully specified objective block ready for the model builder."""
    id: str                 # catalog id for traceability
    name: str               # implementation key in the objectives registry
    sense: str              # "maximize" | "minimize"
    params: Dict[str, Any]  # concrete parameters (after overrides applied)


@dataclass(frozen=True)
class SolverConfig:
    """Normalized solver configuration."""
    name: str                        # "appsi_highs" | "highs" | ...
    options: Dict[str, Union[str, int, float, bool]]


@dataclass(frozen=True)
class ScenarioConfig:
    """
    Builder-ready scenario configuration.
    Note: dataset paths are normalized (absolute) and verified to exist.
    """

    data_paths: Dict[str, Path]
    domain: DomainIndex
    model_params: Dict[str, Any]
    constraints: List[MaterializedConstraint]
    objectives: List[MaterializedObjective]
    solver: SolverConfig
    dataset_id: str
    config_id: str
    dataset_root: Path
    config_path: Path
    raw: Dict[str, Any]  # original (lightly normalized) content for traceability


# ------------------------------ Public API -----------------------------------


def load_scenario(scenario_path: Path) -> ScenarioConfig:
    """
    Load and normalize a scenario YAML:
    1) Parse YAML.
    2) Load packaged catalogs (constraints/objectives).
    3) Resolve catalog references with overrides.
    4) Normalize CSV paths and perform existence checks.
    5) Normalize solver configuration with defaults.
    """
    scenario_path = Path(scenario_path).expanduser().resolve()
    if not scenario_path.is_file():
        raise IOConfigError(f"Scenario file not found: {scenario_path}")

    scenario = _read_yaml_file(scenario_path)
    if not isinstance(scenario, dict):
        raise IOConfigError("Scenario YAML must be a mapping at the top-level.")

    dataset_id, dataset_root = _resolve_dataset_section(
        scenario.get("dataset"),
        scenario_path,
    )
    config_id, config_path = _resolve_config_section(
        scenario.get("config"),
        scenario_path,
    )

    config_data = _read_yaml_file(config_path)
    model_section = _compose_model_section(
        config_data.get("model", {}),
        scenario.get("model", {}),
        context=f"{config_path.name}::model",
    )

    # Load catalogs packaged with the library
    constraints_catalog = _load_packaged_yaml("fbdam.config", "catalogs/constraints_v1.1.yaml")
    objectives_catalog = _load_packaged_yaml("fbdam.config", "catalogs/objectives_v1.0.yaml")

    # Materialize constraints/objectives
    mat_constraints = _materialize_constraints(
        model_section.get("constraints", []),
        constraints_catalog,
        context=f"{config_path.name}::model.constraints",
    )
    mat_objectives = _materialize_objectives(
        model_section.get("objectives", []),
        objectives_catalog,
        context=f"{config_path.name}::model.objectives",
    )

    # Normalize data file paths based on dataset root
    data_paths = _resolve_dataset_paths(dataset_root, dataset_id)

    # Solver configuration (config defaults overridden by scenario-level block)
    solver_section = _merge_solver_sections(
        config_data.get("solver", {}),
        scenario.get("solver", {}),
    )
    solver_cfg = _normalize_solver(
        solver_section,
        context=f"{scenario_path.name}::solver",
    )

    # Domain datasets + model parameters
    try:
        bundle = load_domain_and_params(
            data_paths=data_paths,
            model_section=model_section,
        )
    except DataLoaderError as exc:
        raise IOConfigError(str(exc)) from exc

    # Return a frozen, builder-ready configuration
    normalized_raw = {
        "version": scenario.get("version"),
        "status": scenario.get("status"),
        "dataset": {"id": dataset_id, "path": str(dataset_root)},
        "config": {"id": config_id, "path": str(config_path)},
        "data": {k: str(v) for k, v in data_paths.items()},
        "model": {
            "constraints": [c.__dict__ for c in mat_constraints],
            "objectives": [o.__dict__ for o in mat_objectives],
        },
        "solver": {"name": solver_cfg.name, "options": solver_cfg.options},
        "model_params": bundle.model_params,
    }

    return ScenarioConfig(
        data_paths=data_paths,
        domain=bundle.domain,
        model_params=bundle.model_params,
        constraints=mat_constraints,
        objectives=mat_objectives,
        solver=solver_cfg,
        dataset_id=dataset_id,
        config_id=config_id,
        dataset_root=dataset_root,
        config_path=config_path,
        raw=normalized_raw,
    )


# ------------------------------ YAML loading ---------------------------------


def _read_yaml_file(path: Path) -> Dict[str, Any]:
    """Read a YAML file from the filesystem and return a dict (empty dict if file is empty)."""
    with Path(path).open("rb") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise IOConfigError(f"YAML at {path} must be a mapping at the top-level.")
    return data


def _load_packaged_yaml(package: str, relative: str) -> Dict[str, Any]:
    """
    Load a YAML resource embedded in the package (declared via package-data).
    Example: package="fbdam.config", relative="catalogs/constraints_v1.1.yaml"
    """
    try:
        res = resources.files(package).joinpath(relative)
    except Exception as exc:  # pragma: no cover
        exc_name = type(exc).__name__
        raise IOConfigError(
            f"Cannot resolve packaged resource: {package}:{relative} ({exc_name}: {exc})"
        ) from exc

    if not res.is_file():
        raise IOConfigError(f"Packaged YAML not found: {package}:{relative}")

    with res.open("rb") as fh:
        data = yaml.safe_load(fh) or {}
    if not isinstance(data, dict):
        raise IOConfigError(f"Packaged YAML {package}:{relative} must be a mapping.")
    return data


# ------------------------ Catalog materialization -----------------------------


def _materialize_constraints(
    entries: List[Dict[str, Any]],
    catalog: Dict[str, Any],
    context: str,
) -> List[MaterializedConstraint]:
    """
    Expand scenario constraint entries against the catalog:
    - Each entry may reference a catalog item via `ref`.
    - Optional `override` dict merges into the referenced params.
    """
    catalog_items = _index_catalog(catalog, root_key="constraints", id_key="id")
    materialized: List[MaterializedConstraint] = []

    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise IOConfigError(f"{context}[{i}]: each constraint must be a mapping.")
        ref = entry.get("ref")
        if not ref:
            raise IOConfigError(f"{context}[{i}]: missing 'ref' field for constraint.")

        cat = catalog_items.get(ref)
        if not cat:
            raise IOConfigError(f"{context}[{i}]: unknown constraint ref '{ref}'.")

        base_params = _require_mapping(cat, "params", default={}, context=f"{context}[{i}::{ref}]")
        override = entry.get("override", {}) or {}
        if not isinstance(override, dict):
            raise IOConfigError(f"{context}[{i}::{ref}]: 'override' must be a mapping if provided.")

        merged = _deep_merge(base_params, override)
        materialized.append(MaterializedConstraint(id=ref, params=merged))

    return materialized


def _materialize_objectives(
    entries: List[Dict[str, Any]],
    catalog: Dict[str, Any],
    context: str,
) -> List[MaterializedObjective]:
    """
    Expand scenario objective entries against the catalog:
    - Each entry may reference a catalog item via `ref`.
    - Optional `override` dict merges into the referenced params.
    """
    catalog_items = _index_catalog(catalog, root_key="objectives", id_key="id")
    materialized: List[MaterializedObjective] = []

    for i, entry in enumerate(entries):
        if not isinstance(entry, dict):
            raise IOConfigError(f"{context}[{i}]: each objective must be a mapping.")
        ref = entry.get("ref")
        if not ref:
            raise IOConfigError(f"{context}[{i}]: missing 'ref' field for objective.")

        cat = catalog_items.get(ref)
        if not cat:
            raise IOConfigError(f"{context}[{i}]: unknown objective ref '{ref}'.")

        name = _require_str(cat, "name", context=f"{context}[{i}::{ref}]")
        sense = _require_str(cat, "sense", context=f"{context}[{i}::{ref}]")
        base_params = _require_mapping(cat, "params", default={}, context=f"{context}[{i}::{ref}]")
        override = entry.get("override", {}) or {}
        if not isinstance(override, dict):
            raise IOConfigError(f"{context}[{i}::{ref}]: 'override' must be a mapping if provided.")

        merged = _deep_merge(base_params, override)
        materialized.append(MaterializedObjective(id=ref, name=name, sense=sense, params=merged))

    return materialized


def _index_catalog(catalog: Dict[str, Any], root_key: str, id_key: str) -> Dict[str, Dict[str, Any]]:
    """Index a catalog section by id."""
    section = catalog.get(root_key, [])
    if not isinstance(section, list):
        raise IOConfigError(f"Catalog '{root_key}' must be a list.")
    out: Dict[str, Dict[str, Any]] = {}
    for i, item in enumerate(section):
        if not isinstance(item, dict):
            raise IOConfigError(f"Catalog '{root_key}'[{i}] must be a mapping.")
        cid = item.get(id_key)
        if not isinstance(cid, str) or not cid:
            raise IOConfigError(f"Catalog '{root_key}'[{i}] missing non-empty '{id_key}'.")
        out[cid] = item
    return out


# -------------------------- Paths & solver config -----------------------------


def _resolve_dataset_section(node: Any, scenario_path: Path) -> Tuple[str, Path]:
    context = f"{scenario_path.name}::dataset"
    if not isinstance(node, Mapping):
        raise IOConfigError(f"{context}: 'dataset' must be a mapping with an 'id'.")

    dataset_id = _require_str(node, "id", context)
    raw_path = node.get("path")
    if raw_path is None:
        raw_path = Path("..") / "data" / dataset_id

    dataset_path = Path(raw_path).expanduser()
    if not dataset_path.is_absolute():
        dataset_path = (scenario_path.parent / dataset_path).resolve()

    if not dataset_path.is_dir():
        raise IOConfigError(f"{context}: dataset directory not found -> {dataset_path}")

    return dataset_id, dataset_path


def _resolve_config_section(node: Any, scenario_path: Path) -> Tuple[str, Path]:
    context = f"{scenario_path.name}::config"
    if not isinstance(node, Mapping):
        raise IOConfigError(f"{context}: 'config' must be a mapping with an 'id'.")

    config_id = _require_str(node, "id", context)
    raw_path = node.get("path")
    if raw_path is None:
        raw_path = Path("..") / "configs" / f"{config_id}.yaml"

    config_path = Path(raw_path).expanduser()
    if not config_path.is_absolute():
        config_path = (scenario_path.parent / config_path).resolve()

    if config_path.is_dir():
        config_path = config_path / f"{config_id}.yaml"

    if not config_path.is_file():
        raise IOConfigError(f"{context}: config file not found -> {config_path}")

    return config_id, config_path


def _compose_model_section(
    config_model: Any,
    scenario_override: Any,
    *,
    context: str,
) -> Dict[str, Any]:
    if config_model is None:
        raise IOConfigError(f"{context}: configuration is missing a 'model' section.")
    if not isinstance(config_model, Mapping):
        raise IOConfigError(f"{context}: configuration 'model' must be a mapping.")
    if scenario_override not in (None, {}) and not isinstance(scenario_override, Mapping):
        raise IOConfigError(f"{context}: scenario 'model' overrides must be a mapping if provided.")

    base = dict(config_model)
    if not scenario_override:
        return base

    override = dict(scenario_override)
    return _deep_merge(base, override)


def _resolve_dataset_paths(dataset_root: Path, dataset_id: str) -> Dict[str, Path]:
    required_specs = [
        ("items.csv", True, ("items", "items_csv")),
        ("nutrients.csv", True, ("nutrients", "nutrients_csv")),
        ("households.csv", True, ("households", "households_csv")),
        ("requirements.csv", True, ("requirements", "requirements_csv")),
        ("item_nutrients.csv", True, ("item_nutrients", "item_nutrients_csv")),
    ]
    optional_specs = [
        ("household_item_bounds.csv", False, ("bounds", "household_item_bounds", "household_item_bounds_csv")),
        ("params.yaml", False, ("params", "params_yaml")),
    ]

    resolved: Dict[str, Path] = {}
    dataset_root = dataset_root.resolve()

    for filename, required, aliases in required_specs + optional_specs:
        path = (dataset_root / filename).resolve()
        if path.is_file():
            for alias in aliases:
                resolved[alias] = path
        elif required:
            raise IOConfigError(
                f"dataset '{dataset_id}' is missing required file '{filename}' at {path.parent}"
            )

    return resolved


def _merge_solver_sections(
    base_section: Any,
    override_section: Any,
) -> Dict[str, Any]:
    base = base_section if isinstance(base_section, Mapping) else {}
    override = override_section if isinstance(override_section, Mapping) else {}

    merged: Dict[str, Any] = {}
    merged.update(base)
    merged.update({k: v for k, v in override.items() if k != "options"})

    options: Dict[str, Any] = {}
    if isinstance(base, Mapping):
        options.update(base.get("options", {}) or {})
    if isinstance(override, Mapping):
        options.update(override.get("options", {}) or {})

    merged["options"] = options
    return merged


def _normalize_solver(
    solver_section: Dict[str, Any],
    context: str,
) -> SolverConfig:
    """
    Normalize solver configuration, applying sensible defaults.
    """
    if not isinstance(solver_section, dict):
        raise IOConfigError(f"{context}: 'solver' must be a mapping.")
    name = solver_section.get("name", "appsi_highs")
    if not isinstance(name, str) or not name:
        raise IOConfigError(f"{context}.name must be a non-empty string.")

    options = solver_section.get("options", {}) or {}
    if not isinstance(options, dict):
        raise IOConfigError(f"{context}.options must be a mapping if provided.")

    # Light sanity checks for common options (lenient by design)
    _assert_option_types(options, context)

    return SolverConfig(name=name, options=options)


def _assert_option_types(options: Dict[str, Any], context: str) -> None:
    """Check that options contain only simple JSON-serializable scalars."""
    allowed = (str, int, float, bool)
    for k, v in options.items():
        if not isinstance(v, allowed) and v is not None:
            raise IOConfigError(f"{context}.options['{k}'] must be a simple scalar (str/int/float/bool).")


# ------------------------------- Utilities ------------------------------------


def _require_str(node: Dict[str, Any], key: str, context: str) -> str:
    val = node.get(key)
    if not isinstance(val, str) or not val:
        raise IOConfigError(f"{context}: missing or invalid '{key}' (expected non-empty string).")
    return val


def _require_mapping(node: Dict[str, Any], key: str, default: Optional[Dict[str, Any]], context: str) -> Dict[str, Any]:
    if key not in node:
        return default or {}
    val = node.get(key)
    if not isinstance(val, dict):
        raise IOConfigError(f"{context}: '{key}' must be a mapping.")
    return val


def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep-merge two dicts (override wins). Lists are replaced (not merged).
    This is predictable and adequate for parameter overriding patterns.
    """
    out: Dict[str, Any] = dict(base)
    for k, v in override.items():
        if k in out and isinstance(out[k], dict) and isinstance(v, dict):
            out[k] = _deep_merge(out[k], v)
        else:
            out[k] = v
    return out
