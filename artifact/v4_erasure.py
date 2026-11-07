"""v4 erasure checks: linear-time selection at threshold gates, weighted
thresholds (subset-sum hardness, pseudo-polynomial DP), and the type-enumeration
algorithm for a fixed number of generations with reused per-holder roots.
"""
from itertools import combinations, product
from collections import Counter
import random

from v3_erasure import INF, evaluate, leaves, dp_cost, brute_cost, random_read_once


def select_smallest_sum(values, need):
    """Sum of the `need` smallest values in expected linear time (quickselect),
    without sorting. Deterministic BFPRT selection gives worst-case O(m)."""
    vals = list(values)
    if need <= 0:
        return 0
    if need >= len(vals):
        return sum(vals)
    total, rng = 0, random.Random(len(vals) * 7919 + need)
    while True:
        pivot = vals[rng.randrange(len(vals))]
        lo = [v for v in vals if v < pivot]
        eq = [v for v in vals if v == pivot]
        hi = [v for v in vals if v > pivot]
        if need <= len(lo):
            vals = lo
        elif need <= len(lo) + len(eq):
            return total + sum(lo) + pivot * (need - len(lo))
        else:
            total += sum(lo) + pivot * len(eq)
            need -= len(lo) + len(eq)
            vals = hi


def dp_select(f, weight):
    tag = f[0]
    if tag == "leaf":
        return weight[f[1]]
    if tag == "and":
        return min(dp_select(c, weight) for c in f[1])
    if tag == "or":
        return sum(dp_select(c, weight) for c in f[1])
    k, children = f[1], f[2]
    need = len(children) - k + 1
    if need <= 0:
        return 0
    if k <= 0:
        return INF
    return select_smallest_sum([dp_select(c, weight) for c in children], need)


def check_selection(trials=2500, seed=3):
    rng = random.Random(seed)
    for _ in range(trials):
        f = random_read_once(rng, rng.randint(2, 14), [0])
        weight = {x: (INF if rng.random() < 0.15 else rng.randint(0, 5)) for x in leaves(f)}
        assert dp_select(f, weight) == dp_cost(f, weight)
    return {"formulas": trials, "agrees_with_sorting_recurrence": True}


def weighted_threshold_min(items, k):
    """Min deletion cost so that the surviving weight of a weighted THR_k gate is
    < k. items = [(weight, cost)]. Pseudo-polynomial DP over removed weight."""
    W = sum(w for w, _ in items)
    need = W - k + 1  # weight that must be removed
    if need <= 0:
        return 0
    best = [INF] * (need + 1)
    best[0] = 0
    for w, c in items:
        for x in range(need, -1, -1):
            if best[x] < INF:
                y = min(need, x + w)
                best[y] = min(best[y], best[x] + c)
    return best[need]


def check_weighted_threshold(trials=2000, seed=8):
    rng = random.Random(seed)
    for _ in range(trials):
        m = rng.randint(1, 7)
        items = [(rng.randint(1, 6), rng.randint(0, 6) if rng.random() > 0.1 else INF) for _ in range(m)]
        k = rng.randint(1, sum(w for w, _ in items) + 1)
        brute = INF
        for r in range(m + 1):
            for D in combinations(range(m), r):
                if sum(items[i][0] for i in range(m) if i not in D) < k:
                    brute = min(brute, sum(items[i][1] for i in D))
        assert weighted_threshold_min(items, k) == brute
    # subset-sum gadget: cost = weight, so the optimum is the smallest subset sum >= need
    items = [(3, 3), (5, 5), (7, 7)]
    k = sum(w for w, _ in items) - 8 + 1  # need = 8: hits exactly 3+5
    return {"instances": trials, "subset_sum_gadget_optimum": weighted_threshold_min(items, k)}


def fixed_generation_algorithm(costs, member, demand):
    """Reused per-holder roots, G generations of one seed. Holder h has root cost
    costs[h] (INF = immutable copy) and membership set member[h] of generations.
    Generation g leaks unless at least demand[g] of its holders lose their roots.
    Enumerate how many holders of each membership type to delete; within a type
    the cheapest are optimal. Time (n+1)^(number of types) <= (n+1)^(2^G)."""
    types = {}
    for h, m in member.items():
        types.setdefault(frozenset(m), []).append(costs[h])
    keys = list(types)
    prefix = {}
    for key in keys:
        cs = sorted(types[key])
        acc, sums = 0, [0]
        for c in cs:
            acc += c
            sums.append(acc)
        prefix[key] = sums
    best = INF
    for counts in product(*[range(len(types[key]) + 1) for key in keys]):
        if all(sum(c for key, c in zip(keys, counts) if g in key) >= d for g, d in demand.items()):
            best = min(best, sum(prefix[key][c] for key, c in zip(keys, counts)))
    return best


def check_fixed_generations(trials=400, seed=13):
    rng = random.Random(seed)
    stats = Counter()
    for _ in range(trials):
        n, G = rng.randint(2, 7), rng.randint(1, 3)
        member = {h: set() for h in range(n)}
        demand = {}
        for g in range(G):
            H = rng.sample(range(n), rng.randint(1, n))
            for h in H:
                member[h].add(g)
            t = rng.randint(1, len(H))
            demand[g] = len(H) - t + 1
        costs = {h: (INF if rng.random() < 0.15 else rng.randint(1, 5)) for h in range(n)}
        brute = INF
        for r in range(n + 1):
            for D in combinations(range(n), r):
                if all(sum(1 for h in D if g in member[h]) >= d for g, d in demand.items()):
                    brute = min(brute, sum(costs[h] for h in D))
        assert fixed_generation_algorithm(costs, member, demand) == brute
        stats["instances"] += 1
        stats["impossible"] += brute == INF
    return {"instances": stats["instances"], "impossible": stats["impossible"]}


if __name__ == "__main__":
    import json
    print(json.dumps({"selection": check_selection(),
                      "weighted_threshold": check_weighted_threshold(),
                      "fixed_generations": check_fixed_generations()}, indent=2))
