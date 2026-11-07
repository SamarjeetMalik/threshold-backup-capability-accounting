import unittest
from dataclasses import replace
from threading import Event, Thread
from lifecycle_kernel import ReferenceKernel, Request, Certificate, Rejected, cbor
from capability import sharing_model, in_rowspan, privacy_holds


class Clock:
    def __init__(self):self.now=0
    def __call__(self):return self.now


class LifecycleTests(unittest.TestCase):
    def fresh(self, **options):
        clock=Clock()
        return ReferenceKernel(clock=clock,**options),clock

    def req(self,nonce="r",**changes):
        return replace(Request("acct",nonce,0,0,0,b"recipient",b"manifest"),**changes)

    def prepare(self,k,c,request=None,signers=(1,2)):
        r=request or self.req()
        k.register(r)
        k.authorize(r.nonce,Certificate(r.digest,signers,r.configuration))
        c.now=24
        return r

    def queue(self,k,r):
        token=k.begin_decrypt(r.nonce,k.checkpoint(r.nonce))
        self.assertTrue(k.finish_decrypt(token,b"share-and-opening"))
        return token

    def test_mandatory_hold_after_immediate_approval(self):
        k,c=self.fresh();r=self.prepare(k,c);c.now=23
        with self.assertRaises(Rejected):k.begin_decrypt(r.nonce,k.checkpoint(r.nonce))
        c.now=24
        self.queue(k,r)

    def test_replayed_certificate_rejected(self):
        k,c=self.fresh();r=self.prepare(k,c);r2=self.req("second")
        k.register(r2)
        with self.assertRaises(Rejected):k.authorize(r2.nonce,Certificate(r.digest,(1,2),0))

    def test_changed_recipient_or_request_fields(self):
        for field,value in [("recipient",b"attacker"),("account","other"),("manifest",b"other"),
                            ("bank",1),("epoch",1),("generation",1),("domain","archive")]:
            with self.subTest(field=field):
                k,c=self.fresh();r=self.prepare(k,c)
                with self.assertRaises(Rejected):k.register(replace(r,**{field:value}))

    def test_duplicate_requests_idempotent_but_not_new_votes(self):
        k,c=self.fresh();r=self.req()
        self.assertIs(k.register(r),k.register(r))
        with self.assertRaises(Rejected):k.authorize(r.nonce,Certificate(r.digest,(1,1),0))

    def test_unknown_or_unverified_approval_rejected(self):
        k,c=self.fresh();r=self.req();k.register(r)
        for certificate in [Certificate(r.digest,(1,99),0),Certificate(r.digest,(1,2),0,verified=False),Certificate(r.digest,(1,2),0,committed=False)]:
            with self.assertRaises(Rejected):k.authorize(r.nonce,certificate)

    def test_stale_checkpoint(self):
        k,c=self.fresh();r=self.prepare(k,c);old=k.checkpoint(r.nonce)
        k.propose_configuration(1)
        with self.assertRaises(Rejected):k.begin_decrypt(r.nonce,old)

    def test_expiry_at_every_owned_response_stage(self):
        for stage in ["holding","decrypting","queued","sending"]:
            with self.subTest(stage=stage):
                k,c=self.fresh();r=self.prepare(k,c);token=None
                if stage!="holding":token=k.begin_decrypt(r.nonce,k.checkpoint(r.nonce))
                if stage in ("queued","sending"):self.assertTrue(k.finish_decrypt(token,b"pair"))
                if stage=="sending":k.begin_send(r.nonce,k.checkpoint(r.nonce))
                k.begin_expiry((0,0))
                if stage=="decrypting":self.assertFalse(k.finish_decrypt(token,b"pair"))
                with self.assertRaises(Rejected):k.first_byte_transfer(r.nonce,k.checkpoint(r.nonce))
                self.assertEqual(k.delivered,[])
                self.assertTrue(k.invariant())

    def test_real_thread_expiry_during_decryption(self):
        k,c=self.fresh();r=self.prepare(k,c)
        begun=Event();resume=Event();result=[]
        def worker():
            token=k.begin_decrypt(r.nonce,k.checkpoint(r.nonce))
            begun.set()
            if not resume.wait(5):raise RuntimeError("test schedule timeout")
            result.append(k.finish_decrypt(token,b"pair"))
        thread=Thread(target=worker);thread.start()
        self.assertTrue(begun.wait(5));k.begin_expiry((0,0));resume.set();thread.join(5)
        self.assertFalse(thread.is_alive());self.assertEqual(result,[False]);self.assertEqual(k.delivered,[])
        self.assertTrue(k.invariant())

    def test_queued_buffer_logically_overwritten_before_receipt(self):
        k,c=self.fresh();r=self.prepare(k,c);self.queue(k,r)
        buffer=k.jobs[r.nonce].buffer
        k.begin_expiry((0,0));k.erase_slot((0,0));k.sign_receipt((0,0))
        self.assertTrue(all(x==0 for x in buffer));self.assertTrue(k.invariant())

    def test_interrupted_send_after_first_byte_is_counted_as_disclosure(self):
        k,c=self.fresh();r=self.prepare(k,c);self.queue(k,r)
        k.begin_send(r.nonce,k.checkpoint(r.nonce));k.first_byte_transfer(r.nonce,k.checkpoint(r.nonce))
        k.begin_expiry((0,0));k.crash();k.restart()
        self.assertEqual(len(k.delivered),1);self.assertTrue(k.invariant())

    def test_crash_at_each_durable_expiry_stage(self):
        steps=["begin_expiry","erase_slot","sign_receipt","propose_barrier","commit_barrier"]
        for upto in range(1,len(steps)+1):
            with self.subTest(after=steps[upto-1]):
                k,c=self.fresh()
                for method in steps[:upto]:getattr(k,method)((0,0))
                k.crash();k.restart()
                with self.assertRaises(Rejected):k.register(self.req())
                self.assertTrue(k.invariant())

    def test_receipt_requires_prior_cleanup(self):
        k,c=self.fresh()
        with self.assertRaises(Rejected):k.sign_receipt((0,0))
        k.begin_expiry((0,0))
        with self.assertRaises(Rejected):k.sign_receipt((0,0))

    def test_old_disk_snapshot_rejected_even_before_floor_advances(self):
        for complete in [False,True]:
            k,c=self.fresh();old=k.snapshot();k.begin_expiry((0,0))
            if complete:
                k.erase_slot((0,0));k.sign_receipt((0,0));k.propose_barrier((0,0));k.commit_barrier((0,0))
            k.crash()
            with self.assertRaises(Rejected):k.restart(old)
            k.restart();self.assertTrue(k.invariant())

    def test_incomplete_log_commit_survives_crash_without_activation(self):
        k,c=self.fresh();k.propose_configuration(1);k.crash();k.restart()
        self.assertEqual(k.anchor.configuration,0)
        with self.assertRaises(Rejected):k.register(self.req(configuration=1))
        k.register(self.req());k.commit_configuration()
        self.assertEqual(k.anchor.configuration,1)
        self.assertEqual(k.jobs['r'].stage,'cancelled')

    def test_pending_barrier_is_not_committed_floor(self):
        k,c=self.fresh();k.begin_expiry((0,0));k.erase_slot((0,0));k.sign_receipt((0,0));k.propose_barrier((0,0))
        k.crash();k.restart();self.assertEqual(k.anchor.floor,0)
        k.commit_barrier((0,0));self.assertEqual(k.anchor.floor,1)

    def test_configuration_change_cancels_queued_old_work(self):
        k,c=self.fresh();r=self.prepare(k,c);self.queue(k,r)
        k.propose_configuration(1);k.commit_configuration()
        with self.assertRaises(Rejected):k.first_byte_transfer(r.nonce,k.checkpoint(r.nonce))
        self.assertTrue(k.invariant())

    def test_two_generations_require_both_barriers_before_epoch_floor(self):
        k,c=self.fresh(epoch_keys=((0,0),(0,1),(1,0)))
        r=self.prepare(k,c);self.queue(k,r)
        r2=self.req("second",generation=1);k.register(r2)
        k.authorize(r2.nonce,Certificate(r2.digest,(1,2),0));c.now=48
        self.queue(k,r2)
        for method in ["begin_expiry","erase_slot","sign_receipt","propose_barrier","commit_barrier"]:
            getattr(k,method)((0,0))
        self.assertEqual(k.anchor.floor,0)
        self.assertIsNotNone(k.jobs[r2.nonce].buffer)
        for method in ["begin_expiry","erase_slot","sign_receipt","propose_barrier","commit_barrier"]:
            getattr(k,method)((0,1))
        self.assertEqual(k.anchor.floor,1)
        self.assertTrue(k.anchor.epochs[(1,0)].slot);self.assertTrue(k.invariant())

    def test_byzantine_refusal_does_not_create_fail_open(self):
        k,c=self.fresh(approval_quorum=3);r=self.req();k.register(r)
        with self.assertRaises(Rejected):k.authorize(r.nonce,Certificate(r.digest,(2,3),0))
        c.now=999
        with self.assertRaises(Rejected):k.begin_decrypt(r.nonce,k.checkpoint(r.nonce))
        k2,c2=self.fresh();r2=self.prepare(k2,c2,signers=(2,3));self.queue(k2,r2)

    def test_identity_only_compromise_and_genuine_false_quorum(self):
        k,c=self.fresh();r=self.req(recipient=b"attacker");k.register(r)
        with self.assertRaises(Rejected):k.authorize(r.nonce,Certificate(r.digest,(1,),0))
        k.authorize(r.nonce,Certificate(r.digest,(1,2),0));c.now=24
        self.queue(k,r);k.begin_send(r.nonce,k.checkpoint(r.nonce))
        delivered=k.first_byte_transfer(r.nonce,k.checkpoint(r.nonce))
        self.assertEqual(delivered[0].recipient,b"attacker")

    def test_monotone_clock_failure_closes_release(self):
        k,c=self.fresh();r=self.prepare(k,c);c.now=-1
        with self.assertRaises(Rejected):k.begin_decrypt(r.nonce,k.checkpoint(r.nonce))

    def test_core_deterministic_cbor_vector_and_schema_limits(self):
        self.assertEqual(cbor({-1:0,24:0}).hex(),"a21818002000")
        self.assertEqual(cbor([1,b"a","b",True]).hex(),"840141616162f5")
        with self.assertRaises(TypeError):cbor(1.5)
        with self.assertRaises(ValueError):cbor(1<<64)


