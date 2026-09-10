# Crystal H2 common-mode experiments

These are controlled local input-projection doubles, not edits to production
sources and not global RSI mutations. They wrap the unchanged TypeScript
actual and unchanged Python predictor with the same deliberately incorrect
assumption. The original input goes to C before either double executes.
No failing setup/import/schema event is called a common-mode catch.

H2-M1 projects external manifest bytes into an added semantic string in both
doubles. The timestamp-change and timestamp-removal inputs remain the
original source-vector inputs for C. A-prime and B-prime both report a changed
semantic identity; C preserves it by the definition's external-metadata rule.
The surrogate projection field is explicitly test-double instrumentation,
not a source-defined field or an additional Crystal profile/fixture.

H2-M2 projects the baseline semantic map onto the candidate in both doubles.
A-prime and B-prime both miss the retained-value substitution; C detects it.
Neither experiment changes the frozen expectations, mutates external source,
or claims that the production implementation currently has this bug.

| Experiment | Vector | Pair agrees | Pair semantic identity | C semantic identity | Classification |
|---|---|---|---|---|---|
| H2-M1 | CR-H2-G3 | True | False | True | COMMON_MODE_CAUGHT |
| H2-M1 | CR-H2-G4 | True | False | True | COMMON_MODE_CAUGHT |
| H2-M2 | CR-H2-G2 | True | True | False | COMMON_MODE_CAUGHT |

This establishes selected third-leg sensitivity to shared projection errors.
It does not establish author independence, resistance to every common-mode
bug, independent source authority, or exhaustive transport correctness.
A/B agreement alone would miss the modeled errors; the original frozen D
and existing named regression assertions can also catch later drift on
these cases. C adds a derivation route for origin confidence, not a claim
that D was otherwise powerless.
