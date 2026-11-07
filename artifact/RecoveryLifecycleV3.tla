-------------------------- MODULE RecoveryLifecycleV3 --------------------------
EXTENDS Naturals, FiniteSets, TLC

CONSTANTS EpochCount, GenerationCount, RequestCount, CancelOnExpiry, FinalRecheck,
          BindingGuard, ReceiptGuard, RollbackGuard, InflightGuard
Epochs == 0..(EpochCount-1)
Generations == 0..(GenerationCount-1)
Paths == Epochs \X Generations
Requests == 1..RequestCount
ReqEpoch(r) == (r-1) % EpochCount
ReqGeneration(r) == ((r-1) \div EpochCount) % GenerationCount
ReqPath(r) == <<ReqEpoch(r), ReqGeneration(r)>>
Completed(cs) == {e \in Epochs : \A g \in Generations : <<e,g>> \in cs}
ASSUME EpochCount>0 /\ GenerationCount>0 /\ RequestCount>0
Active == {"holding","decrypting","queued","sending"}

VARIABLES phase, slots, tomb, receipts, pending, committed, floor, highwater,
          config, crashed, stage, requestConfig, endpoint, cert, held, buffers,
          delivered, badExpiry, badBinding, identityCompromised
vars == <<phase, slots, tomb, receipts, pending, committed, floor, highwater,
          config, crashed, stage, requestConfig, endpoint, cert, held, buffers,
          delivered, badExpiry, badBinding, identityCompromised>>

(* v3: "aborting" is cancelled work whose decryption worker has not returned.
   The worker may still hold decrypted share material in its own memory. *)
CancelTo(r) == IF stage[r] = "decrypting" THEN "aborting" ELSE "cancelled"

Init == /\ phase = [e \in Paths |-> "sealed"]
        /\ slots = Paths /\ tomb = {} /\ receipts = {} /\ pending = {}
        /\ committed = {} /\ floor = 0 /\ highwater = 0 /\ config = 0
        /\ crashed = FALSE /\ stage = [r \in Requests |-> "idle"]
        /\ requestConfig = [r \in Requests |-> 0]
        /\ endpoint = [r \in Requests |-> 0]
        /\ cert = [r \in Requests |-> 0] /\ held = {} /\ buffers = {}
        /\ delivered = {} /\ badExpiry = FALSE /\ badBinding = FALSE
        /\ identityCompromised = FALSE

RequestOK(r) == /\ cert[r] = 1 /\ endpoint[r] = 0
                /\ requestConfig[r] = config /\ r \in held
Live(r) == /\ phase[ReqPath(r)] = "sealed" /\ ReqPath(r) \notin tomb
Bound(r) == IF BindingGuard THEN RequestOK(r) ELSE cert[r] # 0 /\ r \in held

Request(r) == /\ ~crashed /\ stage[r] = "idle" /\ Live(r)
              /\ stage' = [stage EXCEPT ![r] = "holding"]
              /\ requestConfig' = [requestConfig EXCEPT ![r] = config]
              /\ UNCHANGED <<phase,slots,tomb,receipts,pending,committed,floor,
                   highwater,config,crashed,endpoint,cert,held,buffers,delivered,
                   badExpiry,badBinding,identityCompromised>>

(* Certificate 1 represents a quorum for the exact immutable request; 2 is a
   replay/mismatch. This abstracts signature validation and quorum generation.
   Byzantine identities and genuine mistaken approvals are checked separately. *)
OfferCertificate(r,c) == /\ ~crashed /\ stage[r] \in Active /\ cert[r] = 0
                         /\ cert' = [cert EXCEPT ![r] = c]
                         /\ UNCHANGED <<phase,slots,tomb,receipts,pending,
                           committed,floor,highwater,config,crashed,stage,
                           requestConfig,endpoint,held,buffers,delivered,
                           badExpiry,badBinding,identityCompromised>>

HoldCompletes(r) == /\ ~crashed /\ stage[r] \in Active /\ r \notin held
                    /\ held' = held \cup {r}
                    /\ UNCHANGED <<phase,slots,tomb,receipts,pending,committed,
                      floor,highwater,config,crashed,stage,requestConfig,endpoint,
                      cert,buffers,delivered,badExpiry,badBinding,identityCompromised>>

ChangeRecipient(r) == /\ ~crashed /\ stage[r] \in Active /\ endpoint[r] = 0
                     /\ endpoint' = [endpoint EXCEPT ![r] = 1]
                     /\ UNCHANGED <<phase,slots,tomb,receipts,pending,committed,
                       floor,highwater,config,crashed,stage,requestConfig,cert,
                       held,buffers,delivered,badExpiry,badBinding,identityCompromised>>

BeginDecrypt(r) == /\ ~crashed /\ stage[r] = "holding" /\ Live(r)
                   /\ ReqPath(r) \in slots /\ Bound(r)
                   /\ stage' = [stage EXCEPT ![r] = "decrypting"]
                   /\ UNCHANGED <<phase,slots,tomb,receipts,pending,committed,
                     floor,highwater,config,crashed,requestConfig,endpoint,cert,
                     held,buffers,delivered,badExpiry,badBinding,identityCompromised>>

