# PQ authority evidence closure v0

Design/evidence only. RSI main remains `05f3853756ad9deb0e5d08d54dfdfd462652a801`. No code, schemas, prior design files or external repositories modified.

**Decision: YELLOW (scope clarification, no model defect). Generic Relation Profile implementation is ready for approval under the explicit policy-only/authentication boundary. Full authenticated-current-authority validation is NOT established by this evidence pass.**

## Exact source set

Repository `trustless-ai/recompute-kit`, canonical branch `main`, exact SHA `15f7f59ac47b3358492bd5741143c418b5d657f5`. All files below are under `conformance/pq-key-binding-v0/`; full SHA-256, Git blob IDs, source classes and identifiers appear in [the closure source map](relation-profile-evidence-closure-v0.json).

| File | Class | Authority/evidence boundary |
|---|---|---|
| `pq-key-binding-v0.spec.md` | Normative profile plus reported deployment claims | Binding/genesis signatures, anchor-time cutoff, predecessor rotation, revocation and historical eligibility |
| `pq-key-binding-v0.rotation.json` | Signed-object artifact | Successor statement, predecessor pointer/key, two signature byte strings; existence is not verification |
| `pq-key-binding-v0.rotation-vectors.json` | Policy vectors | Seven resolution/cutoff cases using supplied chain and validity flags; intended successor anchor time |
| `pq-key-binding-v0.revocation.json` | Signed-object artifact | Revocation target statement and authorization bytes |
| `pq-key-binding-v0.revocation-vectors.json` | Policy vectors | Six before/at/after revocation cases |
| `pq-key-binding-v0.cutoff-vectors.json` | Policy vectors | Eight pre/post-cutoff, wrong-key, no-binding and revocation-slot cases |
| `pq-key-binding-v0.vectors.json` | Binding vectors/artifacts | Genesis binding statements and commitments; not a complete freshness proof |
| `cutoff_enforce.py` | Reference implementation | Selection from supplied history; companion present/valid/key equality; no signature or transition authentication |
| `deep_recompute.py` | Reference implementation | Hash/canonical-string/Merkle/offline record consistency; signature checks deferred |
| `gate.py`, `suite.json` | Gate implementation / manifest | Hash-oriented suite and exact artifact pins; suite inclusion is not verification of every artifact field |

No mutable endpoint, unpublished gateway implementation, or signature selftest response is treated as source authority. No signature library was installed, no signatures or chain inclusion were independently verified here. Policy functions were executed read-only in memory against pinned vectors: cutoff 8/8, rotation 7/7, revocation 6/6 matched their recorded outcomes. These totals are source-vector reproduction, not new RSI fixtures, baseline tests or mutation kills.

## What establishes an authorized transition?

The source **does define** an authenticated transition relation and contains an object intended to witness it. It does **not** follow that the shipped offline gates prove the complete authenticated chain is currently authoritative.

| Evidence level | Present / established? | Exact conclusion |
|---|---|---|
| A. Policy selects new key | Yes, under supplied history | `resolve_in_force` chooses the latest eligible binding by supplied anchor time |
| B. Cutoff/as-of vector | Yes | Exercises supplied temporal boundaries, not their historical authenticity |
| C. Old/new key IDs | Yes | Identifies operands; keys alone authorize nothing |
| D. Transition object | Yes | `rotation.json` contains successor statement and predecessor reference |
| E. Object authenticated | Spec requires it; signatures present; not verified here | Must verify predecessor continuity and successor possession over the recomputed content-address |
| F. Independently verifiable chain | Partially supported as a procedure; not closed evidence | Bytes and algorithm identified; offline deep gate does not verify signatures or trusted-root chain/anchor closure |
| G. Current authority recomputable from complete pinned evidence | Not established | Successor anchor is intended in policy vectors; history completeness/freshness and anchor evidence are not proven by supplied arrays |

### Concrete rotation object

`rotation.json` carries:

- subject/classical account: `0xFf9a176577Fb42b6bc9c19fd05a241e8fCd0ca14`;
- predecessor binding: `b26a01590215926373544dc82d22fadc8d97c98debaae5d6ce8899b83ffd05da`;
- successor content-address: `4fe636a4d0db42061aec75dc07747fdd3be68d0d2985d783e71a0cfa98960028`;
- successor statement fields: schema `kya.pq_key_binding.v0`, subject, new `pq_pubkey`, algorithm `SLH-DSA-SHA2-192s`, `bound_at=1788000000`, profile, predecessor content-address and rotation index 1;
- `continuity_signature`: predecessor PQ key signs `canonical_content_sha256`;
- `pq_companion_signature`: successor key signs that same digest (possession).

