# Version 4.0.0 major-revision report

Capability Exposure Accounting for Threshold-Based Encrypted Backup Recovery
Samarjeet Malik (Ashoka University), Shaurya Pratap Singh (Indian Institute of Science)
Prepared 5 November 2026. Baseline: the local v3.0.0 bundle (`Capability_Exposure_Accounting_Artifact_v3.zip`, verified against its SHA-256 manifest before work began and left unchanged). The public GitHub repository still contains v2.0.0 only. Nothing was pushed, tagged, submitted or published.

---

## Pass 1: Red-team of the mathematics

| Result (v3 numbering; v4 numbers in the action column) | Audit outcome | v4 action |
|---|---|---|
| Thm 3, leakage subspace | Correct. Re-proved; all five parts re-checked numerically | Added Cor 4: exact marginal I(S_T;Y) = dim U_T · log p, conditional I(S_T;Y\|S_K) = dim π_T(U) · log p, chain rule (1,500 exact instances) |
| Thm 3, mask hypothesis | Correct as stated (uniform R), but the necessity of uniformity was never shown | Counterexample: R uniform on {0,1} in F_3 passes the rank test and leaks. Masks uniform on a subspace reduce to B ↦ BC (1,000 instances) |
| Cor 4, adaptive transcripts | Correct. Exact conditions now stated | Needs a transcript-measurable acceptance predicate and stopping rule, and metadata that is a function of the transcript. Counterexample: accept iff R = 0 reveals S. Variable-length and seed-dependent scheduling through answers are fine |
| Thm 5, witness hitting | Correct under origin tagging. ∞ and 0 costs handled. Public facts are immutable witnesses. Several copies of one key are distinct origin atoms | No change |
| Prop 7, read-once | **Inconsistent**: titled linear-time but sorts at threshold gates (O(m log m) per gate) | O(N) with linear-time selection (BFPRT 1973), O(N log N) with sorting; checked on 2,500 formulas |
| (new) weighted thresholds | — | NP-hard for one gate (subset sum); O(mW) pseudo-polynomial DP; 2,000 instances |
| Prop 8, VC reduction | Correct; approximation ratio preserved (identical objective) | Strengthened: APX-hard with each root reused in ≤ 3 generations (Alimonti–Kann, cubic VC) |
| (new) bounded generations | — | Prop: (n+1)^{2^G}-time algorithm via membership types and an exchange argument; 400 instances vs brute force. A common holder set is greedy |
| Thm 11, generations | Correct | No change |
| Thm 12, temporal | Correct; only hand-built scenarios had been checked | 3,000 random histories: 5,388 independent targets, 0 disagreements; 639 correlated targets, 5 unsafe disagreements |
| Prop 14 / 15 | Correct | Added Prop 19: domain-correlated corruption (charge each committee its F largest domains); 3,000 instances vs enumeration |
| Prop 16, deadline | Correct | Concurrent checkpoint and fetch removes one D (assumption stated) |
| **Thm 17, selective composition** | **Two accounting errors.** (1) Q ε_ae with Q counted in objects, although objects have up to 2³²−1 chunks under one key. (2) The object-ID collision term was missing, and without it keys need not be distinct. M also over-counted non-target capsules (loose, not wrong) | Replaced by Thm 24 (restricted-adaptive). The selective case is its L = 1 specialization with corrected terms |
| Kernel (v3) | Four conformance divergences, see Pass 4 | Fixed |
| Bibliography | Karp entry incomplete; **Dinur–Safra title wrong** ("minimum" is not in the Annals title) | Karp: editors, series, address, DOI. Dinur–Safra: title and DOI |

## Pass 2: Adaptive cryptographic security (primary objective)

**Game.** Definition 21 gives an adaptive game with separate interfaces for: slot exposure (device compromise and bank copying, including future slots), coordinate disclosure, HPKE decryption, seed routes (recoverer and archive), data store and open, identity corruption, and one record challenge. Freshness is the Theorem 12 condition.

**Theorem 24 (established).** Adv ≤ L · (ε_mu(N,M) + ε_prf(q) + q(q−1)/2²⁵⁷ + ε_ae(q,c,d)), where L = Π_g Σ_{j<t_g} C(n_g, j) counts the admissible late-exposure patterns of the target generations.
- Proof: six explicit hops (guess, capsules, seed decoupling, PRF, identifiers, AEAD), each naming its games, reduction, query counts and stopping rule.
- Lemma 23: ε_mu(N,M) ≤ N·M·ε_cca, by a guessing hybrid.
- Forward-ordered exposure gives L = 1.
- Concrete values: L = 16 for one 3-of-5 generation; 256 for two such generations; about 9.7·10⁵ for three 5-of-7 generations.

