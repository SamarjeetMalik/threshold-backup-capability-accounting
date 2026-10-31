"""Independent finite enumeration of joint quorum feasibility."""
import json


def main():
    checked = feasible = 0
    for n in range(1, 21):
        for f in range(n + 1):
            for c in range(n + 1):
                for u in range(n - f + 1):
                    available = n - f - u
                    # Enumerate actual share/deletion pairs, not just substitute
                    # the advertised minimum-size inequality.
                    pairs = [(t, q) for t in range(1, available + 1)
                             for q in range(1, available + 1)
                             if min(n, n-q+f+c) < t]
                    approvals = [q for q in range(1, available + 1) if q > f]
                    logs = [q for q in range(1, available + 1) if 2*q > n+f]
                    actual = bool(pairs and approvals and logs)
                    predicted = n >= 3*f+c+2*u+1
                    assert actual == predicted, (n, f, c, u)
                    if pairs:
                        assert all(t >= 2*f+c+u+1 for t, _ in pairs)
                    checked += 1
                    feasible += actual
    print(json.dumps({"n_range": [1, 20], "parameter_configurations": checked,
                      "joint_feasible": feasible, "all_equivalences_pass": True}, indent=2))


if __name__ == "__main__":
    main()
