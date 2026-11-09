# Revision v4.1.13 (10 November 2026)

Simplification of Figs. 2 and 6, requested by the corresponding author. Text, theorems, numbering and the supplement are unchanged, apart from one sentence after Fig. 2 that points to Fig. 4 for erasure. Artifact v4.1.1 is unchanged.

## Fig. 2 (capability exposure)
- Removed the fourth outcome box ("erasure succeeds iff every minimal witness is hit"). It belongs to Section 5 and Fig. 4, and its dashed grey arrow mixed two ideas.
- Source labels shortened so the six boxes are near-uniform; outcomes fed through one bus; the colour legend dropped (the introduction states it once). No box touches another.

## Fig. 6 (game sequence of Theorem 24)
- One chain. Each hop's step and loss sit under its own arrow: guess pattern Γ (×L, red, multiplicative); zero capsules (ε_mu); decouple seed (0); PRF (ε_prf); identifiers (q(q−1)/2^257); AEAD (ε_ae^iid).
- The separate hop table, its "Games" column (which repeated the arrows), the query line and the boxed forward-ordered note are removed. The theorem statement gives the query counts, and the caption says L = 1 under forward-ordered exposure.
- The bound is written once below the chain.

## Checks
- Both figures at natural size (366.6 and 365.9 of 372 pt), inspected at 130 dpi; 0 FIGSCALE.
- `main.tex`/`main_submission.tex` 39 pp., `supplement.tex` 21 pp.; -halt-on-error, 0 overfull, 0 underfull hboxes, 0 undefined references, 0 LaTeX warnings. Abstract 235 words. Numbering unchanged (Theorem 24).
- Theorem 24 packet regenerated (paper pp. 21–28 plus Online Resource 1 pp. 17–21; page ranges asserted). Overleaf zip compiles from an empty directory.

## SHA-256
- Capability_Exposure_Accounting_v4.1.13.pdf: b0653e89dc675426328180b77ec031c183ce46a5401762cfaf27c0181619a321
- Capability_Exposure_Accounting_v4.1.13_submission.pdf: 13245346b45c0a1a819213adbd8916acf2e909317af9b564692c606dd8e80734
- Capability_Exposure_Accounting_v4.1.13_Online_Resource_1.pdf: 6e9043d7cf971502374a92a398699aa12d64a2f177b1aff82e84009aa0c51880
- Capability_Exposure_Accounting_Overleaf_v4.1.13.zip: 5588e190119191c60a4927a2fe4d0b62d7de5a9713f58b661e4aff2a0426731f
- manuscript/main.tex: f3b0e92711f303b8697e0b8fb4025adec5f2de374aa93fca60759cd17d997b81
- manuscript/figures/fig_architecture.tex: b407ef0339dfb3e1b4888376b41b604ee56664df522a7251b40b948cd63df7cc
- manuscript/figures/fig_hybrids.tex: 15bf73b3cd8d112ef3d194d317416d484a584bd92d76e5c76363d0572f44fa1a
- THEOREM25_REVIEW_PACKET_pp21-28_and_OR1_pp17-21.pdf: aafca7ce79ae7a678d73ada552e810da89001ffade6576e146c95967bafd9fbe

Approved by both authors 10 Nov 2026; released as tag v4.1.13, Zenodo DOI 10.5281/zenodo.24092482.
