# Revision v4.1.4 (9 November 2026)

Manuscript-only revision of v4.1.3 for IJIS format compliance. Artifact remains v4.1.1 (DOI 10.5281/zenodo.24060229). Both authors approved v4.1.3 and then v4.1.4 on 9 November 2026 (relayed in chat by the corresponding author).

## Why
IJIS submission guidelines (read 9 Nov 2026, link.springer.com/journal/10207/submission-guidelines):
- "Use of an LLM should be properly documented in the Methods section (and if a Methods section is not available, in a suitable alternative part)."
- Appendix figures continue the main text's numbering; "A1, A2, A3" style is not used.

## Changes (diff against manuscript/main_v4.1.3.tex)
1. Fig. C1 is now Fig. 15 (local \thefigure override removed). It stays in Appendix C's position, at the top of p. 47, before the References.
2. Section 10 (Experimental validation), first paragraph: one added sentence pointing to "Use of large language models" in the Statements and Declarations. The statement itself is unchanged.
3. Data and code availability: "version 4.1.3" -> "version 4.1.4".

No theorem, number, citation, figure content or artifact file changed.

## Checks
- Clean builds with -halt-on-error: both 51 pp, 0 overfull boxes, 0 undefined references, 0 LaTeX warnings.
- Pages 21-31 (Theorem 25 packet) differ from v4.1.3 only in "Fig. 15" for "Fig. C1".
- Abstract 249 words (IJIS: 150-250); 6 keywords (IJIS: 4-6); sn-jnl twocolumn.
- Overleaf zip compiles from an empty directory to 51 pp.

## SHA-256
- Capability_Exposure_Accounting_v4.1.4.pdf: 9dce69d79b183217d598b3d40cd519686a0cd3ebba01af664c676303ba36fa08
- Capability_Exposure_Accounting_v4.1.4_submission.pdf: 9faa1e3240a485998ee09c016312ee343601bb52e511ca8f53bbb9c345e7f891
- Capability_Exposure_Accounting_Overleaf_v4.1.4.zip: 263f154a4acabc531da3d5cb6f533507c0f1eeef6b32020ffd6994069bc978be
- THEOREM25_REVIEW_PACKET_pp21-31.pdf: d4c87cee4dd2232c84a6e866a98f8fcc27063dd5272bec98a4bfaeebdf13c9e8
