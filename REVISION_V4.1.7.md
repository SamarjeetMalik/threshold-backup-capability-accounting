# Revision v4.1.7 (9 November 2026)

Response to an outside review of the v4.1.6 submission PDF. Artifact v4.1.1 and all data files unchanged.

## 1. Fig. 15 position (fixed)
In v4.1.6, Fig. 15 (a full-width float) landed on p. 48 ahead of the Appendix B heading, while its own Appendix C heading and paragraph were on p. 49. A full-width figure can only sit at the top of a page in a two-column layout, so it cannot follow its own heading. v4.1.7 redraws it as a single-column figure with three compact panels (u = 0, 1, 2) and sets it non-floating (minipage with \captionof, package capt-of) directly after the Appendix C paragraph. Order now: end of Appendix A; Appendix B; Appendix C heading and paragraph; Fig. 15; References, all on pp. 48-49 with no blank column. Numbering continues the main text (Fig. 15, not C1). Lettering 8 pt, unscaled (176.7 of 178.9 pt). Caption text unchanged.

## 2. Public documentation (fixed where wrong)
- Root README: already 99 tests on main since commit f6ac66e and in the v4.1.6 release; the 82-test text survives only in the frozen v4.1.1 tag and its Zenodo zip, which are immutable. Header now names manuscript 4.1.7 and the v4.1.6 release.
- AUTHOR_CHECKLIST.md: opening rewritten; co-author confirmations recorded as complete (v4.1.1 declarations; approvals of v4.1.3, v4.1.4 and v4.1.6); public records listed.
- REPRODUCIBILITY.md: now names manuscript v4.1.7 and the v4.1.1 artifact as the source of every result (it still listed the v4.1.1 manuscript and the v4.1.3 PDFs).
- Release notes: GitHub release v4.1.6 exists (marked Latest) and states that the artifact is unchanged.

## 3. Theorem 25 review (still open)
THEOREM25_REVIEW_REQUEST.md already asks about every point raised: G1->G2, G2->G2' seed decoupling, adaptive exposure and decryption-query simulation (Definition 21, Lemma 23), multi-key collision and AE losses (Lemma 24, G4->G5), and propagation into Corollary 26. L stays, full adaptive security is not claimed, Proposition 27 is not broadened. The packet (pp. 22-32) has the same text as in v4.1.6.

## Checks
- Both builds with -halt-on-error: 52 pp, 0 overfull, 0 undefined, 0 LaTeX warnings, 0 FIGSCALE.
- Pages 47-49 inspected; Fig. 15 zoomed at 200 dpi.
- Overleaf zip compiles from an empty directory to 52 pp.

## SHA-256
- Capability_Exposure_Accounting_v4.1.7.pdf: a21772b64c8fc78bce10416a56dbbf28c3f75e645978340279a3a86df01febf6
- Capability_Exposure_Accounting_v4.1.7_submission.pdf: 70eb4ff9d2eadc06087e145c8ee423401b43e9e67527ea0d10847437c184b11c
- Capability_Exposure_Accounting_Overleaf_v4.1.7.zip: 5a15639307006635b32f3208f5246448863ddb62b54a1faa1619749027b55328
- THEOREM25_REVIEW_PACKET_pp22-32.pdf: ec63e94f07225362f36ca8e72575079d325288eba4c26b96ef4f9604a60c6e74
