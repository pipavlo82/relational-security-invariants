# H1 predictor / adapter independence audit

Research-only on main at `45a00875702ed733dfe77c8ba7c30e9a9a93644c`. Seven real domains plus legacy; ERC-8380 remains blocked. Exact local code, pinned evidence bundles, source maps, registry, tests and reports were inspected. No new upstream claim is made. All 389 tracked-file hashes are in the JSON report. No prior wording or implementation was edited.

**NO to an unqualified independent-oracle claim.** All seven domain predictors have separate actual/prediction code paths. That does not establish independent authorship, data-source authority, or freedom from shared interpretation error. Current bounded validation results remain intact; this audit did not establish actual invalidity.

Rubric: 0 no independence, 1 limited/shared-origin route, 2 separate implementation with shared assumptions, 3 strong separation in the specific bounded dimension. Third-leg 1 is local assertion/oracle-generated golden evidence, 2 is source vectors/KATs/definition evidence with shared-origin caveats, 3 requires independently originated full-relation evidence. Total 13-15 STRONG, 9-12 MODERATE, 5-8 WEAK, 0-4 NOT INDEPENDENT. These are review judgments, not confidence probabilities. Author evidence is UNKNOWN for every pair and is not assigned an optimistic numeric score. Same language scores NOT INDEPENDENT for language only. No complete full-relation third leg or common-mode resistance earns 3.

| Domain | Code | Algorithm | Source | Third leg | Common-mode | Total /15 | Assessment |
|---|---:|---:|---:|---:|---:|---:|---|
| Crystal Receipt | 3 | 2 | 1 | 2 | 2 | 10 | MODERATE |
| RVR digest-binding | 3 | 1 | 1 | 2 | 2 | 9 | MODERATE |
| TSEI serializer/adoption | 2 | 1 | 1 | 2 | 2 | 8 | WEAK |
| PQ policy/as-of | 3 | 1 | 1 | 2 | 2 | 9 | MODERATE |
| TAS context/dispatch | 3 | 2 | 1 | 1 | 2 | 9 | MODERATE |
| ConsultEscrow | 3 | 3 | 1 | 2 | 2 | 11 | MODERATE |
| verify-layer | 3 | 2 | 1 | 2 | 2 | 10 | MODERATE |
| Legacy/synthetic | 2 | 1 | 0 | 1 | 1 | 5 | WEAK |

| Domain | Code | Language | Algorithm | Data source | Helper | Author | Path | Oracle |
|---|---|---|---|---|---|---|---|---|
| Crystal Receipt | STRONG | STRONG | MODERATE | WEAK | MODERATE | UNKNOWN | MODERATE | MODERATE |
| RVR digest-binding | STRONG | NOT INDEPENDENT | WEAK | WEAK | MODERATE | UNKNOWN | MODERATE | MODERATE |
| TSEI serializer/adoption | MODERATE | MODERATE | WEAK | WEAK | MODERATE | UNKNOWN | MODERATE | WEAK |
| PQ policy/as-of | STRONG | NOT INDEPENDENT | WEAK | WEAK | MODERATE | UNKNOWN | MODERATE | MODERATE |
| TAS context/dispatch | STRONG | STRONG | MODERATE | WEAK | MODERATE | UNKNOWN | MODERATE | MODERATE |
| ConsultEscrow | STRONG | STRONG | STRONG | WEAK | MODERATE | UNKNOWN | STRONG | MODERATE |
| verify-layer | STRONG | STRONG | MODERATE | WEAK | MODERATE | UNKNOWN | STRONG | MODERATE |
| Legacy/synthetic | MODERATE | NOT INDEPENDENT | WEAK | NOT INDEPENDENT | WEAK | UNKNOWN | WEAK | WEAK |

## Crystal Receipt

Language pairing: Python / source TypeScript.

Predictor modules: `profiles/crystal_receipt/expectation.py`. Actual modules: `adapters/crystal_receipt/execute.mjs`, `adapters/crystal_receipt/model.py`, `adapters/crystal_receipt/__init__.py`.

