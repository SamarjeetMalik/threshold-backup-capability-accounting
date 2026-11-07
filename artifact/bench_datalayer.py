"""Measurements of the reference data layer on the machine that runs it.

These are wall-clock measurements of one Python process, reported with the
environment. They are not comparable across machines and are not part of any
proof. Each figure is the median of several repetitions after one warm-up.
"""
import json, platform, statistics, sys, time, tracemalloc
import hashlib, hmac, os

import cryptography
from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305

from datalayer import DataLayer, Record, AuthFailure


def median_time(fn, reps):
    fn()
    xs = []
    for _ in range(reps):
        t = time.perf_counter(); fn(); xs.append(time.perf_counter() - t)
    return statistics.median(xs)


def main():
    seed = os.urandom(32)
    out = {"environment": {"python": sys.version.split()[0], "machine": platform.machine(),
                           "platform": platform.platform(), "cryptography": cryptography.__version__,
                           "openssl": backend.openssl_version_text()},
           "method": "median wall-clock of repetitions after one warm-up; time.perf_counter",
           "primitives": {}, "objects": []}
    ctx = os.urandom(120)
    out["primitives"]["hmac_derivation_us"] = round(1e6 * median_time(
        lambda: hmac.new(seed, ctx, hashlib.sha256).digest(), 2000), 3)
    for size in (4 << 10, 64 << 10, 1 << 20):
        a = ChaCha20Poly1305(os.urandom(32)); p = os.urandom(size); n = bytes(12); ad = b"a" * 64
        c = a.encrypt(n, p, ad)
        enc = median_time(lambda: a.encrypt(n, p, ad), 50)
        dec = median_time(lambda: a.decrypt(n, c, ad), 50)
        out["primitives"][f"chunk_{size}"] = {"encrypt_us": round(1e6 * enc, 2), "decrypt_us": round(1e6 * dec, 2),
                                              "encrypt_MiB_per_s": round(size / enc / (1 << 20), 1)}
    for obj_size, chunk in [(1 << 20, 64 << 10), (16 << 20, 1 << 20), (64 << 20, 1 << 20), (16 << 20, 64 << 10)]:
        dl = DataLayer(seed)
        data = os.urandom(obj_size)
        store = median_time(lambda: dl.store(0, b"hdr", data, chunk_size=chunk), 3)
        rec = dl.store(0, b"hdr", data, chunk_size=chunk)
        recover = median_time(lambda: dl.open(rec), 3)
        tracemalloc.start(); dl.open(rec); peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        stored = sum(len(c) for c in rec.chunks)
        bad = list(rec.chunks); bad[-1] = bytes(len(bad[-1]))
        def fail():
            try:
                dl.open(Record(rec.ctx, bad))
            except AuthFailure:
                pass
        failure = median_time(fail, 3)
        out["objects"].append({"object_bytes": obj_size, "chunk_bytes": chunk, "chunks": len(rec.chunks),
                               "store_ms": round(1e3 * store, 2), "recover_ms": round(1e3 * recover, 2),
                               "recover_MiB_per_s": round(obj_size / recover / (1 << 20), 1),
                               "ciphertext_overhead_bytes": stored - obj_size,
                               "overhead_analytical_bytes": 16 * len(rec.chunks),
                               "open_peak_python_heap_MiB": round(peak / (1 << 20), 2),
                               "detect_tampered_last_chunk_ms": round(1e3 * failure, 2)})
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()
