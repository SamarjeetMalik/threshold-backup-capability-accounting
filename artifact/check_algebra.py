"""Independent finite distribution checks of the general rank characterization."""
from collections import Counter
from itertools import product
import json
from capability import CapabilityModel, privacy_holds, in_rowspan, sharing_model, subsets, minimal_witnesses, minimum_deletions


def distribution(rows, seeds, masks, p):
    return Counter(tuple(sum(a*x for a, x in zip(row, seeds+r)) % p for row in rows)
                   for r in product(range(p), repeat=masks))


def exhaustive_rank_privacy():
    checked = 0
    p = 3
    for secrets, masks, outputs in [(1, 1, 1), (1, 1, 2), (2, 1, 1), (2, 1, 2), (2, 2, 2)]:
        width = secrets + masks
        for flat in product(range(p), repeat=outputs*width):
            rows = [flat[i*width:(i+1)*width] for i in range(outputs)]
            reference = distribution(rows, (0,)*secrets, masks, p)
            actual = all(distribution(rows, s, masks, p) == reference
                         for s in product(range(p), repeat=secrets))
            predicted = privacy_holds(rows, range(secrets), p)
            assert actual == predicted, rows
            # Independent all-input fiber test of universal reconstruction in
            # the full-field model, rather than repeating Gaussian elimination.
            fibers = {}
            for x in product(range(p), repeat=width):
                y = tuple(sum(a*b for a,b in zip(row,x)) % p for row in rows)
                fibers.setdefault(y, set()).add(x[0])
            reconstructible = all(len(v) == 1 for v in fibers.values())
            assert reconstructible == in_rowspan([1]+[0]*(width-1), rows, p)
            checked += 1
    relation_only = [[1, 1]]
    assert not in_rowspan([1, 0], relation_only, p)
    assert not in_rowspan([0, 1], relation_only, p)
    assert not privacy_holds(relation_only, [0, 1], p)
    return {"field": p, "matrices": checked, "distribution_and_fiber_checks_pass": True,
            "relation_only_example": {"rows": relation_only, "neither_seed_linearly_recovered": True, "joint_privacy": False}}


def generation_tests():
    checked = 0
    for t0, t1 in [(2,2), (2,3), (3,2), (3,3)]:
        spec = [(0,0,3,t0,"old","r0"), (0,1,3,t1,"new","r1")]
        model = sharing_model(spec, p=7)
        public = frozenset({"published:0:0", "published:0:1"})
        for i0 in subsets(range(1,4)):
            for i1 in subsets(range(1,4)):
                pairs = frozenset(f"pair:0:{g}:{h}" for g,items in enumerate([i0,i1]) for h in items)
                actual = model.private(public | pairs)
                assert actual == (len(i0)<t0 and len(i1)<t1)
                checked += 1
    reused = sharing_model([(0,0,3,2,"old","shared"),(0,1,3,2,"new","shared")],p=7)
    observed = frozenset({"published:0:0","published:0:1","pair:0:0:1","pair:0:1:2"})
    assert not reused.private(observed)
    assert "seed:0" in reused.close(observed)
    return {"independent_threshold_pattern_pairs": checked,
            "reused_randomness_subthreshold_per_generation_leaks": True}


def cuts():
    m = sharing_model([(0,0,3,2,"old","r0")],p=7)
    public = frozenset({"published:0:0","record:0","archive-capsule:0"})
    honest = frozenset({"bank-copy:old:1","bank-copy:old:2","bank-copy:old:3","archive-key:0"})
    target = "plaintext:0"
    witnesses = minimal_witnesses(m, honest, public, target)
    answers = minimum_deletions(m,honest,frozenset(),public,target)
    assert {len(x) for x in answers} == {3}  # two ordinary paths AND archive
    checked = 0
    for immutable in [frozenset(),frozenset({"archive-key:0"}),frozenset({"bank-copy:old:1","bank-copy:old:2"})]:
        erasable = honest - immutable
        for deleted in subsets(erasable):
            reconstruction = target in m.close(public | immutable | (erasable-deleted))
            all_hit = all(bool(w & deleted) for w in witnesses)
            assert (not reconstruction) == all_hit
            checked += 1
    relation=CapabilityModel(7,("S0","S1"),{0:0,1:1},observations={"sum":(1,1)})
    privacy_cut=minimum_deletions(relation,frozenset({"sum"}),frozenset(),frozenset(),privacy_targets={0,1})
    recon_cut=minimum_deletions(relation,frozenset({"sum"}),frozenset(),frozenset(),target="seed:0")
    assert privacy_cut==[frozenset({"sum"})] and recon_cut==[frozenset()]
    assert minimal_witnesses(relation,{"sum"},frozenset(),privacy_targets={0,1})==[frozenset({"sum"})]
    return {"minimal_witnesses":[sorted(w) for w in witnesses],
            "minimum_deletion_size":3,"cut_equivalence_checks":checked,
            "immutable_archive_makes_erasure_impossible":not minimum_deletions(m,honest-{"archive-key:0"},frozenset({"archive-key:0"}),public,target),
            "relation_only_cut":{"privacy_deletions":[sorted(x) for x in privacy_cut],"linear_reconstruction_deletions":[sorted(x) for x in recon_cut]}}


def main():
    result = {"scope":"exact finite-field and declared symbolic-rule checks", "rank":exhaustive_rank_privacy(),
              "generations":generation_tests(),"cuts":cuts()}
    print(json.dumps(result,indent=2))


if __name__ == "__main__":
    main()
