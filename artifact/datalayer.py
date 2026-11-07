"""Reference data layer for the profile's object encryption (v4.0.3).

Not a production backup system. It implements exactly the interface counted in
Theorem 24, with maintained primitives: HMAC-SHA256 from the Python standard
library and ChaCha20-Poly1305 from pyca/cryptography. No primitive is written
here.

Object key  = HMAC-SHA256(seed, CBOR(ctx)), memoized per context.
Chunk nonce = 0^32 || uint64(index), never repeated under an object key.
Chunk AAD   = CBOR({ctx digest, index, final}). The final-chunk flag makes
              truncation detectable; the v4.0.2 profile did not specify it.
Identifiers = 32 uniform bytes; Store re-samples if the local index already
              holds the identifier (defensive; the proof still charges the
              collision term because it does not assume a single index).
"""
from dataclasses import dataclass, field
from hashlib import sha256
import hmac
import secrets
import threading

from cryptography.hazmat.primitives.ciphers.aead import ChaCha20Poly1305
from cryptography.exceptions import InvalidTag

from lifecycle_kernel import cbor

MAX_CHUNKS = 2**32 - 1
DOMAIN = "ceab/object/v4.0.3"


class AuthFailure(Exception):
    pass


class Interrupted(Exception):
    pass


@dataclass
class Record:
    ctx: dict
    chunks: list


@dataclass
class Counters:
    store_requests: int = 0
    open_requests: int = 0
    hmac: int = 0
    aead_enc: int = 0
    aead_dec: int = 0           # every decryption call, including failures
    aead_dec_failed: int = 0
    abandoned: int = 0


class DataLayer:
    def __init__(self, seed: bytes, account="acct", configuration=0, rng=None, derive=None):
        assert len(seed) == 32
        self.seed, self.account, self.configuration = seed, account, configuration
        self.rng = rng or secrets.token_bytes
        self._derive = derive or self._hmac
        self.keys = {}                       # memoized encoded ctx -> key
        self.index = set()                   # identifiers held locally
        self.used = set()                    # (key bytes, nonce): key-byte-level reuse guard
        self.count = Counters()
        self.lock = threading.RLock()        # v4.0.4: cache and nonce guard are shared state

    # --- record validation (v4.0.4) ---------------------------------------
    FIELDS = {"domain": str, "account": str, "configuration": int, "epoch": int,
              "id": bytes, "header": bytes}

    def _validate(self, record):
        """Reject malformed or foreign records before any key derivation."""
        if not isinstance(record, Record) or not isinstance(record.ctx, dict):
            raise AuthFailure("malformed record")
        ctx = record.ctx
        if set(ctx) != set(self.FIELDS):
            raise AuthFailure("malformed context")
        for name, typ in self.FIELDS.items():
            v = ctx[name]
            if type(v) is not typ:            # exact types: True is not an int here
                raise AuthFailure(f"context field {name}")
        if len(ctx["id"]) != 32:
            raise AuthFailure("identifier length")
        if (ctx["domain"], ctx["account"], ctx["configuration"]) != (DOMAIN, self.account, self.configuration):
            raise AuthFailure("foreign context")
        chunks = record.chunks
        if not isinstance(chunks, list) or not chunks:
            raise AuthFailure("empty object")
        if len(chunks) > MAX_CHUNKS or any(type(c) is not bytes or len(c) < 16 for c in chunks):
            raise AuthFailure("malformed chunk")

    # --- key derivation -------------------------------------------------
    def _hmac(self, encoded):
        return hmac.new(self.seed, encoded, sha256).digest()

    def key(self, ctx):
        enc = cbor(ctx)
        with self.lock:
            if enc not in self.keys:
                self.count.hmac += 1
                self.keys[enc] = self._derive(enc)
            return self.keys[enc]

    # --- encryption -----------------------------------------------------
    @staticmethod
    def nonce(i):
        return bytes(4) + i.to_bytes(8, "big")

    @staticmethod
    def aad(ctx, i, final):
        return cbor({"ctx": sha256(cbor(ctx)).digest(), "i": i, "final": final})

    def context(self, epoch, header, ident):
        return {"domain": DOMAIN, "account": self.account, "configuration": self.configuration,
                "epoch": epoch, "id": ident, "header": header}

    def store(self, epoch, header: bytes, data: bytes, chunk_size=1 << 20, fail_after=None):
        """Encrypt `data` in chunks. `fail_after` simulates a crash after that
        many chunks; the partial object is abandoned and the creation is retried
        under a fresh identifier, never by re-encrypting under the old key."""
        self.count.store_requests += 1
        n = max(1, -(-len(data) // chunk_size))
        if n > MAX_CHUNKS:
            raise ValueError("object exceeds chunk limit")
        with self.lock:
            while True:
                ident = self.rng(32)
                if ident not in self.index:
                    break
            self.index.add(ident)
        ctx = self.context(epoch, header, ident)
        k = self.key(ctx)
        aead = ChaCha20Poly1305(k)
        chunks = []
        for i in range(n):
            if fail_after is not None and i == fail_after:
                self.count.abandoned += 1
                raise Interrupted(ident)
            nonce = self.nonce(i)
            with self.lock:                  # check and record atomically
                if (k, nonce) in self.used:
                    raise RuntimeError("key/nonce reuse at the key-byte level")
                self.used.add((k, nonce))
            part = data[i * chunk_size:(i + 1) * chunk_size]
            chunks.append(aead.encrypt(nonce, part, self.aad(ctx, i, i == n - 1)))
            self.count.aead_enc += 1
        return Record(ctx, chunks)

    def store_with_retry(self, epoch, header, data, chunk_size=1 << 20, fail_after=None):
        try:
            return self.store(epoch, header, data, chunk_size, fail_after)
        except Interrupted:
            return self.store(epoch, header, data, chunk_size)

    # --- decryption -----------------------------------------------------
    def open(self, record: Record) -> bytes:
        """One object-level request: one context, one key derivation at most,
        one AEAD call per chunk. Empty requests are rejected before derivation."""
        self._validate(record)
        self.count.open_requests += 1
        k = self.key(record.ctx)
        aead = ChaCha20Poly1305(k)
        out = []
        last = len(record.chunks) - 1
        for i, c in enumerate(record.chunks):
            self.count.aead_dec += 1
            try:
                out.append(aead.decrypt(self.nonce(i), c, self.aad(record.ctx, i, i == last)))
            except InvalidTag:
                self.count.aead_dec_failed += 1
                raise AuthFailure(f"chunk {i}")
        return b"".join(out)
