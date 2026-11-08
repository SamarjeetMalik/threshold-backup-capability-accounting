# v4.0.8 → v4.0.9: reviewer-objection pass and figure revision

Capability Exposure Accounting for Threshold-Based Encrypted Backup Recovery.
Samarjeet Malik (Ashoka University) and Shaurya Pratap Singh (Indian Institute of Science).
8 November 2026. Baseline v4.0.8 is unchanged; its text is kept as `manuscript/main_v4.0.8.tex`.

This revision works through the outside critique of v4.0.8 and its figure plan. It adds no theorem, no new security claim and no new measurement. The abstract (234 words) and the keywords are as in v4.0.8.

## 1. Technical audit

Classes: **R** = required, **Rec** = recommended, **E** = editorial.

| # | Finding | Class | Resolution |
|---|---|---|---|
| A1 | §9.3 said "exact agreement on **whole reachable sets**". `v4_refinement.py` compares only **state counts**: TLC's state set is never exported or matched. | R (overclaim) | Corrected to "matching state counts". The text now says that equal cardinalities alone would not establish equal sets. The same correction is in the limitations. |
| A2 | The three-step conformance allowance was unexplained. | R | New paragraph "Why a step bound". The bound is a search depth, not a tolerance. The recorded data show it was never needed: of 80,000 v4 calls, 69,987 were stutters, 9,987 matched one step and 26 matched two; none needed three. The v3 kernel also had no three-step match. |
| A3 | The scope of the nonce guard (threads, processes, restarts) was not stated. | R | It is stated now. The guard is an in-memory set of one instance, locked against that process's threads, not shared and not persistent. A new test demonstrates the per-instance scope, and the proof does not rely on the guard. |
| A4 | The representation of an empty object was not stated, nor what happens when every chunk is removed. | R | Stated: one zero-length chunk with final = 1 (16-byte ciphertext). An empty Open is rejected before derivation, so removing all chunks never decodes as empty. New tests cover it. |
| A5 | Several edge cases had no regression test. | R | `artifact/test_datalayer_v409.py` adds 7 tests (see §3). |
| A6 | Notation collisions: L (deletion floor vs. guessing factor), M (basis vs. capsules), K (root set, seed block, key instances), D (seed domain, distinguisher, decryptions). | Rec | Renamed: L_floor, M_U, 𝒦 (root set), T̄ (rest block), 𝒟 (seed domain), 𝒜′ (distinguisher, including Definition 22, where D was also the decryption count). New Table 2 (notation) lists the remaining **local** reuses: the deletion set D in §5, the polynomial D(X), the latencies in Proposition 20, and R and W in Proposition 9. |
| A7 | Theorem 15 (ideal view) and Theorem 25 (real HPKE) were linked only in a parenthesis. | Rec | New paragraph "From the ideal view to real capsules". |
| A8 | The practical meaning of L was not tabulated, and the non-vacuity condition was not stated. | Rec | New Table 10 (L and log₂L). New paragraph: the bound is informative only if L·ε_base < ½, and a target of 2^−λ needs ε_base ≤ 2^−λ/L. The table notes that log₂L is a loss of the bound, not a security level. |
| A9 | The failure budget could read as a quantified guarantee. | Rec | Renamed "Symbolic failure budget", with Table 12 (term, event, evidence needed) and an explicit sentence that α is unconstrained. |
| A10 | The novelty of §5 relative to attack trees needed to be explicit. | Rec | New paragraph "What is specific here", and a worked triangle instance for Proposition 10: reused banks need 2 deletions (the vertex-cover number), renewed banks need 3. Proposition 11's doubly exponential cost was already stated; Table 15 repeats it. |
| A11 | The applicability of the rank test was scattered across the text. | Rec | New Table 4, and a paragraph on building A and B from a history (its rows match `v4_temporal.py`, which was checked). |
| A12 | There was no single statement of each main result's hypotheses. | Rec | New Table 15 (assumptions and scope), plus a "Three primary contributions" paragraph that groups the seven contributions into (A), (B) and (C). |
| A13 | Eleven figure/table labels were never cited in the text: Table 1, Figs. 1, 2, 3, 5, 6, 8, 9 and 14 in v4.0.8 numbering, the minimum-committee-size figure and the new Table 4. | E | Every float is now cited. |
| A14 | The class printed "Corresponding author(s). E-mail(s):" for one author. | E | `\patchcmd` on `\@maketitle` now prints "Corresponding author. E-mail:". The class file is unchanged. |
| A15 | The benchmark numbers appeared only in plots. | Rec | New Table 11 with medians and IQR from the recorded data. The FEAT_AES/FEAT_PMULL note comes from `sysctl` on the measuring machine. `tracemalloc` is described as measuring heap, not resident memory. |
| A16 | Version relationship between manuscript and artifact. | R | The declaration says the manuscript is v4.0.9 and the artifact is v4.0.7 plus one test file. It contains a new placeholder for the v4.0.9 archive DOI and tag. `REPRODUCIBILITY.md` added. |

