# v4.0.4 → v4.0.5: restricted-adaptive qualification

Capability Exposure Accounting for Threshold-Based Encrypted Backup Recovery
Samarjeet Malik (Ashoka University), Shaurya Pratap Singh (Indian Institute of Science)
6 November 2026.

- **Baseline:** v4.0.4 is preserved unchanged (`..._v4.0.4.zip`, `pdf/..._v4.0.4*.pdf`, `manuscript/main_v4.0.4.tex`).
- **Scope:** manuscript text only. No theorem statement, proof, number, figure, test or artifact code changed.
- **Not done:** nothing was pushed, released or submitted.

## Where the qualification now appears

| Location | v4.0.4 | v4.0.5 |
|---|---|---|
| Abstract | "adaptive composition theorem … loss L" | "*restricted-adaptive* composition theorem …; it does not provide full adaptive security", with L = 1 (forward-ordered), 16 (one 3-of-5 generation) and exponential growth under renewal |
| Keywords | adaptive corruption | restricted-adaptive security |
| Contribution 5 | — | "It is not a full adaptive-security result." |
| Theorem 15 note | ideal view | states that Theorem 25 replaces it by real capsules at the price of L |
| Section 8 title | Adaptive exposure game and composition | … and restricted-adaptive composition |
| After Theorem 25 | key-result box only | warning box "Restricted, not full, adaptive security": L = 970,299 for three renewed 5-of-7 generations, the bound is vacuous when L is large, and removing L would need receiver selective-opening security that HPKE is not known to have |
| Conclusion | — | "This is not full adaptive security; within our approach that would need a receiver selective-opening guarantee." |

## Checks

- Both builds: 45 pages, halt-on-error, 0 overfull boxes, 0 undefined references. The warning box was inspected on page 25 (styled build) and renders as a bold run-in paragraph in the submission build.
- Artifact re-run in the v4.0.5 tree: see `artifact/evidence_v405/full_v405_run.log` (82 tests: 5 + 25 + 14 + 18 + 20; all v2, v3 and v4 TLC configurations match; exit 0).

## Assessment

The score does not change: the limitation was already stated in the theorem. What changed is that a reader who reads only the abstract, the boxed result or the conclusion can no longer come away believing the paper proves full adaptive security.
