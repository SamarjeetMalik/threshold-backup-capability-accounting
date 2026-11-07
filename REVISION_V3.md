# Version 3.0.0 revision report

Capability Exposure Accounting for Threshold-Based Encrypted Backup Recovery
Samarjeet Malik (Ashoka University), Shaurya Pratap Singh (Indian Institute of Science)
Prepared 5 November 2026. v2.0.0 is preserved unchanged in `../Capability_Exposure_Accounting_Artifact_v2.zip`, `manuscript/main_v2.0.0.tex`, `artifact/baseline_v2/`, and the v2 TLA+ module and configurations, which still run.

Nothing was pushed to GitHub, submitted or published.

---

## Pass 1: Independent audit

| Result (v2 numbering) | Status | Defect | Correction in v3 |
|---|---|---|---|
| Thm 1 closure | Correct | Monotonicity used later but not stated | Stated and proved in Thm 1 |
| Thm 2 (i) reconstruction | **Imprecise** | "unit row in row span of [A B]" is dimensionally ambiguous; the target vector is (e_i, 0) ∈ F^{1×(k+r)} | Thm 3(4); also shows linear decoding is optimal on full domains and not on restricted domains (example over F_5) |
| Thm 2 (ii) privacy | Correct for product domains | Converse fails for correlated / non-product seed supports; no leakage quantity | Thm 3(3): privacy iff U annihilates D−D; Thm 3(5): I(S;Y)=H(MS) ≤ (rank[A B]−rank B)·log p |
| Cor 3 adaptive | Correct | Remark that it does not extend to conditioning on freshness was overcautious when acceptance is a function of the transcript | Cor 4 states the conditioned version; no claim for rejected transcripts |
| Thm 4 witness hitting | **Requires a hidden assumption** | False if an atom is both an honest fact and an adversary copy (deleting the honest copy "hits" a witness that survives) | Assumption 1 (origin tagging) made explicit; complexity results added (Props 7–8) |
| Thm 5 joint generations | **False as stated** | Counted complete share/opening pairs. B(x₁) alone plus A(x₂) alone leaks S at t=2 in the paper's own exponent view. 150/375 exhaustive patterns mispredicted | Thm 11 counts touched indices, requires pointwise disclosures (aggregate counterexample shows necessity), proved both directions |
| Deletion bound (eq. 5) | Correct | `min(n, ·)` hid the assumption c ≤ q_d − f | Assumption explicit; 5,427 enumerated configurations agree exactly |
| Quorum feasibility (eq. 6–7) | Correct | Single committee only | Prop 15: separate committees; global vs per-committee budgets |
| Slot lemma | Correct | — | Losses 1 / T / n / nT confirmed; N-epoch double counting clarified |
| Recovery deadline | Valid but under-specified | Depends on hold starting at request observation (unstated); loose | Prop 16: sharper bound 4D+C+max(H+C, hold)+P, alternative if hold starts at certificate |
| Lifecycle invariants (TLA+) | Hold, but **incomplete** | Cancellation atomic in model; kernel's decryption worker runs outside the lock, so a receipt could be signed while it still held plaintext | `RecoveryLifecycleV3.tla` adds an `aborting` state and `ReceiptAfterWorkers`; TLC 7-step counterexample under v2 guards |
| Python kernel | **Defect** | Same in-flight receipt gap; `KeyError` on unknown nonce; vacuous self-issued checkpoint in `finish_decrypt` | Inflight token tracking, `abandon_decrypt`, `Rejected` on unknown nonce; vacuous check documented; v2 kernel preserved and the defect reproduced by a test |
| New: composition theorem (my own draft) | **Error caught in self-review** | First draft let the adversary nominate seeds; then the PRF hop is invalid (it can evaluate HMAC under each candidate) | Game changed: uniform target seed, challenge on record plaintexts |

## Pass 2: Related work and novelty

Newly cited after checking primary records: Cachin–Haralambiev–Hsiao–Sorniotti, *Policy-Based Secure Deletion* (CCS 2013, ePrint 2013/152), the closest predecessor to the witness structure; Reardon–Basin–Capkun, *SoK: Secure Data Deletion* (S&P 2013); Ostrovsky–Yung (PODC 1991); Mauw–Oostdijk (ICISC 2005); Lopuhaä-Zwakenberg–Budde–Stoelinga (IEEE TDSC 2022); Juicebox (ePrint 2025/348); Karp 1972; Dinur–Safra 2005; Canetti–Feige–Goldreich–Naor 1996; Bellare–Boldyreva–Micali 2000.

