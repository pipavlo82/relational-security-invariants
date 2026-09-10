# Relation Profile comparison v0 — design only

Status: architecture recommendation for review; **not an approved schema or implementation**. No adapter is implemented. Exact RSI main inspected: `05f3853756ad9deb0e5d08d54dfdfd462652a801`. GitHub reports the repository private with default branch main.

**Recommendation: Option B**, a separately pinned Relation Profile Contract plus a new, minimal fixture envelope. Preserve every v0 schema and fixture; register the finite synthetic model as a compatibility relation profile. Do not pretend the existing registered-fixture wrapper already provides semantic extensibility.

The current synthetic model exposed an overfit assumption when confronted with the first real source-defined relation. The purpose of the Relation Profile design is to remove that bias without weakening RSI's core invariant. This is architecture refinement, not a new security theory, universal relation calculus, or novelty claim.

## Evidence and preservation boundary

The [source map](relation-profile-source-map-v0.json) records exact repository, commit, path, Git blob OID, SHA-256, source class, and claim boundary for every external source below. References such as CR1 or P5 resolve to that inventory. The inventory also records all 78 tracked RSI file hashes and the three pre-existing untracked Crystal Receipt reports. Those reports were present before this pass, despite the supplied clean-tree description, and are preserved.

| Source authority | Exact canonical main inspected | Method |
|---|---|---|
| `pipavlo82/crystal-receipt` | `45b46bf7df3a60b32583291f577a36bf19d22f00` | Exact committed Git blobs in the local repository; GitHub main checked |
| `trustless-ai/recompute-kit` | `15f7f59ac47b3358492bd5741143c418b5d657f5` | GitHub exact-SHA contents; main checked |
| `pipavlo82/recomputable-verification-receipts` | `287c0ea1c2578c1833405bc2476975f95addbada` | GitHub exact-SHA specification; main checked |

Crystal Receipt's active worktree is a feature branch at `46bed9ba8662ede63f0682ac6d2c93e52b6536cd`, with tracked files clean and 14 pre-existing untracked entries. It is not the selected authority. No checkout, fetch, source execution, or external write was performed. A local PQ repository was inspected for metadata only; its branch is master, and it is not used as semantic authority. Read-only GitHub retrieval establishes repository artifact identity, not deployed behavior or cryptographic validity.

These are four relation families, **not four independent implementations or repositories**. CR and TSEI share a repository. The amendment specification explicitly identifies PQ rotation as a design ancestor. Evidence from those two alone is not independent support for a universal temporal calculus. No ERC-wide conformance claim follows from the bounded RVR/companion suites.

The supplied 150/150 optimized tests, 36 PASS and 16 KILLED baseline is retained as previously verified evidence, not a test run performed in this design pass. No existing code, schema, fixture, expectation, predictor or normative spec is edited. The new `.design.md` is a candidate document only.

## 1. What the current model actually requires

Inspected RSI files include `spec/RSI-core-v0.md`, the extension/expectation contracts, all five files under `schema/`, `rsi/oracle.py`, `rsi/codec.py`, `profiles/synthetic.py`, `runner/execution.py`, `runner/expectation_contract.py`, `runner/expectation_registry.py`, and `extensions/defaults.py`. The source map preserves the complete tracked inventory; it does not imply every inventoried file was semantically reviewed.

A = genuinely cross-domain structural concept; B = relation-profile-specific semantics; C = synthetic-only bias **when imposed universally**; D = insufficient evidence for a universal requirement. A finite synthetic constraint remains valid for its own profile even when classified C.

