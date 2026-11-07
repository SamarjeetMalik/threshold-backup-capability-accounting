"""Reproduce all portable v3 evidence: the unchanged v2 checks, the new v3
mathematical checks against expected/v3_results.json, and the v3 tests.
TLC runs separately: run_tlc.py (v2 configs) and run_tlc_v3.py (v3 configs).
"""
from pathlib import Path
import json, subprocess, sys


def run(cmd, cwd):
    r = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    print(r.stdout + r.stderr, end="", flush=True)
    if r.returncode:
        raise SystemExit(r.returncode)
    return r.stdout


def main():
    root = Path(__file__).resolve().parent
    out = root / "reproduced"
    out.mkdir(exist_ok=True)
    run([sys.executable, "reproduce.py"], root)  # v2 evidence, unchanged expectations
    results = {}
    for name in ("v3_leakage", "v3_erasure", "v3_temporal"):
        results[name] = json.loads(subprocess.run([sys.executable, name + ".py"], cwd=root, text=True,
                                                  capture_output=True, check=True).stdout)
    (out / "v3_results.json").write_text(json.dumps(results, indent=2) + "\n")
    expected = json.loads((root / "expected" / "v3_results.json").read_text())
    if results != expected:
        raise SystemExit("v3 results differ from expected/v3_results.json")
    print("PASS: v3 mathematical checks exactly match expected/v3_results.json", flush=True)
    log = subprocess.run([sys.executable, "-m", "unittest", "-v", "test_v3.py"], cwd=root,
                         text=True, capture_output=True)
    (out / "v3_tests.log").write_text(log.stdout + log.stderr)
    print(log.stdout + log.stderr, end="")
    if log.returncode:
        raise SystemExit(log.returncode)
    print("PASS: v2 evidence, v3 checks and 14 v3 tests")


if __name__ == "__main__":
    main()
