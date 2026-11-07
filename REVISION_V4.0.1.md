# v4.0.0 → v4.0.1: correction and finalization report

Capability Exposure Accounting for Threshold-Based Encrypted Backup Recovery
Samarjeet Malik (Ashoka University), Shaurya Pratap Singh (Indian Institute of Science)
5 November 2026.

**Baseline.** The local v4.0.0 bundle was verified against `Capability_Exposure_Accounting_v4_SHA256SUMS.txt` and its internal manifest before any change. It is preserved unchanged: the v4 zips, `pdf/Capability_Exposure_Accounting_v4.0.0.pdf`, `manuscript/main_v4.0.0.tex` and `artifact/baseline_v4/RecoveryLifecycleV4.tla`.

**Not done.** Nothing was pushed, tagged, released or submitted. The public repository still holds v2.0.0 only.

**Versioning.** v4.0.1 is a correction release. It adds no new theorem and no architectural change; the new items are a fairness map, a coverage check and a reduction table.

## Phase A: Diagnostic audit

| # | Severity | Location (v4.0.0) | Finding | Treatment | Code? | Validation |
|---|---|---|---|---|---|---|
| 1 | Checked; **not a defect** | Thm 24 bound | The brief reports L multiplying only ε_mu. The v4.0.0 source (`L\left(…\right)`, main.tex line 502) and the compiled PDF both apply L to every term. `pdftotext` drops the large parentheses, which makes the extracted text read as L·ε_mu + …. The proof (Adv_0 = L·Adv_1) and Cor 25 were already consistent with it | Bound rewritten with explicit brackets `L·[…]` (eq. 7); expanded single-user form added to Cor 25 | No | Proof re-derived hop by hop |
| 2 | **P0, real** | Thm 24, PRF and AEAD terms | ε_prf(q) and ε_ae(q,c,d) count only honest objects. Each `Open` of an adversarial object can name a new identifier and derives a new key, so up to q+d PRF queries and q+d AE keys occur | Now ε_prf(q+d) and ε_ae(q+d,c,d); proof hops G2'→G3 and G4→G5 rewritten | No | Proof |
| 3 | P0 | Def 21, eq. (6) | L was called "the number of admissible patterns". It is the size of a guessing space 𝒫 that contains every fresh pattern, and is a superset of the reachable patterns when slots are reused | Renamed and defined as 𝒫. The theorem now allows any covering pattern set. "Exact factor" refers to Adv_0 = L·Adv_1 for the chosen 𝒫 | Yes: `v401_patterns.py` | 300 seeded policies, every schedule enumerated: all fresh patterns lie in 𝒫; strictly fewer reachable in 143; 5 of 9 in a reuse example |
| 4 | P0 | Def 21, I_g | Pre- versus post-publication exposure, reused slots and unpublished generations were not stated precisely | I_g defined only for published generations, with exposure "before or after publication". Reused slots touch the index in every generation using them. Pre-publication exposure makes a capsule real but not late-exposed. Monotonicity of non-freshness stated. Duplicate `Challenge` calls are ignored | No | Proof |
| 5 | P0 | Lemma 23 | The reduction was sketched, not specified | Full table (Table 6): games, reduction, query bound, abort, freshness, advantage. NM is stated as the generic loss of this reduction, not a tight bound; N counts keys and M challenge queries, with no double counting | No | Proof |
| 6 | P0 | Thm 14, exponent view | Scope of the iff was unstated | New paragraph. Group and exponent transcripts are information-theoretically equivalent (E ↦ g₀^E is a bijection), so the iff holds for real commitments against unbounded adversaries. With partial disclosures the necessity direction is not efficient: it yields g₀^S, not S. Using the condition in Thm 24 freshness is conservative | No | Proof |
| 7 | P1 | Cor 4 / mask remark | "Uniformity is necessary" was over-broad | Now "necessary for the general coset characterization"; special non-uniform cases need their own argument | No | Existing counterexample re-run |
| 8 | P1 | Cor 5 | Conditional laws were stated without a positive-probability qualifier | Added | No | Proof |
| 9 | P1 | Prop 8 | Complexity units unspecified | O(N) comparisons and additions over ℤ≥0∪{∞}, O(N) memory with deterministic BFPRT; ties, zero and infinite costs covered | No | 2,500 formulas, re-run |
| 10 | P1 | Prop 9 | Incomplete statement | Weakly NP-hard; R = W−k+1; DP state, transition, time O(mR), space O(R); nested read-once time O(N + Σ_γ m_γ R_γ) | No | 2,000 instances, re-run |
| 11 | P1 | Prop 11 | Growth with G not explained | Doubly exponential in G; practical only for small G, consistent with Prop 10 | No | 400 instances, re-run |
| 12 | P1 | Obs 2, liveness | Necessary fairness was not established | Fairness map, six new TLC runs: WF suffices for WorkerReturns; SF is needed for Erase, SignReceipt and Restart; removing any one fails; all-WF fails through a crash/restart loop; WorkerAbandons needs no fairness. TLC traces are not minimal, and the paper now says so. Log and clock are outside the model | Yes: 6 cfgs, 5 spec variants | TLC |
| 13 | P1 | Limitations | The kernel's inability to terminate Python threads was not tied to the liveness requirement | Stated explicitly: the reference kernel does not meet it and needs process isolation | No | — |
| 14 | P2 | Abstract §8.2 | "Full adaptivity is equivalent to receiver selective opening" was unproved in both directions | Rephrased: within this approach, removing L would require an RSO guarantee or another construction; full adaptivity not claimed | No | grep: no "equivalent" remains in cryptographic claims |
| 15 | P2 | §2, Def 22 | Alwen et al. was cited as analysing HPKE **Base** mode; their paper analyses the **authenticated** mode | Citation corrected; Base-mode IND-CCA is an assumption | No | Checked against the ePrint abstract |
| 16 | P2 | Def 22 | Parameter names q, c reused with a different meaning | Renamed Q, K, C, D | No | — |
| 17 | P2 | Bibliography | Five "Springer, ???" (TCC 2007, EUROCRYPT 2009, ASIACRYPT 2015, CRYPTO 2017, EUROCRYPT 2021) | Locations added (Berlin, Heidelberg ×3; Cham ×2); publisher and location also added to Pedersen, BBM 2000, Mauw–Oostdijk | No | `grep ??? main.bbl` → 0 |

