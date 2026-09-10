# Extension Contract v0.1

**Extensibility must not create a second path for semantics.**

**registration != authority**

External domains may supply trusted adapters and independent expectation
predictors. All execution uses the existing Expectation Contract admission and
exact observation comparator. A manifest selects registered objects; it cannot
load code, authorize an artifact, or establish an expectation by declaration.

## Normative identity boundary

The core runtime MUST NOT infer semantics from identifiers: fixture ID,
namespace, adapter ID, profile ID, mutation ID, file path or directory name.
They select registered objects only. They imply no protected relation, authority,
expected result, domain semantics, policy or security claim. Syntax checks and
path-containment checks do not confer semantic meaning.

Canonical fixture identity is `namespace:local_id`. Namespace uses
`[a-z0-9][a-z0-9._-]{0,63}`; local_id uses
`[A-Za-z0-9][A-Za-z0-9._-]{0,127}`. Both are nonempty ASCII. Full IDs are globally
unique within an execution. Equal local IDs in distinct namespaces are allowed.
Duplicates fail closed before any adapter runs; registration order is irrelevant.

Legacy files keep internal IDs unchanged. Manifest `fixture_id` is canonical
(`core:RSI-001`); `fixture_source_id` preserves the file's `RSI-001`. Only explicit
registration maps these identities. No fixture file is rewritten. Source IDs and
check IDs remain opaque profile-local keys in the pinned expectation artifact.
Canonical IDs own all extension registry/report records.

## Corpus registration and deterministic discovery

`runner/fixture_registry.py` registers trusted `Corpus` records: corpus_id,
manifest_path, manifest_digest, and a statically supplied fixture validator.
`schema/fixture-corpus.v0.schema.json` documents `rsi-fixture-corpus.v0`:
corpus_id, namespace, fixture_directory, and nonempty fixtures. Each fixture
entry declares fixture_id, fixture_source_id, path, expectation_profile_id and
adapter_bindings. The latter maps explicit profile execution-plan slots to
registered adapter IDs. It permits multiple targets without rewriting old files.
Neither protected_relation nor expected outcomes are duplicated into manifests.

Metadata uses the existing canonical ASCII/integer JSON serializer. The manifest
SHA-256 is pinned by trusted composition data. Unknown fields, duplicate JSON
keys, malformed declarations, duplicate corpus IDs, duplicate full fixture IDs,
duplicate paths within a corpus, escaped paths, and non-JSON fixture paths fail.
The manifest's declared namespace must agree syntactically with full fixture IDs.

An empty corpus registry fails closed. Filesystem links/junctions encountered
during scanning fail explicitly, so aliases cannot hide undeclared JSON.
Only declared corpora are scanned. All JSON files (case-insensitive suffix) below
a registered directory, including nested directories, must be declared by a
validated registered corpus. Explicit nested corpora own their declared files;
parent scanning neither ignores undeclared files nor rejects declared child corpora. Undeclared
JSON causes an explicit corpus error; no adapter executes after any corpus/config
error. Non-JSON files are not fixtures. Missing or malformed declared files remain
visible as INVALID_FIXTURE. Valid siblings of an incomplete expectation profile
are UNSUPPORTED because atomic admission cannot occur. Corpora, declarations and
final rows are sorted explicitly. A changed manifest needs a new reviewed pin;
updating a pin alone still does not establish expected outcomes.

## Schema compatibility

The original RBCF and result schemas remain byte-identical. A separate
`schema/registered-fixture.v0.schema.json` projects the reference fixture schema
with exactly these extension-only differences:

1. `$id` names the new wrapper.
2. `/properties/id` accepts a restricted source identity instead of six fixed IDs.
3. `/properties/cases/items/properties/requests` accepts one or more named request
   slots instead of two fixed adapter keys. Every value uses the unchanged
   `$defs/request` schema.

Every other field, relation/operation enum, request definition, result, proof and
state constraint is identical. No protected-relation rule, local-validity field,
case role or expected outcome changes. Tests prove the exact projection diff.
The synthetic profile additionally retains the unchanged stricter corpus check.
A future trusted profile validator may validate adapter evidence, but may not
redefine RSI relations or silently add semantic fields to this frozen model.

## Adapter registration

`runner/adapter_registry.py` registers adapter_id, version, supported_profiles
and a trusted evaluator. Duplicate IDs fail closed. IDs resolve by exact lookup;
no reflective discovery, arbitrary imports, network loading or package installs.
Modern registrations set contextual=True for `evaluate(challenge, context)`;
context contains adapter identity/version and expectation profile identity only,
never expected outcomes. Detached copies protect challenge/context boundaries.
The explicit contextual=False compatibility convention wraps existing one-argument
adapters; tests prove all 36 direct and registered results identical.
Unsupported capability or unknown adapter yields UNSUPPORTED for every affected
planned check, retained in the report. Adapter registration order has no effect.

