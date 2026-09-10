# ERC-8380 exact formula matrix

Pins, complete formulas, encoding and file digests: [alignment audit](erc8380-commitment-alignment-v0.md) and [machine report](erc8380-commitment-alignment-v0.json). C8380/N8380 mean the exact tagged Keccak formulas there; C1953/N1953 use identical packing with the old tags. s is private salt (bytes32 in Solidity, Field in Noir). Solidity column means current ERC draft assets; reference column means the separately linked implementation repository.

| Semantic object | Draft formula | Solidity formula | Reference formula | Noir formula | Exact match? | Mismatch class | Security consequence |
|---|---|---|---|---|---|---|---|
| Capability commitment | C8380 | C8380 | C1953 | s | No | MISALIGNED: domain and primitive | No cross-layer proof of the declared envelope |
| Nullifier | N8380 | N8380 | N1953 | s | No | MISALIGNED: domain and primitive | Public-value binding does not prove tagged derivation |
| Executor | 32-byte executor in C | same; sender checked | same shape, old tag | pub Field passed to ignored parameter | Partial | PARTIALLY ALIGNED | Public presence is not commitment derivation |
| Expiry | 32-byte expiry in C | same; timestamp checked | same shape, old tag | pub Field passed to ignored parameter | Partial | PARTIALLY ALIGNED | No commitment constraint on expiry in shown Noir |
| Target/action | A = K(abi.encode(target,callData)); A in C | action equality checked; A in C | same shape, old tag | action pub Field ignored by hash | Partial | PARTIALLY ALIGNED | Action equality in Guard does not repair proof opening |
| Public nullifier | index 8 of 9; derived equality required | cap.nullifier at index 8 | same at index 8 | index 8; assert N == s | Order yes, semantics no | PARTIALLY ALIGNED | Old omitted-input gap fixed, derivation remains wrong |
| Domain tag | K(ERC-8380/.../v1) | same | K(ERC-1953/.../v1) | none | No | MISALIGNED | Different cryptographic domains, no compatibility alias found |
| Hash primitive | Keccak-256 | keccak256 | keccak256 | identity function | No | MISALIGNED | No cryptographic envelope binding in helper |
| Encoding/order | fixed 32-byte packed words; nine-word C | same abi.encodePacked | same word order, different tag | Field scalars; no byte packing | No | MISALIGNED | Full bytes32-to-Field relation unspecified |
| Salt | private bytes32; unique unpredictable issuance salt | bytes32 helper argument | bytes32 helper argument | private Field; returned directly | Partial | PARTIALLY ALIGNED | Not HKDF or Keccak in Noir; no silent byte reduction |

No component's public-input declaration establishes cryptographic equivalence with another component's hash. Guard consumes exactly the public nullifier now; the missing relation is derivation parity. No fresh-nullifier exploit is asserted from this matrix.
