# Relational Security Invariants
## Novelty research and candidate conformance framework — v0

**Research date:** 2026-09-09  
**Primary empirical source:** `decentralised-security-audit-9fe2687-2026-09-09.md`  
**Audited repository revision:** `Interpoll1/decentralised @ 9fe2687b4022af1501c690397af4306b82bb53f9`

---

## 1. Executive conclusion

The individual security failures found in the `Interpoll1/decentralised` audit are **not, by themselves, novel vulnerability classes**. Pre-key authentication, identity misbinding, nonce/key reuse, replay protection, fail-safe authorization, trust-root continuity, authenticated context, and transactional state handling all have substantial prior art.

The potentially original contribution is a **unified cross-domain conformance abstraction**:

> **A locally valid component must not inherit security, authority, identity, provenance, policy, or completion semantics from a relation that has not itself been established.**

The audit produced a useful family of examples in which the local object is valid while the *relation* relied upon by the next layer is false or unproven:

- a signature is valid, but the signer is not the authorized subject;
- a public key is well-formed, but it is not authenticated to the displayed account;
- ciphertext is valid, but it is moved into a different message/context;
- a discovered issuer key is syntactically valid, but discovery has replaced an authority root;
- a policy exists, but fallback silently weakens it during failure;
- a status says `confirmed`, but the evidence needed to justify confirmation never occurred;
- a snapshot is internally hash-consistent, but its contents were not admitted through the normal validation relation;
- a ratchet state transition is locally executable, but authentication failed and therefore the state change was never authorized to commit.

This suggests a candidate framework of **Relational Security Invariants (RSI)** plus **Relation-Binding Conformance Fixtures (RBCF)**.

The novelty thesis should therefore **not** be:

> “We discovered identity binding / replay / nonce reuse / fail-open.”

It should be closer to:

> “We define and test a reusable family of *relation-preservation invariants* across cryptographic, authorization, provenance, synchronization, and evidence-bearing systems, using adversarial fixtures where each local component remains valid while the protected relation between components is changed, missing, stale, or substituted.”

That formulation appears materially less represented in the sources reviewed than the underlying individual mechanisms.

---

## 2. Empirical basis from the audit

The repository audit concluded that the audited commit did **not** establish authenticated E2EE. It reproduced, among other things:

- unauthenticated DM bundle substitution;
- concurrent reuse of a sending-chain position and AES-GCM nonce;
- plaintext upload of large DM attachments;
- bootstrap authentication failure that still changed durable ratchet state;
- historical bootstrap replay and rollback;
- permanent “one-time” prekeys;
- loss of skipped-message keys across ratchets;
- premature receive deduplication;
- `confirmed` delivery without successful delivery or persistence;
- group ciphertext/context rebinding;
- profile signer/subject mismatch;
- discovered issuer keys replacing trusted issuer keys;
- login-required authorization failing open on backend failure;
- alternate P2P paths bypassing identity/anonymity policy;
- snapshot/import paths bypassing live validation.

The audit then extracted reusable rules including:

1. signer-to-subject binding;
2. trust-root non-substitution;
3. authentication-before-commit;
4. atomic key consumption;
5. replay across epochs;
6. context-complete authentication;
7. policy-preserving fallback;
8. evidence-based confirmation;
9. ingestion equivalence;
10. recovery completeness.

This is the strongest basis for the generalized framework: the same structural failure appears across otherwise unrelated subsystems.

---

## 3. Prior-art map

### 3.1 Identity / signer / subject binding

**Prior art is strong. Novelty of the underlying problem: low.**

Signal X3DH explicitly distinguishes key agreement from identity authentication. Its pre-key bundle contains an identity key, signed pre-key, signature over the signed pre-key, and optional one-time pre-key. The initiator verifies the signed pre-key signature and aborts if it fails. The specification further warns that without authentication, users do not obtain a cryptographic guarantee about who they are communicating with, and it has a dedicated section on identity misbinding.

Relevant sources:

- Signal, **The X3DH Key Agreement Protocol**  
  https://signal.org/docs/specifications/x3dh/
- Sethi, Peltonen, Aura, **Misbinding Attacks on Secure Device Pairing and Bootstrapping**, AsiaCCS 2019  
  https://doi.org/10.1145/3321705.3329813
