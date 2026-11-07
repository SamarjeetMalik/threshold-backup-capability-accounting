"""v4.0.4 measurements of the reference data layer and its primitives.

Method: seeded input data (identical across ciphers; objects expanded with SHAKE-256 from the seed); 5 warm-up iterations;
40 timed repetitions for per-chunk and HMAC microbenchmarks; 12 trials for
object-level store/open; statistics are median, quartiles, 5th and 95th
percentiles of wall-clock time (time.perf_counter_ns). Peak Python heap is
measured in a separate traced run, because tracing perturbs timing.
Outputs JSON (raw samples included) and CSV files for the manuscript plots.
These are single-machine observations; they enter no proof.
"""
from pathlib import Path
import csv, json, platform, random, statistics, sys, time, tracemalloc
import hashlib, hmac

import cryptography
from cryptography.hazmat.backends.openssl.backend import backend
from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305, AESGCM

from datalayer import DataLayer

SEED, WARM, REPS, TRIALS = 20261106, 5, 40, 12
KIB, MIB = 1 << 10, 1 << 20


def quantiles(xs):
    xs = sorted(xs)
    def q(p):
        k = (len(xs) - 1) * p
        lo, hi = int(k), min(int(k) + 1, len(xs) - 1)
        return xs[lo] + (xs[hi] - xs[lo]) * (k - lo)
    return {"median": q(0.5), "q1": q(0.25), "q3": q(0.75), "p5": q(0.05), "p95": q(0.95), "n": len(xs)}


def timed(fn, reps):
    for _ in range(WARM):
        fn()
    out = []
    for _ in range(reps):
        t = time.perf_counter_ns(); fn(); out.append((time.perf_counter_ns() - t) / 1e3)  # microseconds
    return out


def main(outdir):
    rng = random.Random(SEED)
    res = {"environment": {"python": sys.version.split()[0], "machine": platform.machine(),
                           "processor": platform.processor(), "platform": platform.platform(),
                           "cryptography": cryptography.__version__, "openssl": backend.openssl_version_text()},
           "method": {"seed": SEED, "warmups": WARM, "micro_reps": REPS, "object_trials": TRIALS,
                      "clock": "time.perf_counter_ns", "units": "microseconds unless stated"},
           "hmac": None, "chunks": [], "objects": []}
    key, ctx = rng.randbytes(32), rng.randbytes(120)
    s = timed(lambda: hmac.new(key, ctx, hashlib.sha256).digest(), REPS)
    res["hmac"] = {"stats": quantiles(s), "samples": s}

    ad = rng.randbytes(64)
    for size in (1 * KIB, 4 * KIB, 16 * KIB, 64 * KIB, 256 * KIB, 1 * MIB):
        data = rng.randbytes(size)
        for name, cls in (("chacha20poly1305", ChaCha20Poly1305), ("aes256gcm", AESGCM)):
            aead = cls(rng.randbytes(32))
            ctr = iter(range(1 << 40))                    # fresh nonce for every encryption
            enc = timed(lambda: aead.encrypt(bytes(4) + next(ctr).to_bytes(8, "big"), data, ad), REPS)
            n0 = bytes(4) + next(ctr).to_bytes(8, "big")
            ct = aead.encrypt(n0, data, ad)
            dec = timed(lambda: aead.decrypt(n0, ct, ad), REPS)
            st = quantiles(enc)
            res["chunks"].append({"cipher": name, "chunk_bytes": size, "encrypt": st, "decrypt": quantiles(dec),
                                  "encrypt_GiBps_at_median": size / (st["median"] * 1e-6) / (1 << 30),
                                  "samples_encrypt": enc, "samples_decrypt": dec})

    for size_mib in (1, 4, 16, 64, 256):
        data = hashlib.shake_256(f"{SEED}/{size_mib}".encode()).digest(size_mib * MIB)  # seeded
        dl = DataLayer(rng.randbytes(32))
        store = timed(lambda: dl.store(0, b"hdr", data, chunk_size=MIB), TRIALS)
        rec = dl.store(0, b"hdr", data, chunk_size=MIB)
        opn = timed(lambda: dl.open(rec), TRIALS)
        tracemalloc.start(); dl.open(rec); peak = tracemalloc.get_traced_memory()[1]; tracemalloc.stop()
        res["objects"].append({"object_MiB": size_mib, "chunk_bytes": MIB, "chunks": len(rec.chunks),
                               "store_ms": {k: (v / 1e3 if k != "n" else v) for k, v in quantiles(store).items()},
                               "open_ms": {k: (v / 1e3 if k != "n" else v) for k, v in quantiles(opn).items()},
                               "open_peak_heap_MiB": peak / MIB,
                               "ciphertext_overhead_bytes": sum(len(c) for c in rec.chunks) - len(data)})
        del data, rec, dl

    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "bench_v404.json").write_text(json.dumps(res, indent=1))
    with open(outdir / "bench_chunks.csv", "w", newline="") as f:
        w = csv.writer(f, delimiter=" ")
        w.writerow(["cipher", "kib", "enc_med", "enc_q1", "enc_q3", "dec_med", "gibps"])
        for r in res["chunks"]:
            e = r["encrypt"]
            w.writerow([r["cipher"], r["chunk_bytes"] // KIB, f"{e['median']:.3f}", f"{e['q1']:.3f}",
                        f"{e['q3']:.3f}", f"{r['decrypt']['median']:.3f}", f"{r['encrypt_GiBps_at_median']:.3f}"])
    with open(outdir / "bench_objects.csv", "w", newline="") as f:
        w = csv.writer(f, delimiter=" ")
        w.writerow(["mib", "store_med", "store_q1", "store_q3", "open_med", "open_q1", "open_q3", "peak_mib"])
        for r in res["objects"]:
            s_, o = r["store_ms"], r["open_ms"]
            w.writerow([r["object_MiB"], f"{s_['median']:.3f}", f"{s_['q1']:.3f}", f"{s_['q3']:.3f}",
                        f"{o['median']:.3f}", f"{o['q1']:.3f}", f"{o['q3']:.3f}", f"{r['open_peak_heap_MiB']:.2f}"])
    print(json.dumps({"hmac_us": res["hmac"]["stats"],
                      "chunks": [(r["cipher"], r["chunk_bytes"], round(r["encrypt"]["median"], 2),
                                  round(r["encrypt_GiBps_at_median"], 2)) for r in res["chunks"]],
                      "objects": [(r["object_MiB"], round(r["store_ms"]["median"], 1), round(r["open_ms"]["median"], 1),
                                   round(r["open_peak_heap_MiB"], 1)) for r in res["objects"]]}, indent=1))


if __name__ == "__main__":
    main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "reproduced" / "bench_v404")
