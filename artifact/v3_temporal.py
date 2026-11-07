"""v3 temporal healing classification and separated-committee feasibility.

Each healing cell is decided by the exact rank test on the Pedersen exponent
view (commitments plus every opened share/blinder coordinate), with the target
seed's privacy conditioned on every other seed. The committee check enumerates
Byzantine/offline placements explicitly instead of using the closed forms.
"""
from itertools import combinations, product
from collections import Counter

from capability import rank

P, BETA, XS = 101, 7, (1, 2, 3)


class History:
    """Epoch seeds, sharing generations, delivery banks and adversary knowledge."""

    def __init__(self, epochs):
        self.epochs = epochs
        self.columns = [("S", e) for e in range(epochs)]
        self.generations = []          # (epoch, gen_id, t, bank)
        self.copied_banks = set()      # (holder, bank) roots in adversary state
        self.responses = set()         # (holder, gen_id) pairs delivered to adversary
        self.reencrypted = {}          # gen_id -> extra bank its capsules were rewrapped under
        self.seed_disclosed = set()    # epochs whose seed was reconstructed/disclosed
        self.archive = {}              # epoch -> archive root label
        self.archive_copied = set()

    def share(self, epoch, t, bank):
        gid = len(self.generations)
        self.generations.append((epoch, gid, t, bank))
        self.columns += [("a", gid, i) for i in range(1, t)] + [("b", gid, i) for i in range(t)]
        return gid

    def col(self, key):
        return self.columns.index(key)

    def opened(self, gid):
        epoch, _, t, bank = self.generations[gid]
        banks = {bank} | ({self.reencrypted[gid]} if gid in self.reencrypted else set())
        return {h for h in XS
                if (h, gid) in self.responses or any((h, b) in self.copied_banks for b in banks)}

    def rows(self):
        width, out = len(self.columns), []
        for epoch, gid, t, bank in self.generations:
            def a_col(i):
                return self.col(("S", epoch)) if i == 0 else self.col(("a", gid, i))
            for i in range(t):  # commitment exponents a_i + beta b_i
                row = [0] * width
                row[a_col(i)] = 1
                row[self.col(("b", gid, i))] = BETA
                out.append(row)
            for h in self.opened(gid):  # an opened capsule gives both coordinates
                ra, rb = [0] * width, [0] * width
                for i in range(t):
                    ra[a_col(i)] = (ra[a_col(i)] + pow(h, i, P)) % P
                    rb[self.col(("b", gid, i))] = pow(h, i, P)
                out += [ra, rb]
        for e in self.seed_disclosed | {e for e, root in self.archive.items() if root in self.archive_copied}:
            row = [0] * width
            row[self.col(("S", e))] = 1
            out.append(row)
        return out

    def private(self, target):
        """Target seed private conditioned on all other seeds (their columns removed)."""
        keep = [j for j, c in enumerate(self.columns) if not (c[0] == "S" and c[1] != target)]
        rows = [[r[j] for j in keep] for r in self.rows()]
        tcol = keep.index(self.col(("S", target)))
        masks = [[x for j, x in enumerate(r) if j != tcol] for r in rows]
        return rank(masks, P) == rank(rows, P) if rows else True


def scenario(name, build, target, expected):
    h = build()
    got = h.private(target)
    assert got == expected, (name, got)
    return {"scenario": name, "target_private": got}


def healing_matrix():
    cells = []

    # (a) mobile pair disclosures, one per period, t = 2.
    def no_refresh():
        h = History(1); g = h.share(0, 2, "b0")
        h.responses |= {(1, g), (2, g)}; return h
    def refresh():
        h = History(1); g0 = h.share(0, 2, "b0"); h.responses.add((1, g0))
        g1 = h.share(0, 2, "b0"); h.responses.add((2, g1)); return h
    cells.append(scenario("pair disclosures, no refresh", no_refresh, 0, False))
    cells.append(scenario("pair disclosures, share refresh", refresh, 0, True))

    # (b) one copied bank root, later one response in the new generation.
    def refresh_same_bank():
        h = History(1); g0 = h.share(0, 2, "b0"); h.copied_banks.add((1, "b0"))
        g1 = h.share(0, 2, "b0"); h.responses.add((2, g1)); return h
    def refresh_new_bank():
        h = History(1); g0 = h.share(0, 2, "b0"); h.copied_banks.add((1, "b0"))
        g1 = h.share(0, 2, "b1"); h.responses.add((2, g1)); return h
    def reencrypt_only():
        h = History(1); g0 = h.share(0, 2, "b0"); h.copied_banks.add((1, "b0"))
        h.reencrypted[g0] = "b1"; h.responses.add((2, g0)); return h
    cells.append(scenario("copied bank, refresh under same bank", refresh_same_bank, 0, False))
    cells.append(scenario("copied bank, refresh under renewed bank", refresh_new_bank, 0, True))
    cells.append(scenario("copied bank, re-encrypt same generation", reencrypt_only, 0, False))

    # (c) a copied bank with two holders: fresh seeds need renewed banks.
    def fresh_seed_same_bank():
        h = History(2); h.share(0, 2, "b0"); h.copied_banks |= {(1, "b0"), (2, "b0")}
        h.share(1, 2, "b0"); return h
    def fresh_seed_new_bank():
        h = History(2); h.share(0, 2, "b0"); h.copied_banks |= {(1, "b0"), (2, "b0")}
        h.share(1, 2, "b1"); return h
    cells.append(scenario("old seed after two copied roots", fresh_seed_same_bank, 0, False))
    cells.append(scenario("fresh seed under copied bank", fresh_seed_same_bank, 1, False))
    cells.append(scenario("fresh seed under renewed bank", fresh_seed_new_bank, 1, True))

    # (d) reconstructed-seed disclosure is irreversible for that seed only.
    def seed_then_refresh():
        h = History(2); h.share(0, 2, "b0"); h.seed_disclosed.add(0)
        h.share(0, 2, "b1"); h.share(1, 2, "b1"); return h
    cells.append(scenario("disclosed seed, then refresh + renewal", seed_then_refresh, 0, False))
    cells.append(scenario("disclosed old seed, fresh seed", seed_then_refresh, 1, True))

    # (e) archive authority: renewal of the ordinary path does not revoke it.
    def archive_reused():
        h = History(2); h.share(0, 2, "b0"); h.archive = {0: "arch0", 1: "arch0"}
        h.archive_copied.add("arch0"); h.share(1, 2, "b1"); return h
    def archive_renewed():
        h = History(2); h.share(0, 2, "b0"); h.archive = {0: "arch0", 1: "arch1"}
        h.archive_copied.add("arch0"); h.share(1, 2, "b1"); return h
    cells.append(scenario("copied archive root, fresh seed same archive", archive_reused, 1, False))
    cells.append(scenario("copied archive root, fresh seed renewed archive", archive_renewed, 1, True))
    cells.append(scenario("copied archive root, old seed", archive_renewed, 0, False))
    return cells


