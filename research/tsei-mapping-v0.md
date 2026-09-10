# TSEI mapping preflight v0 — STOP

Design/evidence only. No TSEI profile, adapter, fixture corpus or expectation set
was added. RSI remains on private main at
`366974070b0684af8b5c07dcf4cba0cde90eb8e5`.

## The unresolved mapping decision

The sources define distinct kinds of authority. They cannot silently substitute
for one another to obtain a positive TSEI-RSI-001:

| Source concept | Exact source | What it establishes | What it does not establish |
|---|---|---|---|
| Normalizer authority | `docs/TRANSFORMATION_STABLE_EVIDENCE_INTEROPERABILITY_V0.md`, §§3,10 | An explicitly trusted, immutable normalizer authority; identity-return matching and fail-closed unknown IDs | Independent provenance of an authority oracle or domain-semantic correctness of an arbitrary normalizer |
| Independent authority/oracle grounding | `conformance/tsei-invariant-discrimination-v0/independent-authority.ts`; v2 public production receipt | The production evaluator has an exact-byte/provider evidence contract; a real v2 receipt reports PROVEN | A publicly reproducible positive result when the required operands are withheld |
| Serializer binding record authority | recompute-kit `conformance/serializer-bindings/README.md` and `records/tsei.frozen-artifact.json` | An immutable canonical schema-to-serializer binding with an exact producer adoption point | Oracle provenance, authority of an answer set, or retroactive binding of earlier frozen artifacts |

The normalizer mechanism explicitly trusts its supplied authority. The registry
record is evidence of a qualified forward producer. Neither may be promoted into
the independent-authority oracle control. A registry-only implementation would
be a valid **narrower task**, but cannot silently replace the requested real
authority/source positive and substitution pair.

## Exact source identities

- TSEI source host: `pipavlo82/crystal-receipt`, canonical main
  `45b46bf7df3a60b32583291f577a36bf19d22f00`. Only TSEI source/spec/test paths
  were read. No Crystal implementation was changed.
- Serializer registry: `trustless-ai/recompute-kit`, canonical main
  `15f7f59ac47b3358492bd5741143c418b5d657f5`.
- Serializer preimages explicitly named by the record:
  `trustless-ai/recompute-kit@f1d75a530761c983e8b6900f036935ac7758538c`.
  Its ancestry to inspected canonical main was checked.

Every inspected path, SHA-256 and evidence class is recorded in
`tsei-source-map-v0.json`. Source files were read as exact GitHub commit blobs;
no external checkout was changed and no moving branch became an evidence pin.

## Chronology closed by repository evidence

| Boundary | Exact repository/commit | Independently checked evidence |
|---|---|---|
| Registry mechanism activation (`registry_contract_commit`, review label) | recompute-kit `d641510dff95541d8cd73d5bc2bf593fe024f79c` | PR #24 merge identity, commit parents, canonical ancestry; record absent from that tree |
| Producer adoption (`effective_commit`, record field) | crystal-receipt `45b46bf7df3a60b32583291f577a36bf19d22f00` | Exact record field, producer commit parents, encoder source digest; first parent `5c3f285495b41c357fab045b04b44d5714ced9a9` |
| Record introduction / authority | recompute-kit `1dfc527d8f9b3561d32ca510f8fefd8d290391f6` | Path history, record tree/blob identity, exact record bytes and ancestry to current main |

`registry_contract_commit` above labels a distinct historical boundary; it is not
invented as a field in the frozen record schema. Producer and registry commits
belong to different repositories and are never ordered by SHA text or inferred
from timestamps.

Record SHA-256:
`f45e3e99f3e31dc4884d92e8b1622b6c8497ecf295424442698db9d9aeb14ec6`.
Those bytes match at introduction and current main. The record pins:

- specification: `22207f8c4047044414da98b5497a2c9683aea14a7a498fc1819a9094c920a1f9`;
- vectors: `8d53ab1d3dfb2de1ba9db23ed06d6864b08b516451938a4b1f6db6bcdcf1950f`;
- adopted encoder: `a82587be42aa3d2e382f02e3ae633efe67b94b5831cb043131b3bc174e4fe3f9`.

The registry's validator checks record structure and qualification-vector
identity. Its own documentation explicitly says it does not resolve remote
references or recompute their digests. Those stronger checks cannot be inferred
from `verdict(record) == valid`. This pass resolved the named source preimages;
it inspected, but did not execute, the producer's 48-vector conformance test.

## Historical artifact boundary

The public `fixtures/authority-object-b-valid-v1.json` preflight example has SHA-256
`0ef9ee8f579b091d7287f05955661b04c386726e1b38c2009fa46005a09e0107` both before
adoption (producer first parent) and at adoption. It is an operational/test
example with a placeholder problem digest, not the real v2 authority operand.

Serializer spec §8 and the binding record require prospective interpretation.
Byte-identical re-encoding is not a historical binding grant. No separate legacy
resolution record for the selected historical artifact was established here.
The positive post-adoption producer boundary must not be attached to that
earlier artifact merely because current serialization reproduces its bytes.

## Authority evidence blocker

The old `evaluateProductionIndependentGrounding` path cannot ingest verified
provider observations and remains UNPROVEN. **This must not be generalized to
all production TSEI paths or instances.** The source also has newer production
Rekor evaluators and a v2 receipt:

`conformance/tsei-invariant-discrimination-v0/public-receipts/`
`tsei-ia-real-v2-20260824-02.production-grounding.json`.

That exact artifact reports `PROVEN`, `VALID_PROVENANCE`, `AGREES`, and
`production_publishable: true`, while explicitly declaring:

- `public_reproducibility = HASH_AND_LOG_RECEIPT_PRIVATE_OPERANDS_WITHHELD`;
- no disclosed Object A/B, oracle, nonce or case-level attribution operands;
- no claim of public recomputation without the withheld operands;
- `sufficient_for_real_run: false`.

The newer evaluator consumes the actual bundle bytes, not just these reported
booleans. The public receipt's hash/log coordinates are not the missing preimages.
Reading its PROVEN field into an expectation artifact would violate RSI
expectation independence. The reported successful evaluation and the older
UNPROVEN path are different instances/entry points, not a contradiction to erase.

No private operand search or replication was performed. This is an availability
limit of the inspected canonical evidence package, not a claim that the private
run never happened or that private operands cannot exist elsewhere.

## Candidate disposition

- TSEI-RSI-001/002: blocked for a reproducible real authority-oracle control and
  endpoint-substitution pair; do not use a reported result or synthetic injection.
- TSEI-RSI-003/004/005: serializer/registry/adoption mapping is bounded and pinned;
  potentially implementable in an explicitly scoped registry-only phase.
- TSEI-RSI-006: prospective-only historical behavior is source-defined; do not
  infer later binding from an unchanged artifact digest.
- TSEI-RSI-007: exact historical test bytes exist, but their real oracle provenance
  and retroactive serializer authority are not established by that fact.

None of these assessments is a runner PASS/FAIL/UNSUPPORTED result: no TSEI
fixture was registered or executed. The complete Phase 2C task remains blocked.

To resume, provide an admissible independently recomputable real authority
evidence package, or explicitly scope a separate serializer-binding/adoption
phase while leaving production oracle authority unverified. No RSI core/schema
change is indicated by this evidence limitation.
