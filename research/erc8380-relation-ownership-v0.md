# ERC-8380 relation ownership v0

| Role | Source owner / artifact | What remains separate |
|---|---|---|
| Issue capability | domain orchestrator; DomainRegistry.orchestratorOf and Guard.issue | issuance policy/decision soundness is external |
| Derive salt/commitment | issuer plus CapabilityCommitment library | tagged Keccak must agree with actual circuit |
| Create proof | agent/prover; Noir main and hash helpers | current helper derivation is incomplete |
| Verify proof | immutable IVerifier dependency | BindingVerifier test registration is not cryptographic verification |
| Supply nullifier | Capability calldata | must equal circuit-derived index-8 value |
| Consume nullifier | CoupledCredentialGuard.execute | consumed mapping scoped to that chain state/Guard |
| Perform action | target.call(callData), atomically with burn | target success does not prove external physical effect |
| Observe finality | off-chain actor/chain policy | no finality engine or threshold provided |
| Trigger external effect | downstream off-chain consumer | must not infer irreversible authority from event presence |

Exact source heads/files: erc8380-source-map-v0.json. The normative PR and reference main are distinct pinned artifacts with different domain tags. RSI owns none of those source semantics and did not repair or merge them.

The family could be materially new through single-use issuance, atomic consumption/action rollback and finality-sensitive observation. This differs from TAS read dispatch, ConsultEscrow settlement conditions and PQ as-of selection. It is not counted as an RSI-validated eighth family because implementation stopped before admission.
