# Phase 3F: ERC-8312 Aggregate Budget mapping

Local edge validity does not establish aggregate root-budget conservation.
The protected quantity is the sum of admitted draws sharing **both rootId and
periodIndex**, bounded by that root's immutable cap. A child/edge is attribution;
it is not a separate source of root budget.

Source discovery resolved the reference repository's old Atlas-Protocol-AI link
to **ERC8312/bounded-agent-actions**. Ethereum/ERCs master at
`84b46e7d69d08dbd8876503e435fd299211c26b8` does not contain erc-8312.md.
The draft is **open PR #1833**, head `0x2kNJ/ERCs`, branch
`add-bounded-agent-actions`, `d94cacf89287a295823ce43e560a575c0cc25e21`.
It is normative draft evidence, not a merged Ethereum standard.

The exact reference main is `728310aa69f5b22152b32f1ef31394b85f3eb8bb`.
The source map lists every relevant file, SHA-256, Git blob ID and evidence class.
The recompute-kit main is `15f7f59ac47b3358492bd5741143c418b5d657f5`.
Its vector digest `ac6f6efd485e887a7f82140ac5be234643af17efb24506d9cd40e87ecd2bcb85`
matches the digest named by the reference's vector test.

## What is executed

The additive `erc8312.aggregate-budget.v0` profile executes exact Solidity
bytecode in a local EVM and exact source `valueFor` TypeScript gate over native
admitted-event observations. A Python ledger-fold predictor produces separately
implemented expectations. Frozen admission decisions have their own derivation
record. Generic registration, expectation admission, adapter dispatch, relation
profile and comparator are reused without modification.

The source PerEdgeBudgetMock is a deliberately nonconforming test witness. Its
two individually admitted sibling draws can total twice the root cap. Recording
that observed violation as conformance PASS means the observation matched the
admitted expectation; it does not turn the witness into a conforming budget
implementation or demonstrate an exploit in a deployed product.

| Fixture | Protected observation | Definition / source test |
|---|---|---|
| AGG-RSI-001 | 600 + 400 reaches cap 1000 exactly | draft section 5; exact-boundary and shared-meter tests |
| AGG-RSI-002 | per-edge 1000 + 1000 is locally admitted, root sum 2000 violates cap 1000 | test_PerEdge_SiblingAmplification_RealizesTwiceTheRootCap |
| AGG-RSI-003 | same-cap siblings in cursor share root; second 1000 reverts | test_Aggregate_SiblingsShareOneMeter_SecondDrawReverts |
| AGG-RSI-004 | 900 + 800 accepted; 700 rejected; then 300 succeeds with no phantom node spend | fan-out source tests; draw write/revert ordering |
| AGG-RSI-005 | same agent under two parents cannot mint root headroom | test_SameAgentUnderTwoParents_CannotMintBudget |
| AGG-RSI-006 | revoking spent node blocks it without refund; remaining sibling gets only residual budget | test_RevokedNodeCannotDraw_AndSpendIsNotRefunded |
| AGG-RSI-007 | period 0 and 1 retain separate stored meters; historical period is not overwritten | test_PeriodRollover_ResetsMeter; stored-key draft and gate definition |
| AGG-RSI-008 | timestamp 101 to 102 within same period preserves all semantic observations | source _periodIndex; gate stored-key/no timestamp-replay rule |
| AGG-RSI-009 | node's own cap remains a separate local check | test_NodeCapBlocksEvenWithRootHeadroom |
| AGG-RSI-010 | capped node cannot delegate; its own eligible draw still succeeds | test_CappedNodeCannotDelegate |
| AGG-RSI-011 | separate roots do not share headroom or meter balances | draft rootId key; createRoot/spentRoot implementation; gate root isolation vector |
| AGG-RSI-012 | ancestor revocation blocks descendant draw and delegation; prior spend remains | test_AncestorRevocationBlocksWholeSubtree |

Parameters are compact RSI instantiations of source-defined cases, not a claim
that every fixture is byte-identical to an upstream test. Mirror-positive 008 is
definition-derived from unchanged period index; time is not falsely added to
the aggregate log predicate. Overflow, depth exhaustion, arbitrary invalid root
creation, deployment identity and unrestricted graph/state fuzzing are not
claimed covered. Source Foundry tests/invariants are pinned evidence; this phase
does not claim to have rerun their entire Forge suite.

## Relation ownership and cross-repo edge

| Role | Source owner / component | Boundary |
|---|---|---|
| Declaration | open ERC draft section 5; aggregate profile | one immutable root cap and stored root/period meter |
| Evidence producer / admission enforcer | AggregateBudgetCursor | source caller/path/node/root checks, atomic storage and Drawn event |
| Recompute consumer | recompute-kit aggregate-budget-v0 gate | filter admitted events by root and period; sum amounts, compare cap |
| Interface composition | agent-ercs ERC8312 IAggregateBudget and README | interface evidence, not an independently executed aggregate implementation |
| Adjacent SDK consumer | agent-sdk ERC8312 base clients/helpers/mock | base substrate profile only; no claim of SDK aggregate-tree validation |
| Adversarial conformance | RSI profile, predictor, admitted rows and comparator | discriminate per-edge attribution from root conservation and prevent claim promotion |

`agent-ercs@01283ca57305f915afb560d23359a27fd748eb5a` and
`agent-sdk@e41b117893fb56bc869922de378daf91aad63def` are pinned for these bounded
roles. The actual cross-repo executable edge validated here is **reference
Drawn/storage observations -> recompute-kit root/period predicate**, not an
unverified SDK deployment path.

## Boundaries and independence

Root conservation is only over draws routed through this meter. Non-bypassability,
asset movement, cross-chain conservation, subtree budgets and authoritative chain
state remain UNSUPPORTED internal capabilities. Capped nodes are leaves; nodeCap
is an own-node limit, not a subtree reservation. Revoke is not a refund. A fresh
period is a distinct key, not permission to rewrite the old key. No execution,
consensus, finality or settlement result is inferred from source events.

The reference's cap/period fields are immutable and this exact ABI provides no
reset/admin setter. This is inspection of the pinned nonproxy implementation,
not a universal guarantee about arbitrary deployments or upgrade mechanisms.

The predictor is **separately implemented**, not unqualifiedly independent.
Solidity/EVM admission and TypeScript event recomputation differ from the Python
ledger fold, but all use the same source meaning and error labels. Source pin
verification, fixture bytes, generic transport/admission and comparator are
shared. Author independence is UNKNOWN; no new clean-room third leg is claimed.
A common mistaken interpretation of the draft can still affect both paths.
Golden decisions add a reviewable definition route, not proof of author independence.

This is a materially different relation family: conservation of a shared budget
across many locally valid delegation edges. It differs from temporal key selection,
read-dispatch binding, and job-local release authorization. It does not establish
all ERC-8312 semantics or ecosystem-wide budget security.
