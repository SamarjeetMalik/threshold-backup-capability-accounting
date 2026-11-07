"""v4 regression tests. Kernel tests document each v3 divergence found by the
refinement-conformance check and show that the v4 kernel removes it."""
import importlib.util
import unittest
from pathlib import Path

import lifecycle_kernel as v4
import v4_leakage, v4_erasure, v4_temporal, v4_quorum, v4_refinement, v401_patterns, v402_checks, v403_checks


def load_v3():
    path = Path(__file__).resolve().parent / "baseline_v3" / "lifecycle_kernel.py"
    spec = importlib.util.spec_from_file_location("lifecycle_kernel_v3", path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m


class Clock:
    def __init__(self): self.now = 0
    def __call__(self): return self.now


def prepared(m, keys=((0, 0),), epoch=0):
    c = Clock(); k = m.ReferenceKernel(epoch_keys=keys, clock=c)
    r = m.Request("acct", "r", epoch, 0, 0, b"recipient", b"manifest")
    k.register(r); k.authorize("r", m.Certificate(r.digest, (1, 2), 0)); c.now = 24
    return k, r


class KernelV4(unittest.TestCase):
    def test_duplicate_completion_does_not_cancel_queued_work(self):
        for m, survives in ((load_v3(), False), (v4, True)):
            k, r = prepared(m)
            tok = k.begin_decrypt("r", k.checkpoint("r"))
            self.assertTrue(k.finish_decrypt(tok, b"pair"))
            k.finish_decrypt(tok, b"pair")  # duplicate message
            self.assertEqual(k.jobs["r"].stage == "queued", survives)

    def test_stale_abandon_does_not_cancel_later_work(self):
        for m, survives in ((load_v3(), False), (v4, True)):
            k, r = prepared(m)
            tok = k.begin_decrypt("r", k.checkpoint("r"))
            k.finish_decrypt(tok, b"pair")
            k.abandon_decrypt(tok)
            self.assertEqual(k.jobs["r"].stage == "queued", survives)

    def test_commit_requires_earlier_epochs(self):
        for m, allowed in ((load_v3(), True), (v4, False)):
            k = m.ReferenceKernel(epoch_keys=((0, 0), (1, 0)), clock=Clock())
            k.begin_expiry((1, 0)); k.erase_slot((1, 0)); k.sign_receipt((1, 0)); k.propose_barrier((1, 0))
            try:
                k.commit_barrier((1, 0)); ok = True
            except m.Rejected:
                ok = False
            self.assertEqual(ok, allowed)
            self.assertEqual(k.anchor.floor, 0)  # the floor was safe in both versions

    def test_authorize_rejected_after_cancellation(self):
        k = v4.ReferenceKernel(clock=Clock())
        r = v4.Request("acct", "r", 0, 0, 0, b"recipient", b"manifest")
        k.register(r); k.begin_expiry((0, 0))
        with self.assertRaises(v4.Rejected):
            k.authorize("r", v4.Certificate(r.digest, (1, 2), 0))

    def test_certificate_cannot_be_replaced(self):
        k, r = prepared(v4)
        k.authorize("r", v4.Certificate(r.digest, (1, 2), 0))  # identical: idempotent
        with self.assertRaises(v4.Rejected):
            k.authorize("r", v4.Certificate(r.digest, (2, 3), 0))

    def test_refinement_conformance_v4_kernel(self):
        out = v4_refinement.conformance(v4, schedules=150)
        self.assertEqual(out["divergent_schedules"], 0)


class MathV4(unittest.TestCase):
    def test_marginal_conditional_leakage(self):
        v4_leakage.check_marginal_conditional(trials=300)

    def test_uniform_masks_are_necessary(self):
        out = v4_leakage.check_nonuniform_mask()
        self.assertTrue(out["rank_test_private"] and out["supports_differ"])

    def test_acceptance_must_be_transcript_measurable(self):
        self.assertTrue(v4_leakage.check_acceptance_measurability()["mask_dependent_acceptance_leaks"])

    def test_selection_and_weighted_thresholds(self):
        v4_erasure.check_selection(trials=300); v4_erasure.check_weighted_threshold(trials=300)

    def test_fixed_generation_algorithm(self):
        v4_erasure.check_fixed_generations(trials=80)

    def test_random_histories(self):
        out = v4_temporal.check_random_histories(histories=400)
        self.assertGreater(out["independent_targets"], 0)

    def test_domain_corruption(self):
        v4_quorum.check_domains(trials=400)

    def test_guessing_space_covers_reachable_patterns(self):
        out = v401_patterns.check(policies=60)
        self.assertEqual(out["reuse_example"]["reachable"], 5)

    def test_object_versus_chunk_accounting(self):
        out = v402_checks.check_accounting(workloads=60)
        self.assertGreater(out["D_exceeds_r"], 0)

    def test_reused_bank_pattern_closed_form(self):
        out = v402_checks.check_reuse_closed_form(cases=40)
        self.assertEqual(out["table"][0]["reachable"], 5)

    def test_exact_reused_bank_count_partial_publication(self):
        out = v403_checks.check(cases=60)
        self.assertEqual(out["example"]["partial_publication_exact"], 36)

    def test_transcription_matches_tlc_small(self):
        self.assertEqual(v4_refinement.Abstract(2, 1, 1).count_reachable(), 5584)


if __name__ == "__main__":
    unittest.main()
