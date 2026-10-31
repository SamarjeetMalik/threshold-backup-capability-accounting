"""Reproduce the paper's saved finite results with Python's standard library."""
from pathlib import Path
import json
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parent
    for program, expected, output in (
        ("model_checks.py", "model_results.json", "baseline_reproduced.json"),
        ("extended_model.py", "extended_results.json", "extended_reproduced.json"),
    ):
        result = subprocess.run(
            [sys.executable, program], cwd=root, text=True,
            capture_output=True, check=True,
        )
        if json.loads(result.stdout) != json.loads((root / expected).read_text()):
            raise RuntimeError(f"Result mismatch: {program}")
        (root / output).write_text(result.stdout)
        print(f"PASS: {program} matches {expected}")
    result = subprocess.run(
        [sys.executable, "-m", "unittest", "-v", "test_extended_model.py"],
        cwd=root, text=True, capture_output=True,
    )
    (root / "test_reproduced.txt").write_text(result.stdout + result.stderr)
    print(result.stdout + result.stderr, end="")
    if result.returncode:
        raise SystemExit(result.returncode)


if __name__ == "__main__":
    main()
