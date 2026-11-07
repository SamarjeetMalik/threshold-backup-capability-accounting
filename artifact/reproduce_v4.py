"""Reproduce all portable v4 evidence: everything reproduce_v3.py checks
(v2 and v3 evidence, unchanged), the v4 checkers against
expected/v4_results.json, and the v4 tests. TLC runs separately:
run_tlc.py (v2), run_tlc_v3.py (v3) and run_tlc_v4.py (v4).
"""
from pathlib import Path
import json, subprocess, sys

PROGRAMS = ("v4_leakage", "v4_erasure", "v4_temporal", "v4_quorum", "v4_refinement", "v401_patterns", "v402_checks", "v403_checks")


def main():
    root = Path(__file__).resolve().parent
    out = root / "reproduced"
    out.mkdir(exist_ok=True)
    r = subprocess.run([sys.executable, "reproduce_v3.py"], cwd=root, text=True, capture_output=True)
    print(r.stdout + r.stderr, end="", flush=True)
    if r.returncode:
        raise SystemExit(r.returncode)
    results = {name: json.loads(subprocess.run([sys.executable, name + ".py"], cwd=root, text=True,
                                               capture_output=True, check=True).stdout)
               for name in PROGRAMS}
    (out / "v4_results.json").write_text(json.dumps(results, indent=2) + "\n")
    if results != json.loads((root / "expected" / "v4_results.json").read_text()):
        raise SystemExit("v4 results differ from expected/v4_results.json")
    print("PASS: v4 checks exactly match expected/v4_results.json", flush=True)
    log = subprocess.run([sys.executable, "-m", "unittest", "-v", "test_v4.py"], cwd=root,
                         text=True, capture_output=True)
    (out / "v4_tests.log").write_text(log.stdout + log.stderr)
    print(log.stdout + log.stderr, end="")
    if log.returncode:
        raise SystemExit(log.returncode)
    print("PASS: v2/v3 evidence, v4 and v4.0.1 checks and v4 tests")


if __name__ == "__main__":
    main()