**Novelty consequence.** The read-once linear-time evaluation and the NP-hardness of shared-node structures were planned as new results. Both are known from attack-tree analysis (minimum erasure is a minimum attack on the dual formula). The manuscript now credits them, and claims only the backup-specific boundary: reusing a delivery credential across 2-of-2 generations is already vertex-cover hard.

The CKS / GKP / Janneck–Riepel / Kintsugi comparisons are carried over from v2 and were **not re-audited** in this pass; the paper says so.

What the paper now claims as its own (Table 1 and §2 of the manuscript):
- **New (elementary, exact):** leakage-subspace characterization, used as the decision object for reconstruction, privacy and leakage.
- **New (correction):** index-counting generation theorem plus the pointwise-disclosure requirement.
- **New (accounting):** temporal exposure theorem and healing classification, i.e. algebraic independence versus delivery independence.
- **New (application of known hardness):** credential reuse as the erasure-hardness boundary.
- **New (standard technique):** selective-exposure composition for the concrete profile.
- **Engineering / evidence:** lifecycle defect and fix, multi-guardian barrier model, committee enumeration.
- **Not original:** linear sharing, monotone closure, hitting-set formulation, bottom-up attack-tree evaluation.

## Pass 3: Theory (all in the manuscript with complete proofs)

Thm 3 (leakage subspace), Cor 4 (adaptive), Thm 5 (witness hitting, with Assumption 1), Prop 7 (read-once, known), Prop 8 (reused-credential hardness), Lemma 9 (blockwise), Thm 11 (corrected generations), Thm 12 + Cor 13 (temporal accounting, healing), Props 14–16 (holders, committees, deadline), Thm 17 (selective composition), Lemma 18 (slots).

Attempted and **not** established:
- Adaptive composition (commitment problem).
- A TLAPS proof.
- A refinement mapping Python ↔ TLA+ ↔ algebra; the paper documents the differences instead (Table 7).
- A polynomial algorithm for reused-bank erasure when every generation uses the same holder set. That case is easy (pick the cheapest max_g(n − t_g + 1) holders), but it was not proved or tested, so it is not in the paper.

## Pass 4: Formal and computational validation

New files (all under `artifact/`):
- `v3_leakage.py`, `v3_erasure.py`, `v3_temporal.py`: checkers; outputs in `expected/v3_results.json`.
- `test_v3.py`: 14 tests, 6 of them kernel tests with real threads.
- `RecoveryLifecycleV3.tla` plus 6 configs; `MultiGuardianErasure.tla` plus 7 configs; `run_tlc_v3.py`; expected results in `expected/v3_tlc_results.json`.
- `reproduce_v3.py`: one entry point for all Python evidence.
- `baseline_v2/`: the unmodified v2 kernel and tests.
- `reproduced/full_v3_run.log`: complete local run (v2 Python, v3 Python, v2 TLC, v3 TLC).

Environment recorded: CPython 3.12, OpenJDK 26.0.2.1 (Homebrew), TLC2 2.19 jar SHA-256 `936a2620…0e88`. The v2 TLC counts reproduce exactly under Java 26.

Sampling disclosure: the leakage, block, read-once, vertex-cover and renewed-credential families are **seeded pseudo-random** families, each member decided exactly. The partial-opening patterns, healing cells and committee configurations are **exhaustive**.

## Pass 5: Manuscript

`manuscript/main.tex` was restructured to follow the requested argument (problem → model → closure → leakage → erasure → temporal → quorum → crypto → formal → experiments → limits). It builds with `latexmk -pdf -halt-on-error`: 27 pages, 0 overfull boxes, 0 undefined references. The abstract and title were finalized last; the title is unchanged because the contribution still fits it.

## Pass 6: Adversarial review

### Reviewer 1 (cryptography)
- *Strength:* Thm 11 now has a correct statement with both directions, and a counterexample shows the old one was wrong. Thm 17 is a proper hybrid with explicit hops.
- *Major:* Thm 17 is selective only. In a backup setting the adversary chooses whom to compromise after seeing traffic, so selective security is a real limitation, not a technicality. **Resolution:** stated in the theorem, in §8.2 and in the limitations; not resolvable without noncommitting encryption or a ROM argument.
- *Major (resolved):* the first draft of Thm 17 had a broken PRF hop (adversary-nominated seeds). Fixed.
- *Minor:* "information-theoretic" claims sit beside computational commitments. The paper now notes that partial disclosures reveal g^S to bounded adversaries.
- *Minor:* the HPKE multi-ciphertext loss M could be tightened using multi-user bounds; not attempted.

