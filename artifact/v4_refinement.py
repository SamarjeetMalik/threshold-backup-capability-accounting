"""v4: a Python transcription of RecoveryLifecycleV4.tla (all guards TRUE) and a
bounded refinement-conformance check of the reference kernel against it.

1. The transcription is validated by exhaustive breadth-first search: its
   reachable-state counts must equal TLC's distinct-state counts for the same
   constants (recorded in expected/v4_tlc_results.json).
2. An abstraction function maps every kernel state to an abstract state, using
   one history variable (`held`). Seeded random schedules of kernel calls are
   executed; after each call the abstract state must be unchanged (stutter) or
   reachable from the previous one in at most three abstract steps. This is
   testing of a refinement mapping on bounded schedules, not a proof.
"""
from collections import deque, Counter
import random

ACTIVE = ("holding", "decrypting", "queued", "sending")


class Abstract:
    def __init__(self, EC, GC, RC):
        self.EC, self.GC, self.RC = EC, GC, RC
        self.paths = [(e, g) for e in range(EC) for g in range(GC)]
        self.reqs = list(range(1, RC + 1))

    def path(self, r):
        return ((r - 1) % self.EC, ((r - 1) // self.EC) % self.GC)

    # state: dict of immutables -> frozen as tuple for hashing
    def init(self):
        return dict(phase={p: "sealed" for p in self.paths}, slots=frozenset(self.paths),
                    tomb=frozenset(), receipts=frozenset(), pending=frozenset(),
                    committed=frozenset(), floor=0, highwater=0, config=0, crashed=False,
                    stage={r: "idle" for r in self.reqs}, requestConfig={r: 0 for r in self.reqs},
                    endpoint={r: 0 for r in self.reqs}, cert={r: 0 for r in self.reqs},
                    held=frozenset(), buffers=frozenset(), delivered=frozenset(),
                    badExpiry=False, badBinding=False, ic=False)

    @staticmethod
    def freeze(s):
        return tuple((k, tuple(sorted(v.items())) if isinstance(v, dict) else v) for k, v in sorted(s.items()))

    def live(self, s, r):
        p = self.path(r)
        return s["phase"][p] == "sealed" and p not in s["tomb"]

    def bound(self, s, r):
        return (s["cert"][r] == 1 and s["endpoint"][r] == 0 and s["requestConfig"][r] == s["config"]
                and r in s["held"])

    def completed(self, committed):
        return sum(1 for e in range(self.EC) if all((e, g) in committed for g in range(self.GC)))

    def successors(self, s):
        out = []
        def nxt(**ch):
            t = dict(s)
            for k, v in ch.items():
                t[k] = v
            out.append(t)
        def upd(d, k, v):
            d = dict(d); d[k] = v; return d
        def cancel_to(stage, r):
            return "aborting" if stage[r] == "decrypting" else "cancelled"
        c = s["crashed"]
        for r in self.reqs:
            st = s["stage"][r]
            if not c and st == "idle" and self.live(s, r):
                nxt(stage=upd(s["stage"], r, "holding"), requestConfig=upd(s["requestConfig"], r, s["config"]))
            if not c and st in ACTIVE and r not in s["held"]:
                nxt(held=s["held"] | {r})
            if not c and st in ACTIVE and s["endpoint"][r] == 0:
                nxt(endpoint=upd(s["endpoint"], r, 1))
            if not c and st == "holding" and self.live(s, r) and self.path(r) in s["slots"] and self.bound(s, r):
                nxt(stage=upd(s["stage"], r, "decrypting"))
            if not c and st == "decrypting" and self.live(s, r) and self.bound(s, r):
                nxt(buffers=s["buffers"] | {r}, stage=upd(s["stage"], r, "queued"))
            if st == "aborting":
                nxt(stage=upd(s["stage"], r, "cancelled"))
            if st == "decrypting":
                nxt(stage=upd(s["stage"], r, "cancelled"))
            if not c and st == "queued" and r in s["buffers"]:
                nxt(stage=upd(s["stage"], r, "sending"))
            if not c and st == "sending" and r in s["buffers"] and self.live(s, r) and self.bound(s, r):
                nxt(stage=upd(s["stage"], r, "done"), delivered=s["delivered"] | {r},
                    buffers=s["buffers"] - {r}, badExpiry=s["badExpiry"] or not self.live(s, r),
                    badBinding=s["badBinding"] or not self.bound(s, r))
            for cv in (1, 2):
                if not c and st in ACTIVE and s["cert"][r] == 0:
                    nxt(cert=upd(s["cert"], r, cv))
        for e in self.paths:
            if not c and s["phase"][e] == "sealed":
                nxt(tomb=s["tomb"] | {e}, phase=upd(s["phase"], e, "expiring"),
                    stage={r: (cancel_to(s["stage"], r) if self.path(r) == e and s["stage"][r] in ACTIVE
                               else s["stage"][r]) for r in self.reqs},
                    buffers=frozenset(r for r in s["buffers"] if self.path(r) != e))
            if not c and s["phase"][e] == "expiring" and e in s["slots"]:
                nxt(slots=s["slots"] - {e})
            if (not c and s["phase"][e] == "expiring" and e not in s["receipts"] and e not in s["slots"]
                    and all(self.path(r) != e for r in s["buffers"])
                    and all(not (self.path(r) == e and s["stage"][r] == "aborting") for r in self.reqs)):
                nxt(receipts=s["receipts"] | {e})
            if not c and e in s["receipts"] and e not in s["pending"] and e not in s["committed"]:
                nxt(pending=s["pending"] | {e})
            if (not c and e in s["pending"] and e not in s["committed"]
                    and all(d in s["committed"] for d in self.paths if d[0] < e[0])):
                com = s["committed"] | {e}
                f = self.completed(com)
                nxt(committed=com, pending=s["pending"] - {e}, phase=upd(s["phase"], e, "erased"),
                    floor=f, highwater=f)
        if not c and s["config"] == 0:
            nxt(config=1, buffers=frozenset(),
                stage={r: (cancel_to(s["stage"], r) if s["stage"][r] in ACTIVE else s["stage"][r]) for r in self.reqs})
        if not s["ic"]:
            nxt(ic=True)
        if not c:
            nxt(crashed=True, buffers=frozenset(),
                stage={r: ("cancelled" if s["stage"][r] in ACTIVE + ("aborting",) else s["stage"][r]) for r in self.reqs})
        if c:
            nxt(crashed=False)
        if c and not s["tomb"] and s["config"] == 0 and s["floor"] == 0:
            nxt(crashed=False, phase={p: "sealed" for p in self.paths}, slots=frozenset(self.paths),
                tomb=frozenset(), floor=0, config=0)
        return out

    def count_reachable(self):
        start = self.init()
        seen = {self.freeze(start)}
        q = deque([start])
        while q:
            s = q.popleft()
            for t in self.successors(s):
                k = self.freeze(t)
                if k not in seen:
                    seen.add(k)
                    q.append(t)
        return len(seen)

    def reachable_within(self, s, target, depth=3):
        goal = self.freeze(target)
        if self.freeze(s) == goal:
            return 0
        frontier, seen = [s], {self.freeze(s)}
        for d in range(1, depth + 1):
            nxt = []
            for u in frontier:
                for v in self.successors(u):
                    k = self.freeze(v)
                    if k == goal:
                        return d
                    if k not in seen:
                        seen.add(k)
                        nxt.append(v)
            frontier = nxt
        return None


def abstraction(kernel, model, held):
    a = kernel.anchor
    st, rc, ce, buf = {}, {}, {}, set()
    inflight = {tok[0] for tok in kernel.inflight} if hasattr(kernel, "inflight") else set()
    for r in model.reqs:
        job = kernel.jobs.get(f"r{r}")
        if job is None:
            st[r], rc[r], ce[r] = "idle", 0, 0
            continue
        stage = job.stage
        if stage == "cancelled" and f"r{r}" in inflight:
            stage = "aborting"
        st[r], rc[r], ce[r] = stage, job.request.configuration, 1 if job.certificate else 0
        if job.buffer is not None:
            buf.add(r)
    paths = model.paths
    return dict(phase={p: a.epochs[p].phase for p in paths},
                slots=frozenset(p for p in paths if a.epochs[p].slot),
                tomb=frozenset(a.tombstones), receipts=frozenset(p for p in paths if a.epochs[p].receipt),
                pending=frozenset(p for p in paths if a.epochs[p].proposed and not a.epochs[p].committed),
                committed=frozenset(p for p in paths if a.epochs[p].committed),
                floor=a.floor, highwater=a.highwater, config=a.configuration, crashed=kernel.crashed,
                stage=st, requestConfig=rc, endpoint={r: 0 for r in model.reqs}, cert=ce,
                held=frozenset(held), buffers=frozenset(buf),
                delivered=frozenset(int(ev[0].nonce[1:]) for ev in kernel.delivered),
                badExpiry=False, badBinding=False, ic=False)


def conformance(kmod, EC=2, GC=1, RC=2, schedules=400, length=40, seed=31):
    """Run seeded random schedules of kernel calls; report divergences."""
    model = Abstract(EC, GC, RC)
    rng = random.Random(seed)
    stats = Counter()
    examples = []
    for sch in range(schedules):
        clock = {"now": 0}
        k = kmod.ReferenceKernel(epoch_keys=tuple(model.paths), clock=lambda: clock["now"])
        held, tokens, config_proposed = set(), [], False
        prev = abstraction(k, model, held)
        history = []
        for step in range(length):
            r = rng.choice(model.reqs)
            e = rng.choice(model.paths)
            ep, gen = model.path(r)
            op = rng.choice(["register", "authorize", "tick", "begin", "finish", "finish", "abandon",
                             "send", "transfer", "expire", "erase", "receipt", "propose", "commit",
                             "propose_config", "commit_config", "crash", "restart"])
            req = kmod.Request("acct", f"r{r}", ep, gen, k.anchor.configuration, b"recipient", b"manifest")
            try:
                if op == "register":
                    k.register(req)
                elif op == "authorize":
                    job = k.jobs.get(f"r{r}")
                    if job:
                        k.authorize(job.request.nonce, kmod.Certificate(job.request.digest, (1, 2), job.request.configuration))
                elif op == "tick":
                    clock["now"] += 24
                elif op == "begin":
                    tokens.append(k.begin_decrypt(f"r{r}", k.checkpoint(f"r{r}")))
                elif op == "finish" and tokens:
                    k.finish_decrypt(rng.choice(tokens), b"pair")
                elif op == "abandon" and tokens and hasattr(k, "abandon_decrypt"):
                    k.abandon_decrypt(rng.choice(tokens))
                elif op == "send":
                    k.begin_send(f"r{r}", k.checkpoint(f"r{r}"))
                elif op == "transfer":
                    k.first_byte_transfer(f"r{r}", k.checkpoint(f"r{r}"))
                elif op == "expire":
                    k.begin_expiry(e)
                elif op == "erase":
                    k.erase_slot(e)
                elif op == "receipt":
                    k.sign_receipt(e)
                elif op == "propose":
                    k.propose_barrier(e)
                elif op == "commit":
                    k.commit_barrier(e)
                elif op == "propose_config" and not config_proposed:
                    k.propose_configuration(1); config_proposed = True
                elif op == "commit_config":
                    k.commit_configuration()
                elif op == "crash":
                    k.crash()
                elif op == "restart":
                    k.restart()
            except (kmod.Rejected, KeyError):
                pass
            # history variable: hold elapsed while the job was active and the kernel up
            if not k.crashed:
                for rr in model.reqs:
                    job = k.jobs.get(f"r{rr}")
                    if job and job.stage in ACTIVE and clock["now"] - job.started >= k.hold:
                        held.add(rr)
            cur = abstraction(k, model, held)
            history.append(op)
            d = model.reachable_within(prev, cur)
            stats["steps"] += 1
            if d is None:
                stats["divergent_steps"] += 1
                stats["cause_" + op] += 1
                if len(examples) < 5:
                    diff = {key: (prev[key], cur[key]) for key in cur if prev[key] != cur[key]}
                    examples.append({"schedule": sch, "after": history[-6:], "changed": str(diff)[:300]})
                prev = cur
                stats["divergent_schedules_marker"] += 1
                break
            stats[f"abstract_steps_{d}"] += 1
            prev = cur
        stats["schedules"] += 1
    stats.pop("divergent_schedules_marker", None)
    causes = {k[6:]: v for k, v in sorted(stats.items()) if k.startswith("cause_")}
    return {"schedules": stats["schedules"], "kernel_steps": stats["steps"], "divergence_causes": causes,
            "stutter_steps": stats["abstract_steps_0"], "one_step": stats["abstract_steps_1"],
            "two_step": stats["abstract_steps_2"], "three_step": stats["abstract_steps_3"],
            "divergent_schedules": stats["divergent_steps"], "examples": examples}


if __name__ == "__main__":
    import json, importlib.util, sys
    from pathlib import Path
    out = {"state_counts": {f"{e}-{g}-{r}": Abstract(e, g, r).count_reachable()
                            for e, g, r in [(1, 1, 1), (2, 1, 1), (1, 1, 2)]}}
    import lifecycle_kernel as v4k
    out["kernel_v4"] = conformance(v4k, schedules=2000)
    spec = importlib.util.spec_from_file_location("k3", Path(__file__).parent / "baseline_v3" / "lifecycle_kernel.py")
    k3 = importlib.util.module_from_spec(spec); spec.loader.exec_module(k3)
    out["kernel_v3"] = conformance(k3, schedules=2000)
    print(json.dumps(out, indent=2))
