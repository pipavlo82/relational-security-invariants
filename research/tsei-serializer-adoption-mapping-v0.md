# TSEI serializer/adoption mapping v0

Scope: Phase 2C.1 only. This is a source-backed serializer-binding and adoption-policy conformance lane, not provenance-authority verification. The prior Phase 2C STOP reports remain unchanged as historical evidence.

RSI base: `366974070b0684af8b5c07dcf4cba0cde90eb8e5`, private `main`.
Canonical source heads were reverified live before implementation:
`pipavlo82/crystal-receipt@45b46bf7df3a60b32583291f577a36bf19d22f00` and
`trustless-ai/recompute-kit@15f7f59ac47b3358492bd5741143c418b5d657f5`.
No external repository was modified. Only TSEI producer and serializer registry material was inspected; existing RSI Crystal and RVR implementations remain frozen.

## Source coordinates and byte pins

All paths below are pinned GitHub content blobs. Vendored bytes are exact; markdown and TypeScript are not passed through RSI fixture transport. These public artifacts contain no private authority operands.

| Repository | Exact commit | Source path | SHA-256 | Evidence class |
|---|---|---|---|---|
| `trustless-ai/recompute-kit` | `15f7f59ac47b3358492bd5741143c418b5d657f5` | `conformance/serializer-bindings/README.md` | `4b0e9b4b80fdd08c5eccde02f1d7986072ab812a59076bb5dfb2db9154f69ccc` | registry contract documentation |
| `trustless-ai/recompute-kit` | `15f7f59ac47b3358492bd5741143c418b5d657f5` | `conformance/serializer-bindings/records/tsei.frozen-artifact.json` | `f45e3e99f3e31dc4884d92e8b1622b6c8497ecf295424442698db9d9aeb14ec6` | immutable registry/binding record |
| `trustless-ai/recompute-kit` | `15f7f59ac47b3358492bd5741143c418b5d657f5` | `conformance/serializer-bindings/validate_binding_record.py` | `6d079d05548534985db46c79faacbdb66736da8bb59b8f6a90abf34c13c100c0` | reference implementation |
| `trustless-ai/recompute-kit` | `15f7f59ac47b3358492bd5741143c418b5d657f5` | `conformance/serializer-bindings/binding-record.schema.json` | `87ea63d6cc98dfea8f9f88fe27b27cfd87f9cf4b0039e304ccd0e97d32644d9e` | normative record shape |
| `trustless-ai/recompute-kit` | `15f7f59ac47b3358492bd5741143c418b5d657f5` | `conformance/serializer-bindings/binding-record.vectors.json` | `7beaabc7166816ae984eb1c5fffc55dc457ca4f86743f1f14e8795841626485e` | synthetic shape vectors, not authority evidence |
| `pipavlo82/crystal-receipt` | `45b46bf7df3a60b32583291f577a36bf19d22f00` | `conformance/tsei-invariant-discrimination-v0/README.md` | `b2dc0105767b26d2f53dcf4b6ef4c3ba37f4b5eb7798ce8fb5a370f2fa91d549` | producer adoption documentation |
| `pipavlo82/crystal-receipt` | `45b46bf7df3a60b32583291f577a36bf19d22f00` | `conformance/tsei-invariant-discrimination-v0/encode-json-utf8-lf-v0.ts` | `a82587be42aa3d2e382f02e3ae633efe67b94b5831cb043131b3bc174e4fe3f9` | adopted producer implementation |
| `pipavlo82/crystal-receipt` | `45b46bf7df3a60b32583291f577a36bf19d22f00` | `tests/receiptos/tsei-encode-json-utf8-lf-v0.test.ts` | `104f6da26d763bc419cefc813efc39134b04877cfa4e9f270fc6558bad727ab0` | upstream qualification/historical preservation tests |
| `trustless-ai/recompute-kit` | `f1d75a530761c983e8b6900f036935ac7758538c` | `conformance/encode-json-utf8-lf-v0/encode-json-utf8-lf-v0.vectors.json` | `8d53ab1d3dfb2de1ba9db23ed06d6864b08b516451938a4b1f6db6bcdcf1950f` | normative qualification vectors |
| `trustless-ai/recompute-kit` | `f1d75a530761c983e8b6900f036935ac7758538c` | `conformance/encode-json-utf8-lf-v0/encode-json-utf8-lf-v0.spec.md` | `22207f8c4047044414da98b5497a2c9683aea14a7a498fc1819a9094c920a1f9` | normative serializer contract |
| `pipavlo82/crystal-receipt` | `45b46bf7df3a60b32583291f577a36bf19d22f00` | `conformance/tsei-invariant-discrimination-v0/fixtures/authority-object-b-valid-v1.json` | `0ef9ee8f579b091d7287f05955661b04c386726e1b38c2009fa46005a09e0107` | historical synthetic preflight example, not real authority oracle |
| `pipavlo82/crystal-receipt` | `45b46bf7df3a60b32583291f577a36bf19d22f00` | `conformance/tsei-invariant-discrimination-v0/public-receipts/tsei-ia-real-v2-20260824-02.production-grounding.json` | `09349e8257da2b94227f7af7f8e4dcdcca9e715dc460e1f419e53a14a22e5a07` | reported public receipt, private operands withheld |

