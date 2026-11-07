# v4.0.2 → v4.0.3: revision report

Capability Exposure Accounting for Threshold-Based Encrypted Backup Recovery
Samarjeet Malik (Ashoka University), Shaurya Pratap Singh (Indian Institute of Science)
6 November 2026.

- **Baseline:** v4.0.2 was verified against its checksums before work began and is preserved unchanged (`..._v4.0.2.zip`, `pdf/..._v4.0.2.pdf`, `manuscript/main_v4.0.2.tex`).
- **Not done:** nothing was pushed, released or submitted.
- **Numbering:** the new Lemma 24 shifts the later results by one. The composition theorem is now **Theorem 25**, the concrete-loss corollary **Corollary 26**, and the reused-bank count **Proposition 27**.

## Phase 1: Issue matrix

| # | Sev. | Location (v4.0.2) | Finding | Fix | Validation |
|---|---|---|---|---|---|
| 1 | **P0** | Thm 24, hop G3→G4 | v4.0.2 said coinciding derived keys were "already accounted for" by the cited multi-key AE game, without checking that game's key-sampling convention. Every object's chunk counter starts at 0, so two distinct contexts with equal key bytes reuse the (key, nonce) pair. | Keys are now *instances*, one per distinct context. ε_ae^iid is defined with independent sampling (with replacement), nonce-respecting per instance index. New **Lemma 24**: ε_ae^iid ≤ ε_ae^dist + K(K−1)/2²⁵⁷, by conditioning-based coupling. Theorem 25 uses ε_ae^iid; Corollary 26 charges the coincidence term explicitly. | Proof. Test: a forced key coincidence is caught by the prototype's key-byte guard. |
| 2 | **P0** | Def 22, Lemma 23, Thm 24 | Advantage normalization was never stated, so a hidden factor of 2 was possible. | Primitives use distinguishing advantage; the record game uses bit-guessing. Each hop bounds \|Pr[Gᵢ⇒1] − Pr[Gᵢ₊₁⇒1]\| by its reduction's distinguishing advantage. Lemma 23's B_j has exactly (1/N)·gap. A primitive bound given in bit-guessing form must be doubled. | Proof; normalization paragraph in Thm 25 |
| 3 | **P0** | Def 21 / Thm 24 counts | Edge cases undefined (empty Open, cached malicious context, abandoned creation, failed chunk) | **Table 7** gives a counting convention for each case | Prototype test `test_counts_match_theorem_quantities` |
| 4 | P1, new result | Prop 26 | Count proved only for all-published or common-threshold runs | **Proposition 27**: an exact count with partial publication and unequal thresholds, 1 + Σ_m Σ_{j<τ_m} C(n,j)(mʲ − (m−1)ʲ), which telescopes to the v4.0.2 form. Scope stated: the reused-bank delivery map only; no closed form for general maps. | 300 exhaustive cases (113 with unequal thresholds); telescoping checked for all n ≤ 7, t ≤ n, G ≤ 4 |
| 5 | P1, new finding | Profile Table 5 | The chunk AAD was unspecified. Per-chunk AEAD with an index nonce does **not** detect truncation of final chunks. | The profile now binds a final-chunk flag (STREAM, Hoang et al. CRYPTO 2015). This is an integrity issue and does not affect Theorem 25. | Test: without the flag, a 4-chunk object truncated to 2 chunks opens successfully |
| 6 | P1 | Data layer | No implementation existed | `datalayer.py`: reference only, using maintained primitives (pyca/cryptography 50.0.2, OpenSSL 4.0.3; stdlib HMAC); 9 tests; measurements | Executed |
| 7 | P1 | Liveness | Assumptions behind "process isolation" were missing | Stated: separate process holding no other secrets; unconditional kill observed before the receipt; swap disabled or encrypted; no physical-erasure claim | — |
| 8 | P2 | Abstract | The smaller reused-bank loss could be read as general | The abstract now ties it to the reused-bank delivery map | — |
| 9 | P2 | Bibliography | Degabriele et al. had no DOI | DOI 10.1145/3460120.3484814 from the ePrint record; Hoang et al. added (DBLP-verified) | Web check |

