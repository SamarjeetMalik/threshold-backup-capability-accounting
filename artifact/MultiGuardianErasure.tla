------------------------ MODULE MultiGuardianErasure ------------------------
(* v3: n holders of one sharing generation run an erasure barrier together.
   Byzantine holders may sign receipts while keeping their slots, or withhold.
   The adversary may copy up to C honest slots before they are erased. A
   barrier commits on Qd receipts. Exposed counts every index whose share is
   still usable by someone: Byzantine slots, copies and surviving honest slots
   (the worst-case final snapshot). Recovery needs T live honest online slots.
   Liveness is checked only under weak fairness for honest online holders and
   the commit step; Byzantine and copy actions get no fairness. *)
EXTENDS Naturals, FiniteSets

CONSTANTS N, T, Qd, F, C, U, ReceiptGuard
Holders == 1..N
ASSUME T \in 1..N /\ Qd \in 1..N /\ F + U <= N

VARIABLES byz, off, slot, receipt, copied, started, committed
vars == <<byz, off, slot, receipt, copied, started, committed>>

Init == /\ byz \in {S \in SUBSET Holders : Cardinality(S) = F}
        /\ off \in {S \in SUBSET (Holders \ byz) : Cardinality(S) = U}
        /\ slot = Holders /\ receipt = {} /\ copied = {}
        /\ started = FALSE /\ committed = FALSE

Honest == Holders \ byz
Online == Honest \ off

Start == /\ ~started /\ started' = TRUE
         /\ UNCHANGED <<byz, off, slot, receipt, copied, committed>>

Copy(h) == /\ h \in Honest /\ h \in slot /\ h \notin copied
           /\ Cardinality(copied) < C
           /\ copied' = copied \cup {h}
           /\ UNCHANGED <<byz, off, slot, receipt, started, committed>>

Erase(h) == /\ started /\ h \in Online /\ h \in slot
            /\ slot' = slot \ {h}
            /\ UNCHANGED <<byz, off, receipt, copied, started, committed>>

HonestReceipt(h) == /\ started /\ h \in Online /\ h \notin receipt
                    /\ (IF ReceiptGuard THEN h \notin slot ELSE TRUE)
                    /\ receipt' = receipt \cup {h}
                    /\ UNCHANGED <<byz, off, slot, copied, started, committed>>

ByzantineReceipt(h) == /\ started /\ h \in byz /\ h \notin receipt
                       /\ receipt' = receipt \cup {h}
                       /\ UNCHANGED <<byz, off, slot, copied, started, committed>>

Commit == /\ started /\ ~committed /\ Cardinality(receipt) >= Qd
          /\ committed' = TRUE
          /\ UNCHANGED <<byz, off, slot, receipt, copied, started>>

Next == Start \/ Commit \/
        \E h \in Holders : Copy(h) \/ Erase(h) \/ HonestReceipt(h) \/ ByzantineReceipt(h)

Fairness == /\ \A h \in Holders : WF_vars(Erase(h)) /\ WF_vars(HonestReceipt(h))
            /\ WF_vars(Commit)
Spec == Init /\ [][Next]_vars /\ Fairness

Exposed == byz \cup copied \cup slot
TypeOK == /\ byz \subseteq Holders /\ off \subseteq Holders /\ slot \subseteq Holders
          /\ receipt \subseteq Holders /\ copied \subseteq Holders
          /\ started \in BOOLEAN /\ committed \in BOOLEAN
ErasureSafe == committed => Cardinality(Exposed) < T
DeletionBound == committed => Cardinality(Exposed) <= N - Qd + F + C
RecoverableBeforeBarrier == ~started => Cardinality(Online \cap slot) >= T
BarrierProgress == started ~> committed
=============================================================================
