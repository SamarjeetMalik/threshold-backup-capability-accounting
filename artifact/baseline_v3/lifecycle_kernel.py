"""Executable reference for queue/expiry/crash ordering, not production crypto.

Certificates/checkpoints are trusted-verifier outputs in this reference. Slots
are capability-presence flags, and the durable anchor is an assumed atomic,
nonrollback store. Python buffer removal is not physical memory erasure.
"""
from dataclasses import dataclass, asdict, field
from copy import deepcopy
from hashlib import sha256
from threading import RLock


class Rejected(Exception):
    pass


def cbor(value):
    """RFC 8949 core deterministic encoding of this schema's small data model.

    No floats, tags, indefinite lengths or arbitrary application objects. Map
    ordering is bytewise lexicographic encoded-key order, not length-first.
    This encoder is not a validating decoder for untrusted wire input.
    """
    def head(major, n):
        if n < 0 or n >= 1 << 64:
            raise ValueError("CBOR integer/length out of bounds")
        if n < 24:
            return bytes([(major << 5) | n])
        for limit, marker, size in [(1<<8,24,1),(1<<16,25,2),(1<<32,26,4),(1<<64,27,8)]:
            if n < limit:
                return bytes([(major << 5) | marker]) + n.to_bytes(size,"big")
    if value is None:
        return b"\xf6"
    if isinstance(value, bool):
        return b"\xf5" if value else b"\xf4"
    if isinstance(value, int):
        return head(0,value) if value >= 0 else head(1,-1-value)
    if isinstance(value, bytes):
        return head(2,len(value))+value
    if isinstance(value, str):
        return head(3,len(value.encode()))+value.encode()
    if isinstance(value, (tuple,list)):
        return head(4,len(value))+b"".join(cbor(x) for x in value)
    if isinstance(value, dict):
        items=sorted((cbor(k),cbor(v)) for k,v in value.items())
        return head(5,len(items))+b"".join(k+v for k,v in items)
    raise TypeError(type(value))


@dataclass(frozen=True)
class Request:
    account: str
    nonce: str
    epoch: int
    generation: int
    configuration: int
    recipient: bytes
    manifest: bytes
    bank: int = 0
    domain: str = "ceab/ordinary-recovery/v2"  # wire label unchanged in v3

    @property
    def digest(self):
        return sha256(cbor(asdict(self))).digest()


@dataclass(frozen=True)
class Certificate:
    request_digest: bytes
    signers: tuple
    configuration: int
    verified: bool = True
    committed: bool = True


@dataclass(frozen=True)
class Checkpoint:
    nonce: str
    revision: int
    configuration: int
    floor: int
    verified: bool = True


@dataclass
class Epoch:
    bank: int = 0
    manifest: bytes = b"manifest"
    phase: str = "sealed"
    slot: bool = True
    receipt: bool = False
    proposed: bool = False
    committed: bool = False


@dataclass
class DurableAnchor:
    epochs: dict
    tombstones: set = field(default_factory=set)
    floor: int = 0
    highwater: int = 0
    configuration: int = 0
    pending_configuration: int | None = None
    revision: int = 0


@dataclass
class Job:
    request: Request
    started: float
    stage: str = "holding"
    certificate: Certificate | None = None
    buffer: bytearray | None = None
    work_revision: int | None = None