Derivation: SPEC-derived equality/json.dumps vs snapshotCounterfactualSemanticJson + canonicalize + relation.observed.

Shared helper nodes: `rsi/codec.py`, `runner/expectation_contract.py`, `runner/execution.py`, `runner/relation_runtime.py`, `profiles/crystal_receipt/source.py`, `profiles/crystal_receipt/relation.py`. These include validation/admission dependencies, not necessarily shared semantic evaluator calls.

Risk: Same chosen semantic-object projection and external metadata exclusion; a shared scope mistake outside frozen examples is invisible. Existing frozen expected rows and named semantic assertions detect subsequent wrong behavior on covered cases; agreement alone cannot validate the original interpretation.

Third leg: PARTIAL. Frozen SPEC, V-SEM-MANIFEST-INVARIANT, mutation vector, direct canonical-string assertions.

Hardening: Independently derive canonical-byte vectors from SPEC; review projection separately. Recommended wording: "separately implemented expectation predictor for the pinned Crystal Receipt scope". Author independence UNKNOWN.


## RVR digest-binding

Language pairing: Python / source Python.

Predictor modules: `profiles/rvr/expectation.py`. Actual modules: `adapters/rvr/model.py`, `adapters/rvr/__init__.py`.

Derivation: Independent functions implementing same Rule/Scope predicates, canonical JSON/SHA256; adapter execs amendment_gate and verdict_binding_gate.

Shared helper nodes: `rsi/codec.py`, `runner/expectation_contract.py`, `runner/execution.py`, `runner/relation_runtime.py`, `profiles/rvr/source.py`, `profiles/rvr/relation.py`. These include validation/admission dependencies, not necessarily shared semantic evaluator calls.

Risk: Same layer/status interpretation; both could originally mistake retained A for resolution or signed_digest equality for authentication. Existing frozen expected rows and named semantic assertions detect subsequent wrong behavior on covered cases; agreement alone cannot validate the original interpretation.

Third leg: PARTIAL. 14 source vectors and explicit unsupported/layer assertions; shared upstream provenance.

Hardening: Third-party obligation table and definition-derived commitment bytes. Recommended wording: "separately implemented expectation predictor for the pinned RVR digest-binding scope". Author independence UNKNOWN.


## TSEI serializer/adoption

Language pairing: Python / TypeScript producer + Python checker/wrapper.

Predictor modules: `profiles/tsei/expectation.py`. Actual modules: `adapters/tsei/encoder.mjs`, `adapters/tsei/model.py`, `adapters/tsei/__init__.py`.

Derivation: json.dumps/hash + hard-coded chronology membership vs TS encoder, source record validator and pinned record/chronology.

Shared helper nodes: `rsi/codec.py`, `runner/expectation_contract.py`, `runner/execution.py`, `runner/relation_runtime.py`, `profiles/tsei/source.py`, `profiles/tsei/relation.py`. These include validation/admission dependencies, not necessarily shared semantic evaluator calls.

Risk: Shared exact snapshot whitelist; predictor mechanism_active=True relies on admissible scope. Same misread adoption/introduction boundary can evade pair comparison. Existing frozen expected rows and named semantic assertions detect subsequent wrong behavior on covered cases; agreement alone cannot validate the original interpretation.

Third leg: PARTIAL. 48 serializer vectors, fixed digests and Git/record evidence; chronology interpretation still shared.

Hardening: Independent Git-parent/record chronology reconstruction and boundary truth table. Recommended wording: "separately implemented expectation predictor for the pinned TSEI serializer/adoption scope". Author independence UNKNOWN.


## PQ policy/as-of

Language pairing: Python / source Python.

Predictor modules: `profiles/pq/expectation.py`. Actual modules: `adapters/pq/model.py`, `adapters/pq/__init__.py`.

Derivation: Sorted governing-binding obligations vs pinned cutoff_enforce.admit/resolve_in_force and deep_recompute.