## Three distinct chronology coordinates

- Registry mechanism: `d641510dff95541d8cd73d5bc2bf593fe024f79c`. Its complete tree contains no `records/tsei.frozen-artifact.json`.
- Producer adoption: `45b46bf7df3a60b32583291f577a36bf19d22f00`. The record explicitly names this producer `effective_commit` and this encoder implementation. First parent `5c3f285495b41c357fab045b04b44d5714ced9a9` supplies the pinned pre-adoption snapshot.
- Record introduction: `1dfc527d8f9b3561d32ca510f8fefd8d290391f6`, parent `79cb2da9c7943bd45fb64f099c3a18eab1922299`. The exact introduced record has SHA-256 `f45e3e99f3e31dc4884d92e8b1622b6c8497ecf295424442698db9d9aeb14ec6`, unchanged at registry main.

Git ancestry and record tree presence were rechecked. No ordering of SHAs, cross-repository timestamps, or prose date is used as execution authority. Exact named snapshots are a finite evidence-backed capability; unknown commits fail closed as UNSUPPORTED and require explicit repinning/ancestry review.

**Introduction is not the artifact coverage cutoff.** The registry contract says record authority starts at introduction, while artifact coverage follows producer `effective_commit`. A post-adoption producer artifact can therefore be covered when consulting the subsequently authoritative record. Rejecting every artifact predating record introduction would invent a stricter rule. Fixture 006 instead uses the source-proven pre-adoption historical example and tests only the explicit prohibition on automatic rebinding. No independent proof of an arbitrary artifact's origin is claimed.

`registry_contract_commit` is a review label for mechanism activation; it is not inserted into the frozen binding record schema.

## Mapping and discriminating cases

One registered Relation Profile, `tsei.serializer-adoption.v0` version `0`, has relation `serializer-adoption-boundary`. It preserves separate output coordinates instead of inventing a universal activation state. The expectation and adapter IDs are also `tsei.serializer-adoption.v0`; identifiers only select statically registered implementations.

| Fixture | Source-defined input / edge | Local validity retained | Observed relation / dependent claim | Interpretation limit |
|---|---|---|---|---|
| TSEI-RSI-001 | Exact `tsei.frozen-artifact` record, versioned serializer, current registry and adopted producer | Record checker returns valid; producer reproduces canonical `core-insertion-ba` vector | Serializer identity matches, adoption and record availability established; serializer-binding claim admissible | No provenance or artifact-origin attestation |
| TSEI-RSI-002 | Only requested serializer identity becomes historical unversioned `encode-json-utf8-lf` | Same object, same valid record, identical serializer bytes | Identity does not match versioned binding; no dependent binding claim | Does not assert an independently qualified alternative implementation; demonstrates byte equality is insufficient |
| TSEI-RSI-003 | Mechanism snapshot with producer first-parent before adoption | Pinned historical JSON remains processable, current prospective record remains well shaped | Mechanism true; producer adoption false; authoritative record absent at registry snapshot | Looking at a future record in a test does not activate it in that snapshot |
| TSEI-RSI-004 | Adopted producer, registry first-parent before record introduction | Source encoder qualified and byte-valid | Adoption true; record introduction false; active coverage not established | Producer and registry are separate query coordinates, not a claimed global wall-clock state |
| TSEI-RSI-005 | Same adopted producer; exact introduction snapshot | Same producer probe and record | Record introduced; prospective producer coverage recognized | No claim that introduction equals effective_commit |
| TSEI-RSI-006 | Historical pre-adoption artifact, adopted current producer, current record | Historical bytes reproduce exactly, SHA-256 `0ef9ee8f579b091d7287f05955661b04c386726e1b38c2009fa46005a09e0107` | Historically unversioned; current record cannot automatically cover it | Public synthetic preflight example only, not real oracle; historical authority is not evaluated |
| TSEI-RSI-007 | Correct serializer/adoption inputs plus public receipt's reported PROVEN / VALID_PROVENANCE | Serializer/adoption relation still holds | Stronger requested provenance-authority claim inadmissible; authority capability UNSUPPORTED | Labels are upstream reports; withheld operands prevent independent recomputation |

