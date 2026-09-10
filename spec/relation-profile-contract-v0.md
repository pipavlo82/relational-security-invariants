# Relation Profile Contract v0.1

> Relation Profiles define relation semantics; they do not authorize expected outcomes.
>
> Source-defined semantics must not be projected into a legacy synthetic relation merely to satisfy the fixture schema.

## Purpose and boundaries

This additive contract implements Option B: a separate trusted relation profile and a minimal fixture envelope coexist with the frozen RBCF v0 path. It does not amend RSI-CORE. Component validity != relation validity != claim validity. A locally valid component with a broken protected relation MUST NOT inherit the dependent claim. Profiles MUST specify the scope of that claim; registration != authority.

This is an architecture refinement driven by source evidence, not a new security theory or a claim of cross-domain validation. No external-domain implementation or corpus is included.

## Fixture envelope and identity

`schema/profiled-relation-fixture.v0.schema.json` requires only:

```json
{"schema":"profiled-relation-fixture.v0","id":"example","relation_profile_id":"example.profile","relation_profile_version":"0","relation_id":"example.relation","cases":[{"case_id":"control","inputs":{}}]}
```

`id` is retained as the source identity field to reuse the existing Expectation Contract byte-binding interface without changing its implementation. The corpus registration supplies the globally unique canonical `namespace:local_id`. Source ID and canonical ID are distinct, explicitly bound identities. A fixture binds one relation and exact profile version; cases carry concrete inputs. Additional envelope/case fields are forbidden. Case IDs MUST be unique in their fixture. Identifiers use 1-128 restricted ASCII letters, digits, dot, underscore, colon or hyphen, beginning with a letter/digit. The runtime enforces the entire string, including rejecting a trailing newline.

Stored JSON MUST use the existing `rsi-json-ascii.v0` serializer: ASCII, bounded integers, no floating values or duplicate keys, deterministic ordering and LF. This transport restriction is not a source serializer or a universal data model. Future sources requiring another transport need a separately reviewed transport change; no implicit conversion is permitted.

The envelope does NOT require proof, policy, state, signature, authority, epoch, transition or provenance. Profile inputs may require any of these only when justified by that profile's semantics.

The core MUST NOT infer semantics from fixture ID, case ID, namespace, adapter ID, profile ID, relation ID, mutation ID, file path or directory name. Equality lookup and identity syntax validation select objects; they never establish truth or authorization.

## Static registration and exact binding

`RelationProfile(profile_id, version, relations, descriptor_sha256=None)` contains an immutable tuple of `Relation` declarations. Registration rejects duplicate `(profile_id, version)`, duplicate relation IDs, invalid names, mutable slot declarations, overlapping slots or non-callable contracts. Different exact versions may coexist. Registry order MUST have no semantic effect. There is no latest-version fallback.

A fixture MAY pin `relation_profile_sha256`; if present it MUST exactly match the descriptor pin in trusted registration. This optional pin is a descriptor identity assertion, not an executable hash or independently verified source closure. The registrant remains responsible for reviewing and verifying the descriptor bytes and dependency closure before registering code. No descriptor is loaded or executed from a fixture. This optional model follows the implementation authorization; it supersedes the earlier draft's mandatory descriptor proposal.

Unknown profile/version, unsupported relation, or mismatched optional descriptor is an availability failure: UNSUPPORTED, before expectation admission or adapter execution.

## Slots and interpretation

Each `Relation` supplies:

- `relation_id`;
- immutable `required_slots` and `optional_slots`;
- deterministic `validate_inputs(inputs)`;
- `evaluate(inputs, context)` for observed interpretation where appropriate;
- deterministic `validate_outputs(result)` defining the permitted output shape and vocabulary.

Every required top-level slot MUST exist; every undeclared slot MUST be rejected. Optional slots may be absent. The profile owns nested shape, endpoint roles, component checks, request grammar, dependent claims, evidence requirements and temporal meaning. Input/output validators must raise on invalid data. Detached copies and canonical serialization detect direct input mutation. These checks do not sandbox Python or prove purity of arbitrary trusted callables; code review remains required.

Endpoint roles MUST remain stable across cases. A substitution negative MUST preserve component validity where possible and change the protected relation, not break setup. A mirror-positive MUST preserve the protected semantic result despite changed representation or non-protected metadata. Neither byte equality nor byte difference establishes relation truth.

## Structured relation result

The internal result is exactly:

```json
{"relation_id":"example.relation","relation_state":"profile-defined-state","outputs":{}}
```

The relation ID MUST match the selected relation. The state is an opaque restricted string, never a universal boolean interpretation. `outputs` is profile-validated structured JSON and has no universal domain fields; the complete serialized result is limited to 1 MiB. A profile MUST bound its own output schema and distinguish the claims it exposes. Effective binding, resolution state, component validity and claim admissibility may be separate profile-defined outputs. Generic code neither promotes nor collapses them.

An adapter may use the registered interpretation helper, or independently compute the implementation-under-test result. An expectation predictor MUST NOT call that actual evaluator to establish its oracle. An interpretation may delegate legacy execution rather than fabricate a relation truth.

## Admission and execution

