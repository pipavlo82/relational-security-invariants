# Relation Profile Contract v0.1 — candidate design

**DESIGN ONLY. Not final normative text, not implemented, and not an amendment to RSI-CORE v0.**

This draft recommends Option B from [the source comparison](../research/relation-profile-comparison-v0.md). Source references CR1-CR3, R1-R8, T1-T9 and P1-P5 resolve to the exact commits/files/digests in [the source map](../research/relation-profile-source-map-v0.json). It is a proposed architecture boundary, not a universal calculus or cross-domain validation result.

> Extensibility must not create a second path for semantics.
>
> registration != authority
>
> component validity != relation validity != claim validity
>
> fixture author declaration != independently established expected relation != implementation-under-test result
>
> Expected outcomes are evidence that must themselves be validated; they are not authoritative merely because they are pinned.

## 1. Interpretation boundary

Candidate requirement: every new fixture MUST explicitly bind one immutable relation profile and one relation declared by that profile. A Relation Profile defines the interpretation of source-defined inputs and observations. It MUST NOT define an arbitrary executable language or allow fixtures to install their own semantics.

A trusted registration associates a unique `profile_id`, explicit version and exact descriptor SHA-256 with statically reviewed implementations/validators. Duplicate identities with ambiguous versions or descriptors MUST fail before any case runs. Resolution MUST use exact identity/version/digest, not latest-version fallback. The descriptor MUST identify its normative source and input/output constraint closure with exact dependency identities. Any missing or mismatching semantic dependency MUST prevent use of the profile. Matching bytes MUST be the bytes actually used; re-reading a mutable locator is not an identity check.

The descriptor MUST NOT hash itself. Its digest is pinned by trusted registration and the new fixture. It MUST NOT embed import paths, executable expressions, network lookups or package installation instructions. Identifying a spec or trusted implementation is not evidence it is semantically correct. Static review and discriminating source-backed tests remain necessary.

An adapter's implementation identity and an expectation predictor's implementation identity MUST remain separate from the relation's meaning. Changing an implementation under test MUST NOT redefine the expected relation.

## 2. Explicit relation and source fidelity

Each profile MUST declare:

- its relation IDs, normative source scope and any interpretation limits;
- endpoint roles and their precise locations/types in case inputs;
- required, optional and forbidden input slots, including any request grammar;
- how relevant components are independently validated;
- how relation results and unavailable/invalid states are interpreted;
- which claims/promotions depend on the relation, and which remain outside its scope;
- output constraints that preserve these distinctions;
- source-justified substitution, mirror-positive and mutation coverage obligations.

Normative sources MUST remain authoritative for source meaning. A mapping MUST NOT replace a source relation with a similarly named RSI synthetic predicate, invent proof/policy/state fields, or treat source acceptance as a broader authorization. A source outcome such as `accepted_snapshot`, `bound`, `unresolved`, `stable` or `ADMIT` MUST retain its stated scope. A profile MUST NOT infer relation truth from that label alone.

Source-declared semantics, implementation behavior, frozen vector expectation, independently recomputed result and deployment claims MUST be distinguished in provenance. Where normative prose and executable behavior leave a composed result unresolved, that result MUST NOT receive an invented oracle row. Resolve the authority boundary or report the candidate unsupported.

## 3. Identifiers and roles

The core runtime MUST NOT infer semantics from fixture ID, namespace, relation ID, adapter ID, expectation profile ID, mutation ID, file path or directory name. Identifiers select registered objects only. Syntactic validation and exact identity equality are permitted and do not confer semantic authority.

An endpoint role MUST have a stable meaning within an immutable relation-profile version. Renaming, swapping or changing its interpretation requires a new reviewed profile identity/version and expectation-set binding. Matching the same untyped value in two slots MUST NOT erase their roles. No implicit default endpoint or ambient authority may fill a missing required slot.

Endpoint values SHOULD be represented once. The input schema/role mapping determines how profile implementations find them; duplicate independently mutable endpoint/request copies are not part of the minimum contract.

## 4. Proposed fixture envelope

This is a future new schema, not a modification of `relation-binding-fixture.v0` or `registered-fixture.v0`:

```text
profiled-relation-fixture.v0
  schema = "profiled-relation-fixture.v0"
  id: existing restricted source identity
  relation_profile:
    profile_id: opaque restricted identifier
    version: explicit stable version
    descriptor_sha256: lowercase SHA-256 of exact descriptor bytes
  relation_id: opaque identifier declared by the profile
  mutation_model: opaque class validated by the profile
  cases:
    - name: unique opaque case identity
      inputs: closed, profile-validated concrete inputs
```

