# Reproducibility manifest: manuscript v4.1.11, artifact v4.1.1 (9 November 2026)

Every result in manuscript v4.1.11 and its Online Resource 1 comes from the version 4.1.1 artifact. Manuscript versions 4.1.2 to 4.1.11 changed wording, layout and figures only; `artifact/` has not changed since v4.1.1.

## Versions and identifiers
| Item | Value |
|---|---|
| Manuscript | v4.1.11, `manuscript/main.tex` (SHA-256 `cdf5cbe499d283d182950a350671d98cf84522da9cce8c32325b1815d8955d8d`) and Online Resource 1, `manuscript/supplement.tex` (SHA-256 `9274733a06f70ad1ff8abf2a211c6fb91cb517c033610ece7638f6648745fba0`) |
| Compiled PDFs | v4.1.11: styled `2a882ea97958b3f91eca6f67d562c82e1ec0432c5bac6bf50a60ecd0ccb41dc4`; submission `dda7b95fec0bf577a83985c3734f6a5f31a6b40fb5f2317257733e9876465877`; Online Resource 1 `ef64f6b7745e1e5e4d125e4a708f11b11186876e652448d69b36d78ad1b1644f` (also in `REVISION_V4.1.11.md`). Published v4.1.10 PDFs: GitHub release v4.1.10 and Zenodo 10.5281/zenodo.24090614. Published v4.1.9 PDFs: GitHub release v4.1.9 and Zenodo 10.5281/zenodo.24090414. Published v4.1.8 PDFs: GitHub release v4.1.8 and Zenodo 10.5281/zenodo.24089585. Published v4.1.7 PDFs: GitHub release v4.1.7 and Zenodo 10.5281/zenodo.24088767. Published v4.1.6 PDFs: GitHub release v4.1.6 and Zenodo 10.5281/zenodo.24084300. Published v4.1.1 PDFs: full hashes in the v4.1.1 SHA256SUMS. |
| Artifact (source of all results) | v4.1.1: Zenodo DOI 10.5281/zenodo.24060229 (published 9 Nov 2026; its artifact zip has MD5 688235160ab9ef19731d4810e034152c); GitHub tag `v4.1.1`. The v4.1.6 release archives the same `artifact/` byte for byte. |
| Archived predecessor | v4.0.7: Zenodo DOI 10.5281/zenodo.24048192; GitHub tag `v4.0.7` → commit `80d40a8c83b13e25712839327de45b144de83b52` |
| All versions | Zenodo concept DOI 10.5281/zenodo.24048191 |
| Measurements in the paper | all from v4.1.1 runs on one Apple M5: `evidence_v411/mac_m5` (timings), `mac_m5_memory`, `mac_m5_supervisor`. Earlier evidence (`evidence_v404`, `evidence_v410`) is kept but no longer plotted. |