- Peltonen, Sethi, Aura, **Formal verification of misbinding attacks on secure device pairing and bootstrapping**, JISA 2020  
  https://doi.org/10.1016/j.jisa.2020.102461
- RFC 8844, **Unknown Key-Share Attacks on Uses of TLS with SDP**  
  https://www.rfc-editor.org/rfc/rfc8844.html

**Assessment:**  
`signer-to-subject binding` is a known authentication/correspondence problem. What may be useful is expressing it as one member of a larger generic relation-binding fixture family.

---

### 3.2 Event correspondence and authenticated relations

**Prior art is conceptually very close. Novelty of “security means a relation between events”: low.**

Formal protocol verification already models authentication as a **correspondence assertion**: if an end-event occurs, a related begin-event with corresponding arguments must have occurred. Injective correspondence strengthens this to one-to-one relationships between protocol events.

Relevant sources:

- ProVerif manual — correspondence assertions / authentication  
  https://publications.bensmyth.com/files/ProVerif-manual-version-2.00.pdf
- General ProVerif literature and applied-pi-calculus protocol verification.

A simplified correspondence form is:

```text
end(subject, session, value)
    ==> begin(subject, session, value)
```

An injective form requires each accepted end-event to correspond to a distinct authorized begin-event.

**Assessment:**  
This is important prior art. RSI should **not** claim to invent relational security reasoning. Its differentiation must be the construction of a practical, cross-domain adversarial conformance methodology where *locally valid artifacts are deliberately relation-swapped*.

---

### 3.3 Authentication-before-commit / failed decrypt must not mutate trusted state

**Prior art is directly on point in secure messaging. Novelty of the invariant itself: low.**

Signal's Sesame session-management specification says that if message parsing, session creation, or cryptographic processing fails, state changes are discarded. This is almost exactly the audit-derived invariant:

```text
reject(input) => durable_state_after == durable_state_before
```

Relevant source:

- Signal, **Sesame Algorithm: Session Management for Asynchronous Message Encryption**  
  https://signal.org/docs/specifications/sesame/

Sesame explicitly treats session processing as tentative until successful decryption and discards changes on failure.

**Assessment:**  
The invariant is known in the messaging domain. A generalized standard that applies it uniformly to *cryptographic state, authorization state, import state, provenance state, and evidence state* may still be useful.

---

### 3.4 Atomic key consumption / concurrency-safe cryptographic state

**Underlying cryptographic requirement is established; concurrency fixture packaging may be more distinctive.**

AES-GCM requires nonce uniqueness for a given key. RFC 5084 states that reusing the same nonce with the same key destroys the security properties.

Relevant source:

- RFC 5084, **Using AES-CCM and AES-GCM Authenticated Encryption in CMS**  
  https://www.rfc-editor.org/rfc/rfc5084.html

The audit's important refinement is operational:

```text
Every logical sending-chain position is consumed at most once
across threads, tabs, retries, workers, service instances, and crash recovery.
```

This is stronger than merely saying “nonces must be unique”: it treats uniqueness as a **state-transition/transactional invariant**.

Candidate fixture:

```text
Given ratchet revision r
When two sends race from r
Then they MUST NOT both emit envelopes derived from position r
```

**Assessment:**  
Nonce uniqueness is old. A standard adversarial fixture for **concurrent state consumption across execution contexts** is more promising as a reusable conformance artifact, particularly when combined with retry and persistence semantics.

---

### 3.5 Replay across epochs / session replacement

**Prior art is strong. Novelty of replay as a class: none.**

X3DH has explicit security considerations for protocol replay and key reuse. Double Ratchet/Sesame provide session-management behavior intended to avoid unsafe replay and stale state acceptance.

Relevant sources:

- Signal X3DH  
  https://signal.org/docs/specifications/x3dh/
- Signal Double Ratchet  
  https://signal.org/docs/specifications/doubleratchet/
- Signal Sesame  
  https://signal.org/docs/specifications/sesame/

**Assessment:**  
The potentially useful abstraction is not “replay protection,” but:

> a formerly valid artifact must not regain authority after the relation's epoch has advanced unless an explicit transition rule authorizes it.

