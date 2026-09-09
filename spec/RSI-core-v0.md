# RSI core - v0 research draft

A locally valid component must not inherit security, authority, identity, provenance, policy, state, or status semantics from a relation that has not itself been established.

MUST and MUST NOT express requirements of this experimental profile, not ratification by a standards body. Individual mechanisms and relational security reasoning have established prior art. The candidate contribution is a cross-domain relation-substitution conformance methodology.

## Three separate levels

1. Component validity: explicitly scoped local checks over each constituent artifact or input.
2. Relation validity: an oracle establishes the protected relationship between the components in the declared policy, subject, scope, operation and state.
3. Claim validity: the positive claim is warranted only when its required local checks and relations hold. Correct rejection does not make that positive claim valid.

For a control, all declared local checks and the protected relation hold and admission is ACCEPT. A mutation preserves those local checks, changes exactly one protected relation, and makes the relation false. The implementation must discriminate before any acceptance or unauthorized state/authority/policy/provenance/status promotion.

## RSI-CORE-1 - No relation inheritance

An implementation MUST NOT infer a protected relation solely from the independent validity of its constituent artifacts.

## RSI-CORE-2 - Explicit protected relation

A verification profile MUST identify every relation whose failure can change the truth of the claimed security or semantic property.

## RSI-CORE-3 - Relation substitution resistance

Replacing one relation endpoint with an independently valid but unauthorized endpoint MUST cause rejection when the protected relation no longer holds.

## RSI-CORE-4 - Authentication before durable commitment

State derived from unauthenticated input MUST NOT become authoritative or durable before the authenticating relation succeeds.

## RSI-CORE-5 - Path invariance

Equivalent inputs evaluated under the same policy MUST receive equivalent admission results across supported ingestion paths, unless different authority semantics are explicitly declared.

## RSI-CORE-6 - Evidence-bounded status

A status MUST NOT imply evidence stronger than the evidence actually obtained and bound to the exact subject, scope, and operation.

## RSI-CORE-7 - Epoch continuity

A relation valid in epoch e MUST NOT be treated as valid in epoch e+n unless an authenticated continuity/transition rule establishes that validity.

## RSI-CORE-8 - Atomic consumption

A one-time authority, nonce position, sequence position, ratchet position, or other consumable relation MUST have at most one successful consumer.

## Scope boundary

This implementation specifies all eight rules and exercises the six requested fixture types only. CORE-7 is specification-only. The reference profile identifies the relations of its bounded claims; it does not enumerate all relations of a production messaging or authorization system.

The source-mutation experiments test the conformance checks' ability to detect specified regressions. They are not evidence of cryptographic novelty, exhaustive race safety, or a proof of universal conformance. See [conformance](conformance.md) for precise executable scope.
