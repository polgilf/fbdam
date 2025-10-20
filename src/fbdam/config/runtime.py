from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, Iterable, Mapping, Optional

import yaml

from fbdam.engine.domain import DomainIndex, Household, Item, ItemNutrient, Nutrient, Requirement

DATA_ROOT = Path("data")
CONFIG_ROOT = Path("config")


@dataclass
class MaterializedScenario:
    dataset_id: str
    config_id: str
    scenario_id: str
    domain: DomainIndex
    config: Dict[str, object]
    dataset_metadata: Dict[str, object]
    scenario_filters: Dict[str, object]


class ScenarioLoadError(RuntimeError):
    """Raised when inputs for a scenario cannot be loaded."""


def _read_yaml(path: Path) -> Dict[str, object]:
    if not path.is_file():
        raise ScenarioLoadError(f"YAML file not found: {path}")
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle) or {}
    if not isinstance(data, dict):
        raise ScenarioLoadError(f"YAML at {path} must be a mapping")
    return dict(data)


def _load_dataset(dataset_id: str) -> tuple[DomainIndex, Dict[str, object]]:
    dataset_dir = DATA_ROOT / dataset_id
    if not dataset_dir.is_dir():
        raise ScenarioLoadError(f"Dataset directory not found: {dataset_dir}")

    metadata = _read_yaml(dataset_dir / "dataset.yaml")

    items_path = dataset_dir / "items.csv"
    households_path = dataset_dir / "households.csv"
    requirements_path = dataset_dir / "requirements.csv"
    item_nutrient_path = dataset_dir / "item_nutrient.csv"

    items: Dict[str, Item] = {}
    with items_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"item_id", "name"}
        if not required.issubset(reader.fieldnames or set()):
            missing = required - set(reader.fieldnames or [])
            raise ScenarioLoadError(
                f"items.csv missing required columns: {', '.join(sorted(missing))}"
            )
        for row in reader:
            stock_val = float(row.get("stock") or 0.0)
            items[row["item_id"]] = Item(
                item_id=row["item_id"],
                name=row["name"],
                stock=stock_val,
                unit=row.get("unit") or None,
                cost=float(row.get("cost") or 0.0),
            )

    households: Dict[str, Household] = {}
    with households_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"h_id", "size"}
        if not required.issubset(reader.fieldnames or set()):
            missing = required - set(reader.fieldnames or [])
            raise ScenarioLoadError(
                f"households.csv missing required columns: {', '.join(sorted(missing))}"
            )
        for row in reader:
            hid = row["h_id"]
            size = float(row.get("size") or 1.0)
            households[hid] = Household(
                household_id=hid,
                name=row.get("name") or hid,
                fairshare_weight=size,
            )

    nutrient_ids: set[str] = set()
    requirements: Dict[tuple[str, str], Requirement] = {}
    with requirements_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"h_id", "nutrient_id", "requirement"}
        if not required.issubset(reader.fieldnames or set()):
            missing = required - set(reader.fieldnames or [])
            raise ScenarioLoadError(
                f"requirements.csv missing required columns: {', '.join(sorted(missing))}"
            )
        for row in reader:
            hid = row["h_id"]
            nid = row["nutrient_id"]
            nutrient_ids.add(nid)
            requirements[(hid, nid)] = Requirement(
                household_id=hid,
                nutrient_id=nid,
                amount=float(row.get("requirement") or 0.0),
            )

    item_nutrients: Dict[tuple[str, str], ItemNutrient] = {}
    with item_nutrient_path.open("r", encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle)
        required = {"item_id", "nutrient_id", "a_ij"}
        if not required.issubset(reader.fieldnames or set()):
            missing = required - set(reader.fieldnames or [])
            raise ScenarioLoadError(
                f"item_nutrient.csv missing required columns: {', '.join(sorted(missing))}"
            )
        for row in reader:
            item_id = row["item_id"]
            nutrient_id = row["nutrient_id"]
            nutrient_ids.add(nutrient_id)
            item_nutrients[(item_id, nutrient_id)] = ItemNutrient(
                item_id=item_id,
                nutrient_id=nutrient_id,
                qty_per_unit=float(row.get("a_ij") or 0.0),
            )

    nutrients: Dict[str, Nutrient] = {
        nid: Nutrient(nutrient_id=nid, name=nid) for nid in sorted(nutrient_ids)
    }

    domain = DomainIndex(
        items=items,
        nutrients=nutrients,
        households=households,
        item_nutrients=item_nutrients,
        requirements=requirements,
        bounds={},
    )
    return domain, metadata


def _apply_filters(domain: DomainIndex, filters: Mapping[str, object]) -> DomainIndex:
    households_filter: Optional[Iterable[str]] = None
    items_filter: Optional[Iterable[str]] = None

    if isinstance(filters, Mapping):
        households_filter = filters.get("households")
        items_filter = filters.get("items")

    def _subset(mapping: Mapping, keys: Iterable[str]) -> Dict:
        return {k: mapping[k] for k in keys if k in mapping}

    new_households = domain.households
    new_items = domain.items
    if households_filter:
        new_households = _subset(domain.households, households_filter)
    if items_filter:
        new_items = _subset(domain.items, items_filter)

    new_requirements = {
        key: value
        for key, value in domain.requirements.items()
        if key[0] in new_households and key[1] in domain.nutrients
    }
    new_item_nutrients = {
        key: value
        for key, value in domain.item_nutrients.items()
        if key[0] in new_items and key[1] in domain.nutrients
    }

    return DomainIndex(
        items=new_items,
        nutrients=domain.nutrients,
        households=new_households,
        item_nutrients=new_item_nutrients,
        requirements=new_requirements,
        bounds={k: v for k, v in domain.bounds.items() if k[0] in new_items and k[1] in new_households},
    )


def load_materialized_scenario(scenario_id: str) -> MaterializedScenario:
    scenario_path = CONFIG_ROOT / "scenario" / f"{scenario_id}.yaml"
    scenario = _read_yaml(scenario_path)

    dataset_id = scenario.get("dataset_id")
    config_id = scenario.get("config_id")
    if not dataset_id or not config_id:
        raise ScenarioLoadError(f"Scenario '{scenario_id}' must declare dataset_id and config_id")

    config_path = CONFIG_ROOT / "params" / f"{config_id}.yaml"
    config = _read_yaml(config_path)

    domain, dataset_meta = _load_dataset(dataset_id)
    filters = scenario.get("filters") or {}
    if filters:
        domain = _apply_filters(domain, filters)

    return MaterializedScenario(
        dataset_id=str(dataset_id),
        config_id=str(config_id),
        scenario_id=str(scenario.get("scenario_id") or scenario_id),
        domain=domain,
        config=config,
        dataset_metadata=dataset_meta,
        scenario_filters=dict(filters),
    )


__all__ = ["MaterializedScenario", "ScenarioLoadError", "load_materialized_scenario"]
