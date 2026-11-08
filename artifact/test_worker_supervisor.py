"""v4.1.0 tests for process-isolated decryption workers: normal completion, a
hung worker blocking the receipt, forced termination, a crashing worker, a
stale completion after termination, and a kernel crash and restart.
Requires pyca/cryptography."""
import unittest

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

import lifecycle_kernel as kernel
from worker_supervisor import WorkerSupervisor, aead_open, hang, crash

KEY = (0, 0)


class Clock:
    def __init__(self): self.now = 0
    def __call__(self): return self.now


def prepared():
    c = Clock(); k = kernel.ReferenceKernel(epoch_keys=(KEY,), clock=c)
    r = kernel.Request("acct", "r", 0, 0, 0, b"recipient", b"manifest")
    k.register(r); k.authorize("r", kernel.Certificate(r.digest, (1, 2), 0)); c.now = 24
    return k, WorkerSupervisor(k)


def expire_and_erase(k):
    k.begin_expiry(KEY); k.erase_slot(KEY)


class SupervisorTests(unittest.TestCase):
    def test_normal_completion_delivers_the_decryption(self):
        k, s = prepared()
        key, nonce = bytes(range(32)), bytes(12)
        ct = ChaCha20Poly1305(key).encrypt(nonce, b"pair-bytes", b"ad")
        tok = s.start("r", aead_open, key, nonce, ct, b"ad")
        self.assertTrue(s.collect(tok, timeout=30))
        self.assertEqual(k.jobs["r"].stage, "queued")
        self.assertEqual(bytes(k.jobs["r"].buffer), b"pair-bytes")
        self.assertEqual(s.exitcodes[tok], 0)

    def test_hung_worker_blocks_receipt_until_terminated(self):
        k, s = prepared()
        tok = s.start("r", hang)
        self.assertIsNone(s.collect(tok, timeout=0.2))
        expire_and_erase(k)
        with self.assertRaises(kernel.Rejected):
            k.sign_receipt(KEY)                      # worker still alive
        proc, _ = s.workers[tok]
        s.terminate(tok)
        self.assertFalse(proc.is_alive())
        self.assertIsNotNone(s.exitcodes[tok])
        self.assertNotIn(tok, k.inflight)
        k.sign_receipt(KEY)                          # exit observed, then accepted
        self.assertTrue(k.anchor.epochs[KEY].receipt)
        self.assertTrue(k.invariant())

    def test_settle_path_terminates_only_after_grace(self):
        k, s = prepared()
        s.start("r", hang)
        expire_and_erase(k)
        s.settle_path(KEY, grace=0.2)
        k.sign_receipt(KEY)
        self.assertEqual(s.workers, {})

    def test_crashing_worker_is_abandoned(self):
        k, s = prepared()
        tok = s.start("r", crash)
        self.assertFalse(s.collect(tok, timeout=30))
        self.assertEqual(s.exitcodes[tok], 3)
        self.assertEqual(k.jobs["r"].stage, "cancelled")
        self.assertNotIn(tok, k.inflight)

    def test_stale_completion_after_termination_is_ignored(self):
        k, s = prepared()
        tok = s.start("r", hang)
        s.terminate(tok)
        self.assertFalse(k.finish_decrypt(tok, b"late pair"))   # token no longer outstanding
        self.assertIsNone(k.jobs["r"].buffer)
        self.assertEqual(k.jobs["r"].stage, "cancelled")

    def test_kernel_crash_ends_workers_and_restart_admits_receipt(self):
        k, s = prepared()
        tok = s.start("r", hang)
        proc, _ = s.workers[tok]
        s.crash()
        self.assertFalse(proc.is_alive())
        self.assertEqual(k.inflight, {})
        k.restart()
        expire_and_erase(k)
        k.sign_receipt(KEY)
        self.assertTrue(k.invariant())


if __name__ == "__main__":
    unittest.main()
