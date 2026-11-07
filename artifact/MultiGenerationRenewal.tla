----------------------- MODULE MultiGenerationRenewal -----------------------
(* v4: a mobile adversary against share refresh. In each period the system
   publishes a fresh, independently randomized generation of the same seed
   (algebraic independence is assumed, as in Theorem 11). The adversary may
   copy at most C holder bank roots per period; F static Byzantine holders
   touch every generation. With Renew each generation is delivered under a new
   bank; with KeepOld old bank roots remain copyable after renewal (cleanup
   not performed). GenPrivate is the counting condition of Theorem 12 for
   every published generation. This checks delivery-path accounting only, not
   cryptography. *)
EXTENDS Naturals, FiniteSets

CONSTANTS N, T, F, C, Periods, Renew, KeepOld
Holders == 1..N
ASSUME F <= N /\ Periods >= 1

VARIABLES byz, period, copies, used
vars == <<byz, period, copies, used>>

Bank(g) == IF Renew THEN g ELSE 1
Copyable == IF KeepOld THEN {Bank(g) : g \in 1..period} ELSE {Bank(period)}

Init == /\ byz \in {S \in SUBSET Holders : Cardinality(S) = F}
        /\ period = 1 /\ copies = {} /\ used = 0

Copy(h, b) == /\ h \notin byz /\ b \in Copyable /\ used < C
              /\ <<h, b>> \notin copies
              /\ copies' = copies \cup {<<h, b>>} /\ used' = used + 1
              /\ UNCHANGED <<byz, period>>

Refresh == /\ period < Periods
           /\ period' = period + 1 /\ used' = 0
           /\ UNCHANGED <<byz, copies>>

Next == Refresh \/ \E h \in Holders, b \in 1..Periods : Copy(h, b)
Spec == Init /\ [][Next]_vars

Touched(g) == byz \cup {h \in Holders : <<h, Bank(g)>> \in copies}
GenPrivate == \A g \in 1..period : Cardinality(Touched(g)) < T
=============================================================================