### Reviewer 2 (systems security)
- *Strength:* the in-flight worker defect is a real erasure bug, the kind receipts are meant to rule out.
- *Major:* there is still no deployment, performance data or end-to-end client. **Resolution:** declared out of scope, and no numbers were invented.
- *Major:* the separate-committee result is negative (it buys nothing under one global budget). Reviewer agrees this is honest and useful, and asks that the paper not imply per-domain budgets are realistic. Wording checked.
- *Minor:* "process crash ends workers" is an abstraction; RAM may persist. This is now stated in the TLA comment and the limitations.

### Reviewer 3 (formal methods)
- *Strength:* every model has a negative control. A liveness property is checked with explicit fairness, and its violation is demonstrated.
- *Major:* there is no refinement proof, and the multi-guardian model abstracts each guardian's lifecycle. **Resolution:** Table 7 lists the correspondences and differences, and the paper claims no refinement.
- *Minor:* the state spaces are small (n ≤ 7). Acceptable for counterexample search; the paper does not claim generality from them.
- *Minor:* `IdentityCompromise` in the lifecycle model is vacuous. Now disclosed.

### Meta-review
The audit and its corrections are the paper's real contribution. One false theorem was corrected. Two hidden hypotheses were made explicit. One code-level erasure defect was found and fixed with matching model-checking evidence. A self-introduced error was caught before release. The theoretical results are exact but elementary. Novelty rests on the backup-recovery accounting, not on new mathematics. Recommendation: suitable for external review at a security journal or a formal-methods-in-security venue, framed as an analysis paper. Not suitable for a top cryptography venue without an adaptive composition theorem.

## Part XII: Quality control

1. **Every theorem correct?** To my checking, yes. Each has a complete proof, and the counterexamples and exhaustive checks agree with the statements. This has not been externally refereed.
2. **Proofs complete?** Yes for all stated results. The lifecycle induction is manual, not TLAPS.
3. **Assumptions explicit?** Yes: origin tagging, pointwise disclosure, honest independent generation, opaque unopened envelopes, selective exposure, hold-start timing, c ≤ q_d − f, and fairness.
4. **Differentiated from literature?** Narrowly. Cachin et al. and the attack-tree literature cover substantial ground, and the paper says so.
5. **Unsupported cryptographic claims?** None found. Composition is selective only. No physical erasure claim is made.
6. **Numerical results reproducible?** Yes, via `reproduce_v3.py`, `run_tlc.py` and `run_tlc_v3.py`, with expected outputs and logs.
7. **TLA+ and Python compatible?** Compatible abstractions with listed differences. No refinement is claimed.
8. **Counterexamples preserved?** Yes: v2 TLC logs, v3 logs, and the in-flight, half-opening, aggregate-response, shared-root and committee cases.
9. **Citations accurate?** The new ones were checked against DBLP, ePrint or publisher records during this revision. Karp 1972, Dinur–Safra, CFGN 1996 and BBM 2000 are standard references cited from memory with standard bibliographic data; verify page numbers before submission.
10. **Conclusion matches results?** Yes.
11. **Ready for external review?** Yes, as an analysis paper.
12. **Strongest remaining weakness:** there is no adaptive end-to-end confidentiality theorem, and the core mathematics is elementary.

## Scores (independent; not inflated by added material)

| Dimension | v2.0.0 | v3.0.0 | Reason |
|---|---|---|---|
| Mathematical rigor | 62 | 80 | One false theorem and two hidden hypotheses fixed; all proofs complete |
| Cryptographic rigor | 50 | 64 | Real hybrid composition theorem, but selective only |
| Originality | 40 | 48 | Accounting and corrections are new; the tools are known, and two planned "new" results turned out to be known |
| Theoretical contribution | 45 | 58 | Leakage subspace, healing classification, hardness boundary |
| Systems contribution | 45 | 52 | Real erasure-ordering defect found and fixed; still no deployment |
| Formal verification | 60 | 72 | Multi-guardian safety and fairness-liveness; documented non-refinement |
| Experimental methodology | 62 | 74 | Exhaustive vs seeded labeled; v2 reproduced on a new JDK |
| Related-work positioning | 55 | 72 | Closest predecessor added; known results credited |
| Writing | 60 | 68 | Restructured argument; still dense |
| **Overall** | **52** | **64** | A sound, honest analysis paper; not a breakthrough |
