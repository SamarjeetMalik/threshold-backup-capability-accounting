# v4.0.7 → v4.0.8: formatting for the International Journal of Information Security

Capability Exposure Accounting for Threshold-Based Encrypted Backup Recovery
Samarjeet Malik (Ashoka University), Shaurya Pratap Singh (Indian Institute of Science)
8 November 2026. Source of the requirements: `output/SUBMISSION_NOTES_v4.0.7.md`.

## What changed
| IJIS requirement | v4.0.7 | v4.0.8 |
|---|---|---|
| Abstract 150–250 words | ≈396 | 234 words in the source, 240 as `pdftotext` counts them (math splits into tokens). Keeps "a *restricted-adaptive* composition theorem … it does not provide full adaptive security", the factor L (L = 1 forward-ordered, exponential in renewed generations) and the receiver selective-opening remark |
| 4–6 keywords | 9 | 6: Capability exposure, encrypted backup, threshold recovery, cryptographic erasure, restricted-adaptive security, TLA+ |
| `twocolumn` | one column | `twocolumn` option; layout reworked (below) |
| "Statements and Declarations" | `\bmhead{Declarations}` | a `\section*{Statements and Declarations}` with competing interests, funding, author contributions, ethics, data and code availability, preprint, and LLM use |
| Corresponding author with e-mail | none | `\author*` Samarjeet Malik, `\email{samarjeet.malik\_tf@ashoka.edu.in}`; the PDF text extracts as samarjeet.malik_tf@ashoka.edu.in |

Text removed from the abstract stays in the body: the L = 16 example, the 3,991 vs 970,299 reused-bank count, the advantage conventions and key coincidence, the data-layer and measurement sentences, and the 2,000-schedule count.

## Layout
sn-jnl's `twocolumn` geometry gives a 178.9 pt (63 mm) column and a 372 pt (131 mm) full width. That is narrower than IJIS's typeset 84 mm / 174 mm, so anything that fits here also fits the journal's page. The class geometry was not altered.
- Spanning floats: Tables 1 (comparison), 3 (healing), 8 (TLC) and 9 (refinement), plus Figs. 2 (leakage), 3 (witness), 4 (reuse timeline) and 11 (truncation). Figure placement was decided from natural widths measured in the log: the four diagrams are 320–373 pt wide, against a 179 pt column. Figs. 1, 8, 10, 14 and 15 were already `figure*`.
- Column widths retuned in Tables 2, 5, 6 and 8. Table 4 is now set in footnotesize.
- Plot widths: Figs. 7, 12 and 13 used `0.62\linewidth`, which at column width made the 16/64/256/1024 tick labels overlap. They now use 0.9–0.98 of the column.
- Equations: 11 displays are now split across lines with `gathered`, `split`, `multline` or `align*`. Their mathematical content is unchanged. The displays are (1), Corollary 4, (2), (3), (4), (5), the Lemma 24 mixture, (7) in Theorem 25, Corollary 26, Proposition 27 and (8).
- Bibliography URLs: sn-jnl's `\burl` (breakurl) did not break long URLs, which overflowed the column by up to 123 pt. `\burl` now passes through xurl's `\url`, with the bst's `\texttildelow` turned back into a literal `~`.
- One citation range is wrapped in `\mbox` so that it cannot break at its en dash.
- Every page of both PDFs was inspected as rendered images. Nothing overlaps and nothing is clipped. The page count fell from 45 to 42.

## Placeholders the authors must fill (bold, `\authorinput` macro in `manuscript/main.tex`)
1. Competing interests
2. Funding
3. Author contributions
4. Use of large language models (an IJIS requirement unless the use was copy-editing only)

Nothing was invented for these. The ethics, data/code availability and preprint statements are factual and taken from earlier records. Data and code availability cites DOI 10.5281/zenodo.24048192 as version 4.0.7, with MIT for the code and CC BY 4.0 for the paper. The preprint statement names the v4.0.7 Zenodo record under CC BY 4.0, as Springer's preprint policy asks.

## Not changed
No theorem, proof, number, test, data file or artifact file changed. `diff -r` against v4.0.7 shows changes only in `manuscript/main.tex` and three `manuscript/figures/plot_*.tex` width settings, plus documentation and metadata. **`artifact/reproduce_all.py` was not re-run**, because nothing under `artifact/` changed. The v4.0.5 run in `artifact/evidence_v405/` still applies. `artifact/README.md` still says v4.0.7, which is correct for the artifact. The v4.0.7 text is kept as `manuscript/main_v4.0.7.tex`. v4.0.7, its bundles and its DOI are untouched.

## Builds
`latexmk -pdf -halt-on-error` from clean, for both `main.tex` and `main_submission.tex`: exit 0, 0 overfull boxes, 0 undefined references, 42 pages each. A grep for `^- ` in the `.tex` sources finds nothing.

## Still to do (author steps)
- Fill the four placeholders.
- Decide on the APC (US$3,690). Any waiver must be requested at submission.
- Optionally add ORCID iDs.
- Not done here, and left to the authors: any push, GitHub release, Zenodo version or submission. A Zenodo upload of 4.0.8 would mint a new version DOI. `CITATION.cff` and `RELEASE_METADATA.json` still give the v4.0.7 DOI and say so.