Shared helper nodes: `rsi/codec.py`, `runner/expectation_contract.py`, `runner/execution.py`, `runner/relation_runtime.py`, `profiles/pq/source.py`, `profiles/pq/relation.py`. These include validation/admission dependencies, not necessarily shared semantic evaluator calls.

Risk: Same supplied anchored/valid flags, history and cutoff interpretation; absent independent anchor or signature truth. Existing frozen expected rows and named semantic assertions detect subsequent wrong behavior on covered cases; agreement alone cannot validate the original interpretation.

Third leg: PARTIAL. 21 source policy vectors and direct historical/unsupported assertions; common source lineage.

Hardening: Definition-derived cutoff equality/revocation/as-of boundary cases. Recommended wording: "separately implemented expectation predictor for the pinned PQ policy/as-of scope". Author independence UNKNOWN.


## TAS context/dispatch

Language pairing: Python / source TypeScript + controlled JS ports.

Predictor modules: `profiles/tas/expectation.py`. Actual modules: `adapters/tas/execute.mjs`, `adapters/tas/model.py`, `adapters/tas/__init__.py`.

Derivation: Tuple/address/membership obligations vs pinned gate/service/manifest with controlled resolver and SDK invoke port.

Shared helper nodes: `rsi/codec.py`, `runner/expectation_contract.py`, `runner/execution.py`, `runner/relation_runtime.py`, `profiles/tas/source.py`, `profiles/tas/relation.py`. These include validation/admission dependencies, not necessarily shared semantic evaluator calls.

Risk: Same accepted/current/member records and getTask projection; no independent context producer or actual SDK execution. Existing frozen expected rows and named semantic assertions detect subsequent wrong behavior on covered cases; agreement alone cannot validate the original interpretation.

Third leg: PARTIAL. Pinned production source and direct dispatch/member assertions; no full external third leg.

Hardening: Independent manifest-to-call-envelope vectors and alternate membership input producer. Recommended wording: "separately implemented expectation predictor for the pinned TAS context/dispatch scope". Author independence UNKNOWN.


## ConsultEscrow

Language pairing: Python integer crypto / Solidity on JS EVM.

Predictor modules: `profiles/consult_escrow/expectation.py`, `profiles/consult_escrow/crypto.py`. Actual modules: `adapters/consult_escrow/execute.mjs`, `adapters/consult_escrow/model.py`.

Derivation: Keccak/secp256k1 and state predicates vs source bytecode/ecrecover/storage/transfer execution.

Shared helper nodes: `rsi/codec.py`, `runner/expectation_contract.py`, `runner/execution.py`, `runner/relation_runtime.py`, `profiles/consult_escrow/source.py`, `profiles/consult_escrow/relation.py`. These include validation/admission dependencies, not necessarily shared semantic evaluator calls.

Risk: Same job/result/signature fixture and setup projection; missing release scenarios can escape both. Unbound amount/recipient signature scope must remain explicit. Existing frozen expected rows and named semantic assertions detect subsequent wrong behavior on covered cases; agreement alone cannot validate the original interpretation.

Third leg: PARTIAL. Keccak KATs, fixed signatures, source contract; EVM is actual leg, not automatically a third full oracle.

Hardening: Externally generated EIP-191 recovery and job-state golden traces. Recommended wording: "separately implemented expectation predictor for the pinned ConsultEscrow scope". Author independence UNKNOWN.


## verify-layer

Language pairing: Python MPT/RLP/Keccak / source JS EthereumJS trie.

Predictor modules: `profiles/verify_layer/expectation.py`, `profiles/verify_layer/oracle.py`. Actual modules: `adapters/verify_layer/execute.mjs`, `adapters/verify_layer/model.py`, `adapters/verify_layer/__init__.py`.

Derivation: Custom Python nibble/path/leaf obligations vs JS verifier with offline RPC replay.

Shared helper nodes: `rsi/codec.py`, `runner/expectation_contract.py`, `runner/execution.py`, `runner/relation_runtime.py`, `profiles/verify_layer/source.py`, `profiles/verify_layer/relation.py`. These include validation/admission dependencies, not necessarily shared semantic evaluator calls.