| Current field or constraint | Class | Actual meaning and evidence |
|---|---|---|
| `schema`, `$id`, versioned serialization contract | A | A stable interpretation boundary is structurally necessary; it does not establish truth. |
| `id` | A | Opaque identity. Original schema enumerates six IDs; registered wrapper permits restricted identifiers. The original closed set is C. |
| `protected_relation` concept | A | A declared relation is necessary across all families. |
| Its six-value enum | C | `signer_to_subject`, `authentication_before_commit`, `atomic_consumption`, `context_binding`, `evidence_bounded_status`, `ingestion_equivalence` are finite synthetic coverage, not the source vocabularies CR1/T1/R2/P1. |
| `mutation_model` | B | Relation substitution is portable; fixed enum (`relation_substitution`, `invalid_authentication`, `concurrent_schedule`, `cross_path`) and its operation assumptions are not universal. Mutation effectiveness must remain independently checked. |
| `profile_version = rsi-reference-profile.v0` | C | It fixes one interpretation. Version identity itself is A. |
| `cases` and explicit case identity | A | Deterministic inventory needed for admission and discrimination. |
| Exactly three cases; `name` limited to control/mutation/mirror_positive | B | Useful conformance-family obligations; not a universal cardinality or proof that those roles were achieved. The oracle/corpus validator adds checks beyond array length. |
| `local_validity_expected` | B | Author-declared expectation, not independent local validation. A single boolean loses per-component and unavailable distinctions. Never derive relation truth from it. |
| `requests` slot map | A/B | Explicit execution inputs are structural; request meaning is profile-specific. The original two fixed adapter keys were C, already removed by the extension wrapper. |
| `operation` enum | B/C | `admit`, `transition`, `consume`, `confirm`, `ingest` are semantic operations of synthetic v0. Universal restriction excludes CR `semantic_snapshot`. |
| Mandatory `proof` on every operation | C | A signature is absent from CR snapshot and TSEI generic preservation; RVR binding suites explicitly separate crypto verification. |
| `proof.payload_hex` | B | Exact bytes are portable; requiring a nonempty hex-encoded signed payload, max 32768 characters, is profile-specific. |
| `proof.public_key_hex`, `signature_hex` | B | 64/128 lowercase hex lengths plus the oracle's Ed25519 verification fix a crypto lane. Not PQ key sizes or universal component validity. |
| Mandatory `policy` on every operation | C | CR snapshot has no authorization policy. TSEI history policy and PQ consumer cutoff are real but different policies. |
| `policy.subject_key`, `scope`, `policy_version` | B | Synthetic authorization relation; each must match independent signed payload fields. A broad context concept is not permission to rename snapshot equivalence as context binding. |
| `policy.evidence_key`, `evidence_kinds` | B/C | Semantic for `confirm`; mandatory even for operations that do not consult them. Original corpus shape, not universal evidence grammar. |
| Mandatory `state` | C | Pure snapshot/commitment comparison has no durable-state transition. |
| `state.revision`, `state.head` | B | Captured synthetic authority projection, bounded integer and nonempty string. Not a generic epoch/history model. |
| `consume.schedule[].kind`, `.worker` | B | Read/commit interleaving with bounded length, not actual concurrency or PQ rotation. |
| `confirm.evidence[]` | B | Qualifying signed receipts, max 16; the abstract need for evidence is shared but this shape is not. |
| `ingest.paths` | B/C | Exactly live/snapshot/import/restore. These paths do not define external domain semantics. |
| Closed objects / required properties | A/B | Fail-closed shape validation is structural; the permitted member set belongs to the selected profile. Arbitrary extra fields are not an extension strategy. |
| Fixed lengths, limits, enum cardinalities | B/D | Keep for legacy resource/contract safety; no evidence these particular limits are universally correct. |
| `x-canonical-serializer = rsi-json-ascii.v0` | B | Honest transport restriction, not JCS or TSEI serialization. Exact evidence bytes may be transported losslessly; never recanonicalize a source using this codec. |

Semantic behavior also lives outside schema fields. `rsi/oracle.py` reads the decoded payload's scope/policy version, evidence operation ID/kind, public keys, and captured state; it increments revision, computes head, implements evidence qualification and CAS schedules. This is the **legacy synthetic predictor**, not a domain-neutral relation interpreter. Keep its bytes unchanged and bind it only to its legacy profile.

The legacy observation schema also has finite semantics: `results[].decision` is ACCEPT/REJECT/CONFLICT/UNVERIFIABLE; `before` and `after` are mandatory revision/head state; `effects` is at most one of admitted/transitioned/consumed/confirmed; label and nullable position are required. These are B, not the top-level conformance taxonomy. Making CR emit these state/effect fields would fabricate behavior. Do not widen this old schema in place.

