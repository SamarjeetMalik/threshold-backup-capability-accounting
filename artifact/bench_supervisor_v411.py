"""v4.1.1: cost of process-isolated decryption (worker_supervisor.py) against a
direct in-process AEAD open of the same ciphertext.

For each size, 21 trials of: direct open; supervised open (begin_decrypt,
spawn worker, decrypt, return result over a pipe, join, finish_decrypt);
an empty supervised task (spawn, IPC, join: the fixed overhead); and a
supervised open whose worker reports its own peak RSS (getrusage ru_maxrss).
Reports median and 95th percentile wall-clock time. Single machine; enters
no proof. Store/Open timings elsewhere in the paper do not include this path.
"""
from pathlib import Path
import csv, hashlib, json, pickle, platform, resource, statistics, sys, time

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
import lifecycle_kernel as kernel
from worker_supervisor import WorkerSupervisor, aead_open, aead_open_rss, nothing

TRIALS, SIZES, MIB = 21, (1 << 10, 1 << 20, 16 << 20, 64 << 20), 1 << 20


class Clock:
    def __init__(self): self.now = 0
    def __call__(self): return self.now


def fresh():
    c = Clock(); k = kernel.ReferenceKernel(epoch_keys=((0, 0),), clock=c)
    r = kernel.Request("acct", "r", 0, 0, 0, b"recipient", b"manifest")
    k.register(r); k.authorize("r", kernel.Certificate(r.digest, (1, 2), 0)); c.now = 24
    return k, WorkerSupervisor(k)


def q(xs, p):
    xs = sorted(xs); i = (len(xs) - 1) * p; lo = int(i); hi = min(lo + 1, len(xs) - 1)
    return xs[lo] + (xs[hi] - xs[lo]) * (i - lo)


def supervised(task, *args):
    k, s = fresh()
    t = time.perf_counter()
    tok = s.start("r", task, *args)
    ok = s.collect(tok, timeout=600)
    dt = (time.perf_counter() - t) * 1e3
    assert ok, "supervised decryption failed"
    return dt, bytes(k.jobs["r"].buffer)


def main(outdir):
    import cryptography
    rows, raw = [], {}
    key, nonce = hashlib.sha256(b"bench-supervisor").digest(), bytes(12)
    for size in SIZES:
        pt = hashlib.shake_256(f"sup/{size}".encode()).digest(size)
        ct = ChaCha20Poly1305(key).encrypt(nonce, pt, b"ad")
        direct, sup, empty, wrss = [], [], [], []
        for _ in range(TRIALS):
            t = time.perf_counter(); out = aead_open(key, nonce, ct, b"ad"); direct.append((time.perf_counter() - t) * 1e3)
            assert out == pt
            dt, got = supervised(aead_open, key, nonce, ct, b"ad"); sup.append(dt); assert got == pt
            dt, _ = supervised(nothing); empty.append(dt)
            _, rep = supervised(aead_open_rss, key, nonce, ct, b"ad"); n, rss = pickle.loads(rep); assert n == size
            wrss.append(rss / MIB)
        raw[size] = {"direct_ms": direct, "supervised_ms": sup, "empty_task_ms": empty, "worker_peak_rss_MiB": wrss}
        rows.append([size, statistics.median(direct), q(direct, .95), statistics.median(sup), q(sup, .95),
                     statistics.median(empty), q(empty, .95), statistics.median(wrss)])
    rss_parent = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    res = {"method": __doc__, "python": sys.version.split()[0], "platform": platform.platform(),
           "cryptography": cryptography.__version__, "trials": TRIALS, "raw": raw,
           "bench_process_peak_rss_MiB": (rss_parent if sys.platform == "darwin" else rss_parent * 1024) / MIB}
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "bench_supervisor_v411.json").write_text(json.dumps(res, indent=1))
    with open(outdir / "bench_supervisor.csv", "w", newline="") as f:
        w = csv.writer(f, delimiter=" ")
        w.writerow(["bytes", "direct_med", "direct_p95", "sup_med", "sup_p95", "empty_med", "empty_p95", "worker_rss_med"])
        for r in rows:
            w.writerow([r[0]] + [f"{x:.3f}" for x in r[1:]])
    print(open(outdir / "bench_supervisor.csv").read(), "bench process peak RSS MiB", round(res["bench_process_peak_rss_MiB"], 1))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "evidence_v411" / "mac_m5_supervisor")
