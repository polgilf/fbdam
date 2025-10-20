from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

SCENARIOS = [
    "scenario-a1",
    "scenario-a2",
    "scenario-b1",
    "scenario-b2",
]

PROFILES = {
    "T": {"time_limit": "30", "mip_gap": "0.0", "seed": "1"},
    "G": {"time_limit": "0", "mip_gap": "0.01", "seed": "2"},
}


def main() -> None:
    for scenario in SCENARIOS:
        for label, profile in PROFILES.items():
            run_id = f"{scenario}-{label.lower()}"
            cmd = [
                sys.executable,
                "-m",
                "fbdam.run",
                "--scenario",
                scenario,
                "--run-id",
                run_id,
                "--seed",
                profile["seed"],
                "--time-limit",
                profile["time_limit"],
                "--mip-gap",
                profile["mip_gap"],
                "--threads",
                "auto",
            ]
            print("Running:", " ".join(cmd))
            env = os.environ.copy()
            pythonpath = env.get("PYTHONPATH", "")
            src_path = str(Path(__file__).resolve().parents[1] / "src")
            env["PYTHONPATH"] = src_path if not pythonpath else f"{src_path}:{pythonpath}"
            subprocess.run(cmd, check=True, env=env)


if __name__ == "__main__":
    main()
