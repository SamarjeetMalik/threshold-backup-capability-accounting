# v4.0.1 → v4.0.2: final technical audit and finalization

Capability Exposure Accounting for Threshold-Based Encrypted Backup Recovery
Samarjeet Malik (Ashoka University), Shaurya Pratap Singh (Indian Institute of Science)
5 November 2026.

**Baseline.** v4.0.1 was verified against `Capability_Exposure_Accounting_v4.0.1_SHA256SUMS.txt` and its internal manifest before any change, and is preserved unchanged: the v4.0.1 zips, `pdf/Capability_Exposure_Accounting_v4.0.1.pdf` and `manuscript/main_v4.0.1.tex`.

**Not done.** Nothing was pushed, released or submitted.

## Stage 1: Issue table

| # | Sev. | Location (v4.0.1) | Finding | Fix | Validation |
|---|---|---|---|---|---|
| 1 | **P0** | Thm 24, Def 21–22, Cor 25 | `d` stood for both object-level `Open` requests and AEAD decryption calls. One `Open` evaluates HMAC at most once (memoized per context), but makes one AEAD call per supplied chunk, so the PRF count was too high and the AEAD decryption count could be too low | Interface stated in Def 21: one context per `Open`, memoized key, one AEAD call per chunk including failures. New counts: q honest contexts (including abandoned creations), r non-honest `Open` requests, C chunk encryptions, D non-honest chunk decryptions. Q_PRF ≤ q+r, K ≤ q+r. Bound L·[ε_mu(N,M) + ε_prf(q+r) + q(q−1)/2²⁵⁷ + ε_ae(q+r,C,D)] | Proof re-derived; `v402_checks.py` accounting model (300 workloads): D > r in 234 |
| 2 | P0 | Thm 24 proof, seed decoupling | The key fact was used without being stated | Invariant (I): on fresh runs with Λ = Γ, every real target capsule is at a touched index. Proved; stated as conditional on Λ = Γ | Proof |
| 3 | P0 | Thm 24 proof, guessing step | Exactness with unreachable patterns was not addressed | Adv₀ = L·Adv₁ is exact for any covering 𝒫; unreachable patterns only enlarge L | Proof |
| 4 | P1 | Def 22 | AE definition did not allow decryption-only keys or say what D counts | Keys may be decryption-only; D counts chunk-level calls including failures; PRF queries are adaptive and repeat-consistent | — |
| 5 | P1 | Identifier term | Scope unstated | Only honest identifiers are sampled. Adversarial identifiers play no part. Key coincidences across distinct contexts are absorbed by the independent-key AE game. Header differences make the bound conservative | — |
| 6 | P1 (new result) | Pattern space | No exact count for any delivery structure | **Prop 26**: with reused per-holder banks, the reachable set has closed-form size Σ_{j<t_min} C(n,j)·Gʲ: exact when all G generations are published, covering under a common threshold. With renewed banks the reachable set is all of 𝒫. Theorem 24 holds with this count. Example: 3,991 vs 970,299 for three 5-of-7 generations | 200 exhaustive enumerations (exact match), 100 partial-publication, 100 renewed |
| 7 | P1, caught in self-review | Prop 26 first draft | Claimed coverage without a publication hypothesis. With unequal thresholds and partial publication, freshness uses the minimum over the published prefix only | Two alternative hypotheses stated, with an explanation | Partial-publication test |
| 8 | P1 | Obs 2 | "WorkerReturns stays enabled" was imprecise: `Crash` disables it | Only `Crash` disables it, and `Crash` also removes the obstacle, so weak fairness suffices | TLC fairness map re-run |
| 9 | P2 | Bibliography | Backendal et al. lacked volume and pages; Janneck–Riepel lacked a primary record | LNCS 16542, 34–65, Springer Cham (verified on the EUROCRYPT 2026 artifact page); ePrint 2026/434 for Janneck–Riepel. Its volume was not verified, so none was added | Web check |
| 10 | P2 | Costs §11 | Request versus primitive cost not stated | One HMAC plus ℓ AEAD calls per ℓ-chunk object | — |
| 11 | P2 | Artifact | No single-command runner or environment specification | `reproduce_all.py`, `ENVIRONMENT.md`, `CHANGELOG.md` | Executed |

