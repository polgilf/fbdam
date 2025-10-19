# tests/test_mps_export.py
from pathlib import Path
from src.fbdam.engine.model import build_minimal_model  # o tu builder real
from src.fbdam.engine.io_utils import save_model_mps

def test_mps_is_written(tmp_path: Path):
    model = build_minimal_model()
    out = save_model_mps(model, tmp_path, scenario_name="baseline", run_id="001")
    assert out.exists()
    assert out.name.startswith("model-") and out.suffix == ".mps"
