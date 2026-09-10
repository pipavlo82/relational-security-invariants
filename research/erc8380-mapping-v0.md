# ERC-8380 mapping v0 — source-preflight STOP

RSI stays at `45a00875702ed733dfe77c8ba7c30e9a9a93644c`. No profile, adapter, admitted expectation, fixture or mutation is added. This is an evidence audit, not a successful eighth-family validation.

## Source identity and authority

The live Magicians topic is 29274, with 33 posts at inspection. Cached HTML exposed only 20; live Discourse JSON and later-post retrieval were used. The thread links reference main `mzf11125/unclonable-agent-execution-credentials` at `50f2ae1ddb85f02e55c7b48ae8c609b1fdda31c5` and ethereum/ERCs PR #1953. That PR is open/unmerged; its current source is `mzf11125/mzf11125-ERCs`, branch `erc-unclonable-agent-execution-credentials`, commit `7068f2a2853504475d966c06c8e04ec6d546dbb8`. The document declares `eip: 8380`, `status: Draft`; GitHub's PR draft flag is false. These statuses are distinct.

Exact files, raw SHA-256, posts and evidence classes: `erc8380-source-map-v0.json`. External repositories/forum were read-only.

## Current binding audit

| Boundary | Current source | Assessment |
|---|---|---|
| Guard-consumed nullifier -> verifier vector | both current Guards and HonkVerifierAdapter put cap.nullifier at index 8 of nine inputs | previous omission FIXED in wiring |
| Nullifier -> hidden salt hash | draft requires tagged Keccak; Noir main asserts equality to hash helper; helper returns salt unchanged | exact cryptographic relation UNSUPPORTED |
| Executor/expiry -> issued commitment | both Solidity libraries include padded executor and expiry; PR draft requires them | preimage omission FIXED in Solidity/draft; Noir commitment helper ignores them |
| Target/calldata -> action | Guard checks keccak256(abi.encode(target, callData)) | source-defined contract relation, not executed by RSI in this stopped phase |
| Home chain/domain | Guard checks chain and registered domain; issuance ceiling/authority scoped per domain | contract source, not independently validated here |
| Deployment/value | Guard address is not in shown preimage; execute is nonpayable and has no value parameter | no fabricated deployment/value binding claim |

The commitment fields are tag, salt, agentId, homeChainId, homeDomainId, capabilityIndex, actionCommitment, executor, expiry. Nullifier is separately derived from tag and salt and occupies the final public input; it is not inserted into the capability preimage. Exact bytes32/uint256/address padding is defined by Solidity abi.encodePacked. Action commits target plus the entire ABI-encoded callData bytes. Selector/arguments are thereby committed as bytes, not interpreted as a separate universal action schema.

## Material STOP blocker

`noir/nullifier/src/hash.nr` defines both nullifier and capability_commitment as returning `salt`. The latter ignores all eight other arguments. This cannot establish the tagged Keccak relation required by SPEC.md / ERC-8380 Derivation. A salt of 7 yields helper value 7 by source inspection. This is not a compiled Noir test claim.

The PR test `test_11_CommitmentParity` supplies salt 7 and expected ERC-8380 digests. A separate Keccak concatenation audit reproduces nullifier `0x387e1b17665773c440b8c1e1091763c9b9c2d2733eeaeaf1fdac1d17aa957338` and capability commitment `0x0ca20742a17fa240d3abf6146f61981ee649b937a992f87bb599c1c1899f88cf`. This verifies the published vector arithmetic only. It does not execute the circuit or prove its soundness.

Reference main still uses ERC-1953 domain tags; the current PR uses ERC-8380 tags. Their digests differ for identical inputs, as recorded in the source map. Treating these as interchangeable would silently change the protected commitment. No tags were rewritten.

The PR tests use `BindingVerifier.issueProof` to register a proof-byte hash against a public-input-vector hash. That is a useful contract wiring harness, not a proof of knowledge or Keccak circuit. Reference MockVerifier accepts unlocked proofs by default and optionally locks a vector. The README marks the generated Honk verifier placeholder and M1 parity as a milestone. No independently pinned known-valid proof plus circuit/VK provenance closes the normative relation here.

The generated verifier's 17 public inputs is NOT a 17-versus-9 bug: it subtracts eight pairing-point entries before checking the supplied vector length, yielding nine. This was checked explicitly and is not listed as a blocker.

## Candidate cases, not admitted fixtures

| Requested case | Source basis | Disposition |
|---|---|---|
| 001 exact control | test_01_HappyPath / BindingVerifier | contract-harness control exists; no real proving control admitted |
| 002 fresh nullifier | test_08_NullifierSubstitution / index 8 | wiring rejection specified/tested upstream; end-to-end proof claim unverified |
| 003 executor / 004 expiry | test_07_ExecutorOrExpiryTamper / commitment library | draft/Solidity binding present; circuit relation incomplete |
| 005 action substitution | Guard ActionMismatch check | candidate contract-only relation |
| 006 first spend / 007 second spend | Guard consumed mapping, test_01/test_02 | candidate atomic-consumption harness scope |
| 008 no finality / 009 reorg | forum posts 28/29/31/33 | intended boundary only; no finalized-chain fixture or policy invented |
| 010 mirror | none established in this preflight | absent; no fabricated metadata |

These are not PASS rows and not security-correctness claims. No fresh-nullifier exploit was demonstrated. The old missing-public-input issue must not be reported as still unchanged; the remaining blocker is the incomplete cryptographic derivation lane.

A future explicitly narrowed contract-only phase could validate the supplied BindingVerifier harness as such. This phase is stopped under the requested source-conflict/exact-nullifier-relation gates, rather than silently replacing real proof validation with that narrower task.
