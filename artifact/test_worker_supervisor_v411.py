"""v4.1.1 supervisor tests: abrupt death of the supervising process, inherited
file descriptors, output discarded after expiry, and stale or duplicate
completions across requests. Requires pyca/cryptography."""
import os
import pickle
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

import lifecycle_kernel as kernel
from worker_supervisor import WorkerSupervisor, hang, aead_open, list_fd_inodes, sleep_then

KEY = (0, 0)
HERE = Path(__file__).resolve().parent


class Clock:
    def __init__(self): self.now = 0
    def __call__(self): return self.now


def prepared():
    c = Clock(); k = kernel.ReferenceKernel(epoch_keys=(KEY,), clock=c)
    r = kernel.Request("acct", "r", 0, 0, 0, b"recipient", b"manifest")
    k.register(r); k.authorize("r", kernel.Certificate(r.digest, (1, 2), 0)); c.now = 24
    return c, k, WorkerSupervisor(k)


def alive(pid):
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    return True


class ParentCrash(unittest.TestCase):
    def test_sigkill_of_supervisor_process_ends_worker_and_no_receipt_survives(self):
        with tempfile.TemporaryDirectory() as tmp:
            state = Path(tmp) / "state.pkl"
            parent = subprocess.Popen([sys.executable, str(HERE / "_parent_crash_helper.py"), str(state)],
                                      cwd=HERE, stdout=subprocess.PIPE, text=True)
            try:
                self.assertEqual(parent.stdout.readline().strip(), "READY")
                saved = pickle.loads(state.read_bytes())
                pid = saved["worker_pid"]
                self.assertTrue(alive(pid))
                os.kill(parent.pid, signal.SIGKILL)            # abrupt: no cleanup, no atexit
                parent.wait(timeout=10)
                deadline = time.time() + 10
                while alive(pid) and time.time() < deadline:
                    time.sleep(0.05)
                self.assertFalse(alive(pid), "worker outlived its supervisor")
            finally:
                if parent.poll() is None:
                    parent.kill()
                    parent.wait()
                parent.stdout.close()
            # restart from the durable anchor: volatile in-flight state is gone
            c = Clock(); k2 = kernel.ReferenceKernel(epoch_keys=(KEY,), clock=c)
            k2.anchor = saved["anchor"]
            k2.crash(); k2.restart()
            self.assertFalse(k2.anchor.epochs[KEY].receipt)
            self.assertFalse(k2.finish_decrypt(saved["token"], b"stale pair"))   # stale completion rejected
            with self.assertRaises(kernel.Rejected):
                k2.sign_receipt(KEY)                                            # no cleanup yet
            k2.begin_expiry(KEY)
            with self.assertRaises(kernel.Rejected):
                k2.sign_receipt(KEY)                                            # slot not erased
            k2.erase_slot(KEY)
            k2.sign_receipt(KEY)
            self.assertTrue(k2.invariant())


class Containment(unittest.TestCase):
    def test_worker_does_not_inherit_unrelated_descriptors(self):
        c, k, s = prepared()
        with tempfile.TemporaryFile() as f:
            st = os.fstat(f.fileno())
            tok = s.start("r", list_fd_inodes)
            self.assertTrue(s.collect(tok, timeout=30))
            seen = pickle.loads(bytes(k.jobs["r"].buffer))
        self.assertNotIn((st.st_dev, st.st_ino), seen)    # an open file of the parent is not inherited

    def test_output_after_expiry_is_discarded(self):
        c, k, s = prepared()
        key, nonce = bytes(range(32)), bytes(12)
        from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
        ct = ChaCha20Poly1305(key).encrypt(nonce, b"pair", b"")
        tok = s.start("r", sleep_then, 0.3, key, nonce, ct, b"")
        k.begin_expiry(KEY)                                # job cancelled while the worker runs
        self.assertFalse(s.collect(tok, timeout=30))       # its later result is refused
        self.assertIsNone(k.jobs["r"].buffer)
        self.assertEqual(k.jobs["r"].stage, "cancelled")

    def test_duplicate_and_cross_request_completions_are_rejected(self):
        c, k, s = prepared()
        t1 = s.start("r", hang)
        s.terminate(t1)                                    # first request abandoned
        r2 = kernel.Request("acct", "r2", 0, 0, 0, b"recipient", b"manifest")
        k.register(r2); k.authorize("r2", kernel.Certificate(r2.digest, (1, 2), 0)); c.now = 48
        key, nonce = bytes(range(32)), bytes(12)
        from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
        ct = ChaCha20Poly1305(key).encrypt(nonce, b"pair-2", b"")
        t2 = s.start("r2", aead_open, key, nonce, ct, b"")
        self.assertFalse(k.finish_decrypt(t1, b"late pair"))      # old worker's token cannot satisfy r2
        self.assertEqual(k.jobs["r2"].stage, "decrypting")
        self.assertTrue(s.collect(t2, timeout=30))
        self.assertFalse(k.finish_decrypt(t2, b"duplicate"))      # token is single-use
        self.assertEqual(bytes(k.jobs["r2"].buffer), b"pair-2")


if __name__ == "__main__":
    unittest.main()
