# Reproduction container for the v4.1.1 artifact (manuscript v4.1.11).
# Base image pinned by index digest (python:3.12.14-slim-bookworm, checked on Docker Hub 9 Nov 2026).
# NOT BUILT OR TESTED by the authors at release time: no container runtime was available on the build machine.
# The reference runs used CPython 3.12.14, pyca/cryptography 50.0.2 and OpenJDK 26 on macOS; see REPRODUCIBILITY.md.
FROM python:3.12.14-slim-bookworm@sha256:392307d22300de8b5986851a12d9176dfc0fc073e65bf6523ebd7dcbeb23564e
RUN apt-get update \
 && apt-get install -y --no-install-recommends openjdk-17-jre-headless ca-certificates \
 && rm -rf /var/lib/apt/lists/*
WORKDIR /work
COPY artifact/ /work/artifact/
WORKDIR /work/artifact
RUN python -m pip install --no-cache-dir -r requirements.txt \
 && python fetch_tlc.py
# fetch_tlc.py downloads TLC 1.7.4 and refuses any jar whose SHA-256 differs from the pinned value.
CMD ["python", "reproduce_all.py", "--java", "/usr/bin/java", "--jar", ".tools/tla2tools.jar"]
