"""Finite temporal disclosure exploration with shortest counterexamples.

Each CopyBank action is an atomic visit ending before the next action, so visits
need not overlap. It copies data capabilities, not signing identities. No bound
on lifetime Byzantine identity compromise is inferred from these traces.
"""
from collections import deque
from dataclasses import dataclass
import json
from capability import sharing_model


@dataclass(frozen=True)
class Leak:
    atom: str
    kind: str
    group: str
    limit: int
    earliest: int = 0
    latest: int = 99
    needs: str = ""


def explore(name, spec, steps, leaks, targets, check_after, expected_private):
    model = sharing_model(spec, p=101)
    public = frozenset(f"record:{e}" for e in model.seeds)
    initial = (0, model.close(public), frozenset())
    queue = deque([initial])
    paths = {initial: []}
    edges = eligible = private_count = 0
    privacy_witness = reconstruction_witness = None
    while queue:
        state = queue.popleft()
        stage, known, used = state
        trace = paths[state]
        if stage >= check_after:
            eligible += 1
            private = model.private(known, targets)
            private_count += private
            if not private and privacy_witness is None:
                privacy_witness = {"trace":trace,"known_seed_atoms":sorted(x for x in known if x.startswith("seed:")),
                                   "observation_atoms":sorted(x for x in known if x.startswith(("obs:","commit:")))}
            if any(f"seed:{e}" in known for e in targets) and reconstruction_witness is None:
                reconstruction_witness = {"trace":trace,"known_seed_atoms":sorted(x for x in known if x.startswith("seed:"))}
        successors = []
        if stage < len(steps):
            atom, label = steps[stage]
            successors.append(((stage+1, model.close(known | {atom}), used), label))
        for i, leak in enumerate(leaks):
            if i in used or not leak.earliest <= stage <= leak.latest:
                continue
            if leak.needs and leak.needs not in known:
                continue
            count = sum(leaks[j].group == leak.group for j in used)
            if count >= leak.limit:
                continue
            successors.append(((stage, model.close(known | {leak.atom}), used | {i}),
                               f"{leak.kind}({leak.atom}); attacker retains copy"))
        for new, label in successors:
            edges += 1
            assert known <= new[1], "Adversary knowledge must be monotone"
            if new not in paths:
                paths[new] = trace+[label]
                queue.append(new)
    result = {"name":name,"states":len(paths),"transitions":edges,"checked_states":eligible,
              "private_states":private_count,"all_checked_states_private":private_count==eligible,
              "shortest_privacy_counterexample":privacy_witness,
              "shortest_linear_reconstruction_counterexample":reconstruction_witness,
              "scope":"declared linear observations and symbolic opens; privacy conditioned on other seed values"}
    assert result["all_checked_states_private"] == expected_private, name
    return result


def bank_leaks(bank, n, budget=2, latest=1):
    return [Leak(f"bank-copy:{bank}:{h}","CopyBank",bank,budget,latest=latest) for h in range(1,n+1)]


def main():
    results = []
    for shared in [False, True]:
        spec=[(0,0,3,2,"old","r0"),(0,1,3,2,"new","r0" if shared else "r1")]
        steps=[("published:0:0","Publish(epoch=0,generation=0)"),("published:0:1","Refresh(epoch=0,generation=1)")]
        leaks=[Leak(f"pair:0:{g}:{h}","CopyShare",f"generation:{g}",1,needs=f"published:0:{g}")
               for g in range(2) for h in range(1,4)]
        results.append(explore("correlated_refresh_randomness" if shared else "independent_share_refresh",
                               spec,steps,leaks,{0},2,not shared))
    for renew in [False,True]:
        spec=[(0,0,3,2,"old","e0"),(1,0,3,2,"clean" if renew else "old","e1")]
        steps=[("published:0:0","Publish(old epoch=0)"),("published:1:0","Publish(fresh epoch=1)")]
        results.append(explore("renewed_recipient_bank" if renew else "fresh_seed_stolen_future_bank",
                               spec,steps,bank_leaks("old",3),{1},2,renew))
    spec=[(0,0,3,3,"old","r0"),(0,1,3,2,"old","r1")]
    results.append(explore("threshold_lowered_with_reused_recipients",spec,
                           [("published:0:0","Publish(threshold=3)"),("published:0:1","Refresh(threshold=2)")],
                           bank_leaks("old",3),{0},2,False))
    spec=[(0,0,3,2,"old","r0"),(0,1,3,2,"clean","r1")]
    results.append(explore("known_seed_not_revoked_by_refresh",spec,
                           [("published:0:0","Publish(generation=0)"),("published:0:1","Refresh(independent bank and masks)")],
                           [Leak("client-copy:0","CompromiseRecoveredClient","client",1,earliest=1,latest=1)],{0},2,False))
    spec=[(0,0,3,2,"old","r0"),(1,0,3,2,"clean","r1")]
    results.append(explore("recovered_client_exposure",spec,
                           [("published:0:0","Publish(epoch=0)"),("published:1:0","Publish(epoch=1)")],
                           [Leak("client-copy:1","CompromiseRecoveredClient","client",1,earliest=2)],{1},2,False))
    spec=[(0,0,3,2,"old","r0")]
    results.append(explore("archive_after_ordinary_erasure",spec,
                           [("published:0:0","Publish(epoch=0)"),("archive-capsule:0","Complete ordinary-path erasure; retain archive capsule")],
                           [Leak("archive-key:0","CompromiseArchiveAuthority","archive",1)],{0},2,False))
    print(json.dumps({"scenarios":results,"total_states":sum(r["states"] for r in results),
                      "total_transitions":sum(r["transitions"] for r in results),
                      "shortest_traces":"BFS, unit-cost named actions, each run separately"},indent=2))


if __name__ == "__main__":
    main()
