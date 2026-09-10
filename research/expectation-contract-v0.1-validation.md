# Expectation Contract v0.1 validation

Base main: `4698cccb1dbb1638b241e1d409e0897eb53dc86e`.
The resulting implementation SHA is the commit containing this report and is
reported exactly after commit; embedding its own hash would be self-referential.

Expectation Contract v0.1 is implemented. Independent predictions must match
all rows of a digest-pinned, fixture-set-bound artifact before any expectation
is admitted. A single mismatch blocks every adapter in that profile. Profile
failures are UNSUPPORTED with an internal PROFILE_ERROR, not malformed fixtures.

| Check | Before | After |
|---|---:|---:|
| Tests | 52 | 93 |
| Optimized Python tests | 52 | 93 |
| Fixture files | 6 | 6 |
| Synthetic PASS | 36 | 36 |
| Legacy KILLED | 12 | 12 |
| Expectation-contract KILLED | 0 | 4 |

All FAIL, INVALID_FIXTURE and UNSUPPORTED baseline counts are zero. Both mutation
sets have zero SURVIVED, VACUOUS and NOT_APPLIED. EXP-M1/M2 are evidence tampering;
EXP-M3/M4 disable enforcement and fail their exact mapped architecture assertions.
Collateral failures are recorded separately in the machine report. EXP-M5 is an
explicit provenance rule and contributes no fabricated kill.

The RSI-CORE normative spec, RBCF fixture schema, observation schema, six complete
fixture files, manifest, old expectation artifact and synthetic predictor remain
byte-identical. The schema diff for both existing schemas is empty. Only a new
parallel expectation envelope schema is added. It binds profile identity/version,
exact fixture bytes and the complete set of unchanged prediction records.
No new relation-truth field or protected-relation rule has been introduced.

Every complete ordered synthetic case record is identical before/after, including
request digest, local validity, expected observation, actual observation and errors.
All 36 wrapped predictions equal the unchanged original predictor, and all legacy
expectation rows are canonically identical. Full reports differ only in source
identity/scope and new reporting metadata; deterministic reruns are byte-identical.

Validation included profile/tamper/registry tests, schema checks, all synthetic
checks, full tests, original mutation gate, four new mapped mutations, optimized
tests, canonical serialization, original fixture generator --check, and static
search of generic execution/admission/oracle code. CI adds expectation admission
and mutation checks to the existing Python 3.12/3.13 matrix; post-push CI status is
reported separately after the exact main commit exists.

See [machine-readable evidence](expectation-contract-v0.1-validation.json) for
all before/after SHA-256 values, exact changed-file inventory, mutation mappings,
collateral failures and outcome digests.

The expectation compatibility gate is resolved: future trusted profiles can be
registered without core oracle branches. The broader Extension Contract can now
proceed. Phase 2 remains blocked by remaining fixture-ID/schema, deterministic
discovery and legacy mutation-registry extension work, plus domain evidence and
predictor review. No external-domain adapter or real-domain claim is implemented.