## Expectation binding and common execution

`runner/extension_runtime.py` performs discovery/validation, groups registrations
by explicit expectation_profile_id, checks exact registered fixture-scope equality,
and calls the unchanged `runner.execution.run_profile`. That is the single
admission/execution/comparison implementation also used by the legacy CLI.

The existing [Expectation Contract](expectation-contract-v0.md) remains normative:
independent prediction, pinned artifact and exact fixture-set binding, complete
row equality, atomic admission, and predictor/adapter independence. No partial
expectations become usable. Adapter-slot mappings and all execution plans must
validate before the first adapter in a profile runs. Unknown profile or a profile
which cannot admit its expectations emits UNSUPPORTED for every affected fixture.
A known profile's invalid expectations never make a valid fixture malformed.

Run `python -m runner.extension_runtime --output artifacts/extension.json` for the
native extension report. Trusted application composition lives in `extensions/`,
not in the core. The original `python -m rsi.run` remains a compatibility entry
point using the same comparator and produces unchanged legacy case records.

## Top-level result taxonomy

All four counts are emitted independently; no counts are derived by subtraction.
PASS: admitted expected observation equals actual observation.
FAIL: execution produced a valid structured observation which differs from the
admitted expected observation. PASS is conformance agreement, not authorization.
INVALID_FIXTURE: malformed/schema-invalid fixture. Corpus/config errors use the
same top-level count with distinct CORPUS_ERROR or REGISTRATION_ERROR diagnostics;
this does not label every otherwise-valid declared fixture malformed.
UNSUPPORTED: missing profile/adapter/capability, unavailable admitted oracle, or
unavailable completed evaluation. Execution exceptions preserve internal
RUNNER_ERROR in the unchanged case record and extension diagnostic EXECUTION_ERROR;
they are UNSUPPORTED, not a claimed semantic comparison failure. The legacy CLI's
historical RUNNER_ERROR/count convention remains available for compatibility.

A blocked profile emits one diagnostic row per registered fixture; successfully
planned profiles emit one row per check. Counts describe visible report rows.
Any corpus configuration error stops all execution; independent complete profiles
may still execute when another profile has a malformed fixture or unavailable oracle.

## Mutation registration and classification

`runner/mutation_registry.py` registers stable unique mutation_id, explicit
adapter/check-class target_id, mapped_check, trusted implementation, optional
applicability predicate and expected_failure_phase. Only decision, admission and
test assertion phases can be valid failure points. IDs never derive target behavior.
The implementation returns an explicit MutationTrace of application state,
phase-tagged check events, and setup/errors. Registration and execution are sorted.

Unknown target, false applicability, missing patch or absent mapped check is
NOT_APPLIED. Syntax/import/setup/pre-check/teardown errors are VACUOUS, even if a
later event appears to fail. A completed mapped check at its required phase is
KILLED only on FAIL; PASS is SURVIVED. Setup/teardown assertions cannot be declared
valid kill phases. Unrelated failures cannot substitute for the mapped check;
collateral completed failures are listed separately. A complete mapped failure
may coexist with collateral test assertions, as in the existing expectation tests.
All four mutation counts are independent and always present.

The 12 legacy source patches live in `extensions/legacy_mutations.py` and the four
expectation-contract attacks/enforcement mutants are statically registered by
`extensions/mutations.py`. Bridges retain the existing controlled execution tools
and expose their actual mapped events to the common classifier. Compatibility
reports keep their historical internal RUNNER_ERROR/OFF_TARGET categories; native
mutation reports use the four required states. No kill is inferred from labels.
`python tools/run_registered_mutations.py` runs the registry after an admitted
extension baseline. Adding a trusted mutation registration needs no core edit.

## Security properties and readiness

The runtime rejects ambiguous discovery and incomplete profile scope, uses exact
fixture bytes under existing expectation-set admission, and never supplies oracle
rows to adapters. Manifests cannot establish code trust or prediction correctness.
Trusted code review remains necessary for predictor independence; EXP-M5 remains
a provenance-class rule, not an invented mechanical kill.

Architecture tests register a new namespaced synthetic test corpus, independent
predictor/profile, and aliased existing implementation without any core edit.
They also exercise two namespaces sharing a local ID, changed identifiers,
unknown dependencies, tampering, order invariance and all four mutation states.
This establishes an architecture gate, not real-domain conformance evidence.
Future adapter implementation/registration, corpus, expectation profile/predictor
and mapped mutations can be added outside RSI-CORE, generic runtime/comparator
and result taxonomy. Phase 2 architecture gate: READY. Whether a particular real
relation maps to the unchanged model remains a Phase 2 empirical question.

## Non-goals

Arbitrary runtime plugins, executable manifests, network loading, dynamic package
installation, domain-specific core branches, new external adapters, automatic
fixture migration, new protected-relation semantics, public release or production
security certification. No external repository is required or modified.
