"""Single command for the whole artifact: Python evidence (v2-v4.0.2 checks and
all tests) and every TLC configuration, each compared with its saved
expectation. Logs go to reproduced/. Usage:

    python3 reproduce_all.py --java /path/to/java --jar .tools/tla2tools.jar

Create the environment with `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`
and run with `.venv/bin/python`. Measurements are separate: `python bench_v404.py` then
`python make_plot_data.py` regenerates every plot's data in ../manuscript/data.
Fetch the pinned jar first with `python3 fetch_tlc.py` if it is not present.
"""
from pathlib import Path
import argparse, subprocess, sys


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--java", default="java")
    ap.add_argument("--jar", default=".tools/tla2tools.jar")
    args = ap.parse_args()
    root = Path(__file__).resolve().parent
    (root / "reproduced").mkdir(exist_ok=True)
    steps = [[sys.executable, "reproduce_v4.py"]] + [
        [sys.executable, runner, "--java", args.java, "--jar", args.jar]
        for runner in ("run_tlc.py", "run_tlc_v3.py", "run_tlc_v4.py")]
    for cmd in steps:
        print("==", " ".join(cmd[1:2]), flush=True)
        r = subprocess.run(cmd, cwd=root)
        if r.returncode:
            raise SystemExit(f"FAILED: {' '.join(cmd)} (exit {r.returncode})")
    try:
        import cryptography  # noqa: F401  (pyca/cryptography, see requirements.txt)
    except ImportError:
        raise SystemExit("NOT RUN: data-layer tests need pyca/cryptography; "
                         "run with the venv from requirements.txt")
    print("== test_datalayer.py, test_datalayer_v404.py, test_datalayer_v409.py, test_worker_supervisor.py, test_worker_supervisor_v411.py", flush=True)
    r = subprocess.run([sys.executable, "-m", "unittest", "-v", "test_datalayer", "test_datalayer_v404", "test_datalayer_v409",
                        "test_worker_supervisor", "test_worker_supervisor_v411"], cwd=root,
                       text=True, capture_output=True)
    (root / "reproduced" / "datalayer_tests.log").write_text(r.stdout + r.stderr)
    print(r.stdout + r.stderr, end="")
    if r.returncode:
        raise SystemExit("FAILED: data-layer or supervisor tests")
    print("PASS: all Python evidence, all tests (including the data layer and worker supervisor) and all TLC configurations match expectations")


if __name__ == "__main__":
    main()
