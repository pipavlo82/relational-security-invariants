# trustless-ai · verify-don't-trust layer (sketch v0)

The piece that makes a **trustless-ai wallet** trustless: instead of *trusting* an RPC's answer for a
balance, it **proves** it. Takes the RPC's `eth_getProof` (EIP-1186 Merkle-Patricia proof) and verifies it
against the block's `stateRoot`, so a lying RPC can't forge a balance without breaking keccak.

## The trust boundary (stated honestly)
- **Account state = proven, not trusted.** Given a `stateRoot`, the balance/nonce/storageRoot/codeHash are
  verified by the Merkle-Patricia proof.
- **Header still from the RPC in v0.** The `stateRoot` comes from the block header, which this sketch fetches
  from the RPC. A full trustless client gets the header from a **consensus light client** (sync committee) —
  swapping the header source is the *only* remaining step to full trustlessness. The state proof is done.

## Two independent defenses (both prove-it-can-fail in the demo)
- **(A) Binding** — `keccak(proof[0]) == block.stateRoot`. Stops an RPC handing a self-consistent proof
  rooted at a *fake* state. Demo: flip one bit of the expected root → **rejected**.
- **(B) MPT proof** — the Merkle-Patricia path for `keccak(address)` must verify. Stops any tampered node /
  forged balance. Demo: corrupt one byte in the account leaf → **rejected** ("Invalid proof provided").

Covers both **account state** (balance/nonce) and **contract storage** (any slot / token balance), each
proven against the state root — storage is chained: `state root → account.storageRoot → slot value`.

## Demo output (live mainnet, WETH)
```
PROVEN  balance = 2,030,382.95 ETH   bound-to-header YES   claim==proof YES  ==> ✅ VERIFIED
[tamper A] wrong stateRoot            ==> ✅ REJECTED (binding)
[tamper B] corrupt account leaf byte  ==> ✅ REJECTED (MPT proof)
[storage] WETH slot 2 (decimals)=18   chain of custody intact  ==> ✅ VERIFIED
```

## Run
```
npm install                       # @ethereumjs/mpt @ethereumjs/rlp @ethereumjs/util @noble/hashes
# needs an archive RPC key at ~/.claude/alchemy_key (mainnet)
node verify.mjs
```

## Next steps (toward the wallet MVP)
1. ✅ **Storage-slot proofs** — done (verify a contract var / token balance, chained to the account root).
   *(The L1/L2 seam is now concrete in code: header sources are pluggable — `RpcHeaderSource` today,
   `LightClientHeaderSource` is the documented drop-in. Swap the source and the header trust label changes;
   the L2 state proof is untouched.)*
2. **Consensus light-client header source (L1)** — the pluggable slot exists (`LightClientHeaderSource`);
   wiring `@lodestar/light-client` (bootstrap → sync-committee verify → execution stateRoot) drops straight
   in and flips the header from `RPC-TRUSTED` to `RE-DERIVED`. Needs a beacon node exposing light-client
   REST endpoints. Get the `stateRoot` from a sync-committee light client
   (helios-style) so the header isn't trusted either → *full* trustlessness.
3. ✅ **Trust-tier disclosure** — done: structured `trust` object labels the *kind* of each answer —
   state `RE-DERIVED` (MPT proof, no circuit trusted) vs header `RPC-TRUSTED` (v0). The marker travels with
   the value; verification kind (re-derive vs proof-attest vs rpc-trust) is never collapsed to one ✓.
4. **Compose our live primitives** — ERC-8373 PQ keys (`PqBindingAnchor` + `/pq/wallet`) + agent actions
   (`AgentMarketEscrow`, `MCPEntitlementRegistry`). Two of three wallet pillars already live.

v0 sketch, open (CC0) — fits the NLnet/EUDI verify story (this *is* the novel piece of that submission).
