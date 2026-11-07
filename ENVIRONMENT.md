# Environment (recorded run of v4.0.4, 6 November 2026)

- Hardware/OS: Apple M5, 24 GiB RAM, macOS 26.5.1 (Darwin 25.5.0)
- Python: CPython 3.12.14. Standard library only for all checks except the reference data layer, which needs `cryptography==50.0.2` (pyca/cryptography; recorded with OpenSSL 4.0.3), pinned in `artifact/requirements.txt`
- Java: OpenJDK 26.0.2.1 (Homebrew). The v2 TLC counts are identical to the original Temurin 17.0.21+9 record; any Java 17+ is expected to work.
- TLC: official TLA+ release v1.7.4 (TLC2 2.19), `tla2tools.jar` SHA-256 `936a262061c914694dfd669a543be24573c45d5aa0ff20a8b96b23d01e050e88`, fetched and verified by `artifact/fetch_tlc.py`
- LaTeX: TeX Live 2026, pdfTeX, BibTeX, latexmk; Springer `sn-jnl` class and `sn-mathphys-num` style included

## Commands

```sh
cd artifact
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
python3 fetch_tlc.py                      # once; verifies the pinned checksum
.venv/bin/python reproduce_all.py --java java --jar .tools/tla2tools.jar
.venv/bin/python bench_v404.py            # optional measurements; machine-dependent
python3 make_plot_data.py                 # regenerates manuscript/data/*.dat
cd ../manuscript
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex             # styled
latexmk -pdf -interaction=nonstopmode -halt-on-error main_submission.tex  # submission-safe
```

The full run takes a few minutes on a laptop. Unsafe TLC configurations are expected to report their named violations; the runners treat an unexpected pass as a failure. TLC opens a local RMI socket, which a sandbox may need to permit.