The envelope and relation-profile reference MUST reject unknown members. Case inventory MUST be nonempty, deterministic and duplicate-free. Registered canonical fixture identity remains supplied by the existing Extension Contract. Coverage roles are explicit profile obligations and MUST NOT be inferred from the spelling of `name`.

There is no universal signature, proof, policy, state, epoch, as-of, evidence-list grammar or operation enum. Required concepts MUST become required slots in the selected profile, not optional ways to bypass its protections. Missing is distinct from null, an empty value, false and unavailable wherever source semantics distinguish them. Unknown inputs MUST NOT be silently discarded.

Fixture transport remains the current canonical ASCII/integer JSON contract. Source bytes outside that domain MUST be transported losslessly under a profile-defined encoding and decoded using the source's pinned rules. Transport canonicalization MUST NOT be substituted for source semantic canonicalization. Source byte hashes and transport/fixture byte hashes MUST be labeled separately. Non-JSON host-object behavior is not covered merely because a JSON example exists.

## 5. Components, relations and claims

The profile's evaluation contract MUST distinguish:

1. Which local component checks ran, their outcomes and limitations.
2. Which protected relation was evaluated, its endpoints and result.
3. Which source-scoped claims/promotions that result permits or prohibits.

These are obligations on observable profile output and validation, not a requirement to fabricate three universal boolean fields. A source-native categorical outcome MUST be preserved where boolean truth would lose information. A relation that was not evaluated MUST NOT be recorded as false or true by default.

`local_validity` in the existing execution report is an admitted reference member. It MUST NOT be represented as actual component-validation evidence by itself. New adapters' observations MUST include sufficient actual component and relation evidence for their selected output contract, independent of this reference value.

A relation may be necessary but insufficient for a claim. For example, a companion's commitment does not prove its signature verifies (R1), and snapshot equality does not authorize a producer (CR1). The profile MUST define all claimed prerequisites or explicitly limit the claim. The fixture may request a claim only within that reviewed profile contract; it cannot enlarge the allowed promotion classes by declaration.

## 6. Substitution and mirror preservation

For a pure relation-substitution negative, the profile MUST identify which endpoint or edge changed and which local checks still hold. A syntax/import/setup failure MUST NOT count as semantic discrimination. A missing relationship may be a valid negative when the source permits locally valid components without that edge; it is not permission to skip component validation.

Every claimed mirror-positive MUST have a source-backed equivalence rule. Changed representations MUST preserve the selected relation and only the claims justified by it. A mirror MUST NOT be established merely because two expected labels are equal. Conversely, changed bytes MUST NOT cause rejection if the source's protected relation is unchanged.

For CR's motivating case, external `audit_timestamp` may change or disappear while the accepted semantic snapshot remains identical (CR1/CR2). `audit_timestamp` inside semantic input is malformed and cannot be silently stripped. Both inputs in CR3 are accepted snapshots while their semantic equivalence is false. This contract MUST express all three facts without signature, authorization policy or state-transition surrogates.

For RVR binding mirrors, changing verdict business outcome while correctly rebinding its preimage can preserve profile binding (R4/R5); it does not preserve the verdict's business meaning. A profile MUST name that narrower protected relation.

## 7. Temporal, state and policy slots

A profile using time or history MUST specify its authenticated reference point, source of ordering, boundary inclusivity, missing-evidence behavior and treatment of historical artifacts. Generic execution MUST NOT consult wall-clock time or choose a current binding implicitly.

PQ anchor-time cutoff and revocation follow P1-P5; a retired key's historically governed artifact can remain eligible while a post-transition artifact under that key fails. Binding-chain authorization and signature validity MUST be established by their actual evidence lane, or explicitly remain assumptions of a policy-only profile. An input `valid:true` is not independently verified cryptography.

TSEI historical serializer resolution requires exact binding identity and a qualifying immutable effective/adoption record (T4/T5). A byte-compatible producer or ratification for new instances MUST NOT silently backfill that authority. A commit boundary MUST NOT be converted into a PQ timestamp or generic epoch rule.

State constraints belong only to profiles with protected state. Policy inputs must be source-authorized, pinned or otherwise independently bound as the source requires. The absence of universal proof/policy/state fields MUST NOT weaken the unchanged synthetic profile's mandatory fields.

## 8. Expectation independence and atomic admission

The existing Expectation Contract remains mandatory. Fixture declaration and relation-profile descriptor determine how to interpret inputs; neither establishes expected truth merely by existing or matching a digest.

An independently reviewed expectation predictor MUST recompute expected observations from the same source-defined inputs. It MUST NOT call the adapter under test, read expectation rows as its oracle, or obtain expected truth from fixture names/labels. A relation profile MAY specify evaluator obligations; it MUST NOT require predictor and adapter to share one decision function. Shared low-level primitives require explicit review of common-mode failure risks.