All seven execute through profiled fixture -> corpus registration -> Relation Profile validation -> atomic expectation admission -> adapter -> existing comparator. A conformance PASS means observed outputs equal independently admitted expectations, including negative outcomes and internal unsupported capabilities.

`serializer_binding` is the match to the exact prospective record's subject/serializer identity. It alone does not mean that record was authoritative at a queried registry snapshot. `record_introduced`, `producer_adopted`, and `artifact_covered` preserve these separate obligations. Only the full conjunction admits a serializer-binding claim. `artifact_commit` is a source-snapshot case coordinate; no general producer-origin attestation is implemented.

## Actual implementation and independent predictor

The adapter executes captured, hash-verified producer TypeScript using Node 22.15 and its native type stripping. The harness runs the real 48 tagged vectors, checking bytes, lengths, SHA-256 and rejection categories, before returning the generated artifact digest. This full source qualification lane is separate from RSI's ASCII/integer fixture transport; Unicode/f64 tagged source vectors are consumed exactly, never coerced into RSI fixtures.

The adapter also executes the pinned Python registry checker with the pinned schema and explicit schema preflight. RSI owns cleanup of the checker's file handle without altering its source bytes. The checker proves record shape and qualification-vector identity, not record authority. The wrapper separately compares the actual record with the pinned canonical record and evaluates exact snapshot membership from the verified chronology.

The independent predictor imports neither adapter nor producer/checker. It derives the ASCII/integer probe digest with Python's compact sorted serialization plus LF, checks the canonical record identity and source-defined binding obligations, and independently classifies the exact chronology coordinates. Its record identity hash is an input pin, not an expected-outcome declaration. Pinned expected rows are admitted only after every row is independently recomputed. One altered expectation blocks the whole profile before any adapter runs.

This remains trusted Python independence, not a proof that two arbitrary implementations are independent. The generic expectation contract does not eliminate review of trusted profile code.

## Authority boundary

The canonical v2 receipt reports `PROVEN` and `VALID_PROVENANCE`. Its `public_disclosure.does_not_disclose` explicitly includes `object_a_bytes`, `object_b_bytes`, `oracle_bytes`, `nonce_bytes`, and `case_level_attribution_sets`. Consequently this lane cannot recompute Object A/B authority, oracle correctness, attribution, nonce binding or provenance. It never feeds a reported status into expected authority truth.

The source record's authority is limited to serializer binding. Serializer/adoption success, `source_class`, valid record syntax and reported receipt labels do not supply missing provenance operands. All results carry:

```json
{"authority_validation":{"status":"UNSUPPORTED","reason":"required authority recomputation operands unavailable in canonical public receipt package"}}
```

## Mutation mapping

TSEI-M1 accepts a mismatched serializer on local validity alone: `test_wrong_serializer`.
TSEI-M2 substitutes mechanism activation for adoption: `test_mechanism_not_adoption`.
TSEI-M3 substitutes adoption for record introduction: `test_adoption_not_record`.
TSEI-M4 removes the artifact effective boundary: `test_nonretroactivity`.
TSEI-M5 promotes successful coverage to PROVEN: `test_no_authority_promotion`.
TSEI-M6 trusts either reported provenance label: `test_reported_labels_not_authority`.

The shared mutation registry requires the named test's decision phase to fail after normal source loading, profile admission and adapter execution. Errors are VACUOUS. Collateral failures are recorded separately; they are not the kill evidence.

## Fail-closed and compatibility boundaries

Missing/changed pinned source bytes, unregistered snapshots and unknown profile versions become UNSUPPORTED before expectation admission. Malformed fixture/record shape is INVALID_FIXTURE; a valid executed result disagreeing with admitted expectation is FAIL. The top-level taxonomy is unchanged.

Offline runs do not query a moving remote branch. Live heads were checked for this pin; consuming a changed source package requires explicit repinning/revalidation. Unsupported RSI non-ASCII/float fixtures are rejected without coercion. No universal proof, policy, state or authority fields were added.

All 158 pre-existing tracked files remain protected byte-for-byte. New composition and CI files extend registration; existing runner, comparator, schemas, result taxonomy, legacy corpus, expectations, predictor, Crystal and RVR code are untouched. The old Phase 2C STOP documents remain unchanged and do not describe closure of this narrower phase.
