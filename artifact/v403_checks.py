"""v4.0.3 checks: the exact reused-bank pattern count with unequal thresholds
and partial publication, versus exhaustive enumeration.

With one reused slot per holder, a holder's exposure is a level l_x in
{0..G'} where G' is the number of published generations. A pattern is
realizable iff the set J of holders with l_x >= 1 satisfies
|J| < tau_m := min_{g <= m} t_g for m = max_x l_x (publishing more generations
only tightens the condition). The count is therefore
    1 + sum_{m=1}^{G} sum_{j=1}^{tau_m - 1} C(n, j) (m^j - (m-1)^j),
which telescopes to sum_{j < t} C(n, j) G^j under a common threshold t.
"""
from itertools import product
from math import comb
import random

from v401_patterns import reachable_patterns


def reachable_partial(G, n, t):
    """All patterns of fresh runs publishing any prefix of the G generations."""
    pats = {tuple(frozenset() for _ in range(G))}
    for Gp in range(1, G + 1):
        for pat in reachable_patterns(Gp, [n] * Gp, t[:Gp], [list(range(n))] * Gp):
            pats.add(tuple(pat) + tuple(frozenset() for _ in range(G - Gp)))
    return pats


def exact_count(n, t):
    G = len(t)
    total = 1
    for m in range(1, G + 1):
        tau = min(t[:m])
        for j in range(1, tau):
            total += comb(n, j) * (m**j - (m - 1)**j)
    return total


def check(cases=300, seed=61):
    rng = random.Random(seed)
    unequal = 0
    for _ in range(cases):
        G, n = rng.randint(1, 3), rng.randint(1, 4)
        t = [rng.randint(1, n) for _ in range(G)]
        assert len(reachable_partial(G, n, t)) == exact_count(n, t), (n, t)
        unequal += len(set(t)) > 1
    # telescoping check against the v4.0.2 closed form for a common threshold
    for n in range(1, 8):
        for t in range(1, n + 1):
            for G in range(1, 5):
                assert exact_count(n, [t] * G) == sum(comb(n, j) * G**j for j in range(t))
    example = {"n": 5, "t": [4, 2, 2], "partial_publication_exact": exact_count(5, [4, 2, 2]),
               "v4.0.2_all_published_t_min": sum(comb(5, j) * 3**j for j in range(2))}
    return {"cases": cases, "unequal_threshold_cases": unequal, "example": example}


if __name__ == "__main__":
    import json
    print(json.dumps(check(), indent=2))
