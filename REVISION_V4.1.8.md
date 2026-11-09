# Revision v4.1.8 (9 November 2026)

Layout revision of v4.1.7, made at the corresponding author's request after noticing the large bottom margin. Artifact v4.1.1 and all data files unchanged.

## 1. Template check
- `manuscript/sn-jnl.cls` and `manuscript/sn-mathphys-num.bst` are byte-identical (SHA-256) to the current official Springer Nature LaTeX template download (`sn-article-template`, 9 Nov 2026). Nothing in the source changes the page geometry.
- The bottom margin is the template's own: its sample PDF (`sn-article.pdf`) and this manuscript both have a 131 mm text width and about 66 mm of space below the last line on A4.
- v4.1.0 to v4.1.7 passed the `twocolumn` option, which splits the template's single-column text area into two 84 mm columns. The sample uses `\documentclass[pdflatex,sn-mathphys-num]{sn-jnl}` (one column). v4.1.8 uses exactly that.

## 2. Changes
- Class options `[pdflatex,sn-mathphys-num]` (single column).
- Display equations that had been broken for narrow columns are set on one or two lines: Corollary 2, eq. (2), eq. (5), Lemma 24 (statement displayed; the mixture identity in its proof on one line), Theorem 25 eq. (7), Corollary 26, eq. (8). No symbol, term or inequality changed.
- Fig. 15: panels enlarged to fill the text width (349.8 of 372 pt); still non-floating in Appendix C after its heading and paragraph, before the References; still 8 pt, unscaled, numbered 15; caption unchanged. Previous source: `manuscript/figures_v4.1.7/plot_minholders.tex`.
- Tables 1 and 5: narrow first columns set ragged-right (removes stretched inter-word spaces).
- Data statement: "This manuscript is version 4.1.8."
- Theorem 25 review packet regenerated for the new page numbers: `THEOREM25_REVIEW_PACKET_pp24-34.pdf` (Section 8.1 to the start of 8.3; replaces `..._pp22-32.pdf`, which is kept in the v4.1.7 release). `THEOREM25_REVIEW_REQUEST.md` updated to match.
- Previous text: `manuscript/main_v4.1.7.tex`.

## 3. Checks
- Both builds with -halt-on-error: styled 56 pp., submission 55 pp.; 0 overfull boxes, 0 undefined references, 0 LaTeX warnings, 0 FIGSCALE (every figure at natural size, widest 369.2 of 372 pt).
- One mild underfull line (badness 1371) in Appendix A. The class emits one "Underfull \vbox while \output is active" per page; Springer's own sample does the same (12 on its 12 pages).
- All 55 submission pages inspected as contact sheets; Theorem 25 and Corollary 26 pages inspected at full size. Appendix order on pp. 50-51: Appendix A, Appendix B, Appendix C heading and paragraph, Fig. 15, References.
- Overleaf zip compiles from an empty directory to 56 / 55 pp.
- No theorem, number, caption text, data file or artifact file changed. L stays; full adaptive security is not claimed; Proposition 27 is unchanged.

## SHA-256
- Capability_Exposure_Accounting_v4.1.8.pdf: 99ec23a970ae07e8bc66c5a26c547576b3a43221d8e941426b7b3d099e9ec82c
- Capability_Exposure_Accounting_v4.1.8_submission.pdf: 8b2ce86b3068ba231e38f9a3c8a6c382a81d5ac6d051f00ca8c70f3430aae393
- Capability_Exposure_Accounting_Overleaf_v4.1.8.zip: a36525086d5096209cf15cfc6f2c127593e8ca7278d13539ae3bd14a98b77d07
- manuscript/main.tex: 3fb98994b21e5143382c93bf892c8928dcba6be3e9bdafeb306fdd741bdc9938
- THEOREM25_REVIEW_PACKET_pp24-34.pdf: da59d16445c478c0c1d5ce9bd1f97c7e90dd440569bab921430de2cbe764f5b3

Approved by both authors 9 Nov 2026; released as tag v4.1.8, Zenodo DOI 10.5281/zenodo.24089585.
