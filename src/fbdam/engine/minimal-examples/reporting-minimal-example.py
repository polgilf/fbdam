from pathlib import Path
from fbdam.engine.model import build_model
from fbdam.engine.solver import solve_model
from fbdam.engine.reporting import write_report

m = build_model(cfg)  # cfg contiene "domain" (DomainIndex) y "model" (spec)
res = solve_model(m, solver_name="appsi_highs", options={"time_limit": 5})

run_dir = Path("outputs/runs/2025-10-19_demo")
manifest = write_report(
    model=m,
    solver_results=res,
    domain=cfg["domain"],
    cfg_snapshot=cfg,                 # o el escenario expandido
    run_dir=run_dir,
    include_constraints_activity=False
)
print("Artifacts written to:", run_dir)
