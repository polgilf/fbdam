from pathlib import Path


def build_run_dir(dataset_id: str, config_id: str, run_id: str) -> Path:
    """Construct the canonical run directory for a dataset/config/run triple."""
    run_path = Path("runs") / dataset_id / config_id / run_id
    run_path.mkdir(parents=True, exist_ok=True)
    (run_path / "logs").mkdir(exist_ok=True)
    (run_path / "figures").mkdir(exist_ok=True)
    return run_path


__all__ = ["build_run_dir"]