class CapabilityTests(unittest.TestCase):
    def test_no_ordinary_graph_or_semantics(self):
        m=sharing_model([(0,0,3,2,"old","r")],p=7)
        self.assertNotIn("pair:0:0:1",m.close({"published:0:0"}))
        self.assertNotIn("pair:0:0:1",m.close({"bank-copy:old:1"}))
        self.assertIn("pair:0:0:1",m.close({"published:0:0","bank-copy:old:1"}))

    def test_known_seed_is_not_revoked(self):
        m=sharing_model([(0,0,3,2,"old","a"),(0,1,3,3,"new","b")],p=7)
        k={"published:0:0","published:0:1","client-copy:0"}
        self.assertIn("seed:0",m.close(k));self.assertFalse(m.private(k))

    def test_joint_relation_is_leakage_without_linear_seed_recovery(self):
        self.assertFalse(in_rowspan([1,0],[[1,1]],7))
        self.assertFalse(in_rowspan([0,1],[[1,1]],7))
        self.assertFalse(privacy_holds([[1,1]],[0,1],7))

    def test_fresh_future_bank_conditioned_on_old_seed(self):
        m=sharing_model([(0,0,3,2,"old","a"),(1,0,3,2,"new","b")],p=7)
        k={"published:0:0","published:1:0","bank-copy:old:1","bank-copy:old:2"}
        self.assertIn("seed:0",m.close(k));self.assertTrue(m.private(k,{1}))


if __name__ == "__main__":unittest.main()