class ReferenceKernel:
    def __init__(self, epoch_keys=((0,0),), identities=(1,2,3), approval_quorum=2,
                 hold=24, clock=lambda: 0, account="acct"):
        self.lock=RLock()
        self.anchor=DurableAnchor({key:Epoch() for key in epoch_keys})
        self.identities=frozenset(identities)
        self.qa=approval_quorum
        self.hold=hold
        self.clock=clock
        self.account=account
        self.jobs={}
        self.delivered=[]
        self.crashed=False
        # v3: decryption workers that have begun and not yet returned. A worker
        # cancelled by expiry may still hold decrypted pair material, so a
        # receipt for its path waits until it returns (finish or abandon).
        self.inflight={}

    def _available(self):
        if self.crashed:
            raise Rejected("crashed")

    def _epoch(self, request):
        key=(request.epoch,request.generation)
        if key not in self.anchor.epochs:
            raise Rejected("unknown generation")
        e=self.anchor.epochs[key]
        if request.bank!=e.bank or request.manifest!=e.manifest:
            raise Rejected("bank or manifest mismatch")
        if request.account!=self.account or request.domain!="ceab/ordinary-recovery/v2":
            raise Rejected("account or domain mismatch")
        return key,e

    def checkpoint(self, nonce):
        with self.lock:
            self._available()
            a=self.anchor
            return Checkpoint(nonce,a.revision,a.configuration,a.floor)

    def _checkpoint(self, cp, req):
        a=self.anchor
        if not cp.verified or (cp.nonce,cp.revision,cp.configuration,cp.floor)!=(req.nonce,a.revision,a.configuration,a.floor):
            raise Rejected("stale or mismatched checkpoint")

    def _certificate(self, cert, req):
        if cert is None or not cert.verified or not cert.committed:
            raise Rejected("missing/uncommitted certificate")
        if cert.request_digest != req.digest or cert.configuration != req.configuration:
            raise Rejected("certificate request binding")
        signers=frozenset(cert.signers)
        if len(signers)!=len(cert.signers) or len(signers)<self.qa or not signers<=self.identities:
            raise Rejected("distinct valid approvers required")

    def register(self, request):
        with self.lock:
            self._available()
            key,epoch=self._epoch(request)
            if request.configuration!=self.anchor.configuration or epoch.phase!="sealed" or key in self.anchor.tombstones or request.epoch<self.anchor.floor:
                raise Rejected("inactive configuration or epoch")
            if request.nonce in self.jobs:
                if self.jobs[request.nonce].request!=request:
                    raise Rejected("nonce reused for different request")
                return self.jobs[request.nonce]
            job=Job(request,self.clock())
            self.jobs[request.nonce]=job
            return job

    def _job(self, nonce):
        if nonce not in self.jobs:
            raise Rejected("unknown request")
        return self.jobs[nonce]

    def authorize(self, nonce, certificate):
        with self.lock:
            self._available()
            job=self._job(nonce)
            self._certificate(certificate,job.request)
            job.certificate=certificate

    def _guard(self, job, checkpoint):
        self._available()
        req=job.request
        key,e=self._epoch(req)
        if e.phase!="sealed" or key in self.anchor.tombstones or not e.slot or req.epoch<self.anchor.floor:
            raise Rejected("expired or missing path")
        if req.configuration!=self.anchor.configuration:
            raise Rejected("stale configuration")
        if self.clock()<job.started:
            raise Rejected("monotone clock rolled back")
        if self.clock()-job.started<self.hold:
            raise Rejected("mandatory hold")
        self._certificate(job.certificate,req)
        self._checkpoint(checkpoint,req)

    def begin_decrypt(self, nonce, checkpoint):
        with self.lock:
            job=self._job(nonce)
            self._guard(job,checkpoint)
            if job.stage!="holding":
                raise Rejected("not holding")
            job.stage="decrypting"
            job.work_revision=self.anchor.revision
            token=(nonce,job.request.digest,job.work_revision)
            self.inflight[token]=(job.request.epoch,job.request.generation)
            return token

    def finish_decrypt(self, token, pair_bytes):
        with self.lock:
            nonce,digest,revision=token
            self.inflight.pop(token,None)
            job=self._job(nonce)
            try:
                if job.stage!="decrypting" or digest!=job.request.digest or revision!=self.anchor.revision:
                    raise Rejected("invalidated work")
                self._guard(job,self.checkpoint(nonce))
            except Rejected:
                self._cancel(job)
                return False
            job.buffer=bytearray(pair_bytes)
            job.stage="queued"
            return True

    def abandon_decrypt(self, token):
        """A worker that fails or is torn down reports that it holds no output."""
        with self.lock:
            self.inflight.pop(token,None)
            job=self.jobs.get(token[0])
            if job is not None:
                self._cancel(job)

    def begin_send(self, nonce, checkpoint):
        with self.lock:
            job=self._job(nonce)
            self._guard(job,checkpoint)
            if job.stage!="queued" or job.buffer is None:
                raise Rejected("nothing queued")
            job.stage="sending"

    def first_byte_transfer(self, nonce, checkpoint):
        """Atomic reference handoff to an external receiver, not a network API.

        Grant a full pair at the first irreversible byte, conservatively. Expiry
        cannot interleave the final guard and this modeled ownership transfer.
        """
        with self.lock:
            job=self._job(nonce)
            self._guard(job,checkpoint)
            if job.stage!="sending" or job.buffer is None:
                raise Rejected("send cancelled")
            event=(job.request,bytes(job.buffer))
            self.delivered.append(event)
            self._wipe(job)
            job.stage="done"
            return event

    @staticmethod
    def _wipe(job):
        if job.buffer is not None:
            job.buffer[:]=b"\x00"*len(job.buffer)
        job.buffer=None

    def _cancel(self,job):
        self._wipe(job)
        if job.stage!="done":
            job.stage="cancelled"

    def begin_expiry(self,key):
        with self.lock:
            self._available()
            epoch=self.anchor.epochs[key]
            if epoch.phase!="sealed":
                raise Rejected("not sealed")
            self.anchor.tombstones.add(key)  # assumed durable before receipt
            epoch.phase="expiring"
            self.anchor.revision+=1
            for job in self.jobs.values():
                if (job.request.epoch,job.request.generation)==key:
                    self._cancel(job)

    def erase_slot(self,key):
        with self.lock:
            self._available()
            epoch=self.anchor.epochs[key]
            if epoch.phase!="expiring":
                raise Rejected("expiry intent not persisted")
            epoch.slot=False
            self.anchor.revision+=1

    def sign_receipt(self,key):
        with self.lock:
            self._available()
            e=self.anchor.epochs[key]
            if e.phase!="expiring" or e.slot or key not in self.anchor.tombstones:
                raise Rejected("cleanup incomplete")
            if any(j.buffer is not None and (j.request.epoch,j.request.generation)==key for j in self.jobs.values()):
                raise Rejected("target buffer remains")
            if key in self.inflight.values():
                raise Rejected("decryption worker for this path has not returned")
            e.receipt=True
            self.anchor.revision+=1

    def propose_barrier(self,key):
        with self.lock:
            self._available()
            e=self.anchor.epochs[key]
            if not e.receipt:
                raise Rejected("no honest receipt")
            e.proposed=True
            self.anchor.revision+=1

    def commit_barrier(self,key):
        """Assumes the selected log has verified the global matching quorum."""
        with self.lock:
            self._available()
            e=self.anchor.epochs[key]
            if not e.proposed or not e.receipt or e.slot:
                raise Rejected("barrier prerequisites")
            e.committed=True
            e.phase="erased"
            self.anchor.revision+=1
            epochs={x for x,g in self.anchor.epochs}
            while self.anchor.floor in epochs and all(v.committed for (x,g),v in self.anchor.epochs.items() if x==self.anchor.floor):
                self.anchor.floor+=1
            self.anchor.highwater=max(self.anchor.highwater,self.anchor.floor)

    def propose_configuration(self,new):
        with self.lock:
            self._available()
            if new<=self.anchor.configuration:
                raise Rejected("configuration not increasing")
            self.anchor.pending_configuration=new
            self.anchor.revision+=1

    def commit_configuration(self):
        with self.lock:
            self._available()
            if self.anchor.pending_configuration is None:
                raise Rejected("no committed proposal")
            self.anchor.configuration=self.anchor.pending_configuration
            self.anchor.pending_configuration=None
            self.anchor.revision+=1
            for job in self.jobs.values():
                self._cancel(job)

    def snapshot(self):
        with self.lock:
            return deepcopy(self.anchor)

    def crash(self):
        with self.lock:
            self.crashed=True
            self.inflight.clear()  # process crash ends workers; not a RAM claim
            for job in self.jobs.values():
                self._cancel(job)

    def restart(self,snapshot=None):
        with self.lock:
            if snapshot is not None:
                a=self.anchor
                if snapshot.revision!=a.revision or snapshot.floor<a.highwater or snapshot.configuration<a.configuration or not a.tombstones<=snapshot.tombstones:
                    raise Rejected("old snapshot rejected by nonrollback anchor")
            self.crashed=False  # current durable journal, not old slot image

    def invariant(self):
        with self.lock:
            a=self.anchor
            assert a.floor>=a.highwater
            for key,e in a.epochs.items():
                if e.receipt:
                    assert not e.slot and key in a.tombstones
                if key in a.tombstones:
                    assert e.phase in ("expiring","erased")
            for j in self.jobs.values():
                if j.buffer is not None:
                    key,e=self._epoch(j.request)
                    assert e.phase=="sealed" and key not in a.tombstones
                    assert j.request.configuration==a.configuration
            return True
