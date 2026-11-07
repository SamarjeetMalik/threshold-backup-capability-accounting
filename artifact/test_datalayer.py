"""Tests for the reference data layer (requires pyca/cryptography)."""
import unittest
from dataclasses import replace

from datalayer import DataLayer, Record, AuthFailure, Interrupted
import datalayer


def seq_rng(values):
    it = iter(values)
    return lambda n: next(it)


class DataLayerTests(unittest.TestCase):
    def setUp(self):
        self.dl = DataLayer(bytes(range(32)))

    def test_roundtrip_sizes_and_chunk_counts(self):
        for size, chunk in [(0, 16), (1, 16), (16, 16), (17, 16), (1000, 64), (5000, 4096)]:
            data = bytes(i % 251 for i in range(size))
            rec = self.dl.store(0, b"h", data, chunk_size=chunk)
            self.assertEqual(len(rec.chunks), max(1, -(-size // chunk)))
            self.assertEqual(self.dl.open(rec), data)

    def test_tampered_chunk_fails_and_is_counted(self):
        rec = self.dl.store(0, b"h", b"x" * 100, chunk_size=10)
        bad = list(rec.chunks); bad[3] = bytes([bad[3][0] ^ 1]) + bad[3][1:]
        before = self.dl.count.aead_dec
        with self.assertRaises(AuthFailure):
            self.dl.open(Record(rec.ctx, bad))
        self.assertEqual(self.dl.count.aead_dec - before, 4)   # chunks 0..3 attempted
        self.assertEqual(self.dl.count.aead_dec_failed, 1)

    def test_reordered_and_cross_object_chunks_fail(self):
        a = self.dl.store(0, b"h", b"a" * 40, chunk_size=10)
        b = self.dl.store(0, b"h", b"b" * 40, chunk_size=10)
        with self.assertRaises(AuthFailure):
            self.dl.open(Record(a.ctx, [a.chunks[1], a.chunks[0]] + a.chunks[2:]))
        with self.assertRaises(AuthFailure):
            self.dl.open(Record(a.ctx, [b.chunks[0]] + a.chunks[1:]))

    def test_truncation_detected_only_with_final_flag(self):
        rec = self.dl.store(0, b"h", b"z" * 40, chunk_size=10)
        with self.assertRaises(AuthFailure):
            self.dl.open(Record(rec.ctx, rec.chunks[:2]))

        class NoFinal(DataLayer):          # the v4.0.2 profile left the AAD unspecified
            @staticmethod
            def aad(ctx, i, final):
                return datalayer.cbor({"ctx": datalayer.sha256(datalayer.cbor(ctx)).digest(), "i": i})
        weak = NoFinal(bytes(range(32)))
        rec = weak.store(0, b"h", b"z" * 40, chunk_size=10)
        self.assertEqual(weak.open(Record(rec.ctx, rec.chunks[:2])), b"z" * 20)  # silent truncation

    def test_abandoned_creation_retries_under_fresh_identifier(self):
        dl = DataLayer(bytes(32), rng=seq_rng([b"A" * 32, b"B" * 32]))
        rec = dl.store_with_retry(0, b"h", b"q" * 50, chunk_size=10, fail_after=2)
        self.assertEqual(rec.ctx["id"], b"B" * 32)
        self.assertEqual(dl.count.abandoned, 1)
        self.assertEqual(dl.count.aead_enc, 2 + 5)                 # abandoned calls count in C
        self.assertEqual(dl.open(rec), b"q" * 50)

    def test_identifier_collision_is_resampled(self):
        dl = DataLayer(bytes(32), rng=seq_rng([b"A" * 32, b"A" * 32, b"C" * 32]))
        r1 = dl.store(0, b"h", b"1")
        r2 = dl.store(0, b"h", b"2")
        self.assertNotEqual(r1.ctx["id"], r2.ctx["id"])

    def test_forced_derived_key_collision_is_caught_at_key_byte_level(self):
        dl = DataLayer(bytes(32), derive=lambda enc: b"K" * 32)   # every context, same key bytes
        dl.store(0, b"h", b"first")
        with self.assertRaises(RuntimeError):
            dl.store(0, b"h", b"second")                          # chunk 0 nonce reused under equal key

    def test_memoized_key_and_empty_open(self):
        rec = self.dl.store(0, b"h", b"m" * 30, chunk_size=10)
        h = self.dl.count.hmac
        self.dl.open(rec); self.dl.open(rec)
        self.assertEqual(self.dl.count.hmac, h)
        with self.assertRaises(AuthFailure):
            self.dl.open(Record(rec.ctx, []))
        self.assertEqual(self.dl.count.hmac, h)

    def test_counts_match_theorem_quantities(self):
        dl = DataLayer(bytes(32))
        honest = [dl.store(0, b"h", bytes(n), chunk_size=8) for n in (5, 40, 17)]
        q = len(honest)
        r = 0
        for rec in honest:                       # honest opens: no new contexts
            dl.open(rec)
        forged = Record(dl.context(0, b"evil", b"E" * 32), [b"\x00" * 24] * 3)
        for _ in range(2):                       # repeated malicious context: one derivation
            r += 1
            with self.assertRaises(AuthFailure):
                dl.open(forged)
        self.assertLessEqual(dl.count.hmac, q + r)
        self.assertEqual(len(dl.keys), q + 1)    # derived-key instances, not distinct byte values
        self.assertEqual(dl.count.aead_enc, sum(len(x.chunks) for x in honest))


if __name__ == "__main__":
    unittest.main()