That wording connects messaging replay to key rotation, trust-root rollback, stale authorization, stale provenance pointers, and snapshot rollback.

---

### 3.6 Trust-root non-substitution / continuity

**Strong prior art.**

The Update Framework (TUF) is built around trusted root continuity. Clients ship with trusted root keys. Root rotation must be authorized by both the previously trusted root and the new root, and roots are versioned to prevent rollback.

Relevant sources:

- TUF specification  
  https://theupdateframework.github.io/specification/draft/
- TUF specification repository  
  https://github.com/theupdateframework/specification

Core structural rule:

```text
Discovery(new_root) != Authorization(new_root)
```

A newly observed root becomes trusted only through an explicitly authenticated continuity relation.

Signal safety numbers similarly provide user-visible identity continuity and warnings/approval semantics for key changes.

Relevant source:

- Signal Support, **What is a safety number and why do I see that it changed?**  
  https://support.signal.org/hc/en-us/articles/360007060632-What-is-a-safety-number-and-why-do-I-see-that-it-changed

**Assessment:**  
Trust-root continuity is not novel. The audit's `trust-root non-substitution` fixture is valuable as a generic test case:

```text
trusted(key_A, namespace_X)
+
discover(valid_key_B, namespace_X)
must not imply
trusted(key_B, namespace_X)
```

---

### 3.7 Complete mediation / fail-safe authorization

**Foundational prior art. Novelty of the principles: none.**

Saltzer and Schroeder's classic security principles include:

- **fail-safe defaults** — access should be based on explicit permission;
- **complete mediation** — every access to every object should be checked for authority.

Relevant source:

- Saltzer & Schroeder, **The Protection of Information in Computer Systems**, Proceedings of the IEEE, 1975  
  DOI: https://doi.org/10.1109/PROC.1975.9939  
  Accessible copy: https://www.cs.virginia.edu/~evans/cs551/saltzer/

The audit's `policy-preserving fallback` is a concrete modern formulation:

```text
mandatory(policy) && unavailable(authorizer)
    must not become
allow
```

**Assessment:**  
The principle is old, but turning outage/fallback behavior into a machine-testable **relation-preservation fixture** is useful:

```text
policy_before_failure == policy_during_failure
unless an authenticated policy transition explicitly changes it
```

This can be applied to auth services, policy engines, RPC failover, AI-agent execution gates, custody systems, and distributed consensus adapters.

---

### 3.8 Context-complete authentication

**Strong cryptographic prior art, but broad cross-layer fixture framing is promising.**

AEAD associated data exists specifically to authenticate context that is not encrypted. X3DH binds identity information into associated data; Double Ratchet authenticates ratchet headers together with ciphertext.

Relevant sources:

- Signal X3DH  
  https://signal.org/docs/specifications/x3dh/
- Signal Double Ratchet  
  https://signal.org/docs/specifications/doubleratchet/
- RFC 5084 on AES-GCM authenticated attributes / AAD  
  https://www.rfc-editor.org/rfc/rfc5084.html

The generalized invariant is:

```text
Authenticate(payload)
is insufficient when acceptance semantics depend on
(payload, subject, scope, epoch, policy, destination, sequence, context).
```

Candidate fixture:

1. Keep ciphertext/signature/hash valid.
2. Move it to another message ID, room, account, chain, policy, timestamp, resource, or execution scope.
3. Acceptance must fail unless the protocol explicitly permits rebinding.

**Assessment:**  
Cryptographic context binding is known. A generic “context-complete authentication” fixture family spanning crypto, authorization, agent actions, provenance receipts, and cross-chain execution could be a distinctive practical framework.

---

### 3.9 Evidence-based confirmation

**Related prior art exists, but this appears to be one of the most promising RSI formulations.**

Many systems distinguish attempted, accepted, persisted, acknowledged, committed, finalized, executed, and verified states. However, the audit exposed a useful generic invariant:

> **A status claim must name and possess the evidence required by its semantics.**

Formally:

```text
Claim(status = S, object = O)
    => Exists(E): SatisfiedEvidencePredicate(S, O, E)
```

Examples:

