"""v3 erasure-planning checks: exact read-once evaluation versus brute force,
the failure of that evaluation under shared roots, and the vertex-cover
reduction for reused delivery credentials across generations.
"""
from itertools import combinations, product
from collections import Counter
import random

INF = float("inf")


# A formula is ("leaf", name) | ("and", [..]) | ("or", [..]) | ("thr", k, [..]).
def evaluate(f, alive):
    tag = f[0]
    if tag == "leaf":
        return f[1] in alive
    if tag == "and":
        return all(evaluate(c, alive) for c in f[1])
    if tag == "or":
        return any(evaluate(c, alive) for c in f[1])
    k, children = f[1], f[2]
    return sum(evaluate(c, alive) for c in children) >= k


def leaves(f):
    if f[0] == "leaf":
        return [f[1]]
    children = f[1] if f[0] in ("and", "or") else f[2]
    return [x for c in children for x in leaves(c)]


def dp_cost(f, weight):
    """Minimum deletion cost that falsifies f, exact when f is read-once.

    weight[x] is the deletion cost of root x; INF marks an immutable root
    (an adversary copy, a public fact or an undeletable alternate authority).
    """
    tag = f[0]
    if tag == "leaf":
        return weight[f[1]]
    if tag == "and":
        return min(dp_cost(c, weight) for c in f[1])
    if tag == "or":
        return sum(dp_cost(c, weight) for c in f[1])
    k, children = f[1], f[2]
    need = len(children) - k + 1  # children that must become false
    if need <= 0:
        return 0
    if k <= 0:
        return INF
    costs = sorted(dp_cost(c, weight) for c in children)
    return sum(costs[:need])


def brute_cost(f, weight):
    names = sorted(set(leaves(f)))
    deletable = [x for x in names if weight[x] != INF]
    best = INF
    for r in range(len(deletable) + 1):
        for D in combinations(deletable, r):
            cost = sum(weight[x] for x in D)
            if cost >= best:
                continue
            if not evaluate(f, set(names) - set(D)):
                best = cost
    return best


def random_read_once(rng, budget, counter):
    if budget <= 1 or rng.random() < 0.25:
        counter[0] += 1
        return ("leaf", f"x{counter[0]}")
    arity = rng.randint(2, min(4, budget))
    parts = [budget // arity] * arity
    children = [random_read_once(rng, max(1, b), counter) for b in parts]
    kind = rng.choice(["and", "or", "thr"])
    if kind == "thr":
        return ("thr", rng.randint(1, len(children)), children)
    return (kind, children)


def check_read_once(trials=2500, seed=3):
    rng = random.Random(seed)
    stats = Counter()
    for _ in range(trials):
        f = random_read_once(rng, rng.randint(2, 10), [0])
        names = leaves(f)
        assert len(names) == len(set(names))
        weight = {x: (INF if rng.random() < 0.15 else rng.randint(1, 5)) for x in names}
        assert dp_cost(f, weight) == brute_cost(f, weight), f
        stats["formulas"] += 1
        stats["leaves"] += len(names)
        stats["impossible"] += dp_cost(f, weight) == INF
    return {"formulas": stats["formulas"], "total_roots": stats["leaves"],
            "instances_where_erasure_impossible": stats["impossible"]}


def check_shared_roots():
    """A root reused under two conjunctions: the read-once evaluation is wrong."""
    f = ("or", [("and", [("leaf", "key"), ("leaf", "cap1")]),
                ("and", [("leaf", "key"), ("leaf", "cap2")])])
    weight = {"key": 1, "cap1": INF, "cap2": INF}
    weight_unit = {"key": 1, "cap1": 1, "cap2": 1}
    return {"formula": "OR(AND(key,cap1), AND(key,cap2)), recorded capsules immutable",
            "treewise_value": dp_cost(f, weight_unit), "true_minimum": brute_cost(f, weight_unit),
            "true_minimum_capsules_immutable": brute_cost(f, weight)}


def min_vertex_cover(n, edges):
    for r in range(n + 1):
        for S in combinations(range(n), r):
            s = set(S)
            if all(u in s or v in s for u, v in edges):
                return r
    return n


def reused_credential_instance(n, edges):
    """Holders = vertices, one reused bank root each (unit cost). Generation
    (u,v) is a 2-of-2 sharing delivered to u and v; capsules are recorded."""
    gens = [("thr", 2, [("and", [("leaf", f"bank{u}"), ("leaf", f"cap{u}_{i}")]),
                        ("and", [("leaf", f"bank{v}"), ("leaf", f"cap{v}_{i}")])])
            for i, (u, v) in enumerate(edges)]
    f = ("or", gens)
    weight = {x: (1 if x.startswith("bank") else INF) for x in leaves(f)}
    return f, weight


def check_vertex_cover_reduction(trials=300, seed=5):
    rng = random.Random(seed)
    agree = 0
    for _ in range(trials):
        n = rng.randint(2, 7)
        pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
        edges = rng.sample(pairs, rng.randint(1, len(pairs)))
        f, weight = reused_credential_instance(n, edges)
        assert brute_cost(f, weight) == min_vertex_cover(n, edges)
        agree += 1
    return {"random_graphs": agree,
            "claim": "minimum reused-bank erasure equals minimum vertex cover"}


def check_renewed_credentials(trials=300, seed=9):
    """Same sharings, but each generation delivered under a fresh bank root:
    the instance becomes read-once and the linear-time evaluation is exact."""
    rng = random.Random(seed)
    for _ in range(trials):
        n = rng.randint(2, 5)
        pairs = [(u, v) for u in range(n) for v in range(u + 1, n)]
        edges = rng.sample(pairs, rng.randint(1, min(6, len(pairs))))
        gens = [("thr", 2, [("and", [("leaf", f"bank{u}_{i}"), ("leaf", f"cap{u}_{i}")]),
                            ("and", [("leaf", f"bank{v}_{i}"), ("leaf", f"cap{v}_{i}")])])
                for i, (u, v) in enumerate(edges)]
        f = ("or", gens)
        weight = {x: (1 if x.startswith("bank") else INF) for x in leaves(f)}
        assert dp_cost(f, weight) == brute_cost(f, weight) == len(edges)
    return {"random_graphs": trials, "minimum": "one root per generation"}


if __name__ == "__main__":
    import json
    print(json.dumps({"read_once": check_read_once(), "shared_roots": check_shared_roots(),
                      "vertex_cover": check_vertex_cover_reduction(),
                      "renewed_credentials": check_renewed_credentials()}, indent=2))
