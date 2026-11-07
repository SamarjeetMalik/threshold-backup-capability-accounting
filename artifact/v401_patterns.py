"""v4.0.1: the guessing space of Theorem 24 versus reachable late-exposure patterns.

A policy has G target generations published in order; index x of generation g
is delivered to slot delta(g, x), and slots may be reused across generations
(a reused bank). The adversary chooses, for every slot, an exposure time:
never, or just before publication k, or after the last publication. Exposing a
slot touches every target index delivered to it in a published generation; it
late-exposes those published before the exposure. Disclosures are omitted, as
they only add touched indices without late exposure. For each policy the check
enumerates all schedules, keeps the fresh ones (|I_g| < t_g for every g), and
verifies that every resulting pattern Lambda lies in the guessing space whose
size is L = prod_g sum_{j<t_g} C(n_g, j). It reports how many patterns are
actually reachable.
"""
from itertools import product
from math import comb
import random


def reachable_patterns(G, n, t, delta):
    slots = sorted({s for g in range(G) for s in delta[g]})
    times = list(range(G + 2))  # 0 = never; k in 1..G = before publication k; G+1 = after all
    patterns = set()
    for sched in product(times, repeat=len(slots)):
        when = dict(zip(slots, sched))
        I = [set() for _ in range(G)]
        Lam = [set() for _ in range(G)]
        for g in range(G):
            for x, s in enumerate(delta[g]):
                k = when[s]
                if k == 0:
                    continue
                I[g].add(x)
                if k > g + 1:  # exposed after generation g (published at time g+1)
                    Lam[g].add(x)
        if all(len(I[g]) < t[g] for g in range(G)):
            patterns.add(tuple(frozenset(l) for l in Lam))
    return patterns


def guessing_space_size(n, t):
    L = 1
    for ng, tg in zip(n, t):
        L *= sum(comb(ng, j) for j in range(tg))
    return L


def check(policies=300, seed=41):
    rng = random.Random(seed)
    strict, exact, total_ratio = 0, 0, []
    for _ in range(policies):
        G = rng.randint(1, 3)
        n = [rng.randint(1, 4) for _ in range(G)]
        t = [rng.randint(1, ng) for ng in n]
        pool = rng.randint(max(n), max(n) + 3)
        delta = []
        for g in range(G):
            delta.append(rng.sample(range(pool), n[g]) if rng.random() < 0.5
                         else list(range(n[g])))  # reused bank: same slot per holder
        pats = reachable_patterns(G, n, t, delta)
        L = guessing_space_size(n, t)
        for pat in pats:
            assert all(len(l) < tg and all(x < ng for x in l) for l, tg, ng in zip(pat, t, n))
        assert len(pats) <= L
        strict += len(pats) < L
        exact += len(pats) == L
        total_ratio.append(len(pats) / L)
    # a concrete reuse example: two 2-of-2 generations on the same two slots
    pats = reachable_patterns(2, [2, 2], [2, 2], [[0, 1], [0, 1]])
    return {"policies": policies, "reachable_strictly_smaller_than_L": strict,
            "reachable_equal_to_L": exact,
            "min_reachable_fraction": round(min(total_ratio), 4),
            "reuse_example": {"policy": "two 2-of-2 generations, same slots",
                              "L": guessing_space_size([2, 2], [2, 2]),
                              "reachable": len(pats)}}


if __name__ == "__main__":
    import json
    print(json.dumps(check(), indent=2))