```text
confirmed(message)
    => recipient_ack OR defined_durable_publication_evidence

verified(artifact)
    => verifier_identity + committed_inputs + verification_relation + verdict

executed(action)
    => execution receipt tied to exact action

included(tx)
    => proof tied to exact chain/block/tx commitment
```

This is related to provenance and attestation systems, but it is not identical to simply signing an event.

**Adjacent prior art:**

- in-toto links bind signed evidence to specific supply-chain steps, actors, materials, and products.  
  https://in-toto.io/  
  https://github.com/in-toto/docs/blob/master/in-toto-spec.md
- Formal event-correspondence verification treats security claims as relations between protocol events.

**Assessment:**  
The broad **status-to-required-evidence relation** deserves deeper literature search. It may be the best bridge to TSEI / ReceiptOS / Semantic ABI work.

---

### 3.10 Ingestion equivalence

**No exact canonical security principle with this name was identified in this research pass.**

The audit found that an object could face one validation relation through live ingestion but a weaker relation through snapshot/import.

Candidate invariant:

```text
For equivalent object O and policy P:

Accept_live(O, P)
== Accept_snapshot(O, P)
== Accept_import(O, P)
== Accept_restore(O, P)

unless the profile explicitly defines different authority semantics.
```

This resembles:

- complete mediation;
- canonical parsing / parser differential security;
- consistent validation at trust boundaries;
- supply-chain verification;
- database import validation.

But the exact **cross-ingestion relational equivalence fixture** is not a widely standardized named security primitive in the sources reviewed.

**Assessment:**  
Promising candidate for a reusable conformance rule. Novelty claim still requires a dedicated literature search across parser differentials, backup/restore security, serialization, distributed databases, and secure import systems.

---

### 3.11 Recovery completeness

The audit's formulation is:

> backup success means the stated recovery contract is satisfied.

This can be expressed as a round-trip relation:

```text
Recover(Export(S)) ≈_P S
```

where `≈_P` means equivalent under a declared protected recovery relation `P`, rather than byte-identical.

For example, a backup might claim to preserve:

- user identity;
- decryptability of old conversations;
- current trust anchors;
- membership keys;
- authorization state;
- device/session identity;
- message history.

A backup that preserves only some fields must not claim a stronger recovery relation.

**Assessment:**  
Round-trip and disaster-recovery testing are established practices. The promising aspect is defining the **protected relation explicitly** and testing semantic recovery rather than checking that an export file exists.

---

## 4. Closest conceptual ancestors

The proposed framework has several intellectual ancestors.

### A. Formal authentication correspondence

ProVerif and related formal methods already describe authentication as relations between events. RSI should acknowledge this directly.

**Difference:** RSI fixtures would be implementation-facing and adversarial: mutate or substitute a relation while preserving local validity, then test the concrete system.

---

### B. Unknown-key-share / identity-misbinding research

These attacks show that valid cryptography can still authenticate the wrong identity relationship.

**Difference:** RSI generalizes “misbinding” beyond endpoint identity to authority, policy, provenance, context, epochs, ingestion paths, recovery, and evidence semantics.

---

### C. Complete mediation and fail-safe defaults

These principles require authority checks to remain effective across all access paths and failure modes.

**Difference:** RSI attempts to make these principles executable as conformance fixtures over explicit relations.

---

### D. Capability security / confused deputy

Capability systems address the separation between designation and authority. The confused-deputy literature demonstrates that possessing authority is not equivalent to having authority for the current request.

Useful contemporary overview:
https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html

**Difference:** RSI is not an authority system. It is a verification framework for detecting when one component incorrectly inherits authority or meaning from another through an unestablished relation.

---

### E. TUF trust continuity

TUF provides a strong example of treating trust-root replacement as an explicitly authenticated transition instead of accepting newly discovered keys.

**Difference:** RSI generalizes continuity/transition checks to arbitrary protected relations.

---

### F. in-toto provenance

in-toto binds actors, steps, materials, products, and signed link metadata into a verifiable supply-chain relation.

**Difference:** RSI focuses specifically on adversarial cases where all local artifacts can remain structurally/cryptographically valid while the *linkage* between them is modified.

---

## 5. Candidate core model

A useful formal starting point:

Let a system consume components:

```text
C = {c1, c2, ..., cn}
```

