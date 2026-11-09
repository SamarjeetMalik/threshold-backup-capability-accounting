# Capability Exposure Accounting for Threshold-Based Encrypted Backup Recovery

**Samarjeet Malik**, Ashoka University; **Shaurya Pratap Singh**, Indian Institute of Science.

Manuscript version **4.1.9**, 9 November 2026 (see `REVISION_V4.1.9.md`): the paper no longer recounts its own version history, and measurement, model-checking and test detail moved to a supplement, Online Resource 1 (`manuscript/supplement.tex`); results are unchanged since 4.1.1; release 4.1.9 is archived at Zenodo DOI [10.5281/zenodo.24090414](https://doi.org/10.5281/zenodo.24090414) (tag `v4.1.9`). Manuscript release 4.1.8 (official Springer Nature template in single column) is archived at Zenodo DOI [10.5281/zenodo.24089585](https://doi.org/10.5281/zenodo.24089585) (tag `v4.1.8`). The previous manuscript release, 4.1.7, is archived at Zenodo DOI [10.5281/zenodo.24088767](https://doi.org/10.5281/zenodo.24088767) (tag `v4.1.7`); 4.1.6 is archived at Zenodo DOI [10.5281/zenodo.24084300](https://doi.org/10.5281/zenodo.24084300) (tag `v4.1.6`). Artifact version **4.1.1** (Zenodo DOI [10.5281/zenodo.24060229](https://doi.org/10.5281/zenodo.24060229), published 9 November 2026; tag `v4.1.1`) reproduces every result; reproduction in `REPRODUCIBILITY.md`. Not yet submitted. Version 4.0.7 was released as tag `v4.0.7` and archived on Zenodo, DOI [10.5281/zenodo.24048192](https://doi.org/10.5281/zenodo.24048192) (v4.0.6 added licences to v4.0.5, which superseded v2.0.0; versions 3.0.0 to 4.0.4 were not released separately). Two PDFs from one source: `manuscript/main.tex` (styled) and `manuscript/main_submission.tex` (submission-safe); build `main_submission.tex` before `supplement.tex`, whose references to the paper are read from `main_submission.aux`. Environment: `ENVIRONMENT.md`. Changes: `CHANGELOG.md`. Springer Nature journal LaTeX (`sn-jnl`, single column, numerical math/physics references), with an Overleaf-ready source archive and compiled PDF provided as release assets.

This formal security-analysis paper models surviving backup-recovery capabilities using typed conjunctive derivation rules and finite-field observations. It separates reconstruction from information leakage, characterizes permitted erasure through minimal witness supports, and analyzes independently refreshed generations, copied delivery credentials and alternate recovery routes. A checked lifecycle and Python reference exercise release, expiry, queue cancellation, crashes and rollback contracts.

The claims are relative to declared operations and affine views. The paper deliberately uses a component-security argument for concrete cryptography. Its composition theorem is restricted-adaptive: exposures may be adaptive, but the bound carries a guessing factor L that is exponential in the number of renewed generations, so it is not a full adaptive-security result. It does not establish complete concrete-client confidentiality, physical erasure, production liveness or human recognition.

## Read and reproduce

- `manuscript/main.tex`: complete single-file Springer manuscript.
- `manuscript/references.bib`: bibliography; official class/style files are included.
- `artifact/README.md`: exact commands, dependencies, outputs and finite model scope.
- `REVISION_V4.1.1.md`: v4.1.0 → v4.1.1 changes, Theorem 25 audit, runs, open items, checklist.
- `REVISION_V4.1.0.md`: v4.0.9 → v4.1.0 changes, executed runs, unreproduced claims, author steps.
- `REVISION_V4.0.9.md`: v4.0.8 → v4.0.9 audit, changes, figure log, placeholders, IJIS/TOPS checklists.
- `REPRODUCIBILITY.md`: versions, commands, recorded runs, data provenance and hashes.
- `REVISION_V4.0.8.md`: v4.0.7 → v4.0.8 IJIS formatting; lists the author-supplied placeholders.
- `REVISION_V4.0.7.md`: v4.0.6 → v4.0.7 Zenodo DOI.
- `REVISION_V4.0.6.md`: v4.0.5 → v4.0.6 licensing (MIT code, CC BY 4.0 paper).
- `REVISION_V4.0.5.md`: v4.0.4 → v4.0.5 restricted-adaptive qualification pass (text only).
- `REVISION_V4.0.4.md`: v4.0.3 → v4.0.4 audit, data-layer fixes, benchmarks, figures, reviews, scores.
- `REVISION_V4.0.3.md`: v4.0.2 → v4.0.3 issue matrix, key-collision analysis, conventions, data layer, reviews, scores.
- `REVISION_V4.0.2.md`: v4.0.1 → v4.0.2 issue table, proof-status table, executed checks, reviews, scores.
- `REVISION_V4.0.1.md`: v4.0.0 → v4.0.1 diagnostic table, validation, reviews, assessment.
- `REVISION_V4.md`: v4 audit, adaptive-security pass, reviews, assessment.
- `REVISION_V3.md`: v3 audit table, novelty study, reviewer reports, quality control and scores.
- `REVIEW_RESPONSE.md`: the v2.0.0 major-revision response (historical).
- `AUTHOR_CHECKLIST.md`: author-supplied details to confirm before submission.
- `SHA256SUMS`: integrity manifest for the curated source tree.

Build the paper with pdfLaTeX/BibTeX:

```sh
cd manuscript
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

For Overleaf, upload the release's source ZIP, choose `main.tex` as the main document and pdfLaTeX as the compiler. The document uses ordinary TeX Live packages and has no absolute-path inputs, external fonts or shell-escape requirements. It has been compiled locally; no claim is made that it has been uploaded to an Overleaf account or submitted to a journal.

Run portable evidence from the repository root:

```sh
python3 artifact/reproduce_v4.py
python3 artifact/fetch_tlc.py
python3 artifact/run_tlc.py --java java --jar artifact/.tools/tla2tools.jar
python3 artifact/run_tlc_v3.py --java java --jar artifact/.tools/tla2tools.jar
python3 artifact/run_tlc_v4.py --java java --jar artifact/.tools/tla2tools.jar
```

One command, `artifact/.venv/bin/python artifact/reproduce_all.py --java java --jar artifact/.tools/tla2tools.jar` (venv from `artifact/requirements.txt`), runs everything. All 99 Python tests pass (5 baseline, 25 v2, 14 v3, 18 v4, 27 data layer, 10 worker supervisor); the v3 and v4 checkers match `expected/v3_results.json` and `expected/v4_results.json`; the 8 v2, 13 v3 and 15 v4 TLC configurations (9 from v4.0.0, 6 fairness-map runs added in v4.0.1) reproduce their recorded outcomes and counts (recorded run: `reproduction_logs_v411/reproduce_all_v4.1.1_tree.log`).

The current artifact is v4.1.1, DOI 10.5281/zenodo.24060229 (tag `v4.1.1`); its predecessor v4.0.7 is DOI 10.5281/zenodo.24048192. No journal acceptance is claimed. Public source availability does not establish novelty or production readiness. Springer class/style notices remain intact; see the licence section below.

## Licence

- **Code and artifact** (everything under `artifact/`): MIT, see `LICENSE`.
- **Paper** (`manuscript/main.tex`, `main_submission.tex`, `style.tex`, `figures/`, `data/`, `references.bib`, the compiled PDFs and the `REVISION_*.md` reports): Creative Commons Attribution 4.0 International (CC BY 4.0), see `LICENSE-CC-BY-4.0.txt`.
- **Excluded:** the Springer Nature class and bibliography style (`manuscript/sn-jnl.cls`, `manuscript/sn-mathphys-num.bst`) keep their own upstream terms (LaTeX Project Public License notices) and are redistributed unchanged.

