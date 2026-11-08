# v4.1.0 → v4.1.1: release-consistency pass

Capability Exposure Accounting for Threshold-Based Encrypted Backup Recovery.
Samarjeet Malik (Ashoka University) and Shaurya Pratap Singh (Indian Institute of Science). 9 November 2026.
v4.1.0 is unchanged; its text is kept as `manuscript/main_v4.1.0.tex`. Inputs to this revision: the user's request to re-run the timings and re-check related work, and an outside review of the v4.1.1-interim PDF.

## 1. Mathematical and cryptographic changes
- **Notation.** `K` is now `K_key` (derived-key instances) and `D` is now `D_dec` (chunk decryptions), everywhere: Definition 22, Lemma 24, Theorem 25, Corollary 26, Tables 2 and 9, Figs. 7, 8 and 10, §§8.3 and 10.
- **Definition 22, two conditions made explicit.** No result changes.
  1. Decryption is excluded only for a challenge ciphertext under its *own key and label*. The record game allows `Dec` of a published capsule under another `info`, so the multi-user game must allow it too.
  2. A corrupted key may not be challenged. Lemma 23's step "a corrupted key cannot be challenged" depends on this. Theorem 25 meets it, because an eligible capsule's slot is unexposed when it is challenged.
- **Theorem 14.** It now says in its first sentence that the criterion is information-theoretic and does not imply efficient recovery of the scalar seed.
- **Conclusion.** Refresh is now stated to heal only under delivery-path independence.
- **Unchanged:** no theorem statement, hypothesis, bound or complexity result.

### Proof audit of Theorem 25 (by Claude, for the authors; NOT independent)
| Item | Checked | Result |
|---|---|---|
| Def. 21 | exposures, `Dec` exclusion, freshness monotone, touched sets cover late and early slot exposure and partial disclosure | consistent |
| Def. 22 | advantage forms; multi-user game conditions | 2 implicit conditions made explicit (above) |
| Lemma 23 | hybrid order; simulation of challenge, decryption and corruption; abort only before the j-th query; 1/N per hop; sum NM | correct, given Def. 22 as amended |
| Lemma 24 | ideal world key-independent; conditioning on no collision gives the distinct-key game; mixture (no factor 2) | correct |
| G0→G1 | Λ ∈ 𝒫 on fresh runs; Γ independent; early stop only on runs with Λ ≠ Γ; exact factor L | correct |
| G1→G2 | eligible = index ∉ Γ and slot unexposed at publication; a later exposure of such a slot is a late exposure outside Γ, so both games stop and no inadmissible corruption occurs; `Dec` on own capsules excluded; `Dec` under other `info` forwarded (needs condition 1) | correct |
| G2→G2′ | invariant (I); answers that the translation must preserve: commitments, coordinates at touched indices, real capsules, `Dec` on adversarial or mauled capsules (decrypt to touched-index coordinates or to zeros), acceptance as a function of transcript and Γ | correct |
| G2′→G3 | S used only as the HMAC key; q+r queries; target `SeedRoute` stops the run | correct |
| G3→G4 | the identifier event concerns equal contexts; distinct contexts with equal keys are carried by ε^iid | correct |
| G4→G5 | instance per context; nonce = chunk index; abandoned creation gets a fresh identifier; reordered or cross-context honest chunks counted in D_dec | correct |
| Cor. 26 | Lemma 23 + Lemma 24 terms propagated; no factor 2 | correct |

**Limitation of this audit.** It was done by the same assistant that helped write the proof, so it is not an independent review. An external cryptographer should still check G1→G2 and G2→G2′ before or during review. The paper's limitations section now says the proof was audited by the authors, not independently.

## 2. Implementation changes
- **Abrupt-death lifeline.** `worker_supervisor.py` now gives each worker a lifeline pipe. If the supervising process dies abruptly (SIGKILL), the worker exits at once (exit code 70).
- **New `test_worker_supervisor_v411.py` (4 tests):**
  - a real SIGKILL of a separate supervising process (`_parent_crash_helper.py`). The worker is gone within the deadline. The restarted kernel, rebuilt from the durable anchor, has no receipt, rejects the stale token, and accepts a receipt only after expiry and erasure.
  - a file opened by the parent is not inherited by the worker;
  - a completion arriving after expiry is discarded;
  - a terminated worker's token cannot satisfy a later request, and a duplicate completion is rejected.
