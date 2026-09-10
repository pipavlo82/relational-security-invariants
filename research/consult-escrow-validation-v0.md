# ConsultEscrow validation v0

Base RSI main: `43a7a4832344a0c5019774756fa2c8209f7517df`.
Local Phase 3B gates pass. Closure requires CI on the resulting commit; the final
handoff records that exact HEAD and CI outcome. No public release, tag or PR.

| Gate | Before | After |
|---|---:|---:|
| Full tests | 366 PASS | 398 PASS |
| python -O | 366 PASS | 398 PASS |
| Conformance checks | 72 PASS | 79 PASS |
| Mutations | 50 KILLED | 55 KILLED |
| Other conformance/mutation statuses | 0 | 0 |
| Prior outcome diff | 0 | 0 |
| Prior mutation record diff | 0 | 0 |
| Previous tracked-file hashes preserved | 290 | 290 |
| Generic/core/schema/comparator/taxonomy changes | 0 | 0 |
| Semantic exceptions | 0 | 0 |

All 72 prior rows remain byte-identical, covering legacy, Crystal, RVR, TSEI, PQ
and TAS. All prior 50 mutation records, including collateral/error data, are
unchanged. The legacy mutation tool's implementation-hash inventory expands to
include new files; this is not a change in prior mutation records. The six-family
pipeline uses existing registries, independent admission and comparator unchanged.
Static anti-coupling passes. The structured report rerun is deterministic, and
canonical compiler/bundle outputs reproduce exactly.

## Fixtures and real decision points

Five fixture documents contain seven cases:

- CE-RSI-001: control and wrong attestor. Control releases the stored amount to
  stored provider; wrong attestor is rejected with `bad attestor sig`.
- CE-RSI-002: wrong job and wrong result. The original signature remains locally
  valid on the original tuple; substituted tuples do not acquire release authority.
- CE-RSI-006: repeated release fails `not open`; no second provider balance delta.
- CE-RSI-007: source-backed relayer mirror preserves the exact semantic result.
- CE-RSI-008: checkpointed preflight is eligible but retains no event, balance
  change or Released status; execution remains UNSUPPORTED for that case.

CE-RSI-003/004/005 are deliberately not fabricated. Amount/provider are immutable
job-state values, not independently signed release arguments. Chain and deployment
address are not signed. These gaps are documented rather than converted into PASS
expectations. Scope details and every source-file digest are in
[signature scope](consult-escrow-signature-scope-v0.md) and
[source map](consult-escrow-source-map-v0.json).

| Mutation | Mapped decision | Result |
|---|---|---|
| CE-M1 | Wrong job accepted when commitment uses original job endpoint | KILLED |
| CE-M5 | Signer guard removed; wrong attestor incorrectly accepted | KILLED |
| CE-M6 | Preflight eligibility promoted to retained local execution | KILLED |
| CE-M7 | Non-protected relayer change incorrectly rejected | KILLED |
| CE-M8 | Open guard removed; second release incorrectly allowed | KILLED |

All mapped failures occur at intended test assertions after successful source
load, fixture validation, admission and actual EVM execution. No setup/import/
schema failure is counted as a kill. Collateral failures are recorded separately
in the JSON. No amount/recipient/domain-separator mutations are manufactured.

## Source and independence

- agent-ercs main: `01283ca57305f915afb560d23359a27fd748eb5a`.
- agent-sdk main: `e41b117893fb56bc869922de378daf91aad63def`.

Both canonical source heads were reverified unchanged during this pass. External
repositories remain read-only. Contract/interface, source tests, Foundry settings,
README and SDK recomputation/client paths are pinned. The SDK helper's resultText
emission comment disagrees with the actual resultHash event ABI; contract and
interface govern this mapping. No broader state-channel or pre-outcome ordering
claim is made.

Actual uses pinned Solidity compiled to Cancun bytecode on JavaScript EVM,
including ecrecover and local transfers. Expected uses independent Python integer
Keccak/secp256k1 recovery and state obligations. No semantic helper is shared.
Different language/code paths do not establish independent authorship or a full
cryptographic audit. The Python oracle is conformance code, not production crypto.

ASCII fixture transport preserves bytes32/addresses/signatures as validated hex
and uint256 amounts as decimal strings. The 1 ETH amount is greater than 2^53;
no unsafe JSON numeric conversion occurs. Source UTF-8 comments remain exact
pinned bytes. Arbitrary recipient code, RPC chain state, transaction inclusion,
finality, gas economics, refund paths and mainnet execution are outside this lane.

## Supported claim and remaining gaps

RSI validates the job/result authorization boundary **within the supplied
contract-local escrow state**. A signature on another job/result does not confer
release eligibility, and eligibility is distinct from execution evidence.

Isolated retained EVM execution is observed through status, balance delta and log.
Mainnet settlement occurrence remains a separate unvalidated claim. Deployment/
chain replay resistance is not established by this signature preimage; no
exploitability conclusion is asserted. Deadline enables refund rather than
expiring the signature. All prior unsupported domain scopes remain unsupported.

This is not all escrow security, end-to-end payment security or universal
settlement correctness. No verify-layer implementation was started.

Generated third-party bundle/license whitespace is retained for exact byte
reproducibility. The whitespace check excludes only those two generated files;
all other added files pass. This is a formatting note, not a semantic exception.