# ---------------------------------------------------------------------------
# Committees: worst-case placements versus closed forms.

def holder_safe_by_enumeration(n, t, f, c, u, qd):
    """True iff every Byzantine/offline/copy/receipt placement leaves < t useful
    indices after a barrier with qd receipts, and the barrier and recovery are
    both reachable. Copies sit at honest erasers (a copy at a surviving honest
    index adds nothing)."""
    H = range(n)
    if t > n - f - u or qd > n - f - u:
        return False
    for byz in combinations(H, f):
        honest = [h for h in H if h not in byz]
        for off in combinations(honest, u):
            online = [h for h in honest if h not in off]
            for k in range(0, min(qd, f) + 1):  # Byzantine receipts in the quorum
                honest_receipts = qd - k
                if honest_receipts > len(online):
                    continue
                for signers in combinations(online, honest_receipts):
                    survivors = set(H) - set(signers)
                    copies = min(c, len(signers))
                    if len(survivors) + copies >= t:
                        return False
                    break  # by symmetry one signer set per (byz, off, k) suffices
    return True


def holder_closed_form(n, t, f, c, u, qd):
    return t <= n - f - u and qd <= n - f - u and qd >= n - t + f + c + 1


def check_committees():
    agree = Counter()
    for n in range(1, 9):
        for t, f, c, u, qd in product(range(1, n + 1), range(0, 3), range(0, 3), range(0, 3), range(1, n + 1)):
            if f + u > n:
                continue
            a = holder_safe_by_enumeration(n, t, f, c, u, qd)
            b = holder_closed_form(n, t, f, c, u, qd)
            if a != b:
                # only when the copy budget exceeds the honest erasers, where the
                # closed form is conservative (it charges copies that cannot exist)
                assert c > qd - f and a and not b, (n, t, f, c, u, qd, a, b)
                agree["closed_form_conservative"] += 1
            agree["configurations"] += 1
            agree["feasible"] += a
    # overlap does not couple worst cases: per-committee budgets min(f,|X|)
    rows = []
    for f, c, u, k in [(1, 0, 0, 1), (1, 1, 1, 1), (2, 1, 1, 1), (2, 2, 2, 2), (3, 1, 0, 2)]:
        nh = 3 * f + c + 2 * u + 1
        na = 2 * f + u + k
        nl = 3 * f + 2 * u + 1
        rows.append({"f": f, "c": c, "u": u, "k": k, "min_holders": nh,
                     "min_approvers": na, "min_log": nl, "shared_committee": max(nh, na, nl)})
    return {"holder_configurations": agree["configurations"],
            "holder_feasible": agree["feasible"],
            "closed_form_conservative_cases": agree["closed_form_conservative"],
            "minimum_sizes": rows}


def check_deadline(samples=((1, 2, 5, 3, 0.1, 1), (2, 1, 1, 9, 0.2, 0), (1, 1, 20, 2, 0.0, 1))):
    """Sharper serial bound 4D+C+max(H+C, hold)+P never exceeds the v2 bound."""
    out = []
    for D, C, H, tau, rho, Pw in samples:
        hold = (1 + rho) * tau / (1 - rho)
        v2 = 4 * D + 2 * C + max(H, hold) + Pw
        v3 = 4 * D + C + max(H + C, hold) + Pw
        after_approval = 4 * D + 2 * C + H + hold + Pw
        assert v3 <= v2 <= after_approval
        out.append({"D": D, "C": C, "H": H, "tau": tau, "rho": rho, "P": Pw,
                    "v2": round(v2, 6), "v3_sharper": round(v3, 6),
                    "hold_starts_after_certificate": round(after_approval, 6)})
    return out


if __name__ == "__main__":
    import json
    print(json.dumps({"healing": healing_matrix(), "committees": check_committees(),
                      "deadline": check_deadline()}, indent=2))
