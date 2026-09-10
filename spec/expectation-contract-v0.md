# Expectation Contract v0.1

**Expected outcomes are evidence that must themselves be validated; they are not authoritative merely because they are pinned.**

This extension-level contract preserves RSI-CORE and the RBCF v0 semantic model.
Fixture author declaration != independently established expected relation != implementation-under-test result.

## Roles and trust boundary

A fixture supplies a challenge. A trusted, statically registered expectation
profile independently predicts its outcome. A pinned artifact records those
predictions. An adapter executes the implementation under test. The generic
comparator compares the actual observation with an admitted prediction.
Neither an artifact digest nor an author's expected label establishes an oracle.
No relation truth is inferred from ACCEPT, REJECT, CONFLICT or UNVERIFIABLE.
The existing local_validity and observation distinction is preserved; this
contract adds no relation_expected field or other fixture semantic field.

## Profile registration

`runner/expectation_registry.py` defines immutable `ExpectationProfile` records:
profile_id, version, explicit fixture_scope (identity/path pairs), predictor,
expectations_path and expectations_digest. Trusted callbacks validate fixtures,
prediction records, scope, and construct execution plans. Executable callbacks
are wired by Python source, never deserialized from registration metadata.
IDs use ASCII `[a-z0-9][a-z0-9._-]{0,127}`. Duplicate profile IDs and duplicate
fixture identities/paths within a scope fail registration. Registry enumeration
is sorted. Identity selects registered code, never an expected outcome.
Different profiles have separately scoped fixture sets and atomic admissions.
`profiles/defaults.py` is the application composition root; the runner and
comparator contain no project-specific semantic branches.

The first profile is `core.synthetic.v0`, version `0`. It wraps the unchanged
`rsi.oracle.predict` and local-validity interpreter, and retains the old corpus
verification as a compatibility scope validator. The old expectation artifact,
fixtures, manifest, and their schemas remain byte-identical. Its historical
adapter execution order lives in the compatibility profile, outside the runner.

## Artifact and exact fixture-set binding

`schema/expectations.v0.schema.json` documents the closed versioned envelope:

```json
{
  "schema": "rsi-expectations.v0",
  "profile_id": "core.synthetic.v0",
  "profile_version": "0",
  "fixture_set_digest": "<SHA-256>",
  "expectations": [{"fixture_id": "<identity>", "prediction": {"<check-id>": {"local_validity": true, "observation": {}}}}]
}
```

The empty observation above is schematic, not a valid synthetic observation.
The registered prediction validator enforces existing observation semantics.
Each prediction contains the existing check records without reinterpretation.
The original artifact remains pinned separately by the legacy corpus manifest;
the new envelope preserves all 36 individual expectation records exactly.

fixture_set_digest is SHA-256 of the canonical JSON encoding of the sorted
array of `{fixture_id, sha256}` records. Each sha256 hashes the exact fixture
file bytes, including whitespace. Ordering uses fixture_id. Adding, removing,
or replacing a registered fixture invalidates the binding. Only explicitly
registered files enter a scope. Relative paths cannot escape the repository.
This does not claim to implement general directory discovery or migrate RBCF IDs.

## Atomic admission

The runner loads and validates every scoped fixture, verifies the profile's
scope, then computes every prediction on detached fixture values before opening
the profile's expectation artifact. Predictions are validated and frozen through
canonical encoding. Predictor mutation of its input fails admission.
The artifact's raw SHA-256 must match the explicit registration pin. Its schema,
profile/version identity, exact fixture-set digest, unique rows, and complete
row coverage must match. Each recorded prediction must equal its independently
recomputed prediction in canonical encoding. Missing, extra or duplicate rows
fail admission. Any mismatch rejects the entire profile; no adapter executes.

Pinned(E) and ValidDigest(E) are insufficient. Admission requires both plus
Predict_profile(F) == E[F] for every F in the exact registered set.
Admitted data is held as immutable encoded values; consumers receive copies.
No persistent admission cache survives fixture or artifact changes.
Execution plans must exactly cover admitted check identities before any adapter
runs. Adapter inputs contain challenge data only, never admitted expectations.

## Results and errors

Top-level `totals` always emits PASS, FAIL, INVALID_FIXTURE and UNSUPPORTED.
Unknown profiles or adapters yield UNSUPPORTED; unknown adapters retain every
planned row. Structurally malformed registered fixtures yield INVALID_FIXTURE.
A valid fixture with untrustworthy expectations is **not** called malformed:
internal PROFILE_ERROR identifies the cause, mapped to UNSUPPORTED because no
trustworthy oracle is available. It emits one diagnostic row for the blocked
profile and admits zero expectations. Counts therefore describe report rows,
not a claim that every fixture in a blocked profile was individually executed.
All such conditions cause nonzero CLI exit. `--profile` selects a registered ID;
`--output` writes the structured report, including all four counts.
Execution exceptions retain internal RUNNER_ERROR, counted as top-level FAIL.
The legacy evidence.counts remains for existing mutation tooling; new consumers
must use totals. PASS denotes benchmark agreement, not artifact authorization.

## Independence and prove-can-fail

Predictors must not read the expectation artifact, call the adapter under test,
or choose expected output from fixture-ID naming conventions. Static trusted
code review is part of registration: Python callables are not a security sandbox.
The runtime denies direct identical predictor/adapter functions, separates input
channels, computes predictions before artifact access, and detects input mutation.
It cannot honestly prove arbitrary Python closures or filesystem reads independent.
EXP-M5 is therefore a provenance-class review rule, not a fabricated mutation kill.

`tools/prove_expectations_can_fail.py` runs EXP-M1 (repinned recorded-value
substitution), EXP-M2 (valid fixture modification with stale binding), EXP-M3
(disabled prediction equality), and EXP-M4 (disabled atomic admission barrier).
M1/M2 require their exact admission guard to reject the attack; M3/M4 require
the mapped architecture assertion to fail after normal loading and execution.
Collateral failures are listed separately. Setup/import/syntax errors are
VACUOUS; unapplied source targets are NOT_APPLIED; unrelated assertion failures
cannot substitute for the mapped failure. The original 12 mutation mappings and
outcomes are unchanged and run separately.

## Non-goals

No arbitrary runtime plugins, network loading, package installation, external
adapters, automatic inference of domain semantics, or RSI protected-relation
rule changes. A trusted predictor's correctness and independence need source
review and domain evidence; registration alone does not establish either.
General fixture-ID migration, directory discovery, and legacy mutation registry
extensibility remain separate Extension Contract work.