FinishDecrypt(r) == /\ ~crashed /\ stage[r] = "decrypting"
                    /\ (IF FinalRecheck THEN Live(r) /\ Bound(r) ELSE TRUE)
                    /\ buffers' = buffers \cup {r}
                    /\ stage' = [stage EXCEPT ![r] = "queued"]
                    /\ UNCHANGED <<phase,slots,tomb,receipts,pending,committed,
                      floor,highwater,config,crashed,requestConfig,endpoint,cert,
                      held,delivered,badExpiry,badBinding,identityCompromised>>

(* The cancelled worker returns and discards its output. *)
WorkerReturns(r) == /\ stage[r] = "aborting"
                    /\ stage' = [stage EXCEPT ![r] = "cancelled"]
                    /\ UNCHANGED <<phase,slots,tomb,receipts,pending,committed,
                      floor,highwater,config,crashed,requestConfig,endpoint,cert,
                      held,buffers,delivered,badExpiry,badBinding,identityCompromised>>

StartSend(r) == /\ ~crashed /\ stage[r] = "queued" /\ r \in buffers
                /\ stage' = [stage EXCEPT ![r] = "sending"]
                /\ UNCHANGED <<phase,slots,tomb,receipts,pending,committed,floor,
                  highwater,config,crashed,requestConfig,endpoint,cert,held,
                  buffers,delivered,badExpiry,badBinding,identityCompromised>>

(* First-byte transfer is the irreversible disclosure point. Conservatively
   grant the entire share to the receiver, even for an interrupted send. *)
Transfer(r) == /\ ~crashed /\ stage[r] = "sending" /\ r \in buffers
               /\ (IF FinalRecheck THEN Live(r) /\ Bound(r) ELSE TRUE)
               /\ stage' = [stage EXCEPT ![r] = "done"]
               /\ delivered' = delivered \cup {r}
               /\ buffers' = buffers \ {r}
               /\ badExpiry' = (badExpiry \/ ~Live(r))
               /\ badBinding' = (badBinding \/ ~RequestOK(r))
               /\ UNCHANGED <<phase,slots,tomb,receipts,pending,committed,floor,
                 highwater,config,crashed,requestConfig,endpoint,cert,held,identityCompromised>>

BeginExpiry(e) == /\ ~crashed /\ phase[e] = "sealed"
                  /\ tomb' = tomb \cup {e}
                  /\ phase' = [phase EXCEPT ![e] = "expiring"]
                  /\ stage' = [r \in Requests |->
                       IF CancelOnExpiry /\ ReqPath(r)=e /\ stage[r] \in Active
                       THEN CancelTo(r) ELSE stage[r]]
                  /\ buffers' = IF CancelOnExpiry
                       THEN {r \in buffers : ReqPath(r) # e} ELSE buffers
                  /\ UNCHANGED <<slots,receipts,pending,committed,floor,highwater,
                    config,crashed,requestConfig,endpoint,cert,held,delivered,
                    badExpiry,badBinding,identityCompromised>>

Erase(e) == /\ ~crashed /\ phase[e] = "expiring" /\ e \in slots
            /\ slots' = slots \ {e}
            /\ UNCHANGED <<phase,tomb,receipts,pending,committed,floor,highwater,
              config,crashed,stage,requestConfig,endpoint,cert,held,buffers,
              delivered,badExpiry,badBinding,identityCompromised>>

SignReceipt(e) == /\ ~crashed /\ phase[e] = "expiring" /\ e \notin receipts
                  /\ (IF ReceiptGuard THEN e \notin slots /\
                        \A r \in buffers : ReqPath(r) # e ELSE TRUE)
                  /\ (IF InflightGuard THEN
                        \A r \in Requests : ReqPath(r) = e => stage[r] # "aborting"
                      ELSE TRUE)
                  /\ receipts' = receipts \cup {e}
                  /\ UNCHANGED <<phase,slots,tomb,pending,committed,floor,
                    highwater,config,crashed,stage,requestConfig,endpoint,cert,
                    held,buffers,delivered,badExpiry,badBinding,identityCompromised>>

Propose(e) == /\ ~crashed /\ e \in receipts /\ e \notin pending
              /\ e \notin committed /\ pending' = pending \cup {e}
              /\ UNCHANGED <<phase,slots,tomb,receipts,committed,floor,highwater,
                config,crashed,stage,requestConfig,endpoint,cert,held,buffers,
                delivered,badExpiry,badBinding,identityCompromised>>

Commit(e) == /\ ~crashed /\ e \in pending /\ e \notin committed
             /\ \A d \in Paths : d[1] < e[1] => d \in committed
             /\ committed' = committed \cup {e} /\ pending' = pending \ {e}
             /\ phase' = [phase EXCEPT ![e] = "erased"]
             /\ LET f == Cardinality(Completed(committed \cup {e}))
                 IN /\ floor' = f /\ highwater' = f
             /\ UNCHANGED <<slots,tomb,receipts,config,crashed,stage,requestConfig,
               endpoint,cert,held,buffers,delivered,badExpiry,badBinding,identityCompromised>>

ConfigUpdate == /\ ~crashed /\ config=0 /\ config'=1
                /\ buffers' = {}
                /\ stage' = [r \in Requests |->
                     IF stage[r] \in Active THEN CancelTo(r) ELSE stage[r]]
                /\ UNCHANGED <<phase,slots,tomb,receipts,pending,committed,floor,
                  highwater,crashed,requestConfig,endpoint,cert,held,delivered,
                  badExpiry,badBinding,identityCompromised>>

IdentityCompromise == /\ ~identityCompromised /\ identityCompromised'=TRUE
                      /\ UNCHANGED <<phase,slots,tomb,receipts,pending,committed,
                        floor,highwater,config,crashed,stage,requestConfig,
                        endpoint,cert,held,buffers,delivered,badExpiry,badBinding>>

(* A process crash ends every worker; it is not a claim about physical RAM. *)
Crash == /\ ~crashed /\ crashed'=TRUE /\ buffers'={}
         /\ stage' = [r \in Requests |->
              IF stage[r] \in Active \cup {"aborting"} THEN "cancelled" ELSE stage[r]]
         /\ UNCHANGED <<phase,slots,tomb,receipts,pending,committed,floor,highwater,
           config,requestConfig,endpoint,cert,held,delivered,badExpiry,badBinding,identityCompromised>>

