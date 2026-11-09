# Container

`Dockerfile` packages the v4.1.1 artifact with pinned versions:

- base image `python:3.12.14-slim-bookworm`, pinned by index digest `sha256:392307d22300de8b5986851a12d9176dfc0fc073e65bf6523ebd7dcbeb23564e`;
- `cryptography==50.0.2` from `artifact/requirements.txt`;
- TLC 1.7.4, fetched by `artifact/fetch_tlc.py`, which checks the jar's pinned SHA-256;
- Debian's `openjdk-17-jre-headless` (the reference runs used OpenJDK 26; TLC 1.7.4 needs Java 11 or later).

```sh
docker build -t cea-artifact .
docker run --rm cea-artifact          # 99 tests and every TLC configuration
```

**Status: not yet built or tested.** No container runtime was available on the authors' build machine when v4.1.11 was released. The reproduction recorded in `REPRODUCIBILITY.md` was done without a container. Reports of a successful or failed build are welcome. Benchmarks are not run by default, because timings inside a container are not comparable with the recorded ones.
