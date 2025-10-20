import json
from pathlib import Path

import yaml

from fbdam.run import run_cli


def test_runner_produces_artifacts():
    run_id = "test-run"
    code = run_cli([
        "--scenario",
        "scenario-a1",
        "--run-id",
        run_id,
        "--seed",
        "5",
        "--time-limit",
        "1",
        "--mip-gap",
        "0.01",
        "--threads",
        "auto",
    ])
    assert code == 0

    run_dir = Path("runs") / "ds-a" / "alpha-0.4" / run_id
    assert run_dir.exists()
    assert (run_dir / "run_params.yaml").is_file()
    assert (run_dir / "atom.yaml").is_file()
    assert (run_dir / "metrics.json").is_file()
    assert (run_dir / "logs" / "solver.log").is_file()

    with (run_dir / "run_params.yaml").open("r", encoding="utf-8") as handle:
        run_params = yaml.safe_load(handle)
    assert run_params["scenario_id"] == "scenario-a1"
    assert run_params["overrides"]["solver"]["time_limit_s"] == 1.0
    assert run_params["overrides"]["solver"]["mip_gap"] == 0.01

    with (run_dir / "metrics.json").open("r", encoding="utf-8") as handle:
        metrics = json.load(handle)
    assert "tnu" in metrics
    assert "equity_index_hoover" in metrics

    with (run_dir / "atom.yaml").open("r", encoding="utf-8") as handle:
        atom = yaml.safe_load(handle)
    assert atom["meta"]["dataset_id"] == "ds-a"
    assert atom["meta"]["config_id"] == "alpha-0.4"
    assert atom["meta"]["scenario_id"] == "scenario-a1"
    assert atom["meta"]["model_effective_dials"]["alpha_i"] in (0.4, 0.6)

    # Clean up the generated run directory to keep the workspace tidy
    for path in sorted(run_dir.rglob("*"), reverse=True):
        if path.is_file():
            path.unlink()
        else:
            path.rmdir()
    run_dir.rmdir()

    # Ensure parent directories remain for fixtures or other tests
    for parent in [run_dir.parent, run_dir.parent.parent, run_dir.parent.parent.parent]:
        if parent.exists() and not any(parent.iterdir()):
            parent.rmdir()