Restart == /\ crashed /\ crashed'=FALSE
           /\ UNCHANGED <<phase,slots,tomb,receipts,pending,committed,floor,
             highwater,config,stage,requestConfig,endpoint,cert,held,buffers,
             delivered,badExpiry,badBinding,identityCompromised>>

(* An old disk image must be rejected if trusted tombstones/config/floor are
   newer. The mutant deliberately restores application state past a barrier. *)
RollbackRestart == /\ crashed
                   /\ (IF RollbackGuard THEN tomb={} /\ config=0 /\ floor=0
                       ELSE committed # {})
                   /\ crashed'=FALSE /\ phase'=[e \in Paths |-> "sealed"]
                   /\ slots'=Paths /\ tomb'={} /\ floor'=0 /\ config'=0
                   /\ UNCHANGED <<receipts,pending,committed,highwater,stage,
                     requestConfig,endpoint,cert,held,buffers,delivered,
                     badExpiry,badBinding,identityCompromised>>

Next == (\E r \in Requests : Request(r) \/ HoldCompletes(r) \/
           ChangeRecipient(r) \/ BeginDecrypt(r) \/ FinishDecrypt(r) \/ WorkerReturns(r) \/
           StartSend(r) \/ Transfer(r) \/ (\E c \in {1,2}: OfferCertificate(r,c)))
        \/ (\E e \in Paths : BeginExpiry(e) \/ Erase(e) \/
             SignReceipt(e) \/ Propose(e) \/ Commit(e))
        \/ ConfigUpdate \/ IdentityCompromise \/ Crash \/ Restart \/ RollbackRestart

TypeOK == /\ phase \in [Paths -> {"sealed","expiring","erased"}]
          /\ slots \subseteq Paths /\ tomb \subseteq Paths
          /\ receipts \subseteq Paths /\ pending \subseteq Paths
          /\ committed \subseteq Paths /\ floor \in 0..EpochCount
          /\ highwater \in 0..EpochCount /\ config \in {0,1}
          /\ crashed \in BOOLEAN /\ identityCompromised \in BOOLEAN
          /\ stage \in [Requests -> ({"idle","done","cancelled","aborting"} \cup Active)]
          /\ requestConfig \in [Requests -> {0,1}]
          /\ endpoint \in [Requests -> {0,1}] /\ cert \in [Requests -> {0,1,2}]
          /\ held \subseteq Requests /\ buffers \subseteq Requests
          /\ delivered \subseteq Requests /\ badExpiry \in BOOLEAN /\ badBinding \in BOOLEAN
NoPostExpiryRelease == ~badExpiry
ExactRequestBinding == ~badBinding
FloorMonotone == floor >= highwater /\ floor = Cardinality(Completed(committed))
ReceiptAfterCleanup == \A e \in receipts : e \notin slots /\
                         (\A r \in buffers : ReqPath(r) # e)
(* v3: no decryption worker for the path may still be running at the receipt. *)
ReceiptAfterWorkers == \A e \in receipts : \A r \in Requests :
                         ReqPath(r) = e => stage[r] \notin {"decrypting","aborting"}
NoStaleWork == \A r \in buffers : ReqPath(r) \notin tomb /\
                requestConfig[r] = config /\ phase[ReqPath(r)] = "sealed"

Spec == Init /\ [][Next]_vars
=============================================================================
