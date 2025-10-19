# src/fbdam/engine/io_utils.py
from __future__ import annotations
from pathlib import Path
from datetime import datetime
from pyomo.opt import ProblemFormat

def _slug(s: str) -> str:
    """kebab-case minimalista (sin espacios/acentos) para nombres de archivo."""
    return "".join(ch.lower() if ch.isalnum() else "-" for ch in s).strip("-")

def save_model_mps(model, base_dir: Path, scenario_name: str, run_id: str | None = None) -> Path:
    """
    Guarda el modelo Pyomo en formato .mps con nombre gobernado.

    Args:
        model: instancia Pyomo.
        base_dir: carpeta raíz de outputs (p.ej., Path('outputs')).
        scenario_name: nombre legible del escenario (se normaliza a kebab-case).
        run_id: identificador corto de la corrida (opcional, p.ej., '001' o hash).

    Returns:
        Path al archivo .mps generado.
    """
    ts = datetime.now().strftime("%Y%m%d-%H%M")
    scen = _slug(scenario_name) or "scenario"
    rid = f"-{_slug(run_id)}" if run_id else ""
    out_dir = (Path(base_dir) / "models")
    out_dir.mkdir(parents=True, exist_ok=True)

    fname = f"model-{ts}-{scen}{rid}.mps"
    fpath = out_dir / fname

    # Etiquetas simbólicas y determinismo para reproducibilidad
    io_opts = {
        "symbolic_solver_labels": True,   # usa nombres de variables/cts
        "file_determinism": 2,            # orden estable (Pyomo)
    }

    # Escribe en MPS (lineal). Si alguna restricción no es lineal, considerar .lp
    model.write(str(fpath), format=ProblemFormat.mps, io_options=io_opts)
    return fpath
