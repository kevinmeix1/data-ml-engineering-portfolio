from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROJECTS = [
    "01-lakehouse-data-platform",
    "02-feature-store-inference",
    "03-mlops-lifecycle-platform",
    "04-data-observability-lineage",
    "05-rag-evaluation-pipeline",
    "06-streaming-fraud-anomaly",
    "07-elt-connector-framework",
]


def run_project_tests(project: str) -> int:
    cwd = ROOT / project
    env = os.environ.copy()
    env["PYTHONPATH"] = str(cwd / "src")
    print(f"\n== {project} ==")
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=cwd,
        env=env,
        text=True,
    )
    return result.returncode


def main() -> int:
    failures = [project for project in PROJECTS if run_project_tests(project) != 0]
    if failures:
        print("\nFailed projects:")
        for project in failures:
            print(f"- {project}")
        return 1
    print("\nAll portfolio project tests passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
