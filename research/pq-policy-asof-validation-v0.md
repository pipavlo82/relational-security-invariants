# PQ policy/cutoff/as-of validation v0

## Scope and decision

Local validation passed. Phase 2D closure requires successful CI on the commit containing this report; the delivery response records that exact HEAD and CI result. This validates conditional policy behavior over pinned, supplied binding history. It does not verify deployed anchors or an authenticated authority chain.

RSI HEAD before: `b899b485f02dbe9de4d20b10cfcfb1e2e74578a2`, branch `main`, private repository. HEAD after is the commit containing this report. No external repository was modified.

Source: `trustless-ai/recompute-kit`, canonical `main`, `15f7f59ac47b3358492bd5741143c418b5d657f5`. All 11 source files, exact paths, evidence classes and SHA-256 digests are recorded in [the source map](pq-policy-asof-source-map-v0.json) and [mapping](pq-policy-asof-mapping-v0.md). Canonical source pins were reverified before implementation.

## Exact results

| Check | Before | After |
|---|---:|---:|
| Full unittest suite | 303 | 337 |
| Full suite under python -O | 303 | 337 |
| Conformance PASS | 57 | 64 |
| FAIL / INVALID_FIXTURE / UNSUPPORTED | 0 / 0 / 0 | 0 / 0 / 0 |
| Mutation KILLED | 38 | 45 |
| SURVIVED / VACUOUS / NOT_APPLIED | 0 / 0 / 0 | 0 / 0 / 0 |

The new 34 tests pass. PQ contributes six fixture files and seven case checks: PQ-RSI-001, 002, 003, 004 (two cases), 005, 007. PQ-RSI-006 is omitted: the inspected policy lane does not establish a general subject/signature authority relation.

- PQ-RSI-001: A governs the supplied pre-cutoff as-of point.
- PQ-RSI-002: old A companion after the rotation/cutoff boundaries is rejected by source policy despite a supplied local-validity flag.
- PQ-RSI-003: B is selected under the supplied pinned history; transition authentication remains unsupported.
- PQ-RSI-004: historical A is retained at its supplied anchored pre-cutoff point while current authority is B. The paired created_at-only case is rejected; signing time alone does not establish historical eligibility.
- PQ-RSI-005: a stale A snapshot cannot inherit B's governing as-of relation, even when native policy admission succeeds.
- PQ-RSI-007: policy admission and predecessor/signature metadata cannot promote into authenticated transition authority.

All 21 supplied cutoff/rotation/revocation policy vectors also match both the pinned native reference and the independent predictor. Expectations admit atomically; tampering blocks admission. The adapter executes pinned source policy logic and cannot read expected rows. The predictor does not call the adapter or source implementation.

PQ-M1 through PQ-M7 are KILLED at their mapped assertions. Setup/import/schema failures do not count as kills. Every result has an empty errors list; collateral assertion failures are recorded separately in the deterministic JSON report.

## Preservation and determinism

All prior 57 outcomes and all prior 38 mutation records are identical. Legacy, Crystal Receipt, RVR and TSEI outcome differences are each zero. All 202 pre-change tracked-file hashes match, including the earlier protected sets. No prior tracked file changed.

RSI-CORE, legacy and profiled schemas, generic runner/comparator, taxonomy, expectation/extension core, and previous domain implementations remain unchanged. Semantic exceptions: zero. Static anti-coupling: PASS. All four domains execute through the same pipeline. Repeated structured reports are byte-identical. Local validation logs are under ignored `artifacts/pq-phase2d/`.

## Evidence limits

The source rotation anchor is explicitly intended, not a proven deployed anchor. Policy vectors supply anchored/signature-validity flags. Results remain conditional on these inputs; independent anchor verification is UNSUPPORTED. The tested distinction is governing binding at the supplied anchor/as-of point versus created_at/current authority, not a claim that the anchor was cryptographically proven here.

The rotation artifact declares `SLH-DSA-SHA2-192s`. The inspected offline deep recomputation lists deferred `ML-DSA` signature checks. Both identities are preserved; algorithm-specific verification is UNSUPPORTED. Presence of signatures, predecessor references or successful digest checks does not prove signature authenticity.

RVR crypto authentication, TSEI provenance authority and full PQ authenticated transition-chain validation remain UNSUPPORTED. A top-level conformance PASS means actual matches independently admitted expectation; it does not promote any unsupported capability. ASCII/integer transport limits and trusted Python predictor independence caveats remain.

The narrow four-domain architecture claim is supported by these local results, subject to exact-commit CI: semantic-snapshot equivalence, profile/verdict digest binding, serializer/adoption boundary binding, and conditional temporal authority/as-of binding. No universal security or full authority-chain claim is made.

## Files added

- `.github/workflows/pq.yml`
- `adapters/pq/__init__.py`
- `adapters/pq/model.py`
- `corpora/pq/fixtures/PQ-RSI-001.json`
- `corpora/pq/fixtures/PQ-RSI-002.json`
- `corpora/pq/fixtures/PQ-RSI-003.json`
- `corpora/pq/fixtures/PQ-RSI-004.json`
- `corpora/pq/fixtures/PQ-RSI-005.json`
- `corpora/pq/fixtures/PQ-RSI-007.json`
- `evidence/pq/cutoff_enforce.py`
- `evidence/pq/deep_recompute.py`
- `evidence/pq/gate.py`
- `evidence/pq/pq-key-binding-v0.cutoff-vectors.json`
- `evidence/pq/pq-key-binding-v0.revocation-vectors.json`
- `evidence/pq/pq-key-binding-v0.revocation.json`
- `evidence/pq/pq-key-binding-v0.rotation-vectors.json`
- `evidence/pq/pq-key-binding-v0.rotation.json`
- `evidence/pq/pq-key-binding-v0.spec.md`
- `evidence/pq/pq-key-binding-v0.vectors.json`
- `evidence/pq/source-pin.v0.json`
- `evidence/pq/suite.json`
- `extensions/pq.corpus.v0.json`
- `extensions/pq.py`
- `profiles/pq/__init__.py`
- `profiles/pq/expectation-profile.v0.json`
- `profiles/pq/expectation.py`
- `profiles/pq/expectations.v0.json`
- `profiles/pq/relation.py`
- `profiles/pq/source.py`
- `research/pq-policy-asof-mapping-v0.md`
- `research/pq-policy-asof-source-map-v0.json`
- `research/pq-policy-asof-validation-v0.json`
- `research/pq-policy-asof-validation-v0.md`
- `tests/test_pq.py`
- `tools/check_pq_policy_asof.py`
- `tools/prove_pq_can_fail.py`
- `tools/run_pq_policy_asof.py`
