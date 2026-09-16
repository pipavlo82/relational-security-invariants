# Semantic ABI declared-edge admission (post-v0)

## Evidence boundary

This additive family validates the `linkEdge` decision over supplied typed
declarations at `trustless-ai/semantic-abi@d15c666dfccff17f7350fe97d2fc7b71cb2cbaee`.
It does not execute a Semantic ABI backend, establish declaration truth, or
establish that an action occurred. The upstream manifest is explicitly a draft.
The historical RSI `v0` tag is unchanged.

Base RSI commit: `ff7e3089e1ab7b2de834e7a0d85f12eabb7e232c`.
Source file identities and SHA-256 values are in
`semantic-abi-source-map-v1.json` and `../evidence/semantic-abi/source-pin.v0.json`.
The vendored linker and its five upstream tests are byte-identical copies, not
RSI reimplementations. Upstream repositories were only read.

## Relation and input boundary

Profile: `semantic-abi.claim-edge.v0`, version `0`.
Relation: `claim-authority-scope-time-binding`.

A requirement is satisfied only when one established claim matches claim type,
scope, temporal field name and value, and compatible authority. Equal authority
is allowed; the only cross-authority conversion is
`INDEPENDENT_RECOMPUTATION -> SEMANTIC_VERIFICATION` for the same claim boundary.
This rule is directed, not global and not reversible. Coordinates from several
claims cannot be combined into a fictitious matching claim.

RSI validates an explicit schema-conforming ASCII subset: nonempty string
coordinates, a closed authority enum, exactly one temporal key per claim,
1–32 established claims and 0–32 negative boundaries. The count limits are RSI
profile bounds, not upstream requirements. Full manifests, endpoint routing,
chains of edges, unrestricted Unicode and malformed-input permissiveness are
outside this profile. The producer wrapper carries `component`, `establishes`
and `does_not_establish`; it is not represented as a complete manifest.
The projection does not validate closest-claim ranking, diagnostic prose, or
which matching claim object is returned when multiple candidates are compatible.

Temporal values are compared literally. A value such as `receipt.verified_at`
is not dereferenced into a receipt or checked against wall-clock time. Negative
boundaries contain no temporal field and are matched by claim, authority and
scope. The pinned linker searches positive claims first: contradictory positive
and negative declarations return the positive edge. RSI records that behavior
without asserting that it is a desirable conflict policy.

The output keeps `edge_compatible` and `explicit_boundary_hit` separate from
`claim_truth` and `execution_occurrence`. The latter two always remain
`UNSUPPORTED`. RSI PASS means agreement with admitted observations; it does not
promote declared compatibility to proof of the declared proposition.
Authority labels are supplied declarations: this profile does not verify that
the producer actually recomputed a result or that its claimed authority is earned.

## Cases

| Case | Substitution or boundary | Source-supported observation |
|---|---|---|
| SABI-RSI-001 | Exact typed claim control | Compatible |
| SABI-RSI-002 | Claim name only | Incompatible |
| SABI-RSI-003 | Scope only | Incompatible |
| SABI-RSI-004 | Authority only | Incompatible |
| SABI-RSI-005 | Temporal value only | Incompatible |
| SABI-RSI-006 | Temporal key only, same value | Incompatible |
| SABI-RSI-007 | Exact local recomputation conversion | Compatible |
| SABI-RSI-008 | Conversion with different claim | Incompatible |
| SABI-RSI-009 | Conversion with different scope | Incompatible |
| SABI-RSI-010 | Conversion with different time | Incompatible |
| SABI-RSI-011 | Reverse authority conversion | Incompatible |
| SABI-RSI-012 | Coordinates distributed over two claims | Incompatible |
| SABI-RSI-013 | Component display label only | Same result as 001 |
| SABI-RSI-014 | Matching explicit negative boundary, no positive | Incompatible; boundary hit |
| SABI-RSI-015 | Negative reason text only | Same result as 014 |
| SABI-RSI-016 | Matching positive and negative declarations | Compatible; no boundary hit |

These are local definition-derived fixtures, not evidence of live production
traffic. The basic typed claim is backed by the pinned upstream linker test.
Per-case derivations and fixture hashes are in
`semantic-abi-golden-derivation-v1.json`. Expected booleans were specified before
executing the new adapter or predictor; neither was used to generate them.
During admission testing, the initial fixture-authoring script was found to
retain an in-memory alias between producer and requirement. It unintentionally
changed both sides of several substitutions. Atomic admission rejected the
resulting expectation mismatch. The fixtures were repaired to hold the producer
constant; the prewritten expected decisions were not changed. A regression test
checks the intended one-sided substitutions. This is not a blind-authoring claim.

