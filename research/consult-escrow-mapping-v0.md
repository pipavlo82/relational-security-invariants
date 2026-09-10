# ConsultEscrow mapping v0

This is the sixth concrete relation family in RSI. It tests job-bound outcome
attestation against a contract-local escrow state, not complete payment security.
Source identity/digests and field-by-field scope are in
[signature scope](consult-escrow-signature-scope-v0.md) and
[source map](consult-escrow-source-map-v0.json).

| Fixture | Protected relation | Source and interpretation boundary |
|---|---|---|
| CE-RSI-001 (control, wrong_attestor) | job status and attestor recovery | test_release_happyPath; test_release_wrongSigner_reverts. Stored amount/provider checked by local balance/event evidence. |
| CE-RSI-002 (wrong_job, wrong_result) | signed jobId/resultHash commitment | test_signature_isBoundToJobId; release commitment expression. Same 65-byte signature remains valid on original job; two structurally valid funded jobs. resultHash substitution is a source-derived extension of the commitment test. |
| CE-RSI-006 (replayed_release) | Open status gates one-time release | test_release_notOpen_reverts. Second call after successful release; another funded job makes skip-status mutant observable rather than an insufficient-balance setup error. |
| CE-RSI-007 (relayer_mirror) | release caller is not a signed or checked endpoint | release implementation; no msg.sender authorization condition. Source-derived metamorphic mirror, not a published golden mirror vector. Caller changes; signed tuple, stored job and economic result do not. |
| CE-RSI-008 (preflight_only) | eligibility without retained settlement evidence | release implementation plus isolated EVM checkpoint/revert harness. Adapter instrumentation boundary, not a new on-chain view method. Simulation logs are discarded and state/balances reverted. |

The profile `consult-escrow.release-binding.v0`, version `0`, relation
`job-bound-release`, uses only registered profile-specific slots. Addresses,
bytes32 and 65-byte signatures are canonical lowercase ASCII hex. uint256 values
are canonical decimal strings and converted to JavaScript BigInt exactly. The
1 ETH fixture amount exceeds 2^53 and is never a JSON numeric value. The harness
has an explicit funding bound and two distinct funded jobs; EOA behavior only.
Unicode in pinned Solidity comments remains exact UTF-8 source bytes and is not
silently coerced into fixture transport. Result text/raw arbitrary calldata,
transaction signatures, chain state and arbitrary recipient contracts are not
part of this transport/profile scope.

## Actual and expected separation

Actual: unmodified pinned Solidity and interface compiled by solc 0.8.25,
Cancun, optimizer disabled; deployed and executed by pinned EthereumJS EVM.
Its ecrecover precompile performs signature recovery. ABI encoding/log decoding
uses pinned ethers. There is no RPC call, wallet connection or real transfer.
A fresh EVM/state is created for every case. The adapter returns observations,
never expected rows. The three additional compiled bytecodes are controlled
mutation artifacts, not selectable through fixture inputs.

Expected: separately implemented Python Keccak-256, integer secp256k1 recovery,
and declarative status/payment obligations. It neither calls EVM/ethers nor
imports adapter code. It derives every expectation row before atomic admission.
Shared source pin verification is evidence plumbing, not a shared evaluator.
Known hash answers, recovery-v sensitivity and the original-job signature test
check this path. Different languages/code paths strengthen independence;
author independence and independent cryptographic audit are not established.
This test oracle is not a production cryptography library.

The source test key 0xA11CE is a public test fixture, not a funded/secret wallet.
Signatures use source test jobA/jobB/sameResult values. Harness addresses are
explicit isolated EOAs; there is no address-derived authority.

## Claim boundary

PASS means actual matched independently admitted expected behavior. A rejected
wrong-job release is a conformance PASS. Successful local EVM payment includes
retained state, provider balance change and Released log. Checkpointed preflight
can establish eligibility while execution remains UNSUPPORTED. Neither outcome
asserts mainnet settlement, deployment authenticity, finality, result truth or
cross-instance signature replay resistance.

CE-M1 substitutes the commitment's job endpoint with the source test's original
jobA in compiled mutant bytecode. CE-M5 removes the signer check. CE-M8 removes
the Open guard. CE-M6 and CE-M7 mutate the adapter's claim/relayer handling. Each
is classified through the unchanged phase-aware mutation registry; setup/source
errors cannot count as KILLED. Amount/recipient/chain mutations are omitted where
no independent signed field exists, not registered as artificial coverage.

The inspected TypeScript ConsultEscrowClient.release separates simulateContract
from writeContract and waitForTransactionReceipt. CE-RSI-008 models that boundary
with checkpoint/revert; it does not execute the SDK network client. Exact consumer
pins are in the source map. The SDK verify helper checks commitment equality, not
ECDSA authorization. Production attestor signature generation remains caller-owned.
