# TAS verified Workflow context to invocation mapping v0

Scope: source gate applicability plus controlled **read `getTask` dispatch**, not a signed exact-call intent or end-to-end agent execution. The synthesis unambiguously identified this component; canonical default branch is `feature/tas-poc`, not an invented `main`. It remains at `a344ef80f7c52c03b9183814d1874b8054639c3e`.

**context verified != invocation authorized != action executed**

Here “invocation admitted” means this source service reached its controlled SDK port after gate and supplied same-block membership checks. It is not proof of wallet ownership, chain consensus or action occurrence. No write/signing path is implemented.

## What source actually binds

| Field | Source-defined boundary |
| --- | --- |
| fingerprint | Exact accepted/current equality; supplied accepted source result, not recomputed source verification. |
| chain / network | Exact chainId string; source-test Anvil 31337. |
| RPC scope | Exact rpcUrl string; endpoint identity is not trustworthy chain evidence by itself. |
| Workflow target | Case-insensitive workflowAddress equality in gate; production resolver returns this address for the Workflow namespace. |
| exact block | Gate requires block_hash selector but does not require equality to old accepted block. Membership must match returned current block hash. |
| agent / caller | Configured agent_id must match supplied membership projection and is_member=true; read account uses current authentication_wallet. |
| method | Explicit registered getTask entry selects binding target. Unknown tool rejected. Gate does not cryptographically commit a method. |
| arguments / task | Source schema validates taskHash string; hex value is forwarded unchanged. Another valid taskHash is allowed, not a substitution failure. |
| policy / nonce / expiry / payment | No such gate binding established by this lane. No borrowed replay or settlement semantics. |
| execution | client.invoke is a controlled observation. The controlled SDK throws after recording dispatch; native EXTERNAL_UNAVAILABLE is preserved and no on-chain result is invented. |

Source: [src/core/workflow/sourceGate.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/src/core/workflow/sourceGate.ts); [src/core/workflow/operationService.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/src/core/workflow/operationService.ts); [src/core/workflow/contractAddressResolver.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/src/core/workflow/contractAddressResolver.ts).

## Fixture mapping

| Fixture | Cases and local validity | Expected relation | Claim boundary |
| --- | --- | --- | --- |
| 001 | matching control; no accepted context | dispatch / WORKFLOW_SOURCE_VERIFICATION_REQUIRED | supplied current validity alone does not admit invocation |
| 002 | same valid fingerprint, changed valid Workflow address | WORKFLOW_SOURCE_VERIFICATION_REQUIRED, no dispatch | wrong target cannot inherit acceptance |
| 004 | changed fingerprint; wrong member agent id; stale member block | gate rejection or AUTHORIZATION_DENIED | context acceptance alone does not establish member applicability |
| 005 | current exact block advances; membership follows current block | dispatch preserved | byte differences alone do not invalidate the protected tuple |
| 006 | allowed read dispatch followed by controlled SDK unavailability | invocation admitted; execution UNSUPPORTED | no occurrence inference |

001 has two cases, 004 has three; total **five fixture files / eight checks**. 003 omitted: no accepted-context commitment to method/arguments exists here. 007 omitted: gate acceptance is not single-use. No false negative is invented for a permitted second task or replay.

Mirror and target vectors derive from [test/unit/workflow/sourceGate.test.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/test/unit/workflow/sourceGate.test.ts). Membership/dispatch construction derives from [test/unit/workflow/operationService.test.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/test/unit/workflow/operationService.test.ts). Expected Python predicates are separately implemented tuple and membership obligations. They never call the TypeScript runtime, adapter, or expectation rows. Author independence is not established.

## Runtime, pinning and transport

Exact TypeScript files are preserved under evidence/tas/source. `source-runtime.mjs` is an offline esbuild 0.25.10 bundle of the three production exports, JSON codec, TasError and viem 2.55.19 getAddress closure. Build provenance and npm lock integrity are pinned; npm packages are not loaded or installed during evaluation. Dependency licenses are included. No external repository was modified.

The selected compiled subset is checked in existing Node 22.15 RSI jobs and an additional Node 24.19 TAS job (source package engine >=24 <25). This is not a build/test claim for the entire TAS package. Dependency build inputs and pinned source must be reviewed before repinning the bundle. Source drift is detected offline by exact commit-manifest/artifact digests and maps to UNSUPPORTED, including profile-wide atomic blocking; no live latest lookup occurs during evaluation.

Inputs remain ASCII and safe integers. The source's large agent id is a decimal **string**, not rounded into a number. This lane uses nonzero digit-only EVM source-test addresses and a 32-byte hex taskHash string; no silent Unicode, float, raw-byte, ABI or checksum coercion. Full arbitrary EVM transport and wallet signing are outside scope.

All generic core, schemas, comparator, taxonomy and prior domain files remain unchanged. Registration selects trusted static implementations only. Candidate mutation M2 (method commitment) and M7 (nonce) are inapplicable and unregistered; M1/M3/M4/M5/M6 are mapped to actual decision assertions. Setup failures cannot count as kills.

## Rebuild the frozen runtime (maintenance only)

From repository root, copy evidence/tas/package.json and package-lock.json into artifacts/tas-phase3a/runtime, run npm ci --ignore-scripts there, then node evidence/tas/build.cjs from root. Use an in-workspace npm cache. esbuild and viem versions/integrities are locked. The resulting source-runtime.mjs SHA-256 must equal the pin before any admission. The build was reproduced exactly locally; evaluation never invokes npm or fetches code.

Canonical SDK getTask reads getAgentTask from the selected contract and returns task/proven data. This lane does not execute it or trust a proven flag. Its controlled port deliberately fails after recording the exact argument/context transfer. No conclusion about a deployed task's existence, proven status, runtime bytecode, RPC consensus or wallet ownership follows.
