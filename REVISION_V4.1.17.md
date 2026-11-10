# Revision v4.1.17 (10 November 2026)

*Superseded by v4.1.18 (one cross-reference correction), never released.*

Corrections only, on v4.1.16, answering a third outside review (pasted in chat, 10 Nov 2026). Each point was checked against the source first. No theorem statement, proof or number changed; numbering unchanged (Theorem 24). Artifact v4.1.1 is unchanged. v4.1.15 and v4.1.16 were never released; this version carries all of their changes.

## Corrections
- **Table 1, witness-hitting row:** "NP-hard with reused credentials" now reads "NP-hard and APX-hard with reused credentials" (Proposition 10), matching the abstract and conclusion.
- **Abstract, touched indices:** now states Theorem 14's hypotheses: honestly generated Pedersen-committed generations with independent coefficient blocks and pointwise disclosures. To stay under 250 words, "3,000 seeded histories with 5,388 target seeds" became "3,000 random histories" (both numbers stay in Section 6 and Section 10) and "a baseline with four defect classes" became "a defective baseline" (the four classes stay in Section 9).
- **Manuscript-artifact mapping:** the data availability statement now says the artifact has not changed since v4.1.1, that later manuscript revisions (including 4.1.17) changed only text, figures and layout, and that every number is produced by the v4.1.1 artifact. README states that artifact v4.1.1 supports manuscript versions 4.1.1 to 4.1.17.

## Checked, no change needed
- Contribution 2 already distinguishes the XP bound from the open FPT question (fixed in 4.1.16).
- Artifact correspondence: `artifact/` is byte-identical to tag v4.1.1 (`git diff v4.1.1 -- artifact` empty at every release since). `reproduce_all.py` compares the v3/v4 checkers with `expected/*.json` and every TLC configuration with its recorded outcome and counts; it ran from a fresh pinned container on each release tag v4.1.11-v4.1.14, all passing (REPRODUCIBILITY.md). Benchmark timings are measurements, not reproduced values.

## Not changed (author decision)
- **LLM-use statement.** The review says ChatGPT assisted with review and revision. The statement names only Claude. Whether to add another tool, and what it did, is for the authors to state; nothing was added (AUTHOR_CHECKLIST item 0a).
- **Independent review of Theorem 24.** Still open; packet ready.

## Checks
- Abstract 246 words (PDF count; limit 250). Clean builds with -halt-on-error: submission 39 pp. (styled 40), Online Resource 1 21 pp.; 0 overfull/underfull hboxes, 0 undefined references or citations, 0 LaTeX warnings, 0 BibTeX errors, 0 FIGSCALE; no "[?" in the PDF.
- Theorem 24 packet regenerated (page ranges asserted unchanged). Overleaf zip compiles from an empty directory.
- Previous source: manuscript/main_v4.1.16.tex.

## SHA-256
- Capability_Exposure_Accounting_v4.1.17.pdf: 1400373b85cbd851f8ce7fe480b8da867a8813c39397db7d9a066640476e2e7f
- Capability_Exposure_Accounting_v4.1.17_submission.pdf: 7cb8aced791f23fff92fc2f00047ac65f9cec4dec07e599d826bd5be7aad0739
- Capability_Exposure_Accounting_v4.1.17_Online_Resource_1.pdf: f6fe34de1d7d9781625ab0656f46b4805aca00e898648abb86395addb4da0449
- Capability_Exposure_Accounting_Overleaf_v4.1.17.zip: 15a2279a89066b25eb1961ef327fa2438b4239283a5512bbac6f7bcb240b4646
- manuscript/main.tex: 3843903806de6f4b24b247b206501fd9de0dc9899d59a1e214c70ef86296429e
- manuscript/supplement.tex: 0b649c636fb784f9c38cbe5df4e0a50bac9941ff5fe4d91848af5641006ef155
- THEOREM25_REVIEW_PACKET_pp21-28_and_OR1_pp17-21.pdf: 7cb3d8f4ab1bc76efc249302ee3411b4c5117cbf28080cdb89df725013c4459b

Not yet approved; needs both authors' approval before release.
