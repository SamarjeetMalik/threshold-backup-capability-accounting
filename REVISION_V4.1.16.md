# Revision v4.1.16 (10 November 2026)

Precision pass on v4.1.15, answering a second outside review (pasted in chat, 10 Nov 2026). Each point was checked against the source first. No theorem statement, proof or number changed; numbering unchanged (Theorem 24). Artifact v4.1.1 is unchanged. v4.1.15 was never released; this version carries all of its changes (REVISION_V4.1.15.md).

## Corrections (review P0, confirmed)
- **XP versus FPT.** Section 5 said the problem "is not fixed-parameter tractable (FPT)", and the abstract said "XP but not FPT". Proposition 11 gives an XP algorithm; nothing in the paper rules out an FPT algorithm, and APX-hardness does not either. Section 5 now says the bound is XP rather than FPT and that we neither give an FPT algorithm nor rule one out; the abstract, contributions, Table 1 and conclusion say FPT is open.
- **Weak NP-hardness.** Proposition 9 proves weak NP-hardness (pseudo-polynomial DP); the abstract, Table 1 and conclusion said "NP-hard". They now say "weakly NP-hard with weighted thresholds", and the hardness under credential reuse is stated separately (NP-hard and APX-hard, Proposition 10).
- **Transcript-adaptive observations.** The contributions list and Table 1 said "adaptively chosen observations"; they now say observations whose selection and stopping depend only on the visible transcript, pointing to Table 2 (the abstract never made the claim).

## Additions (review P1)
- Each primary contribution is introduced by the question it answers, and contribution 2 now cites Theorem 6 (witness hitting).
- The introduction states the chain Theorem 14 -> Theorem 15 -> Theorem 24 (information-theoretic criterion; finite histories in the ideal view; concrete profile at the price of L).
- Section 8.2 has a paragraph "What this means for a backup deployment": the bound is conditional, L = 1 under forward-ordered exposure, a few target generations cost about log2 L bits, many late-exposed refreshes make it vacuous, seed renewal starts a new target epoch (protecting new data, not old), and the reused-bank count holds only under Proposition 26's delivery map.
- REPRODUCIBILITY.md records that every release tag v4.1.11-v4.1.14 re-ran the container reproduction from the tagged source in CI, all passing (runs 42677418700, 42683621318, 42692218309, 42699472006).

## Checked, no change needed
- Theorem 24 and Corollary 25 apply L to the whole bracket (the review confirms this; unchanged).
- Bibliography: all 42 cited keys are in references.bib; all 35 DOIs resolve (HTTP 302 at doi.org); 7 entries have no DOI (boneh1996, perlman2007, dauterman2020, connell2024, ma2025, sec2, trapp2025).

## Still open (author actions)
- Independent review of Theorem 24 and Lemmas 22-23 (packet ready).
- LLM-use statement: confirm it covers every AI tool that materially contributed (AUTHOR_CHECKLIST item 0a).

## Checks
- Abstract 246 words (PDF count; limit 250). Clean builds with -halt-on-error: submission 39 pp. (styled 40 pp.), Online Resource 1 21 pp.; 0 overfull/underfull hboxes, 0 undefined references or citations, 0 LaTeX warnings, 0 BibTeX errors, 0 FIGSCALE; no "[?" in either PDF.
- Theorem 24 packet regenerated (page ranges asserted unchanged). Overleaf zip compiles from an empty directory.
- Previous sources: manuscript/main_v4.1.15.tex, manuscript/main_v4.1.14.tex, manuscript/references_v4.1.14.bib.

## SHA-256
- Capability_Exposure_Accounting_v4.1.16.pdf: 2ec50c7ab34e5c8e864ff4dc0a1e365695edbffd7b14094813bdc2bf75a7ff12
- Capability_Exposure_Accounting_v4.1.16_submission.pdf: 9f1540b52895c57924a1c2385878165742c0bcd6453d73c24f229da3897aa8de
- Capability_Exposure_Accounting_v4.1.16_Online_Resource_1.pdf: fd557b48bca5a87dbcfd75d8e509979ac565feaaf1a522b1d5a07146f85fed14
- Capability_Exposure_Accounting_Overleaf_v4.1.16.zip: a7ad547f32a07f77c91af0687dc9a89ccd70865dda24b88cf3f70a8e25f2342c
- manuscript/main.tex: 29192050119465b1e25a22e327323f7e8155da756f3f01f954f6c84cb1467cea
- manuscript/supplement.tex: 65904cfdb1f9be29bc3cb8d9ba03ecb587141e1f0154ef43d9fd70a0e4073a0d
- THEOREM25_REVIEW_PACKET_pp21-28_and_OR1_pp17-21.pdf: 6734460a15c117da895ed2e3299d0e6dd74ea4ecc8a7fe7eed8918d6852c746b

Not released; superseded by v4.1.17 (REVISION_V4.1.17.md) before approval.