The required preimage is the source-canonical statement; SHA-256 produces the 32-byte signed content-address. Independent checks in this pass confirmed canonical string equality, content-address recomputation, and equality of the statement's predecessor pointer with the artifact's predecessor object. They did not verify either signature.

Source-prescribed verification requires recomputing the successor address, resolving the predecessor's trusted binding/key, verifying continuity under that predecessor key and possession under the new key using the identified algorithm, and establishing the applicable anchor boundary. The exact account/new-key/predecessor/profile fields are inside the hashed statement, so substitution changes the signed message **if the signatures and predecessor authority are actually verified**. A self-supplied predecessor key is not a trust root.

The object has `bound_at` and `rotation_index`; neither is by itself authenticated anchor time or a demonstrated general replay/fork policy. The rotation vectors explicitly describe 1788000000 as an **intended** on-chain anchor. The object contains no successor on-chain inclusion receipt that closes that step. Genesis chain/transaction coordinates are reported in the spec; this pass does not turn those coordinates into an independently verified chain read.

### Source inconsistency / scope mismatch

The spec says the rotation signatures “both verify in the deep lane.” The actual `deep_recompute.py::check_rotation` checks only the statement content hash and optional canonical string, then returns deferred signature checks. Its deferred labels say **ML-DSA**, while the pinned rotation/revocation objects identify **SLH-DSA-SHA2-192s**. The file refers to live gateway selftests, but their pinned implementation/results are not included in this reviewed source set.

Preserve all three facts: a normative continuity requirement, actual signature bytes with an algorithm identifier, and an offline gate that does not verify them. Do not infer verified cryptography from the word deep, from suite success, or from the mismatched label. This bounds the stronger claim as unsupported; it does not make the generic Relation Profile model inadequate.

## Case matrix

`not established` is an evidence-review statement, not an invented PQ API enum. ADMIT/REJECT in the policy column are conditional on supplied history/validity evidence. `anchor_time` is artifact anchor time, not verification time or self-reported creation time.

| Case | Local crypto validity | Current authority | Historical/as-of authority | Transition evidence | Claim admissibility | RSI candidate relation outcome | Source support / limitations |
|---|---|---|---|---|---|---|---|
| Key A before cutoff, proven anchored and governing | Classical eligibility assumed; policy gate does not check crypto | Irrelevant to this historical lookup | A at artifact anchor | Supplied genesis history; full lane needs trusted binding/anchor | Policy ADMIT `anchored_before_cutoff` | Historical eligibility under declared evidence scope | cutoff vector `pre-cutoff anchored, no companion`; missing binding still rejects |
| Key A after cutoff, A still in force | Needs valid PQ companion under A; classical-only insufficient | Not independently established; policy supplied A | A | No rotation required merely because cutoff passed | ADMIT with valid in-force companion; REJECT without it | Preserve conditional policy outcome, not blanket retired-key rejection | cutoff valid/no-companion vectors; cutoff is not automatically rotation |
| Retired A after rotation and cutoff | Companion `valid:true` under A in vector | Supplied successor B | B at later artifact anchor | Supplied two-binding policy history | REJECT `post_cutoff_no_valid_companion` | Local-valid flag does not imply in-force key relation | rotation vector `post-cutoff after rotation, companion under RETIRED key`; no crypto checked |
| B after cutoff with valid authenticated transition | Requires verified companion B plus verified transition/possession | B only with complete applicable history | B at artifact anchor | Normative old-key/new-key signatures plus anchor; artifact present but full proof not verified here | Full claim conditional; policy ADMIT under supplied B history | Policy result reproducible; full authority claim unsupported in this pass | rotation NEW-key case; spec Rotation; intended successor anchor limitation |
| B after cutoff without authenticated transition evidence | Signature B could be locally valid | Cannot establish B from that fact | Cannot establish authorized B | Absent/unverified | No full authorization promotion | Full lane unavailable/unsupported; policy-only function may still ADMIT if given B in its array | `cutoff_enforce.py` never checks predecessor signatures; not a source-defined universal REJECT for a missing proof API |
| Historical A artifact verified after cutoff/rotation | Classical verification still relevant; optional PQ companion | May now be B | A if artifact was anchored in A's era | Retained trustworthy historical binding/anchor evidence required | Remains historically eligible; current-key difference does not invalidate it | Preserve as-of authority and `anchored_before_cutoff` result | spec Verifier rule/Rotation/Revocation; between-rotations and before-revocation vectors; signing before cutoff alone is insufficient |
| Substituted subject, locally valid signature | Crypto under a key can remain valid | Wrong-subject key does not prove this subject's authority | Must resolve matching subject binding | Signed binding must include subject and trusted predecessor | No full subject-authority promotion | Subject relation not established; policy-only result cannot settle it | spec binding statement/per-agent distinction; policy artifact grammar has no subject check, so exact subject-substitution negative is not covered by these vectors |
| Stale binding snapshot | Signatures in snapshot may be valid | Latest authority/completeness not established | May support an older artifact only if governing history is sufficiently evidenced | Missing later rotation/revocation evidence may be material | No current-authority claim from stale snapshot | Preserve evidence-unavailable boundary; do not fabricate current authority | `resolve_in_force` selects max in supplied list only; no freshness/completeness proof or universal stale-snapshot result |