`runner/execution.py` compares encoded `observation` objects exactly after profile validation. It does not require the legacy observation schema itself: `profiles/synthetic.py` supplies that validator. The `local_validity` prediction member is relayed from the admitted reference, not independently observed by the runtime. A new profile must therefore include actual component-check evidence in its observation; copying this reference member is not proof that the adapter checked components. The generic codec remains ASCII/integer JSON, another explicit transport boundary.

## 2. Source-defined families

### A. Crystal Receipt: semantic snapshot and external audit metadata

Authority: CR1 frozen `counterfactual-audit-boundary-v0/SPEC.md`; CR2 `V-SEM-MANIFEST-INVARIANT`; CR3 `V-SEM-MUTATION-DIFFERS`.

- Relation: equivalence of accepted semantic snapshots across packaging changes. Endpoints are the two semantic inputs/snapshots, not signer and scope. External manifests accompany those inputs but are outside the semantic projection.
- Scope: this frozen audit-boundary profile only, not all ReceiptOS authorization, graph traversal or receipt admission.
- Local validity: each input admits descriptor-safe snapshot construction. Internal `audit_timestamp` is malformed and rejected, never stripped. External `audit_timestamp` is permitted.
- Relation validity: canonical snapshots match for the manifest variants; they differ when the source semantic field is changed. Both sides of CR3 remain `accepted_snapshot`.
- Claim: semantic identity is preserved, or cannot be inherited for the changed semantic artifact. Neither `accepted_snapshot` nor equality authorizes a producer, signer, policy or durable write.
- Evidence/context: full semantic input, external manifest variants and the pinned snapshot contract. Packaging is optional non-semantic data. No required signature, proof object, authorization policy, epoch, as-of or durable state.
- Mandatory mirror: CR2 changes timestamps and removes the field entirely while retaining the same accepted snapshot. This is a real frozen source vector, not a made-up RSI positive.
- Negative: CR3 changes `expected_conformance_observation` as **semantic input data**, not as an RSI expectation declaration. Snapshot acceptance survives; equality does not. A mapping must not turn source acceptance into REJECT merely to obtain a negative RSI decision.

Proposed representation: relation `snapshot_equivalence` in a pinned CR relation profile; case inputs retain baseline/variant semantic objects and external manifests separately. The profile defines endpoint extraction; the independent predictor derives snapshots without reading source `expected` rows. Observation retains snapshot acceptance and equality separately. This passes the non-negotiable mirror test without context_binding, fake proof, fake policy or fake transitions.

### B. RVR and the companion/amendment/verdict suites

Authorities: R1-R7 in merged recompute-kit; R8 in the independent RVR repository. They are related surfaces, not one interchangeable specification.

- Relations/endpoints: companion content-address to verdict core; amendment prior/new commitments and escrow to both parties' named signed digest; effective profile to the profile **inside** the resolver's signed verdict preimage.
- Scope: commitment/binding conformance. Local profile/verdict objects and digest preimages can be well formed while the cross-object relation fails. R1/R2/R4 explicitly exclude signature cryptography from their gates.
- Conditions: recompute commitments; bind this escrow and required parties; resolve the effective commitment; require verdict profile equality and signed-digest equality to its own core. Missing/wrong relation yields source `unresolved`; amendment effective commitment stays A, verdict bound commitment is null. Do not collapse unresolved to boolean false or an authorization decision.
- Claims: permitted **binding transition** and bound verdict, not proof the signatures verify or the resolved business claim is true. R8 independently separates VERIFIED/REFUTED/UNVERIFIABLE from REPRODUCED/DIVERGED/CANNOT_RECOMPUTE and excludes settlement semantics.
- Evidence/context: task escrow, actual profile objects, amendment preimage, required-party declarations and authorization records, verdict core/resolver record. Escrow is mandatory for the amendment suite. R8 v0 forbids uncommitted outcome-relevant external context. No universal durable-state write is exercised; prior/effective commitments are resolution inputs/results.
- Time: R2 motivates an in-force-at-anchor relationship, but its gate has no temporal selector. Do not import PQ timestamp rules into this gate.
- Mirrors: R3 `permitted-distinct-pubkey` preserves digest binding (not verified key authorization); R5 `bound-distinct-verdict` changes verdict payload plus corresponding digest while preserving effective-profile binding. It changes the business outcome, so it is a mirror **only for the binding relation**, not verdict semantic equivalence.
- Negatives: `bare-swap-no-amendment`, `wrong-escrow`, `auth-names-wrong-digest`, and `wrong-profile` retain relevant local shape but break the named edge.

