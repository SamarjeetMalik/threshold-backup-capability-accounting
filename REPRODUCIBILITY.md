# Reproducibility manifest, v4.1.1 (9 November 2026)

## Versions and identifiers
| Item | Value |
|---|---|
| Manuscript | v4.1.1, `manuscript/main.tex` (SHA-256 `53b90045468b316f9201bfa92e84ef1a0ce6d83519d5c87af7787851d8bcf156`) |
| Compiled PDFs | `output/pdf/Capability_Exposure_Accounting_v4.1.1.pdf` (`20d655a31b0a8c5cb99cac5c36e2f3e656e39157ca7949c1f49e02a478c693a1`); `…_v4.1.1_submission.pdf` (`8a22345435ce2938512732b66fa4876d7522872b2d1263cfbd780d2fc97dbfc1`) |
| Artifact | v4.1.1: Zenodo DOI 10.5281/zenodo.24060229 (reserved 9 Nov 2026; registered on publication); GitHub tag `v4.1.1` |
| Archived predecessor | v4.0.7: Zenodo DOI 10.5281/zenodo.24048192; GitHub tag `v4.0.7` → commit `80d40a8c83b13e25712839327de45b144de83b52` |
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
cd ../manuscript && latexmk -pdf -halt-on-error main.tex && latexmk -pdf -halt-on-error main_submission.tex
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
