"""v4 checks: marginal versus conditional leakage, the necessity of uniform
masks, masks uniform on a subspace, and the transcript-measurability condition
of the adaptive corollary. Each claim is decided by exact enumeration.
"""
from itertools import product
from collections import Counter, defaultdict
from math import log2
import random

from capability import rank
from v3_leakage import leakage_space, joint_counts, mutual_information, random_matrix, mat_vec


def project(U, cols):
    rows = [[u[j] for j in cols] for u in U]
    return rows


def dim_span(rows, p):
    return rank(rows, p) if rows else 0


def intersect_with_coords(U, keep, k, p):
    """dim of {u in U : u_j = 0 for j not in keep}, via rank-nullity."""
    drop = [j for j in range(k) if j not in keep]
    return len(U) - dim_span(project(U, drop), p) if U else 0


def marginal_and_conditional(A, B, p, target, k):
    """Exact I(S_T;Y) and I(S_T;Y|S_K) for independent uniform seeds."""
    r = len(B[0]) if B and B[0] else 0
    full = list(product(range(p), repeat=k))
    cnt = joint_counts(A, B, p, full)
    # joint law of (S_T, Y) and (S_K, S_T, Y)
    pt = defaultdict(Counter)
    for s, c in cnt.items():
        st = tuple(s[j] for j in target)
        for y, n in c.items():
            pt[st][y] += n
    marg = mutual_information(pt)
    other = [j for j in range(k) if j not in target]
    groups = defaultdict(dict)
    for s, c in cnt.items():
        groups[tuple(s[j] for j in other)][tuple(s[j] for j in target)] = c
    cond = sum(mutual_information(g) for g in groups.values()) / len(groups)
    return marg, cond


def check_marginal_conditional(p=3, trials=1500, seed=21):
    """I(S_T;Y) = dim(U ∩ (F^T x 0)) log p and I(S_T;Y|S_K) = dim(pi_T U) log p."""
    rng = random.Random(seed)
    stats = Counter()
    for _ in range(trials):
        k, r, m = rng.randint(2, 3), rng.randint(0, 2), rng.randint(1, 3)
        A = random_matrix(m, k, p, rng)
        B = random_matrix(m, r, p, rng) if r else [[] for _ in range(m)]
        target = sorted(rng.sample(range(k), rng.randint(1, k - 1)))
        U = leakage_space(A, B, p)
        dim_marg = intersect_with_coords(U, target, k, p)
        dim_cond = dim_span(project(U, target), p)
        marg, cond = marginal_and_conditional(A, B, p, target, k)
        assert abs(marg - dim_marg * log2(p)) < 1e-9, (A, B, target)
        assert abs(cond - dim_cond * log2(p)) < 1e-9, (A, B, target)
        other = [j for j in range(k) if j not in target]
        assert len(U) == dim_cond + intersect_with_coords(U, other, k, p)  # chain rule
        stats["instances"] += 1
        stats["conditional_exceeds_marginal"] += dim_cond > dim_marg
    return {"field": p, "instances": stats["instances"],
            "conditional_strictly_larger": stats["conditional_exceeds_marginal"]}


def check_nonuniform_mask():
    """Y = S + R over F_3 with R uniform on {0,1}: rank test passes, privacy fails."""
    p = 3
    laws = {}
    for s in range(p):
        laws[s] = frozenset(((s + r) % p) for r in (0, 1))
    U = leakage_space([[1]], [[1]], p)
    return {"rank_test_private": not U, "supports_differ": len(set(laws.values())) > 1}


def check_subspace_masks(p=3, trials=1000, seed=4):
    """R uniform on a subspace spanned by the columns of C: replace B by B C."""
    rng = random.Random(seed)
    for _ in range(trials):
        k, r, m, d = rng.randint(1, 2), rng.randint(1, 3), rng.randint(1, 3), rng.randint(1, 2)
        A = random_matrix(m, k, p, rng)
        B = random_matrix(m, r, p, rng)
        C = random_matrix(r, d, p, rng)
        BC = [[sum(B[i][l] * C[l][j] for l in range(r)) % p for j in range(d)] for i in range(m)]
        full = list(product(range(p), repeat=k))
        # law of Y with R = C z, z uniform: enumerate z
        laws = set()
        for s in full:
            c = Counter()
            for z in product(range(p), repeat=d):
                rv = mat_vec(C, z, p)
                c[tuple((a + b) % p for a, b in zip(mat_vec(A, s, p), mat_vec(B, rv, p)))] += 1
            laws.add(frozenset(c.items()))
        assert (len(laws) == 1) == (not leakage_space(A, BC, p))
    return {"field": p, "instances": trials}


def check_acceptance_measurability(p=5):
    """If acceptance depends on the mask itself, not on the transcript, the
    accepted subdistribution can reveal the seed. Y = S + R, accept iff R = 0."""
    acc = {}
    for s in range(p):
        acc[s] = Counter((s + r) % p for r in range(p) if r == 0)
    transcript_measurable = {}
    for s in range(p):
        transcript_measurable[s] = Counter((s + r) % p for r in range(p) if (s + r) % p != 0)
    differ = len({frozenset(c.items()) for c in acc.values()}) > 1
    # Contrast: "accept iff Y != 0" is a function of the transcript, and the
    # translation argument gives equal accepted masses for every seed.
    equal_masses = len({sum(c.values()) for c in transcript_measurable.values()}) == 1
    return {"mask_dependent_acceptance_leaks": differ,
            "transcript_predicate_Y_nonzero_equal_masses": equal_masses}


if __name__ == "__main__":
    import json
    print(json.dumps({"marginal_conditional": check_marginal_conditional(),
                      "nonuniform_mask": check_nonuniform_mask(),
                      "subspace_masks": check_subspace_masks(),
                      "acceptance": check_acceptance_measurability()}, indent=2))
