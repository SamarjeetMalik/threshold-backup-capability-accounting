# Capability Exposure Accounting for Threshold-Based Encrypted Backup Recovery

**Samarjeet Malik**, Ashoka University; **Shaurya Pratap Singh**, Indian Institute of Science.

Version **2.0.0**, 1 November 2026. Springer Nature journal LaTeX (`sn-jnl`, numerical math/physics references), with an Overleaf-ready source archive and compiled PDF provided as release assets.

This formal security-analysis paper models surviving backup-recovery capabilities using typed conjunctive derivation rules and finite-field observations. It separates reconstruction from information leakage, characterizes permitted erasure through minimal witness supports, and analyzes independently refreshed generations, copied delivery credentials and alternate recovery routes. A checked lifecycle and Python reference exercise release, expiry, queue cancellation, crashes and rollback contracts.

The claims are relative to declared operations and affine views. The paper deliberately uses a component-security argument for concrete cryptography. It does not establish complete concrete-client confidentiality, physical erasure, production liveness or human recognition.

## Read and reproduce

- `manuscript/main.tex`: complete single-file Springer manuscript.
- `manuscript/references.bib`: bibliography; official class/style files are included.
- `artifact/README.md`: exact commands, dependencies, outputs and finite model scope.
- `REVIEW_RESPONSE.md`: requirement-by-requirement major-revision response.
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
python3 artifact/reproduce.py
python3 artifact/fetch_tlc.py
python3 artifact/run_tlc.py --java java --jar artifact/.tools/tla2tools.jar
```

All 30 regression tests pass. Four safe TLC runs contain 316,332 reachable states in total; four unsafe mutations yield the intended shortest-action counterexamples. Detailed counts and scope are recorded in the paper and artifact README.

No DOI or journal acceptance is claimed. Public source availability does not establish novelty or production readiness. Springer class/style notices remain intact; no additional license for the authors' material has been declared.
