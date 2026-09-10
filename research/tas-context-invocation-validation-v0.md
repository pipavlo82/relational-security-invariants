# TAS verified-context to invocation validation v0

RSI base: `9aed903353035ca9e30f6068ab67ea9293ab416f`, private main. Scope is **conditional verified Workflow applicability to controlled read getTask dispatch**, not a signed call-intent protocol or end-to-end execution security.

## Results

- Before: 337 tests and 337 optimized tests; 64 prior checks; 45 mutation kills.
- After: 366 tests and 366 optimized tests; TAS 8 PASS / 0 FAIL / 0 INVALID_FIXTURE / 0 UNSUPPORTED; combined 72 PASS.
- TAS-M1/M3/M4/M5/M6: 5 KILLED. Total 50 KILLED; SURVIVED/VACUOUS/NOT_APPLIED zero. Collateral failures remain in the JSON mutation traces and are not counted as mapped kills.
- Exact prior conformance report diff 0; all 45 prior mutation records unchanged.
- All 244 protected pre-existing tracked hashes unchanged. RSI core, all legacy schemas, generic runtime/comparator/taxonomy and previous four domain implementations unchanged. No semantic exception.
- Deterministic report rerun and Node 22.15 / Node 24.19 exact TAS outcome comparison pass. No TAS-specific generic branch.
- Exact pushed-HEAD CI is a completion gate recorded in GitHub Actions and delivery, not a predicted self-referential commit claim here.

## Established relation

An accepted source fingerprint remains applicable only to the matching chainId/rpcUrl/Workflow address. The current context must have an exact block selector. A newer exact block is allowed when the protected tuple remains the same, while membership must resolve at that returned current block for the configured agent. The canonical registered getTask entry constructs the read invocation. Wrong Workflow, fingerprint, member agent, or membership block fails before the controlled SDK port.

Five fixture files hold eight cases: 001 control/unaccepted, 002 target substitution, 004 fingerprint/member/block substitutions, 005 mirror, 006 dispatch/occurrence separation. All negatives keep locally well-formed components; they fail source relation checks rather than setup/parsing. The mirror comes directly from the canonical sourceGate test, not invented byte equivalence.

The SDK port records dispatch and then intentionally throws. Source EXTERNAL_UNAVAILABLE is retained. This is not a setup failure: it happens after the mapped native invocation boundary, and the admitted expectation explicitly requires that native behavior. No transaction/receipt/proven flag is synthesized. Top-level PASS is conformance to that bounded observation.

## Mutations and scope

| Mutation | Mapped boundary |
| --- | --- |
| M1 | Replace supplied current target with accepted target, wrongly allowing original target substitution |
| M3 | Replace member agent id with configured agent id, suppressing membership mismatch |
| M4 | Automatically accept current context when no acceptance exists |
| M5 | Promote observed dispatch to EXECUTED |
| M6 | Reject changed exact block despite unchanged protected tuple |

Each mapped test executes the real registry/admission/adapter/comparator path and rejects setup diagnostics before its decision assertions. M2/M7 are unregistered, not fake kills: no exact method/task commitment or nonce semantics exist in this gate. Unknown tool selection is tested separately; changing a valid taskHash is permitted by source and is not relabeled a negative.

## Evidence and limitations

TAS default branch `feature/tas-poc` at `a344ef80f7c52c03b9183814d1874b8054639c3e`. Connected SDK `e41b117893fb56bc869922de378daf91aad63def`; agent-ercs `01283ca57305f915afb560d23359a27fd748eb5a`. Exact source files/digests and fixture mappings: [source map](tas-context-invocation-source-map-v0.json), [mapping](tas-context-invocation-mapping-v0.md), [ownership](tas-relation-ownership-v0.md).

Actual uses pinned production TypeScript compiled with pinned dependencies; expected uses separately implemented Python tuple/membership obligations. No adapter/predictor calls or expected-row access are shared. Different languages/code paths do not prove author independence or rule out common interpretation errors.

Context acceptance and membership are supplied evidence; source/deployment/chain authenticity, wallet ownership and execution occurrence remain unverified. The real SDK/contract is inspected but not run. ASCII/safe-integer transport remains; agent id is its source-defined decimal string, taskHash is hex, source-test addresses are a declared digit-only subset. No Unicode/float/raw-ABI coercion or fake proof/policy/state was added.

All external repositories remain unchanged. No stronger RVR, TSEI or PQ capability is unlocked. The additional reusable family is verified-context applicability at the TAS-side dispatch boundary under controlled dependencies; it does not close all Trustless AI execution paths.
