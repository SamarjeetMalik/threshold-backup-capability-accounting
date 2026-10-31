"""Execute pinned TLC configs and preserve raw logs and shortest bad traces.

Usage: python3 run_tlc.py --java /path/to/java --jar /path/to/tla2tools.jar
TLC must be version 1.7.4 (TLC2 2.19); Java 17 is the recorded runtime.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re
import subprocess
import tempfile

PINNED_SHA256 = "936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--java",default="java")
    ap.add_argument("--jar",required=True)
    ap.add_argument("--output-dir")
    args = ap.parse_args()
    root = Path(__file__).resolve().parent
    jar = Path(args.jar).resolve()
    if hashlib.sha256(jar.read_bytes()).hexdigest() != PINNED_SHA256:
        raise SystemExit("TLC jar checksum differs from pinned release v1.7.4")
    output_dir = Path(args.output_dir).resolve() if args.output_dir else root/"reproduced/tlc"
    output_dir.mkdir(parents=True, exist_ok=True)
    runs = []
    configs = [("SafeOneEpoch",None),("SafeTwoEpoch",None),("SafeCombined",None),("SafeGenerations",None),
               ("UnsafeQueue","NoPostExpiryRelease"),("UnsafeReceipt","ReceiptAfterCleanup"),
               ("UnsafeRollback","FloorMonotone"),("UnsafeBinding","ExactRequestBinding")]
    for config, violation in configs:
        with tempfile.TemporaryDirectory(prefix="ceab-tlc-") as meta:
            command = [args.java,"-Xmx2g","-XX:+UseParallelGC","-jar",str(Path(args.jar).resolve()),
                       "-workers","1","-seed","1","-fp","0","-config",config+".cfg",
                       "-metadir",meta,"RecoveryLifecycle"]
            result = subprocess.run(command,cwd=root,text=True,capture_output=True)
        output = result.stdout+result.stderr
        (output_dir/(config+".log")).write_text(output)
        if violation is None:
            assert result.returncode == 0 and "Model checking completed. No error has been found." in output,output[-5000:]
        else:
            assert f"Invariant {violation} is violated" in output,output[-5000:]
            assert result.returncode != 0
        counts = re.search(r"(\d+) states generated, (\d+) distinct states found",output)
        actions = re.findall(r"State \d+: <([^>]+)>",output)
        run = {"config":config,"exit_code":result.returncode,
               "expected_violation":violation,"states_generated":int(counts[1]) if counts else None,
               "distinct_states":int(counts[2]) if counts else None,
               "counterexample_actions":actions,
               "raw_log":config+".log"}
        runs.append(run)
        print(config,run["distinct_states"],violation or "all invariants hold",flush=True)
    version = subprocess.run([args.java,"-version"],capture_output=True,text=True)
    report={"scope":"finite explicit-state safety checking; no liveness or cryptographic proof",
            "tlc_version":"TLC2 2.19, release v1.7.4",
            "jar_sha256":hashlib.sha256(Path(args.jar).read_bytes()).hexdigest(),
            "java_version":version.stdout+version.stderr,"runs":runs}
    expected = json.loads((root/"expected/tlc_results.json").read_text())
    def semantic(run):
        return (run["config"], run["exit_code"], run["expected_violation"],
                run["states_generated"], run["distinct_states"],
                [action.split(" line ")[0] for action in run["counterexample_actions"]])
    assert [semantic(r) for r in runs] == [semantic(r) for r in expected["runs"]]
    (output_dir/"tlc_results.json").write_text(json.dumps(report,indent=2)+"\n")
    print("PASS: TLC state counts, invariants and counterexample action sequences match expected results")


if __name__ == "__main__":main()
