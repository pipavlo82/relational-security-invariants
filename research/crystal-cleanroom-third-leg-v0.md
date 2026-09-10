# H2 Crystal Receipt definition-derived third validation leg

**Local validation complete.** Final closure requires green CI on the separate
H2 commit; its exact SHA and CI result are recorded in the delivery. Initial
RSI HEAD: `45a00875702ed733dfe77c8ba7c30e9a9a93644c`.

The ambiguous-tree gate found exactly 11 ERC-8380 research files and 6 H1
research files, with no unexplained content. Their unchanged bytes were
committed and pushed separately, in the required order:

1. `e052e3ae2ea4ebc3d8a54a8b7a6f4579f0a227c1` — ERC-8380 alignment/STOP research.
2. `c31c4cb1bb112c7f2b415b9721ee3078044dbdb7` — H1 independence audit.

The latter is the clean H2 baseline. Its exact-HEAD CI passed on Python 3.12
and 3.13. Local baseline reruns also produced 430 tests, 430 optimized tests,
85 conformance PASS, and unchanged prior 61 KILLED records.

## Definition and scope

Source: `pipavlo82/crystal-receipt` at
`45b46bf7df3a60b32583291f577a36bf19d22f00`.
Definition: `conformance/counterfactual-audit-boundary-v0/SPEC.md`, sections
Semantic input domain, Audit metadata domain, Reserved field, and frozen
accepted-snapshot vocabulary. SHA-256:
`9c17bd826c4a789464dab80c78a136153f3d9ce2f253198d0cf386bdef3a6d0b`.
The local bytes were independently checked against pinned Git blob
`8287dc7dcaf88f582ebf32104d8494c8f1341f56`.

That definition explicitly retains semantic values, orders keys, forbids
reserved metadata inside the artifact, and excludes external audit metadata
from semantic identity. It is sufficient without executing the TS helpers.
H2 covers only the already admitted flat printable-ASCII string-map subset.
Source vector inputs are shared immutable evidence; their expected outputs
are not the third leg's semantic authority. Exact source/file/vector/code
hashes and complete A/B/C/D outputs are in the JSON companion.

## Separation and protocol

The standalone JavaScript reproducer lives under
`reproducers/crystal-receipt-cleanroom/`. It imports only Node fs/crypto,
verifies SPEC bytes, parses its own restricted duplicate-rejecting transport,
and renders ordered semantic pairs with a manual string-token transformation.
It has no rsi.codec, adapter, predictor, expectation-row, or executable source
helper dependency. Its comparison harness lives separately under tools/.

The definition note and four manual golden deductions preceded the H2
implementation/comparison. Existing predictor/source branches had already
been inspected during H1: procedural blindness is NOT claimed. In every
comparison, all C subprocesses finish before A/B computation or D admission;
this ordering is tested. Golden inputs map exactly to the existing admitted
four cases, preserving the old fixtures and expected artifact.

## Results

| H2 vector | Relation | A/B/C/D + definition golden |
|---|---|---|
| G1 | Control identity preserved | All agree |
| G2 | Semantic value substitution changes snapshot | All agree |
| G3 | External audit_timestamp changed, identity preserved | All agree |
| G4 | External audit_timestamp removed, identity preserved | All agree |

H2-M1 binds external metadata in both local projection doubles; G3 and G4
expose the wrong result. H2-M2 ignores semantic substitution in both doubles;
G2 exposes it. In all three witnesses A-prime equals B-prime while C disagrees
on the semantic relation: COMMON_MODE_CAUGHT. These are two selected research
experiments, not three new global mutations or production defect claims.
See the matrix and experiment companions for exact inputs and observations.

Frozen expectations detect divergence from previously admitted semantics; they do not by themselves prove that the original expectation was independently derived.

## Independence assessment

Crystal remains **10/15 MODERATE**, using the unchanged H1 rubric. Runnable
third-leg evidence and selected common-mode catches strengthen the evidence
within existing score bands; they do not establish independent source origin,
author independence, or exhaustive resistance. JavaScript C and TypeScript A
share Node/V8. Author independence remains UNKNOWN. A/B and admission retain
rsi.codec; C bypasses it, while the comparison harness remains trusted.
Only the Crystal entry/section of the H1 dependency graph was updated.
No other domain's independence claim was promoted.

Allowed Crystal-only wording: Crystal Receipt semantic-snapshot validation
now has three separately implemented derivation/execution legs, including a
definition-derived clean-room reproducer that catches selected common-mode
errors shared by the existing actual/predictor pair. Here clean-room denotes
dependency and derivation separation, not blind or author-independent work.

## Preservation and reproducibility

- 16 H2 tests PASS; full suite **446 PASS**, optimized suite **446 PASS**.
- All **85 conformance PASS**; exact Crystal/all-domain/legacy outcome diff 0.
- All **61 ordinary mutations KILLED**; all prior mutation-record diffs 0;
  SURVIVED, VACUOUS, and NOT_APPLIED remain 0.
- **389 historical protected hashes unchanged**. Of 406 post-research baseline
  tracked files, 404 are unchanged; the only two changes are the authorized
  Crystal-only H1 dependency graph updates. No unexpected hash drift.
- Generic core, schemas, comparator, taxonomy, and validated domain semantics
  unchanged; semantic exceptions 0; anti-coupling PASS.
- H2 comparison rerun is byte-identical. No external repository was modified.

Run `python tools/check_crystal_cleanroom.py` for the complete comparison.
Standalone execution needs only Node, reproduce.mjs, pinned SPEC.md, and one
input JSON; see the reproducer README for POSIX and PowerShell commands.
The isolated minimal-bundle test runs without adapters, predictors, frozen
expectations, private runtime packages, or home-directory assumptions.
A dedicated clean-checkout CI job runs all four standalone inputs and both
Python modes, and checks deterministic comparison output.

Crystal is technically ready as the first bounded externally reproducible
RSI example once these private repository files are made available. No
external-author reproduction or public distribution has occurred. Nested,
Unicode, numeric, descriptor, provenance-authority, Lane K, and broader
ReceiptOS semantics remain outside H2. No new domain phase is started.