- **Totals:** supervisor tests 6 → 10; all tests 95 → 99. Stable over three consecutive runs.
- **New `bench_supervisor_v411.py`:** direct vs process-supervised decryption.
- **Unchanged:** kernel, data layer, TLA+ models, expectations.

## 3. Experimental changes
- **Chunk and object timings re-run** on the Apple M5 (`evidence_v411/mac_m5`).
  - ChaCha20-Poly1305 ≥ 16 KiB and AES-256-GCM ≥ 64 KiB agree with v4.0.4 within 8%.
  - Store/Open at 256 MiB is 8–10% faster.
  - Small-chunk AES-GCM medians differ by up to 2×, and the paper says so.
  - v4.0.4 data kept.
- **Memory re-run under v4.1.1** (`evidence_v411/mac_m5_memory`, 7 trials per size): heap identical to before; RSS at 256 MiB median 807.9 MiB (range 807.8–808.2). The v4.1.0 minimum of 722 MiB did not recur.
  - Method now stated: two fresh processes per trial, `getrusage(RUSAGE_SELF).ru_maxrss` lifetime peak, MiB.
  - The reason for the 2× heap is now stated, checked against `datalayer.py`: the list of decrypted chunks plus the joined plaintext. The ciphertext is loaded before tracing starts.
- **Supervision cost** (`evidence_v411/mac_m5_supervisor`, 21 trials):

  | Size | Direct (median) | Supervised (median) | Worker RSS |
  |---|---|---|---|
  | 1 KiB | 0.02 ms | 48 ms | 29 MiB |
  | 64 MiB | 36 ms | 137 ms | 157 MiB |

  A fixed ~47 ms per decryption goes to starting the worker process. All §8.3 numbers are stated to exclude supervision.
- **Second platform (x86-64 Linux, Ashoka server, Slurm job 8081): NOT included.** The job stayed queued behind the user's other jobs (per-user CPU limit) for the whole session. All measurements are therefore still from one Apple M5, and the paper says so.

## 4. Related work (re-checked against full texts)
- **CKS** (ePrint 2024/914, the copy the user downloaded; text identical to the author-hosted June 2024 version): S1 verified. Thm. 3 (p. 23) gives preservation for CKS-compatible games in the ROM with non-committing one-time encryption. New point: §1 (p. 7) calls protecting the evolving state with HSM or PPSS, and securely erasing its old versions, "an orthogonal issue to CKS".
- **Standard-model CKS** (ePrint 2024/2100): S2 verified, including "selective security only" (§1.1, p. 4) and the impossibility (§2.3).
- **GKP/Grappa** (ePrint 2025/1028 full version, 71 pp.): S3 was incomplete. Its security is selective (§1, p. 9), and adaptive security is listed as open (§7.1, p. 41). Secret sharing appears only as a possible extension.
- **Paper and bibliography:** the paragraph is rewritten, and Table 1's CKS/GKP row is corrected. The bib now cites CRYPTO 2024 (DOI 10.1007/978-3-031-68379-4_3, pp. 75–109) and TCC 2024 (DOI 10.1007/978-3-031-78011-0_15, pp. 444–475), both checked against Crossref. The "not re-audited" disclaimer is gone.

## 5. Editorial changes
- **Version:** v4.1.1 is canonical throughout. Earlier-version labels survive only where they describe history.
- **Abstract:** "3,000 seeded histories with 5,388 target seeds"; the supervisor is mentioned. Length is 245 words (pdftotext), within the 250 limit.
- **Contribution list:** the version-by-version narration is removed; the content is unchanged.
- **New Table 11 (nonce and key-reuse properties)** and a sentence on deployment options.
- **Limitations** regrouped into: cryptographic; algebraic and observation model; formal lifecycle; implementation and measurements; operational and trust.
- **§9.4:** the lifeline, the 10 tests, the cost of supervision (new table), and a sentence on what process isolation does not establish.
- **Layout:** Fig. C1 now precedes the References (`\clearpage`), and the bibliography ends cleanly. 52 pages.

