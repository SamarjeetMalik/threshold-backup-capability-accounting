# Revision v4.1.11 (9 November 2026)

Work on the score items listed after v4.1.10, done at the corresponding author's request. Artifact v4.1.1 is unchanged. No theorem, bound, proof step or previously reported number changed; the only new numbers are the second-machine measurements.

## Done
**Presentation**
- Table 1 "Results at a glance" (one row per main result, with its section).
- Running example: the introduction's history is named as such and used in Sections 6.3 and 8.2.
- Notation table limited to symbols used across sections.
- Sections 8.4 (independent-slot component) and 8.5 (symbolic failure budget) moved to Online Resource 1, Section S5 (Lemma S1, eq. (S1), Table S8); Section 8.3 states both in one paragraph.
- Section 6.2: two paragraphs that both explained the efficient-adversary gap merged (−138 words).
- Section 8's remaining remark paragraphs each carry a definition, a number or a theorem-specific point; they were kept.

**Figures**
- Fig. 1: outcome arrows leave U through one bus and enter each outcome box horizontally.
- Fig. 4: panel (d) folded into (c), so the outcome sits under the counts; caption updated.
- Fig. 9: (a) path and (b) request panels with orthogonal routing and no diagonal or crossing arrows. A side-by-side layout does not fit the 13 cm text width (the request chain alone needs about 11 cm).
- All three at natural size (0 FIGSCALE), 8 pt.

**Formatting**
- DOIs added to seven references after checking title, authors, venue and pages on Crossref. The Perlman (NDSS 2007) hit on Crossref is a 2005 workshop version and was not used.

**Reproducibility**
- x86 benchmark (Slurm job 8081) completed: 2-socket AMD EPYC 9554, CPython 3.11.16, same library versions; scripts byte-identical to `artifact/`. Evidence in `evidence_x86_epyc9554/` (lab paths and host name redacted); reported in Section 8.3 and Online Resource 1, Table S3. The limitations now say the data-layer measurements come from two machines and the supervisor costs from one.
- `Dockerfile` and `CONTAINER.md`: pinned container (base image by digest, cryptography 50.0.2, checksum-verified TLC). Built and run in GitHub Actions (x86-64 Linux): all 99 tests and every TLC configuration pass with `docker run --init` (run 42676588599). Without an init process the supervisor-crash test fails: its exited worker is reparented to PID 1, never reaped, and counted as alive; the diagnostic in the workflow records state Z without `--init` and reaped with it. The first run (42676060145, without `--init`) failed that one test. Logs in `container_runs/`.
- `scripts/rerun_and_log.sh` and `COAUTHOR_RERUN.md`: one-command re-run that logs OS, Python, Java, library versions and the commit, and checks `artifact/` against `SHA256SUMS`; self-tested end to end on the authors' Mac (99 tests, all TLC, exit 0).

**ORCID**
- Both authors' ORCID iDs (0009-0003-9924-7432, 0009-0009-0778-6038), checked against the ORCID registry, in the title block of the paper and supplement (linked iD badge), CITATION.cff, .zenodo.json and the Zenodo record.

## Not done here (needs people or new research)
- Independent review of Theorem 25 and a second reader for Theorems 14–15: need an outside cryptographer.
- Shaurya's re-run on his own machine (the kit is ready: `bash scripts/rerun_and_log.sh "Shaurya Pratap Singh"`).
- New mathematical results (general delivery maps, a fully adaptive variant, a lower bound on L): research, not presentation.

## Checks
- `main_submission.tex` 46 pp., `main.tex` 47 pp., `supplement.tex` 13 pp.; all with -halt-on-error: 0 overfull, 0 underfull hboxes, 0 undefined references, 0 LaTeX warnings, 0 FIGSCALE. Abstract 235 words.
- Every "Online Resource 1, Fig./Table/Section S#" pointer checked against `supplement.aux`.
- Redrawn figures inspected at 140 dpi; all pages inspected as contact sheets.
- Theorem 25 packet regenerated (pp. 23–34).
- Overleaf zip compiles from an empty directory.

## SHA-256
- Capability_Exposure_Accounting_v4.1.11.pdf: 2a882ea97958b3f91eca6f67d562c82e1ec0432c5bac6bf50a60ecd0ccb41dc4
- Capability_Exposure_Accounting_v4.1.11_submission.pdf: dda7b95fec0bf577a83985c3734f6a5f31a6b40fb5f2317257733e9876465877
- Capability_Exposure_Accounting_v4.1.11_Online_Resource_1.pdf: ef64f6b7745e1e5e4d125e4a708f11b11186876e652448d69b36d78ad1b1644f
- manuscript/main.tex: cdf5cbe499d283d182950a350671d98cf84522da9cce8c32325b1815d8955d8d
- manuscript/supplement.tex: 9274733a06f70ad1ff8abf2a211c6fb91cb517c033610ece7638f6648745fba0
- manuscript/references.bib: 7db747bedc6b30460cc0a741b6e9928123516493ec76d31f400644d03e83b57c
- THEOREM25_REVIEW_PACKET_pp23-34.pdf: 5da4b620be3d9e48248f26318d4ad15275cf85ba99a756f01465a4cb18249342
- Dockerfile: 052a405118143b709a46f8f8a43dd5373b11b023bc7f0e0db3ca58b8e39a77d6

Approved by both authors 9 Nov 2026; ORCID iDs, the container result and the re-run kit were added on the corresponding author's instruction at release. Released as tag v4.1.11, Zenodo DOI 10.5281/zenodo.24091137.