Before any profile expectation is used, the current pinned artifact identity, exact fixture-set binding, complete row inventory and prediction equality MUST pass for every registered fixture. One bad row prevents admission of that entire expectation profile. No partial fallback or weaker alternate path is permitted.

For new fixtures, the relation-profile descriptor digest is in fixture bytes; fixture-set binding therefore binds that selected semantic closure. Trusted registration MUST check the exact descriptor and dependencies before prediction/execution. Legacy compatibility must bind its frozen relation profile through trusted static registration; it does not silently rewrite historical expectation artifacts.

The existing expectation artifact schema need not change: `prediction` remains constrained by its registered validator. New profile-specific observation schemas MUST retain source-native states and evidence; old synthetic `observation.v0` remains unchanged.

## 9. Runtime, unavailable cases and mutations

Proposed flow:

```text
registered corpus and fixture bytes
  -> envelope validation and exact relation-profile binding
  -> profile-specific input validation
  -> independent expectation profile resolution and atomic admission
  -> registered adapter execution
  -> profile-specific observation validation
  -> existing exact comparator
  -> PASS / FAIL / INVALID_FIXTURE / UNSUPPORTED
```

Unknown/unavailable semantic profile is a profile-availability diagnostic mapped to UNSUPPORTED, not evidence of malformed domain data. A structurally invalid fixture remains INVALID_FIXTURE. A source-defined unresolved outcome may itself be a completed, correctly reproduced observation and yield conformance PASS; that does not grant its refused claim. Infrastructure inability to evaluate is UNSUPPORTED with its diagnostic, not a synthetic source outcome. Preserve existing Extension Contract error conventions.

Trusted composition selects validators and registered implementations. It MUST NOT introduce relation/domain conditionals into generic execution or the comparator. No new top-level result vocabulary is proposed.

Future mutations use the existing shared registry. Substitution guards, mirror preservation and semantic-closure binding require mapped tests whose decision points actually execute. Setup/import/parse/teardown failures are VACUOUS, not KILLED; unmapped targets remain NOT_APPLIED; collateral failures remain separately recorded. This draft adds no mutations and changes none of the 16 existing outcomes.

## 10. Legacy compatibility

Register one explicit legacy synthetic relation profile covering the six existing relations. Keep its fixtures, schemas, request/observation semantics, independent predictor, expectation rows and mutation mappings byte-identical. Compatibility registration binds corpus identity, legacy schema and expectation-profile identity to that frozen profile; no prefix dispatch.

The new contract MUST NOT reinterpret legacy ACCEPT as an independently reported relation-true field, manufacture historical component observations, or claim implementation of RSI-CORE-7. A future implementation MUST compare all 36 complete legacy observations and all 16 mutation outcomes and rerun the 150 baseline tests, including optimized Python, before making compatibility claims. No migration is performed in this design pass.

## 11. Review gates and non-goals

Before implementation approval, review exact descriptor closure, profile-specific observation requirements and byte-transport rules. Preserve the identified source limitations: RVR's A-to-A composed result needs a pinned rule/vector; TSEI historical activation remains unestablished in the inspected source; PQ policy-only evidence does not prove an authenticated successor chain. Do not generate expectations for those stronger claims until evidence supports them.

Reject a proposed profile if it changes source semantics, permits self-authorized expectations, infers meaning from identifiers, silently modifies legacy outcomes, or needs domain logic in generic execution. If a source relation cannot be represented faithfully, report the unsupported case rather than adapting the source to RSI.

Non-goals: arbitrary runtime plugins, network-loaded semantics, dynamic package installation, an executable manifest language, universal proof/policy/state, automatic relation discovery, source-repository changes, new external adapters, retrospective authority, rewriting RSI-CORE, new result taxonomy, production certification, or a mathematical novelty claim.


## Implementation disposition

This document preserves the earlier design review. The authorized generic implementation is specified in `spec/relation-profile-contract-v0.md` and recorded in `research/relation-profile-implementation-v0.md`. Option B was retained. The evidence-closure review remains YELLOW (bounded wording/scope), not upgraded to external conformance. Its exact pins are in `research/relation-profile-evidence-closure-v0.json`.

The implemented envelope uses source `id` for compatibility, exact profile ID/version and optional descriptor pin; the earlier mandatory-descriptor proposal is not implemented. Profile-specific structured states preserve unresolved/effective-state distinctions. The implementation does not establish authenticated transition continuity or remove source transport/evidence limitations. No external adapter was added.