and make a security-relevant claim `Q`.

The claim is usually not a property of one component. It is a property of a relation:

```text
R(c1, c2, ..., cn)
```

Examples:

```text
R_signer(signature, public_key, subject)
R_bundle(account, device, identity_key, signed_prekey, opk, epoch)
R_message(ciphertext, sender, recipient, room, sequence, session_epoch)
R_authority(discovered_record, namespace, trust_root)
R_policy(request, policy_version, authorization_decision)
R_confirmation(operation, status, evidence)
R_provenance(artifact, producer, context, policy, receipt)
R_import(object, validation_profile, destination_state)
R_recovery(pre_state, exported_artifact, restored_state, recovery_contract)
```

### Relational acceptance rule

A system MUST NOT promote local validity into semantic/security validity unless the required protected relation is established.

```text
LocalValid(c1) ∧ LocalValid(c2) ∧ ...
    ↛
SecurityClaim(Q)

unless

VerifiedRelation(R(c1, c2, ...))
```

### Relation substitution test

Given a known-good tuple:

```text
T0 = (a, b, c, d)
```

construct:

```text
T1 = (a, b', c, d)
```

where `b'` is individually valid, but:

```text
R(a, b', c, d) = false
```

The system must reject `T1` if `R` is protected.

This is the central candidate fixture pattern.

---

## 6. Candidate taxonomy of relation failures

### 6.1 Subject substitution

A valid authenticator is bound to the wrong subject.

Examples:

- attacker signature + victim identifier;
- valid identity key returned for another account;
- valid agent credential attached to another agent identity.

---

### 6.2 Scope substitution

An artifact valid in scope A is replayed in scope B.

Examples:

- ciphertext moved between rooms;
- authorization moved between resources;
- receipt reused across chain/deployment/context;
- proof reused under another policy version.

---

### 6.3 Epoch substitution

A historically valid relation is reused after an authorized state transition.

Examples:

- old bootstrap after ratchet transition;
- old trust root after rotation;
- old membership key after revocation epoch;
- stale policy after update.

---

### 6.4 Authority substitution

Discovery or representation is mistaken for authority.

Examples:

- discovered issuer overwrites pinned issuer;
- self-reported source class treated as provenance;
- API-returned identity treated as authenticated identity;
- registry pointer interpreted as authorization without historical binding.

---

### 6.5 Evidence substitution

A label/status is treated as if the evidence implied by that label exists.

Examples:

- `confirmed` without persistence or acknowledgement;
- `verified` without closed verifier inputs;
- `executed` without execution receipt;
- `included` without inclusion proof.

---

### 6.6 Path substitution

An object rejected through one trust boundary is accepted through another path.

Examples:

- live validation vs snapshot import;
- API validation vs backup restore;
- direct execution vs fallback execution;
- canonical serializer vs alternate serializer.

---

### 6.7 State-commit substitution

Tentative state is promoted to durable state before the relation authorizing it is established.

Examples:

- session state committed before AEAD authentication;
- authorization reservation consumed before request binding;
- registry mutation committed before signature verification.

---

### 6.8 Concurrency substitution

Two operations each observe themselves as the unique consumer of the same logical state position.

Examples:

- duplicate nonce/message key;
- double-spend of one ratchet revision;
- concurrent claim of a one-time token;
- duplicate sequence assignment.

---

## 7. Proposed conformance fixture format

A minimal fixture could be:

```json
{
  "schema": "relation-binding-fixture.v0",
  "id": "RBF-AUTH-SUBJECT-001",
  "protected_relation": "signer_to_subject",
  "control": {
    "components": ["artifact", "signature", "signer_key", "subject"],
    "expected": "ACCEPT"
  },
  "mutation": {
    "preserve_local_validity": ["artifact", "signature", "signer_key"],
    "change": ["subject"],
    "relation_expected": false
  },
  "expected": "REJECT",
  "failure_if": [
    "accept",
    "state_commit",
    "authority_promotion",
    "status_upgrade"
  ]
}
```

A stronger format should also bind:

- canonical serialization;
- exact input bytes/digests;
- policy/profile version;
- evaluator implementation/version;
- initial durable state digest;
- final durable state digest;
- accepted/rejected outcome;
- emitted side effects;
- required evidence;
- relation oracle.

