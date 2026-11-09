# Independent re-run by a co-author

Goal: a second person reproduces every artifact result on their own machine, and the log is kept in the repository.

1. `git clone https://github.com/SamarjeetMalik/threshold-backup-capability-accounting && cd threshold-backup-capability-accounting`
2. Install Python 3.12 (3.11 also works) and Java 11 or later.
3. `bash scripts/rerun_and_log.sh "Shaurya Pratap Singh"`
4. Expected end of the log: `PASS: all Python evidence, all tests (including the data layer and worker supervisor) and all TLC configurations match expectations` and `exit status: 0`. It takes a few minutes; nothing is uploaded anywhere.
5. Send the file `reruns/rerun_*.log` and the SHA-256 the script prints. It is added to `reruns/` with a line in `REPRODUCIBILITY.md`.

The log records the operating system, Python, Java, cryptography/OpenSSL versions and the git commit, and checks `artifact/` against `SHA256SUMS` before running.

Status: not yet run (as of v4.1.11).
