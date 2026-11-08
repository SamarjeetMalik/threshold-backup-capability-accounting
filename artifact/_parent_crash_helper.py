"""Helper for test_worker_supervisor_v411: plays the kernel's operating-system
process. It starts a hung decryption worker, writes the worker's PID, the
outstanding token and a snapshot of the durable anchor, then waits to be
killed with SIGKILL (no cleanup runs)."""
import pickle
import sys
import time

import lifecycle_kernel as kernel
from worker_supervisor import WorkerSupervisor, hang


class Clock:
    def __init__(self): self.now = 0
    def __call__(self): return self.now


if __name__ == "__main__":
    out = sys.argv[1]
    c = Clock(); k = kernel.ReferenceKernel(epoch_keys=((0, 0),), clock=c)
    r = kernel.Request("acct", "r", 0, 0, 0, b"recipient", b"manifest")
    k.register(r); k.authorize("r", kernel.Certificate(r.digest, (1, 2), 0)); c.now = 24
    s = WorkerSupervisor(k)
    tok = s.start("r", hang)
    proc, _ = s.workers[tok]
    with open(out, "wb") as f:
        pickle.dump({"worker_pid": proc.pid, "token": tok, "anchor": k.snapshot()}, f)
    print("READY", flush=True)
    time.sleep(3600)