**No-change boundary needing resolution:** R2's prose lists A→A as normal resolution. R3 contains eight vectors, none for A→A. R6 and R7 have no equality/no-change fast path: without amendment they return `transition_status=unresolved` and effective=A, including when proposed=A. It is possible to preserve this amendment result and separately bind an A verdict, but there is no inspected end-to-end no-change vector defining the combined result. Do not invent `permitted` or claim this pass independently established A→A ACCEPT. The proposed model can retain the separate fields without contradiction; final composed expectation for that candidate is withheld pending a pinned composition rule/vector. This is a source/composition question, not grounds to modify RSI or upstream code.

### C. TSEI: preservation authority and historical binding boundaries

Authorities: T1 runtime specification, T2 normalizer tests, T3 transformation tests. T4-T9 concern a separate grounding/serializer methodology lane and must not be relabeled TSEI runtime verdicts.

- Runtime relation: a declared admissible transformation preserves independently recomputed normative and forbidden surfaces under a particular binding/profile; stability surface follows its explicit history policy. Endpoints are source/target evaluations; when normalizers are used, requested normalizer identity must equal the separately supplied authority's returned entry identity.
- Local validity: source/target validity is binding-supplied. A well-shaped authority and locally valid artifacts do not establish that a returned entry matches the requested identity. T2 explicitly tests a branded authority returning the wrong ID: profile validation fails closed before a preservation verdict.
- Relation/claim validity: a normative mismatch produces `violation`; a missing/wrong normalizer authority makes the profile invalid, not a preservation violation. No automatic default authority, inline normalizer, or authority from an identifier is permitted.
- Mirror: T2's multiset reorder preserves multiplicity and normalizes identically; replacing a ref or changing duplicate counts does not. T3 explicitly keeps classification stable when allowed telemetry changes. These are committed source tests, not proof of an independently grounded production run.
- Context/evidence: binding procedures/projections, declared classification policy and any explicitly resolved normalizer authority. T1 requires a history-sensitive policy for this runtime profile. It defines no universal signature primitive and no durable-state write. Ordered cycles retain terminal-edge failure, not an invented epoch counter.
- Grounding lane: T6 includes wrong SAN/endpoint and exact oracle-byte binding tests. Those are authority/evidence relations; self-declared source/account/provenance fields cannot mint VALID_PROVENANCE. Synthetic agreement and production status are explicitly distinct (T4/T8). Unpublished private operands prevent public re-derivation of the historical 12/12 comparison; no claim of production PROVEN is made here.
- Historical serializer relation: T5 §8 requires an immutable, exact historical-binding record, effective boundary, spec digest and vector digest. T4 states activation at a named producer boundary requires a later record whose `effective_commit` names the landed adoption commit. T7 proves an explicit inventory's byte stability, which is **not** retrospective binding authority. T9 ratifies new protocol instances, not every historical serializer binding. No qualifying activation record is established by this inspection; do not invent one.

Thus a locally valid producer artifact under an unestablished historical alias remains unavailable for that claimed binding, even if serializer outputs match. The profile can represent source-specific binding identity and commit boundary without conflating it with PQ anchor time. Full grounding evidence and runtime preservation are different relation profiles.

### D. PQ: in-force authorization at artifact anchor time

Authorities: P1 normative profile; P2-P4 policy vectors; P5 executable enforcer read as source.

