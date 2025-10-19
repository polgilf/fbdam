"""
domain.py — Core domain entities
--------------------------------
Immutable, typed dataclasses for the FBDAM optimization domain.
This module declares pure domain objects (no I/O, no Pyomo). It is
consumed by the model builder after the I/O layer prepares data.

Design goals:
- Immutability with @dataclass(frozen=True) → safer and easier to reason about
- Minimal validation to catch common data issues early
- No imports from pandas/pyomo; keep concerns separated
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping, Optional

# ---------------------------
# Common type aliases (IDs)
# ---------------------------
ItemId = str
NutrientId = str
HouseholdId = str


# ---------------------------
# Value objects (core domain)
# ---------------------------

@dataclass(frozen=True)
class Item:
    """
    A product that can be allocated (e.g., rice, beans).
    - stock: available quantity (>= 0)
    - cost: optional unit cost (>= 0), used in cost-related objectives/constraints
    - unit: optional string for display (e.g., 'kg', 'pack')
    """
    item_id: ItemId
    name: str
    stock: float
    cost: float = 0.0
    unit: Optional[str] = None
    metadata: Optional[Mapping[str, str]] = None

    def __post_init__(self) -> None:
        if self.stock < 0:
            raise ValueError(f"Item.stock must be >= 0 (got {self.stock}) for {self.item_id}")
        if self.cost < 0:
            raise ValueError(f"Item.cost must be >= 0 (got {self.cost}) for {self.item_id}")
        if not self.item_id:
            raise ValueError("Item.item_id cannot be empty")
        if not self.name:
            raise ValueError("Item.name cannot be empty")


@dataclass(frozen=True)
class Nutrient:
    """
    A nutrient tracked by the model (e.g., Protein, Iron).
    - unit: display/reference unit (e.g., 'g', 'mg')
    """
    nutrient_id: NutrientId
    name: str
    unit: Optional[str] = None
    metadata: Optional[Mapping[str, str]] = None

    def __post_init__(self) -> None:
        if not self.nutrient_id:
            raise ValueError("Nutrient.nutrient_id cannot be empty")
        if not self.name:
            raise ValueError("Nutrient.name cannot be empty")


@dataclass(frozen=True)
class Household:
    """
    A demand recipient (e.g., a family, household, or beneficiary unit).
    - fairshare_weight: proportional weight used in fairness constraints (>= 0)
    - group: optional bucket label (e.g., region or vulnerability group)
    """
    household_id: HouseholdId
    name: str
    fairshare_weight: float = 1.0
    group: Optional[str] = None
    metadata: Optional[Mapping[str, str]] = None

    def __post_init__(self) -> None:
        if not self.household_id:
            raise ValueError("Household.household_id cannot be empty")
        if not self.name:
            raise ValueError("Household.name cannot be empty")
        if self.fairshare_weight < 0:
            raise ValueError(
                "Household.fairshare_weight must be >= 0 "
                f"(got {self.fairshare_weight}) for {self.household_id}"
            )


@dataclass(frozen=True)
class Requirement:
    """
    Requirement R for a given (household, nutrient).
    - amount: required nutrient amount per reference period (>= 0)
    """
    household_id: HouseholdId
    nutrient_id: NutrientId
    amount: float

    def __post_init__(self) -> None:
        if self.amount < 0:
            raise ValueError(
                f"Requirement.amount must be >= 0 (got {self.amount}) for "
                f"({self.household_id}, {self.nutrient_id})"
            )



@dataclass(frozen=True)
class ItemNutrient:
    """
    Nutrient content of an item.
    - qty_per_unit: nutrient units delivered per 1 unit of item (>= 0)
      (e.g., protein grams per kg of rice)
    """
    item_id: ItemId
    nutrient_id: NutrientId
    qty_per_unit: float

    def __post_init__(self) -> None:
        if self.qty_per_unit < 0:
            raise ValueError(
                f"ItemNutrient.qty_per_unit must be >= 0 (got {self.qty_per_unit}) for "
                f"({self.item_id}, {self.nutrient_id})"
            )


@dataclass(frozen=True)
class AllocationBounds:
    """
    Per-(item, household) bounds applied to decision variable x[item, household].

    The builder should enforce:
      lower <= x[i,h] <= upper

    - lower: lower bound (>= 0)
    - upper: upper bound (>= lower); use None to indicate 'no explicit cap'
    """
    item_id: ItemId
    household_id: HouseholdId
    lower: float = 0.0
    upper: Optional[float] = None

    def __post_init__(self) -> None:
        if self.lower < 0:
            raise ValueError(
                f"AllocationBounds.lower must be >= 0 (got {self.lower}) for "
                f"({self.item_id}, {self.household_id})"
            )
        if self.upper is not None and self.upper < self.lower:
            raise ValueError(
                f"AllocationBounds.upper must be >= lower (got upper={self.upper}, lower={self.lower}) "
                f"for ({self.item_id}, {self.household_id})"
            )

# ---------------------------
# Aggregated, read-only views
# ---------------------------

@dataclass(frozen=True)
class DomainIndex:
    """
    Read-only index of domain entities and relations for model construction.
    This is a *pure data container* to hand over to the model builder.

    Expected usage:
      - io.py populates this structure after reading/validating inputs
      - model.py consumes it to create Pyomo sets/params/vars

    Notes:
      - All mappings should be total over their keys (no missing references)
      - Keep this object small and predictable (no behavior beyond getters)
    """
    items: Mapping[ItemId, Item]
    nutrients: Mapping[NutrientId, Nutrient]
    households: Mapping[HouseholdId, Household]

    # relations
    item_nutrients: Mapping[tuple[ItemId, NutrientId], ItemNutrient]
    requirements: Mapping[tuple[HouseholdId, NutrientId], Requirement]
    bounds: Mapping[tuple[ItemId, HouseholdId], AllocationBounds]

    def get_item(self, item_id: ItemId) -> Item:
        return self.items[item_id]

    def get_nutrient(self, nutrient_id: NutrientId) -> Nutrient:
        return self.nutrients[nutrient_id]

    def get_household(self, household_id: HouseholdId) -> Household:
        return self.households[household_id]

    def get_item_nutrient(self, item_id: ItemId, nutrient_id: NutrientId) -> ItemNutrient:
        return self.item_nutrients[(item_id, nutrient_id)]

    def get_requirement(self, household_id: HouseholdId, nutrient_id: NutrientId) -> Requirement:
        return self.requirements[(household_id, nutrient_id)]

    def get_bounds(self, item_id: ItemId, household_id: HouseholdId) -> AllocationBounds:
        return self.bounds[(item_id, household_id)]


# ---------------------------
# Lightweight “factory” hints
# ---------------------------
# NOTE: Actual I/O/validation belongs in io.py. If needed later,
# you can add tiny helpers here that *only* transform already-validated
# dicts into dataclasses (without touching files/paths/pandas).
#
# Example pattern (to implement in io.py):
#
# def build_domain_index(raw: dict) -> DomainIndex:
#     items = {r["item_id"]: Item(**r) for r in raw["items"]}
#     nutrients = {r["nutrient_id"]: Nutrient(**r) for r in raw["nutrients"]}
#     households = {r["household_id"]: Household(**r) for r in raw["households"]}
#     item_nutrients = {
#         (r["item_id"], r["nutrient_id"]): ItemNutrient(**r) for r in raw["item_nutrients"]
#     }
#     requirements = {
#         (r["household_id"], r["nutrient_id"]): Requirement(**r) for r in raw["requirements"]
#     }
#     bounds = {
#         (r["item_id"], r["household_id"]): AllocationBounds(**r) for r in raw.get("bounds", [])
#     }
#     return DomainIndex(
#         items=items,
#         nutrients=nutrients,
#         households=households,
#         item_nutrients=item_nutrients,
#         requirements=requirements,
#         bounds=bounds,
#     )
