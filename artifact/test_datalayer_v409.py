"""v4.0.9 data-layer edge cases requested in review: multi-chunk truncation,
all chunks removed, header modification, a forged final chunk in a non-final
position, concurrent Store, and the scope of the nonce guard (one DataLayer
instance only). Requires pyca/cryptography."""
import threading
import unittest

from datalayer import DataLayer, Record, AuthFailure
from test_datalayer_v404 import forge


class EdgeCaseTests(unittest.TestCase):
    def setUp(self):
        self.dl = DataLayer(bytes(range(32)))
        self.rec = self.dl.store(0, b"h", b"0123456789" * 4, chunk_size=10)   # four chunks

    def assertRejected(self, chunks, ctx=None):
        with self.assertRaises(AuthFailure):
            self.dl.open(Record(ctx or self.rec.ctx, chunks))

    def test_truncation_of_several_final_chunks(self):
        for keep in (1, 2, 3):
            self.assertRejected(self.rec.chunks[:keep])

    def test_all_chunks_removed_is_not_the_empty_object(self):
        # A legitimate empty object is one authenticated zero-length chunk with final=1.
        empty = self.dl.store(0, b"h", b"")
        self.assertEqual(len(empty.chunks), 1)
        self.assertEqual(len(empty.chunks[0]), 16)
        self.assertEqual(self.dl.open(empty), b"")
        h = self.dl.count.hmac
        self.assertRejected([])                                # non-empty object, every chunk removed
        self.assertRejected([], ctx=empty.ctx)                 # the empty object, its chunk removed
        self.assertEqual(self.dl.count.hmac, h)                # rejected before key derivation

    def test_modified_header_is_rejected(self):
        self.assertRejected(self.rec.chunks, ctx=dict(self.rec.ctx, header=b"H"))

    def test_final_chunk_forged_into_a_non_final_position(self):
        forged = forge(self.dl, self.rec.ctx, [b"x"] * 2, [False, True])[1]
        chunks = list(self.rec.chunks)
        chunks[1] = forged                                     # flag says final, position says not
        self.assertRejected(chunks)

    def test_non_final_chunk_in_final_position(self):
        chunks = self.rec.chunks[:3] + [self.rec.chunks[2]]    # last chunk replaced by a non-final one
        self.assertRejected(chunks)


class ConcurrencyAndGuardScopeTests(unittest.TestCase):
    def test_concurrent_store_never_reuses_a_key_nonce_pair(self):
        dl = DataLayer(bytes(range(32)))
        records, errors = [], []

        def worker(i):
            try:
                for j in range(5):
                    records.append((i, j, dl.store(0, b"h", bytes([i, j]) * 50, chunk_size=16)))
            except Exception as exc:                           # pragma: no cover - reported below
                errors.append(exc)

        threads = [threading.Thread(target=worker, args=(i,)) for i in range(8)]
        for t in threads:
            t.start()
        for t in threads:
            t.join()
        self.assertEqual(errors, [])
        self.assertEqual(len(records), 40)
        self.assertEqual(len(dl.used), sum(len(r.chunks) for _, _, r in records))
        for i, j, r in records:
            self.assertEqual(dl.open(r), bytes([i, j]) * 50)

    def test_guard_is_per_instance_only(self):
        # The key-byte/nonce guard lives in one DataLayer object's memory. A second
        # instance (another process, or a restart) does not see it; the proof's
        # collision term, not the guard, accounts for that case.
        same_key = lambda enc: b"K" * 32
        a = DataLayer(bytes(32), derive=same_key)
        b = DataLayer(bytes(32), derive=same_key)
        a.store(0, b"h", b"first")
        b.store(0, b"other-header", b"second")                 # not refused
        with self.assertRaises(RuntimeError):
            a.store(0, b"third", b"third")                     # refused inside one instance


if __name__ == "__main__":
    unittest.main()
