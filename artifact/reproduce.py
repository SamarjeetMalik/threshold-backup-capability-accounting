"""Verify all portable Python evidence against saved expected outputs."""
from pathlib import Path
import json
import subprocess
import sys


def main():
    root = Path(__file__).resolve().parent
    out = root / "reproduced"
    out.mkdir(exist_ok=True)
    for program, name in [("check_algebra.py", "algebra_results.json"),
                          ("explore_temporal.py", "temporal_results.json"),
                          ("check_parameters.py", "parameter_results.json")]:
        result = subprocess.run([sys.executable, program], cwd=root,
                                text=True, capture_output=True, check=True)
        expected = json.loads((root / "expected" / name).read_text())
        actual = json.loads(result.stdout)
        if actual != expected:
            raise RuntimeError(f"Result mismatch: {program}")
        (out / name).write_text(result.stdout)
        print(f"PASS: {program} exactly matches expected/{name}", flush=True)
    old = subprocess.run([sys.executable, "reproduce.py"], cwd=root/"baseline",
                         text=True, capture_output=True)
    (out / "baseline.log").write_text(old.stdout + old.stderr)
    print(old.stdout + old.stderr, end="", flush=True)
    if old.returncode:
        raise SystemExit(old.returncode)
    new = subprocess.run([sys.executable, "-m", "unittest", "-v", "test_revision.py"],
                         cwd=root, text=True, capture_output=True)
    (out / "revision_tests.log").write_text(new.stdout + new.stderr)
    print(new.stdout + new.stderr, end="")
    if new.returncode:
        raise SystemExit(new.returncode)
    print("PASS: all Python checks, 5 baseline tests and 25 revision tests")


if __name__ == "__main__":
    main()
