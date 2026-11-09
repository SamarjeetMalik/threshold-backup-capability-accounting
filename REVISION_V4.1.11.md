# Revision v4.1.11 (9 November 2026)

Work on the score items listed after v4.1.10, done at the corresponding author's request. Artifact v4.1.1 is unchanged. No theorem, bound, proof step or previously reported number changed; the only new numbers are the second-machine measurements.

## Done
**Presentation**
- Table 1 "Results at a glance" (one row per main result, with its section).
- Running example: the introduction's history is named as such and used in Sections 6.3 and 8.2.
- Notation table limited to symbols used across sections.
- Sections 8.4 (independent-slot component) and 8.5 (symbolic failure budget) moved to Online Resource 1, Section S5 (Lemma S1, eq. (S1), Table S8); Section 8.3 states both in one paragraph.
- Section 6.2: two paragraphs that both explained the efficient-adversary gap merged (−138 words).
- Section 8's remaining remark paragraphs each carry a definition, a number or a theorem-specific point; they were kept.

**Figures**
- Fig. 1: outcome arrows leave U through one bus and enter each outcome box horizontally.
- Fig. 4: panel (d) folded into (c), so the outcome sits under the counts; caption updated.
- Fig. 9: (a) path and (b) request panels with orthogonal routing and no diagonal or crossing arrows. A side-by-side layout does not fit the 13 cm text width (the request chain alone needs about 11 cm).
- All three at natural size (0 FIGSCALE), 8 pt.

**Formatting**
- DOIs added to seven references after checking title, authors, venue and pages on Crossref. The Perlman (NDSS 2007) hit on Crossref is a 2005 workshop version and was not used.

**Reproducibility**
- x86 benchmark (Slurm job 8081) completed: 2-socket AMD EPYC 9554, CPython 3.11.16, same library versions; scripts byte-identical to `artifact/`. Evidence in `evidence_x86_epyc9554/` (lab paths and host name redacted); reported in Section 8.3 and Online Resource 1, Table S3. The limitations now say the data-layer measurements come from two machines and the supervisor costs from one.
- `Dockerfile` and `CONTAINER.md`: pinned container (base image by digest, cryptography 50.0.2, checksum-verified TLC). Not built: no container runtime was available here; the file says so.

## Not done here (needs people or new research)
- ORCID iDs: need the authors' iDs.
- Independent review of Theorem 25 and a second reader for Theorems 14–15: need an outside cryptographer.
- Shaurya's re-run of `reproduce_all.py` on his machine.
- New mathematical results (general delivery maps, a fully adaptive variant, a lower bound on L): research, not presentation.

## Checks
- `main_submission.tex` 46 pp., `main.tex` 47 pp., `supplement.tex` 12 pp.; all with -halt-on-error: 0 overfull, 0 underfull hboxes, 0 undefined references, 0 LaTeX warnings, 0 FIGSCALE. Abstract 235 words.
- Every "Online Resource 1, Fig./Table/Section S#" pointer checked against `supplement.aux`.
- Redrawn figures inspected at 140 dpi; all pages inspected as contact sheets.
- Theorem 25 packet regenerated (pp. 23–34).
- Overleaf zip compiles from an empty directory.

## SHA-256
- Capability_Exposure_Accounting_v4.1.11.pdf: 7bf6caad615563d1b933f52fbafa716b9bf97f80434a576f947103d350f9b22d
- Capability_Exposure_Accounting_v4.1.11_submission.pdf: af662c88f6c0b28cc2904d734cdf1945f68515178e791c829a407e9f123d8d34
- Capability_Exposure_Accounting_v4.1.11_Online_Resource_1.pdf: b58ab27360554830d4c072f503ec64904a3e5922c48605d5ca9c82f0efbc07f3
- manuscript/main.tex: c8aafbebe6251876290c4aaac5e0c3f86b264adfb2ee1c7e0f330d2c3b23e41e
- manuscript/supplement.tex: 6dd118a56b332f7a23830f6ae03b64693c72dad866003862aa1ccc23b9644306
- manuscript/references.bib: 7db747bedc6b30460cc0a741b6e9928123516493ec76d31f400644d03e83b57c
- THEOREM25_REVIEW_PACKET_pp23-34.pdf: 293dd0f6738ad4d2a8b2f57dbbbf3bc29dca4de8d702d30f3da0c013e2fd471d
- Dockerfile: 8d83344758ad7d72fe3592c098588e238293036b328190cded62a348b6a5eac6

Not released. Needs both authors' approval; a GitHub/Zenodo release needs an explicit request.