Risk: Same supplied proof/header and trust projection; no canonical header verification. Shared absence/root-first interpretation needs broader trie corpus. Existing frozen expected rows and named semantic assertions detect subsequent wrong behavior on covered cases; agreement alone cannot validate the original interpretation.

Third leg: PARTIAL. Real supplied proof, Keccak KATs and direct root/account/balance assertions; no independent authoritative header.

Hardening: External inclusion/non-inclusion/embedded-node vectors and separate trust-tier obligations. Recommended wording: "separately implemented expectation predictor for the pinned verify-layer scope". Author independence UNKNOWN.


## Legacy/synthetic

Language pairing: Python / Python messaging and SQLite models.

Predictor modules: `profiles/synthetic.py`, `rsi/oracle.py`. Actual modules: `adapters/generic/model.py`, `adapters/messaging/model.py`, `rsi/wire.py`.

Derivation: rsi.oracle predicates vs separate adapters; inspect vs wire.valid_signature use same cryptography and codec.

Shared helper nodes: `rsi/codec.py`, `runner/expectation_contract.py`, `runner/execution.py`, `runner/relation_runtime.py`. These include validation/admission dependencies, not necessarily shared semantic evaluator calls.

Risk: Generator imports oracle to create golden rows; shared codec/digest/crypto and finite-model conventions can agree on same original error. Existing frozen expected rows and named semantic assertions detect subsequent wrong behavior on covered cases; agreement alone cannot validate the original interpretation.

Third leg: PARTIAL. Contract and direct scenario assertions; expected artifact is oracle-generated, not independent origin.

Hardening: Definition-derived finite truth table plus alternative codec/crypto vectors. Recommended wording: "separately implemented expectation predictor for the pinned Legacy/synthetic scope". Author independence UNKNOWN.

## Shared constants, artifacts and hidden conventions

TSEI predictor RECORD_IDENTITY plus hard-coded producer/landed commits correspond to the adapter's record and chronology. PQ HISTORY_SHA256 and the SLH-DSA literal correspond to the same pinned history/artifact read by actual. These identity commitments are not copied expected rows, but they share origin and scope. RVR separately reproduces source canonical JSON/SHA256 and obligations. TAS repeats the selected getTask target/tool and tuple normalization. Crystal repeats the source semantic projection and accepted-snapshot vocabulary. None is an independent source of authority merely because constants are duplicated.

CE crypto.py and VL oracle.py duplicate Keccak RC/ROT constants and similar permutation structure across predictors. They do not import each other's helper and the JS/EVM actual paths do not call that Python implementation. This is cross-predictor correlation and should be backed by external KATs, not represented as independent crypto authorship.

rsi.codec controls transport, normalization, digesting, and comparison. A common defect can affect both inputs and equality. Source.py pin checks, relation.validate_inputs/validate_outputs, safe_path, plan and atomic admission are shared gates. A wrongly narrowed input domain can hide a missing counterexample. TSEI mechanism_active=True relies on whitelisted snapshots; PQ rejects equal anchor times; CR has a narrow accepted semantic-object subset. These limitations must stay visible.

Relation interpreters may call adapters, but predictors inspected here do not call those interpreters. Direct function-identity checks only catch direct aliasing; wrappers/dynamic execution are not sandboxed. Static substring tests and expectation-file deletion tests establish selected dependency properties, not universal inability to read ambient files. No shared domain evaluation function was found computing both real-domain outputs.

runner/execution.py copies local_validity from admitted reference rows. It is not a second independent actual-side validity measurement. Real profiles generally set True after shape/scope validation; do not count this as dual local validation.

Legacy tools/generate_fixtures.py imports rsi.oracle to generate expected rows; frozen goldens therefore share oracle origin. Both adapter models and oracle use rsi.codec and cryptography Ed25519. Separate predicate wrappers, SQLite state transitions and direct tests still provide useful discrimination. Fixture identifiers do not supply expected truth to predict(), but fixture generation and predictor share the finite model and operation conventions.

## Common-mode experiment H1-E1

