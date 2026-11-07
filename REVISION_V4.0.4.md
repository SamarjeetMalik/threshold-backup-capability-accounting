# v4.0.3 → v4.0.4: revision and visual redesign report

Capability Exposure Accounting for Threshold-Based Encrypted Backup Recovery
Samarjeet Malik (Ashoka University), Shaurya Pratap Singh (Indian Institute of Science)
6 November 2026.

- **Baseline:** v4.0.3 was verified against its checksums and is preserved unchanged (`..._v4.0.3.zip`, `pdf/..._v4.0.3.pdf`, `manuscript/main_v4.0.3.tex`).
- **Not done:** nothing was pushed, released or submitted.
- **Style reference:** `2026-417.pdf` was used for visual cues only (booktabs tables, bold run-in headings, coloured citations, restrained accents). No text, figure or content was taken from it.

## 1. Cryptographic audit

| # | Item | Finding | Action |
|---|---|---|---|
| 1 | **Lemma 24 proof** | **Defect.** The v4.0.3 proof bounded the real-world and ideal-world output probabilities *separately* by δ. Done carefully, that argument gives \|ε_iid − ε_dist\| ≤ 2δ, not δ. The stated lemma was correct; its proof was not. | Rewritten as a common-mixture argument. The ideal world (fresh strings and ⊥ per instance index) does not depend on the keys, so p_ideal splits with the same weights, and the signed gap is (1−δ)·gap_dist + δ·gap_col. Hence \|gap_iid\| ≤ (1−δ)\|gap_dist\| + δ ≤ ε_dist + δ, with δ = 1 − Π(1 − i/2²⁵⁶) ≤ K(K−1)/2²⁵⁷. |
| 2 | Theorem 25 | Re-derived. L multiplies every term. Hop normalization (distinguishing advantage for primitives, bit-guessing for the record game) is consistent; Lemma 23's B_j has exactly (1/N)·gap; no factor of 2 is missing or added. Invariant (I) holds only under Λ = Γ, as stated. | No change to the statement |
| 3 | Counts q, r, K, C, D | Re-checked against the implementation (Table 7 and the counting test). Empty Opens are now rejected *before* derivation, and so are malformed or foreign records. | Implementation tightened; theorem unchanged |
| 4 | Collision terms | The identifier event (equal honest contexts) and the key-instance event (distinct contexts, equal output) are distinct and both charged. | Warning box added in the paper |
| 5 | Final-chunk integrity | Decoder checked against the source: the flag is computed from position, so missing, duplicated or early markers, appended, duplicated or reordered chunks, and cross-object chunks are rejected, and no plaintext is released on partial failure. Classified as an integrity property, not a confidentiality theorem. | 11 regression tests |

## 2. Data-layer audit (source, not prose)

Two real gaps were found and fixed:

1. **Malformed or foreign records.** These raised generic exceptions, and a record for another domain, account or configuration still triggered an HMAC evaluation. Records are now validated (exact field set and types, a 32-byte identifier, non-empty chunks of at least tag length) and rejected before key derivation.
2. **No lock.** The key cache, nonce guard and identifier index were unlocked. They are now updated under an `RLock`.

No time-of-check/time-of-use issue, accidental nonce reuse, cache contamination or partial-plaintext release was found. New tests: `test_datalayer_v404.py` (11 tests), alongside the original 9.

## 3. Benchmarks (re-executed; `artifact/evidence_v404/bench_v404/`)

**Method.**
- Inputs are seeded: object data is SHAKE-256-expanded from the seed and is identical across ciphers.
- 5 warm-ups before each measurement.
- 40 repetitions per microbenchmark; 12 trials per object operation.
- Reported: median, quartiles, 5th and 95th percentiles. Raw samples are saved.
- Hardware and software: Apple M5, 24 GiB, macOS 26.5.1, Python 3.12.14, cryptography 50.0.2, OpenSSL 4.0.3.

**Results on this machine:**
- **HMAC:** 0.92 µs median.
- **ChaCha20-Poly1305:** about 2.0 GiB/s from 16 KiB chunks.
- **AES-256-GCM** (engineering comparison only): about 8.8 GiB/s.
- **Store/Open:** linear up to 256 MiB, about 140 ms.
- **Overhead:** exactly 16 B per chunk, matching the calculation.
- **Peak heap:** about 2× the object size.

These measurements enter no proof. XChaCha20 is not discussed, because no implementation or nonce analysis was done.

## 4. Figures and plots

All are vector graphics (TikZ/PGFPlots). Diagram fonts are set in absolute sizes so the figures render identically in both builds. The 15 figures:

| Fig. | Content | Source |
|---|---|---|
| 1 | Four-layer capability architecture with AND hyperedges | `figures/fig_architecture.tex` |
| 2 | Leakage subspace, with a leakage-without-reconstruction panel | `fig_leakage.tex` |
| 3 | Witness hitting: a possible case and an impossible case | `fig_witness.tex` |
| 4 | Reused versus renewed banks, with level function and patterns | `fig_reuse_timeline.tex` |
| 5 | Feasible thresholds, three scenarios (n = 13) | `fig_feasible.tex` + `data/feasible.dat` |
| 6 | Minimum holder-committee heatmap | `plot_minholders.tex` + `data/minholders_u*.dat` |
| 7 | Key-collision bound (log₂) | `plot_keycoll.tex` + `data/keycoll.dat` |
| 8 | Hybrid sequence G0…G5 with losses and the L multiplier | `fig_hybrids.tex` |
| 9 | Guessing-space growth: L vs L_reuse vs L = 1, equal and unequal thresholds | `plot_guess.tex` + `data/guess_*.dat` |
| 10 | Implemented data layer with the collision route | `fig_datalayer.tex` |
| 11 | Truncation experiment | `fig_truncation.tex` |
| 12–14 | Latency (median and IQR), throughput, object Store/Open and peak heap | `plot_latency/throughput/objects.tex` + `data/bench_*.dat` |
| 15 | Lifecycle state machine | `fig_lifecycle.tex` |

