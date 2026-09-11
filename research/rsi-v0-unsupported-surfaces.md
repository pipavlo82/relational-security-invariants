# RSI v0 unsupported surfaces

| Family | Unsupported / unvalidated capability |
|---|---|
| Crystal Receipt | Provenance authority, Lane K, broad ReceiptOS semantics |
| RVR | Cryptographic signatures / authenticated transition chain |
| TSEI | Provenance authority: Object A/B, oracle, nonce and attribution operands unavailable |
| PQ | Authenticated transition chain, independent anchor verification; SLH-DSA artifact / ML-DSA label mismatch preserved |
| TAS | Arbitrary method/action authorization, source-context authenticity, execution occurrence |
| ConsultEscrow | Cross-deployment/chain replay security, chain inclusion/finality, hostile recipients, end-to-end payments |
| verify-layer | Consensus/header authority, finality, storage lane, broad downstream claim |
| ERC-8354 CAPV | Full Guard acceptance, executor authorization, domain/root policy and execution occurrence |
| ERC-8312 Aggregate Budget | Non-bypassability, asset movement, cross-chain/subtree budgets and authoritative chain state |
| ERC-8299 reference application | Action authorization/occurrence, anchor authority, judgment soundness, raw-to-canonical transform and conditional execution |
| ERC-8380 | Entire new validation lane blocked by the pinned draft/prover commitment alignment audit; not counted as a validated family. |

No universal security framework, all-repository verification, end-to-end execution/payment security, consensus/finality correctness, fully independent oracle, or mathematical novelty claim is supported. Unanalyzed ecosystem edges remain untested.
