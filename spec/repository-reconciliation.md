# Repository reconciliation - 2026-09-09

## One maintained implementation

`main` is the canonical working branch. Its existing two-target implementation is retained. The unrelated `codex/rsi-v0` prototype is retired as an active branch, with its complete commit retained as the second parent of this reconciliation. This is an explicit selection of one implementation, not a claim that the two codebases are equivalent or that their fixtures can be mixed.

No frozen release or public standard is created. The repository remains private and the existing license-decision-pending policy remains unchanged.

## Exact inputs reviewed

| Snapshot | Commit | Scope |
|---|---|---|
| Existing main, selected | `b0f93298453b3043765d4543c233fbb63647b11d` | Six families, three cases per family, two target adapters; 36 evaluations and 12 guard mutants. |
| Alternate prototype, retired | `fdffde495e6763a1282f0b7146207b7171238c06` | Six paired reference fixtures, six guard mutants, and 51 tests recorded in its evidence files. |

The repository existed before the alternate branch upload. Both commits are attributed to the owner's Git identity, but that does not identify which human or agent session created the earlier implementation. This reconciliation makes no claim about that provenance.

## Why main was selected

The selected implementation verifies a pinned corpus and separately derived oracle, validates adapter output against a closed observation schema, runs every family against both an in-memory messaging model and a SQLite journal model, and checks positive cases whose signed bytes change without changing meaning. Its CI also runs ordinary and optimized Python. These are concrete coverage advantages over the alternate minimal prototype.

The selected code is not declared universally superior. The alternate prototype has a real AES-GCM auth-before-commit example, a different fixture schema, explicit INVALID_FIXTURE/UNSUPPORTED result states, and different status/evidence modeling. Those contracts have not been silently spliced into the selected code.

Remaining differences from the initial request are explicit: the selected auth-before-commit case uses an invalid Ed25519 signature rather than ciphertext; missing confirmation evidence is UNVERIFIABLE; runner errors use RUNNER_ERROR rather than separate INVALID_FIXTURE/UNSUPPORTED counts; fixtures use cases plus a detached oracle rather than the original control/mutation object shape. Its CLI reports JSON to output files and diagnostics to the console. Addressing these interface differences is future implementation work, not an outcome of repository cleanup.

The license files also differed. Selecting main keeps its pending-license policy; the retired prototype's MIT file does not become the license of the selected tree.

## Independently reproduced verification

Using the declared dependencies `cryptography==46.0.4` and `jsonschema==4.26.0` on Python 3.12.14 / Windows:

| Check | Result |
|---|---|
| Definition-derived regeneration | PASS, byte-for-byte corpus match |
| Schema/corpus/oracle validation | 6 fixtures, 36 cases validated |
| Reference conformance | PASS=36, FAIL=0, RUNNER_ERROR=0 |
| Unit tests | 52 passed, 0 failures/errors, 0 skips |
| Optimized Python unit tests | 52 passed, 0 failures/errors, 0 skips |
| Guard mutants | KILLED=12, SURVIVED=0, VACUOUS=0, NOT_APPLIED=0, RUNNER_ERROR=0, OFF_TARGET=0 |
| Mutation classifier controls | 4/4 correct |

The existing GitHub CI for the reviewed base also completed successfully: [base CI run](https://github.com/pipavlo82/relational-security-invariants/actions/runs/34417335671). That is distinct from the local rerun and from CI on the new reconciliation commit.

Only README and research/reconciliation documentation change in this consolidation. Adapter code, schemas, fixtures, oracle, tests, dependencies and workflow remain byte-identical to the reviewed main. Research categories Established, Adjacent, Promising and Unverified are preserved explicitly; none is promoted to a novelty claim.

## History and recovery

Both original commits remain reachable through the reconciliation commit's parents. The retired prototype can be inspected at [its exact commit](https://github.com/pipavlo82/relational-security-invariants/tree/fdffde495e6763a1282f0b7146207b7171238c06); a separate live branch is unnecessary. No force-push or deletion of either commit is part of the reconciliation. New work starts from main and uses its documented commands and contracts.
