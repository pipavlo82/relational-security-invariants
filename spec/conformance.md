# Relation-Binding Conformance Fixtures - v0

## Fixture contract

The shipped schema is Draft 2020-12 JSON Schema. It defines exactly six closed profile branches. IDs, protected relations, expected states, required evidence, policy version, local-validity predicates, changed-field declarations, failure conditions and final-state constraints are explicit and profile-bound. Control and mutation both carry concrete components. Unknown fields, malformed shapes, omitted expectations and unrecognized required schema features reject.

The offline standard-library evaluator intentionally implements only: `$schema`, `title`, `description`, `type` (object, array, string, integer, boolean), `properties`, `required`, `additionalProperties: false`, `items`, `minItems`, `uniqueItems`, `enum`, `const`, `oneOf`, `pattern`, `minimum`, and `minLength`. Supported pattern expressions in this schema use only simple ASCII ranges, groups and repetitions shared with JSON Schema. Other keywords/dialects reject; no references are fetched and no defaults are inferred. It is not a general Draft 2020-12 implementation. A future schema extension requires an explicit evaluator/version change and tests.

The loader rejects duplicate JSON keys and non-JSON NaN/Infinity. Schema validation is followed by pair validation: exact changed fields, successful named local checks, true control relation, false mutation relation, and consistency of any initial state digest. `initial_state_digest` is optional; its referent is the state object for RSI-003, `{revision: n}` for RSI-004 and `{}` for stateless profiles. Digests use SHA-256 over compact, sorted-key, ASCII-escaped Python JSON. This is a v0 restricted-input serialization contract, not a claim of JCS conformance.

## Reference policy and relation oracles

| ID | Relation and acceptance oracle | Mutation constraint |
|---|---|---|
| RSI-001 | Verify Ed25519 over the body; signer must equal its subject. Test-key registry has victim and attacker. | Same body, attacker signer and corresponding valid signature. No admission/authority promotion. |
| RSI-003 | AES-GCM authentication authorizes committing tentative bootstrap state. | Corrupt ciphertext while preserving parseable bytes and initial state. Reject, tentative path executes, no commit, final state digest equals initial digest. |
| RSI-004 | One logical position can authorize at most one consumer. | Add a second distinct consumer of the same revision. Both read first; try both commit orders. At most one succeeds and final revision agrees with successful consumption. |
| RSI-006 | Signed body context must equal presented context. | Change only presented context; signature remains valid. No admission/provenance promotion. |
| RSI-008 | At least one successful acknowledgment/publication record must bind the exact subject/scope/operation. | Fail both channels, retain all evidence coordinates. Reject and remain failed; no confirmed status. |
| RSI-009 | Signed member role is required on each supported path under the same policy. | Re-sign the same object with guest role; all four paths reject. No policy promotion. |

Local checks are computed, not trusted from a Boolean label in a fixture. The schema establishes structural predicates; cryptographic predicates verify actual bytes. Re-signing changes signature bytes to preserve local validity; it does not add a second protected relation. Relations for atomic consumption and status concern a set of operations/evidence; changing an array is a single declared relation intervention.

The invalid RSI-004 aggregate claim is that both operations may consume one one-time position. Batch `REJECT` is compatible with one authorized `ACCEPT`. It does not require rolling back the first legitimate consumer. This differs from RSI-003, which requires no durable-model state change after authentication failure.

No different ingestion authority semantics are declared in v0. A future profile may declare such semantics explicitly, but silently treating import or restore as more authoritative is prohibited here.

## Adapter contract and observations

Reference functions receive a deep copy of components only. They do not receive fixture expectations or oracle results. A separate judge compares observed decisions and effects against the profile. Source mutation replaces only a target adapter assignment; fixture preconditions, crypto primitives and the conformance judge remain fixed.

Output observations are bounded to the profile: outcome plus the relevant authority/provenance/policy flag, tentative and final state evidence, consumption decisions/revision, or status evidence result. There is no arbitrary side-effect interception or network transport. Production adapters would need trustworthy capture of all relevant effects and independently bound evidence before these checks could establish anything about a real system.

Each report includes separately named component, relation and positive claim validity. `claim_validity` is the oracle's normative assessment, not the adapter's self-report. Observed outcome is separate. The atomic reverse schedule has an additional raw observation and repeats the same mapped check.

## Result states

- PASS: both pair members meet their expected decisions and constraints.
- FAIL: a system decision/effect violates a check, or adapter execution/output processing fails. Execution errors are explicitly marked.
- INVALID_FIXTURE: schema, JSON, pair preconditions, initial digest or duplicate fixture identity fails.
- UNSUPPORTED: the evaluator name/version is not implemented.

Both JSON totals and zero-valued states are explicit. Every count is accumulated directly; no count is inferred by subtraction. Empty selection is failure. Validator exits zero only when all cases PASS, including for `--schema-only` (which validates preconditions without running the adapter).

## Prove-can-fail contract

Each of the six source patches has exactly one unique anchor. The harness compiles a modified function into an isolated namespace without editing repository source. It reports original/mutant SHA-256, replacement text, baseline, mutant observations and mapped checks.

- KILLED: baseline PASS; patch applied; mutant control still passes; mapped mutation check executes and fails at the decision/effect assertion; no execution error.
- SURVIVED: patch applied, control and mapped check execute, but the mapped check does not fail.
- VACUOUS: baseline is not PASS, control regresses, or mapped check does not execute.
- NOT_APPLIED: invalid fixture/schema, missing/ambiguous/unchanged anchor, syntax/import/setup error, or adapter crash prevents a valid experiment.

Malformed fixture JSON is NOT_APPLIED. A structurally valid fixture whose semantic preconditions fail gives a nonpassing baseline and is VACUOUS. Neither is a kill. An unrelated failed check cannot qualify. Only all KILLED yields exit zero.

The atomic patch disables compare-and-swap eligibility; the ingestion patch bypasses member checks on alternate paths; the others bypass one binding/commit/evidence condition. No mutation targets the test oracle or expected result. These are six bounded mutation experiments, not a comprehensive mutation score for a production implementation.
