#!/usr/bin/env python3
"""One-command reproduction: regenerate data -> run evaluation -> rebuild risk-register views."""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from sfa_fairness import generate_data, pipeline  # noqa: E402

if __name__ == "__main__":
    generate_data.main()
    pipeline.main()
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_risk_register.py")], check=True)
