# Relation Profile Contract v0.1 implementation

## Outcome

Generic Option B is implemented alongside the frozen legacy path. No external adapter/corpus or external repository change was made. The current synthetic model exposed an overfit assumption when confronted with the first real source-defined relation. This change removes that universal proof/policy/state requirement without weakening RSI's core invariant.

Base main: `05f3853756ad9deb0e5d08d54dfdfd462652a801`. Repository: private `pipavlo82/relational-security-invariants`. The implementation commit is the commit containing this report; its exact SHA and post-push CI result are reported separately to avoid a self-referential commit hash.

## Validation

| Gate | Before | After |
|---|---:|---:|
| Full tests | 150 | 200 |
| Python -O tests | 150 | 200 |
| Legacy checks PASS | 36 | 36 |
| FAIL / INVALID_FIXTURE / UNSUPPORTED | 0 / 0 / 0 | 0 / 0 / 0 |
| Legacy/expectation mutations KILLED | 12 + 4 | 12 + 4 |
| Relation Profile mutations KILLED | 0 | 7 |
| Total KILLED | 16 | 23 |
| SURVIVED / VACUOUS / NOT_APPLIED | 0 / 0 / 0 | 0 / 0 / 0 |

All 36 old case records are exactly equal before/after, including expected/observed results and input digests. All 16 old mutation records are exactly equal. Whole report hashes differ because their implementation inventories include new files; this is explicitly separated from unchanged outcome records.

The deterministic JSON companion records SHA-256 before/after identities, 76 protected legacy file hashes, mutation mappings/collateral failures, new generic-module hashes and the complete changed-file inventory. The only edits to previously tracked files are README and CI. RSI-CORE, all five legacy schema files, fixtures, expectations, predictor, old generic runner/comparator and existing registries remain byte-identical.

## Implemented boundary

New files provide the minimal schema, immutable relation/profile declarations, exact-version registry, relation-aware coordinator, explicit legacy compatibility registration, test-only independent predictor and adapter, seven mapped mutations, implemented spec and preservation checker. The new CLI is `python -m runner.relation_runtime`.

The envelope uses `id` as the source identity to preserve the existing expectation byte-binding interface. Canonical namespaced identity remains in the unchanged corpus registration. Exact profile ID/version and relation ID are bound in the fixture. Required/optional slots and output contracts are profile-specific. Undeclared slots reject. Optional descriptor digest is identity metadata supplied by trusted registration; it is not automatic source/code verification.

The coordinator resolves and validates relation dependencies before atomically admitting expectations. It binds each planned check to its exact case inputs, then uses the unchanged adapter/expectation pipeline and comparator. Unknown profile/version/relation yields UNSUPPORTED; malformed profile inputs yield INVALID_FIXTURE. A valid execution mismatch yields FAIL. No profile-defined unresolved/effective-state value is promoted to a generic result.

## Mutation evidence

| Mutation | Mapped architecture property | Result |
|---|---|---|
| RP-M1 | Required profile resolution before admission/execution | KILLED |
| RP-M2 | Exact version, no implicit fallback | KILLED |
| RP-M3 | Static rejection of identifier-prefix behavior | KILLED |
| RP-M4 | Rich state is not collapsed into truth | KILLED |
| RP-M5 | Optional metadata cannot change protected equivalence | KILLED |
| RP-M6 | Proven historical binding governs anchored artifact | KILLED |
| RP-M7 | Independent expectation equality remains load-bearing | KILLED |

The initial RP-M1 test was too weak: checking UNSUPPORTED alone could be satisfied by a later adapter error. The final test checks non-admission and supplies a normal controlled adapter if the guard is bypassed. An initial broad RP-M1 mutant was correctly classified VACUOUS due to an unrelated error, then a narrower applied mutant exposed that assertion gap; neither was reported as a valid kill. The final mapped mutant produces an assertion failure without relying on setup/import/parse crashes. Collateral assertions are recorded separately in JSON. RP-M3 is a static architecture mutation, not a source-domain behavioral claim.

## Source evidence and readiness

The reviewed sources remain pinned in `relation-profile-evidence-closure-v0.json`: recompute-kit `15f7f59ac47b3358492bd5741143c418b5d657f5`, companion drafts `02fef5fd1f54eff9221b863cc746cb74a97f3220`, reference consumer `bdba0b674c2b2d301b75b4b23a33702b0bacfa64`, and RVR `287c0ea1c2578c1833405bc2476975f95addbada`. This implementation reused that review and did not re-audit or modify external sources.

RVR remains YELLOW: no amendment retains effective A; unresolved amendment state is neither ACCEPT nor substantive divergence resolution. Transition binding, verdict binding and resolution remain distinct. PQ remains YELLOW: supplied policy/cutoff vectors do not prove authenticated continuity; the inspected offline recomputation defers signature verification and has the documented ML-DSA/SLH-DSA labeling discrepancy. Earlier signing time alone does not establish historical validity.

**Crystal Receipt Phase 2A semantic gate: READY.** A future profile can accept an external audit_timestamp change while preserving semantic snapshot equivalence, using profile inputs without fake proof/policy/state, renaming to a synthetic relation, comparator changes or admission bypass. This is representability and an architecture-test result, not validation of an external adapter.

RVR, TSEI and PQ policy/cutoff profiles are architecturally representable. Full PQ authenticated-chain validation remains UNSUPPORTED. No external profile was implemented automatically.

## Limitations and retained assumptions

- Existing ASCII/integer canonical transport remains; arbitrary source JSON/float/binary transport is not silently accepted.
- Trusted Python code is not sandboxed. Indirect predictor/adapter self-validation, ambient filesystem reads and nondeterminism require review; direct alias/mutation checks are not a general proof of independence.
- Profile output contracts and the 1 MiB serialized result cap bound structured outputs; no universal state or claim vocabulary is imposed.
- Descriptor source closure is not automatically loaded or verified. The earlier design's mandatory descriptor proposal was narrowed to the optional pin expressly allowed by implementation authorization.
- Legacy finite relation/operation classes remain in the legacy compatibility profile, not the new schema.
- Previously uncommitted source/design/Phase 2A STOP reports are preserved as historical evidence and included in this private commit. Their old status statements describe the earlier review; they do not mean an external adapter has now been validated.
- CI checks both Python 3.12 and 3.13. The exact post-push workflow outcome is reported against the resulting commit.

## Reproduction

Run the full and optimized unittest suites, the existing shared mutation gate, `tools/prove_relations_can_fail.py`, and `tools/check_relation_contract.py` with the two mutation-report paths. Run the checker twice and compare bytes. It checks protected artifacts, exact old/new extension rows, deterministic execution and generic anti-coupling. Baseline command logs and exact pre/post structured reports are retained under ignored `artifacts/relation-profile-v0/` locally; reproducible hashes/results are included in the committed JSON companion.