- Endpoints: artifact content-address/anchor, classical-to-PQ binding, in-force key, companion signature, authenticated successor/revocation edge where relevant.
- Local validity: a signature can be valid under a retired or non-in-force key. P2/P4 express this using `valid:true` with the wrong key. This flag is an input to the policy lane, not a signature check performed by it.
- Relation: resolve a governing binding at the artifact's anchor time, then admit pre-cutoff anchored history or require a valid companion under that governing key. Rotation and revocation are different. No governing binding means REJECT, even with a signature under a revoked key.
- Claims: eligibility under this consumer's policy and historical binding. The consumer sets the cutoff; `created_at` is not trusted anchor evidence. Preserve exact inclusive/exclusive boundaries: binding starts at its anchor, revocation ends authority at/after its anchor, pre-cutoff is strictly earlier than cutoff.
- Evidence: source binding chain, artifact/anchor evidence, consumer cutoff, and signature/transition verification in the separate deep lane. State/history means authenticated binding history, not mandatory mutable revision/head or a state write.
- Source negative: P2 post-cutoff retired-key companion is locally flagged valid but rejected; successor key admits. P3 retains historical eligibility before revocation and rejects at/after it.
- Mirror availability: P1 explicitly makes PQ companions optional for pre-cutoff anchored history. Adding a detached companion without changing the primary content-address can preserve eligibility. This is normative source support; a dedicated paired frozen mirror vector was not found in P2-P4, so no newly executed/frozen mirror claim is made.
- Boundary: P5 resolves the **supplied** chain and does not authenticate predecessor edges. It must not be used alone to assert B-without-authenticated-edge rejection. P1 requires predecessor authorization and successor possession, but P2's successor anchor time is explicitly intended, not verified on-chain inclusion in this pass. No production rotation claim or real signature proof was independently reproduced.

The model can represent cutoff, historical as-of and edge evidence faithfully. A future full-authentication profile still needs pinned deep-lane evidence and an independently discriminating no-edge case. The policy-only profile must say policy-only.

## 3. Minimum common model, derived from sources

All four need an explicitly selected interpretation and concrete operands; none justifies mandatory Ed25519 proof, revision/head state or one universal authorization policy. CR and RVR both demonstrate that binding/snapshot validity differs from a broader claim. CR and TSEI supply independently specified representation-preservation boundaries; RVR and PQ supply different scoped binding checks.

Keep the envelope limited to:

1. Versioned fixture identity and deterministic case inventory: structurally necessary.
2. Exact relation-profile identity/version/descriptor digest: necessary to prevent semantic reinterpretation, supported by T1 authority identity/version and R8 dependency closure.
3. Explicit opaque relation ID plus full profile-validated case inputs: all four; IDs select, never explain semantics.
4. Explicit mutation/case roles validated under the profile and evidence of discriminatory/mirror behavior: conformance structure, not an expected-answer declaration.

Endpoint roles, evidence requirements, request grammar, scope, allowable claims/prohibited promotions, and any temporal/state rules live in the **profile**. Concrete values live in the **instance**. Endpoint locations are specified once in the profile's input schema/role map; do not duplicate the same values in a universal `endpoints` array and a second request object.

Do not include universal `context_slots`, `temporal_scope`, `state_constraints`, `proof` or `policy` members. These are profile-required slots when sourced. A source-specific concept remains legitimate in one profile; it does not become a generic field on that basis. Commit-adoption order and anchored time are both scoped boundaries, not evidence for one interchangeable epoch algebra.

## 4. Architecture alternatives

| Criterion | A: extend current schema with optional fields | B: minimal envelope + separate Relation Profile | C: envelope + relation instance + separate request/evidence object |
|---|---|---|---|
| Compatibility | Can retain old bytes with versioning, but optionalization easily weakens v0 validation | Frozen legacy path and explicit compatibility binding | Possible with an explicit legacy view |
| Semantic clarity | Mixed enums and domain objects invite fake/default values; optional fields alone do not close unknown shapes | Exact profile grammar explains all required/absent concepts | Clear separation if needed, but duplicates role/value binding surfaces |
| Source fidelity | Poor unless effectively reinventing profiles in schema conditionals | Preserves source grammar and native observations | Also good with exact cross-object identity checks |
| Extension safety | Large union/conditional schema risks second semantic path | Static registration; pinned descriptor; strict profile validation; existing expectation admission | Same controls plus extra cross-object binding and completeness checks |
| Complexity | Initially small, grows with every domain | One new envelope/descriptor and compatibility composition | Higher object-resolution and pinning complexity |
| Core leakage | High risk of domain conditionals | No core domain branches needed | No branches required, but more generic plumbing |
| Synthetic effects | High regression risk if requirements relaxed in place | No fixture/predictor rewrite | No rewrite required, but needless legacy assembly |
| 150-test baseline | Could remain if old schema frozen; cannot assume after weakening it | Semantically unchanged by design; later rerun required | Semantically unchanged possible; later rerun required |