Only in-memory callables were replaced: both TSEI prediction and actual annotation changed authority_validation.status from UNSUPPORTED to SUPPORTED. Pair-only outputs agreed. The real pipeline with unchanged expected artifact rejected all seven rows through PROFILE_ERROR:PREDICTION_MISMATCH before adapter execution (zero calls, no admissions). Research classification ADMISSION_BLOCKED, not a new KILLED or COMMON_MODE_SURVIVED pipeline result.

Frozen rows are a temporal guard against later dual code drift. They are not necessarily a third independently originated oracle. An original shared mistake, or jointly revised code/goldens/assertions, can survive despite byte pins. Current explicit semantic assertions would catch the named example errors on covered cases; this audit does not claim those examples silently pass the present full suite.

## Highest-value hardening

1. Definition-derived third-leg vectors with provenance and separate review. Highest breadth, medium cost: start canonical snapshot bytes and TSEI chronology, then cutoff equality and RVR layer obligations. Freeze independent expected bytes/statuses before implementation.
2. Common-mode research experiments and golden-origin review. Medium cost, broad risk reduction: distinguish later dual-code drift (admission should block) from originally shared-oracle errors; test without changing result/mutation taxonomy.
3. External clean-room reproduction plus shared codec/crypto KATs. First and only recommended candidate: **Crystal Receipt semantic-snapshot subset**. Compact source/spec/vectors, real mirror-positive, no blockchain/proof transport. Supply normative artifacts and inputs, not current implementation code; ensure public-source accessibility without private RSI dependencies.

Strongest current separation: ConsultEscrow, then Crystal/verify-layer for different reasons. Weakest real-domain score: TSEI chronology; legacy is weakest overall. RVR/PQ reuse the same source policy algorithms in the same language; TAS depends on controlled ports. No ranking of authors or projects is implied.

Global wording: "separately implemented expectation predictor". Add the exact source/language/path and bounded scope. Claim independent authorship or independent semantic origin only with separate evidence. Existing TAS/VL caveats are substantially accurate; broad independent-oracle wording should be qualified, not used to retract valid conformance results.

## Validation

Fresh baseline: 430 tests PASS and 430 PASS under python -O. All 85 conformance checks PASS, other top-level baseline statuses zero. Before/after and preceding-phase outcome reports are byte-identical. All 61 mutations freshly KILLED; SURVIVED/VACUOUS/NOT_APPLIED zero. Every mutation record exactly matches the previous baseline (diff 0). All 389 tracked hashes and all prior research reports match. Anti-coupling remains PASS, semantic exceptions added zero. The full suites ran once on unchanged code; conformance was repeated after research generation rather than unnecessarily repeating all suites. Six new H1 research files only; no code, external changes, commit or push. Working tree has these six plus eleven prior untracked ERC-8380 reports; no tracked changes.


## Concrete shared preprocessing in PQ vector tests

`tests/test_pq.py:test_source_vector_reproduction` calls the source `apply_revocations` once and supplies its output to both source `admit` and the Python predictor. It also sets `snapshot_key` from actual `resolved_pq_pubkey`; the compared predictor output is the policy object. This demonstrates neither independent revocation preprocessing nor independent snapshot selection. Fixed vector expected fields remain a partial third leg. This is a precise test-evidence limitation, not invalidation of the registered policy/as-of scope. Add a separately derived pre/post-revocation history before claiming that preprocessing independently validated.


## Per-domain wording and dependency summary

