# Revision v4.1.15 (10 November 2026)

Response to an outside review of v4.1.14 (pasted in chat, 10 Nov 2026, score 86/100). Each point was checked against the paper before acting. No theorem statement, proof or number changed; numbering unchanged (Theorem 24). Artifact v4.1.1 is unchanged.

## Acted on
- **Contribution hierarchy (review: critical).** The abstract and the introduction now name three primary contributions: (1) exposure accounting (closure, leakage subspace); (2) temporal and erasure accounting (touched indices, temporal theorem and healing, erasure complexity); (3) validation against a concrete profile (restricted-adaptive composition, TLA+ lifecycle and kernel conformance). Committee feasibility, the data layer, the worker supervisor and the measurements are listed as supporting results; the Committees row of Table 1 is marked "supporting". The introduction names the three results to read first (Theorem 3, Theorems 14-15, Theorem 24). Abstract 237 words.
- **Efficient extraction after Theorem 14 (review: high).** The review was right: the old text said an efficient adversary obtains g0^A(x) from any partial disclosure. For v = αA(x)+γB(x) with γ≠0, g0^E(x)·h0^(-v/γ) = G_x^A(x) with G_x = g0·h0^(-α/γ), a base that depends on α/γ. The paragraph now shows these group operations and claims interpolation in the exponent only when every touched index with γ≠0 shares one ratio (in particular A-only or B-only disclosures, base g0), with γ=0 indices fitting any base; for mixed ratios no efficient-extraction claim is made. The information-theoretic theorem and the conservative freshness condition of Theorem 24 are unaffected.
- **Related work (review: medium).** One sentence citing Huang, Lai, Zeng and Mu, "Receiver selective opening security for identity-based encryption in the multi-challenge setting", Des. Codes Cryptogr. 91(4):1233-1259 (2023), DOI 10.1007/s10623-022-01147-8 (verified via Crossref). The review also mentioned "2026 HIBE work"; no such paper could be found, so nothing was cited for it.
- **Editorial (review: low).** The unclosed quotation ``v2 on p. 21 is closed.

## Already addressed, no change
- **Plot of log2 L against the number of generations, reused and renewed banks (review: critical).** Table 6 lists L and log2 L (19.9 bits for three renewed 5-of-7 generations; 12.0 reused), and Fig. 7 plots L against the number of generations for the general and reused-bank counts with L = 1 for forward-ordered exposure. The paragraph "When the bound is useful" gives the bit-loss reading.
- **Formal-verification and implementation hedges (review points 4-5).** Already stated in Sections 9-11 and Online Resource 1; kept as they are.

## Checks
- Clean builds with -halt-on-error: 39 pp. (both versions), Online Resource 1 21 pp.; 0 overfull/underfull hboxes, 0 undefined references or citations in all three logs, 0 LaTeX warnings, 0 BibTeX errors, 0 FIGSCALE; no "[?" in either PDF text.
- Theorem 24 packet regenerated (page ranges asserted unchanged). Overleaf zip compiles from an empty directory.
- Previous sources: manuscript/main_v4.1.14.tex, manuscript/references_v4.1.14.bib.

## SHA-256
- Capability_Exposure_Accounting_v4.1.15.pdf: 67e6fb531125294b8c94cfb21fb77334a131f78ce3edcd6929f073dcbab7dcb0
- Capability_Exposure_Accounting_v4.1.15_submission.pdf: 26621504a54ef1c2c55a6e22bda4d24c7098c3a6f42fb8d23d76dcec18ec2975
- Capability_Exposure_Accounting_v4.1.15_Online_Resource_1.pdf: 594f2a02c84e804ac01f1ed8ab162721790b1f33a9cd89c80dfc68a669da5c7e
- Capability_Exposure_Accounting_Overleaf_v4.1.15.zip: d01b49441afc70c6f2b9c39379694c8d847dcd318d0426fdfc3c772f189ae686
- manuscript/main.tex: d95936ad252670e32dcfac7424f7c52f16d5bc7ec6c11923c54aa4e85eb37af9
- manuscript/supplement.tex: 406db6389ff18222942fae79743de10f0bfe78288919647a8e188e0b53bb68bd
- manuscript/references.bib: 7faa77aea959501aadf865b752750ecc537496c8be41fa57ba3076a694c41642
- THEOREM25_REVIEW_PACKET_pp21-28_and_OR1_pp17-21.pdf: 7ad30471390672f8416bb6c6c6bcfc7200e7ffb3c640c7123629ce153e5f85ec

Not released; superseded by v4.1.16 (REVISION_V4.1.16.md) before approval.
