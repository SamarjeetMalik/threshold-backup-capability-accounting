"""v4.0.2 checks.

1. Data-layer accounting. An executable model of the profile's client data
   interface (Store, Open) with counters for every quantity in Theorem 24:
   object-level requests, HMAC evaluations, distinct contexts, distinct AEAD
   keys, chunk encryptions and chunk decryptions. HMAC-SHA256 is real (stdlib);
   the AEAD is a counting stub, since only call counts are checked. Random
   workloads assert Q_PRF <= q + r, K <= q + r, C = sum of chunk counts, and
   D = chunk decryptions of non-honest chunks (each Open of an object decrypts
   every chunk it is given, so D can exceed r).
2. Reachable late-exposure patterns when every holder keeps one bank slot for
   all generations: the closed form sum_{j < t_min} C(n, j) G^j is compared with
   exhaustive enumeration (v401_patterns.reachable_patterns).
"""
from collections import Counter
from math import comb
import hashlib, hmac, os, random

from v401_patterns import reachable_patterns, guessing_space_size


class DataLayer:
    """Profile data layer: object key = HMAC(seed, ctx); chunk i uses nonce
    0^32 || uint64(i). One Open request names one object context and a list of
    chunk ciphertexts; it derives the key once (memoized per context) and
    calls AEAD decryption once per chunk, including chunks that fail."""
    MAX_CHUNKS = 2**32 - 1

    def __init__(self, seed, rng):
        self.seed, self.rng = seed, rng
        self.keys = {}                 # memoized ctx -> key
        self.honest = {}               # (ctx, i) -> ciphertext
        self.count = Counter()
        self.nonces = set()            # (key, nonce) pairs used for encryption

    def _key(self, ctx):
        if ctx not in self.keys:
            self.count["hmac"] += 1
            self.keys[ctx] = hmac.new(self.seed, ctx, hashlib.sha256).digest()
        return self.keys[ctx]

    def store(self, header, chunks):
        ident = self.rng.getrandbits(256).to_bytes(32, "big")   # fresh uniform identifier
        ctx = b"ctx|" + ident + b"|" + header
        assert chunks <= self.MAX_CHUNKS
        k = self._key(ctx)
        self.count["store_requests"] += 1
        for i in range(chunks):
            nonce = bytes(4) + i.to_bytes(8, "big")
            assert (k, nonce) not in self.nonces          # nonce uniqueness per key
            self.nonces.add((k, nonce))
            self.honest[(ctx, i)] = hashlib.sha256(k + nonce).digest()  # stub ciphertext
            self.count["aead_enc"] += 1
        return ctx, chunks

    def open(self, ctx, chunk_cts):
        self.count["open_requests"] += 1
        k = self._key(ctx)
        for i, ct in enumerate(chunk_cts):
            if self.honest.get((ctx, i)) == ct:
                self.count["honest_chunk_dec"] += 1    # answered from records in the proof
            else:
                self.count["aead_dec_nonhonest"] += 1  # forwarded to the AE game
        return k


def check_accounting(workloads=300, seed=53):
    rng = random.Random(seed)
    stats = Counter()
    for _ in range(workloads):
        dl = DataLayer(rng.randbytes(32), rng)
        objs = []
        for _ in range(rng.randint(1, 6)):
            objs.append(dl.store(rng.choice([b"h1", b"h2"]), rng.randint(1, 5)))
        r = 0
        nonhonest_ctx = set()
        for _ in range(rng.randint(0, 8)):
            kind = rng.random()
            if kind < 0.4:                              # honest object, honest chunks
                ctx, n = rng.choice(objs)
                dl.open(ctx, [dl.honest[(ctx, i)] for i in range(n)])
            elif kind < 0.7:                            # honest context, tampered chunks
                ctx, n = rng.choice(objs)
                dl.open(ctx, [rng.randbytes(32) for _ in range(rng.randint(1, 4))])
                r += 1
            else:                                       # adversarial new context
                ctx = b"ctx|" + rng.randbytes(32) + b"|adv"
                dl.open(ctx, [rng.randbytes(32) for _ in range(rng.randint(1, 4))])
                r += 1
                nonhonest_ctx.add(ctx)
        q = len(objs)
        assert dl.count["hmac"] <= q + r                # Q_PRF <= q + r
        assert len(dl.keys) <= q + r                    # K <= q + r
        assert dl.count["aead_enc"] == sum(n for _, n in objs)   # C counts chunks
        stats["workloads"] += 1
        stats["D_exceeds_r"] += dl.count["aead_dec_nonhonest"] > r
        stats["hmac_below_q_plus_r"] += dl.count["hmac"] < q + r
    return dict(stats)


def reuse_count(n, G, t_min):
    return sum(comb(n, j) * G**j for j in range(t_min))


def check_reuse_closed_form(cases=200, seed=59):
    rng = random.Random(seed)
    rows = []
    for _ in range(cases):
        G, n = rng.randint(1, 3), rng.randint(1, 4)
        t = [rng.randint(1, n) for _ in range(G)]
        pats = reachable_patterns(G, [n] * G, t, [list(range(n))] * G)
        assert len(pats) == reuse_count(n, G, min(t)), (n, G, t)
    # common threshold, partial publication: patterns of runs publishing only the
    # first G' generations (padded with empty sets) lie in the full-G closed-form set
    for _ in range(100):
        G, n = rng.randint(2, 3), rng.randint(1, 4)
        t = rng.randint(1, n)
        full = reachable_patterns(G, [n] * G, [t] * G, [list(range(n))] * G)
        for Gp in range(1, G):
            part = reachable_patterns(Gp, [n] * Gp, [t] * Gp, [list(range(n))] * Gp)
            for pat in part:
                assert tuple(pat) + tuple(frozenset() for _ in range(G - Gp)) in full
    for n, t, G in [(2, 2, 2), (5, 3, 2), (7, 5, 3), (10, 7, 3)]:
        rows.append({"n": n, "t": t, "G": G, "reachable": reuse_count(n, G, t),
                     "L": guessing_space_size([n] * G, [t] * G)})
    # renewed banks (disjoint slots per generation): the reachable set is all of P
    for _ in range(100):
        G, n = rng.randint(1, 2), rng.randint(1, 3)
        t = [rng.randint(1, n) for _ in range(G)]
        delta = [[g * n + x for x in range(n)] for g in range(G)]
        assert len(reachable_patterns(G, [n] * G, t, delta)) == guessing_space_size([n] * G, t)
    return {"closed_form_cases": cases, "renewed_cases": 100, "partial_publication_cases": 100, "table": rows}


if __name__ == "__main__":
    import json
    print(json.dumps({"accounting": check_accounting(), "reuse": check_reuse_closed_form()}, indent=2))
