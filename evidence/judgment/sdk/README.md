# ERC-8299 — WYRIWE: Input Provenance for AI Inference (TypeScript)

**Recompute-to-verify: YES.**

Both `IWyriweAttestation.verify()` (L3 — input provenance) and `IJudgmentExecutionAttestation.verify()` (L4 — judgment chain-of-custody) are deterministic, callable-by-anyone, `view` functions that check EIP-712 signatures against a known attestor address. Calling the contract yourself and getting back `valid` is independent recomputation — the same trust model as re-checking a signature or Merkle proof. You trust the (public, auditable, immutable) checking procedure once, not each party who invokes it.

For this reason, both clients expose `verify()` as a **read-only simulated call** (no gas, no funded key needed).

## Two interfaces, two clients, one ERC

| Interface | Layer | Client |
|-----------|-------|--------|
| `IWyriweAttestation` | L3 — input provenance | `WyriweAttestationClient` |
| `IJudgmentExecutionAttestation` | L4 — judgment chain-of-custody | `JudgmentExecutionClient` |

Both share the same EIP-712 domain (`ERC8004AttestationGateway` / v1) by design — see the ERC's README.

## API

### WyriweAttestationClient (L3)

- `verify(attestation, signature)` — simulated call, no gas: checks the EIP-712 signature against the known attestor.
- `proofSystem()` — returns `"attestation/wyriwe"` for conforming implementations.

### JudgmentExecutionClient (L4)

- `verify(attestation, signature)` — simulated call, no gas: checks the EIP-712 signature against the known attestor.
- `proofSystem()` — returns `"attestation/judgment"` for conforming implementations.

## Layer 2 — Pure recompute

**Pure recompute: YES (two functions).**

Even beyond the on-chain `verify()`, two deterministic computations can be reproduced off-chain from public inputs:

1. **`computeRawInputHash(rawInputHex)`** — `raw_input_hash = keccak256(raw_user_input)` (ERC-8299 Section 45). Golden vector: `raw_input_hex: "0x68656c6c6f"` → `"0x1c8aff950685c2ed4bc3174f3472287b56d9517b9c948127319a09a7a36deac8"`.

2. **`computeSanitizationPipelineHash(specCid, rawInputHash)`** — `sanitization_pipeline_hash = keccak256(utf8(cid) || raw_input_hash)` (ERC-8299 Section 46). Golden vector: `spec_cid: "ipfs://QmccvoM6aRVgZ2dtFWvT6Wm3DmTvoAUHHotK7uQufnStVR"`, `raw_input_hash: "0x1c8aff950685c2ed4bc3174f3472287b56d9517b9c948127319a09a7a36deac8"` → `"0x5798efed4aa92f96a0622fc30268042b067294bdb5fd06f599bf8d84fd5d734b"`.

These live in `recompute.ts` and are tested against golden conformance vectors from `recompute-kit/conformance/agent-flow.vectors.json` (steps `wyriwe/raw` and `wyriwe/pipeline`). The recompute tests are pure function calls with no RPC, no anvil, and no deployed contract.

See `recompute.ts` for the implementation and `test/verify/ERC8299/recompute.test.ts` for tests.
