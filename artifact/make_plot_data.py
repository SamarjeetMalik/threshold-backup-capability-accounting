"""Generate the data files behind every manuscript plot (v4.0.4).

Exact quantities come from the paper's formulas (eq. 6 for L, Proposition 27
for L_reuse, Lemma 24 for the key-collision bound, Proposition 17 for the
feasibility region and minimum committee size). Measured quantities are copied
from the benchmark output. Nothing here is fitted or estimated.
"""
from pathlib import Path
from math import comb, log2
import shutil, sys

from v403_checks import exact_count


def general_L(n, ts):
    L = 1
    for t in ts:
        L *= sum(comb(n, j) for j in range(t))
    return L


def main(out, bench, memory=None):
    out.mkdir(parents=True, exist_ok=True)
    # Plot 1a: equal thresholds
    with open(out / "guess_equal.dat", "w") as f:
        f.write("G L75 R75 L53 R53\n")
        for G in range(1, 7):
            f.write(f"{G} {general_L(7, [5]*G)} {exact_count(7, [5]*G)} {general_L(5, [3]*G)} {exact_count(5, [3]*G)}\n")
    # Plot 1b: unequal (non-increasing) thresholds, n = 7, partial publication allowed
    seq = [6, 5, 4, 4, 3, 3]
    with open(out / "guess_unequal.dat", "w") as f:
        f.write("G L R\n")
        for G in range(1, 7):
            f.write(f"{G} {general_L(7, seq[:G])} {exact_count(7, seq[:G])}\n")
    # Plot 2: derived-key collision bound, log2 scale (bad-event bound, not a frequency)
    with open(out / "keycoll.dat", "w") as f:
        f.write("log2K log2bound\n")
        for k in range(1, 65):
            K = 2**k
            f.write(f"{k} {log2(K) + log2(K - 1) - 257:.4f}\n")
    # Figure 8: feasibility of t for n = 13 in three scenarios (Proposition 17)
    with open(out / "feasible.dat", "w") as f:
        f.write("scenario f t ok\n")
        for s, (c, u) in enumerate([(0, 0), (1, 1), (2, 2)]):
            for fb in range(0, 5):
                for t in range(1, 14):
                    ok = int(2 * fb + c + u + 1 <= t <= 13 - fb - u)
                    f.write(f"{s} {fb} {t} {ok}\n")
    # Plot 8: minimum holders n = 3f + c + 2u + 1
    for u in range(0, 3):
        with open(out / f"minholders_u{u}.dat", "w") as f:
            f.write("f c n\n")
            for fb in range(0, 5):
                for c in range(0, 4):
                    f.write(f"{fb} {c} {3*fb + c + 2*u + 1}\n")
    # measured benchmark tables (copied verbatim)
    for name in ("bench_chunks.csv", "bench_objects.csv"):
        shutil.copy(bench / name, out / name.replace(".csv", ".dat"))
    # per-cipher split of the chunk table, for the latency and throughput plots
    rows = (out / "bench_chunks.dat").read_text().splitlines()
    for cipher, fname in (("chacha20poly1305", "bench_chacha.dat"), ("aes256gcm", "bench_aes.dat")):
        lines = ["kib enc_med enc_q1 enc_q3 dec_med gibps"] + [" ".join(r.split()[1:]) for r in rows[1:] if r.split()[0] == cipher]
        (out / fname).write_text("\n".join(lines) + "\n")
    # v4.1.0: repeated memory measurement (bench_memory_v410.py), copied verbatim
    if memory is not None:
        shutil.copy(memory / "bench_memory.csv", out / "bench_memory.dat")
    # v4.1.1: process-supervised versus direct decryption (bench_supervisor_v411.py)
    sup = Path(__file__).resolve().parent / "evidence_v411" / "mac_m5_supervisor" / "bench_supervisor.csv"
    if sup.exists():
        shutil.copy(sup, out / "bench_supervisor.dat")
    print("wrote", sorted(p.name for p in out.iterdir()))


if __name__ == "__main__":
    root = Path(__file__).resolve().parent
    main(root.parent / "manuscript" / "data", Path(sys.argv[1]) if len(sys.argv) > 1 else root / "evidence_v411" / "mac_m5",
         Path(sys.argv[2]) if len(sys.argv) > 2 else root / "evidence_v411" / "mac_m5_memory")