B wins because the current runtime already permits profile validators, opaque request plans and exact observation comparison. C is not ruled out forever, but independent relation/request object addressing is not required by these sources and introduces additional substitution opportunities. A's convenience does not justify a semantic union tied to domain names.

## 5. Concept ownership

| Concept | Primary owner | Concrete binding / observation responsibility |
|---|---|---|
| Relation ID | Relation Profile | Fixture names an exact registered relation; generic core treats it as opaque |
| Endpoint roles | Relation Profile | Fixture supplies values; adapter and predictor independently interpret the same roles |
| Local validity | Relation Profile | Adapter checks actual components; Expectation Profile independently predicts; fixture declaration grants nothing |
| Relation truth | Relation Profile | Defines meaning and unavailable states; predictor derives expected, adapter derives actual |
| Expected result | Expectation Profile | Pinned set admitted atomically after independent recomputation |
| Adapter ID | RBCF generic core / extension registration | Selects trusted implementation, not authority |
| Operation/request type | Relation Profile | Fixture provides profile-valid request; never a core domain dispatch |
| Proof | Relation Profile | Concrete evidence in instance when required; no universal signature shape |
| Policy | Relation Profile | Source-authorized concrete inputs in instance; not author-selected weakening |
| State | Relation Profile | Captured protected state in instance only when source requires it |
| Authority | Relation Profile | Exact trusted authority/evidence binding; provenance metadata alone cannot grant it |
| Provenance | Source provenance metadata | If source makes it outcome-relevant, its exact bytes also become profile-bound evidence |
| Context | Relation Profile | Required/optional/forbidden slots explicitly stated, no ambient context |
| Epoch | Relation Profile | Instance supplies sourced boundary/evidence, if defined |
| As-of | Relation Profile | Source-specific anchor/commit semantics, not wall clock or filename |
| Evidence requirements | Relation Profile | Required slots and validation phases; instance supplies exact data |
| Prohibited promotions | Relation Profile | Explicit source-scoped claim limits, observed by adapter and predicted independently |
| Source artifact digest | Source provenance metadata | Exact fixture/evidence/profile closure when outcome-relevant; digest is not semantic authority |

The generic core owns discovery, identity uniqueness, trusted resolution, deterministic transport, atomic expectation admission, exact comparison and the four conformance states. It does not decide what a signature, snapshot, effective profile, authority or historical binding means.

## 6. Exact future delta proposed, not performed

Create a **new** schema, candidate `schema/profiled-relation-fixture.v0.schema.json`; do not change either existing fixture schema. Closed top-level required members:

- `schema`, constant `profiled-relation-fixture.v0`;
- `id`, the existing restricted source-ID syntax, mapped to canonical identity through existing corpus registration;
- `relation_profile`, a closed record of `profile_id`, `version`, `descriptor_sha256`;
- `relation_id`, a nonempty restricted opaque identifier;
- `mutation_model`, an opaque profile-validated identifier;
- `cases`, nonempty with unique case names and each containing exactly `name` and `inputs`. The profile defines input schema and case coverage obligations. No required `local_validity_expected`, proof, policy, state or fixed operation enum.

The profile descriptor separately pins its normative source closure, input/output constraints and relation IDs, endpoint roles, required/optional/forbidden slots, component predicates, relation interpretation, claim boundaries and case/mutation obligations. Trusted code is statically associated, never loaded from descriptor fields. Profile descriptor bytes are hashed outside themselves; all outcome-relevant dependencies are pinned transitively. Adapter identity is separate from relation meaning and expectation implementation identity.

No change is needed to the old `observation.v0` or the four conformance states. New profiles supply **separate profile-specific observation constraints** through existing `validate_prediction`. `observation` must preserve component/relation/claim distinctions and source-native categorical/unavailable results; do not translate `accepted_snapshot`, `unresolved` or `history_sensitive` into synthetic authorization labels. The current expectation envelope can stay unchanged: its generic `prediction` object admits profile constraints, and fixture-set hashing binds the new fixture's profile descriptor pin transitively. Legacy expectation rows retain their exact shape.

