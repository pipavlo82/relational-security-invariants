# ERC-8380 commitment alignment audit

## Decision and pins

**MISALIGNED. Phase 3D remains BLOCKED.** No adapter, fixture, mutation, code, external change, commit or push is introduced. Five research outputs only; six earlier STOP reports remain untouched.

RSI main: `45a00875702ed733dfe77c8ba7c30e9a9a93644c`.
Reference `mzf11125/unclonable-agent-execution-credentials`, main: `50f2ae1ddb85f02e55c7b48ae8c609b1fdda31c5`.
Draft `mzf11125/mzf11125-ERCs`, `erc-unclonable-agent-execution-credentials`: `7068f2a2853504475d966c06c8e04ec6d546dbb8`, open unmerged ethereum/ERCs PR #1953.
Both current refs were queried again; no delta. All 20 pinned files were fetched read-only again and their SHA-256 matched. Live forum still has 33 posts; posts 31/33 and their content hashes match the prior capture. No source authority is inferred from an old chat summary.

## Exact formulas

K means Ethereum Keccak-256 (not standardized SHA3-256). U256(x) is the unsigned 32-byte big-endian encoding; address executor becomes uint160, then uint256, then bytes32. Concatenation is ||. Salt s is bytes32 on the Solidity surface.

```text
TC8380 = K(ASCII("ERC-8380/capability/v1"))
TN8380 = K(ASCII("ERC-8380/nullifier/v1"))
A = K(abi.encode(address target, bytes callData))
C8380 = K(TC8380 || s || U256(agentId) || U256(homeChainId)
          || U256(homeDomainId) || U256(capabilityIndex) || A
          || U256(uint160(executor)) || U256(expiry))
N8380 = K(TN8380 || s)
```

These are the draft Derivation section and draft asset CapabilityCommitment.computeCapabilityCommitment / computeNullifier. Outer Solidity encoding is abi.encodePacked, nine fixed 32-byte words (288 bytes) for C and two words (64 bytes) for N. The action hash uses ordinary ABI encoding of address and dynamic bytes, not packed address/calldata. Nullifier is not an additional commitment word: both derivations share the private salt. No chain ID or payload is added to the nullifier. No Guard address or value word is present.

The reference Solidity library has exactly the same field order and conversions but substitutes:

```text
TC1953 = K(ASCII("ERC-1953/capability/v1"))
TN1953 = K(ASCII("ERC-1953/nullifier/v1"))
C1953 = C formula with TC1953
N1953 = K(TN1953 || s)
```

Reference SPEC.md also names the old domain. No inspected alias or dispatch accepting both domains exists. Tags are hashed string bytes, then the resulting 32 bytes are included in the outer preimage; they are not cosmetic comments. Distinct tags define distinct domains. A universal mathematical assertion that every pair of outputs must differ would ignore hash collisions; the published vector demonstrably differs, and no equivalence/compatibility is defined.

Noir is an identity relation, not Keccak or Poseidon:

```text
hash::nullifier(salt: Field) -> Field { salt }
hash::capability_commitment(salt, agent_id, home_chain_id, home_domain_id,
                           capability_index, action_commitment, executor, expiry) -> Field { salt }
main: assert(nullifier == hash::nullifier(salt))
      assert(capability_commitment == hash::capability_commitment(salt, ...))
therefore: nullifier == capability_commitment == salt (as Field values)
```

Exact code path: reference noir/nullifier/src/main.nr calls hash.nr; hash.nr nullifier lines 6-8 and capability_commitment lines 10-21 return salt. All seven envelope parameters are ignored by the helper. No tag, byte packing, Keccak or explicit bytes32-to-Field mapping is executed there. Comments call this an intended M1 shape and recommend future in-circuit Keccak; comments do not implement it.

The draft recommends HKDF(issuerSecret, agentId || homeDomainId || capabilityIndex) for issuance and permits a unique unpredictable salt with at least 128 bits entropy. It does not fully specify an HKDF suite/encoding there. Neither commitment helper derives that issuance salt. No HKDF parameters are invented here.

## Public inputs and layer-specific fixes

Guard _buildPublicInputs passes exactly:

