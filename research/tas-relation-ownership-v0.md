# TAS relation ownership v0

| Responsibility | Owner | Evidence / boundary |
| --- | --- | --- |
| Declare accepted context shape | TAS VerifiedWorkflowContext and source gate | fingerprint, chainId, rpcUrl, workflowAddress, exact block selector |
| Produce verified context | TAS source verification path; gate receives accepted result | Source authenticity/deployment recomputation outside this fixture lane |
| Consume gate result | TAS WorkflowOperationService | assertCurrent is first action before caller input/binding inspection |
| Select method and arguments | TAS operation registry + JSON schema + binding argument order | Canonical generated getTask manifest entry, not arbitrary manifest authorization |
| Resolve target | TAS WorkflowContractAddressResolver | Workflow namespace maps to verified workflowAddress |
| Resolve member/account | same-block memberResolver and read-account factory | Supplied controlled projection; no independent chain proof |
| Construct SDK invocation | TAS operationService / AgentSdkBindingClient contract | verified chain/RPC/contract, account, ordered taskHash |
| Execute SDK/network action | agent-sdk / underlying provider | Replaced by controlled observation; not validated as execution |
| Establish expectation | RSI separate Python predictor + atomic admission | Pinned expectations alone cannot authorize truth |
| Accidental overclaim | caller/UI/consumer | A verified fingerprint is not a signed call, member projection is not independently verified authority, dispatch is not occurrence |

TAS canonical `a344ef80f7c52c03b9183814d1874b8054639c3e`; SDK canonical `e41b117893fb56bc869922de378daf91aad63def`; agent-ercs canonical `01283ca57305f915afb560d23359a27fd748eb5a`. All read-only. Exact used paths and digests are in the source map. The connected SDK implementation is not executed; this closes only the TAS-side dispatch boundary under controlled dependencies.
