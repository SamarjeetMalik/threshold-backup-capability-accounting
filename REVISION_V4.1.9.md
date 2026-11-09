# Revision v4.1.9 (9 November 2026)

Wording and structure revision of v4.1.8, requested by the corresponding author as the version to submit to IJIS. Artifact v4.1.1 and all data files are unchanged. No theorem, bound, proof step or reported number changed.

## 1. Version history removed from the paper
The text named its own earlier versions 34 times. Every such passage is now a plain statement or is gone; the history stays in `CHANGELOG.md` and the `REVISION_*.md` files.
- "Corrections to earlier versions" paragraph (after Fig. 7 of v4.1.8): replaced by "Selective exposure and the separate counts", which keeps the two mathematical points it carried: the selective case is Theorem 25 with L = 1 and an Mε_cca capsule term, and the PRF/key-instance counts (q + r) are separate from the AE chunk counts (C, D_dec).
- Theorem 3 part (4), the Proposition 8 remark on sorting, the Section 6.2 title ("Corrected" dropped) and its partial-disclosure remark, the testing sentence after Theorem 15, the truncation remark after eq. (3), the deadline-bound remark, the profile table, the G2′→G3 hop, the lifecycle and conformance text, the truncation and lifecycle figure labels, the abstract and the conclusion.
- The conformance finding is described as what it is: a baseline kernel without the binding and ordering guards (kept in the artifact) diverges in four classes; the reference kernel does not.
- Data statement: names the v4.1.1 artifact (tag and DOI) that reproduces every result, without the manuscript's version history. Preprint statement: points to the all-versions DOI 10.5281/zenodo.24048191.
- Kept on purpose: the wire constant `CEAB-v2-Pedersen-H` (now explained as a fixed label), artifact file names in the supplement, and "version 4.1.1 artifact" where the artifact is cited.

## 2. Length: 55 → 48 pages (submission PDF)
Moved to a new supplement, Online Resource 1 (`manuscript/supplement.tex`, 11 pp.), with a short summary and pointer left in the main text:
- Section 8.3: data-layer and truncation figures, nonce-guard table, the full test list, the measurement method and tables, the two measurement figures (Online Resource 1, Section S1).
- Section 9: the TLC table, the liveness counterexamples, the step-bound statistics, the manual lifecycle induction (former Appendix A) (Section S2); the supervisor test list, cost table and model-correspondence table (Section S3).
- Section 10: a single de-versioned list of checks remains in the paper; the map from each check to its artifact script and expected output is in Section S4.
- Section 8.5 failure-budget table, binding records (former Appendix B), committee figures (former Appendix C and the feasible-threshold figure) (Section S5).
- The paper now has no appendices, so the Fig. 15 placement question no longer arises.
- The supplement reads the paper's numbers through `xr` from `main_submission.aux`; every "Online Resource 1, …S#" pointer in the paper was checked against `supplement.aux`.
- Section 10's numbers were checked one by one against `artifact/expected/v3_results.json` and `v4_results.json`.

The cut is 7 pages, slightly under the 8–10 suggested; further cuts would remove core figures or proofs.

## 3. Theorem 25 review
Packet regenerated: `THEOREM25_REVIEW_PACKET_pp23-34.pdf` (Section 8 start to Section 8.3). Its text differs from the v4.1.8 packet only by the replaced corrections paragraph and one reworded sentence in the G2′→G3 hop; `THEOREM25_REVIEW_REQUEST.md` says so. L stays, full adaptive security is not claimed, Proposition 27 is unchanged.

## Checks
- `main.tex` and `main_submission.tex`: 48 pp. each; `supplement.tex`: 11 pp. All with -halt-on-error: 0 overfull, 0 underfull hboxes, 0 undefined references, 0 LaTeX warnings, 0 FIGSCALE.
- Abstract 250 words (IJIS limit 250) by pdftotext count; 6 keywords.
- Compiled text scanned for "v2/v3/v4", "version", "previously", "corrected", "now fixed": remaining hits are the wire constant, the artifact citation and bibliography entries ("Version 2.0", "version 1.3").
- All pages of both PDFs inspected as contact sheets.
- Overleaf zip compiles from an empty directory (main_submission, then supplement).

## SHA-256
- Capability_Exposure_Accounting_v4.1.9.pdf: 2d9ed4516bcb3526a48fb06438142b72bc633031db4af8d4c00fa9f335cb7a70
- Capability_Exposure_Accounting_v4.1.9_submission.pdf: c0968eaee32e6f930c43a69b3e424e08c3b644cefb893c225bc68b8e2b133135
- Capability_Exposure_Accounting_v4.1.9_Online_Resource_1.pdf: 8ec64eff43b19e58ce9233e6c0e54ef8a68f3ddfd384e78939cfc32d24d5f186
- manuscript/main.tex: 8f06924cfa768b032329a75fe5d958f6096f7acbf774de11bca4fdd3aea8e727
- manuscript/supplement.tex: f6be334dca05748a56492f178cbd9593841feed414cfefc4ab86758d51f178c1
- THEOREM25_REVIEW_PACKET_pp23-34.pdf: 51c380e4864302b3064eac9ad91e163775f2d3c76b115ded367413ef60083dfa

Approved by both authors 9 Nov 2026; released as tag v4.1.9, Zenodo DOI 10.5281/zenodo.24090414.
