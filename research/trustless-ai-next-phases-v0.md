# Proposed next RSI phases v0

Design proposals only. No new domain, fixture, adapter, mutation or external repository change is implemented in this synthesis. Canonical commits and file digests are in the source map; repin and revalidate drift before implementation.

## Candidate 2E: Workflow verification-to-invocation context

| Item | Proposal |
| --- | --- |
| Repos | trustless-ai/trustless-agent-substrate; trustless-ai/agent-sdk; trustless-ai/agent-ercs |
| Edges | E13; E14 |
| Protected relation | Accepted source/deployment fingerprint applies to current chain/RPC/workflow context before SDK invocation. |
| Control | Upstream sourceGate verified context is accepted and matching current context allows invocation. |
| Relation-substitution negative | Keep the fingerprint and valid context shape but replace workflowAddress, chain or RPC; gate refuses and no invocation occurs. Include stale fingerprint and in-flight invalidation. |
| Mirror-positive | Existing sourceGate test accepts a newer exact block hash when fingerprint and chain/RPC/workflow context are unchanged. Literal block-hash equality is not the source rule. |
| Expected predictor source | Separately implement tuple/revision obligations from sameContext, snapshot and sourceGate tests; do not call the gate for expected results. |
| Adapter source | Pinned production sourceGate.ts and operationService.ts with controlled SDK port; deployment verifier is a separately scoped obligation. |
| Mutation | Drop workflowAddress comparison or invoke SDK before gate assertion. |
| Likely blocker | Pin TypeScript/dependency closure; distinguish supplied verified context from independent deployment or consensus verification. Chain-bound runtime currently Anvil-only. |
| New family | Verified source/deployment identity to current invocation applicability and race invalidation. |
| Source | [S058: trustless-ai/trustless-agent-substrate/src/core/workflow/sourceGate.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/src/core/workflow/sourceGate.ts); [S060: trustless-ai/trustless-agent-substrate/test/unit/workflow/sourceGate.test.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/test/unit/workflow/sourceGate.test.ts); [S057: trustless-ai/trustless-agent-substrate/src/core/workflow/operationService.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/src/core/workflow/operationService.ts); [S059: trustless-ai/trustless-agent-substrate/src/core/workflow/sourceVerifier.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/src/core/workflow/sourceVerifier.ts) |

## Candidate 2F: Job-bound settlement release

| Item | Proposal |
| --- | --- |
| Repos | trustless-ai/agent-ercs; trustless-ai/agent-sdk |
| Edges | E11 |
| Protected relation | Attestor signature binds exact jobId/resultHash whose escrow state and payment change. |
| Control | test_release_happyPath opens job A, signs commitment, releases once to provider. |
| Relation-substitution negative | test_signature_isBoundToJobId: two valid open jobs share resultHash/attestor; valid A signature must not release B. |
| Mirror-positive | Proposed from public release implementation: different transaction relayer submits same job-bound signature; msg.sender does not select the attestor. Exact mirror pair not yet a published test. |
| Expected predictor source | Solidity commitment preimage/state obligations plus independent EIP-191 recovery; SDK hash is a cross-check, not sole oracle. |
| Adapter source | Exact ConsultEscrow.sol in isolated EVM/Foundry harness. |
| Mutation | Omit jobId from commitment or bypass recovered attestor comparison. |
| Likely blocker | Pin compiler/EVM/dependencies. SDK comment says resultText is emitted, but contract Released contains resultHash, not text. Supply pinned text preimage or work with resultHash. Signature preimage lacks chain/contract separation; do not claim global replay resistance. |
| New family | Authenticated evidence gating durable monetary state transition. |
| Source | [S015: trustless-ai/agent-ercs/contracts/settlement/ConsultEscrow/ConsultEscrow.sol](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/settlement/ConsultEscrow/ConsultEscrow.sol); [S018: trustless-ai/agent-ercs/test/settlement/ConsultEscrow/ConsultEscrow.t.sol](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/test/settlement/ConsultEscrow/ConsultEscrow.t.sol); [S024: trustless-ai/agent-sdk/python/src/agent_sdk/settlement/erc8203/recompute.py](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/python/src/agent_sdk/settlement/erc8203/recompute.py) |

## Candidate 2G: State-proof binding and header-authority separation

| Item | Proposal |
| --- | --- |
| Repos | trustless-ai/verify-layer; trustless-ai/primitives |
| Edges | E18 |
| Protected relation | Self-consistent MPT proof binds to selected stateRoot/address/slot; proof success retains header trust class. |
| Control | Pin exact public EIP-1186 account/storage proof and selected block root. |
| Relation-substitution negative | Keep valid original proof bytes, substitute another well-formed expected stateRoot; MPT local consistency cannot imply boundToHeader. |
| Mirror-positive | Proposed representation test: hex letter-case changes with identical decoded proof/root bytes. Requires validation; no existing frozen mirror vector claimed. |
| Expected predictor source | Separate MPT/RLP/root implementation plus pinned account/slot and explicit RPC-TRUSTED header obligation. |
| Adapter source | Pinned checkAccountProof / verifyStorage logic isolated from live main() and credential access. |
| Mutation | Ignore root binding or promote RPC-TRUSTED to consensus verified after proof success. |
| Likely blocker | No frozen offline proof corpus inspected; independently pin one and second oracle. LightClientHeaderSource is unwired. Deterministic tests must not need live RPC credentials. |
| New family | Cryptographic state inclusion versus independent header/consensus authority. |
| Source | [S063: trustless-ai/verify-layer/verify.mjs](https://github.com/trustless-ai/verify-layer/blob/84afc4b738dc37269089c858404eed8086435f5d/verify.mjs); [S062: trustless-ai/verify-layer/README.md](https://github.com/trustless-ai/verify-layer/blob/84afc4b738dc37269089c858404eed8086435f5d/README.md); [S036: trustless-ai/primitives/check.py](https://github.com/trustless-ai/primitives/blob/6b39e9540d4bd0a78decb588c0a8e328c303f208/check.py) |


## Why these three

TAS has direct production gates plus already-published discriminating and mirror tests, and adds execution-context applicability. ConsultEscrow adds actual state/payment gating with a source test preserving a valid signature while substituting the job. verify-layer adds proof/root versus header-authority separation, but ranks third because frozen offline evidence and a second oracle are prerequisites.

ERC8275 convention identity is a strong lower-cost alternative, especially for historical convention handling, but its full settlement→reputation claim needs authentic event-set extraction. CCIP/ReceiptOS transport composition is also valuable; it does not require pretending the TSEI receipt's private authority operands are available. Neither lower effort nor higher mutation count justifies a broader claim.

## Admission conditions for any next phase

- Verify live canonical source and pin exact bytes; preserve source-specific status and version boundaries.
- Prove the control, locally valid relation substitution and mirror before claiming a new family.
- Obtain a predictor independent of implementation-under-test; do not use source test labels as self-authorizing truth.
- Preserve all current 337 tests, 64 checks, 45 mutation records and protected semantic hashes.
- Use the existing generic pipeline without domain branches; stop if semantics or unsupported transport would need silent reinterpretation.
- Keep absence of deployment/anchor/consensus/signature evidence explicit. A reference consumer or pure digest function is not an end-to-end execution proof.

Semantic ABI remains read-only during the hackathon. Full RVR amendment authentication, TSEI provenance authority and PQ authenticated history are separate evidence-closure tasks, not automatically unlocked by these proposals.
