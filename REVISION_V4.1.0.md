# v4.0.9 → v4.1.0: finalisation pass

Capability Exposure Accounting for Threshold-Based Encrypted Backup Recovery.
Samarjeet Malik (Ashoka University) and Shaurya Pratap Singh (Indian Institute of Science).
9 November 2026. Baseline v4.0.9 is unchanged; its text is kept as `manuscript/main_v4.0.9.tex`.

Scope: the outside review of the v4.0.9 PDF, and the plan approved on 9 Nov. No theorem, proof, bound or earlier result changed. The abstract (234 words) and the six keywords are unchanged.

## 1. Mathematical and notation changes (meaning unchanged)
- **K:** the adversary root set is now `𝒦_root` throughout §3 and §6 (24 occurrences). `K` now means only the derived-key instances.
- **D:** `D` now means only the chunk-decryption count.
  - The §5 deletion set is now `𝓔` (erasure set).
  - The polynomial `D(X)` in the Theorem 14 proof is now `Φ(X)`.
  - The latencies in Proposition 20 are now `T_rt, T_log, T_app, T_loc`, in the statement, eq. (5), the proof and the text. The local wait `L` in its proof is now `ℓ`.
- **Table 2:** the remaining "local" rows are gone, except R and W in Proposition 9, which are marked.
- **Complexity:** Proposition 11 is now described as **XP in G, not FPT**: polynomial for each fixed G, with exponent ∝ 2^G. The same wording is in the contribution list, "What is specific here" and Table 15.
- **New paragraphs:**
  - "What Theorem 14 establishes" (information vs. efficient recovery: g₀^S vs. S; complete openings);
  - "Operational reading" after Corollary 16;
  - a reading of Table 10 in log₂L terms. Each renewed 5-of-7 generation adds about 6.6 bits: about 20 bits for three generations and about 40 for six. Reused-bank counts hold only for Proposition 27's map. Values come from `data/guess_equal.dat`.

## 2. Implementation changes
- **Corrected a false statement in v4.0.9.** v4.0.9 said "the Python reference kernel runs workers as threads", and older text said "Python threads cannot be killed". The kernel runs no workers: it hands out a token at `begin_decrypt` and waits for `finish_decrypt` or `abandon_decrypt`. Until now, nothing in the artifact executed or terminated a worker.
- **New `artifact/worker_supervisor.py`.**
  - Each decryption runs in its own OS process (spawn start method), receiving only one key, nonce, ciphertext and associated data.
  - A returned result goes to `finish_decrypt`.
  - On a crash, or on termination after a grace period, the supervisor joins the process, records the exit code, and only then calls `abandon_decrypt`.
  - A kernel crash terminates every worker first.
  - The kernel is unchanged.
- **New `artifact/test_worker_supervisor.py` (6 tests):**
  - normal completion (real ChaCha20-Poly1305 open in the child);
  - a hung worker blocks `sign_receipt` until it is terminated;
  - termination after a grace period;
  - a crashing worker (exit code 3) is abandoned;
  - a late completion after termination is rejected;
  - a kernel crash, then restart, then receipt.
- **Manuscript:**
  - new §9.4 "Process-isolated workers";
  - the observation, warning box, Table 14 row, Table 15 row and §11 limitations are rewritten.
  - Liveness is still TLC-checked under fairness only. The supervisor is tested, not proved, and it is not a sandbox and does not scrub memory.

## 3. Experimental changes
- **New `artifact/bench_memory_v410.py`.** It uses 7 independent trials per size (1–256 MiB). Each trial stores the object in one fresh process and opens it in another, and records the `tracemalloc` peak during Open and `ru_maxrss`. There are 7 idle-interpreter baselines. Raw data is in `artifact/evidence_v410/`.
- **Results:**
  - Python heap was identical in all trials: 1.00 MiB at 1 MiB, and exactly 2× the object size from 4 MiB up.
  - Process RSS medians: 31.3, 41.5, 78.0, 224 and 808 MiB. The 256 MiB range was 722–808.
  - The idle baseline is about 28.7 MiB.
- **Paper:**
  - Fig. 13 (right) now plots both memory series with their ranges.
  - Table 11 has heap and RSS columns.
  - The text and caption say that RSS includes the interpreter and the loaded ciphertext.
- **Timings:** the v4.0.4 timings are unchanged and were not re-run.
- **Data regeneration:** `make_plot_data.py` regenerates every earlier data file byte for byte.

## 4. Editorial changes
- **Declarations:** competing interests, funding, CRediT and LLM use are filled in from the corresponding author's answers in chat on 9 Nov. For LLM use, the author first chose "copy-editing only". I pointed out that this would misstate the recorded use, and the author chose the disclosure statement instead.
- **Remaining placeholder (1):** the DOI and release tag of the v4.1.0 artifact.
- **Data-availability text:** rewritten for v4.1.0.
- **Fig. 8:** labels raised from 5.6 pt to 6.6 pt, games and bound to 8 pt, with wider spacing.
- **Fig. 13:** fonts raised to 8 pt.
- **Final page:** the reference stranded on a near-empty last page in v4.0.9 is gone; the bibliography now ends naturally on p. 49.
- **Length:** 48 → 49 pages, from §9.4, the new paragraphs and the longer Table 11.

## 5. Tests and runs actually executed (9 Nov 2026)
| Run | Exit | Result |
|---|---|---|
| `test_worker_supervisor` alone | 0 | 6/6 |
| `bench_memory_v410.py` | 0 | 35 measurements + 7 baselines |
| `make_plot_data.py evidence_v404/bench_v404 evidence_v410` | 0 | earlier data byte-identical |
| `reproduce_all.py` on the v4.1.0 tree | 0 | 95 tests (5 + 25 + 14 + 18 + 33), every TLC configuration |
| v4.1.0 artifact zip unpacked into an empty directory, fresh venv, TLC jar freshly fetched (SHA-256 verified): SHA256SUMS and full `reproduce_all.py` | 0 | 0 checksum mismatches; 95 tests, every TLC configuration |
| `latexmk -halt-on-error`, both builds from clean | 0 | 0 overfull boxes, 0 undefined references, 49 pp each |

## 6. Claims not independently reproduced here
- The v4.0.4 timings (Fig. 12, Table 11 times). They are recorded on one Apple M5 and were not re-run.
- All measurements come from one machine. There are no cross-platform, concurrent or streaming measurements.
- The CKS and GKP/Grappa comparisons are carried over from v2.0.0 and were not re-audited (the manuscript says so).

## 7. Author steps before submission
1. Shaurya Pratap Singh confirms the four declarations.
2. Publish the v4.1.0 artifact (GitHub tag `v4.1.0`, then a new Zenodo version). Insert its DOI and tag in place of the last `\authorinput`, rebuild, and check that no placeholder text remains in either PDF.
3. APC decision and waiver request (IJIS, US$3,690).
4. Optional: ORCID iDs; the CKS/GKP re-audit.

After this, the manuscript is frozen. Further changes should come only from a substantive reviewer objection or a demonstrated error.
