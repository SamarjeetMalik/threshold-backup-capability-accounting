"""Typed symbolic operations plus exact linear observations over a prime field.

The closure is complete only for its declared rules and linear decoders. Privacy
is checked separately: inability to linearly recover a seed is not enough.
No implementation of PKE, signatures, physical erasure, or consensus is claimed.
"""
from dataclasses import dataclass, field
from itertools import combinations


def rref(rows, p):
    a = [[x % p for x in row] for row in rows]
    if not a:
        return [], []
    pivot_cols, k = [], 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(k, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        a[k], a[pivot] = a[pivot], a[k]
        inv = pow(a[k][col], -1, p)
        a[k] = [(x * inv) % p for x in a[k]]
        for i in range(len(a)):
            if i != k:
                scale = a[i][col]
                a[i] = [(x - scale * y) % p for x, y in zip(a[i], a[k])]
        pivot_cols.append(col)
        k += 1
        if k == len(a):
            break
    return a[:k], pivot_cols


def rank(rows, p):
    return len(rref(rows, p)[1])


def in_rowspan(target, rows, p):
    return rank(rows, p) == rank(list(rows) + [list(target)], p)


def privacy_holds(rows, seed_columns, p):
    """Joint seed-value independence for Y=A*S+B*R, R uniform over F_p.

    Non-target seeds must be explicitly conditioned/subtracted or represented as
    nuisance values, not silently counted as uniformly random masking columns.
    Here seed_columns contains *all* potentially nonuniform seed coordinates.
    """
    if not rows:
        return True
    seed_columns = set(seed_columns)
    masks = [[v for j, v in enumerate(row) if j not in seed_columns] for row in rows]
    return rank(masks, p) == rank(rows, p)


@dataclass(frozen=True)
class Rule:
    premises: frozenset
    conclusion: str
    operation: str = "open"


@dataclass
class CapabilityModel:
    p: int
    variables: tuple
    seeds: dict  # epoch -> column; embedded seed values need not fill the field
    rules: list = field(default_factory=list)
    observations: dict = field(default_factory=dict)

    def add_rule(self, premises, conclusion, operation="open"):
        self.rules.append(Rule(frozenset(premises), conclusion, operation))

    def row(self, **entries):
        return tuple(entries.get(v, 0) % self.p for v in self.variables)

    def close(self, knowledge):
        known = set(knowledge)
        while True:
            before = frozenset(known)
            for rule in self.rules:
                if rule.premises <= known:
                    known.add(rule.conclusion)
            rows = self.rows(known)
            for epoch, col in self.seeds.items():
                target = [0] * len(self.variables)
                target[col] = 1
                if in_rowspan(target, rows, self.p):
                    known.add(f"seed:{epoch}")
            if frozenset(known) == before:
                return frozenset(known)

    def rows(self, known):
        rows = [row for atom, row in self.observations.items() if atom in known]
        for epoch, col in self.seeds.items():
            if f"seed:{epoch}" in known:
                unit = [0] * len(self.variables)
                unit[col] = 1
                rows.append(tuple(unit))
        return rows

    def private(self, knowledge, targets=None):
        assumed = set(knowledge)
        if targets is not None:
            assumed.update(f"seed:{e}" for e in self.seeds if e not in targets)
        known = self.close(assumed)
        rows = self.rows(known)
        if targets is None:
            return privacy_holds(rows, self.seeds.values(), self.p)
        # Protect targets conditioned on every other seed value. Subtract the
        # latter columns; treating them as uniform masks would overclaim privacy.
        cols = [i for e, i in self.seeds.items() if e not in targets]
        keep = [i for i in range(len(self.variables)) if i not in cols]
        reduced = [[row[i] for i in keep] for row in rows]
        seed_cols = [keep.index(i) for e, i in self.seeds.items() if e in targets]
        return privacy_holds(reduced, seed_cols, self.p)


def sharing_model(generations, p=101, beta=2):
    """Each item: (epoch,generation,n,threshold,bank,randomness_block).

    Equal randomness_block names intentionally correlate refreshed coefficients.
    Public commitments are represented by their stronger exponent view. This is
    appropriate for hiding checks and makes no discrete-log binding assertion.
    """
    epochs = sorted({g[0] for g in generations})
    variables = [f"S:{e}" for e in epochs]
    block_threshold = {}
    for _, _, _, t, _, block in generations:
        if block in block_threshold and block_threshold[block] != t:
            raise ValueError("A reused randomness block must have the same degree")
        block_threshold[block] = t
    for block, t in sorted(block_threshold.items()):
        variables.extend(f"a:{block}:{k}" for k in range(1, t))
        variables.extend(f"b:{block}:{k}" for k in range(t))
    seeds = {e: variables.index(f"S:{e}") for e in epochs}
    m = CapabilityModel(p, tuple(variables), seeds)
    for e, g, n, t, bank, block in generations:
        if not (0 < t <= n < p):
            raise ValueError("Need distinct nonzero indices and 1<=t<=n<p")
        published = f"published:{e}:{g}"
        for k in range(t):
            entries = {f"b:{block}:{k}": beta}
            entries[f"S:{e}" if k == 0 else f"a:{block}:{k}"] = 1
            atom = f"commit:{e}:{g}:{k}"
            m.observations[atom] = m.row(**entries)
            m.add_rule([published], atom, "public commitment")
        for holder in range(1, n + 1):
            cap = f"capsule:{e}:{g}:{holder}"
            key = f"slot:{bank}:{e}:{holder}"
            m.add_rule([published], cap, "recorded public capsule")
            m.add_rule([f"bank-copy:{bank}:{holder}"], key, "captured bank snapshot")
            pair = f"pair:{e}:{g}:{holder}"
            m.add_rule([cap, key], pair, "matching labeled decryption")
            m.add_rule([f"sender-copy:{e}:{g}:{holder}"], pair, "sender buffer")
            m.add_rule([f"response-copy:{e}:{g}:{holder}"], pair, "delivered response")
            m.add_rule([f"response-envelope:{e}:{g}:{holder}", f"response-key:{e}:{g}:{holder}"], pair, "recorded response opening")
            a = {f"S:{e}": 1}
            a.update({f"a:{block}:{k}": pow(holder, k, p) for k in range(1, t)})
            b = {f"b:{block}:{k}": pow(holder, k, p) for k in range(t)}
            for kind, entries in (("A", a), ("B", b)):
                atom = f"obs:{kind}:{e}:{g}:{holder}"
                m.observations[atom] = m.row(**entries)
                m.add_rule([pair], atom, "pair observation")
        m.add_rule([f"archive-capsule:{e}", f"archive-key:{e}"], f"seed:{e}", "archive authority")
        m.add_rule([f"client-copy:{e}"], f"seed:{e}", "reconstructed client seed")
        m.add_rule([f"seed:{e}", f"record:{e}"], f"plaintext:{e}", "data decryption")
    return m


def subsets(values):
    values = tuple(sorted(values))
    for k in range(len(values) + 1):
        yield from (frozenset(v) for v in combinations(values, k))


def bad_target(model, knowledge, target, privacy_targets):
    if privacy_targets is not None:
        return not model.private(knowledge, set(privacy_targets))
    return target in model.close(knowledge)


def minimal_witnesses(model, candidates, public, target=None, privacy_targets=None):
    witnesses = []
    for selected in subsets(candidates):
        if any(w <= selected for w in witnesses):
            continue
        if bad_target(model,public | selected,target,privacy_targets):
            witnesses.append(selected)
    return witnesses


def minimum_deletions(model, honest, immutable, public, target=None, privacy_targets=None):
    """Exact finite optimization, not a polynomial ordinary-graph min-cut."""
    answers, size = [], None
    for deleted in subsets(honest):
        if size is not None and len(deleted) > size:
            break
        if not bad_target(model,public | immutable | (honest - deleted),target,privacy_targets):
            size = len(deleted)
            answers.append(deleted)
    return answers
