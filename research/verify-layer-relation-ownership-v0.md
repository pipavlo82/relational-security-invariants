# verify-layer relation ownership v0

| Role | Pinned owner | Boundary |
|---|---|---|
| Declare account/root rule | verify-layer `checkAccountProof` at 84afc4b738dc37269089c858404eed8086435f5d | root hash equality plus Keccak(address) MPT traversal |
| Produce proof | Ethereum RPC `eth_getProof`; captured dRPC response | supplied data, not trusted authority |
| Produce header/root | RPC `eth_getBlockByNumber` | `RpcHeaderSource` takes stateRoot on faith |
| Verify account relation | verify-layer plus EthereumJS/Noble dependencies | state conditional on supplied root |
| Establish consensus context | nobody in inspected runnable lane | `LightClientHeaderSource` throws, unwired |
| Consume account result | verify-layer `main` demo output | no pinned production wallet decision consumer identified |
| Discover component | primitives registry/check.py at 6b39e9540d4bd0a78decb588c0a8e328c303f208 | repository/surface checks; not consumption of MPT result |
| Adversarial conformance | RSI profile, separate expectation, actual adapter | prevents tested false promotions in observation comparison |

The cross-repo edge is currently discovery/composition intent, not proof that primitives or a production wallet enforces this verification result. The largest promotion risk is treating `RE-DERIVED` state as independently trusted header or downstream balance authority. Source trust tier disclosure is retained. No production consumer was invented.

Source file hashes and exact identifiers: `verify-layer-source-map-v0.json`. No external repository was modified.
