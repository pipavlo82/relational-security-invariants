# ConsultEscrow signature scope v0

Source: `trustless-ai/agent-ercs`, canonical `main` at `01283ca57305f915afb560d23359a27fd748eb5a`.
The exact component is `contracts/settlement/ConsultEscrow/ConsultEscrow.sol`,
identified by synthesis Candidate 2F. Canonical source was reverified through
GitHub, not inferred from the SDK folder name. No external repository was modified.

## Exact preimage and verification

`commitmentHash = keccak256(abi.encode(bytes32 jobId, bytes32 resultHash))`.
Both values occupy one 32-byte ABI word: 64 bytes in this order, without dynamic
ABI offsets. The signature digest is Keccak-256 of the 28-byte EIP-191 prefix
`0x19 || "Ethereum Signed Message:" || 0x0a || "32"` followed by the commitment.
`signature` is exactly 65 bytes, packed `r[32] || s[32] || v[1]`.
The source calls EVM `ecrecover` and compares the recovered address to the stored
job attestor. Pubkey presence and digest equality alone are not used as proof.
There is no explicit low-s check. No EIP-712 domain separator is present.

| Field | Protection actually present |
|---|---|
| jobId | Directly signed; selects this contract's `jobs[jobId]` |
| resultHash | Directly signed; result text itself is not supplied to release |
| provider/recipient | Stored at open, immutable through the exposed lifecycle; transfer destination read from job |
| amount | Native ETH `msg.value` stored at open; transfer amount read from job |
| attestor | Stored at open; recovered signer must match |
| consumer/payer | Stored opener; refund destination; not part of signed preimage |
| escrow identity | Contract-local jobId is signed; contract address is not |
| asset | Native ETH only; no selectable token argument |
| chainId / deployment address | Absent from signed preimage and EIP-191 prefix |
| caller / relayer | Not an authorization condition in release |
| deadline | Stored at open; enables refund, not signature expiry or release cutoff |
| nonce / replay | No signed nonce; Open -> Released/Refunded prevents subsequent release; job cannot be reopened |
| milestone / policy / action selector | Not signed; no such release inputs |

## Conditions and economic boundary

Release requires Open status AND recovery to the stored attestor. It then sets
Released, sends stored amount to stored provider, requires successful payment,
and emits Released. A reverted payment rolls back state by EVM semantics.

**Signed intent != release eligibility != fund movement.**
The isolated EVM harness observes state, balance delta and event. A checkpointed
preflight is reverted and supplies no retained settlement evidence. No mainnet
receipt, inclusion, finality or deployment-bytecode verification is performed.

Deadline opens the competing refund path; source does not disallow release after
deadline while Open. We do not invent an expiry-rejection fixture. Refund and
hostile recipient/reentrancy behavior remain outside this corpus.

## Missing-binding analysis

CE-RSI-003/004 are not fabricated: amount and recipient are not independently
signed release parameters. Within one immutable job they are constrained by
state. That is a different protection from signing the amount/recipient directly.
CE-RSI-005 is not registered as a rejecting chain/deployment test: no such domain
binding exists. Reuse against another instance/chain with the same jobId and
attestor is not cryptographically excluded by this preimage. Different stored
amount/provider could change the economic effect. This is a source-defined scope
gap; no victim deployment, funds-at-risk scenario or exploit transaction has been
established here. Such acceptance is not counted as a passing security fixture.

The Python SDK helper at `e41b117893fb56bc869922de378daf91aad63def` correctly reconstructs the commitment from
jobId and result text, but its docstring incorrectly says resultText is emitted.
The contract/interface emit **resultHash**, not resultText. We preserve the
contract's exact ABI and do not claim public result-text availability, verdict
truth, or pre-outcome ordering. The component README explicitly distinguishes
this OutcomeAttestation from an OutcomeCommitment/state-channel lifecycle.

## Pinned evidence

| Repository | Commit | File | SHA-256 | Evidence class |
|---|---|---|---|---|
| trustless-ai/agent-ercs | `01283ca57305f915afb560d23359a27fd748eb5a` | `contracts/settlement/ConsultEscrow/ConsultEscrow.sol` | `373e1f6feab886d1115eceef391cebce97a16b51d4bdfdfb1e5bd4bdb3bd07f5` | contract |
| trustless-ai/agent-ercs | `01283ca57305f915afb560d23359a27fd748eb5a` | `contracts/settlement/ConsultEscrow/IConsultEscrow.sol` | `5ed94f6db2460548ea0dd52d7339288ca1f8f974e23567a60f98d09eb7000584` | contract |
| trustless-ai/agent-ercs | `01283ca57305f915afb560d23359a27fd748eb5a` | `test/settlement/ConsultEscrow/ConsultEscrow.t.sol` | `6514b07c495618755a03d5206eff67804bd62fc70189e97316e26e5f455f78cc` | test |
| trustless-ai/agent-ercs | `01283ca57305f915afb560d23359a27fd748eb5a` | `foundry.toml` | `a1e37ff8d0e0cc50d0682ae3bed1875b75783f46ae0635b84dd8cc556b6c19ea` | documentation/configuration |
| trustless-ai/agent-ercs | `01283ca57305f915afb560d23359a27fd748eb5a` | `contracts/settlement/ConsultEscrow/README.md` | `0ff2d3ef4bdc71d7f76b4eac13214bcf69c3cf68149d31348ea1dbc26375fef0` | documentation/configuration |
| trustless-ai/agent-sdk | `e41b117893fb56bc869922de378daf91aad63def` | `python/src/agent_sdk/settlement/erc8203/recompute.py` | `6960e4dd22a8dd62cc0171ceefc1b014bfe8f28b2a0cd8df14214cc803f4c980` | implementation |

## Direct SDK consumers inspected

Python and TypeScript ConsultEscrowClient.release both accept an externally
provided jobId/resultHash/signature and select a configured deployment. They do
not create the attestor signature. TypeScript explicitly calls simulateContract,
then writeContract, then waitForTransactionReceipt: successful preflight is not
the transaction receipt. Python transacts and waits for a receipt. Both verify
helpers compare commitment hashes only; those helpers are not signature verifiers.
The SDK clients were inspected as evidence, not executed against a live chain.

| Repository | Commit | File | SHA-256 | Evidence |
|---|---|---|---|---|
| trustless-ai/agent-sdk | `e41b117893fb56bc869922de378daf91aad63def` | `python/src/agent_sdk/settlement/erc8203/client.py` | `448dbde2b3ee00320f93d1f2c709786f2ba03ec915b3c84d2f48f106ae591b1c` | SDK consumer |
| trustless-ai/agent-sdk | `e41b117893fb56bc869922de378daf91aad63def` | `typescript/src/settlement/ERC8203/client.ts` | `a7f6cad7814536d0297a2a754ef87e28e0a4eacb807bc44ebcfbcda4d178b7f8` | SDK consumer |
