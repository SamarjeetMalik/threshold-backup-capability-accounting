# Revision v4.1.6 (9 November 2026)

Second figure pass on v4.1.5, at the corresponding author's request: make every figure 10/10 and the colours "more professional" (v4.1.5 read as generated). Builds on REVISION_V4.1.5.md. Artifact v4.1.1 and all data files unchanged. Both authors approved v4.1.6 on 9 November 2026 (relayed in chat by the corresponding author).

## Changes
- Palette: deep blue #1F3A5F (honest), brick red #A93226 (adversary), grey #5E6670 (public); honest boxes white, adversary #FBEFED, public #F1F1F1; 0.6 pt outlines, 1 pt corners (were 2 pt with pastel fills); grid #E4E4E4 at 0.3 pt; axes black 75%. The styled build's text boxes use the same palette.
- Tick numbers: printed in the figure font (Helvetica 8 pt), including powers of ten on log axes (style.tex).
- Fig. 14: cancelled state moved; WorkerAbandons and WorkerReturns enter it on separate anchors; the sending-to-cancelled arrow is routed orthogonally. No arrows cross.
- Fig. 9: callouts "L = 970,299" and "L_reuse = 3,991" on leader lines into empty space; panel titles capitalised.
- Fig. 7: adds K(K-1)/2^129 for hypothetical 128-bit key instances (comparison only; exceeds 2^-128 for K >= 3); the 128-bit target is dotted. Caption states both and that the identifier term q(q-1)/2^257 has the same form.
- Fig. 15: heat-map ramp white to 38% deep blue.

## Checks
- Both builds with -halt-on-error: 52 pp, 0 overfull, 0 undefined, 0 LaTeX warnings, 0 FIGSCALE (every figure at natural size).
- Every figure inspected at 170 dpi.
- Overleaf zip compiles from an empty directory to 52 pp.
- Theorem 25 packet: pp. 22-32 (unchanged page range).

## SHA-256
- Capability_Exposure_Accounting_v4.1.6.pdf: 11926751f2859529bdc1a7647bc42de9f88ad1a5d6c0ec7dce0eb3aa2312db8e
- Capability_Exposure_Accounting_v4.1.6_submission.pdf: bd9617f96405b1b792621e492eab59be24802d1d70fc5a58ad0fadaeeb59c742
- Capability_Exposure_Accounting_Overleaf_v4.1.6.zip: e002bd1a09d563c2a01443a5dd57c44bc5ed1ac13aa0956c871cf11f5bc8da3f
- THEOREM25_REVIEW_PACKET_pp22-32.pdf: 670b025a60a514695c35e2dcc584766cb087bdf4a2be768f73b012b40d488b60