**Two errors caught in my own draft.** The first draft had two broken hops:
- The PRF reduction would have had to answer `SeedRoute` on the target without knowing the seed.
- The AEAD reduction would have had to answer `Open` on the challenge.

The fix stops the game with a fair bit as soon as a run becomes non-fresh. Non-freshness is monotone, so this leaves the output distribution unchanged.

**Techniques assessed**

| Technique | Verdict |
|---|---|
| Guessing / complexity leveraging | Used, confined to late-exposure patterns of the target only, which gives L |
| Multi-user IND-CCA with corruptions | Used as the capsule assumption; bounded generically by N·M·ε_cca |
| Generalized selective decryption / pebbling (Panjwani 2007; Jafargholi et al. 2017) | Could shrink L for structured patterns. Not attempted; cited |
| Noncommitting or RSO-secure encryption (CFGN 1996; Hazay–Patra–Warinschi 2015) | Would remove L but requires replacing HPKE |
| Selective opening (Bellare–Hofheinz–Yilek 2009) | Full adaptivity here is exactly receiver selective opening for share-distributed messages; IND-CCA is not known to imply it |
| Programmable-RO DEM via HPKE exporter | Plausible smaller change, **not proved**; ChaCha20 itself is not programmable |
| Lossy, dual-mode, puncturable or key-evolving encryption | Not pursued. Each changes the primitive, and none was needed for the restricted theorem |

**Not established:** full adaptivity, and any tight multi-user bound for HPKE.

## Pass 3: Temporal and refresh terminology

Theorem 12 is now validated on arbitrary random finite histories rather than only hand-built scenarios. Bank migration and archive rotation are classified in text (both follow from Corollary 16 items 2–3). "Proactive" now refers only to the cited refresh protocols, and the paper says it establishes no refresh protocol and no corruption-window guarantee.

## Pass 4: Formal methods

- **Fix audit.** v3 fixed only the receipt guard. v4 adds `WorkerAbandons`.
- **Liveness.** `ExpiryCompletes` holds under strong fairness of `Erase`, `SignReceipt`, `Restart` and `WorkerReturns`. Without worker fairness, TLC finds a lasso in which a hung worker blocks erasure forever. Erasure progress therefore requires that workers can be terminated; Python threads cannot be.
- **Mobile adversary.** `MultiGenerationRenewal.tla`: renewal with cleanup is safe in all 775 states; bank reuse and renewal without deletion each fail within three steps.
- **Refinement.** A Python transcription of `RecoveryLifecycleV4` reproduces TLC's state counts exactly (5,584 and 27,904). An abstraction function, with one history variable, maps kernel states to abstract states. Over 2,000 seeded schedules:
  - v3 kernel: 215 divergent schedules, in four classes (authorize on a cancelled request, duplicate completion, stale abandon, out-of-order commit). None released data after expiry.
  - v4 kernel: no divergence in 80,000 calls. Each class has a regression test run against both kernels.

  This is bounded testing, **not a refinement proof**.
- **Not done:**
  - separate committees, reconfiguration, partitions and certificate replay in the multi-guardian model;
  - eventual-synchrony liveness;
  - TLAPS.

## Pass 5: Quorum

- Domain-correlated corruption added (Prop 19).
- An ILP for minimum robust membership was not written: a formulation without an experiment adds little.

## Pass 6: Literature

All new references were checked against primary or indexing records during this revision:
- Panjwani (TCC 2007, LNCS 4392:21–40)
- Jafargholi et al. (CRYPTO 2017, LNCS 10401:133–163)
- Alwen et al. (EUROCRYPT 2021, LNCS 12696:87–116)
- Hazay–Patra–Warinschi (ASIACRYPT 2015, LNCS 9452:443–469)
- Bellare–Hofheinz–Yilek (EUROCRYPT 2009, LNCS 5479:1–35)
- Alimonti–Kann (TCS 237:123–134, 2000)
- Degabriele et al. (CCS 2021, 1981–2003)
- Blum et al. (JCSS 7(4):448–461, 1973)
- Karp 1972 (DOI 10.1007/978-1-4684-2001-2_9)
- Dinur–Safra (DOI 10.4007/annals.2005.162.439)

Effect on novelty:
- The guessing idea is standard, and the paper says so.
- What is new is applying it to share-delivery exposure, with a loss counted in late-exposure patterns rather than slots.
- The CKS, GKP and Janneck–Riepel comparisons are still carried over and were not re-audited.

## Pass 7: Experiments actually executed (all reproduced in `artifact/reproduced/full_v4_run.log`)

Seeded families:
- conditional leakage (1,500)
- subspace masks (1,000)
- selection vs sorting (2,500)
- weighted thresholds (2,000)
- few-generation algorithm (400)
- random histories (3,000)
- domain corruption (3,000)
- refinement conformance (2 × 2,000 schedules)

