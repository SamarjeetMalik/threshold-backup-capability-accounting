# Re-run of the archived v4.1.1 artifact against manuscript v4.1.19 (10 November 2026)

The authors re-ran this check on their own Mac. It is not an independent reproduction.

## Setup
- Source: `git archive v4.1.1`, extracted into an empty directory (the archived release, not this working tree).
- Machine: Apple M5, macOS 26.5.1. CPython 3.12.14 in a fresh venv from `artifact/requirements.txt` (cryptography 50.0.2). OpenJDK 26.0.2.1. TLC 1.7.4 jar with SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`, which matches `REPRODUCIBILITY.md`.
- The SHA-256 hashes of the extracted evidence JSONs, `lifecycle_kernel.py`, `make_plot_data.py` and `reproduce_all.py` match `REPRODUCIBILITY.md`.

## Results
1. `reproduce_all.py --java ... --jar ...` exited with 0 after 1 min 40 s (`reproduce_all.log`).
   - 99 tests pass (5 + 25 + 14 + 18 + 37).
   - Every Python check exactly matches `expected/*.json`.
   - Every TLC configuration matches its recorded outcome, state count and counterexample actions.
2. Every TLC state count in Table S4 of Online Resource 1 equals the count in this log.
3. `make_plot_data.py` regenerated all 13 files that the manuscript's figures read (`plot_data_regenerated/`). All 13 are byte-identical to `manuscript/data/`.
4. The hand-typed tables were checked cell by cell against the regenerated data:
   - Table S2 (M5 timings and memory);
   - Table S5 (supervision);
   - the HMAC median of 0.96 µs (IQR 0.92–1.00);
   - Table S3 (EPYC), regenerated from `evidence_x86_epyc9554/` by the same script (`plot_data_regenerated_epyc/`).
   - the Holders column of Table S11, against `minholders_u*.dat`.
   All agree to the printed rounding.
5. Every TLC state count in Table S4 was compared with the log (item 2).

## Not covered
- Benchmark timings are measurements, so they were not re-measured.
- Figs. 1–6 and 8 and Figs. S1–S2 are diagrams or derived illustrations, so there is nothing to regenerate. Fig. 1 is derived from Theorem 15.
- Fig. 7 and Figs. S3–S7 plot the files compared in item 3.
- The other columns of Table S11 (t, Approvers, Log) were not recomputed.
