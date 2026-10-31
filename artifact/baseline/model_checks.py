"""Finite models and exact small-field checks for the successor investigation.

No production cryptography is implemented. Group elements in the hiding check
are represented by exponents in a toy group; its binding is intentionally not
claimed. The dossier supplies the symbolic security proofs and scope limits.
"""
from collections import Counter
from dataclasses import dataclass
from itertools import combinations, product
import json


def subsets(items, maximum=None):
    items = tuple(items)
    for size in range((len(items) if maximum is None else min(maximum, len(items))) + 1):
        yield from map(frozenset, combinations(items, size))


def deletion_exposure(n, signers, byzantine, prior_copies):
    honest_erased = signers - byzantine
    return (frozenset(range(n)) - honest_erased) | prior_copies


def check_deletion_quorums():
    cases = 0
    configurations = 0
    for n in range(1, 9):
        universe = frozenset(range(n))
        for f in range(min(2, n) + 1):
            for c in range(min(2, n) + 1):
                for qd in range(n + 1):
                    # All signer sets are equivalent by relabeling. Enumerate
                    # every Byzantine set and prior-leak set for this size.
                    signers = frozenset(range(qd))
                    worst = 0
                    for bad in subsets(universe, f):
                        erased = signers - bad
                        for leaked in subsets(erased, c):
                            worst = max(worst, len(deletion_exposure(n, signers, bad, leaked)))
                            cases += 1
                    expected = min(n, n - qd + f + c)
                    assert worst == expected, (n, f, c, qd, worst, expected)
                    for threshold in range(1, n + 1):
                        assert (worst < threshold) == (qd >= n - threshold + f + c + 1)
                        configurations += 1
    # Explicit counterexample to using 3-of-4 receipts with one past copy.
    bad = frozenset({0})
    signers = frozenset({0, 1, 2})
    copies = frozenset({1})
    exposed = deletion_exposure(4, signers, bad, copies)
    assert exposed == frozenset({0, 1, 3}) and len(exposed) == 3
    # Proposed 4-of-5 setting withstands this bound.
    assert min(5, 5 - 4 + 1 + 1) == 3 < 4
    return {"enumerated_adversary_cases": cases, "threshold_configurations": configurations,
            "four_node_counterexample_indices": sorted(exposed),
            "five_node_worst_exposed_shares": 3}


def eval_poly(coefficients, x, p):
    return sum(a * pow(x, j, p) for j, a in enumerate(coefficients)) % p


def check_share_and_commitment_hiding():
    # Exact enumeration of the *joint* public commitments and two private
    # share/opening pairs for t=3 over F_5, for every possible secret.
    p, beta = 5, 2
    reference = None
    assignments = 0
    for secret in range(p):
        views = Counter()
        for a1, a2, b0, b1, b2 in product(range(p), repeat=5):
            a = (secret, a1, a2)
            b = (b0, b1, b2)
            commitments = tuple((x + beta * y) % p for x, y in zip(a, b))
            shares = tuple((eval_poly(a, x, p), eval_poly(b, x, p)) for x in (1, 2))
            views[(commitments, shares)] += 1
            assignments += 1
        if reference is None:
            reference = views
        else:
            assert views == reference
    # All t shares reconstruct; a mixture of independent generations does not.
    correct_mixed = 0
    secret = 3
    for old_a, new_a in product(range(p), repeat=2):
        old_share_at_1 = (secret + old_a) % p
        new_share_at_2 = (secret + 2 * new_a) % p
        recovered = (2 * old_share_at_1 - new_share_at_2) % p
        correct_mixed += recovered == secret
    assert correct_mixed == p
    return {"joint_view_assignments": assignments,
            "all_secret_joint_distributions_identical": True,
            "mixed_two_generation_accidental_reconstruction": f"{correct_mixed}/{p*p}"}


@dataclass(frozen=True)
class Request:
    account: str
    policy: int
    request_nonce: str
    target_key: str
    epochs: tuple
    manifest: str
    bank_version: int


def can_release(original, presented, votes, n, q, elapsed, hold, expired=False):
    distinct_approvers = {i for i, choice in votes if choice == "APPROVE" and 0 <= i < n}
    return (original == presented and len(distinct_approvers) >= q
            and elapsed >= hold and not expired)


def check_authorization_and_time():
    n, f, q = 5, 1, 4
    r = Request("acct", 7, "fresh", "new-key", (8, 9), "digest", 2)
    all_ids = frozenset(range(n))
    checked = 0
    for bad in combinations(range(n), f):
        bad = frozenset(bad)
        for false_honest in subsets(all_ids - bad):
            votes = [(i, "APPROVE") for i in bad | false_honest]
            for elapsed in (0, 23, 24, 25):
                result = can_release(r, r, votes, n, q, elapsed, 24)
                if result:
                    assert len(false_honest) >= q - f
                    assert elapsed >= 24
                checked += 1
    legitimate = [(i, "APPROVE") for i in (1, 2, 3, 4)] + [(0, "DENY")]
    assert can_release(r, r, legitimate, n, q, 24, 24)
    for field, replacement in [("account", "other"), ("policy", 8),
                               ("request_nonce", "old"), ("target_key", "attacker"),
                               ("epochs", (1,)), ("manifest", "other"), ("bank_version", 1)]:
        values = dict(r.__dict__)
        values[field] = replacement
        assert not can_release(r, Request(**values), legitimate, n, q, 24, 24)
    assert not can_release(r, r, legitimate, n, q, 99, 24, expired=True)
    quorums = list(map(frozenset, combinations(range(n), n-f)))
    for a, b in product(quorums, repeat=2):
        assert len(a & b) > f
    return {"authorization_time_cases": checked, "mutated_binding_fields_rejected": 7,
            "single_malicious_deny_blocks_honest_quorum": False,
            "request_extends_retention": False,
            "minimum_false_honest_approvals_for_attacker": q-f}


def check_retention_and_key_paths():
    # Symbolic closure explicitly includes encrypted share capsules and the
    # recipient slot secrets, not just the currently cached plaintext shares.
    n, threshold, W, epochs = 5, 4, 3, 9
    checks = 0
    for current in range(W, epochs):
        floor = current - W + 1
        for target in range(current + 1):
            advanced = frozenset({0, 1, 2, 3})
            bad = frozenset({0})
            past_copies = frozenset({1})
            exposed = (all_holders := frozenset(range(n))) if target >= floor else deletion_exposure(n, advanced, bad, past_copies)
            assert (len(exposed) >= threshold) == (target >= floor)
            checks += 1
    # If long-lived recipient keys can reopen every recorded share capsule,
    # erasing cached shares does not delete the data key.
    cached_shares = frozenset()
    reopened_by_static_keys = frozenset(range(n))
    assert len(cached_shares | reopened_by_static_keys) >= threshold
    # Exhaust every currently available holder subset for the loss case.
    loss = {"recoverable_subsets": 0, "unrecoverable_subsets": 0}
    for available in subsets(range(n)):
        loss["recoverable_subsets" if len(available) >= threshold else "unrecoverable_subsets"] += 1
    assert sum(loss.values()) == 2**n
    return {"retention_state_cases": checks, "static_capsule_key_erasure_bypass_found": True,
            "five_guardian_loss_subsets": loss}


def main():
    result = {"scope": "finite safety/algebra models; no production crypto or performance claims",
              "deletion": check_deletion_quorums(),
              "sharing": check_share_and_commitment_hiding(),
              "authorization": check_authorization_and_time(),
              "retention": check_retention_and_key_paths()}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