**Unverifiable item.** I could not read the definitions in Degabriele et al. Scripted fetches return HTTP 403, and the browser lands on a bot-verification page, which I did not attempt to pass. Lemma 24 makes the theorem correct under either key-sampling convention, so the inspection is no longer needed for correctness. Someone should still check which convention the paper uses before plugging in its numeric bound.

**Options for key collisions.**

| Option | What it does | Verdict |
|---|---|---|
| A. Account (chosen) | Keep the design; charge K(K−1)/2²⁵⁷ | Below 2⁻²⁰¹ for K ≤ 2²⁸ |
| B. Context-bound nonce prefix | Leaves only 32 bits of prefix with a 64-bit counter in a 96-bit nonce, so it lowers but does not remove cross-object coincidence | Would need XChaCha20 (192-bit nonce), a primitive change |
| C. Extra KDF separation | Does not change the collision probability of 256-bit random-function outputs | No benefit |

The prototype also re-samples identifiers already in its local index (defensive). The proof still charges the identifier term.

## Phase 5: Proof status

- Every result audited in v4.0.2 remains **correct as written**.
- **Thm 25** (was 24): corrected (key-instance semantics, normalization) and re-proved hop by hop.
- **Cor 26**: corrected.
- **Lemma 24**: new, proved.
- **Prop 27**: generalized, proved and tested.
- **Lemma 23**: correct; normalization now explicit.

## Phase 6: Executed (`artifact/reproduced/full_v403_run.log`; fresh-unpack log alongside)

- **Single command.** `.venv/bin/python reproduce_all.py` runs:
  - all v2–v4 checkers, which reproduce their saved outputs exactly (v4.0.2 outputs unchanged);
  - **71 tests**: 5 + 25 + 14 + 18 + 9 (data layer);
  - TLC: 8 v2, 13 v3 and 15 v4 configurations, all matching.
- **Measurements** (`bench_datalayer.json`; one machine: Apple arm64, macOS 26.5.1; not compared across runs):
  - HMAC derivation: 0.9 µs.
  - ChaCha20-Poly1305: about 1.7–2.2 GiB/s.
  - 64 MiB object: store 36 ms, recover 31 ms.
  - Overhead: exactly 16 B per chunk, as calculated.
  - Peak heap: about 2× the object size (the reference does not stream).
- **Build:** 40 pages, 0 overfull boxes, 0 undefined references, 0 placeholders.

## Phase 8: Reviews

- **Cryptography: weak accept, 74.** The key-instance correction is right, and the coupling lemma is the clean way to stay agnostic about the cited AE game. The normalization is now explicit. Remaining weaknesses: an L that is exponential under renewal; the generic N·M factor; HPKE Base IND-CCA is assumed.
- **Theory: weak accept, 66.** The exact count with partial publication is a tidy, verified generalization that is honestly scoped. Novelty is still in the application.
- **Systems / formal methods: weak accept, 75.** The prototype adds real evidence and found an integrity gap in the profile. Measurements are clearly scoped. Still missing: a refinement proof, distributed liveness, and a streaming implementation.
- **Meta-review: weak accept.** No critical findings remain open.

## Final assessment

| Dimension | v4.0.2 | v4.0.3 |
|---|---|---|
| Mathematical rigor | 89 | 90 |
| Originality | 51 | 52 |
| Theoretical contribution | 62 | 63 |
| Cryptographic correctness | 82 | 86 |
| Adaptive security | 59 | 60 |
| Systems contribution | 61 | 66 |
| Formal verification | 82 | 82 |
| Experimental quality | 79 | 82 |
| Reproducibility | 83 | 85 |
| Scholarly presentation | 67 | 67 |
| **Overall** | **72** | **74** |

**Strongest reason for rejection.** The adaptive guarantee pays a guessing loss that is exponential in the number of renewed generations, and the remaining mathematics is elementary. The contribution is careful accounting and verification, not new cryptography.
