# Request: focused proof review of Theorem 25 (restricted-adaptive composition)

Paper: *Capability Exposure Accounting for Threshold-Based Encrypted Backup Recovery* (Malik, Singh), manuscript v4.1.9. Pages to read: `THEOREM25_REVIEW_PACKET_pp23-34.pdf` (pp. 23–34 of the submission PDF: Definitions 21–22, Lemmas 23–24, Theorem 25 and its hybrids, Corollary 26, Proposition 27). Notation is in Table 2 of the full PDF. Relative to the v4.1.8 packet (pp. 24–34), only wording changed: the paragraph on corrections to earlier versions is replaced by a paragraph on selective exposure and the separate counts, and one sentence in the G2′→G3 hop no longer names earlier versions; no statement, bound or proof step changed.

The claim is restricted-adaptive security with a guessing factor L. It is not full adaptive security. Removing L is out of scope.

| Item | Question |
|---|---|
| Definition 21 | Does the record game model adaptive exposure and target freshness correctly? |
| Definition 22 | Are the HPKE game restrictions complete: label-specific decryption exclusion, and no challenge under a corrupted key? |
| Lemma 23 | Are corruption, challenge and decryption-oracle responses simulated correctly? |
| Lemma 24 | Is the move to distinct keys justified by the stated collision event? |
| G0→G1 | Is the loss L exact for the freshness-conditioned experiment? |
| **G1→G2** | Is an eligible capsule whose slot is exposed later handled correctly? Do the stopping rule and challenge eligibility rule out corruption after a challenge? |
| **G2→G2′** | Does seed decoupling preserve the whole accepted transcript: Pedersen commitments, coordinates at touched indices, real capsules, decryption answers to modified ciphertexts, acceptance predicates and the guessed late-exposure pattern? |
| G2′→G3 | Is the HMAC-to-PRF step bounded correctly? |
| G3→G4 | Are identifier collisions kept separate from derived-key collisions? |
| G4→G5 | Are key instances, nonce uniqueness and AE query counts right? |
| Corollary 26 | Are all hybrid losses and collision terms carried through? |

The authors would most value time spent on the two bold rows. Please report any gap as a concrete step that fails, with a counter-strategy if you have one. The authors will repair the proof and every statement it affects. Otherwise the theorem stays as stated.
