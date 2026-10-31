"""Independent finite lifecycle exploration. No cryptographic security proof.

State stores adversary copies separately from honest erased state. Capsules are
symbolic authenticated encryptions: possession of the matching slot opens them.
Exploration abstracts one immutable epoch, one fixed Byzantine identity, and at
most one copy/erase operation per honest identity. See README.md for exclusions.
"""
from collections import deque
from dataclasses import dataclass
from itertools import combinations, product
import json


def bits(mask, n):
    return [i for i in range(n) if mask & (1 << i)]


def explore(n, t, qd, copy_budget):
    # Identity 0 can sign a false receipt at any time; it never actually erases.
    # A state represents every prefix in the quotient graph, not just end sets.
    start = (0, 0)  # erased honest paths, irrevocable adversary copies
    queue = deque([start])
    paths = {start: []}
    edges = barriers = 0
    violations = []
    universe = (1 << n) - 1
    while queue:
        erased, copied = state = queue.popleft()
        useful = (universe ^ erased) | copied
        if erased.bit_count() + 1 >= qd:
            barriers += 1
            if useful.bit_count() >= t:
                violations.append({"trace": paths[state] + ["false receipt by 0; commit barrier; snapshot remaining slots"],
                                   "erased": bits(erased, n), "copies": bits(copied, n),
                                   "useful_indices": bits(useful, n)})
        successors = []
        for i in range(1, n):
            bit = 1 << i
            if not erased & bit:
                successors.append(((erased | bit, copied), f"erase({i})"))
                if not copied & bit and copied.bit_count() < copy_budget:
                    successors.append(((erased, copied | bit), f"copy_slot({i}); release device; retain adversary copy"))
        for new, label in successors:
            edges += 1
            assert new[1] | copied == new[1], "Attacker memory must be monotone"
            if new not in paths:
                paths[new] = paths[state] + [label]
                queue.append(new)
    return {"n": n, "t": t, "qd": qd, "copy_budget": copy_budget,
            "states": len(paths), "transitions": edges, "barrier_states": barriers,
            "unsafe_barrier_states": len(violations),
            "shortest_counterexample": violations[0] if violations else None}


def polynomial(secret, coeff, x, p=101):
    return (secret + sum(a * pow(x, j + 1, p) for j, a in enumerate(coeff))) % p


def reconstruct(points, p=101):
    result = 0
    for x, y in points:
        weight = 1
        for z, _ in points:
            if z != x:
                weight = weight * (-z) * pow(x - z, -1, p) % p
        result = (result + weight * y) % p
    return result


@dataclass
class CapsuleWorld:
    n: int = 5
    t: int = 4
    generation: int = 0
    # Known slots do not disappear when the corresponding honest slot is erased.
    known_slots: set = None
    pairs: dict = None
    secrets: dict = None

    def __post_init__(self):
        self.known_slots = set()
        self.pairs = {}
        self.secrets = {}

    def share(self, secret, coefficients, bank="original"):
        g = self.generation
        self.generation += 1
        self.secrets[g] = secret
        for h in range(1, self.n + 1):
            self.pairs[g, h] = (bank, polynomial(secret, coefficients, h))
        return g

    def copy_slot(self, holder, bank="original"):
        self.known_slots.add((bank, holder))

    def open_generation(self, generation):
        return [(h, y) for (g, h), (bank, y) in self.pairs.items()
                if g == generation and (bank, h) in self.known_slots]


def capsule_attacks():
    w = CapsuleWorld()
    old = w.share(42, (7, 13, 29))
    # Only one currently controlled identity at each step. All copies persist.
    sequential = []
    for h in (1, 2, 3, 4):
        w.copy_slot(h)
        sequential.append({"active_corruptions": 1, "holder": h,
                           "retained_slot_copies": len(w.known_slots)})
    assert reconstruct(w.open_generation(old)) == 42
    refreshed = w.share(42, (5, 17, 31))
    assert reconstruct(w.open_generation(refreshed)) == 42
    future_same_bank = w.share(67, (11, 19, 37))
    assert reconstruct(w.open_generation(future_same_bank)) == 67
    fresh_bank = w.share(81, (3, 23, 41), bank="clean")
    assert len(w.open_generation(fresh_bank)) == 0
    # New banks do not remove the recorded old capsules or their stolen keys.
    assert reconstruct(w.open_generation(old)) == 42
    return {"mobile_trace": sequential, "old_secret_recovered": 42,
            "same_slot_refresh_secret_recovered": 42,
            "independent_future_secret_under_stolen_bank_recovered": 67,
            "fresh_bank_exposed_shares": 0,
            "old_secret_still_recovered_after_bank_replacement": 42}