```text
[capabilityCommitment, agentId, homeChainId, homeDomainId,
 capabilityIndex, actionCommitment, executor, expiry, nullifier]
```

Numeric values occupy bytes32; executor is left-padded via uint160/uint256. cap.nullifier is index 8. Reference adapter and Noir declaration use the same nine-value order. Guard additionally checks executor against caller, expiry against timestamp, action hash against target/calldata, issuance and consumed state.

Executor and expiry are committed in draft and BOTH Solidity libraries, and present as public inputs. Noir receives them but does not bind them into its commitment derivation. Public-input equality is not semantic alignment: a proof can commit to an exact public vector while establishing the wrong relation among those values. A newly generated proof versus reuse of the same proof must also be distinguished.

Fresh-nullifier status: **PARTIALLY CLOSED**. The omitted-input wiring gap is fixed, but the intended proof derivation is not aligned. This is not evidence that the old fresh-nullifier replay succeeds unchanged, nor an impact demonstration. Under the shown Noir constraints C and N must be equal to one private Field; arbitrary fresh N with fixed C does not satisfy that circuit either.

## Compatibility and numerical counterexample

For salt=7, agent=5, chain=11155111, domain=1, index=3, action=bytes32(0x63), executor=address(1), expiry=1900000000:

| Lane | Nullifier | Capability commitment |
|---|---|---|
| draft/Solidity 8380 | 0x387e1b17665773c440b8c1e1091763c9b9c2d2733eeaeaf1fdac1d17aa957338 | 0x0ca20742a17fa240d3abf6146f61981ee649b937a992f87bb599c1c1899f88cf |
| reference 1953 | 0x53c376eeb2e70a0a6477d0db43a3c66bf9a66ccbeeccd7167ac2c8aba07e05fb | 0x684c5eb45dac7a158d87d48685f171345779cd4dcd06d5499bfcae37bf31ad08 |
| shown Noir with salt=7 | Field(7) | Field(7) |

The Keccak values were independently recomputed in the preceding STOP audit; current source bytes are identical. That computation is not Solidity or Noir proof execution. The current audit reuses the digest-checked evidence.

**No conforming proof path is demonstrated for a correctly draft-derived capability.** The published control cannot satisfy the shown Noir equations with its intended salt, and C != N also precludes another shared salt under faithful equality. Mock tests can accept those values because they never execute the circuit. This is not a proof of logical impossibility for every conceivable hash input/collision, nor a claim about a deployed verifier whose generated key has not been reproducibly linked to this source.

Full bytes32 values and Noir Field values require a specified injective representation/range strategy. The generated Honk file has scalar modulus 21888242871839275222246405745257275088548364400416034343698204186575808495617; arbitrary 256-bit digests cannot be assumed to fit. No modulo reduction is authorized as an equivalent encoding. Its 17 public-input count includes eight pairing entries: 17 - 8 = 9. That count is NOT a mismatch finding. Compiler/prover/VK linkage and a known-valid real proof remain missing closure evidence.

## Finality and classifications

