# ERC-8380 test-gap and future prove-can-fail map

Evidence: draft assets/erc-8380/test/ERC8380.t.sol and Harness.sol at 7068f2a2853504475d966c06c8e04ec6d546dbb8; reference test/adversarial/Coupled.t.sol and src/mocks/MockVerifier.sol at 50f2ae1ddb85f02e55c7b48ae8c609b1fdda31c5. Full SHA-256 ledger is in the alignment audit. This is source inspection, not a fresh Foundry/Noir test run.

Draft _cap uses the library under test. BindingVerifier.issueProof registers keccak(proof) -> keccak(abi.encode(publicInputs)); verify compares that registered vector. It checks no witness or cryptographic circuit. Reference MockVerifier returns true for unlocked proofs, or compares vector hashes when lockProof is used. Its adversarial test constructs 1953 preimages directly, independently of the library call but from the same source formula. Neither lane is an author-independent cryptographic oracle.

Draft test_11_CommitmentParity compares the Solidity helper with hard-coded numeric expected C/N for the published vector; this IS a useful non-tautological Solidity regression. It would catch changing that library's tag, primitive, order, executor inclusion or expiry inclusion for the unequal chosen fields. Its name does not mean it executes the Noir circuit. Reference-local test success cannot establish 8380/1953 interoperability.

| Boundary | Existing coverage | Missing coverage | Proposed minimal conformance/mutation and intended kill point |
|---|---|---|---|
| Domain tag | test_11_CommitmentParity hard-coded 8380 vector catches changing draft Solidity tag | No cross-repo/circuit parity execution; reference tests use 1953 tags | A: alter TC/TN; fixed independent vector equality must fail |
| Salt passthrough | No Noir execution in inspected Solidity tests | BindingVerifier/MockVerifier never evaluate hash.nr | B: replace hash with s; circuit witness constraints for independent C/N must fail |
| Field order / primitive | test_11 catches Solidity changes against frozen expected digest | No generated-proof lane proving identical circuit preimage | C: swap two unequal words; circuit parity assertion must fail |
| Executor | test_07_ExecutorOrExpiryTamper and reference test_Coupled_ForgedExecutor_Reverts bind a vector | Fixed-vector rejection is not salt-to-envelope proof | D: omit executor; proof under changed executor/fixed issued C must fail |
| Expiry | test_07_ExecutorOrExpiryTamper and reference test_Coupled_ForgedExpiry_Reverts | Same vector-lock limitation | E: omit expiry; changed expiry/fixed issued C must fail |
| Nullifier derivation | test_11 checks Solidity N; test_08_NullifierSubstitution checks vector lock | No circuit-produced N under correct tag verified on-chain | F: alter nullifier derivation; independent N witness constraint must fail |
| Fresh Guard nullifier | test_08 and reference test_Coupled_ForgedNullifier_Reverts exercise Guard mismatch | No real proof/VK linkage tested | G: same real proof + new cap.nullifier; verifier/Guard BadProof must execute |

Future minimum lane: independent fixed byte preimages and expected digests; execute Solidity and Noir with the same witness/envelope; generate a real proof with pinned compiler/prover/VK; verify the exact nine public values in the real Guard. Test each field with distinct nonzero values and canonical encoding, and test out-of-field bytes without silent coercion. Only after an unmodified real control passes may A-G be classified as mutations. A failing setup, compiler import, serialization rejection or baseline-red circuit is VACUOUS, never KILLED. For D/E, hold the issued commitment fixed and regenerate a proof with substituted executor/expiry; a mere same-proof-vector mismatch does not prove envelope hashing is load-bearing.

No new mutations, fixtures or tests are implemented here. Finality remains a separate policy/evidence lane rather than a hash test.
