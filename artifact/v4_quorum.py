"""v4 committee checks under domain-correlated corruption, plus the guessing
loss of the restricted-adaptive composition theorem (pure arithmetic).

Parties belong to administrative domains; the adversary fails up to F whole
domains (every member Byzantine). The closed form charges each committee the
sum of its F largest domain counts. It is compared with explicit enumeration
of failed-domain sets over all committees jointly.
"""
from itertools import combinations
from math import comb
from collections import Counter
import random


def holder_ok(n, f, t, c, u):
    return 2 * f + c + u + 1 <= t <= n - f - u


def approval_ok(n, f, u, k):
    return n >= 2 * f + u + k


def log_ok(n, f, u):
    return n >= 3 * f + 2 * u + 1


def check_domains(trials=3000, seed=29):
    rng = random.Random(seed)
    stats = Counter()
    for _ in range(trials):
        D = rng.randint(2, 6)
        parties = list(range(rng.randint(4, 14)))
        domain = {p: rng.randrange(D) for p in parties}
        H = rng.sample(parties, rng.randint(3, len(parties)))
        A = rng.sample(parties, rng.randint(2, len(parties)))
        L = rng.sample(parties, rng.randint(3, len(parties)))
        F, t, c, u, k = rng.randint(0, 2), rng.randint(1, len(H)), rng.randint(0, 1), 0, 1
        def count(X, failed):
            return sum(1 for p in X if domain[p] in failed)
        # enumeration: every failed-domain set of size <= F must leave all committees feasible
        enum = all(holder_ok(len(H), count(H, S), t, c, u) and approval_ok(len(A), count(A, S), u, k)
                   and log_ok(len(L), count(L, S), u)
                   for r in range(F + 1) for S in combinations(range(D), r))
        def worst(X):
            per = Counter(domain[p] for p in X)
            return sum(sorted(per.values(), reverse=True)[:F])
        closed = (holder_ok(len(H), worst(H), t, c, u) and approval_ok(len(A), worst(A), u, k)
                  and log_ok(len(L), worst(L), u))
        assert enum == closed
        stats["instances"] += 1
        stats["feasible"] += enum
    return dict(stats)


def guessing_loss(generations):
    """L = prod_g sum_{j < t_g} C(n_g, j): number of admissible late-exposure
    patterns for the target seed's generations."""
    L = 1
    for n, t in generations:
        L *= sum(comb(n, j) for j in range(t))
    return L


def loss_table():
    rows = []
    for gens in [[(3, 2)], [(5, 3)], [(7, 5)], [(10, 7)], [(5, 3), (5, 3)], [(7, 5), (7, 5), (7, 5)]]:
        rows.append({"generations": gens, "L": guessing_loss(gens)})
    return rows


if __name__ == "__main__":
    import json
    print(json.dumps({"domains": check_domains(), "guessing_loss": loss_table()}, indent=2))
