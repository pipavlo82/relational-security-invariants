# Executable conformance

## Admission before execution

1. Verify exact manifest field set, six-id inventory, required files and raw pins.
2. Require byte-canonical stored JSON under rsi-json-ascii.v0.
3. Validate the closed Draft 2020-12 fixture/request contract; no network refs.
4. Recompute local signature validity and the reference observation from inputs.
5. Compare that to the detached oracle; a mismatch stops the run.
6. Require accepting controls, changed-byte mirror-positives and a discriminating negative.
   Check that the negative changes only its declared endpoint/schedule and that
   local validity is preserved except in the explicit invalid-authentication family.
7. Give each target a deep copy of the request only; validate returned shape.
8. Compare exact observation, including state and side effects, to the oracle.

## Finite coverage

| Family | Target checks (both adapters) | Input negative | Source mutant |
|---|---|---|---|
| RSI-001 | Ed25519 key == authorized subject key | change expected subject | remove subject guard |
| RSI-003 | no authoritative commit on failed auth | flip signature byte | commit candidate before verification |
| RSI-004 | one commit per observed revision | read/read/commit/commit | bypass revision compare/SQL condition |
| RSI-006 | signed scope == requested scope | change requested scope | remove scope guard |
| RSI-008 | signed, matching, authorized evidence | remove receipts | bypass evidence requirement |
| RSI-009 | same policy gate on four input paths | incompatible policy version | skip policy gate on import |

Six families, each with control, mutation and mirror-positive, each exercised
against both target domains = 36 evaluations. This is not 36 production bugs.
RSI-002,005,007,010,011,012 and general CORE-7 are not covered.

## Outcomes and exit codes

A completed exact comparison yields PASS or FAIL. An exception, unsupported
input, changed request, unavailable dependency or malformed observation yields
RUNNER_ERROR. `python -m rsi.run`: 0 all PASS; 1 completed FAIL(s); 2 any runner or
contract failure. A VIOLATED input is not a failed checker when correctly rejected.

## Prove-can-fail rules

The baseline must be 36/36. Apply a mutation in an isolated temporary checkout:
exactly one source match or NOT_APPLIED. Compile failure is VACUOUS. Runtime
exception, absent report, timeout or invalid output is RUNNER_ERROR. Only a
completed FAIL on the mutation's mapped negative case earns KILLED; other
failures are OFF_TARGET. A completed green run is SURVIVED. Killed-by cases are
measured from the run; collateral is retained and never silently counted as a
mapped kill. Console wording is diagnostic, never the classifier input.

The expected mapping in `tools/prove_can_fail.py` declares where a mutation is
supposed to fail. The report records where it actually failed. These are two
objects, not aliases. Four classifier controls require compile error->VACUOUS,
call exception->RUNNER_ERROR, absent patch->NOT_APPLIED, equivalent edit->SURVIVED.
A green full gate requires all 12 intended guard mutants KILLED and all four
classifier controls correct.

The unit suite also tests always-reject behavior, detached challenge boundaries,
oracle tampering after repinning, absent fixtures, strict numeric types, and
wrong-operation/wrong-scope/wrong-issuer/wrong-kind receipt evidence. It runs
under ordinary Python and `python -O`; security guards use no `assert` statement.

## Extending beyond the prototype

A real integration needs an exact target revision, a stable adapter contract,
observed state/effects rather than modeled ones, explicit missing prerequisites,
a compatible semantic oracle, accepting/mirror controls, an isolated negative
implementation control and a separate review. Do not count an added JSON file
as an integrated domain before those obligations execute.
