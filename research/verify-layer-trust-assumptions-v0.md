# verify-layer trust assumptions v0

Proof validity != supplied-root binding != header authority != downstream authority.

* Source `RpcHeaderSource` explicitly reports `RPC-TRUSTED`; header authority is supplied, not independently established.
* `LightClientHeaderSource` is an unwired throwing stub. Consensus signatures/checkpoints and chain finality remain UNSUPPORTED.
* `finalized` is an RPC query tag. A returned block number/hash is not consensus evidence. No root-to-block-hash, chain ID, network, provider authentication, epoch or historical-finality verification is implemented here.
* The proof establishes account inclusion/balance under a supplied root. It does not prove contract behavior, execution, provenance, eligibility, spending authority, or current canonical-chain balance.
* Correct root binding and correct claimed balance are separate checks. A matching balance under a wrong root still fails the source `verified` conjunction.
* The only deployed/consumer material inspected is source discovery in primitives and verify-layer's own demo. No live production downstream policy is validated.
* The original source's statement about a header swap being the only remaining step to full trustlessness is source commentary, not an RSI conclusion.
* Primitives `check.py` independently warns that RPC transport/endpoint corroboration is not chain authority; it does not implement the missing header verifier.
* Raw RPC observations are pinned for reproducibility, not upgraded to authority by freezing them. Explicit repin/revalidation is needed for source drift. Conformance performs no network access or credential lookup.
* Source exceptions are narrowly recognized; arbitrary errors cannot masquerade as relation rejection. MPT coverage is this account inclusion/path negative, not exhaustive MPT fuzzing or storage proof validation.

A top-level PASS establishes admitted expectation agreement. Internal header and downstream authority remain UNSUPPORTED, including on the control and mirror-positive.