| Domain | Adapter / predictor language | Shared helpers and source | Derivation route | Common-mode risk | Third leg | Score | Wording accuracy / recommendation |
|---|---|---|---|---|---|---|---|
| Crystal Receipt | Python / source TypeScript (predictor first) | codec, admission and scope validation; same pinned fixture/source interpretation | SPEC-derived equality/json.dumps vs snapshotCounterfactualSemanticJson + canonicalize + relation.observed | Same chosen semantic-object projection and external metadata exclusion; a shared scope mistake outside frozen examples is invisible | PARTIAL | 10/15 | code/path separation supported; author/oracle independence not established. separately implemented expectation predictor for the pinned Crystal Receipt scope |
| RVR digest-binding | Python / source Python (predictor first) | codec, admission and scope validation; same pinned fixture/source interpretation | Independent functions implementing same Rule/Scope predicates, canonical JSON/SHA256; adapter execs amendment_gate and verdict_binding_gate | Same layer/status interpretation; both could originally mistake retained A for resolution or signed_digest equality for authentication | PARTIAL | 9/15 | code/path separation supported; author/oracle independence not established. separately implemented expectation predictor for the pinned RVR digest-binding scope |
| TSEI serializer/adoption | Python / TypeScript producer + Python checker/wrapper (predictor first) | codec, admission and scope validation; same pinned fixture/source interpretation | json.dumps/hash + hard-coded chronology membership vs TS encoder, source record validator and pinned record/chronology | Shared exact snapshot whitelist; predictor mechanism_active=True relies on admissible scope. Same misread adoption/introduction boundary can evade pair comparison | PARTIAL | 8/15 | code/path separation supported; author/oracle independence not established. separately implemented expectation predictor for the pinned TSEI serializer/adoption scope |
| PQ policy/as-of | Python / source Python (predictor first) | codec, admission and scope validation; same pinned fixture/source interpretation | Sorted governing-binding obligations vs pinned cutoff_enforce.admit/resolve_in_force and deep_recompute | Same supplied anchored/valid flags, history and cutoff interpretation; absent independent anchor or signature truth; source-vector tests share apply_revocations preprocessing and use actual snapshot_key | PARTIAL | 9/15 | code/path separation supported; author/oracle independence not established. separately implemented expectation predictor for the pinned PQ policy/as-of scope |
| TAS context/dispatch | Python / source TypeScript + controlled JS ports (predictor first) | codec, admission and scope validation; same pinned fixture/source interpretation | Tuple/address/membership obligations vs pinned gate/service/manifest with controlled resolver and SDK invoke port | Same accepted/current/member records and getTask projection; no independent context producer or actual SDK execution | PARTIAL | 9/15 | code/path separation supported; author/oracle independence not established. separately implemented expectation predictor for the pinned TAS context/dispatch scope |
| ConsultEscrow | Python integer crypto / Solidity on JS EVM (predictor first) | codec, admission and scope validation; same pinned fixture/source interpretation | Keccak/secp256k1 and state predicates vs source bytecode/ecrecover/storage/transfer execution | Same job/result/signature fixture and setup projection; missing release scenarios can escape both. Unbound amount/recipient signature scope must remain explicit | PARTIAL | 11/15 | code/path separation supported; author/oracle independence not established. separately implemented expectation predictor for the pinned ConsultEscrow scope |
| verify-layer | Python MPT/RLP/Keccak / source JS EthereumJS trie (predictor first) | codec, admission and scope validation; same pinned fixture/source interpretation | Custom Python nibble/path/leaf obligations vs JS verifier with offline RPC replay | Same supplied proof/header and trust projection; no canonical header verification. Shared absence/root-first interpretation needs broader trie corpus | PARTIAL | 10/15 | code/path separation supported; author/oracle independence not established. separately implemented expectation predictor for the pinned verify-layer scope |
| Legacy/synthetic | Python / Python messaging and SQLite models (predictor first) | codec, admission and scope validation; same pinned fixture/source interpretation | rsi.oracle predicates vs separate adapters; inspect vs wire.valid_signature use same cryptography and codec | Generator imports oracle to create golden rows; shared codec/digest/crypto and finite-model conventions can agree on same original error | PARTIAL | 5/15 | code/path separation supported; author/oracle independence not established. separately implemented expectation predictor for the pinned Legacy/synthetic scope |


Scoring caveat: both paths must evaluate the SAME concrete input and normative relation. Sharing that input or standard Keccak constants is necessary and is not itself a defect. The source/algorithm scores measure independent derivation/provenance routes and common interpretation exposure, not a requirement to change the specification or choose a different hash algorithm. Strong computational separation also does not validate a supplied authority/anchor assumption.
