# Crystal H2 independence rescore

The H1 rubric is unchanged. Review judgment: **10/15 MODERATE -> 10/15
MODERATE**. More concrete evidence within a score band is useful without
manufacturing a numerical upgrade.

| Dimension | Before | After | Reason |
|---|---:|---:|---|
| Code independence | 3 | 3 | C imports only Node fs/crypto; separate parser and semantic token renderer; no A/B semantic helper. |
| Algorithm independence | 2 | 2 | Manual retained-pair derivation is separately implemented, but the same chosen flat projection and ordering rule remain shared interpretation. |
| Source independence | 1 | 1 | Same frozen source definition and vector origin; no independently authoritative source. |
| Third-leg evidence | 2 | 2 | Runnable definition-derived C now exists; H1 score 3 requires independently originated full-relation evidence. |
| Common-mode resistance | 2 | 2 | Both selected common-mode experiments caught; not complete full-relation resistance. |

Language: Python B differs from TypeScript A; JavaScript C shares Node/V8
with A. C shares neither rsi.codec nor an executable semantic helper with
A/B. The harness/admission and A/B still depend on RSI codec and validators;
a comparison-harness bug can still misstate agreement. Shared immutable
input bytes are intentional and are not shared executable truth.

Author independence: UNKNOWN. Procedural blindness: NOT ESTABLISHED;
existing predictor/source branches were inspected during H1. A definition
note and manual golden deductions preceded C implementation, and all C
results precede A/B/D computation in the comparison harness. That narrower
protocol is tested; it is not a clean-room authorship claim.

Allowed Crystal-only wording:

> Crystal Receipt semantic-snapshot validation now has three separately
> implemented derivation/execution legs, including a definition-derived
> clean-room reproducer that catches selected common-mode errors shared by
> the existing actual/predictor pair.

Here clean-room describes dependency/derivation separation, not procedural
blindness or independent authorship. Do not say fully independent. Other
RSI domains retain their H1 assessments and the conservative wording
separately implemented expectation predictor. Bounded prior semantic
validation claims remain intact.