---

## 8. Proposed initial fixture suite

| ID | Protected relation | Mutation | Required result |
|---|---|---|---|
| RSI-001 | signer → subject | attacker signs locally valid victim-shaped object | reject |
| RSI-002 | discovery → trust root | replace pinned key with valid discovered key | reject / quarantine |
| RSI-003 | auth → state commit | invalid ciphertext triggers tentative session | reject + zero durable mutation |
| RSI-004 | ratchet position → consumer | two parallel sends consume same revision | exactly one consumer per position |
| RSI-005 | bootstrap → epoch | replay old valid bootstrap after session advance | reject / explicit replacement path |
| RSI-006 | ciphertext → context | move valid ciphertext to another room/id/scope | reject |
| RSI-007 | mandatory policy → fallback | authorizer unavailable | policy remains mandatory |
| RSI-008 | status → evidence | transports fail, status attempts `confirmed` | status must not upgrade |
| RSI-009 | object → ingestion policy | same invalid object via live/import/snapshot | equivalent rejection |
| RSI-010 | export → recovery contract | restore from “complete backup” | declared properties preserved |
| RSI-011 | membership → confidentiality epoch | removed member retains prior key | future-content guarantee must match actual rotation semantics |
| RSI-012 | device → account identity | second device publishes incompatible bundle | explicit device semantics / no silent replacement |

---

## 9. Novelty matrix

Legend:

- **Established** — substantial direct prior art.
- **Adjacent** — known ideas exist, but the exact fixture/generalization is less obvious.
- **Promising** — this research pass did not find an obvious standardized equivalent.
- **Unverified** — requires deeper dedicated literature/patent/standards search.

| Candidate | Prior art | Novelty assessment |
|---|---|---|
| Signer-to-subject binding | UKS/misbinding, formal authentication | Established |
| Signed pre-key / identity continuity | X3DH, Signal safety numbers | Established |
| Authentication-before-commit | Sesame transactional receive semantics | Established in messaging |
| Nonce uniqueness | AEAD standards | Established |
| Atomic ratchet consumption under concurrency | nonce rules + concurrent state management | Adjacent |
| Replay across epochs | protocol replay / anti-rollback | Established |
| Trust-root non-substitution | TUF continuity | Established |
| Policy-preserving fallback | fail-safe defaults | Established principle; fixture is adjacent |
| Context-complete authentication | AEAD AAD, transcript binding | Established |
| Evidence-based confirmation | attestations, event correspondence, receipts | **Promising as a generic status/evidence invariant** |
| Ingestion equivalence | complete mediation, parser/validation consistency | **Promising as an explicit cross-path fixture** |
| Recovery completeness under declared relation | backup/restore semantics | Adjacent / promising |
| Relation-substitution fixture family | misbinding + formal correspondence + conformance testing | **Promising synthesis** |
| Single protected-relation taxonomy spanning crypto/auth/provenance/policy/state | many adjacent literatures | **Promising synthesis; novelty unverified** |

---

## 10. Strongest candidate contribution

The strongest candidate is not a new cryptographic primitive.

It is a **testing and specification methodology**:

### Relational Security Invariants (RSI)

A security claim is admitted only if all protected relations needed by that claim are explicitly established.

### Relation-Binding Conformance Fixtures (RBCF)

Adversarial tests that:

1. start from a valid control;
2. preserve local validity of the relevant artifacts;
3. mutate exactly one protected relation;
4. verify that acceptance, state mutation, authority promotion, or status promotion does not survive the relation break.

This creates a useful distinction:

```text
component validity
vs.
relation validity
vs.
claim validity
```

Many production bugs occur because systems collapse those three levels.

---

## 11. Connection to protected-relation work

The audit's best generalized finding is structurally compatible with the protected-relation idea:

> **Weak/local observational equality must not imply equality of the protected semantic relation.**

Security version:

> **Local cryptographic, syntactic, or structural validity must not imply validity of the protected authority/identity/context/evidence relation.**

This can be expressed as:

```text
P_local(S0) = P_local(S1)
but
R_protected(S0) != R_protected(S1)
```

