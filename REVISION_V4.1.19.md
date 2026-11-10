# Revision v4.1.19 (10 November 2026)

Approved by both authors (10 Nov 2026). Released as tag v4.1.19, Zenodo DOI 10.5281/zenodo.24112284.

Compliance pass on v4.1.18, answering items 2-4 of a fifth outside review (pasted in chat, 10 Nov 2026). No theorem, proof, number, figure, table or abstract changed; numbering unchanged (Theorem 24). Artifact v4.1.1 is unchanged. v4.1.15 to v4.1.18 were never released; this version carries all of their changes.

## Item 3: artifact reproduction
The archived tag v4.1.1 was re-run from a clean extract against this manuscript. All checks pass; see `reproduction_logs_v4119/README.md`.
- 99 tests and all TLC configurations pass.
- All 13 plot-data files are byte-identical.
- Tables S2, S3, S4 and S5, the HMAC timing and the Holders column of Table S11 agree with the regenerated data.

The authors ran this on their own Mac, so it is not an independent reproduction; that is still open (`COAUTHOR_RERUN.md`).

## Item 4: journal compliance (IJIS submission guidelines, read 10 Nov 2026)
- **Abstract and keywords:** the abstract is 246 words (limit 150-250); there are 6 keywords (limit 4-6).
- **Statements and Declarations:** the section is present, with competing interests, funding, author contributions, ethics, data and code availability, and LLM use. Competing interests and author contributions must also be entered in the submission interface.
- **References, DOIs:** all 37 DOIs resolve, and each matches its entry's title in Crossref. They print as https://doi.org links, as the guidelines ask.
- **References, entries without a DOI:** the 8 such entries resolve to the right works.
- **Corrected reference:** Lopuhaä-Zwakenberg et al. is TDSC 20(5), 4169-4187, **2023**; the entry said 2022, with no volume or pages. Fixed.
- **Supplementary file:** it is cited in the text as "Online Resource 1". The guidelines ask each file to name the article title, journal, authors and the corresponding author's affiliation and e-mail. The journal name was missing and is now added. At upload, name the file `ESM_1.pdf` and give it a caption (see AUTHOR_CHECKLIST item 0).
- **Page limit:** the guidelines state none.

## Item 2: LLM statement (author decision; not changed)
The guidelines say:
- LLM use "should be properly documented in the Methods section (and if a Methods section is not available, in a suitable alternative part)";
- AI-assisted copy editing (readability, style, grammar, spelling, punctuation, tone) need not be declared.

The statement currently names only Claude. If ChatGPT's outside reviews led to changes in substance, the policy points to disclosing that. If they only affected wording, no disclosure is needed. Only the authors know which applies.

## Build
Clean `-halt-on-error` builds with no undefined references, BibTeX errors or overfull boxes, and no "[?" in either PDF. Submission 39 pp., styled 40 pp., Online Resource 1 21 pp.

SHA-256: styled `6967376101b96c41e1cc074d3df4f5ba6f9edabb52bb30b9e242c4c664f31bea`; submission `923e09d81449bd073829785c12519c8ee719e6b1f83b59578277d234b63733c8`; Online Resource 1 `f7c0189d8bddfca06037e293c6ab809420c334599b10a3c8171557a672613f63`; main.tex `14613127441c5557b5d6b8deb41b5bfc32bd4dc468dcc867f34e2356fa8332b8`; supplement.tex `427bb1231bd0bce5e7d95bda1234a69404ded55525803d90657d93a565866c94`; references.bib `144aa35bbb8e8ef12320221c8157cddc5ea897f576eb2ecf117e0ca554d2cb39`.
