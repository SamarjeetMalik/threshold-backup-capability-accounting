"""v3 checks for the leakage-subspace theorem and the corrected generation theorem.

Every claim is decided twice: once by the linear-algebra criterion stated in the
paper and once by direct enumeration of the joint distribution of (S, Y). All
fields are tiny so the enumeration is exhaustive, not sampled.
"""
from itertools import product, combinations
from math import log2
from collections import Counter, defaultdict
import random

from capability import rank, in_rowspan


def mat_vec(M, v, p):
    return tuple(sum(a * b for a, b in zip(row, v)) % p for row in M)


def leakage_space(A, B, p):
    """Basis of U = {lam A : lam B = 0}, by elimination on [B | A]."""
    m = len(A)
    if m == 0:
        return []
    k, r = len(A[0]), len(B[0]) if B and B[0] else 0
    # rows of [B A]; eliminate the B part, keep rows whose B part vanished
    rows = [list(B[i]) + list(A[i]) for i in range(m)]
    rows = [[x % p for x in row] for row in rows]
    lead = 0
    for col in range(r):
        piv = next((i for i in range(lead, m) if rows[i][col]), None)
        if piv is None:
            continue
        rows[lead], rows[piv] = rows[piv], rows[lead]
        inv = pow(rows[lead][col], -1, p)
        rows[lead] = [(x * inv) % p for x in rows[lead]]
        for i in range(m):
            if i != lead and rows[i][col]:
                s = rows[i][col]
                rows[i] = [(x - s * y) % p for x, y in zip(rows[i], rows[lead])]
        lead += 1
    tail = [row[r:] for row in rows[lead:]]
    basis = []
    for row in tail:
        if rank(basis + [row], p) > len(basis):
            basis.append(row)
    return basis


def joint_counts(A, B, p, domain):
    """Exact counts N[s][y] over uniform masks for every s in the domain."""
    r = len(B[0]) if B and B[0] else 0
    out = {}
    for s in domain:
        c = Counter()
        As = mat_vec(A, s, p)
        for rv in product(range(p), repeat=r):
            Br = mat_vec(B, rv, p) if r else tuple(0 for _ in A)
            c[tuple((a + b) % p for a, b in zip(As, Br))] += 1
        out[s] = c
    return out


def mutual_information(counts):
    """I(S;Y) in bits for uniform S on the given domain."""
    ns = len(counts)
    py = Counter()
    for c in counts.values():
        tot = sum(c.values())
        for y, n in c.items():
            py[y] += n / tot / ns
    info = 0.0
    for c in counts.values():
        tot = sum(c.values())
        for y, n in c.items():
            pyx = n / tot
            info += pyx / ns * log2(pyx / py[y])
    return info


def independent(counts):
    vals = [frozenset((y, n * 1.0 / sum(c.values())) for y, n in c.items()) for c in counts.values()]
    return len(set(vals)) == 1


def determines(counts, coordinate):
    seen = defaultdict(set)
    for s, c in counts.items():
        for y in c:
            seen[y].add(s[coordinate])
    return all(len(v) == 1 for v in seen.values())


def random_matrix(rows, cols, p, rng):
    return [[rng.randrange(p) for _ in range(cols)] for _ in range(rows)]