**Checked and found correct (no change needed):** Theorem 3 parts (1)–(5); Corollary 5's three conditions and its counterexamples; Theorem 25's L multiplying the whole bracket; the q(q−1)/2²⁵⁷ and K(K−1)/2²⁵⁷ terms; Lemma 24's mixture argument; Proposition 27's assumptions; Proposition 11's stated running time. I did not re-derive every hybrid hop of Theorem 25 line by line in this pass. That audit was done in v4.0.3–v4.0.4 (REVISION_V4.0.3.md, REVISION_V4.0.4.md), and none of that text changed.

**Not done in this revision (open):**
- **Related-work re-audit of CKS and GKP/Grappa.** The manuscript still says these comparisons were not re-audited. A security-property matrix would need the full papers, and I did not read them in this pass.
- **No ACM TOPS build.** Only a checklist is given (§6). The authors should choose one venue, and submissions must not be simultaneous.
- **Figure redesigns not attempted:** Fig. 1 (source categories, AND semantics), Fig. 2 (five-step layout), Fig. 3 (witness root-set labels), Fig. 8 (two-row hybrid layout, larger labels), Fig. 10 (separate derivation/encryption blocks, two collision cases) and Fig. 14 (three swim lanes). Their content is correct but their small text remains small. Fig. 5 was not expanded either, because its numerical example is now Fig. 4.
- **No new measurements.** Concurrency, streaming and multi-machine measurements were not run, and the text says so.

## 2. Change log (manuscript)
- Front matter: "Corresponding author" in the singular. The abstract and keywords are unchanged.
- §1: a motivating example (7 holders, t = 5, three sharings, copies after g₁ and g₂) and "Three primary contributions".
- §3: Table 2 (notation); L_floor.
- §4: notation M_U, 𝒟 and T̄; Table 4 (rank-test applicability); "Building A and B from a history"; citations for Figs. 1–2.
- §5: "What is specific here"; the worked triangle instance; Fig. 3 cited.
- §6: 𝒦 in the closure and temporal results; "From the ideal view to real capsules"; "A worked history" with the new Fig. 4; Table 5 cited.
- §7: the Fig. 6 bounds are described, and the committee-size figure moved to Appendix C (Fig. C1).
- §8: 𝒜′ in Definition 22 and Lemmas 23–24; "When the bound is useful" and Table 10; Proposition 27's assumptions spelled out; the data-layer empty-object and guard-scope paragraph; 27 tests listed; the AES hardware note; Table 11; Figs. 12 and 13 of v4.0.8 merged into one two-panel Fig. 12; "Symbolic failure budget" and Table 12.
- §9: the state-count correction (A1); "Why a step bound" (A2); Fig. 14 cited.
- §10: counts updated to 89 tests, with both fresh reproduction runs recorded.
- §11: Table 15 (assumptions and scope); the Refinement paragraph now says the Python kernel cannot terminate worker threads.
- Statements and Declarations: the version relationship, plus one new placeholder (§4).
- Appendix C: committee-size reference (Fig. C1).
- Length: 42 → 48 pages, from the tables and Fig. 4. No text was deleted.

