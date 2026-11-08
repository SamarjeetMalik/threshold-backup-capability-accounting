"""Process-isolated decryption workers for the reference kernel (v4.1.0).

The kernel never runs a worker itself: it hands out a token at begin_decrypt
and expects finish_decrypt or abandon_decrypt, and sign_receipt refuses while
a token for the path is outstanding. This supervisor supplies the missing
executor. Each decryption runs in its own operating-system process (spawn
start method), which receives only the single key and ciphertext it needs.
The supervisor can terminate a worker that does not return and reports the
abandonment to the kernel only after it has observed the process exit, which
is the WorkerReturns/WorkerAbandons step of RecoveryLifecycleV4.

A worker also holds the read end of a lifeline pipe whose write end only the
supervisor process holds. If the supervisor process dies abruptly (SIGKILL,
no cleanup), the lifeline reaches end-of-file and the worker exits at once,
so no orphaned worker outlives its parent (v4.1.1).

This is a reference demonstration of the termination mechanism, not a
production isolation boundary: it does not sandbox the worker, scrub its
memory or constrain the operating system's scheduling.
"""
import multiprocessing
import os
import threading
import time

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305


# --- worker tasks (module level, so the spawn start method can import them) ---
def aead_open(key, nonce, ciphertext, aad):
    """Stand-in for capsule decryption: one AEAD open with one slot key."""
    return ChaCha20Poly1305(key).decrypt(nonce, ciphertext, aad)


def sleep_then(delay, key, nonce, ciphertext, aad):
    time.sleep(delay)
    return aead_open(key, nonce, ciphertext, aad)


def list_fd_inodes(*_):
    """Test task: report (device, inode) of every descriptor open in the worker."""
    import pickle
    out = []
    for name in os.listdir("/dev/fd"):
        try:
            st = os.fstat(int(name))
            out.append((st.st_dev, st.st_ino))
        except OSError:
            pass
    return pickle.dumps(out)


def aead_open_rss(key, nonce, ciphertext, aad):
    """Benchmark task: decrypt, then report plaintext length and this worker's peak RSS."""
    import pickle, resource, sys
    out = aead_open(key, nonce, ciphertext, aad)
    rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return pickle.dumps((len(out), rss if sys.platform == "darwin" else rss * 1024))


def nothing(*_):
    return b""


def hang(*_):
    time.sleep(3600)


def crash(*_):
    os._exit(3)


def _watch_lifeline(lifeline):
    try:
        lifeline.recv()             # blocks; nothing is ever sent
    except (EOFError, OSError):
        pass
    os._exit(70)                    # the supervisor process is gone


def _run(conn, lifeline, task, args):
    threading.Thread(target=_watch_lifeline, args=(lifeline,), daemon=True).start()
    try:
        out = task(*args)
        conn.send((True, bytes(out)))
    except Exception:
        conn.send((False, None))
    finally:
        conn.close()


class WorkerSupervisor:
    def __init__(self, kernel):
        self.kernel = kernel
        self.mp = multiprocessing.get_context("spawn")
        self.workers = {}           # token -> (process, receiving end of the pipe)
        self.exitcodes = {}         # token -> observed exit code
        self.lifelines = {}         # token -> write end of the worker's lifeline

    def start(self, nonce, task, *args):
        token = self.kernel.begin_decrypt(nonce, self.kernel.checkpoint(nonce))
        recv, send = self.mp.Pipe(duplex=False)
        life_r, life_w = self.mp.Pipe(duplex=False)
        proc = self.mp.Process(target=_run, args=(send, life_r, task, args), daemon=True)
        proc.start()
        send.close()                # the parent keeps only the receiving end
        life_r.close()              # ... and only the write end of the lifeline
        self.lifelines[token] = life_w
        self.workers[token] = (proc, recv)
        return token

    def _reap(self, token):
        proc, recv = self.workers.pop(token)
        proc.join()
        recv.close()
        self.lifelines.pop(token).close()
        self.exitcodes[token] = proc.exitcode
        return proc

    def collect(self, token, timeout=0.0):
        """Deliver a returned worker's result. None if it is still running."""
        proc, recv = self.workers[token]
        if not recv.poll(timeout):
            return None
        try:
            ok, out = recv.recv()
        except EOFError:            # the worker died without reporting
            ok, out = False, None
        self._reap(token)
        if ok:
            return self.kernel.finish_decrypt(token, out)
        self.kernel.abandon_decrypt(token)
        return False

    def terminate(self, token):
        """Kill a worker, observe its exit, then report abandonment."""
        proc, _ = self.workers[token]
        proc.terminate()
        proc = self._reap(token)
        assert not proc.is_alive() and proc.exitcode is not None
        self.kernel.abandon_decrypt(token)

    def settle_path(self, key, grace=0.5):
        """Before a receipt: collect workers of path `key`, terminating any that do not return within `grace`."""
        for token in [t for t in self.workers if self.kernel.inflight.get(t) == key]:
            if self.collect(token, grace) is None:
                self.terminate(token)

    def crash(self):
        """A kernel crash ends every worker process before the kernel forgets them."""
        for token in list(self.workers):
            proc, _ = self.workers[token]
            proc.terminate()
            self._reap(token)
        self.kernel.crash()
