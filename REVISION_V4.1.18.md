# Revision v4.1.18 (10 November 2026)

*Superseded by v4.1.19 (compliance pass), never released.*

One cross-reference correction on v4.1.17, answering a fourth outside review (pasted in chat, 10 Nov 2026). No theorem, proof, number, figure, table or abstract changed; numbering unchanged (Theorem 24). Artifact v4.1.1 is unchanged. v4.1.15 to v4.1.17 were never released; this version carries all of their changes.

## Correction
- **Contribution 3** read "(Theorem 24, Section 9)". Theorem 24 is in Section 8.2 (Section 9 is the formal lifecycle verification). It now reads "(Theorem 24, Section 8.2; lifecycle models, Section 9)". The reviewer proposed "Section 8.2" alone; the second pointer is kept because the same item also claims the TLA+ models and conformance testing, which are in Section 9.
- **Contribution 2** read "(..., Theorems 14 and 15, Section 5)". Theorem 6 is in Section 5, but Lemma 12 and Theorems 14 and 15 are in Section 6, so it now reads "Sections 5 and 6". Found by the sweep below, not by the review.

## Check
A script mapped every label to its enclosing section and compared it with each "result ... Section" pair in the source. These two were the only mismatches.

## Remaining actions from the review (not changed here)
- Independent audit of Lemmas 22-23 and Theorem 24: author action; packet and request are ready.
- Clean-environment reproduction by someone other than the authors: author action (`COAUTHOR_RERUN.md`); CI has re-run it from a fresh pinned container on every release tag since v4.1.11.
- LLM statement against every materially used tool and IJIS policy: author decision.
- Final DOI, bibliography and format check: at release and submission time.

## Build
Clean `-halt-on-error` builds, no undefined references, no BibTeX errors, no overfull boxes; no "[?" in Online Resource 1. Submission 39 pp., styled 40 pp., Online Resource 1 21 pp. Review packet regenerated (13 pp.).

SHA-256: styled `de06df22a1647761a072bf66042424b25b4f155f31b2297483c65dfa09148898`; submission `df1acbeb892f3fd4b3960f9f1d6a60ff93ebe5bbf9fc9d958c44d4f3231a1bdd`; Online Resource 1 `c053c7bc1f9e057f529fd3a2995d8201a1090d223186d9b33dd5f273ba8fc7ae`; main.tex `c54a0286fe38fff1fa381d4fa5d99a68deb8c5553e36754ec5cfebd005891558`; supplement.tex `588f4f88468766bbb220e4f0259beca15a24839301269266ca980db63bf18ebf`.
