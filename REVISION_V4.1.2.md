# v4.1.2: layout-only revision of v4.1.1 (9 November 2026)

Not released or published. v4.1.1 (DOI 10.5281/zenodo.24060229) is unchanged.

- Appendix headings run on at full column width. Previously the title was hung beside "Appendix B" in a narrow box ("Binding / and / inventory / records").
- Removed the `\clearpage` before the bibliography. It forced Fig. C1 onto a page of its own, leaving most of that page blank. The references now start directly after Appendix C, and Fig. C1 sits at the top of the next page.
- The data statement now says "version 4.1.2, a layout-only revision of version 4.1.1 with unchanged text and results". The artifact is still v4.1.1.
- Result: 52 → 51 pages. Both builds use halt-on-error and have 0 overfull boxes and 0 undefined references.
- A word-level diff against v4.1.1 shows only the version sentence and changed hyphenation.
- Remaining short columns (2–5 lines, pp. 3, 5, 12, 17, 36) are ordinary breaks before headings and lists. They were left alone.