## Environment
Apple M5, 24 GiB, macOS 26.5.1, which reports FEAT_AES and FEAT_PMULL. Software:
- CPython 3.12.14 with cryptography 50.0.2 (OpenSSL 4.0.3);
- OpenJDK 26.0.2.1;
- TLC2 2.19 (v1.7.4); jar SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`;
- TeX Live 2026 (pdfTeX, BibTeX, latexmk).

## Commands
```sh
cd artifact
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
python3 fetch_tlc.py
.venv/bin/python reproduce_all.py --java "$(command -v java)" --jar .tools/tla2tools.jar   # 99 tests + all TLC
.venv/bin/python bench_v404.py evidence_v411/mac_m5            # timings (machine-dependent)
.venv/bin/python bench_memory_v410.py evidence_v411/mac_m5_memory
.venv/bin/python bench_supervisor_v411.py evidence_v411/mac_m5_supervisor
python3 make_plot_data.py                                       # defaults read evidence_v411
cd ../manuscript && latexmk -pdf -halt-on-error main.tex && latexmk -pdf -halt-on-error main_submission.tex && latexmk -pdf -halt-on-error supplement.tex
```

## Executed runs
See `REVISION_V4.1.1.md` §6 and the logs in `reproduction_logs_v411/`.

## Provenance
| Item | Source | Kind |
|---|---|---|
| Fig. 12, Table 12 (times) | `evidence_v411/mac_m5` | measured |
| Fig. 13, Table 12 (memory) | `evidence_v411/mac_m5_memory` | measured |
| Table 15 (supervision) | `evidence_v411/mac_m5_supervisor` | measured |
| Figs. 6, 7, 9, C1; Table 10 | `make_plot_data.py` from the paper's formulas | analytical |
| Fig. 4 | derived from Theorem 15 | derived |

## Hashes (SHA-256)
```
908fd6c4b20dcade709b1f5b843e63e374baf135e59a94e499fba0754e76b1d0  artifact/lifecycle_kernel.py
181695e190ad1892e06219700302ed199d0980f92cc8b6f1c618591c0915bcf9  artifact/datalayer.py
b6b7007ea24df16ce9269d2002483ce6d75cc7ade79af31dc23d2ac802db3bec  artifact/worker_supervisor.py
0b6f354075063fdeadf9270acc92ae8e4fe3baa06ea45272dc93035f757ddcc4  artifact/test_worker_supervisor.py
afd40eafa87a16300ab93a445ef16430ddfbbb4b54aea11756b06292364b70c7  artifact/test_worker_supervisor_v411.py
4a49ca469893056d5fcf2a50316ac914c88881cc3cabcfc5f686def163263743  artifact/_parent_crash_helper.py
4aeb562a2995d8a00a86588d7452b46cce289e57c6eec8b1d4c74b179604768f  artifact/bench_supervisor_v411.py
14795bf1ce7d65cce4642ae79b70d0597fb0d037f7e54aef07bbd681cd8c6b5d  artifact/bench_memory_v410.py
5d9d32942f5716af7d2ca85b95aab24c961bf91602fcd218d99de7314b25d6f4  artifact/bench_v404.py
b38c7f7d45aec66cd4511aa48fdee6f5679e51dda8de7c2ee6d660a5e6919b36  artifact/reproduce_all.py
2d08b8688e5f06c06da5602a5b044d101da9041e89230b00c940628e7c5abc0c  artifact/make_plot_data.py
66240f078afe66c82541621be1a7e95b0eb9a431661522900581ac94486e5f08  artifact/evidence_v411/mac_m5/bench_v404.json
b0c33052dec813909b99b547aad012b87ab116e8f491e8cdfa884e3a68adc8e9  artifact/evidence_v411/mac_m5_memory/bench_memory_v410.json
b677b3871b2c305f6aa77c508ba3dfc1f36d5381cd9343b8ad8f7027b50cc2bd  artifact/evidence_v411/mac_m5_supervisor/bench_supervisor_v411.json
```
Every released file is listed in `SHA256SUMS`.

## Second machine and container (v4.1.11)
- `evidence_x86_epyc9554/`: the data-layer and memory benchmarks re-run unchanged on a 2-socket AMD EPYC 9554 server (Slurm job 8081, 9 Nov 2026; CPython 3.11.16, pyca/cryptography 50.0.2, OpenSSL 4.0.3). Its scripts are byte-identical to `artifact/`. Reported in Online Resource 1, Table S3. The supervisor benchmark was not run there.
- `Dockerfile` / `CONTAINER.md`: pinned container (python:3.12.14-slim-bookworm by digest, cryptography 50.0.2, checksum-verified TLC 1.7.4). Built and run in GitHub Actions (x86-64 Linux, run 42676588599, 9 Nov 2026) with `docker run --init`: all 99 tests and every TLC configuration pass. Logs in `container_runs/`. Without `--init`, the supervisor-crash test counts its exited, unreaped (zombie) worker as alive; see CONTAINER.md.
- `scripts/rerun_and_log.sh` / `COAUTHOR_RERUN.md`: one-command independent re-run with a recorded log (self-tested on the authors' Mac; the co-author re-run is pending).