## Dependency and independence discipline

Actual: Python transport -> Node -> exact pinned upstream `linkEdge`.
Expectation: Python tuple-set construction with a directed authority closure ->
membership test. The predictor does not import the adapter, invoke Node, read
source-derived result tables or read frozen expectations. Frozen rows are
checked against the predictor by the existing atomic admission contract.

The paths share immutable inputs, `rsi.codec`, schema/shape validation, source
pin verification and the generic runner/comparator. The predictor and actual
use different semantic code and different execution languages. They still
share the interpretation of one source contract. Negative-boundary precedence
is implementation-derived, not separately specified normative evidence. There
is no additional clean-room third leg, external author-independence evidence,
or claim that this family resolves common-mode interpretation risk.

Use **separately implemented expectation predictor**. Author independence is
**UNKNOWN**. Existing Crystal external evidence is not transferred to this
family. Mutation kills prove mapped decisions are load-bearing; they do NOT
prove independently derived semantic expectations.

| Independence dimension | Assessment | Reason |
|---|---|---|
| Code | STRONG | Source linker and tuple-set predictor have no shared semantic evaluator |
| Language | STRONG | JavaScript decision versus Python derivation; insufficient alone |
| Algorithm | MODERATE | Set closure/membership versus per-claim search; same interpreted rule |
| Data source | WEAK | Contract and implementation share upstream origin; no external third leg |
| Helpers | MODERATE | Semantic code separate; codec, input validation and source-integrity gate shared |
| Author | UNKNOWN | No evidence of independent authorship of this validation |
| Implementation path | STRONG | Real pinned source execution versus local set derivation |
| Oracle | MODERATE | Definition-derived rows and predictor; correlated interpretation remains possible |

These assessments describe this bounded profile only and do not revise H1 or
the Crystal H2/external-review records. No single aggregate independence label
is inferred from the language difference or mutation count.

Frozen expectations detect divergence from previously admitted semantics;
they do not by themselves prove that the original expectation was independently
derived. Serialization is RSI's existing restricted ASCII sorted-key JSON,
with a final LF; no JCS claim is made.

## Mapped mutations

Mutations change the local actual-side wrapper/projection while leaving source
bytes, predictor and frozen rows unchanged. They demonstrate a crossing of that
boundary; they do not claim exhaustive mutation coverage of upstream source.
Setup or source-integrity failures are classified as VACUOUS, not KILLED.

| Mutation | Wrong assumption | Mapped test |
|---|---|---|
| SABI-M1 | Ignore claim substitution | test_claim |
| SABI-M2 | Ignore scope substitution | test_scope |
| SABI-M3 | Ignore authority substitution | test_authority |
| SABI-M4 | Ignore temporal value | test_time_value |
| SABI-M5 | Alias the two temporal keys | test_time_kind |
| SABI-M6 | Global recomputation conversion | test_no_universal_recomputation |
| SABI-M7 | Bind component display label | test_component_mirror |
| SABI-M8 | Mix coordinates from different claims | test_no_cross_claim_mixing |
| SABI-M9 | Promote compatibility to claim truth | test_no_truth_promotion |
| SABI-M10 | Promote compatibility to execution | test_no_execution_promotion |

## Reproduction

Use the repository's pinned Python dependencies and Node 22.15.0. Evaluation is
offline after checkout and dependency installation; the required upstream
files are vendored with exact-byte integrity checks.

```sh
python -m unittest tests.test_semantic_abi -v
python -O -m unittest tests.test_semantic_abi -v
node --test evidence/semantic-abi/runner/test/linker.test.mjs
python tools/run_semantic_abi.py --include-previous --output artifacts/semantic-abi.json
python tools/prove_semantic_abi_can_fail.py --output artifacts/semantic-abi-mutations.json
```

Validation totals and preservation evidence are recorded separately in
`semantic-abi-validation-v1.json`. The old compositions remain runnable without
the new family. No generic core/schema/comparator/taxonomy change is needed.

## Bounded claim

Under the pinned Semantic ABI linker, RSI distinguishes exact declared
claim/authority/scope/temporal compatibility from coordinate substitutions,
global authority coercion and mixed-claim matching, while preserving selected
display-only changes. Compatibility of supplied declarations does not establish
their truth, cryptographic validity, freshness, or action execution.
