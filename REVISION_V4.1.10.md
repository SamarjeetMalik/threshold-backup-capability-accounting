# Revision v4.1.10 (9 November 2026)

Presentation revision of v4.1.9, requested by the corresponding author to tighten the caveats. Artifact v4.1.1 and all data files are unchanged. No theorem, bound, proof step or reported number changed.

## 1. Caveats: each limitation stated once
Principle: a limitation is stated where it matters and once in Section 11. Repeats elsewhere were removed. Mathematical negations ("not FPT", "not a multiple of (1, β)") are part of the results and stay.
- Abstract and contribution 5: the selective-opening remark (kept in the Theorem 25 box, Section 8.2 "What full adaptivity would require", and Section 11).
- Contribution 7: "this is testing, not a refinement proof" (kept in Section 9.3 and Table 12).
- Section 2: "natural targets for the accounting, not objects it improves upon"; "broader claims … would require external validation" (the scope of the contribution is stated in Section 11).
- After Theorem 14: the second sentence saying a violation gives no efficient seed recovery (the first stays).
- After Fig. 4: "it is not a measurement" (the caption already says so).
- After Proposition 27: two remarks restated by the "Reused banks are not safer" box.
- Before eq. (8): "the δ terms have no asserted value" (the next sentence says the budget is symbolic).
- Section 9.3: the state-count caveat is one sentence; "kernel buffers are logical state" removed (Section 11 covers physical erasure).
- Conclusion: the selective-opening clause.

"Not full adaptive security" still appears in the abstract, contribution 5, the Theorem 25 box, Section 11 and the conclusion. L is unchanged; Proposition 27 is unchanged.

Sentences of the caveat type outside proofs: 129 → 115; body text 14,190 → 13,763 words.

## 2. Section 11
The six limitation paragraphs (Cryptographic; Algebraic and observation model; Formal lifecycle; Implementation and measurements; Operational erasure and trust; Strongest remaining weakness) are replaced by:
- one paragraph, "Limitations beyond the table", covering only what Table 12 does not show: the composition loss and the audit status of Theorem 25; the system contracts (log, certificates, anchor, clocks; no malicious-dealer VSS, refresh protocol or revocation; unquantified failure terms and α); and physical erasure (inventory omissions, receipts, process isolation without zeroed memory, swap, in-memory reference, local nonce guard, one machine);
- "Nature of the contribution" (unchanged text).
Table 12's TLC row now also names the manual composition of the one-guardian and multi-guardian models and the assumed renewal algebra, which the removed "Formal lifecycle" paragraph carried.

## 3. Other presentation
- Section 10: the list of checks is now Table 11, "Executable checks" (Result / Checked against / Size and outcome), with the same numbers in the same order. Online Resource 1, Table S6 maps its rows to the artifact scripts.
- Fig. 6 (derived-key collision bound) is taller: plot height 6.8 cm instead of 5.6 cm, so it is less wide-and-short.
- Abstract 235 words (was 250; IJIS limit 250).
- Page bottoms: \flushbottom was tested and rejected; it stretched six pages past badness 10000, so \raggedbottom stays.

## Checks
- `main.tex`, `main_submission.tex`: 47 pp.; `supplement.tex`: 11 pp. All with -halt-on-error: 0 overfull, 0 underfull hboxes, 0 undefined references, 0 LaTeX warnings, 0 FIGSCALE.
- Pages with Table 11, Section 11 and Fig. 6 inspected at full size.
- Theorem 25 packet regenerated (pp. 23–34); its only text change from v4.1.9 is the two removed remarks after Proposition 27.
- Overleaf zip compiles from an empty directory.

## SHA-256
- Capability_Exposure_Accounting_v4.1.10.pdf: 4b63a1712cadfb5938d8b79091d7208c7596bfa1622c073bbff94911580b299c
- Capability_Exposure_Accounting_v4.1.10_submission.pdf: 906ad87a251783c712c6e356f7189915b294b063e35a83c3f9273af5b2354d36
- Capability_Exposure_Accounting_v4.1.10_Online_Resource_1.pdf: 7e165fb0a6e1fc14e5dce49dcafdb44c3d5d7ee044c9b0f440821d72aa0021c0
- manuscript/main.tex: 6a0116860771439abd7684da0515d35056b01b2d44678dd6ac0d2c24455ac276
- manuscript/supplement.tex: 7acb49d09b2609d49947b6f2e5c7f03dc3ea0cc6d03ffd699d26c2ae84fbe6c6
- THEOREM25_REVIEW_PACKET_pp23-34.pdf: 75fdaf33a87aaa10a8d62edac203ebac5bd9182761c3e8b3a10174ea4d09ecd6

Approved by both authors 9 Nov 2026; released as tag v4.1.10, Zenodo DOI 10.5281/zenodo.24090614.