Every plotted value is regenerated by `artifact/make_plot_data.py`, from exact formulas or from the raw benchmark output. Figure 9 reproduces the paper's numbers: 970,299 against 3,991, and 256 against 51.

**Not done:** a figure for unequal-threshold partial publication beyond Fig. 9's right panel, and a standalone level-function diagram (Fig. 4 shows the level for the copied holder).

## 5. Presentation

- **Palette:** navy #17365D, cobalt #2563EB, burgundy #B42318, slate #667085, pale blue, pale red and light grey.
- **Boxes, used sparingly:**
  - three key-result boxes (Theorems 3, 14 and 25);
  - three warning boxes (key coincidence; reused banks are not safer; worker termination);
  - one implementation-finding box (truncation).
- **Tables:** navy headers and alternating rows on the comparison, counts, profile and TLC tables.
- **Links:** navy and cobalt.
- **Template:** the class, margins and section styles are untouched, with microtype added.
- **Two builds from one source:**
  - `main.tex` is the styled version;
  - `main_submission.tex` sets `\submissionmode`: boxes become bold run-in paragraphs, links turn black, table accents are dropped, and figures stay identical.
- **Content check:** a word-multiset comparison of the two PDFs differs only by two text-extraction artefacts (a line-break hyphen and a run-together word). The scientific content is identical.
- **Page count:** 45 pages for both builds (40 in v4.0.3), from the figures.
- **Inspection:** every figure page and the end matter were inspected visually. Fixes found by inspection: wrapping and overlap in Figures 1–3, 6–8 and 10–11, legend collisions in Figure 9, axis-label crowding in Figure 14, and a stale v4.0.2 sentence.
- **Bibliography:** ChaCha20/Poly1305/IETF casing protected; "van Renesse" fixed.

## 6. Executed (`artifact/reproduced/full_v404_run.log`; fresh-unpack log alongside)

- **82 tests** pass: 5 + 25 + 14 + 18 + 20.
- All v2–v4 checkers reproduce their saved outputs exactly.
- TLC: 8 v2, 13 v3 and 15 v4 configurations, all matching.
- Both LaTeX builds: halt-on-error, 0 overfull boxes, 0 undefined references, 0 placeholders.

## 7. Reviews

**Reviewer 1, cryptography: weak accept, 75.**
- The Lemma 24 fix matters: the old proof only gave 2δ. The mixture argument is correct because the ideal world is key-independent.
- Theorem 25's accounting is consistent and the counts match the implementation.
- Remaining weaknesses: L is exponential under renewal; the multi-user term is generic; HPKE Base IND-CCA is assumed.
- Minor: the key-collision plot is decorative, since the bound is negligible, but it is correctly labelled.

**Reviewer 2, mathematics and theory: weak accept, 66.**
- No mathematical result changed; all audited results stand.
- Figures 2, 3, 4 and 9 make Theorem 3, Theorem 6 and Proposition 27 easier to follow.
- Fig. 9 plots exact values.
- Novelty is unchanged and modest.

**Reviewer 3, systems and presentation: accept / weak accept, 78.**
- The decoder hardening and its tests are solid.
- The benchmark methodology is now acceptable (warm-ups, repetitions, IQR, seeded data, environment recorded) and clearly limited to one machine.
- The figures are clean and the two builds match.
- The paper is long (45 pages); a venue may require moving figures 6, 7, 12 and 13 to an appendix.

**Meta-review: weak accept.** No critical objection is open; the Lemma 24 proof defect is resolved.

## 8. Final assessment

| Dimension | v4.0.3 | v4.0.4 |
|---|---|---|
| Mathematical correctness | 90 | 91 |
| Theoretical novelty | 52 | 52 |
| Cryptographic rigor | 86 | 88 |
| Adaptive-security contribution | 60 | 60 |
| Complexity-theoretic contribution | 61 | 61 |
| Systems-security contribution | 66 | 69 |
| Formal verification | 82 | 82 |
| Experimental validation | 82 | 85 |
| Figure and plot quality | 45 | 80 |
| Typography and presentation | 67 | 79 |
| Reproducibility | 85 | 87 |
| **Overall publication readiness** | **74** | **77** |

**What genuinely improved:**
- Lemma 24 now has a correct proof.
- The data-layer decoder is hardened and validated.
- The benchmark methodology meets the requested standard.
- The paper has a full set of reproducible, technically accurate figures.
- There are two consistent builds.

**What remains unresolved:**
- full adaptivity;
- a tight multi-user HPKE bound;
- a refinement proof;
- distributed liveness;
- a streaming data layer;
- measurements on more than one machine.

**Strongest reason for rejection (unchanged).** The adaptive guarantee pays a guessing loss that is exponential in the number of renewed generations, and the remaining mathematics is elementary. Better presentation does not change that.
