# Reproduction artifact, v4.0.5

v4.0.5 changes manuscript text only (restricted-adaptive qualification); the artifact code, tests and evidence are those of v4.0.4.

v4.0.4 adds record validation and locking to `datalayer.py`, `test_datalayer_v404.py` (11 tests), `bench_v404.py` (repeated, seeded measurements with raw samples) and `make_plot_data.py` (data for every manuscript plot). Evidence: `evidence_v404/`.

# v4.0.3 additions

v4.0.3 adds the reference data layer (`datalayer.py`, `test_datalayer.py`, `bench_datalayer.py`, `requirements.txt`) and `v403_checks.py` (exact reused-bank pattern count). Kernel and TLA+ unchanged. Raw measurements: `evidence_v403/bench_datalayer.json` (machine-dependent, not compared).

# v4.0.2 additions

v4.0.2 adds `v402_checks.py` (data-layer counting model; reused-bank pattern closed form), two tests and `reproduce_all.py` (single command). No TLA+ or kernel changes; all TLC expectations are those of v4.0.1.

# v4.0.1 additions

v4.0.1 adds `v401_patterns.py` (guessing space versus reachable late-exposure patterns), five liveness spec variants in `RecoveryLifecycleV4.tla` with six `V401*.cfg` configurations (fairness map), one test, and `evidence_v401/`. The v4.0.0 module is kept in `baseline_v4/`. The nine v4.0.0 TLC runs reproduce identically.

| v4.0.1 configuration | Distinct states | Expected outcome |
|---|---:|---|
| V401WorkerWF | 27,904 | ExpiryCompletes holds (weak fairness suffices for WorkerReturns) |
| V401AllWF / NoErase / NoReceipt / NoRestart | 27,904 each | temporal property violated |
| V401NoWorkerMin (one request) | 1,084 | temporal property violated |

# Reproduction artifact, v4.0.0

## What changed in v4