def rank(matrix, p=101):
    a = [list(row) for row in matrix]
    if not a:
        return 0
    r = 0
    for col in range(len(a[0])):
        pivot = next((j for j in range(r, len(a)) if a[j][col] % p), None)
        if pivot is None:
            continue
        a[r], a[pivot] = a[pivot], a[r]
        inv = pow(a[r][col], -1, p)
        a[r] = [x * inv % p for x in a[r]]
        for j in range(len(a)):
            if j != r:
                scale = a[j][col]
                a[j] = [(x - scale * y) % p for x, y in zip(a[j], a[r])]
        r += 1
        if r == len(a):
            break
    return r


def refresh_linear_views():
    # Exact rank criterion for uniform independent polynomial coefficients.
    # S is hidden iff the S column lies in the span of random-coefficient columns.
    n, t, generations = 4, 3, 2
    subsets = [c for k in range(t) for c in combinations(range(1, n + 1), k)]
    checked = 0
    for exposure in product(subsets, repeat=generations):
        rows = []
        for g, indices in enumerate(exposure):
            for x in indices:
                row = [1] + [0] * (generations * (t - 1))
                for degree in range(1, t):
                    row[1 + g * (t - 1) + degree - 1] = pow(x, degree, 101)
                rows.append(row)
        assert rank(rows) == rank([r[1:] for r in rows])
        checked += 1
    return {"field": 101, "n": n, "t": t, "generations": generations,
            "exposure_set_pairs": checked, "all_sharing_views_hide_secret": True,
            "excludes": "recipient slots, commitments, malicious refresh, transitions, reconstructor compromise"}


def availability():
    result = []
    for n, t in ((4, 3), (5, 4)):
        counts = {}
        for mask in range(1 << n):
            available = mask.bit_count()
            counts[str(available)] = counts.get(str(available), 0) + 1
        result.append({"n": n, "t": t, "all_survivor_subsets": counts,
                       "recoverable_subset_count": sum(v for k, v in counts.items() if int(k) >= t),
                       "one_byzantine_withholds_plus_one_honest_offline": n - 2 >= t})
    return result


def authorization_traces():
    # Lifecycle trace witnesses, rather than a statistical model for humans.
    genuine_false_signers = {0, 1, 2, 3}
    attacker_receiver = "attacker"
    elapsed, hold, now, expiry = 24, 24, 24, 25
    release = len(genuine_false_signers) >= 4 and elapsed >= hold and now < expiry
    assert release and attacker_receiver == "attacker"
    # A request with insufficient expiry slack fails even with every approval.
    request_started, expiry = 10, 20
    assert request_started + hold >= expiry
    # Witness for an unsafe implementation refinement, NOT a base-protocol break.
    unsafe_trace = ["check SEALED and unexpired", "decrypt into queued response",
                    "Expire; erase slot; sign receipt", "send stale queued response"]
    return {"genuine_false_quorum_releases_after_hold": release,
            "honest_false_approvals_needed_with_one_byzantine": 3,
            "hold_outlasts_retention_causes_unrecoverable_request": True,
            "atomicity_obligation_witness": unsafe_trace,
            "witness_scope": "unsafe refinement if Expire does not cancel every queued buffer; dossier requires cleanup"}


def main():
    result = {"scope": "finite quotient-state exploration, symbolic slot closure, exact finite-field rank checks",
              "deletion_exploration": [explore(4, 3, 3, 1), explore(5, 4, 4, 1), explore(5, 4, 4, 2)],
              "capsule_attacks": capsule_attacks(), "refresh": refresh_linear_views(),
              "availability": availability(), "authorization": authorization_traces()}
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
