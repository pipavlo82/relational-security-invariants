# ConsultEscrow relation ownership v0

| Responsibility | Exact owner / boundary |
|---|---|
| Declare commitment and lifecycle | agent-ercs ConsultEscrow.sol and IConsultEscrow.sol at the pinned commit |
| Produce outcome authorization | Named attestor; upstream test _sign demonstrates EIP-191 producer. SDK clients take an externally supplied signature; actual production signing workflow not independently inspected |
| Recompute commitment for consumer | agent-sdk python settlement/erc8203/recompute.py; accepts jobId and resultText, outputs commitment only |
| Select escrow context | Caller chooses deployed contract and jobId; contract/chain not signed |
| Verify authorization | ConsultEscrow.release: Open status plus recovered signer equals stored attestor |
| Determine amount/recipient | Immutable job fields populated by payable open, read by release |
| Perform modeled fund movement | Pinned Solidity bytecode in isolated EVM; provider call, Released status/log |
| Consume execution evidence | RSI adapter records local state, balance delta and log; SDK clients simulate/send/wait or transact/wait and parse receipt logs; inspected but external/mainnet execution not validated |
| Independently admit expected result | RSI expectation profile's Python crypto/state obligations, checked atomically |
| Potential overclaim | Client treating SDK hash, any valid signature, simulated release, or a Released label as arbitrary release authority or finalized settlement |

Both SDK and contract can compute correct local commitments while the chosen
network/deployment differs. Neither the SDK hash nor EIP-191 preimage proves that
cross-repo scope. The SDK folder label ERC-8203 also does not turn this contract
into a complete state-channel lifecycle. An attestor signature states a bounded
outcome attestation; it does not prove delivered result correctness.

Signed intent != release eligibility != fund movement.
Authorization, simulation, retained local execution and external chain occurrence
are separate. No external repository or prior RSI domain was modified.