- `v4_leakage.py`: marginal/conditional leakage and chain rule; non-uniform mask counterexample; subspace masks; acceptance-measurability counterexample.
- `v4_erasure.py`: selection at threshold gates; weighted thresholds (subset-sum gadget, DP); few-generation type algorithm vs brute force.
- `v4_temporal.py`: 3,000 random histories, Theorem 15 predicate vs exact rank; correlated-block disagreements counted.
- `v4_quorum.py`: domain-correlated corruption vs enumeration; guessing-loss arithmetic.
- `v4_refinement.py`: Python transcription of `RecoveryLifecycleV4.tla` (state counts equal TLC's) and kernel conformance on seeded schedules, run against the v4 kernel and the preserved v3 kernel (`baseline_v3/`).
- `RecoveryLifecycleV4.tla` (+ `V4*.cfg`): `WorkerAbandons`, `ExpiryCompletes` under strong fairness, and the counterexample without worker fairness.
- `MultiGenerationRenewal.tla` (+ `MGRenew*.cfg`, `MGReuse.cfg`): mobile adversary with per-period copy budget.
- `lifecycle_kernel.py`: rejects certificates for inactive requests and replacement certificates; ignores completion/abandon messages whose token is not outstanding; commits earlier epochs first.
- `test_v4.py` (14 tests), `reproduce_v4.py`, `run_tlc_v4.py`, `expected/v4_*.json`, `evidence_v4/`.

```sh
python3 reproduce_v4.py
python3 run_tlc_v4.py --java java --jar .tools/tla2tools.jar
```

| v4 configuration | Distinct states | Expected outcome |
|---|---:|---|
| V4SafeOneEpoch / TwoEpoch / Combined / Generations | 27,904 / 5,584 / 140,404 / 161,032 | all invariants hold |
| V4LiveExpiry | 27,904 | ExpiryCompletes holds under strong fairness |
| V4LiveNoWorkerFairness | 27,904 | temporal property violated (hung worker) |
| MGRenew / MGReuse / MGRenewKeepOld | 775 / 84 / 116 | pass / GenPrivate violated / GenPrivate violated |

The remainder of this README is the v3.0.0 text.

# v3.0.0 reproduction notes

## What changed in v3

- `v3_leakage.py`: leakage-subspace theorem (dimension, exact mutual information, decoders, arbitrary domains); partial-opening patterns showing the v2 pair count is wrong; block lemma.
- `v3_erasure.py`: read-once erasure versus brute force; shared-root failure; reused-bank erasure equals vertex cover.
- `v3_temporal.py`: 13-cell healing classification by exact rank; exhaustive holder-committee placements; deadline comparison.
- `RecoveryLifecycleV3.tla` (+ `V3*.cfg`): adds the `aborting` worker state and `ReceiptAfterWorkers`; `V3UnsafeInflight` reproduces the v2 receipt-ordering defect.
- `MultiGuardianErasure.tla` (+ `MG*.cfg`): n holders, Byzantine receipts, copies, outages; safety and weak-fairness liveness.
- `lifecycle_kernel.py`: in-flight worker tracking, `abandon_decrypt`, `Rejected` for unknown nonces. The v2 kernel and tests are kept unchanged in `baseline_v2/`.
- `test_v3.py` (14 tests), `reproduce_v3.py`, `run_tlc_v3.py`, `expected/v3_*.json`, `evidence_v3/` (raw logs of the recorded run).

```sh
python3 reproduce_v3.py
python3 run_tlc_v3.py --java java --jar .tools/tla2tools.jar
```

| v3 configuration | Distinct states | Expected outcome |
|---|---:|---|
| V3SafeOneEpoch / TwoEpoch / Combined / Generations | 27,888 / 5,584 / 140,356 / 160,984 | all invariants hold |
| V3V2GuardsOnly | 149,844 | v2 invariants hold (the defect is invisible to them) |
| V3UnsafeInflight | 520 | ReceiptAfterWorkers violated |
| MGSafe / MGSafeTwoFaults / MGSafeOutage | 4,325 / 21,987 / 146,706 | safety and BarrierProgress under weak fairness |
| MGUnsafeQuorum / MGUnsafeReceipt | 3,086 / 4,103 | ErasureSafe violated |
| MGNoProgress | 1,120 | temporal property violated (Byzantine withholding) |
| MGUnrecoverable | initial state | RecoverableBeforeBarrier violated |

Seeded families (leakage, blocks, read-once, vertex cover) are fixed pseudo-random draws, each decided exactly. Partial-opening patterns, healing cells and committee placements are exhaustive. The rest of this README is the v2.0.0 text, still accurate for the files it describes.

# v2.0.0 reproduction notes

This artifact accompanies **Capability Exposure Accounting for Threshold-Based Encrypted Backup Recovery**, by Samarjeet Malik (Ashoka University) and Shaurya Pratap Singh (Indian Institute of Science).

It contains finite-field checks, temporal exposure exploration, a TLA+ lifecycle specification, and a standard-library Python lifecycle reference. It is research evidence, not a cryptographic backup product. The concrete-client confidentiality composition, actual consensus/transport implementations, physical erasure and human recognition remain outside the proved claims.

## Requirements

- Python 3.12 (recorded: CPython 3.12.14). No pip dependencies.
- Java 17 for TLC (recorded: Temurin 17.0.21+9). A different Java 17 patch release may change the runtime metadata, not expected state counts.
- Official TLA+ release v1.7.4, TLC2 2.19 (8 August 2024, rev 5a47802).
- Optional manuscript build: TeX Live with pdfLaTeX, BibTeX and latexmk. Recorded: TeX Live 2026, pdfTeX 1.40.29 and latexmk 4.87. The portable Springer sources are in `../manuscript/`.

## Run the portable checks

From this directory:

```sh
python3 reproduce.py
```

The command checks complete JSON equality for three new programs and both preserved baseline outputs, then executes the five original and 25 new tests. It writes generated outputs to `reproduced/`; the unchanged baseline runner also writes its generated files under `baseline/`. Expected evidence is under `expected/` and the originally recorded logs are under `evidence/`.

Expected results:

| Check | Expected result |
|---|---|
| Baseline deletion enumeration | 14,714 adversary cases, 2,150 configurations |
| Baseline toy sharing | 15,625 assignments |
| Baseline static authorization | 320 cases, seven field mutations and expiry rejection |
| Baseline symbolic retention | 39 cases |
| Baseline transition exploration | 288 quotient states and 732 transitions across three runs |
| Baseline two-generation ranks | 121 patterns |
| New direct distribution/fiber comparison | 7,407 matrices over F3 |
| Independent-generation exposure pairs | 256 over F7 |
| Cut checks | 28 deletion/copy cases; relation-only privacy fixture |
| Temporal scenarios | Eight runs, 120 states and 174 transitions |
| Parameter feasibility | 28,335 configurations, 1,914 jointly feasible |
| Regression tests | Five baseline plus 25 revision tests pass |

The temporal JSON preserves unit-action BFS shortest privacy and reconstruction witnesses separately. The two privacy-preserving scenarios and six violating scenarios are individually bounded; their totals do not describe one global state graph. Bank visits disclose data capabilities, not automatically signing authority. `capability.py` implements a declared Horn/linear language, not arbitrary cryptanalysis.

## Run all TLC checks

Fetch the official jar, validating it before writing:

```sh
python3 fetch_tlc.py
python3 run_tlc.py --java java --jar .tools/tla2tools.jar
```

The jar URL is `https://github.com/tlaplus/tlaplus/releases/download/v1.7.4/tla2tools.jar`. Its SHA-256 is:

```text
936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88
```

The runner validates this checksum again before execution. It uses `-Xmx2g -XX:+UseParallelGC`, breadth-first exploration, one worker, seed 1 and fingerprint polynomial index 0. Allow Java to open local sockets: TLC uses a local RMI listener. All eight configurations are checked; the four unsafe runs are expected to exit nonzero with the named invariant violation. A failure of the runner is not an expected unsafe-model exit.

| Configuration | Distinct states | Expected outcome |
|---|---:|---|
| SafeOneEpoch | 26,448 | All invariants hold |
| SafeTwoEpoch | 5,444 | All invariants hold |
| SafeCombined | 132,232 | All invariants hold |
| SafeGenerations | 152,208 | All invariants hold |
| UnsafeQueue | 766 | NoPostExpiryRelease violated |
| UnsafeReceipt | 16 | ReceiptAfterCleanup violated |
| UnsafeRollback | 581 | FloorMonotone violated |
| UnsafeBinding | 529 | ExactRequestBinding violated |

Safe runs sum to 316,332 states across four separate graphs. Unsafe counts are states explored before the first breadth-first violation. Logs include complete counterexample states, action labels, fingerprint collision estimates and runtime metadata. The runner compares semantic counts and counterexample action sequences with `expected/tlc_results.json`; timestamps, paths, timings, Java metadata and source-line formatting are not treated as scientific results.

Deadlock/liveness checking is disabled. The model assumes verified certificate/log outputs and a nonrollback anchor, and conservatively charges an entire share at first irreversible byte transfer. It checks one honest guardian's local obligations under concurrent requests, not a complete distributed network or concrete signature scheme. The manual induction in the paper is not a TLAPS-certified proof.

## Reference kernel scope

`lifecycle_kernel.py` implements the critical ordering with a lock, split decryption completion, generation-tagged tombstones, buffer cancellation, durable-state snapshots and a trusted antirollback anchor. Certificates/checkpoints are trusted-verifier objects. No HPKE, real signatures, TLS or consensus is implemented. Tests include a real scheduled thread paused during decryption, but no refinement proof from all Python executions to TLA+ is claimed. Python buffer overwrite is only logical state cleanup.

## Files and integrity

- `capability.py`, `check_algebra.py`, `explore_temporal.py`, `check_parameters.py`: algebra and temporal accounting.
- `RecoveryLifecycle.tla` and eight `.cfg` files: final lifecycle model.
- `lifecycle_kernel.py`, `test_revision.py`: executable critical path and 25 tests.
- `baseline/`: unchanged original checkers, expected JSON and five tests.
- `expected/`: saved semantic outputs; `evidence/`: original run logs.
- Root `SHA256SUMS`: every curated release file except the checksum file itself and Git metadata. Verify before running, since generated outputs can change after reproduction.

The official Springer class and bibliography style retain their upstream notices. No new license grant for the authors' material is asserted here. Source availability does not itself establish deployment suitability.