def check_leakage_theorem(p=3, trials=4000, seed=7):
    """Theorem (leakage subspace): dim U = rank[A B]-rank B = I(S;Y)/log p for
    uniform S; S_i determined by Y (any decoder) iff e_i in U on the full domain;
    on an arbitrary domain D, Y independent of S iff U (s-s') = 0 on D."""
    rng = random.Random(seed)
    stats = Counter()
    nonlinear_example = None
    nonproduct_example = None
    for _ in range(trials):
        k, r, m = rng.randint(1, 2), rng.randint(0, 2), rng.randint(1, 3)
        A = random_matrix(m, k, p, rng)
        B = random_matrix(m, r, p, rng) if r else [[] for _ in range(m)]
        U = leakage_space(A, B, p)
        rAB = rank([a + b for a, b in zip(A, B)], p)
        rB = rank(B, p) if r else 0
        assert len(U) == rAB - rB
        full = list(product(range(p), repeat=k))
        counts = joint_counts(A, B, p, full)
        mi = mutual_information(counts)
        assert abs(mi - len(U) * log2(p)) < 1e-9, (A, B, mi, U)
        for i in range(k):
            unit = [1 if j == i else 0 for j in range(k)]
            in_u = bool(U) and in_rowspan(unit, U, p)
            assert determines(counts, i) == in_u
            v2 = in_rowspan(unit + [0] * r, [a + b for a, b in zip(A, B)], p)
            assert v2 == in_u  # the dimensionally precise v2 target vector
        stats["full_domain"] += 1
        # arbitrary (generally non-product) domains of size >= 2
        dom = rng.sample(full, rng.randint(2, len(full))) if len(full) > 1 else full
        dcounts = {s: counts[s] for s in dom}
        pred = all(all(sum(u[j] * ((s[j] - dom[0][j]) % p) for j in range(k)) % p == 0
                       for u in U) for s in dom)
        assert independent(dcounts) == pred
        stats["arbitrary_domain"] += 1
        if pred and U and nonproduct_example is None:
            nonproduct_example = {"A": A, "B": B, "domain": dom}
    # nonlinear decoding on a restricted product domain: Y = S0 + 2 S1 over F5
    A, B, p5 = [[1, 2]], [[]], 5
    dom = list(product(range(2), repeat=2))
    c = joint_counts(A, B, p5, dom)
    U = leakage_space(A, B, p5)
    nonlinear_example = {"A": A, "p": 5, "domain": "{0,1}^2",
                         "S0_determined": determines(c, 0),
                         "e0_in_U": in_rowspan([1, 0], U, p5)}
    assert nonlinear_example["S0_determined"] and not nonlinear_example["e0_in_U"]
    return {"field": p, "random_instances": stats["full_domain"],
            "arbitrary_domain_instances": stats["arbitrary_domain"],
            "nonproduct_private_despite_rank_failure": nonproduct_example,
            "nonlinear_decoding_on_restricted_domain": nonlinear_example}


# ---------------------------------------------------------------------------
# Corrected joint generation theorem: Pedersen exponent view, partial openings.

def generation_rows(t, xs, disclosures, beta, p, seed_col=0, offset=1):
    """Rows over (S, a_1..a_{t-1}, b_0..b_{t-1}) for one generation.

    disclosures maps x -> tuple of functionals among 'A','B','E' (E = A+beta B,
    which the commitments already reveal), or ('sum', x2) handled by caller.
    Returns rows with columns [S | a_1..a_{t-1} | b_0..b_{t-1}] for this block.
    """
    width = 1 + (t - 1) + t
    rows = []
    # commitment exponents a_i + beta b_i, i = 0..t-1 (a_0 = S)
    for i in range(t):
        row = [0] * width
        row[0 if i == 0 else i] = 1
        row[t + i] = beta % p
        rows.append(row)

    def a_row(x):
        row = [0] * width
        row[0] = 1
        for i in range(1, t):
            row[i] = pow(x, i, p)
        return row

    def b_row(x):
        row = [0] * width
        for i in range(t):
            row[t + i] = pow(x, i, p)
        return row

    for x, kinds in disclosures.items():
        for kind in kinds:
            if kind == "A":
                rows.append(a_row(x))
            elif kind == "B":
                rows.append(b_row(x))
            elif kind == "E":
                rows.append([(u + beta * v) % p for u, v in zip(a_row(x), b_row(x))])
    return rows, a_row, b_row


def block_private(rows, p):
    """Privacy of the single seed column 0 against uniform coefficient columns."""
    masks = [row[1:] for row in rows]
    return rank(masks, p) == rank(rows, p)