`runner.relation_runtime.execute` coordinates:

1. Explicit corpus discovery using the unchanged Extension Contract.
2. Envelope validation and exact relation-profile resolution.
3. Profile-specific input validation for every case.
4. Independent Expectation Profile resolution and atomic expectation-set admission.
5. Exact binding of planned check identity to relation profile/version, relation and case inputs.
6. Registered adapter execution.
7. Profile output validation and unchanged generic comparison against admitted expectations.

Expected rows are independently predicted before the pinned artifact is read. Fixture bytes and set identity remain bound by the unchanged Expectation Contract. A relation profile MUST NOT read the expectation artifact or return an expected result. Predictor, adapter and fixture declaration remain separate. Direct predictor/evaluator identity is rejected; indirect wrappers, closures, global/file access and logical independence still require trusted-source review. Registration does not provide arbitrary-code isolation.

One relation dependency failure blocks that entire expectation profile from admission. Siblings are visible as UNSUPPORTED; no partial set is admitted. Plans cannot substitute another case's inputs or alter the profile binding. Profile-specific validation is applied to expected and actual observations without recomputing expected truth from the adapter.

## Status and failure boundaries

Top-level taxonomy remains PASS / FAIL / INVALID_FIXTURE / UNSUPPORTED.

- INVALID_FIXTURE: malformed envelope, malformed profile-bound input, missing/undeclared slot or structural validation failure.
- UNSUPPORTED: unavailable profile/version/relation/adapter/expectation implementation or unadmitted expectation set. Registered validator setup exceptions are fail-closed diagnostics and do not certify malformed source semantics.
- PASS: execution matched an independently admitted expectation.
- FAIL: execution completed with a valid-shaped observation that differs from that expectation.

The existing extension path retains its internal EXECUTION_ERROR diagnostic and reports crashed adapters as UNSUPPORTED. Such a crash is not a semantic mismatch or mutation kill. Profile-defined `unresolved`, `stale`, `bound` or any similar term is not a new top-level state and implies none of these statuses on its own.

## Temporal and source evidence boundaries

Temporal slots and historical evaluation belong to profiles. Current authority != authority governing an artifact at a proven anchor/as-of. Signing before a cutoff alone MUST NOT imply historical eligibility. Generic architecture tests use a supplied anchor-evidence flag solely to exercise this separation, not to prove a real anchor.

The pinned evidence review in `research/relation-profile-evidence-closure-v0.json` remains YELLOW for both inspected families:

- RVR: A with no amendment retains effective profile A; the amendment reference may remain unresolved. This implies neither ACCEPT nor substantive divergence resolution. Transition binding and verdict binding are distinct; substantive resolution remains separate. The generic rich-state test preserves effective A alongside unresolved resolution without labeling the relation successful.
- PQ: policy/cutoff vectors do not prove authenticated transition continuity. Transition artifacts may contain predecessor references/signatures, but the inspected offline `deep_recompute.py` defers signature verification. Its ML-DSA labels do not match the inspected SLH-DSA artifact. Full authenticated-chain validation remains unsupported. Historical validity depends on the governing binding at a proven anchor/as-of; an earlier signing time alone is insufficient.

These statements are bounded to the exact evidence pins in that review, not assertions about all implementations or current upstream behavior.

## Compatibility and extension composition

Legacy fixture bytes, schemas, expectation artifact and predictor remain untouched. `profiles/legacy_relation.py` registers `core.synthetic.v0`, version `0`, with its six relation classes and an explicit corpus binding. Its legacy fixture slot retains the old five operations and proof/policy/state requirements for that profile only. The compatibility interpretation reports delegation; existing actual adapters and independent predictions remain unchanged. Old and relation-aware execution produce exactly the same 36 rows.

No corpus manifest schema change is needed: the existing pinned corpus entry binds source fixture bytes, canonical identity, adapter slots and expectation profile. The new fixture itself binds its exact relation profile. A corpus must register the new envelope validator and enter through the relation-aware coordinator. The historical extension CLI remains the legacy compatibility entrypoint; it is not a relation-contract bypass approved for new profiled corpora.

Trusted composition lives in `extensions/relations.py`. Future domains add their profile/adapter/predictor implementation, explicit registration, pinned fixture corpus and mapped mutations. Generic runner/comparator and taxonomy need no domain branches.

## Mutation evidence and non-goals

`tools/prove_relations_can_fail.py` explicitly registers RP-M1 through RP-M7 through the unchanged shared MutationRegistry. Mappings cover resolution, exact version, identifier opacity, rich-state preservation, mirror-positive, as-of binding and expectation admission. RP-M3 is a mapped static architecture check. Source mutants execute in isolated copies. Setup/import errors are VACUOUS; unexecuted mappings are NOT_APPLIED; valid mapped assertions distinguish KILLED from SURVIVED. Collateral failures are recorded separately.

Non-goals: external adapters or corpora, arbitrary runtime plugins, reflection-based imports, network-loaded semantics, dynamic package installation, universal proof/policy/state vocabulary, automatic source authority, universal unresolved semantics, authenticated-chain implementation, and changes to RSI protected-relation rules.
