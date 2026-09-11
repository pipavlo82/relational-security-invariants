# Phase 3F validation: ERC-8312 Aggregate Budget

Local validation is complete. Phase closure additionally requires green CI on the exact pushed commit; this report does not pre-claim that delivery gate.

Base: `484cd49fb7bd97c4659206302573f60ffd0ce4e2`. No generic or prior-domain file changed.

| Gate | Result |
|---|---|
| Normal / optimized tests | 509 / 509 PASS; 477 / 477 before |
| Conformance | 111 PASS, all other statuses 0; new 12 / prior 99 |
| Mutations | 76 KILLED; new 9 / prior 67; all other statuses 0 |
| Prior report / ordered rows / mutation records | exact diff 0 / 0 / 0 |
| Protected hashes | 498 unchanged |
| External / execution closure | 22 / 39 pinned files, all digests verified |
| Native rebuild / deterministic rerun / offline clean copy | byte-identical |
| Anti-coupling | PASS across 17 generic Python files |
| Generic core / taxonomy changes / semantic exceptions | 0 / 0 / 0 |

## Observed cases

PASS is conformance to the admitted observation. It does not certify that a deliberately nonconforming witness conserves a budget.

| Case | Realized sum | Root/period conservation | Native reverts |
|---|---:|---|---|
| AGG-RSI-001/control | 1000 | True | none |
| AGG-RSI-002/edge_amplification | 2000 | False | none |
| AGG-RSI-003/shared_root | 1000 | True | RootBoundExceeded |
| AGG-RSI-004/fanout_atomic | 2000 | True | RootBoundExceeded |
| AGG-RSI-005/diamond | 1000 | True | RootBoundExceeded |
| AGG-RSI-006/revoke_no_refund | 1000 | True | PathRevoked, RootBoundExceeded |
| AGG-RSI-007/period_history | 2000 | True | none |
| AGG-RSI-008/timestamp_mirror | 1000 | True | none |
| AGG-RSI-009/node_cap | 200 | True | NodeBoundExceeded |
| AGG-RSI-010/capped_leaf | 200 | True | CappedNodeCannotDelegate |
| AGG-RSI-011/root_isolation | 3000 | True | RootBoundExceeded |
| AGG-RSI-012/ancestor_revoked | 1000 | True | PathRevoked, PathRevoked |

The period-history case admits 1000 in each of two distinct periods; 2000 across both is not a violation. Root isolation similarly sums across distinct roots only for display; conservation is checked per key.

## Mutation matrix

| Mutation | Changed decision | Mapped test | Result |
|---|---|---|---|
| AGG-M1 | max per-edge subtotal replaces root sum | tests.test_aggregate.AggregateTests.test_edge_amplification | KILLED |
| AGG-M2 | omit root bound check | tests.test_aggregate.AggregateTests.test_shared_root | KILLED |
| AGG-M3 | revoke resets spent root | tests.test_aggregate.AggregateTests.test_revoke_no_refund | KILLED |
| AGG-M4 | collapse all periods to zero | tests.test_aggregate.AggregateTests.test_period_history | KILLED |
| AGG-M5 | allow capped node delegation | tests.test_aggregate.AggregateTests.test_capped_leaf | KILLED |
| AGG-M6 | ignore revoked path | tests.test_aggregate.AggregateTests.test_ancestor_revoked | KILLED |
| AGG-M7 | ignore own-node cap | tests.test_aggregate.AggregateTests.test_node_cap | KILLED |
| AGG-M8 | promote metered conservation to non-bypassability | tests.test_aggregate.AggregateTests.test_unsupported_claims | KILLED |
| AGG-M9 | reject same-period timestamp mirror | tests.test_aggregate.AggregateTests.test_mirror | KILLED |

Each mutation reaches its mapped test assertion. Setup/import/native execution errors remain VACUOUS. Mutation counts demonstrate these decisions are load-bearing, not complete coverage or oracle independence.

## Scope and evidence

See [source map](aggregate-budget-source-map-v0.json), [exact file hashes](aggregate-budget-source-files-v0.md), [relation mapping and ownership](aggregate-budget-mapping-v0.md), and [offline reproduction](../evidence/aggregate/REPRODUCING.md).

ERC-8312 remains an open draft PR at the recorded source state. Agent-ercs is interface evidence; the SDK base helpers are not an aggregate implementation. The executed cross-repo edge is reference native Drawn/storage -> recompute-kit admitted-log predicate.

The separately implemented Python predictor folds admitted history, while the actual path executes Solidity and TypeScript. Shared definitions/codec/pins and author-independence UNKNOWN remain explicit. No clean-room third leg or independent cryptographic oracle is claimed.

Non-bypassability, asset movement, cross-chain conservation, subtree budgets, authoritative chain state, deployment identity and finality remain unsupported. The deliberate per-edge mock is not a production exploit claim. All prior RVR/TSEI/PQ/TAS/ERC-8380 unsupported boundaries remain unchanged.

## Recommended bounded closure claim

RSI distinguishes local delegation-edge validity from aggregate conservation of a single root/period budget. Under the pinned per-edge counterexample, individually admitted draws exceed the root cap; under the pinned AggregateBudgetCursor, the shared root meter rejects the excess and reconciles with admitted-log recomputation. The result covers metered single-chain traces and does not establish non-bypassability, asset movement or ecosystem-wide ERC-8312 security.

Phase 3G and the final v0 tag are separate future gates. Neither is started here.
