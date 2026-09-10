# Extension Contract v0.1 validation

Base main: `b881d2bee325dc86a8348e31d0d33e5b083cc3f4`.
Implementation: the commit containing this report. Its exact resulting SHA and
CI result are recorded after commit, avoiding a self-referential commit hash.

**Phase 2 architecture gate: READY.**

A future domain can add an adapter, static registration, fixture corpus,
independent expectation profile/predictor and mapped mutations without editing
RSI-CORE, the generic runtime/comparator, or result taxonomy. Architecture tests
exercise this with renamed synthetic challenges and the existing implementation;
no real external adapter or external-domain conformance claim was added.

| Check | Before | After |
|---|---:|---:|
| Tests | 93 | 150 |
| Optimized tests | 93 | 150 |
| Legacy fixture files | 6 | 6 |
| PASS checks | 36 | 36 |
| FAIL / INVALID_FIXTURE / UNSUPPORTED | 0 / 0 / 0 | 0 / 0 / 0 |
| Legacy mutations KILLED | 12 | 12 |
| Expectation mutations KILLED | 4 | 4 |
| Native registry KILLED | not registered | 16 |

SURVIVED, VACUOUS and NOT_APPLIED are zero in both mutation gates and the native
combined registry. The four states are independently counted. Setup, pre-check,
import, syntax and teardown faults cannot become mapped kills; completed
collateral assertion failures are reported separately.

The core normative spec, original RBCF/result schemas, all six legacy fixtures,
old expectation artifact, predictor, and pinned Expectation Contract files are
byte-identical. All 36 complete ordered legacy case records are identical before
and after, and extension records contain these same case records with explicit
canonical identities. Direct adapter calls equal registry calls for every case.
All existing source patches and mapped checks are unchanged; the legacy catalogue
adds explicit target_adapter_id metadata and moves outside generic execution.

The original schemas have an empty diff. The separate registered-fixture schema
changes only its own schema identity, source-ID admissibility and request-slot
names/cardinality; all request values use the unchanged request definition.
Exact before/after projection values and every preservation digest are in the
[machine report](extension-contract-v0.1-validation.json).

Discovery validates pinned manifests and every declared fixture, rejects missing
or malformed files, global duplicate identities, undeclared JSON, empty registries
and filesystem links. Explicit nested corpora are supported. Namespace, profile,
adapter and mutation registration order has no semantic effect. Unknown adapters
and profiles remain visible as UNSUPPORTED. One invalid expectation set blocks
all fixtures using that profile without calling them malformed.

Validation covered registration/schema/discovery/registry tests, all original
checks, both original mutation gates, all 16 registered mutations, full and
optimized suites, unchanged fixture generation, static anti-coupling checks,
exact hash/outcome comparison and deterministic runtime/architecture reruns.
The combined mutation report is bound to the exact implementation source hashes.
CI runs the same extension checks on Python 3.12 and 3.13.

Remaining boundary: readiness is architectural. Real-domain evidence, predictor
independence and whether each real relation fits the frozen model still require
Phase 2 validation. Legacy compatibility-only corpus and patch mappings remain
explicit outside generic runtime logic. No identifiers confer semantics or code
authority. No external repository was modified.
