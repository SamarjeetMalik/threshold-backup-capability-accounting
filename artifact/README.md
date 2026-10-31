# Reproduction artifact, v2.0.0

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
