# Container

`Dockerfile` packages the v4.1.1 artifact with pinned versions:

- base image `python:3.12.14-slim-bookworm`, pinned by index digest `sha256:392307d22300de8b5986851a12d9176dfc0fc073e65bf6523ebd7dcbeb23564e`;
- `cryptography==50.0.2` from `artifact/requirements.txt`;
- TLC 1.7.4, fetched by `artifact/fetch_tlc.py`, which checks the jar's pinned SHA-256;
- Debian's `openjdk-17-jre-headless` (the reference runs used OpenJDK 26; TLC 1.7.4 needs Java 11 or later).

```sh
docker build -t cea-artifact .
docker run --rm --init cea-artifact      # 99 tests and every TLC configuration
```

**Use `--init`.** One test kills the supervising process with SIGKILL and checks that its decryption worker exits, by testing `os.kill(pid, 0)`. Without an init process the orphaned worker is reparented to the container's PID 1, the Python process running the checks, which never reaps it. The worker has exited but stays a zombie, and the check still counts it as alive. With `--init`, Docker's init reaps it. On a normal host the system's init reaps it, so the test passes without a container.

## Recorded runs (GitHub Actions, `.github/workflows/container.yml`)
- **Run 42676588599, 9 Nov 2026, x86-64 Linux, Docker 28.0.4: PASS.** All 99 tests and every TLC configuration match their expected outputs (`container_runs/gha_42676588599/reproduce.log`). The diagnostic step records the orphaned worker's `/proc` state 3 s after the supervisor is killed: `Z` (zombie) without `--init`, reaped with `--init` (`diagnostic.log`).
- **Run 42676060145, 9 Nov 2026: 98 of 99 tests passed** (without `--init`); the supervisor-crash test failed for the reason above (`container_runs/gha_42676060145/reproduce.log`). Every TLC configuration and every other check passed.

The workflow runs on every `v*` tag and can be started by hand. Benchmarks are not run in the container, because timings there are not comparable with the recorded ones.