Exhaustive:
- transcription state counts
- TLC runs: v4 lifecycle (4 safety, 2 liveness) and renewal (3)

Arithmetic only: the guessing-loss table. Tests: 14 new; all 58 pass.

## Pass 9: Reviews

### Reviewer 1 (cryptography): weak accept
- **Summary:** Theorem 24 is a correct, carefully staged restricted-adaptive composition. The corrections to v3 Theorem 17 are real.
- **Strengths:** explicit hops; an honest statement of what full adaptivity needs; generic multi-user lemma.
- **Major weaknesses:** L is exponential in the number of target generations, so long-lived seeds with many refreshes get vacuous bounds unless exposure is forward-ordered. The multi-user term N·M·ε_cca is loose.
- **Minor weaknesses:** HPKE IND-CCA is assumed, not derived from Gap-DH; ε_ae is left symbolic.
- **Questions:** Can pebbling (Jafargholi et al.) cut L to polynomial for threshold structures? Does an exporter-based DEM give RSO in the ROM?
- **Required revisions:** none blocking.
- **Score:** 68.

### Reviewer 2 (theory and algorithms): weak accept
- **Summary:** The erasure complexity map is now coherent: read-once O(N), weighted NP-hard / pseudo-polynomial, bounded-G polynomial, cubic reuse APX-hard. The leakage corollary is clean.
- **Strengths:** every algorithm is checked against brute force; the hypotheses are shown necessary by counterexample.
- **Major weakness:** all results are elementary, so novelty is in the application.
- **Minor weaknesses:** the n^{O(2^G)} algorithm is impractical beyond G ≈ 3; no FPT result in solution size is stated, although a standard one exists.
- **Required revisions:** none blocking.
- **Score:** 62.

### Reviewer 3 (systems security and formal methods): accept / weak accept
- **Summary:** The conformance harness is the most useful addition. It found four real divergences, and the transcription is validated by exact state counts. The liveness finding (hung workers block erasure) is operationally important.
- **Strengths:** negative controls for every model; fairness stated explicitly.
- **Major weaknesses:** no refinement proof; the multi-guardian model still lacks committees, reconfiguration and partitions.
- **Minor weakness:** schedules are 40 calls over 2 paths and 2 requests.
- **Required revisions:** none blocking.
- **Score:** 72.

### Meta-review
The reviewers agree that v4 makes real progress on the stated v3 weakness: there is now a restricted-adaptive theorem with exact accounting. Reviewer 3 values the engineering findings most, and Reviewer 2 discounts for elementary mathematics; both readings are fair. **Recommendation: weak accept** at a security venue for analysis or verification papers, or a journal such as ACM TOPS or JCS. It is **not** competitive at IACR flagship venues without removing L.

## Final assessment

| Dimension | v3.0.0 | v4.0.0 | Why |
|---|---|---|---|
| Mathematical rigor | 80 | 84 | Runtime inconsistency fixed; hypotheses shown necessary |
| Novelty | 48 | 53 | Restricted-adaptive accounting and the erasure complexity map; the techniques are standard |
| Theoretical contribution | 58 | 64 | Theorem 24, conditional leakage, few-generation algorithm |
| Cryptographic security | 64 | 72 | Composition corrected and extended to adaptive exposure |
| Adaptive security | 20 | 55 | Restricted only; L can be large |
| Formal verification | 72 | 79 | Liveness, mobile-adversary renewal model, validated transcription |
| Systems contribution | 52 | 60 | Four kernel defects fixed; worker-termination requirement |
| Experimental quality | 74 | 78 | Random histories and conformance testing target new failure modes |
| Literature positioning | 72 | 77 | Selective-opening and adaptive-security literature added |
| Writing | 68 | 66 | Clearer status labels, but 33 pages and dense |
| **Overall** | **64** | **69** | |

- **What improved:** adaptive security; Theorem 17 accounting; the complexity map; refinement evidence; liveness.
- **What remains weak:** L; no refinement proof; elementary core; length.
- **New results:** Corollary 4 (conditional leakage), Propositions 9 and 11 (weighted thresholds, few generations), Proposition 10 strengthened (cubic reuse), Proposition 19 (domain-correlated corruption), Lemma 23, Theorem 24, Corollary 25, Observations 2 and 3.
- **Narrowed:** the read-once runtime claim, and the use of "proactive".
- **Unproved:** full adaptivity, a tight multi-user HPKE bound, TLAPS, refinement.
- **Strongest rejection argument:** the cryptographic core is a guessing argument with an exponential loss, and everything else is elementary.
- **Best venue category:** a systems-security or formal-methods-in-security venue or journal (e.g. ACM TOPS, JCS, CSF, ESORICS), framed as an analysis-and-verification paper.