## 3. Artifact change
`artifact/test_datalayer_v409.py` adds seven tests:
1. truncation that keeps 1, 2 or 3 of 4 chunks;
2. all chunks removed vs. the legitimate empty object (a 16-byte ciphertext, rejected before derivation);
3. a modified header;
4. a forged final chunk in a non-final position;
5. a non-final chunk in the final position;
6. 40 objects stored from 8 threads: no key-nonce reuse, and all objects round-trip (under CPython's GIL, so this tests locking, not parallel speed);
7. the guard is per-instance: two instances with forced equal key bytes both encrypt.

`reproduce_all.py` runs the new file, and the artifact README describes it. No other code, model, expectation or evidence file changed.

**Runs:** the v4.0.7 archive passes 82/82 from a fresh unpack. The v4.0.9 tree passes 89/89, with all TLC configurations in both runs. Logs are in `reproduction_logs_v409/`.

## 4. Author-supplied placeholders still in the PDF (bold `[Author-supplied placeholder: …]`)
1. Competing interests.
2. Funding.
3. Author contributions (CRediT roles; do not guess who did what).
4. Use of large language models. IJIS requires this to be documented unless the use was copy-editing only.
5. **New:** the archive DOI and release tag of the v4.0.9 artifact, once it is published.

None of these may survive into the submitted PDF. Running `grep -c authorinput manuscript/main.tex` finds 7 lines: the macro definition, a comment and the five uses. The placeholder text appears 5 times in each PDF.

## 5. Figure-by-figure log (v4.0.9 numbering)
| Fig. | Change | Analytical / measured |
|---|---|---|
| 1 | cited in text; no redesign | schematic |
| 2 | cited; no redesign | schematic |
| 3 | cited; no redesign | schematic |
| **4 (new)** | worked history: event order, reused vs. renewed grids, touched counts (5,5,5) vs. (4,1,0) against t, outcome | derived from Theorem 15, not measured |
| 5 | unchanged (old Fig. 4) | schematic |
| 6 | boundary lines t_min = 2f+c+u+1 and t_max = n−f−u, legend, 8 pt fonts; the lines pass exactly along the feasible squares | analytical |
| 7 | operating point K = 2²⁸ marked; label "bound < 2⁻²⁰¹"; larger fonts | analytical |
| 8 | cited; no redesign | schematic |
| 9 | legend in figure; pins at 970,299 and 3,991; 8 pt fonts | exact analytical |
| 10 | unchanged | schematic |
| 11 | release rule added: all chunks authenticate with final = 1 on the last, or nothing is released | executed test |
| 12 | old Figs. 12 and 13 merged: (a) time with IQR; (b) throughput with bars from the time quartiles | measured (v4.0.4) |
| 13 | caption: `tracemalloc`, one trial per size, not resident memory; 2× line explained | measured (v4.0.4) |
| 14 | cited; no redesign | schematic |
| C1 | moved to Appendix C | analytical |

Provenance is listed in `REPRODUCIBILITY.md`. Every page of both PDFs was inspected as rendered images: nothing is clipped or overlapping, and there are no orphaned captions. Font size: Figs. 6, 7, 9 and 12 use 8 pt labels. Fig. 4 is scaled to 92% of its natural width, so its labels are about 7.4 pt and its bar values about 6.4 pt. Figs. 1–3, 5, 8, 10, 11 and 14 keep their v4.0.8 6.6/5.6 pt diagram fonts, which is below the 8–9 pt the critique asks for.

## 6. Checklists

### IJIS (Springer, sn-jnl)
- [x] Abstract 150–250 words (234 in the source, 240 by pdftotext); 6 keywords
- [x] `twocolumn`; 0 overfull boxes; 0 undefined references; both builds 48 pp
- [x] "Statements and Declarations" heading
- [ ] Fill the 5 placeholders (§4)
- [x] Corresponding author with e-mail
- [ ] ORCID iDs (optional)
- [ ] Publish the v4.0.9 artifact (GitHub tag and Zenodo version), then insert its DOI
- [ ] APC decision (US$3,690); any waiver must be requested at submission; check Ashoka coverage
- [ ] Re-audit CKS/GKP (open item above) before submission if possible
- [ ] Upload the source (Overleaf zip) and PDF; declare the preprint DOI and its licence at submission

### ACM TOPS (not built)
- [ ] Rebuild in `acmart` (`acmsmall`, ACM reference format) with CCS concepts
- [ ] A shorter security-centred narrative; proofs moved to appendices or supplementary material
- [ ] Check ACM's policy on the CC BY preprint and on LLM disclosure
- [ ] Do not submit to IJIS and TOPS at the same time

## 7. Builds
Both builds were run from clean with `latexmk -pdf -halt-on-error`: exit 0, 0 overfull boxes, 0 undefined references, 48 pages each. A grep for `^- ` in `.tex` files finds nothing.
