# Phase 2B.1 — RVR digest-binding validation

**Local validation passed.** This closes the implementation and local validation
gates for the intentionally bounded digest-binding scope. Final remote CI and
commit identity must be checked on the published private-main commit; no CI
result is inferred from local tests.

RSI HEAD before: `5a3b90ccab1e6b9d463a80f419576820e0129608`.
Repository remains private; only `main` is used. No external repository content
was changed. No public release, tag or PR is part of this work.

## Results

| Gate | Before | After |
|---|---:|---:|
| Full unittest suite | 229 PASS | 264 PASS |
| Full suite under `python -O` | 229 PASS | 264 PASS |
| Legacy checks | 36 PASS | 36 PASS; exact outcome diff 0 |
| Crystal Receipt checks | 4 PASS | 4 PASS; exact report byte diff 0 |
| RVR digest checks | — | 10 PASS across 6 fixtures |
| Combined generic pipeline | 40 PASS | 50 PASS |
| Existing mutation records | 26 KILLED | 26 KILLED; exact record diff 0 |
| New RVR mutations | — | 6 KILLED |
| All mutations | 26 KILLED | 32 KILLED |
| SURVIVED / VACUOUS / NOT_APPLIED | 0 / 0 / 0 | 0 / 0 / 0 |
| FAIL / INVALID_FIXTURE / UNSUPPORTED checks | 0 / 0 / 0 | 0 / 0 / 0 |
| Protected historical artifact hashes | 80 | All 80 unchanged |
| Expanded pre-change file protection | — | 124 existing files byte-identical |
| Generic core changes / semantic exceptions | 0 / 0 | 0 / 0 |

The expanded 124-file protection covers every previously tracked file except the
CI workflow, which adds three RVR commands. The protected working-tree bytes also
match the pre-change committed Git blobs, so this proof does not depend on a
Windows newline materialization difference. All technical additions use LF.

The machine report `rvr-digest-binding-validation-v0.json` contains the complete
execution rows, expectation admissions, mapped mutation classifications and
collateral failures. Two independent report runs must be byte-identical. Old
extension, expectation, Relation Profile and Crystal gates were rerun unchanged.

## Source identity

- recompute-kit: `15f7f59ac47b3358492bd5741143c418b5d657f5`.
- RVR: `287c0ea1c2578c1833405bc2476975f95addbada`.
- Reference consumer: `bdba0b674c2b2d301b75b4b23a33702b0bacfa64`.
- Current companion main: `f5f36778e7cbf6c26fd61a7d66b70b9108447746`.

The companion's v0.3.9 file remains byte-identical to the prior inspected cut.
Exact source paths, SHA-256 digests, evidence classes and fixture derivations are
in `rvr-digest-binding-source-map-v0.json` and `rvr-digest-binding-mapping-v0.md`.
The two pinned Python references execute in the adapter; the independently
implemented predictor is checked against all 14 source vectors. Both pinned
JavaScript reference CLIs additionally reproduced 8/8 amendment and 6/6 verdict
vectors. Context-only source documents do not become execution oracles.

## What passed

- RVR-RSI-001: no amendment retains A with amendment unresolved; a separately
  digest-bound A verdict does not resolve the amendment or a substantive dispute.
- RVR-RSI-002: an unbound A-to-B substitution and a wrong party digest leave A
  effective. Both profile endpoints remain locally well-shaped.
- RVR-RSI-003: the source bilateral digest relation makes B effective. Changing
  the public-key representation does not manufacture or remove authentication.
- RVR-RSI-004: B-bound verdict and source alternative verdict both establish
  their scoped profile/core digest relation.
- RVR-RSI-005: a verdict locally bound to its own recomputed digest but naming
  stale A fails the effective-B relation, while the earlier transition remains
  permitted at digest scope.
- RVR-RSI-006: successful transition/verdict digest binding cannot admit a
  requested crypto-authentication claim.

RVR-M1 through M6 each reached their mapped semantic assertion and were KILLED.
They exercise unbound substitution, false resolution from retained A, ignored
verdict mismatch, unresolved-layer collapse, digest-to-crypto promotion, and
pubkey-to-crypto promotion. Setup/import/source errors cannot be valid kills.
Optional M7 is not registered; explicit hostile-label tests cover ignored vector
names and excluded expectation-label authority.

## Scope and remaining limitations

**RVR cryptographic-authentication scope: UNSUPPORTED.** A digest-scoped fixture
PASS means actual behavior matched independently admitted expected behavior. It
does not prove cryptographic authorization, identity/control of a public key,
substantive verdict truth, divergence resolution or execution.

The source references themselves omit signature cryptography. No substitute
signature lane was added. The profile's explicit unsupported capability and
inadmissible crypto claim are wrapper coverage/claim boundaries, not new source
cryptographic evidence. Substantive resolution is `not_evaluated`; no companion
resolution policy is silently inferred or implemented.

Only the source bilateral default and the existing ASCII/integer fixture
transport are covered. Neither generic JCS conformance nor arbitrary party
policies are claimed. Pinned offline evidence requires explicit upstream repin
and revalidation. Trusted Python implementation independence remains subject to
source review; tests are not a filesystem sandbox.

The same fixture-registration → Relation Profile → expectation admission →
adapter → comparator pipeline executes Crystal Receipt and RVR together, with
their different semantics and no generic branch. Crystal source/profile/adapter
and fixtures remain unchanged.

After exact-commit CI succeeds, the allowed closure is **Phase 2B.1 CLOSED,
RVR digest-binding scope VALIDATED**. **Full Phase 2B remains BLOCKED** until a
separately pinned, independent signature-verification lane exists and is
validated. No third domain is started.

Allowed claim: “RSI validated a second real relation family: RVR profile-transition
and verdict digest binding, while mechanically preventing promotion of digest
binding into an unsupported cryptographic-authentication claim.”
