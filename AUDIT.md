# RSI v0 implementation audit - 2026-09-09

## Independently verified

A new standalone local Git repository exists on branch `codex/rsi-v0`, with an unborn HEAD and no remote. No commit, push, publication or deployment was performed. Existing PRF and Semantic ABI repositories were not modified.

The repository contains all requested paths, six concrete fixtures, eight normative core rules, a closed schema, offline reference adapters, a conformance runner, a source-mutation harness, and tests. Standard Ed25519 and AES-GCM are supplied by `cryptography==50.0.1`; all cryptographic key material is public test material.

Verification ran with Python 3.12.14 and cryptography 50.0.1 on Windows. See [actual environment](evidence/environment.json) for the exact reported runtime version.

| Verification | Exact totals |
|---|---|
| Unit tests | PASS=51, FAIL=0, ERROR=0, SKIP=0, EXPECTED_FAILURE=0, UNEXPECTED_SUCCESS=0 |
| Schema and pair preconditions | PASS=6, FAIL=0, INVALID_FIXTURE=0, UNSUPPORTED=0 |
| Reference conformance | PASS=6, FAIL=0, INVALID_FIXTURE=0, UNSUPPORTED=0 |
| Prove-can-fail | KILLED=6, SURVIVED=0, VACUOUS=0, NOT_APPLIED=0 |

All source text passed LF-only checks. The [source manifest](evidence/source-manifest.json) binds 32 implementation, specification, test, fixture and research files. Its SHA-256 is `c6d03558d3aed9205989e70436938f4b9e9d97dc2b907f454c5a68297c62d71c`. This generated audit and evidence reports are excluded from that manifest to avoid recursive hashes. There is no commit SHA to report.

Evidence: [unit test records](evidence/tests.json), [test log](evidence/tests.txt), [schema report](evidence/schema.json), [conformance report](evidence/conformance.json), and [mutation report](evidence/mutation.json). Mutation records include exact original/mutated source digests, replacement text and executed mapped failures. Baselines and controls pass; syntax/import/setup/crash failures are not counted as kills. Negative tests separately exercise NOT_APPLIED, VACUOUS and SURVIVED classifications.

## Implemented boundaries

- RSI-001 verifies a real attacker signature over a victim-shaped body and discriminates signer/subject authorization.
- RSI-003 creates tentative state and authenticates real AES-GCM before committing its durable-state model.
- RSI-004 tests both commit orders after two stale reads of one position; the first legitimate consumer may succeed.
- RSI-006 keeps the signed artifact valid while changing its presented context.
- RSI-008 blocks confirmed status when both evidence channels fail and separately tests exact subject/scope/operation matching.
- RSI-009 keeps signatures valid while changing the policy-relevant role; live/import/snapshot/restore all reject under the same policy.
- Schema and semantic checks reject unknown structures, omitted expectations, wrong local validity, inconsistent relations, extra input changes, wrong initial state digests, duplicate JSON keys and duplicate fixture IDs.

## Still missing / not claimed

No production-system adapter, complete messaging protocol, real storage/transport integration, process/thread/distributed race test, crash-recovery test, exhaustive schedule exploration or formal proof exists here. Schema support is deliberately limited to the documented closed subset; it is not a general JSON Schema validator. The single direct crypto dependency is pinned; an independently reproducible dependency wheelhouse is not bundled.

RSI-CORE-7 is normative text only. Trust-root substitution, epoch/replay, fallback, recovery, membership and device fixtures remain outside the requested six-case v0 scope. Cross-domain utility on unrelated real implementations and publication-grade novelty review remain unverified.

## Source and novelty evidence

The supplied research is preserved as [a normalized source copy](research/source-research-v0.md). Original source SHA-256: `80ed386c04072f94713a275191ae45f583a860f92da088854371c2105a2830cd`. The reported audited revision is `9fe2687b4022af1501c690397af4306b82bb53f9`; that audit was not independently rerun. The Established / Adjacent / Promising / Unverified distinctions are preserved verbatim in the derived prior-art matrix. Promising is not upgraded to novel.