## 6. Executed runs (9 Nov 2026)
| Run | Exit | Result |
|---|---|---|
| `bench_v404.py` (Mac) | 0 | evidence_v411/mac_m5 |
| `bench_memory_v410.py` (Mac) | 0 | evidence_v411/mac_m5_memory |
| `bench_supervisor_v411.py` (Mac) | 0 | evidence_v411/mac_m5_supervisor |
| `make_plot_data.py` | 0 | data regenerated from v4.1.1 evidence |
| supervisor tests ×3 | 0 | 10/10 each time |
| `reproduce_all.py`, v4.1.1 tree (final code) | 0 | 99 tests (5 + 25 + 14 + 18 + 37), every TLC configuration; log in `reproduction_logs_v411/` |
| v4.1.1 artifact zip unpacked into an empty directory; fresh venv; TLC jar fetched and SHA-256 verified | 0 | 0 checksum mismatches; 99 tests, every TLC configuration |
| LaTeX, both builds from clean | 0 | 0 overfull boxes, 0 undefined references, 52 pp |

## 7. Not verified, or remaining assumptions
- Theorem 25: audited by the authors' assistant only, not independently.
- Second platform: not measured (see §3).
- The v4.1.1 artifact DOI and tag do not exist yet; one placeholder remains.
- Shaurya Pratap Singh has not yet confirmed the declarations, including the LLM disclosure.
- IJIS's current LLM policy was not re-read in this session.

## 8. Submission checklist
1. Co-author approves the declarations.
2. Reserve the Zenodo DOI for v4.1.1, insert it and the tag, then rebuild (see `release_staging/RELEASE_NOTES_v4.1.1.md`).
3. Publish the GitHub release and the Zenodo record. Re-run the fresh-unpack reproduction from the published files.
4. Optional: let job 8081 finish and add the x86 data as v4.1.2. The job writes to `/scratch/samarjeet_malik/cea_bench411/`.
5. Optional: an external cryptographer reviews G1→G2 and G2→G2′.
6. APC decision; submit.

## 9. Second release-candidate edits (rc2, after an outside reading of rc1)
Manuscript text only; no artifact code changed, so the 99-test runs in §6 still apply. rc1 is kept as `manuscript/main_v4.1.1-rc1.tex` and `output/pdf/Capability_Exposure_Accounting_v4.1.1-rc1*.pdf`.
- **§9.4, cost of supervision.** The trade-off is now spelled out. At 1 MiB the fixed ~47 ms dominates (50 ms supervised vs 0.5 ms direct). At 64 MiB supervised decryption takes 3.8 times as long as direct (137 vs 36 ms). The text also says that the combined peak RSS of the parent and worker processes was **not measured**; only the worker's own peak is reported.
- **§10, experimental unit.** The unit is now "target seeds" (5,388 with independent randomness, 639 with correlated randomness), the same term as in the abstract and §6.3.
- **Not done, and not something Claude can do:**
  - Publishing the v4.1.1 artifact and inserting its DOI and tag (the authors' release step; see `release_staging/RELEASE_NOTES_v4.1.1.md`).
  - An independent cryptographic review of Theorem 25.

## 10. DOI inserted (9 Nov 2026)
- **New version on Zenodo:** the user created the new-version draft (record 24060229). Claude reserved its DOI, **10.5281/zenodo.24060229**, set the version to 4.1.1 and saved the draft. Nothing is published.
- **Where the DOI now appears:** the data-availability statement (with tag v4.1.1), `CITATION.cff`, `.zenodo.json`, `RELEASE_METADATA.json`, `README.md` and the artifact README. The v4.0.7 DOI is still cited as the preprint and as the predecessor.
- **Placeholders:** none remain in either PDF.
- **Still to do:**
  - upload the files to the draft, update its description, and publish;
  - create and push the GitHub tag v4.1.1 with its release;
  - co-author confirmation.
