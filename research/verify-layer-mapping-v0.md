# verify-layer mapping v0 — Phase 3C

Scope: source `verifyAccount`, account MPT path, supplied stateRoot, and RPC claimed balance. Source is a sketch, not a consensus verifier. No external repository was modified.

The synthesis resolves `trustless-ai/verify-layer/verify.mjs` unambiguously. Canonical main is `84afc4b738dc37269089c858404eed8086435f5d`; `trustless-ai/primitives` main is `6b39e9540d4bd0a78decb588c0a8e328c303f208`. Exact bytes, hashes and evidence classifications are in `verify-layer-source-map-v0.json` and `evidence/verify-layer/source-pin.v0.json`.

## Actual protected relation

`keccak(accountProof[0]) == supplied stateRoot`; independently traverse MPT at `keccak(address)`; decode account balance; require RPC claimed balance equal proven balance. `verified` combines root binding and balance agreement after successful path verification. Neither the chain nor the block hash is authenticated. Account address is a trie key, not a verified deployment identity or code behavior.

| Fixture | Source function/check | Supported observation |
|---|---|---|
| VL-RSI-001 | checkAccountProof / verifyAccount | account inclusion and supplied-root/claimed-balance match |
| VL-RSI-002 | checkAccountProof boundToHeader / main tamper A | unchanged account proof fails different supplied stateRoot |
| VL-RSI-005 | checkAccountProof key / verifyMerkleProof | unchanged original proof does not establish alternate account path |
| VL-RSI-006 | verifyAccount accountProof.map(hexToBytes) | hex digit case changes preserve exact decoded proof bytes |
| VL-RSI-007 | RpcHeaderSource / LightClientHeaderSource / trust | verified state remains RPC-TRUSTED at header layer |
| VL-RSI-008 | verifyAccount claimMatchesProof | correct account/root cannot authorize a substituted RPC balance |

VL-RSI-002 substitutes another real provider-returned 32-byte stateRoot, keeping the entire original proof and account fixed. That proof still verifies under its original root. VL-RSI-005 substitutes an address while preserving original proof bytes; the source MPT implementation throws its exact `EthereumJSError: Invalid proof provided`. Only that recognized verification exception is mapped to `MPT-REJECTED`; setup/import/other errors remain availability failures, never successful mutation kills. This negative establishes failure for the requested path, not invalidity of the original proof.

VL-RSI-006 changes hex letter case in proof nodes. Source `hexToBytes` decodes the same bytes; no invented audit field is used. VL-RSI-007 deliberately repeats the valid account relation to isolate the non-promotion obligation. VL-RSI-008 changes only claimed balance by one wei. It does not claim a consensus-trusted header exists.

VL-RSI-003/004 are omitted: number/hash/chain rejection would invent source behavior. The header number selects the RPC proof query, but the source does not independently establish number-to-root or hash-to-root authenticity. VL-M3/M4/M8 are consequently inapplicable; they are not registered. VL-M5 covers account-path identity, not cross-chain deployment assurance.

## Real evidence and reproducibility

The source repository has no frozen proof corpus or tests; its `main` demo requests live WETH proofs. RSI captured a real EIP-1186 response from public dRPC, for exact returned block 25949241, after requesting `finalized`. Header and response raw JSON are frozen, with hashes. The selected stateRoot is `0x3cb08f43bb7e9249e250d889871d113a5799264ccff284bf71179f33217481a8`. Header block hash is provider-reported only. PublicNode supplied the alternate root; its proof request failed its proof-window limit. This is not evidence of canonical-chain disagreement or finality.

The actual lane executes literal upstream function bodies with RPC replay replacing only live transport, credentials and demo entry point. Pinned EthereumJS 10.1.3 and Noble hashes 2.4.0 execute Keccak/RLP/MPT. Upstream had ranges and no lock; RSI freezes a compatible dependency lock and offline bundle. No packages or network are loaded at conformance runtime. `build.cjs` builds the checked-in bundle from `build-entry.mjs` and the pinned lock installation in `artifacts/vl-phase3c/runtime`. Bundle and source are hash-admitted before execution.

The predictor separately implements Python Keccak, canonical RLP and MPT path obligations. It never calls JavaScript or the adapter, and is checked against known Keccak answers. This is language/code-path separation and source-derived reimplementation, not demonstrated author independence, formal proof, or general proof-system assurance.

## Carrier and lossiness

The existing ASCII/safe-integer JSON transport carries proof bytes as validated even-length hex strings and block/balance quantities as hex strings. Actual wei output is an exact decimal string (2057762111636750387534361 for the control). No unsafe number conversion enters the comparator. The upstream derived `provenBalanceEth` float is explicitly excluded as display-only; exact wei remains. Full RPC JSON, other account outputs and raw bytes are evidence, not silently coerced profile slots. This is a partial projection, not all verify-layer semantics.

Malformed profile shape maps to INVALID_FIXTURE. Unknown exact version or source/bundle drift maps to UNSUPPORTED. Admitted expected/actual disagreement maps to FAIL. A PASS with `headerAuthority: UNSUPPORTED` means conformance, not independently trusted chain state.
