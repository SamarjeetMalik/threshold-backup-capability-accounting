# Revision v4.1.14 (10 November 2026)

Simplification of Fig. 3, requested by the corresponding author, and one defect fix in Online Resource 1. Text, theorems and numbering are unchanged. Artifact v4.1.1 is unchanged.

## Fig. 3 (leakage subspace)
- One chain: seed and uniform mask → view Y = AS + BR → "cancel the masks: any λ with λB = 0" → "exposed: λY = u·S with u = λA ∈ U". The separate A and B boxes are folded into the view.
- The "What the view reveals" text panel is removed: it restated Theorem 1(2) and (5), which the caption and theorem carry.
- The red example (leakage without reconstruction, Y = S_0 + S_1) is kept, in two lines.

## Online Resource 1: missing reference list (defect in v4.1.12 and v4.1.13)
- v4.1.12 moved the proofs of the erasure-complexity propositions to Section S6. Their citations of Karp 1972, Dinur and Safra 2005 and Alimonti and Kann 2000 moved with them, but the supplement had no bibliography and the paper no longer cites these works, so the released v4.1.12 and v4.1.13 supplements print "[? ]" in three places. The build log warned; the release checks counted undefined references in the paper only.
- The supplement now ends with its own reference list from `references.bib` (three entries, all already in the bibliography). Still 21 pages.

## Checks
- Fig. 3 at natural size (344.2 of 372 pt), inspected at 140 dpi in colour and grayscale; 0 FIGSCALE.
- Clean builds with -halt-on-error: `main.tex`/`main_submission.tex` 39 pp., `supplement.tex` 21 pp.; 0 overfull or underfull hboxes, 0 undefined references or citations in any of the three logs, 0 LaTeX warnings, 0 BibTeX errors.
- Theorem 24 packet regenerated (paper pp. 21–28 plus Online Resource 1 pp. 17–21; page ranges asserted). Overleaf zip compiles from an empty directory, supplement citations resolved.

## SHA-256
- Capability_Exposure_Accounting_v4.1.14.pdf: 337e8b4947a94b5df54b6457706db6d9b5ee8009139431fac94f3941814f1b2a
- Capability_Exposure_Accounting_v4.1.14_submission.pdf: 1210280ab7c06aff507d918488352a11dc9b050f8e47e09ff22481e4dc83cab6
- Capability_Exposure_Accounting_v4.1.14_Online_Resource_1.pdf: 3084a8641a5454861a8ad7afc4980af16566590704adc4ca7f1d3ef13dc6a5a7
- Capability_Exposure_Accounting_Overleaf_v4.1.14.zip: f4a9671929a8a9cf4f4e6127d0e3689aab823805445b534969a8409cb21ca109
- manuscript/main.tex: cfceb3f19507076e3a31523ad6b6357f59683bf1009a17100d961e0891557472
- manuscript/supplement.tex: 477e9cbab2b7997e2fbb204f7970ea3f97a455275785a9c89cc76166e6ff3bd4
- manuscript/figures/fig_leakage.tex: 09ec12bc44b6d5c31661b891b99471a6a081b40ffced951852ebd99cc88a820b
- THEOREM25_REVIEW_PACKET_pp21-28_and_OR1_pp17-21.pdf: 50278f835a005870eefdcb284df66df40cf315555638c4ff2d6275511ad72525

Approved by both authors 10 Nov 2026; released as tag v4.1.14, Zenodo DOI 10.5281/zenodo.24093096.