At-most-once / not exactly-once is already explicit in draft Security Considerations. Residual phrases such as "unit of exactly once" remain elsewhere; they do not create a liveness guarantee. The finality/off-chain section is still **INTENDED**, not normative: live author posts [31](https://ethereum-magicians.org/t/29274/31) and [33](https://ethereum-magicians.org/t/29274/33) promise an update. Reorg-specific handling is forum clarification only. No threshold or consensus model is supplied by this audit.

Nullifier binding PARTIALLY ALIGNED; capability commitment MISALIGNED; executor PARTIALLY ALIGNED; expiry PARTIALLY ALIGNED; tag/domain MISALIGNED; hash primitive MISALIGNED; finality PARTIALLY ALIGNED (normative at-most-once, intended off-chain/reorg clarification). Overall MISALIGNED.

## RSI preservation and resumption

Verified unchanged 389 tracked hashes before/after generation. Immediately preceding normal/optimized logs show 430/430 PASS and the two outcome artifacts are byte-identical with 85 PASS. These are verified prior-run artifacts, not freshly rerun suites in this research-only audit. Prior 61 KILLED is retained verified history; no mutation execution is claimed now. Six prior STOP reports are byte-identical. No generic/domain code, schema or semantic exception was added. No external repository or forum content changed.

Phase 3D cannot resume until a pinned circuit/prover/verifier lane proves the intended byte-exact derivations, known-valid and negative vectors establish parity, and field/proof encoding is defined. See repair options and test-gap map. No narrowed implementation scope is silently substituted.

## Source ledger

Each linked immutable file below carries its evidence class. Normative draft, Solidity, proving implementation, reference implementation, tests and forum intent are not interchangeable. Source extraction and compatibility conclusions above are audit inferences from these exact artifacts.

- [SPEC.md](https://github.com/mzf11125/unclonable-agent-execution-credentials/blob/50f2ae1ddb85f02e55c7b48ae8c609b1fdda31c5/SPEC.md) — normative draft; SHA-256 `319e10c5f793daa7fb2da73e7698ee5606d28c66884ce029af28d9391e723cae`.
- [README.md](https://github.com/mzf11125/unclonable-agent-execution-credentials/blob/50f2ae1ddb85f02e55c7b48ae8c609b1fdda31c5/README.md) — documentation; SHA-256 `084ccc88a526f8b1726d60747dd7dfe122dad03e870533432f0eadc7ed1fd7a1`.
- [src/CoupledCredentialGuard.sol](https://github.com/mzf11125/unclonable-agent-execution-credentials/blob/50f2ae1ddb85f02e55c7b48ae8c609b1fdda31c5/src/CoupledCredentialGuard.sol) — contract; SHA-256 `bb786b808d8a60f8a194a8e39c2dab29802cb02bd51d2b36e8e011d9c2995b10`.
- [src/libraries/CapabilityCommitment.sol](https://github.com/mzf11125/unclonable-agent-execution-credentials/blob/50f2ae1ddb85f02e55c7b48ae8c609b1fdda31c5/src/libraries/CapabilityCommitment.sol) — contract; SHA-256 `41e6ea173d0ee0ac1c2b50d9a6f7f96d8c090e5935725f05150dbe3f2b4204b1`.
- [src/verifier/IVerifier.sol](https://github.com/mzf11125/unclonable-agent-execution-credentials/blob/50f2ae1ddb85f02e55c7b48ae8c609b1fdda31c5/src/verifier/IVerifier.sol) — circuit/verifier; SHA-256 `1b9275e0a24b9cdfbcce2f97121c73d27791806b0f1543501d839963b58f6e09`.
- [src/verifier/HonkVerifierAdapter.sol](https://github.com/mzf11125/unclonable-agent-execution-credentials/blob/50f2ae1ddb85f02e55c7b48ae8c609b1fdda31c5/src/verifier/HonkVerifierAdapter.sol) — circuit/verifier; SHA-256 `1b51a1fb1fbde6c73e90f514d5fc9bceaf051c5181958ce56678b92931eacbb5`.
- [src/verifier/HonkVerifier.sol](https://github.com/mzf11125/unclonable-agent-execution-credentials/blob/50f2ae1ddb85f02e55c7b48ae8c609b1fdda31c5/src/verifier/HonkVerifier.sol) — circuit/verifier; SHA-256 `314be3896d9fb0f62decf89bb0fcafad720f0d56966e9bb4ae5276551f95bbfb`.
- [src/mocks/MockVerifier.sol](https://github.com/mzf11125/unclonable-agent-execution-credentials/blob/50f2ae1ddb85f02e55c7b48ae8c609b1fdda31c5/src/mocks/MockVerifier.sol) — test/vector; SHA-256 `7106ef2fd5ac95319a960f8e15b4dc6fa75fbbb0ea59af7bbf4efe2c973243a6`.
- [noir/nullifier/src/main.nr](https://github.com/mzf11125/unclonable-agent-execution-credentials/blob/50f2ae1ddb85f02e55c7b48ae8c609b1fdda31c5/noir/nullifier/src/main.nr) — circuit/verifier; SHA-256 `8ee757e146b0b10d0f8f7f146b9eb5fc076ce154079f1f68839ba3e3bdcbb8bf`.
- [noir/nullifier/src/hash.nr](https://github.com/mzf11125/unclonable-agent-execution-credentials/blob/50f2ae1ddb85f02e55c7b48ae8c609b1fdda31c5/noir/nullifier/src/hash.nr) — circuit/verifier; SHA-256 `66b109dc22cc00e7118f446ac273bca317d1a567914921298665f5383ff5adb5`.
- [test/adversarial/Coupled.t.sol](https://github.com/mzf11125/unclonable-agent-execution-credentials/blob/50f2ae1ddb85f02e55c7b48ae8c609b1fdda31c5/test/adversarial/Coupled.t.sol) — test/vector; SHA-256 `169401df4eb87743970151ad05573701f6a547ed578b0aedb55c0ee22f77a2d7`.
- [ERCS/erc-8380.md](https://github.com/mzf11125/mzf11125-ERCs/blob/7068f2a2853504475d966c06c8e04ec6d546dbb8/ERCS/erc-8380.md) — normative draft; SHA-256 `b2435f8261ce64dab4cb8f222183fb5193353a1612b2934cfd9af8229736d6cd`.
- [assets/erc-8380/CoupledCredentialGuard.sol](https://github.com/mzf11125/mzf11125-ERCs/blob/7068f2a2853504475d966c06c8e04ec6d546dbb8/assets/erc-8380/CoupledCredentialGuard.sol) — contract; SHA-256 `5a719843b377b5e5c5b8b66e02a627480b0546d7d2ca6537c2f4ff9782f4cc71`.
- [assets/erc-8380/CapabilityCommitment.sol](https://github.com/mzf11125/mzf11125-ERCs/blob/7068f2a2853504475d966c06c8e04ec6d546dbb8/assets/erc-8380/CapabilityCommitment.sol) — contract; SHA-256 `4f9cb6de88d4bdf71b599bb1afa140336041b6f839ac3dd34946e4cac644e371`.
- [assets/erc-8380/IVerifier.sol](https://github.com/mzf11125/mzf11125-ERCs/blob/7068f2a2853504475d966c06c8e04ec6d546dbb8/assets/erc-8380/IVerifier.sol) — contract; SHA-256 `1b9275e0a24b9cdfbcce2f97121c73d27791806b0f1543501d839963b58f6e09`.
- [assets/erc-8380/IUnclonableCredential.sol](https://github.com/mzf11125/mzf11125-ERCs/blob/7068f2a2853504475d966c06c8e04ec6d546dbb8/assets/erc-8380/IUnclonableCredential.sol) — contract; SHA-256 `889a89e85727994973e9bea2a54c56372f6b2391eb55a2999d8bfe7807d441c0`.
- [assets/erc-8380/DomainRegistry.sol](https://github.com/mzf11125/mzf11125-ERCs/blob/7068f2a2853504475d966c06c8e04ec6d546dbb8/assets/erc-8380/DomainRegistry.sol) — contract; SHA-256 `42eaa245ea6462f89a77a31a8b501e78151bb865056bca7d16ede3098b9f3051`.
- [assets/erc-8380/test/ERC8380.t.sol](https://github.com/mzf11125/mzf11125-ERCs/blob/7068f2a2853504475d966c06c8e04ec6d546dbb8/assets/erc-8380/test/ERC8380.t.sol) — test/vector; SHA-256 `6d16a5cec7a5b552de0a870b2494a2a2578541bf66076601a81ad9f2e875a350`.
- [assets/erc-8380/test/Harness.sol](https://github.com/mzf11125/mzf11125-ERCs/blob/7068f2a2853504475d966c06c8e04ec6d546dbb8/assets/erc-8380/test/Harness.sol) — test/vector; SHA-256 `fe141b9f303fa9b82979067b80be5072c7d3569e66d8bf271e8eb4c7d0a1e0c5`.
- [assets/erc-8380/test/README.md](https://github.com/mzf11125/mzf11125-ERCs/blob/7068f2a2853504475d966c06c8e04ec6d546dbb8/assets/erc-8380/test/README.md) — test/vector; SHA-256 `5367c3af207331daaa046c45287d8555fac1a98589c33ec24c968f8fd160fbf8`.