## Historical validity, precisely

PQs cutoff rule is by **proven anchor time**. An artifact signed before cutoff but anchored only later does not gain the pre-cutoff exemption merely from its signature timestamp. For an artifact genuinely anchored before consumer cutoff, under a governing binding, classical-only eligibility is retained; a later verification time/current key does not rewrite that historical relation.

The enforcer first requires an eligible binding: `binding_anchor_time <= artifact.anchor_time`, excluding a binding when `artifact.anchor_time >= revoked_at`, then chooses the latest eligible time. Pre-cutoff is strict `< consumer_cutoff`. A governing binding plus valid companion under its key can admit post-cutoff artifacts. Revocation at time T excludes artifacts at/after T, while earlier anchored artifacts retain their historical eligibility. Source P3 vectors distinguish exactly-at from before.

Archived authenticated binding/anchor evidence must remain available to substantiate this history. Missing evidence cannot establish historical authority; the current policy function has no complete evidence-availability protocol and does not specify a universal `unresolved` string for that case. Relation Profile should report its inability to establish the full claim without relabeling it as a source-computed REJECT or asserting acceptance. Current authority and historical authority must remain separate, including when the same key appears in both.

## Recommended decomposition

The proposed three relations are useful **review decomposition**, not newly discovered source protocol names:

| Relation | Endpoints | Required evidence / temporal scope | Outcome and dependent claim |
|---|---|---|---|
| R_transition | Trusted old binding -> signed successor statement -> new binding/key | Exact preimage, old-key continuity signature, new-key possession, predecessor identity; authenticated activation anchor | Authenticated succession only when all required evidence verifies; artifact presence alone insufficient |
| R_auth | Subject -> governing binding/key at anchor/as-of | Trusted genesis and relevant authenticated history, subject binding, rotation/revocation boundaries and evidence completeness appropriate to claim | Governing key or no governing binding; current-authority claim requires current evidence, not a historical snapshot |
| R_artifact | Artifact content-address/signature -> governing key | Artifact bytes/anchor, companion verification under resolved key, consumer cutoff | Policy ADMIT/REJECT with resolution reason; historical exemption separate from post-cutoff companion requirement |

R_transition supplies authenticated history to R_auth; R_auth supplies a scoped key to R_artifact. Do not let R_auth merely trust R_transition's declared label, or let policy success retroactively authenticate its inputs. A policy-only profile starts with supplied history/validity evidence and must explicitly stop its claim there.

## Comparison with the unchanged design draft

| Issue | Assessment | Draft support |
|---|---|---|
| Boolean vs categorical outcomes | GREEN | §5 allows source-native categories and non-evaluated states |
| Current vs historical authority | GREEN | §7 requires source-defined time/reference, inclusive boundaries and missing-evidence behavior |
| Authenticated transition edge | GREEN | §§2,5,7 support required evidence, component checks and claim limits |
| Policy evidence vs verified proof | GREEN | §7 already explicitly calls validity flags assumptions of a policy-only lane |
| Claim/promotion binding and independent expectations | GREEN | §§5,8 forbid elevation from declaration or adapter self-validation |
| Exact shipped deep-lane coverage | YELLOW | Wording should explicitly record hash-only gate and SLH-DSA/ML-DSA mismatch |
| Generic core changes / new result model | GREEN | None required to represent separate scoped outcomes/evidence |

Proposed clarification only, **not applied**:

```diff
  An input valid:true is not independently verified cryptography.
+ The pinned PQ offline deep gate verifies hashes, not rotation signatures.
+ Signature bytes and a declared algorithm establish a verification candidate,
+ not authenticated current authority. Policy-only conformance may proceed
+ with explicitly supplied history; full authority-transition claims remain
+ unsupported until signature, trusted-chain and applicable-anchor evidence close.
```

The two remaining questions are closed as **evidence boundaries**, not as proof that every domain case succeeds. Under the user's decision rule, the generic contract can proceed to implementation approval: existing draft already represents richer outputs and refuses unsupported authority claims. This is not approval to implement external PQ adapters or to announce verified authenticated rotation. No prior design edits are required to repair a semantic model; the proposed wording should be acknowledged before implementation.