A conforming verifier must discriminate `S0` and `S1` whenever its claim depends on `R_protected`.

That gives a clean bridge between:

- adversarial structural fixtures;
- authentication binding;
- provenance;
- semantic ABI / action constraints;
- recomputation profiles;
- execution receipts;
- stateful cryptographic protocols.

---

## 12. Candidate standard language

Possible normative language:

### RSI-CORE-1 — No relation inheritance

> An implementation **MUST NOT** infer a protected relation solely from the independent validity of its constituent artifacts.

### RSI-CORE-2 — Explicit protected relation

> A verification profile **MUST** identify every relation whose failure can change the truth of the claimed security or semantic property.

### RSI-CORE-3 — Relation substitution resistance

> Replacing one relation endpoint with an independently valid but unauthorized endpoint **MUST** cause rejection when the protected relation no longer holds.

### RSI-CORE-4 — Authentication before durable commitment

> State derived from unauthenticated input **MUST NOT** become authoritative or durable before the authenticating relation succeeds.

### RSI-CORE-5 — Path invariance

> Equivalent inputs evaluated under the same policy **MUST** receive equivalent admission results across all supported ingestion paths, unless the profile explicitly specifies different authority semantics.

### RSI-CORE-6 — Evidence-bounded status

> A status **MUST NOT** imply evidence stronger than the evidence actually obtained and bound to the exact subject, scope, and operation.

### RSI-CORE-7 — Epoch continuity

> A relation valid in epoch `e` **MUST NOT** be treated as valid in epoch `e+n` unless an authenticated continuity or transition rule establishes that validity.

### RSI-CORE-8 — Atomic consumption

> A one-time authority, nonce position, sequence position, ratchet position, or other consumable relation **MUST** have at most one successful consumer.

---

## 13. What should *not* be claimed yet

Do **not** currently claim:

- “first framework to reason about security relations”;
- “new class of identity-misbinding vulnerability”;
- “new authentication theory”;
- “new replay-protection principle”;
- “first evidence-binding standard”;
- “mathematically novel”;
- “no prior art.”

Those claims are not supported by this research pass.

A defensible statement today is:

> A preliminary prior-art review found extensive work on the individual mechanisms, but did not identify a single implementation-facing conformance framework that unifies signer/subject, authority/root, context, epoch, state-commit, ingestion-path, recovery, and status/evidence relations under one adversarial relation-substitution fixture model.

That is a **research finding**, not a final novelty proof.

---

## 14. Next research required before publication

A publication-grade novelty review should search at least:

### Formal protocol verification
- Lowe authentication hierarchy;
- correspondence assertions;
- agreement / injective agreement;
- strand spaces;
- Tamarin;
- ProVerif;
- CryptoVerif.

### Cryptographic composition
- context binding;
- channel binding;
- transcript binding;
- unknown-key-share;
- identity misbinding;
- cross-protocol attacks;
- domain separation.

### Authorization
- complete mediation;
- confused deputy;
- capability systems;
- object-capability security;
- fail-safe defaults;
- policy decision/enforcement point consistency.

### Distributed/stateful security
- anti-rollback;
- state continuity;
- fork consistency;
- transactional cryptographic state;
- crash consistency;
- nonce allocation under concurrency.

### Provenance / attestations
- in-toto;
- SLSA;
- DSSE;
- Sigstore;
- SCITT;
- RATS/EAT;
- transparency logs;
- proof-carrying data.

### Data ingress / parser security
- parser differentials;
- canonicalization attacks;
- alternate ingestion paths;
- backup/restore validation;
- deserialization trust boundaries.

### AI-agent execution / receipts
- action authorization;
- deterministic policy gates;
- signed execution receipts;
- evidence-bound agent actions;
- semantic constraints across tool calls.

A patent search should be separate if commercial IP claims matter. This document is a technical prior-art review, not legal advice or a patentability opinion.

---

## 15. Recommended repo/document structure

If this becomes a standalone project:

