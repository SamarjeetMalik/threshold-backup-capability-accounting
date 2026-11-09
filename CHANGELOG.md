# Changelog

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
