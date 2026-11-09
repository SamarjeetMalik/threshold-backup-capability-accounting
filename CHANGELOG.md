# Changelog

## 4.1.11 (9 November 2026), manuscript presentation, references and reproducibility; artifact remains v4.1.1
- Results at a glance: new Table 1 after the contributions, one row per main result with its section.
- Running example: the introduction's history (three 5-of-7 generations, copied bank roots) is named as such and used in Sections 6.3 and 8.2.
- Notation table: only symbols used across sections (seven single-section symbols are defined where they appear).
- Sections 8.4 (independent-slot component, now Lemma S1) and 8.5 (symbolic failure budget, now eq. (S1) and Table S8) moved to Online Resource 1, Section S5; a short paragraph in Section 8.3 states both results.
- Section 6.2: "What Theorem 14 establishes" and "Scope of the exponent view" merged (the efficient-adversary remark was stated twice).
- Figures redrawn: Fig. 1 outcome arrows through a bus; Fig. 4 panel (d) folded into (c); Fig. 9 as panels (a) path and (b) request with orthogonal routing. A side-by-side layout for Fig. 9 does not fit the 13 cm text width.
- References: DOIs added to seven entries (Herzberg et al. 1995, Zhou et al. 2005, Marsh-Schneider 2004, Reardon et al. 2013, Mauw-Oostdijk 2006, Panjwani 2007, Hazay et al. 2015), each checked on Crossref for title, authors, venue and pages. The remaining eight entries without a DOI have none (USENIX, NDSS, arXiv, ePrint, SECG, book). The Crossref DOI for Perlman's assured-delete paper belongs to a 2005 workshop version, not the cited NDSS 2007 paper, and was not used.
- Second machine: the x86 benchmark (Slurm job 8081, 2-socket AMD EPYC 9554) completed; evidence in evidence_x86_epyc9554/ (lab paths and host name redacted), reported in Section 8.3 and Online Resource 1, Table S3. Limitations now say the data-layer measurements come from two machines and the supervisor costs from one.
- Container: Dockerfile and CONTAINER.md (pinned by digest; not yet built).
- Not done here: ORCID iDs (need the authors' iDs); independent review of Theorem 25; Shaurya's re-run; new mathematical results.
- Main text 46 pp. (submission; styled 47), Online Resource 1 12 pp.; abstract 235 words. Previous text: manuscript/main_v4.1.10.tex, supplement_v4.1.10.tex, references_v4.1.10.bib, figures_v4.1.10/.

## 4.1.10 (9 November 2026), manuscript presentation; artifact remains v4.1.1
- Caveats consolidated: each limitation is stated once where it matters and once in Section 11. Removed repeats: the selective-opening remark in the abstract and in contribution 5 (kept in the Theorem 25 box, Section 8.2 and Section 11), "testing, not a refinement proof" in contribution 7 (kept in Section 9.3 and Table 12), two hedges in Section 2, the duplicate efficiency remark after Theorem 14, "not a measurement" after Fig. 4 (kept in its caption), two remarks after Proposition 27 (kept in the "Reused banks are not safer" box), "no asserted value" before eq. (8), the logical-state remark in Section 9.3, and the selective-opening clause of the conclusion. "Not full adaptive security" still appears in the abstract, contribution 5, the Theorem 25 box, Section 11 and the conclusion; L is unchanged.
- Section 9.3: the state-count caveat is one sentence instead of two.
- Section 10: the list of checks is now Table 11 (same numbers, same order); Online Resource 1 Table S6 maps its rows to scripts.
- Section 11: the six limitation paragraphs are one paragraph covering only what Table 12 does not (composition loss and audit status, system contracts, physical erasure), plus "Nature of the contribution". Table 12's TLC row now also names the manual model composition and the assumed renewal algebra.
- Fig. 6 (derived-key collision bound) is taller (6.8 cm plot height, was 5.6 cm).
- Abstract 235 words (was 250). Main text 47 pp. (was 48); Online Resource 1 11 pp. Previous text: manuscript/main_v4.1.9.tex, supplement_v4.1.9.tex, figures_v4.1.9/plot_keycoll.tex.
- Kept \raggedbottom: \flushbottom stretched six pages past badness 10000.
- Approved by both authors 9 Nov 2026; released as tag v4.1.10, Zenodo DOI 10.5281/zenodo.24090614.

## 4.1.9 (9 November 2026), manuscript wording and structure; artifact remains v4.1.1
- Version history removed from the paper (it stays in this changelog and the REVISION files). The paragraph "Corrections to earlier versions" is replaced by a paragraph on selective exposure and why the PRF/key and AE counts are separate; sentences naming v2.0.0, v3, v4, v4.0.x or v4.1.x are restated plainly (Theorem 3 part (4), Proposition 8 remark, Section 6.2 title and remark, Theorem 15 testing, eq. (3) truncation remark, deadline bound remark, profile table, G2'->G3 hop, lifecycle and conformance text, figure text of the truncation and lifecycle figures). The baseline kernel in the conformance test is now described as such. The domain tag CEAB-v2-Pedersen-H is a wire constant and stays.
- New supplement, Online Resource 1 (manuscript/supplement.tex, 11 pp.): data-layer tests, measurements, Table and Figs. of the measurements, the nonce-guard table, the data-layer and truncation figures, every TLC configuration, liveness counterexamples, the manual lifecycle induction (former Appendix A), conformance step statistics, supervisor tests and cost table, the model-correspondence table, an evidence map from each check to its script, the failure-budget table, binding records (former Appendix B) and the committee figures (former Appendix C and the feasible-threshold figure). The main text keeps a summary of each with a pointer.
- Section 10 is one de-versioned list of checks; every number matches artifact/expected/*.json. The data statement names the v4.1.1 artifact only; the preprint statement points to the all-versions DOI.
- Abstract 250 words. Main text 48 pp. (submission and styled; was 55/56), no appendices. Previous text: manuscript/main_v4.1.8.tex, figures_v4.1.8/.
- Theorem 25 review packet: pp. 23-34 (THEOREM25_REVIEW_PACKET_pp23-34.pdf).
- Approved by both authors 9 Nov 2026; released as tag v4.1.9, Zenodo DOI 10.5281/zenodo.24090414.

## 4.1.8 (9 November 2026), manuscript layout only; artifact remains v4.1.1
- Single column: the class options are now `[pdflatex,sn-mathphys-num]`, exactly as in the official Springer Nature template sample (sn-jnl.cls and sn-mathphys-num.bst are byte-identical to the current template download). The `twocolumn` option had split the template's single-column text area (131 x 194 mm) into two narrow columns.
- Display equations that had been broken for narrow columns are set on one or two lines: Corollary 2, eq. (2), eq. (5), Lemma 24 (statement displayed, proof mixture on one line), Theorem 25 eq. (7), Corollary 26, eq. (8). No symbol or term changed.
- Fig. 15 panels enlarged to fill the text width (350 of 372 pt); still 8 pt, unscaled, numbered 15, in Appendix C before the References. Tables 1 and 5: narrow columns set ragged-right.
- Theorem 25 review packet regenerated for the new page numbers: pp. 24-34 (THEOREM25_REVIEW_PACKET_pp24-34.pdf).
- 56 pp. styled, 55 pp. submission. No theorem, number, caption text, data file or artifact file changed. Previous text: manuscript/main_v4.1.7.tex, figures_v4.1.7/plot_minholders.tex.
- Approved by both authors 9 Nov 2026; released as tag v4.1.8, Zenodo DOI 10.5281/zenodo.24089585.

## 4.1.7 (9 November 2026), manuscript layout only; artifact remains v4.1.1
- Fig. 15 is now non-floating and sits in Appendix C after its heading and paragraph, before the References. In v4.1.6 it floated to p. 48 ahead of the Appendix B heading. It is single-column with three compact panels, still 8 pt and unscaled, and still numbered 15.
- Documentation: AUTHOR_CHECKLIST.md records the completed co-author confirmations and the public records; REPRODUCIBILITY.md now names manuscript v4.1.7 and the v4.1.1 artifact as the source of every result.
- 52 pp. No theorem, number, caption text, data file or artifact file changed. Previous text: manuscript/main_v4.1.6.tex, figures_v4.1.6/plot_minholders.tex.
- Approved by both authors 9 Nov 2026; released as tag v4.1.7, Zenodo DOI 10.5281/zenodo.24088767.

## 4.1.6 (9 November 2026), manuscript figures only; artifact remains v4.1.1
- Muted palette (deep blue 1F3A5F, brick red A93226, grey 5E6670), white boxes with thin 1 pt corners, lighter grid; layer titles in black.
- Tick numbers and powers of ten on every axis now in the sans figure font.
- Fig. 14 re-routed: no arrow crosses another. Fig. 9 callouts use leader lines and sit clear of the data; panel titles capitalised.
- Fig. 7: adds the same birthday bound for hypothetical 128-bit key instances, for comparison only; caption updated.
- 52 pp. No theorem, number, data file or artifact file changed. Previous text: manuscript/main_v4.1.5.tex, style_v4.1.5.tex, figures_v4.1.5/.

## 4.1.5 (9 November 2026), manuscript figures only; artifact remains v4.1.1
- All 15 figures: lettering is Helvetica (URW Nimbus Sans) at 8 pt, as IJIS asks (8-12 pt, sans serif); maths keeps the math font. No figure is scaled: `\figbox` typesets each at natural size and the build log records FIGSCALE if one would need shrinking (none does).
- Layout fixes: Fig. 12 and 13 legends moved off the data; Fig. 14 edge labels clear of the states, grey arrows explained in the caption; Fig. 5 "late" label off its arrow; Fig. 8 now a game chain plus a hop/replacement/loss table; Figs. 1-5, 10, 11 re-laid out to fit at 8 pt; Fig. 6 lines drawn under the markers, distinct dash styles; Fig. 9 decade ticks and an aligned legend; Fig. 15 cells fill the axes.
- Fig. 7 now shows the 2^-128 level of the profile's 128-bit target and where the bound meets it (K_key ~ 2^64.5). Captions of Figs. 7, 8, 9, 13 and 14 updated to match.
- 52 pp. (was 51). No theorem, number, data file or artifact file changed. Previous text: manuscript/main_v4.1.4.tex, style_v4.1.4.tex, figures_v4.1.4/.

## 4.1.4 (9 November 2026), manuscript only; artifact remains v4.1.1
- IJIS compliance: the appendix figure is numbered Fig. 15 (consecutive with the main text) instead of Fig. C1; Section 10 now points to the LLM-use statement, since IJIS asks for LLM use to be documented in the methods part.
- Data and code availability names the manuscript as version 4.1.4. 51 pp. Nothing else changed. Previous text: manuscript/main_v4.1.3.tex.

## 4.1.3 (9 November 2026), manuscript only; artifact remains v4.1.1
- Data and code availability names the v4.1.1 artifact (DOI 10.5281/zenodo.24060229, tag v4.1.1) as the one supporting the paper; v4.0.7 is named only as its predecessor. The duplicate archive paragraph is gone.
- Fig. C1 is output before the References and no longer splits the bibliography.
- Wording: the conclusion now states the integrated contribution in place of "the core mathematics is elementary". The introduction's "elementary linear algebra" sentence was reworded. The abstract says the reused-credential bound is XP but not FPT. The evidence list says how the 5,388 target seeds are counted. The LLM statement says what figure preparation means.
- Root README corrected from 82 to 99 tests. REPRODUCIBILITY.md records the Zenodo record as published. Author checklist updated. Theorem 25 review request and page packet added.
- 51 pp. No theorem, bound, number or artifact file changed. Previous texts: manuscript/main_v4.1.1.tex and main_v4.1.2.tex.

## 4.1.2 (9 November 2026), layout only; not released
- Appendix headings at full width; removed the \clearpage before the bibliography (52 → 51 pp).

## 4.1.1 (9 November 2026)
- Release-consistency pass; details, Theorem 25 audit record and open items in REVISION_V4.1.1.md. Previous text preserved as manuscript/main_v4.1.0.tex.
- Related work re-checked against the full texts of CKS, standard-model CKS and GKP. The GKP sentence was corrected (its security is selective only). CRYPTO and TCC proceedings citations.
- Timings re-run on the Apple M5. Memory re-run (7 trials). New measurement of supervision cost.
- Supervisor: lifeline pipe, so a worker exits when its supervising process is SIGKILLed. 4 new tests (10 supervisor, 99 in total).
- Notation K_key and D_dec. Definition 22 states label-specific decryption exclusion and no challenges under corrupted keys.
- Abstract and contribution list tightened; nonce-scope table; limitations regrouped; Fig. C1 placed before the References.
- rc2: supervision trade-off (3.8x at 64 MiB; fixed ~47 ms dominates at 1 MiB; combined RSS not measured); "target seeds" used consistently.

## 4.1.0 (9 November 2026)
- Finalisation pass; details in REVISION_V4.1.0.md. No theorem, bound or earlier result changed. Previous text preserved as manuscript/main_v4.0.9.tex.
- Notation: 𝒦_root (root set), 𝓔 (erasure set), Φ(X), T_rt/T_log/T_app/T_loc (Proposition 20). K and D now each have one meaning.
- Proposition 11 described as XP, not FPT. New paragraphs: what Theorem 14 establishes; operational reading of Corollary 16; reading Table 10 in log2 L.
- Corrected a false v4.0.9 statement that the kernel runs workers as threads. Added a process-isolated worker supervisor with 6 tests (§9.4). 95 tests pass.
- Memory re-measured with 7 trials per size: heap and process RSS (evidence_v410). Fig. 13 and Table 11 updated.
- Declarations completed from the corresponding author's answers. One placeholder remains: the v4.1.0 artifact DOI and tag.
- Fig. 8 labels enlarged; the stranded last reference is gone.

## 4.0.9 (8 November 2026)
- Reviewer-objection pass; details and audit in REVISION_V4.0.9.md. No new theorem, claim or measurement. Previous text preserved as manuscript/main_v4.0.8.tex.
- Corrected an overclaim: the Python transcription matches TLC by state counts, not by reachable sets. Explained the conformance step bound (max observed distance 2 of 3).
- Notation: L_floor, M_U, 𝒦, T̄, 𝒟, 𝒜′; Table 2 (notation).
- New tables: rank-test applicability (4), guessing factor with log2 L (10), recorded measurements (11), symbolic failure budget (12), assumptions and scope (15).
- New text: motivating example; three primary contributions; building A and B; what §5 adds over attack trees; worked vertex-cover instance; ideal-to-real bridge; non-vacuity condition for Theorem 25; empty object and nonce-guard scope.
- Figures: new Fig. 4 (worked history, derived); Fig. 6 bounds; Fig. 7 operating point; Fig. 9 legend and labels; Fig. 11 release rule; latency and throughput merged (Fig. 12); committee-size heatmap moved to Appendix C; every float cited.
- Artifact: test_datalayer_v409.py (7 tests), run by reproduce_all.py: 89 tests pass. The archived v4.0.7 artifact re-runs to 82/82 from a fresh unpack. REPRODUCIBILITY.md and reproduction_logs_v409/ added.
- "Corresponding author" in the singular (title-block patch; class unchanged). Declarations: version relationship and a fifth placeholder (v4.0.9 artifact DOI).

## 4.0.8 (8 November 2026)
- Manuscript formatted for the International Journal of Information Security (IJIS). Only presentation, front matter and declarations change; no theorem, proof, number, test or artifact file changed. Previous text preserved as manuscript/main_v4.0.7.tex.
- Abstract cut from about 396 to 234 words. It keeps the restricted-adaptive qualification, the sentence "it does not provide full adaptive security", the loss factor L and the receiver selective-opening remark. Dropped from the abstract (still in the body): the L = 16 example, the 3,991 vs 970,299 reused-bank count, the advantage-convention and key-coincidence sentence, the data-layer and measurement sentences, and the 2,000-schedule detail.
- Keywords cut from 9 to 6: Capability exposure, encrypted backup, threshold recovery, cryptographic erasure, restricted-adaptive security, TLA+. Removed: linear secret sharing, selective opening, refinement.
- `twocolumn` sn-jnl option. Tables 1, 3, 8 and 9 and Figs. 2, 3, 4 and 11 moved to `table*`/`figure*`; column widths of Tables 2, 5 and 6 adjusted and Table 4 set in footnotesize; plot widths of Figs. 7, 12 and 13 set relative to the column; 11 displayed equations broken across lines (no change to their content); bibliography URLs made breakable (`\burl` routed through xurl's `\url`). 0 overfull boxes in both builds.
- `\bmhead{Declarations}` replaced by a "Statements and Declarations" section: competing interests, funding, author contributions and LLM use as author-supplied placeholders; ethics; data and code availability (DOI 10.5281/zenodo.24048192, MIT / CC BY 4.0); preprint disclosure.
- Corresponding author: Samarjeet Malik, samarjeet.malik_tf@ashoka.edu.in (underscore escaped in `\email`).

## 4.0.7 (8 November 2026)
- Zenodo DOI 10.5281/zenodo.24048192 (reserved for this version) added to the declarations, README, CITATION.cff and artifact README. No other change. Previous text preserved as manuscript/main_v4.0.6.tex.

## 4.0.6 (7 November 2026)
- Licences: MIT for everything under artifact/ (`LICENSE`); CC BY 4.0 for the manuscript, figures, plot data and reports (`LICENSE-CC-BY-4.0.txt`, official legal code from creativecommons.org). Springer class/style files keep their upstream terms.
- Declarations name tag v4.0.6 and the licences. No other change. Previous text preserved as manuscript/main_v4.0.5.tex.
## 4.0.5 (6 November 2026)
- Restricted-adaptive qualification made explicit everywhere it matters: abstract ("it does not provide full adaptive security", with L = 1 / 16 / exponential), keywords, contribution 5, the Theorem 15 note, the Section 8 title, a warning box directly after Theorem 25 ("Restricted, not full, adaptive security": L = 970,299 for three renewed 5-of-7 generations; the bound is vacuous when L is large; removing L would need receiver selective-opening security that HPKE is not known to have), and the conclusion.
- No theorem, proof, number, test or artifact code changed. Previous text preserved as manuscript/main_v4.0.4.tex.
## 4.0.4 (6 November 2026)
- Lemma 24: proof rewritten as a common-mixture argument (the v4.0.3 proof bounded real and ideal probabilities separately, which only gives 2*delta).
- Data layer: record validation before key derivation (malformed and foreign records rejected); lock around key cache, nonce guard and identifier index; 11 new regression tests (completeness, final markers, duplicates, partial failure, aliasing, retry, nonce reuse). 20 data-layer tests in all.
- Benchmarks re-run with seeded data, 5 warm-ups, 40 / 12 repetitions, median and IQR, AES-256-GCM comparison (`bench_v404.py`, raw data in evidence_v404).
- 15 vector figures and plots (TikZ/PGFPlots) with data regenerated by `make_plot_data.py`.
- Styled build (main.tex) and submission build (main_submission.tex) from one source; palette, sparing callout boxes, styled tables.
- Tests: 82.

## 4.0.3 (6 November 2026)
- Advantage conventions fixed: primitives in distinguishing form, record game in bit-guessing form; Lemma 23 and every hop use them, with no hidden factor of 2.
- Derived keys are *instances* (one per distinct context), not distinct byte strings. New Lemma 24: eps_ae^iid <= eps_ae^dist + K(K-1)/2^257. Theorem 25 uses eps_ae^iid; Corollary 26 charges the key-coincidence term explicitly. (v4.0.2 asserted without checking that the cited multi-key game covered coinciding keys; its definition could not be inspected: the ePrint PDF is behind bot verification.)
- Table 7: counting conventions per interface case (empty Open, cached malicious contexts, abandoned creation, failed chunks).
- Proposition 27 (was 26): exact reused-bank count with partial publication and unequal thresholds, 1 + sum_m sum_j C(n,j)(m^j - (m-1)^j); scope limited to the reused-bank delivery map.
- Reference data layer (`datalayer.py`) with pyca/cryptography ChaCha20-Poly1305 and stdlib HMAC; 9 tests; measurements (`bench_datalayer.py`). Profile clarification: the chunk AAD must carry a final-chunk flag, otherwise truncation goes undetected (demonstrated by a test).
- Process-isolation assumptions for worker termination stated.
- Bibliography: DOI for Degabriele et al.; Hoang-Reyhanitabar-Rogaway-Vizar (CRYPTO 2015) added.
- Tests: 71 (5 + 25 + 14 + 18 + 9).

## 4.0.2 (5 November 2026)
- Theorem 24: object-level requests separated from chunk-level primitive calls. q = honest contexts (including abandoned creations), r = non-honest Open requests, C = chunk encryptions, D = non-honest chunk decryptions, Q_PRF <= q+r, K <= q+r. Bound: L[eps_mu(N,M) + eps_prf(q+r) + q(q-1)/2^257 + eps_ae(q+r,C,D)].
- Definitions 21-22: Store/Open interface stated (one context per Open, memoized key, one AEAD call per chunk, including failures); AE game allows decryption-only keys.
- Seed-decoupling hop: explicit invariant (I), conditional on Lambda = Gamma.
- Guessing step: exactness of Adv_0 = L Adv_1 for any covering set, including unreachable patterns.
- New Proposition 26: closed form sum_{j<t} C(n,j) G^j for reused per-holder banks (exact when all generations are published; covering under a common threshold); renewed banks reach all of P.
- Observation 2: precise reason weak fairness suffices for WorkerReturns (only Crash disables it, and Crash also removes the obstacle).
- Artifact: v402_checks.py (data-layer accounting model; pattern closed form), 2 tests (61 total), reproduce_all.py, ENVIRONMENT.md.

## 4.0.1
PRF/AE key counts, guessing-space definition, Lemma 23 table, exponent-view scope, fairness map, bibliography locations, HPKE attribution.

## 4.0.0
Restricted-adaptive composition, erasure complexity map, conditional leakage, lifecycle liveness, renewal model, kernel conformance testing.
