# Revision v4.1.5 (9 November 2026)

Figure revision of v4.1.4, requested by the corresponding author after a figure review (all 15 figures, target 10/10). Artifact remains v4.1.1 (DOI 10.5281/zenodo.24060229); no data file changed. Author choices (9 Nov): Fig. 7 kept and improved rather than removed; sans-serif 8 pt lettering; page count may grow.

## IJIS requirement addressed
"Lettering ... usually about 2-3 mm (8-12 pt)", Helvetica or Arial preferred. v4.1.4 used 5.6-6.6 pt serif lettering and shrank nine diagrams further with \resizebox.

## Changes
- style.tex: \figfont = Helvetica (phv) 8 pt; \figtiny now an alias (nothing below 8 pt); pgfplots axes, ticks, labels, legends at \figfont; titles 8.5 pt bold; no hyphenation inside figure nodes; \figbox replaces \resizebox and logs FIGSCALE if a figure would need shrinking.
- Every figure source rewritten or adjusted to fit at natural size (widths 330-372 pt of 372 pt; Fig. 7 179 of 179 pt).
- Per figure: 1 re-laid out; 2 two side-by-side panels, no stretched maths; 3 deleted roots drawn as dashed honest roots (were red, conflicting with the legend); 4 three rows; 5 "late exposure" label off its arrow, blocked routes end in a cross without an arrowhead; 6 lines under markers, dash vs dash-dot, legend spaced; 7 2^-128 reference line and crossing at K_key ~ 2^64.5 (formula continued beyond the artifact's data range of log2 K <= 64); 8 game chain plus hop table; 9 decade ticks, open markers for 3-of-5, dotted forward-ordered line, aligned legend; 10 bad-event probability inside its box; 11 larger chunks with outcome arrows; 12 shared legend below (it hid data points); 13 legends below (it hid the RSS curve), panel titles; 14 edge labels clear of the states; 15 cells fill the axes, sans cell numbers.
- Captions updated: Figs. 7, 8, 9, 13, 14. Data and code availability: "version 4.1.5".

## Checks
- Both builds with -halt-on-error: 52 pp, 0 overfull boxes, 0 undefined references, 0 LaTeX warnings, 0 FIGSCALE.
- PyMuPDF on the submission PDF: all figure lettering 7.97 pt (8 pt); only maths sub/superscripts are smaller (6 pt and 5 pt), as in standard maths typesetting.
- Every figure inspected at 170 dpi; every page inspected in context.
- Overleaf zip compiles from an empty directory to 52 pp.
- Theorem 25 packet regenerated: pp. 22-32 (Section 8.1 to the start of 8.3).

## SHA-256
- Capability_Exposure_Accounting_v4.1.5.pdf: 27d5f9b97fa9821b98f40bd95c74db0517f32e303b17513d8173c98ad52d1bc5
- Capability_Exposure_Accounting_v4.1.5_submission.pdf: be8b39bb2e365ff5bc9cac863e75fe7b160f6b48664f3435f8d274c4885f19c1
- Capability_Exposure_Accounting_Overleaf_v4.1.5.zip: c7c3eb5714093039cd57ab9235deb4a84157222061100c7aaa24f048a1faa2d8
- THEOREM25_REVIEW_PACKET_pp22-32.pdf: 20b97b3832ce29baca412b1875e92dffa8da1d9c42b06acf80d4141ff9c5357d