```text
relational-security-invariants/
├── README.md
├── spec/
│   ├── RSI-core-v0.md
│   ├── terminology.md
│   ├── threat-model.md
│   └── conformance.md
├── schema/
│   └── relation-binding-fixture.v0.schema.json
├── fixtures/
│   ├── signer-subject/
│   ├── trust-root/
│   ├── auth-before-commit/
│   ├── atomic-consumption/
│   ├── replay-epoch/
│   ├── context-binding/
│   ├── policy-fallback/
│   ├── evidence-status/
│   ├── ingestion-equivalence/
│   └── recovery/
├── adapters/
│   ├── messaging/
│   ├── provenance/
│   ├── agent-actions/
│   └── distributed-state/
└── research/
    ├── prior-art.md
    └── case-studies/
```

---

## 16. Recommended immediate experiment

Before writing a large paper, build a **10–12 fixture proof-of-concept** against two or three unrelated systems.

The key test for whether RSI is genuinely useful is:

> Can the exact same fixture schema expose relation failures in systems from different domains without redefining the core semantics each time?

Suggested targets:

1. the audited decentralized messenger;
2. one provenance / receipt workflow;
3. one agent/action authorization workflow.

If the same core mutation model works across all three, that is much stronger evidence that the framework captures a real reusable abstraction instead of merely renaming known messaging bugs.

---

## 17. Bottom line

### Known / established

The field already knows that:

- valid signatures can be bound to the wrong identity;
- authenticated key exchange needs identity binding;
- prekeys need authentication and lifecycle semantics;
- AEAD nonce reuse is catastrophic;
- replay and rollback require explicit handling;
- failed authentication must not be treated as successful protocol completion;
- trust roots require continuity;
- mandatory authorization should fail safely;
- context often belongs inside authenticated data;
- provenance needs authenticated actors and artifact links.

### Potentially new or at least under-standardized

The strongest candidate is the **cross-domain unification and fixture methodology**:

> preserve each local component's validity, mutate only the protected relation, and require the implementation to distinguish the mutated case before it promotes identity, authority, state, policy, provenance, or status.

That is concrete enough to specify, implement, fuzz, and turn into conformance vectors.

It is also sufficiently different from “a list of security best practices” because each rule has:

- an explicit protected relation;
- a control pair;
- a discriminating mutation;
- an acceptance oracle;
- state/evidence side-effect constraints;
- a reusable machine-readable fixture.

This is the direction worth developing.

---

## References

1. Signal — The X3DH Key Agreement Protocol  
   https://signal.org/docs/specifications/x3dh/

2. Signal — The Double Ratchet Algorithm  
   https://signal.org/docs/specifications/doubleratchet/

3. Signal — Sesame Algorithm: Session Management for Asynchronous Message Encryption  
   https://signal.org/docs/specifications/sesame/

4. Signal Support — Safety numbers and identity-key changes  
   https://support.signal.org/hc/en-us/articles/360007060632-What-is-a-safety-number-and-why-do-I-see-that-it-changed

5. RFC 5084 — Using AES-CCM and AES-GCM Authenticated Encryption in CMS  
   https://www.rfc-editor.org/rfc/rfc5084.html

6. RFC 8844 — Unknown Key-Share Attacks on Uses of TLS with SDP  
   https://www.rfc-editor.org/rfc/rfc8844.html

7. Sethi, Peltonen, Aura — Misbinding Attacks on Secure Device Pairing and Bootstrapping, AsiaCCS 2019  
   https://doi.org/10.1145/3321705.3329813

8. Peltonen, Sethi, Aura — Formal verification of misbinding attacks on secure device pairing and bootstrapping, JISA 2020  
   https://doi.org/10.1016/j.jisa.2020.102461

9. ProVerif manual — correspondence assertions and authentication  
   https://publications.bensmyth.com/files/ProVerif-manual-version-2.00.pdf

10. Saltzer & Schroeder — The Protection of Information in Computer Systems, 1975  
    https://doi.org/10.1109/PROC.1975.9939  
    https://www.cs.virginia.edu/~evans/cs551/saltzer/

11. The Update Framework specification  
    https://theupdateframework.github.io/specification/draft/

12. in-toto specification  
    https://github.com/in-toto/docs/blob/master/in-toto-spec.md

13. in-toto documentation  
    https://in-toto.io/docs/getting-started/

14. AWS — The confused deputy problem  
    https://docs.aws.amazon.com/IAM/latest/UserGuide/confused-deputy.html
