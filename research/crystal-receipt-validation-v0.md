# Crystal Receipt / ReceiptOS Phase 2A validation v0

## Result and scope

RSI admitted its first real external domain, Crystal Receipt / ReceiptOS, through the existing Relation Profile, Extension, and Expectation contracts without changing RSI core semantics.

Phase 2A is CLOSED for the source-backed semantic-snapshot scope implemented here, conditional on the implementation commit's post-push CI succeeding. This is not full ReceiptOS coverage or cross-domain validation. CR-RSI-003 and CR-RSI-004 remain explicitly unimplemented/UNSUPPORTED candidates, not hidden passing fixtures.

RSI base main: `30e13ba3a39915c91a607f70975c669ead7a231e`. Repository remains private. The resulting commit SHA and exact-head CI are reported separately; embedding this commit's own hash would be self-referential.

## Source identity

Canonical source repo: `https://github.com/pipavlo82/crystal-receipt`, main `45b46bf7df3a60b32583291f577a36bf19d22f00`. Live main was checked directly and has not advanced from the previous observation. Local source path exists at `C:/Users/msi/dev/crystal-receipt`; worktree branch `feature/tsei-spec-artifact-v0`, HEAD `46bed9ba8662ede63f0682ac6d2c93e52b6536cd`, tracked clean with the same 14 pre-existing untracked entries. No source content, checkout, branch, dependency installation or external repository was modified.

`crystal-receipt-source-map-v0.json` records every used/assessed path, exact commit, raw SHA-256, blob OID and source class. Five byte-identical canonical source files are pinned under `evidence/crystal-receipt/`; only the two original TypeScript production helpers execute. Their Node built-in dependency is explicit. Node 22.15.0 was used locally and is pinned in CI; type stripping is explicit and no runtime package/plugin installation is used.

Source pin artifact SHA-256: `17f072840b3dd50f23fafaadafe6ee8321b771f6c211e8af5bc95b17ee0229fb`.

## Executed fixtures

| Canonical fixture | Cases | Actual source observation | Conformance |
|---|---:|---|---|
| crystal-receipt:CR-RSI-001 | 2 | Control snapshots equal; one semantic value substitution leaves both snapshots accepted but changes canonical identity | 2 PASS |
| crystal-receipt:CR-RSI-002 | 2 | External audit_timestamp changed or removed; exact accepted semantic snapshot preserved | 2 PASS |

No fake proof, policy, state, signature or transition fields exist. The relation is source semantic-snapshot equivalence, not renamed context/provenance binding. The dependent claim is semantic identity equivalence only. The negative does not assert that the candidate artifact is malformed, unauthorized or rejected; it correctly denies inheritance of the baseline identity.

Every case traverses fixture registration, envelope validation, exact relation-profile resolution, profile input validation, independent expectation admission, adapter lookup, real source execution, unchanged generic comparison and unchanged top-level result taxonomy. Combined legacy + Crystal registration uses the same coordinator and gives 40 PASS.

The independent Python predictor derives canonical strings and equality from the frozen SPEC, separately from the actual TypeScript helpers and relation observation function. Artifact deletion tests show actual-side/profile interpretation does not require the expectation file. Patching actual-side behavior leaves expected results unchanged. A repinned tampered expectation row prevents admission of the entire two-fixture expectation set.

## Validation totals

| Gate | Before | After |
|---|---:|---:|
| Full unittest suite | 200 PASS | 229 PASS |
| python -O unittest suite | 200 PASS | 229 PASS |
| Legacy checks | 36 PASS | 36 PASS |
| Crystal checks | 0 | 4 PASS |
| Combined checks | 36 PASS | 40 PASS |
| Existing mutation kills | 23 | 23 |
| Crystal mutation kills | 0 | 3 |
| Total mutation kills | 23 | 26 |

FAIL / INVALID_FIXTURE / UNSUPPORTED are all zero for the executed conformance baseline. SURVIVED / VACUOUS / NOT_APPLIED are all zero for the successful final mutation gates. Omitted candidate assessments are separate and remain visible in the machine report.

Exact pre/post comparison found zero changes in all 36 legacy case records and all 23 prior mutation records. Full report source-inventory digests naturally change as files are added; this is not an outcome change. All 76 historical protected hashes plus four additive generic Relation Profile artifacts match, for 80 protected hashes. The only previously tracked files edited are CI and the three Crystal research reports. No runner, comparator, registry core, result taxonomy, RSI-CORE text or schema was edited.

Structured report reruns are byte-identical. Generic static checks contain no Crystal/ReceiptOS/audit_timestamp/snapshot/Lane K semantic branches. Exact file/hash evidence and observed rows are in `crystal-receipt-validation-v0.json`.

## Mutation discrimination

| Mutation | Controlled fault | Mapped decision | Result |
|---|---|---|---|
| CR-M1 | Bypass equality discrimination after both real source helpers execute | Relation-substitution negative must lose semantic identity | KILLED |
| CR-M2 | Changed external metadata incorrectly changes relation result | Mirror-positive must preserve identity | KILLED |
| CR-M3 | Promote identity using only accepted local snapshots | Accepted unequal snapshots must not inherit equivalence | KILLED |

Source mutations apply only in isolated RSI copies. Mapped tests first require successful source execution, admitted expectations and normal adapter results; setup/import/schema/source failures raise test ERROR and classify VACUOUS. Only the intended semantic assertion can establish KILLED. Collateral failures are recorded separately. No CR-M4 is claimed because no provenance fixture was implemented.

During implementation a composition attempt called a nonexistent AdapterRegistry.register method. It failed explicitly before conformance execution; composition was corrected to use the existing constructor API, without changing the registry. This setup error was not counted as a mutation kill or successful check.

## Uncovered candidates and limits

- CR-RSI-003: the inspected separate admission seam proves evidence/proof-root consistency and object identity. It is not treated as proof of a distinct provenance/context authority relation, and no admission adapter or independently derived admission oracle is included.
- CR-RSI-004: Lane K v1 is canonical, but its 12-process/120-evaluation schedule protocol was not executed. The inspected specification alone does not establish the requested weak-observation-preserving global-substitution negative. No graph/snapshot surrogate is used.
- Profile coverage is restricted to the concrete source-backed flat printable ASCII string artifacts. Wider finite-number, Unicode, nested/runtime object, accessor, proxy, cycle and array behavior remains outside this corpus. Unsupported forms are not silently normalized.
- Source code is immutable offline evidence during execution. An explicit live preflight detects upstream main drift and requires repin/revalidation; runtime does not fetch new code or silently adopt moving main.
- Independent implementations and constrained input channels are reviewed/tested, but trusted Python/Node execution is not an arbitrary-code/filesystem sandbox.
- No real-world provenance authority, signer, full ReceiptOS correctness or broader Trustless AI result is claimed.

## Reproduction and CI

Run `tools/verify_crystal_source.py --source-repo C:/Users/msi/dev/crystal-receipt` for the explicit read-only live preflight. Run `tools/run_crystal_receipt.py` (or `--include-legacy`), `tools/prove_crystal_can_fail.py`, both unittest modes and `tools/check_crystal_receipt.py --mutations <mutation-report>`. Compare repeated structured report bytes. The source helper runs from verified captured bytes staged inside RSI, not from the mutable external worktree.

Pre-change and post-change command logs, structured reports and exact hash inventories are retained locally under ignored `artifacts/crystal-phase2a/`. The committed reports contain reproducible source pins, protected hashes, actual/expected rows and mutation classifications. Post-push CI on Python 3.12 and 3.13 and final worktree status are checked against the resulting commit and reported in the completion response.
