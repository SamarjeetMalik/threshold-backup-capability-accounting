# Request: focused proof review of Theorem 24 (restricted-adaptive composition; Theorem 25 up to v4.1.11)

Paper: *Capability Exposure Accounting for Threshold-Based Encrypted Backup Recovery* (Malik, Singh), manuscript v4.1.19. Pages to read: `THEOREM25_REVIEW_PACKET_pp21-28_and_OR1_pp17-21.pdf`. Part 1 is pp. 21–28 of the submission PDF: Definitions 20–21, the statements of Lemmas 22–23, Theorem 24 with its game sequence (Fig. 6, simplified in v4.1.13) and a proof sketch, Corollary 25 and Proposition 26. Part 2 is pp. 17–21 of Online Resource 1, with the full proofs of Lemmas 22–23, Theorem 24 and Proposition 26. **Numbering changed in v4.1.12:** a proposition in Section 7 moved to the supplement, so Definitions 21–22, Lemmas 23–24, Theorem 25, Corollary 26 and Proposition 27 of earlier versions are now Definitions 20–21, Lemmas 22–23, Theorem 24, Corollary 25 and Proposition 26. The file names keep the old number. Notation is in Table 3 of the full PDF. Since v4.1.12 the full proofs are in the supplement. Their text is unchanged except that inside the proof of Theorem 24 the freshness and win events are written Fr and Win (they were F and W, which name other objects in the paper). Earlier wording changes since v4.1.8 are listed in CHANGELOG.md; no statement, bound or proof step changed.

The claim is restricted-adaptive security with a guessing factor L. It is not full adaptive security. Removing L is out of scope.

| Item | Question |
|---|---|
| Definition 20 | Does the record game model adaptive exposure and target freshness correctly? |
| Definition 21 | Are the HPKE game restrictions complete: label-specific decryption exclusion, and no challenge under a corrupted key? |
| Lemma 22 | Are corruption, challenge and decryption-oracle responses simulated correctly? |
| Lemma 23 | Is the move to distinct keys justified by the stated collision event? |
| G0→G1 | Is the loss L exact for the freshness-conditioned experiment? |
| **G1→G2** | Is an eligible capsule whose slot is exposed later handled correctly? Do the stopping rule and challenge eligibility rule out corruption after a challenge? |
| **G2→G2′** | Does seed decoupling preserve the whole accepted transcript: Pedersen commitments, coordinates at touched indices, real capsules, decryption answers to modified ciphertexts, acceptance predicates and the guessed late-exposure pattern? |
| G2′→G3 | Is the HMAC-to-PRF step bounded correctly? |
| G3→G4 | Are identifier collisions kept separate from derived-key collisions? |
| G4→G5 | Are key instances, nonce uniqueness and AE query counts right? |
| Corollary 25 | Are all hybrid losses and collision terms carried through? |

The authors would most value time spent on the two bold rows. Please report any gap as a concrete step that fails, with a counter-strategy if you have one. The authors will repair the proof and every statement it affects. Otherwise the theorem stays as stated.