The kernel, the data layer and the TLA+ files are unchanged in v4.0.2. **The artifact contains no implementation of the data layer.** The interface is the profile's, and `v402_checks.py` is a model of its counting, not of an implementation.

## Stage 3: Proof-status table (independent re-check)

| Result | Status |
|---|---|
| Thm 1 Closure | Correct as written |
| Thm 3 Leakage subspace | Correct as written |
| Cor 4 Marginal/conditional leakage | Correct as written (1,500 exact instances) |
| Cor 5 Adaptive translation | Correct after v4.0.1 clarifications |
| Thm 6 Witness hitting | Correct as written (origin tagging assumed) |
| Prop 8 Read-once | Correct as written |
| Prop 9 Weighted thresholds | Correct as written |
| Prop 10 APX-hardness | Correct as written |
| Prop 11 Few generations | Correct as written |
| Lemma 12 Blockwise | Correct as written |
| Thm 14 Joint generations | Correct; scope (information-theoretic, group and exponent views equivalent) stated in v4.0.1 |
| Thm 15 Temporal accounting | Correct as written (random-history evidence is not proof) |
| Cor 16 Healing | Correct as written |
| Props 17–19 Quorums | Correct as written |
| Prop 20 Deadline | Correct as written; assumptions explicit |
| Lemma 23 Multi-user | Correct; NM is a generic loss |
| Thm 24 Composition | **Required a proof correction** (counts) plus an explicit invariant; corrected |
| Cor 25 Concrete loss | Corrected with Thm 24 |
| Prop 26 Reachable patterns | New; proved with an explicit hypothesis; tested |
| Lemma 27 Slots | Correct as written |

## Stage 5: Executed (`artifact/reproduced/full_v402_run.log`, one command)

- `reproduce_all.py` runs all v2, v3 and v4 checkers, which reproduce their saved outputs exactly. The v4.0.1 checker outputs are unchanged.
- Tests: 61 executed and passing (5 + 25 + 14 + 17).
- TLC: 8 v2, 13 v3 and 15 v4 configurations, all in compare mode.
- LaTeX: halt-on-error build, 0 overfull boxes, 0 undefined references, 0 placeholders, 37 pages.
- Isolated Overleaf-zip build: see below.

## Stage 6: Reviews

**Cryptography: weak accept, 71.**
- Theorem 24 now has unambiguous units: contexts, keys, chunk encryptions, chunk decryptions.
- Invariant (I) makes the decoupling step checkable.
- Proposition 26 is useful but also exposes a perverse artefact, which the paper states: the proof's loss is larger for renewed (safer) banks.
- Remaining weaknesses: the generic NM factor, an assumed HPKE Base IND-CCA, and an L that is exponential in the number of generations under renewal.

**Theory: weak accept, 65.** All results check. Proposition 26 is a modest but clean addition with an exact count. Originality is still in application.

**Systems / formal methods: accept / weak accept, 74.** The fairness wording is now exact. The single-command reproduction worked. There is still no refinement proof and no data-layer implementation.

**Meta-review: weak accept.** No critical findings remain open.

## Final assessment

| Dimension | v4.0.1 | v4.0.2 |
|---|---|---|
| Mathematical rigor | 88 | 89 |
| Cryptographic correctness | 78 | 82 |
| Adaptive-security analysis | 56 | 59 |
| Complexity-theoretic contribution | 61 | 61 |
| Originality | 50 | 51 |
| Formal verification | 82 | 82 |
| Systems-security contribution | 61 | 61 |
| Experimental reproducibility | 79 | 83 |
| Scholarly positioning | 80 | 81 |
| Presentation | 67 | 67 |
| **Overall** | **71** | **72** |

**Unresolved:**
- full adaptivity;
- a tight multi-user HPKE bound;
- a refinement proof;
- TLAPS;
- a data-layer implementation;
- multi-guardian committees, reconfiguration and partitions.

**Strongest reason for rejection.** The cryptographic core is a guessing argument whose loss is exponential in the number of renewed generations, and the remaining mathematics is elementary.
