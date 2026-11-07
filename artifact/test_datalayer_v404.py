"""v4.0.4 data-layer regression tests: whole-object completeness, malformed
records, aliasing and collision handling. Requires pyca/cryptography."""
import unittest

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from datalayer import DataLayer, Record, AuthFailure


def forge(dl, ctx, plaintexts, finals):
    """Encrypt chunks under the honest key with chosen final flags, as an
    insider who knows the object key could; used to test the decoder."""
    a = ChaCha20Poly1305(dl.key(ctx))
    return [a.encrypt(dl.nonce(i), p, dl.aad(ctx, i, f)) for i, (p, f) in enumerate(zip(plaintexts, finals))]


class CompletenessTests(unittest.TestCase):
    def setUp(self):
        self.dl = DataLayer(bytes(range(32)))
        self.rec = self.dl.store(0, b"h", b"0123456789" * 4, chunk_size=10)

    def assertRejected(self, chunks, ctx=None):
        with self.assertRaises(AuthFailure):
            self.dl.open(Record(ctx or self.rec.ctx, chunks))

    def test_final_chunk_deletion(self):
        self.assertRejected(self.rec.chunks[:-1])

    def test_missing_final_marker(self):
        self.assertRejected(forge(self.dl, self.rec.ctx, [b"a", b"b"], [False, False]))

    def test_duplicate_final_marker(self):
        self.assertRejected(forge(self.dl, self.rec.ctx, [b"a", b"b"], [True, True]))

    def test_chunk_after_final(self):
        extra = forge(self.dl, self.rec.ctx, [b"x"] * 5, [False] * 4 + [True])[4:]
        self.assertRejected(self.rec.chunks + extra)

    def test_duplicate_chunk_index(self):
        c = self.rec.chunks
        self.assertRejected([c[0], c[0], c[2], c[3]])

    def test_partial_failure_releases_no_plaintext(self):
        bad = list(self.rec.chunks); bad[2] = bytes(len(bad[2]))
        before = self.dl.count.aead_dec
        try:
            out = self.dl.open(Record(self.rec.ctx, bad))
        except AuthFailure:
            out = None
        self.assertIsNone(out)                         # nothing returned for chunks 0..1
        self.assertEqual(self.dl.count.aead_dec - before, 3)

    def test_empty_object_round_trip(self):
        rec = self.dl.store(0, b"h", b"")
        self.assertEqual(len(rec.chunks), 1)
        self.assertEqual(self.dl.open(rec), b"")


class MalformedAndAliasTests(unittest.TestCase):
    def setUp(self):
        self.dl = DataLayer(bytes(range(32)))
        self.rec = self.dl.store(0, b"h", b"payload")

    def test_malformed_records_rejected_before_derivation(self):
        h = self.dl.count.hmac
        cases = [Record("ctx", self.rec.chunks), Record({}, self.rec.chunks),
                 Record(dict(self.rec.ctx, epoch=True), self.rec.chunks),
                 Record(dict(self.rec.ctx, id=b"short"), self.rec.chunks),
                 Record(dict(self.rec.ctx, account="other"), self.rec.chunks),
                 Record(dict(self.rec.ctx, domain="other"), self.rec.chunks),
                 Record(self.rec.ctx, ["str"]), Record(self.rec.ctx, [b"tiny"]),
                 Record(self.rec.ctx, [])]
        for rec in cases:
            with self.assertRaises(AuthFailure):
                self.dl.open(rec)
        self.assertEqual(self.dl.count.hmac, h)

    def test_context_aliasing(self):
        ctx = dict(self.rec.ctx)
        reordered = dict(reversed(list(ctx.items())))
        self.assertEqual(self.dl.key(ctx), self.dl.key(reordered))    # canonical CBOR
        self.assertNotEqual(self.dl.key(ctx), self.dl.key(dict(ctx, epoch=1)))

    def test_identifier_retry_never_reuses_nonce(self):
        seq = iter([b"A" * 32, b"A" * 32, b"B" * 32, b"C" * 32])
        dl = DataLayer(bytes(32), rng=lambda n: next(seq))
        r1 = dl.store(0, b"h", b"1")
        r2 = dl.store_with_retry(0, b"h", b"22" * 10, chunk_size=4, fail_after=1)
        self.assertEqual((r1.ctx["id"], r2.ctx["id"]), (b"A" * 32, b"C" * 32))

    def test_nonce_reuse_under_equal_key_bytes_is_refused(self):
        dl = DataLayer(bytes(32), derive=lambda enc: b"K" * 32)
        dl.store(0, b"h", b"first")
        with self.assertRaises(RuntimeError):
            dl.store(0, b"other-header", b"second")


if __name__ == "__main__":
    unittest.main()
