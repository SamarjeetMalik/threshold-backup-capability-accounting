"""v4 temporal checks on random finite histories.

A history has several epochs, several generations per epoch with their own
thresholds and holder sets, delivery banks drawn from a small pool (so some are
reused and some renewed), copied bank roots, partial coordinate disclosures,
whole responses, re-encryption under another bank, and occasional seed or
archive disclosure. Theorem 12's predicate (count touched indices through the
closure) is compared with the exact rank test on the Pedersen exponent view.
With independent coefficient blocks they must agree on every history; with a
reused coefficient block they need not, and the disagreements are counted.
"""
from collections import Counter
import random

from capability import rank

P, BETA = 101, 7


class Hist:
    def __init__(self, rng, correlated):
        self.rng = rng
        self.E = rng.randint(1, 3)
        self.cols = [("S", e) for e in range(self.E)]
        self.gens = []          # dict(epoch, t, holders, banks, block)
        self.copied = set()     # (holder, bank)
        self.funcs = []         # (gen, x, kind) kind in A, B, AB, E
        self.seed_routes = set()
        self.correlated = correlated
        self.reused_block = False

    def add_generation(self):
        rng = self.rng
        e = rng.randrange(self.E)
        n = rng.randint(1, 4)
        holders = sorted(rng.sample(range(1, 6), n))
        t = rng.randint(1, n)
        bank = rng.choice(["b0", "b1", "b2"])
        block = None
        if self.correlated:
            same = [g for g in self.gens if g["epoch"] == e and g["t"] == t]
            if same and rng.random() < 0.6:
                block = same[-1]["block"]
                self.reused_block = True
        gid = len(self.gens)
        if block is None:
            block = gid
            self.cols += [("a", gid, i) for i in range(1, t)] + [("b", gid, i) for i in range(t)]
        self.gens.append({"epoch": e, "t": t, "holders": holders, "banks": {bank}, "block": block})

    def step(self):
        rng = self.rng
        r = rng.random()
        if not self.gens or r < 0.3:
            self.add_generation()
        elif r < 0.45:
            self.copied.add((rng.randint(1, 5), rng.choice(["b0", "b1", "b2"])))
        elif r < 0.75:
            g = rng.randrange(len(self.gens))
            x = rng.choice(self.gens[g]["holders"])
            self.funcs.append((g, x, rng.choice(["A", "B", "AB", "E"])))
        elif r < 0.9:
            g = rng.randrange(len(self.gens))
            self.gens[g]["banks"].add(rng.choice(["b0", "b1", "b2"]))  # re-encryption
        elif r < 0.95:
            self.seed_routes.add(rng.randrange(self.E))

    def touched(self, g):
        gen = self.gens[g]
        out = {x for x in gen["holders"] if any((x, b) in self.copied for b in gen["banks"])}
        out |= {x for gg, x, kind in self.funcs if gg == g and kind != "E"}
        return out

    def predicate(self, e):
        if e in self.seed_routes:
            return False
        return all(len(self.touched(g)) < gen["t"] for g, gen in enumerate(self.gens) if gen["epoch"] == e)

    def rows(self):
        W, out = len(self.cols), []
        idx = {c: j for j, c in enumerate(self.cols)}
        def a_row(gen, x):
            row = [0] * W
            row[idx[("S", gen["epoch"])]] = 1
            for i in range(1, gen["t"]):
                row[idx[("a", gen["block"], i)]] = pow(x, i, P)
            return row
        def b_row(gen, x):
            row = [0] * W
            for i in range(gen["t"]):
                row[idx[("b", gen["block"], i)]] = pow(x, i, P)
            return row
        for g, gen in enumerate(self.gens):
            for i in range(gen["t"]):
                row = [0] * W
                row[idx[("S", gen["epoch"])] if i == 0 else idx[("a", gen["block"], i)]] = 1
                row[idx[("b", gen["block"], i)]] = BETA
                out.append(row)
            opened = {x for x in gen["holders"] if any((x, b) in self.copied for b in gen["banks"])}
            for x in opened:
                out += [a_row(gen, x), b_row(gen, x)]
        for g, x, kind in self.funcs:
            gen = self.gens[g]
            if kind in ("A", "AB"):
                out.append(a_row(gen, x))
            if kind in ("B", "AB"):
                out.append(b_row(gen, x))
            if kind == "E":
                out.append([(u + BETA * v) % P for u, v in zip(a_row(gen, x), b_row(gen, x))])
        for e in self.seed_routes:
            row = [0] * W
            row[idx[("S", e)]] = 1
            out.append(row)
        return out

    def exact_private(self, e):
        keep = [j for j, c in enumerate(self.cols) if not (c[0] == "S" and c[1] != e)]
        rows = [[r[j] for j in keep] for r in self.rows()]
        t = keep.index(self.cols.index(("S", e)))
        masks = [[v for j, v in enumerate(r) if j != t] for r in rows]
        return rank(masks, P) == rank(rows, P)


def check_random_histories(histories=3000, seed=17):
    rng = random.Random(seed)
    stats = Counter()
    for i in range(histories):
        correlated = i % 3 == 2
        h = Hist(rng, correlated)
        for _ in range(rng.randint(3, 14)):
            h.step()
        for e in range(h.E):
            pred, exact = h.predicate(e), h.exact_private(e)
            if not h.reused_block:
                assert pred == exact, (i, e)
                stats["independent_targets"] += 1
                stats["independent_private"] += exact
            else:
                stats["correlated_targets"] += 1
                stats["correlated_disagreements"] += pred != exact
                stats["correlated_pred_private_but_leaks"] += pred and not exact
    return dict(stats)


if __name__ == "__main__":
    import json
    print(json.dumps({"random_histories": check_random_histories()}, indent=2))
