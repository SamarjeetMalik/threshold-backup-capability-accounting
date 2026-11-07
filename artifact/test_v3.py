"""v3 regression tests. Each covers a property no v2 test exercised."""
import importlib.util
import unittest
from dataclasses import replace
from pathlib import Path
from threading import Event, Thread

from lifecycle_kernel import ReferenceKernel, Request, Certificate, Rejected
import v3_leakage, v3_erasure, v3_temporal


def load_v2_kernel():
    path = Path(__file__).resolve().parent / "baseline_v2" / "lifecycle_kernel.py"
    spec = importlib.util.spec_from_file_location("lifecycle_kernel_v2", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class Clock:
    def __init__(self):self.now=0
    def __call__(self):return self.now


def prepared(module):
    clock=Clock()
    k=module.ReferenceKernel(clock=clock)
    r=module.Request("acct","r",0,0,0,b"recipient",b"manifest")
    k.register(r)
    k.authorize(r.nonce,module.Certificate(r.digest,(1,2),r.configuration))
    clock.now=24
    return k,r


def paused_worker(k,r):
    begun,resume,result=Event(),Event(),[]
    def worker():
        token=k.begin_decrypt(r.nonce,k.checkpoint(r.nonce))
        begun.set()
        if not resume.wait(5):raise RuntimeError("test schedule timeout")
        result.append(k.finish_decrypt(token,b"pair"))
    thread=Thread(target=worker);thread.start()
    assert begun.wait(5)
    return thread,resume,result


class InflightWorkerTests(unittest.TestCase):
    def test_receipt_waits_for_cancelled_worker(self):
        import lifecycle_kernel as v3
        k,r=prepared(v3)
        thread,resume,result=paused_worker(k,r)
        k.begin_expiry((0,0));k.erase_slot((0,0))
        with self.assertRaises(Rejected):k.sign_receipt((0,0))
        resume.set();thread.join(5)
        self.assertEqual(result,[False])
        k.sign_receipt((0,0))
        self.assertTrue(k.anchor.epochs[(0,0)].receipt and k.invariant())

    def test_v2_kernel_signed_receipt_with_worker_running(self):
        """Documents the v2 defect: the receipt precedes the worker's return."""
        v2=load_v2_kernel()
        k,r=prepared(v2)
        thread,resume,result=paused_worker(k,r)
        k.begin_expiry((0,0));k.erase_slot((0,0))
        k.sign_receipt((0,0))  # accepted while decrypted material may exist
        self.assertTrue(k.anchor.epochs[(0,0)].receipt)
        resume.set();thread.join(5)
        self.assertEqual(result,[False])

    def test_abandoned_worker_releases_receipt(self):
        import lifecycle_kernel as v3
        k,r=prepared(v3)
        token=k.begin_decrypt(r.nonce,k.checkpoint(r.nonce))
        k.begin_expiry((0,0));k.erase_slot((0,0))
        with self.assertRaises(Rejected):k.sign_receipt((0,0))
        k.abandon_decrypt(token)
        k.sign_receipt((0,0))

    def test_inflight_on_other_path_does_not_block_receipt(self):
        import lifecycle_kernel as v3
        clock=Clock();k=v3.ReferenceKernel(epoch_keys=((0,0),(1,0)),clock=clock)
        r=v3.Request("acct","r",1,0,0,b"recipient",b"manifest")
        k.register(r);k.authorize(r.nonce,v3.Certificate(r.digest,(1,2),0));clock.now=24
        k.begin_decrypt(r.nonce,k.checkpoint(r.nonce))
        k.begin_expiry((0,0));k.erase_slot((0,0));k.sign_receipt((0,0))

    def test_crash_ends_workers(self):
        import lifecycle_kernel as v3
        k,r=prepared(v3)
        token=k.begin_decrypt(r.nonce,k.checkpoint(r.nonce))
        k.crash();k.restart()
        k.begin_expiry((0,0));k.erase_slot((0,0));k.sign_receipt((0,0))
        self.assertFalse(k.finish_decrypt(token,b"pair"))

    def test_unknown_nonce_is_rejection_not_crash(self):
        import lifecycle_kernel as v3
        k,_=prepared(v3)
        for call in (lambda:k.authorize("missing",None),
                     lambda:k.begin_decrypt("missing",k.checkpoint("missing")),
                     lambda:k.begin_send("missing",k.checkpoint("missing"))):
            with self.assertRaises(Rejected):call()


class MathematicalChecks(unittest.TestCase):
    def test_leakage_subspace_theorem(self):
        out=v3_leakage.check_leakage_theorem(trials=800)
        self.assertEqual(out["random_instances"],800)

    def test_partial_openings_count_indices_not_pairs(self):
        out=v3_leakage.check_partial_openings()
        self.assertFalse(out["half_opening_counterexample"]["private"])
        self.assertGreater(out["patterns_where_v2_pair_count_mispredicts"],0)

    def test_privacy_is_blockwise_reconstruction_is_not(self):
        out=v3_leakage.check_block_lemma(trials=600)
        self.assertGreater(out["joint_only_reconstruction_cases"],0)

    def test_read_once_erasure_is_exact(self):
        v3_erasure.check_read_once(trials=400)

    def test_shared_root_breaks_treewise_evaluation(self):
        out=v3_erasure.check_shared_roots()
        self.assertEqual((out["treewise_value"],out["true_minimum"]),(2,1))

    def test_reused_bank_erasure_is_vertex_cover(self):
        v3_erasure.check_vertex_cover_reduction(trials=60)

    def test_healing_classification(self):
        cells={c["scenario"]:c["target_private"] for c in v3_temporal.healing_matrix()}
        self.assertFalse(cells["copied bank, refresh under same bank"])
        self.assertTrue(cells["copied bank, refresh under renewed bank"])

    def test_committee_closed_form(self):
        self.assertEqual(v3_temporal.check_committees()["closed_form_conservative_cases"],0)


if __name__=="__main__":
    unittest.main()
