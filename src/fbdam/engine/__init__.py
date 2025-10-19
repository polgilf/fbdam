"""
fbdam.engine — Core execution engine
------------------------------------
Contains the core building blocks used to load configuration/data,
assemble the Pyomo model, solve it, and emit reports.

Public API (developer-facing):
    - load_scenario: read/validate config + datasets (if implemented)
    - DomainIndex:  typed, immutable domain container
    - build_model:  construct Pyomo model from DomainIndex + spec
    - solve_model:  run the solver (appsi_highs / highs)
    - write_report: generate structured artifacts (manifest, metrics, tables)

Internal modules (not re-exported here):
    - constraints, objectives: plugin registries
"""

# Developer-facing API
try:
    from fbdam.engine.io import load_scenario  # optional; may not exist in early skeletons
except Exception:  # pragma: no cover
    load_scenario = None

from fbdam.engine.domain import DomainIndex
from fbdam.engine.model import build_model
from fbdam.engine.solver import solve_model
from fbdam.engine.reporting import write_report

__all__ = [
    "load_scenario",
    "DomainIndex",
    "build_model",
    "solve_model",
    "write_report",
]