def check_partial_openings(p=11, beta=3):
    kinds = [(), ("A",), ("B",), ("A", "B"), ("E",)]
    results = Counter()
    for t in (1, 2, 3):
        xs = [1, 2, 3]
        for pattern in product(range(len(kinds)), repeat=len(xs)):
            disc = {x: kinds[c] for x, c in zip(xs, pattern) if kinds[c]}
            rows, _, _ = generation_rows(t, xs, disc, beta, p)
            private = block_private(rows, p)
            v2_pairs = sum(1 for x, c in disc.items() if set(c) == {"A", "B"})
            v3_indices = sum(1 for x, c in disc.items() if set(c) - {"E"})
            assert private == (v3_indices < t), (t, disc)
            results["patterns"] += 1
            if private != (v2_pairs < t):
                results["v2_pair_count_wrong"] += 1
    # the concrete counterexample quoted in the paper
    rows, _, _ = generation_rows(2, [1, 2], {1: ("B",), 2: ("A",)}, beta, p)
    witness = {"t": 2, "disclosed": "B(x1) only, A(x2) only", "complete_pairs": 0,
               "private": block_private(rows, p)}
    assert witness["private"] is False
    # aggregated response: A(x1)+A(x2) touches two indices yet stays private
    rows, a_row, _ = generation_rows(2, [1, 2], {}, beta, p)
    rows.append([(u + v) % p for u, v in zip(a_row(1), a_row(2))])
    aggregate = {"t": 2, "disclosed": "A(x1)+A(x2)", "touched_indices": 2,
                 "private": block_private(rows, p)}
    assert aggregate["private"] is True
    return {"field": p, "beta": beta, "patterns": results["patterns"],
            "patterns_where_v2_pair_count_mispredicts": results["v2_pair_count_wrong"],
            "half_opening_counterexample": witness,
            "aggregate_response_is_not_index_countable": aggregate}


def block_diag(blocks):
    width = sum(len(b[0]) for b in blocks)
    rows, off = [], 0
    for b in blocks:
        w = len(b[0])
        for row in b:
            rows.append([0] * off + list(row) + [0] * (width - off - w))
        off += w
    return rows


def check_block_lemma(p=3, trials=3000, seed=11):
    """Independent mask blocks: joint privacy == AND of blockwise privacy;
    joint leakage space == sum of blockwise leakage spaces."""
    rng = random.Random(seed)
    stats = Counter()
    for _ in range(trials):
        k = rng.randint(1, 3)
        G = rng.randint(2, 3)
        As, Bs = [], []
        for _ in range(G):
            m, r = rng.randint(1, 2), rng.randint(1, 2)
            As.append(random_matrix(m, k, p, rng))
            Bs.append(random_matrix(m, r, p, rng))
        A = [row for a in As for row in a]
        B = block_diag(Bs)
        U = leakage_space(A, B, p)
        Us = [leakage_space(a, b, p) for a, b in zip(As, Bs)]
        joint_private = not U
        assert joint_private == all(not u for u in Us)
        summed = [row for u in Us for row in u]
        assert len(U) == rank(summed, p) if summed else len(U) == 0
        if summed:
            assert all(in_rowspan(row, U, p) for row in summed)
        for i in range(k):
            unit = [1 if j == i else 0 for j in range(k)]
            joint = bool(U) and in_rowspan(unit, U, p)
            local = any(u and in_rowspan(unit, u, p) for u in Us)
            if joint and not local:
                stats["joint_only_reconstruction"] += 1
        stats["instances"] += 1
    # two-seed example: generation 1 leaks S0+S1, generation 2 leaks S0-S1
    example = {"generation_1": "S0+S1", "generation_2": "S0-S1 (p=3)",
               "S0_from_one_generation": in_rowspan([1, 0], [[1, 1]], 3)
               or in_rowspan([1, 0], [[1, 2]], 3),
               "S0_from_both": in_rowspan([1, 0], [[1, 1], [1, 2]], 3)}
    assert example["S0_from_both"] and not example["S0_from_one_generation"]
    return {"field": p, "instances": stats["instances"],
            "joint_only_reconstruction_cases": stats["joint_only_reconstruction"],
            "two_seed_example": example}


if __name__ == "__main__":
    import json
    print(json.dumps({"leakage": check_leakage_theorem(),
                      "partial_openings": check_partial_openings(),
                      "block_lemma": check_block_lemma()}, indent=2))
