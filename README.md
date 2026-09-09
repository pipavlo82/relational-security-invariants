# Relational Security Invariants (RSI)

Relational Security Invariants (RSI) is a conformance framework for failures where each local component can remain valid while the security-relevant relation between components is changed, missing, stale, or unauthorized.

**Core invariant:**

```text
local validity preserved + protected relation broken
=> no acceptance / authority / state / policy / provenance / status promotion
```

This project does not claim to invent replay protection, identity binding, nonce uniqueness, complete mediation, trust-root continuity, or relational security reasoning. The research question is whether one implementation-facing adversarial fixture model can unify these relation failures across domains.

**v0 research / implementation proof-of-concept, not a final standard.** The candidate contribution is the cross-domain relation-substitution conformance methodology. Six offline reference fixtures demonstrate the mechanism; they do not establish novelty or production-system conformance.

## Run locally

Python 3.12+ and the single pinned direct dependency in `requirements.txt` are required. `cryptography` supplies standard Ed25519 and AES-GCM, avoiding a home-grown crypto implementation. All keys and the fixed cipher vector are public test material. The remaining code uses the standard library, including an explicitly bounded JSON Schema evaluator.

From this repository directory:

```sh
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m runner.validate_fixtures --schema-only
python -m runner.validate_fixtures
python -m runner.prove_can_fail
```

The install step may use a package index; execution never uses the network. For an air-gapped setup, supply the pinned package and its platform dependencies from a preprovisioned wheelhouse and use `pip install --no-index --find-links WHEELHOUSE -r requirements.txt`. No external services or credentials are required. Direct script invocation also works: `python runner/validate_fixtures.py`.

Both runners emit JSON and exit nonzero unless every selected case succeeds. Every state is counted independently, including zero-valued states. `--schema-only` includes pair preconditions and local-validity checks; it does not execute the reference system. Optional positional paths select fixtures; `--schema PATH` is available on the validator. Unknown evaluator name/version is `UNSUPPORTED` during execution.

## Initial coverage

| Fixture | Concrete reference behavior |
|---|---|
| RSI-001 signer -> subject | A real attacker Ed25519 signature over an unchanged victim-shaped body verifies locally but cannot authorize the victim identity. |
| RSI-003 auth -> commit | A structurally valid tampered AES-GCM ciphertext creates tentative bootstrap state; authentication fails and durable-model state remains unchanged. |
| RSI-004 position -> consumer | Two workers read revision 7 before either commits. Both possible commit orders are checked; at most one consumes that position. |
| RSI-006 artifact -> context | An unchanged valid signed artifact is presented in another room and rejected. |
| RSI-008 status -> evidence | Recipient acknowledgment and durable-publication evidence both fail; confirmed status is withheld. Evidence must bind subject, scope and operation. |
| RSI-009 object -> ingestion policy | A validly signed guest object violates the member-only policy and is rejected via live, import, snapshot and restore. |

The three levels are reported separately: component validity, relation validity and claim validity. Rejection of a broken relation is a conformance `PASS`, not a positive security claim. Atomic consumption permits the first authorized consumer; the aggregate request that both consumers succeed is rejected.

## What this proves, and what remains

The source-mutation harness neutralizes one enforcing condition per fixture, preserves the oracle, and records the exact original/mutant source digests and mapped failed checks. It requires a passing baseline and control, an applied mutation, and an executed failed conformance check. Syntax/import/setup errors and earlier crashes cannot count as kills.

Implemented: eight core rules as v0 normative text; a closed six-profile schema; actual local cryptographic verification; six reference evaluators; independent pair preconditions and output checks; deterministic state/concurrency models; structured reports and mutation controls.

Still missing: production adapters, real messenger/database integration, physical durable storage and crash recovery, OS/process/distributed concurrency testing, exhaustive schedules, and fixtures for trust-root substitution, epoch continuity/replay, fail-safe fallback, recovery, membership epochs and device identity. RSI-CORE-7 is specified but has no executable initial fixture. Generic and messaging folders are reference models, not independent real-world validation. There is no complete system-security claim, formal proof, publication-grade novelty review, or general-purpose JSON Schema engine.

Read [the v0 core](spec/RSI-core-v0.md), [terminology](spec/terminology.md), [conformance contract](spec/conformance.md), [prior-art assessment](research/prior-art-v0.md), and [verification audit](AUDIT.md). The original supplied research is preserved with source digests; its underlying audit findings remain upstream reported.
