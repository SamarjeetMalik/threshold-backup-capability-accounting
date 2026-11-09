# Second-machine measurements: AMD EPYC 9554 (x86-64)

Measurements of the reference data layer on a second machine, added with manuscript v4.1.11 (Online Resource 1, Section S1). They live outside `artifact/` so that the v4.1.1 artifact stays byte-identical.

- **Scripts.** `bench_v404.py`, `bench_memory_v410.py` and `datalayer.py` were run unchanged; their SHA-256 equals the files in `artifact/` (checked 9 Nov 2026).
- **Machine.** 2-socket AMD EPYC 9554 (64 cores per socket; flags `aes`, `vaes`, `pclmulqdq`, `vpclmulqdq`, `avx2`, `avx512f`, see `cpuflags.txt`, `lscpu.txt`), Linux 6.8.0, glibc 2.39. Run as Slurm job 8081 on 9 Nov 2026 with 4 CPU threads and 16 GB (`run.sbatch`); the node was shared with other jobs.
- **Software.** CPython 3.11.16 (the Apple M5 run used 3.12.14), pyca/cryptography 50.0.2 with OpenSSL 4.0.3 (`env.txt`).
- **Method.** As on the Apple M5: seeded inputs, five warm-ups, 40 repetitions per microbenchmark, 12 trials per object operation, seven fresh-process trials per object size for memory. Raw samples: `out_bench/bench_v404.json`, `out_mem/bench_memory_v410.json`; summaries in the CSV files; console output in `slurm-8081.out`.
- **Redactions.** The working directory, interpreter path and host name are replaced by `<workdir>`, `<python3.11>` and `<server>`. Nothing else was edited.
- **Not measured here.** The process-supervisor cost (`bench_supervisor_v411.py`) was not run on this machine.
