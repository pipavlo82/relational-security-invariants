# Phase 3G: signed judgment / terminal-record binding

All local gates PASS. Phase closure additionally requires CI green on the exact pushed commit. The final v0 delivery/tag records that gate separately.

Base: `5ec20dd971a9a1c0b50f3641b545bb74efbfd2d4`.

| Gate | Result |
|---|---|
| Tests normal / optimized | 539 / 539 PASS; before 509 / 509 |
| Conformance | 123 PASS: prior 111 + new 12; other statuses 0 |
| Mutations | 84 KILLED: prior 76 + new 8; other statuses 0 |
| Prior report / rows / mutation records | exact diff 0 / 0 / 0 |
| Protected hashes | 572 unchanged |
| Sources | 20 exact files; SHA-256 and Git blob identities checked |
| Anti-coupling | PASS, 17 unchanged generic Python files |
| Generic core / taxonomy / semantic exceptions | unchanged / unchanged / 0 |

## Results

Every source signature in the 12-case corpus is real and verifies. Terminal/action-ref substitutions fail the record join; signed-other-envelope and wrong-policy identity cases fail admission; late/no/existence-only anchor cases preserve distinct conditional ordering states. Anchor-note mirror passes. A terminal `not_executed` label produces the same source join result, so actual occurrence remains unsupported.

The source control contains a signed **reject** verdict. Its overall source PASS means joined records, not approval. Top-level RSI PASS is agreement with admitted expected observation, including negative and unsupported internal states.

## Mutation matrix

| Mutation | Mapped check | Result |
|---|---|---|
| JEX-M1 | tests.test_judgment.JudgmentTests.test_terminal_substitution | KILLED |
| JEX-M2 | tests.test_judgment.JudgmentTests.test_action_ref | KILLED |
| JEX-M3 | tests.test_judgment.JudgmentTests.test_other_signed_envelope | KILLED |
| JEX-M4 | tests.test_judgment.JudgmentTests.test_late_anchor | KILLED |
| JEX-M5 | tests.test_judgment.JudgmentTests.test_execution_unsupported | KILLED |
| JEX-M6 | tests.test_judgment.JudgmentTests.test_authorization_not_inherited | KILLED |
| JEX-M7 | tests.test_judgment.JudgmentTests.test_anchor_not_authority | KILLED |
| JEX-M8 | tests.test_judgment.JudgmentTests.test_mirror | KILLED |

All mutations reach mapped assertion execution. Setup/import/source failures remain VACUOUS. Frozen rows and mutation kills are not proof of independent oracle origin.

## Claim and limits

RSI validates binding between a signed judgment, the supplied canonical proposal envelope and the supplied terminal record under the pinned ERC-8299 reference application. A valid signature does not transfer to a different envelope/action reference, establish approval, prove anchor authority or prove that an action occurred.

The scope is supplied-record binding, not complete ERC-8299, conditional-action execution or production authorization. Source trust assumptions are named, not repaired silently. All prior domain unsupported surfaces and ERC-8380 blocked status remain intact.

See [source/derivation map](judgment-execution-mapping-v0.md), [exact pins](judgment-execution-source-map-v0.json), [ownership](judgment-execution-relation-ownership-v0.md) and [reproduction](../evidence/judgment/REPRODUCING.md).
