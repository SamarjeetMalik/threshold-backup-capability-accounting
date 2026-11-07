"""Run the v4 TLC configurations (RecoveryLifecycleV4, MultiGenerationRenewal),
including the v4.0.1 fairness-map variants.

Usage: python3 run_tlc_v4.py --java /path/to/java --jar .tools/tla2tools.jar
Same pinned TLC2 2.19 jar and flags as run_tlc.py. Each configuration has a
declared expected outcome; an unexpected pass is as much a failure as an
unexpected violation. With --record the semantic results become the new
expected/v4_tlc_results.json; otherwise they are compared with it.
"""
from pathlib import Path
import argparse, hashlib, json, re, subprocess, tempfile

PINNED_SHA256 = "936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88"
RUNS = [
    ("RecoveryLifecycleV4", "V4SafeOneEpoch", "pass"),
    ("RecoveryLifecycleV4", "V4SafeTwoEpoch", "pass"),
    ("RecoveryLifecycleV4", "V4SafeCombined", "pass"),
    ("RecoveryLifecycleV4", "V4SafeGenerations", "pass"),
    ("RecoveryLifecycleV4", "V4LiveExpiry", "pass"),
    ("RecoveryLifecycleV4", "V4LiveNoWorkerFairness", "temporal"),
    ("MultiGenerationRenewal", "MGRenew", "pass"),
    ("MultiGenerationRenewal", "MGReuse", "invariant GenPrivate"),
    ("MultiGenerationRenewal", "MGRenewKeepOld", "invariant GenPrivate"),
    # v4.0.1 fairness map for ExpiryCompletes
    ("RecoveryLifecycleV4", "V401WorkerWF", "pass"),
    ("RecoveryLifecycleV4", "V401AllWF", "temporal"),
    ("RecoveryLifecycleV4", "V401NoErase", "temporal"),
    ("RecoveryLifecycleV4", "V401NoReceipt", "temporal"),
    ("RecoveryLifecycleV4", "V401NoRestart", "temporal"),
    ("RecoveryLifecycleV4", "V401NoWorkerMin", "temporal"),
]


def outcome(text):
    if "Model checking completed. No error has been found." in text:
        return "pass"
    m = re.search(r"Invariant (\w+) is violated", text)
    if m:
        return "invariant " + m[1]
    if "Temporal properties were violated" in text:
        return "temporal"
    return "error"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--java", default="java")
    ap.add_argument("--jar", required=True)
    ap.add_argument("--record", action="store_true")
    args = ap.parse_args()
    root = Path(__file__).resolve().parent
    jar = Path(args.jar).resolve()
    if hashlib.sha256(jar.read_bytes()).hexdigest() != PINNED_SHA256:
        raise SystemExit("TLC jar checksum differs from pinned release v1.7.4")
    out = root / "reproduced/tlc_v4"
    out.mkdir(parents=True, exist_ok=True)
    runs = []
    for module, config, expected in RUNS:
        with tempfile.TemporaryDirectory(prefix="ceab-tlc-") as meta:
            r = subprocess.run([args.java, "-Xmx2g", "-XX:+UseParallelGC", "-jar", str(jar),
                                "-workers", "1", "-seed", "1", "-fp", "0", "-config", config + ".cfg",
                                "-metadir", meta, module], cwd=root, text=True, capture_output=True)
        text = r.stdout + r.stderr
        (out / (config + ".log")).write_text(text)
        got = outcome(text)
        assert got == expected, (config, got, text[-3000:])
        counts = re.search(r"(\d+) states generated, (\d+) distinct states found", text)
        actions = [a.split(" line ")[0] for a in re.findall(r"State \d+: <([^>]+)>", text)]
        run = {"module": module, "config": config, "outcome": got,
               "states_generated": int(counts[1]) if counts else None,
               "distinct_states": int(counts[2]) if counts else None,
               "counterexample_actions": actions}
        runs.append(run)
        print(config, run["distinct_states"], got, flush=True)
    report = {"scope": "finite explicit-state checking; liveness only under the declared weak fairness",
              "tlc_version": "TLC2 2.19, release v1.7.4", "jar_sha256": PINNED_SHA256, "runs": runs}
    expected_path = root / "expected/v4_tlc_results.json"
    if args.record:
        expected_path.write_text(json.dumps(report, indent=2) + "\n")
    else:
        assert json.loads(expected_path.read_text())["runs"] == runs
        print("PASS: v4 TLC outcomes, state counts and counterexample actions match expected")
    (out / "v4_tlc_results.json").write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