No corpus-schema field is necessary for new fixtures: their explicit relation-profile binding is in their bytes. Legacy compatibility uses a statically registered `(corpus identity, expectation profile, legacy schema) -> synthetic relation profile` binding, checked before execution. No inference from ID or path. New trusted composition must select the correct corpus validator; `extensions/defaults.py` currently supplies the registered synthetic wrapper to all default corpora. Changing **composition** and adding registration is necessary later; a domain branch in `runner/execution.py` is not.

Preserve `rsi-json-ascii.v0` transport. Non-ASCII, floating-point or exact source byte inputs can use a profile-defined lossless ASCII byte transport (for example hex) with explicit source parsing/canonicalization. This is not a cryptographic proof field. A profile must verify that transport reproduces exact source bytes and is covered by the expectation fixture-set digest. Full host-object descriptor behavior, such as getters/proxies, is not automatically expressible as JSON; mark that coverage unsupported unless an independently specified construction procedure exists.

## 7. Compatibility and approval decision

Legacy bytes **can** remain unchanged. Explicit compatibility registration binds the unchanged six fixtures to a synthetic relation profile. Keep the original `rsi/oracle.py`, synthetic validator/plan, expectation artifacts, old observation schema, all 36 complete observations, and all 16 mapped mutation behaviors. This is a design argument, not a rerun proving a future implementation. No relation-true field is backfilled from ACCEPT labels into historical evidence. RSI-CORE's finite normative rules and its unimplemented epoch-continuity candidate remain exactly as written.

Proof/policy/state conclusion: CR snapshot requires none of these. TSEI generic preservation requires its declared history policy and procedures, but not signature proof or durable writes; its separate grounding lane requires provider proof and policy. RVR binding conformance requires commitment evidence and authorization-binding records, not crypto verification or durable writes; broader RVR profile policy is scoped. PQ full authorization needs signature/anchor/transition evidence and consumer cutoff policy; history is relevant, but mutable revision/head state is not universal. Make such slots required by their own profiles, not optional loopholes in legacy v0.

The CR mirror maps faithfully. RVR/TSEI/PQ structures are representable without special-case core logic, but **full source-backed validation is not established**: RVR no-change composition is unresolved; TSEI historical activation is not established; PQ policy inputs cannot stand in for authenticated-chain/deep-lane evidence. These candidates must not receive invented admitted expectations.

Ready to review/approve the **bounded Option B architecture direction**: yes. Ready for unconditional implementation plus all four domain claims: **no**. Before implementation approval, settle the exact descriptor dependency closure and observation contracts, preserve lossless transport, and explicitly exclude or resolve the RVR no-change composition and unsupported source lanes. Do not repair upstream sources or change expectations in this task. The proposed design does not require a contradiction, but any attempt to assert the unresolved composed results must stop.

Remaining risks: trusted profile and predictor code can share a conceptual bug; function inequality does not prove independence; source schemas may omit relevant relationships; raw-source integrity does not establish historical authority; unavailable evidence must remain distinct from false relations; canonicalization must not silently erase source distinctions. These are explicit review boundaries, not reasons to manufacture universal proof/policy/state.

No code/schema implementation, external modification, commit, push, PR, tag or release was performed. Only this report, the source map and the candidate design document are new artifacts.


## Implementation disposition

This document preserves the earlier design review. The authorized generic implementation is specified in `spec/relation-profile-contract-v0.md` and recorded in `research/relation-profile-implementation-v0.md`. Option B was retained. The evidence-closure review remains YELLOW (bounded wording/scope), not upgraded to external conformance. Its exact pins are in `research/relation-profile-evidence-closure-v0.json`.

The implemented envelope uses source `id` for compatibility, exact profile ID/version and optional descriptor pin; the earlier mandatory-descriptor proposal is not implemented. Profile-specific structured states preserve unresolved/effective-state distinctions. The implementation does not establish authenticated transition continuity or remove source transport/evidence limitations. No external adapter was added.
