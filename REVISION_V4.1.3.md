# v4.1.3: final manuscript consistency revision (9 November 2026)

This revision changes the manuscript only. The artifact that reproduces every result stays at v4.1.1: GitHub tag `v4.1.1`, Zenodo DOI 10.5281/zenodo.24060229. No theorem, bound, reported number, test or artifact file changed, and no new test run is claimed. The 99-test and TLC evidence is the v4.1.1 run in `reproduction_logs_v411/`.

## Checks made before editing
- **Zenodo.** DOI 10.5281/zenodo.24060229 resolves (HTTP 302). The API reports record 24060229 as Version 4.1.1, published 2026-11-09, with 5 files. The artifact zip's MD5 (`688235160ab9ef19731d4810e034152c`) equals the local `Capability_Exposure_Accounting_Artifact_v4.1.1.zip`. Calling it "archived" is therefore accurate.
- **The 5,388 count.** `artifact/v4_temporal.py::check_random_histories` adds one to `independent_targets` for each epoch seed `e` of each history without a reused block. Each history's epoch seeds are distinct seeds, so "target seeds" is the correct term. The evidence list now says that each is checked once.
- **Benchmark numbers.** Table 15 matches `evidence_v411/mac_m5_supervisor/bench_supervisor.csv` row for row. The memory figure for 256 MiB (heap 512.03, RSS 807.9 with range 807.8–808.2) matches `evidence_v411/mac_m5_memory/bench_memory.csv`. The labels still use `tracemalloc` = Python heap and `ru_maxrss` = peak RSS, and Table 15 still reports worker RSS only.
- **Qualifiers.** Source scan: "not full adaptive security" appears in the abstract, Table 17, the limitations (Section 11) and the conclusion. XP/not-FPT appears in the contribution list, Section 5 and Table 17, and now in the abstract. Appendix A says "manual induction, not a TLAPS proof". There is no bare `\mathcal K` (only `\mathcal K_{\mathrm{root}}`), no `$D$` and no `D(X)`. The limitations already say that Theorem 25 "has been audited by the authors, not by an independent cryptographer". That sentence is kept.

## Changes
1. **Data and code availability.** Rewritten as one paragraph. It names the v4.1.1 artifact (contents, tag, DOI and licences), then this manuscript's version, then v4.0.7 as the predecessor. The separate Preprint statement (v4.0.7, CC BY 4.0) is kept.
2. **Fig. C1.** Defined just before `\begin{appendices}`, so it floats to the top of the next page, ahead of the References. Its number is kept as C1 (local `\thefigure`/`\theHfigure`). Inspection: Fig. C1 is at the top of p. 47 in both PDFs. The References heading and [1] follow Appendix C (p. 47 in the submission PDF, p. 48 in the styled PDF), and no float appears inside the bibliography.
3. **Conclusion.** "The core mathematics is elementary; the contribution is accounting and verification, not new cryptography." is replaced by a statement of the integrated contribution that keeps "not a new cryptographic primitive".
4. **Introduction.** Contribution 1 no longer calls itself "elementary linear algebra used as a single decision object". It now says that one characterization is the decision object for reconstruction, privacy, leakage and erasure, and that the linear algebra is standard.
5. **Abstract.** "solvable in $n^{O(2^G)}$ time" became "XP but not FPT in the number $G$ of generations with reused credentials ($n^{O(2^G)}$ time)". "the capsule encryption" became "capsule encryption". Length: 249 words by `pdftotext` (limit 250).
6. **LLM statement.** Scope unchanged. "Prepare figures" became "write the TikZ and pgfplots source that draws the figures from the artifact's data files". The statement now says that no figure is an AI-generated image, and that the authors verified every proof, measurement and interpretation. No model version or dates are given, because the sessions before 9 Nov 2026 are not recorded here.

## Builds
`latexmk -C`, then `latexmk -pdf -halt-on-error` for `main.tex` and `main_submission.tex`. Both have 51 pages, 0 overfull boxes, 0 undefined references and 0 duplicate destinations, and no `^- ` lines in the source. The Overleaf zip also compiles from an empty directory (51 pp).

| File | SHA-256 |
|---|---|
| `output/pdf/Capability_Exposure_Accounting_v4.1.3.pdf` | `429843b4f7dfb698d7bd005056f8237cebf2978b18282b88ff97df7b31a5e415` |
| `output/pdf/Capability_Exposure_Accounting_v4.1.3_submission.pdf` | `c0eadb802b0584eaba210ae72800b1bc0019d26e3718fb2d0a5aa9d5d66a0420` |
| `output/Capability_Exposure_Accounting_Overleaf_v4.1.3.zip` | `b6132fa3214c88b327b632d2552062bdab0864d4febc6ef14f734f41b809d808` |
| v4.1.2 PDF (superseded, not released) | `9269f89c8d0b7a618ac0b23b49e41847198b590f3c2bcfe1e8ab492e4447ee91` |

## Not done, and why
- **Independent review of Theorem 25.** This needs a human cryptographer. `THEOREM25_REVIEW_REQUEST.md` and `THEOREM25_REVIEW_PACKET_pp21-31.pdf` are ready to send.
- **Co-author approval of the exact v4.1.3 file.** Shaurya Pratap Singh's agreement (relayed 9 Nov) covered the v4.1.1 declarations. v4.1.3 changed the wording of the LLM statement and the conclusion.
- **Public repository.** The corrected root README has not been pushed. The published v4.1.1 release is left unchanged, and no new artifact version was made.
- **IJIS placement of the AI declaration.** Not checked against the live portal.