All 43 bibliography entries were re-read. Those already verified in v3 and v4 against DBLP, ePrint, publisher or indexing records were kept. No DOI was added unless it had been verified.

## Phase D: Validation actually executed (`artifact/reproduced/full_v401_run.log`)

- All v2, v3 and v4 Python checks reproduce their saved outputs exactly. The v4.0.0 checker outputs are unchanged.
- New check: `v401_patterns.py`.
- Tests: 59 pass (5 baseline, 25 v2, 14 v3, 15 v4).
- TLC: 8 v2 configurations, 13 v3, 9 v4.0.0 (identical to their saved records) and 6 new.
- Kernel conformance re-run: v4 kernel 0 divergences in 80,000 calls; v3 kernel 215 divergent schedules (212 authorize, 1 abandon, 1 commit, 1 finish).
- Random histories: 5,388 independent targets with 0 disagreements; 5 of 639 correlated targets disagree. This is evidence, not proof.
- LaTeX: halt-on-error build, 0 overfull boxes, 0 undefined references, 0 placeholders; 35 pages, two more than v4.0.0, mostly the Lemma 23 table.

## Phase E: Reviews

**Reviewer 1 (cryptography): weak accept, 70.**
- Theorem 24 is now internally consistent, and the hops have correct units (q+d keys, c chunk calls, d decryptions).
- The Lemma 23 table is complete.
- Remaining weaknesses: the generic NM loss; L is exponential in the number of target generations; HPKE Base IND-CCA is assumed rather than derived.
- The exponent-view scope paragraph resolves my concern that an information-theoretic necessity was being read computationally.
- Question: can 𝒫 be restricted to delivery-reachable patterns in the statement, as the coverage check suggests? (It can; the theorem now says any covering set is allowed.)

**Reviewer 2 (theory): weak accept, 64.**
- The complexity statements now match the algorithms, with units, edge cases and weak NP-hardness.
- The leakage results are correct and checked exhaustively on small fields.
- Novelty remains in the application, not in the mathematics.

**Reviewer 3 (systems / formal methods): accept / weak accept, 74.**
- The fairness map is what a liveness claim should carry: each assumption is shown necessary by a counterexample.
- The worker-termination requirement is stated honestly, including that the Python kernel does not meet it.
- Refinement is still tested, not proved, and is clearly labelled.

**Meta-review: weak accept.**
- No critical objection remains open.
- The major limitations are disclosed: restricted adaptivity, no refinement proof, and elementary mathematics.

## Final assessment

| Dimension | v4.0.0 | v4.0.1 | Reason |
|---|---|---|---|
| Mathematical correctness | 84 | 88 | Scope, units and edge cases fixed; nothing found false |
| Mathematical originality | 50 | 50 | Unchanged |
| Complexity-theoretic contribution | 58 | 61 | Complete statements; no new results |
| Cryptographic rigor | 72 | 78 | PRF/AE key counts corrected; full Lemma 23; exponent-view scope |
| Adaptive-security strength | 55 | 56 | Same theorem; covering-set refinement only |
| Systems-security contribution | 60 | 61 | Worker-termination gap stated precisely |
| Formal verification | 79 | 82 | Fairness map with necessity counterexamples |
| Experimental quality | 78 | 79 | Coverage check |
| Related-work accuracy | 77 | 80 | HPKE attribution and bibliography fixed |
| Presentation | 66 | 67 | Clearer statements; two more pages |
| **Overall** | **69** | **71** | |

**Strongest rejection argument (unchanged).** The cryptographic core is a guessing argument with a loss that is exponential in the number of generations, and the remaining mathematics is elementary.

**Venue category.** A journal or conference for security analysis and verification (ACM TOPS, JCS, CSF, ESORICS).
