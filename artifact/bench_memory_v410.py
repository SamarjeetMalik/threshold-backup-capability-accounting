"""v4.1.0 memory measurement of the reference data layer's Open.

Method: for every object size (1 MiB chunks) and every trial, a fresh child
process stores a seeded object (SHAKE-256 of the seed) and writes the record
to a temporary file; a second fresh child process loads the record, starts
tracemalloc, opens the object once, and reports
  * the tracemalloc peak during Open (Python-managed allocations), and
  * the process's peak resident set size (getrusage ru_maxrss), which also
    contains the interpreter, the imported modules and the loaded record.
An idle child that only imports the same modules gives the RSS baseline.
Seven trials per size; outputs raw JSON and a CSV of median, min and max.
These are single-machine observations; they enter no proof.
"""
from pathlib import Path
import csv, hashlib, json, os, pickle, platform, resource, statistics, subprocess, sys, tempfile

SEED, TRIALS, SIZES = 20261109, 7, (1, 4, 16, 64, 256)
MIB = 1 << 20


def maxrss_bytes():
    r = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    return r if sys.platform == "darwin" else r * 1024      # Linux reports KiB


def child_store(size_mib, path):
    from datalayer import DataLayer
    data = hashlib.shake_256(f"{SEED}/{size_mib}".encode()).digest(size_mib * MIB)
    dl = DataLayer(hashlib.sha256(f"{SEED}/seed".encode()).digest())
    rec = dl.store(0, b"hdr", data, chunk_size=MIB)
    with open(path, "wb") as f:
        pickle.dump((rec.ctx, rec.chunks), f)


def child_open(path):
    import tracemalloc
    from datalayer import DataLayer, Record
    with open(path, "rb") as f:
        ctx, chunks = pickle.load(f)
    dl = DataLayer(hashlib.sha256(f"{SEED}/seed".encode()).digest())
    tracemalloc.start()
    out = dl.open(Record(ctx, chunks))
    peak = tracemalloc.get_traced_memory()[1]
    tracemalloc.stop()
    print(json.dumps({"bytes": len(out), "tracemalloc_peak": peak, "maxrss": maxrss_bytes()}))


def child_idle():
    from datalayer import DataLayer, Record  # noqa: F401  (same imports as child_open)
    import tracemalloc  # noqa: F401
    print(json.dumps({"maxrss": maxrss_bytes()}))


def run(*args):
    here = Path(__file__).resolve().parent
    r = subprocess.run([sys.executable, str(Path(__file__).resolve()), *map(str, args)], cwd=here,
                       capture_output=True, text=True, check=True)
    return r.stdout.strip()


def summary(xs):
    return {"median": statistics.median(xs), "min": min(xs), "max": max(xs), "n": len(xs)}


def main(outdir):
    import cryptography
    res = {"method": __doc__, "python": sys.version.split()[0], "platform": platform.platform(),
           "machine": platform.machine(), "cryptography": cryptography.__version__, "trials": TRIALS,
           "idle_maxrss_bytes": [json.loads(run("--idle"))["maxrss"] for _ in range(TRIALS)], "objects": []}
    with tempfile.TemporaryDirectory() as tmp:
        for size in SIZES:
            samples = []
            for t in range(TRIALS):
                path = Path(tmp) / f"rec_{size}_{t}.pkl"
                run("--store", size, path)
                s = json.loads(run("--open", path))
                assert s["bytes"] == size * MIB
                samples.append(s)
                path.unlink()
            res["objects"].append({"object_MiB": size, "samples": samples,
                                   "tracemalloc_MiB": summary([s["tracemalloc_peak"] / MIB for s in samples]),
                                   "maxrss_MiB": summary([s["maxrss"] / MIB for s in samples])})
    res["idle_maxrss_MiB"] = summary([b / MIB for b in res["idle_maxrss_bytes"]])
    outdir.mkdir(parents=True, exist_ok=True)
    (outdir / "bench_memory_v410.json").write_text(json.dumps(res, indent=1))
    with open(outdir / "bench_memory.csv", "w", newline="") as f:
        w = csv.writer(f, delimiter=" ")
        w.writerow(["mib", "tm_med", "tm_min", "tm_max", "rss_med", "rss_min", "rss_max"])
        for r in res["objects"]:
            a, b = r["tracemalloc_MiB"], r["maxrss_MiB"]
            w.writerow([r["object_MiB"], f"{a['median']:.2f}", f"{a['min']:.2f}", f"{a['max']:.2f}",
                        f"{b['median']:.1f}", f"{b['min']:.1f}", f"{b['max']:.1f}"])
    print(json.dumps({"idle_rss_MiB": res["idle_maxrss_MiB"],
                      "objects": [(r["object_MiB"], r["tracemalloc_MiB"], r["maxrss_MiB"]) for r in res["objects"]]},
                     indent=1))


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--store":
        child_store(int(sys.argv[2]), sys.argv[3])
    elif len(sys.argv) > 1 and sys.argv[1] == "--open":
        child_open(sys.argv[2])
    elif len(sys.argv) > 1 and sys.argv[1] == "--idle":
        child_idle()
    else:
        main(Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent / "evidence_v410")
