# Trustless AI repository and relation matrix v0

Inspection RSI HEAD `5e964b0335b42d1f8e298bb8b6afdbead6254f5a`. Source citations resolve exact commits. Status is surface-specific, never whole-repo assurance. Mutation coverage numbers in repo rows overlap shared domain mappings and must not be summed.

| Repo/component | Canonical HEAD | Primary role | Protected relations | Producer | Consumer | RSI profile / status | Mutation coverage | Gaps / next fixture |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| trustless-ai/agent-ercs (main) | 01283ca57305f915afb560d23359a27fd748eb5a | Solidity interfaces and a concrete ConsultEscrow base; interface declarations are not proof of deployed enforcement | agent/proof-profile authorization; workflow task/reply/run binding; job/result/attestor settlement binding; chain/domain/action commitment; immutable source-token provenance versus live ownership | contract implementations; signers; workflow emitters | SDK clients; workflow agents; escrow beneficiaries |  / mapped but unvalidated | 0 | No RSI execution of these contracts; deployment/audit descriptions not independently verified here Next: job-bound settlement; policy-action replay scope |
| trustless-ai/agent-sdk (main) | e41b117893fb56bc869922de378daf91aad63def | Typed off-chain clients and pure recomputation; integration index explicitly is not endorsement | task/reply hash preimage; settlement commitment; policy action/verdict digest; issued convention to reputation value | SDK recompute functions and callers supplying evidence | TAS reviewed SDK bindings; downstream verifiers |  / mapped but unvalidated | 0 | Pure hash/formula reproduction does not authenticate event completeness, action execution or proof validity Next: workflow source/context gate; settlement; convention-pinned reputation |
| trustless-ai/recompute-kit (main) | 15f7f59ac47b3358492bd5741143c418b5d657f5 | Source-pinned recompute recipes, conformance vectors, serializers and evidence-capsule builders | profile/verdict digest binding; serializer/adoption binding; conditional PQ policy/as-of; capsule root/portable object identity; anchor-to-proposal/artifact origination binding | reference functions; serializer registry; capsule exporter | RSI; SDK; ReceiptOS; gateway/consumer implementations | rvr.digest-binding.v0; tsei.serializer-adoption.v0; pq.policy-asof.v0 / partially validated | 19 | Only selected v0 lanes admitted; v1 PQ, other recipes and live authority resolvers not RSI-tested Next: receipt export/import identity; provenance-anchor relation |
| trustless-ai/ccip-router (main) | 6bd66611b88a4751a0acc233c718aa9a13294de4 | Signed observation mesh, divergence preservation, TSEI Profile A transport and commit/reveal settlement | exact receipt bytes to signed observation; origin signer versus forwarding peer; observation identity versus attestation identity; snapshot/period/sender to reveal commitment | gateway signer; mesh nodes | Profile A consumer; settlement contracts |  / mapped but unvalidated | 0 | TSEI receipt transport does not recompute private authority; deployment notes not live-reverified; no RSI mesh/settlement fixture Next: TSEI receipt-to-observation; message-to-action non-promotion |
| trustless-ai/semantic-abi (main) | d15c666dfccff17f7350fe97d2fc7b71cb2cbaee | Typed claim/authority/scope/time compatibility linker plus its own protected-relation adapter evaluation | producer establishes to consumer consumes compatibility; explicit negative claim boundary; pair outcome versus backend conformance | component manifest authors and source-specific adapters | semantic linker and downstream composition |  / mapped but unvalidated | 0 | Not integrated into RSI; declarations do not independently authenticate their own truth; owner-independent authorship is a source rule, not audited here Next: manifest-to-runtime claim correspondence; read-only during hackathon |
| trustless-ai/trustless-agent-substrate (feature/tas-poc) | a344ef80f7c52c03b9183814d1874b8054639c3e | TypeScript runtime with Profile-bound discovery, workflow verification and statically reviewed SDK calls; default branch is feature/tas-poc | verified source/deployed runtime fingerprint to execution context; current member wallet at exact block to caller authorization; reviewed manifest to SDK invocation | Profile resolver; compiler/code reader; manifest loader | workflow operation service and SDK port |  / mapped but unvalidated | 0 | Local Anvil chain-bound scope; live chat/concrete proof provider deferred; no RSI end-to-end execution claim Next: workflow fingerprint/context substitution |
| trustless-ai/pq-agent-binding (main) | 4f934ad31e96979002d818cd8a5f12909c1b6713 | PQ binding design and v1 temporal authority construction; not the executed v0 policy checker | acceptance sequence/authorization/manifest/anchor decomposition; governs_from from closed manifest chain; frozen legacy inheritance versus derived post-cutover ordering | binding owner; producer acceptance log; anchor publisher | recompute-kit profile and future wallet consumers |  / mapped but unvalidated | 0 | RSI PQ validates recompute-kit v0 supplied history, not this full v1 construction or this repo wholesale Next: earliest-anchor completeness; authenticated successor binding |
| trustless-ai/verify-layer (main) | 84afc4b738dc37269089c858404eed8086435f5d | MPT account/storage verification against supplied header stateRoot; trust labels distinguish header source | stateRoot to account proof; account storageRoot to slot proof/value; proof validity versus consensus header authority | RPC proof provider and header source | verification result / proposed wallet consumer |  / mapped but unvalidated | 0 | LightClientHeaderSource throws not wired; demo uses live RPC and no frozen offline proof corpus inspected Next: state-proof/root binding with header-authority non-promotion |
| trustless-ai/primitives (main) | 6b39e9540d4bd0a78decb588c0a8e328c303f208 | Discovery index plus drift checker; registry explicitly is not authority | index entry to referenced repo/recipe existence; RPC code-presence corroboration to bounded status | index maintainers; RPC/GitHub observations | discovery consumers; CI |  / mapped but unvalidated | 0 | Two endpoints are not proven independent consensus; presence/HTTP 200 is not semantic conformance Next: index corroboration/status-promotion fail-closed |
| trustless-ai/.github (main) | 63fcf1911eeb129e71919a3f629e8fc08dc56b9d | Organization front door and declared boundary-chain map; not an executable verifier | No executable relation claimed | documentation authors | ecosystem readers |  / README/architecture only | 0 | Marketing/deployment/audit statements do not establish whole-stack verification Next: none: use component sources |
| pipavlo82/crystal-receipt (main) | 45b46bf7df3a60b32583291f577a36bf19d22f00 | ReceiptOS packages supplied evidence into portable recomputable artifacts; TSEI is a separate specification hosted here | accepted semantic snapshot equivalence; serializer producer adoption; portable artifact identity and downstream admission boundaries | ReceiptOS producer; frozen conformance artifacts | RSI; recompute-kit registry/exporter; CCIP TSEI adapter | crystal-receipt.v0; tsei.serializer-adoption.v0 / partially validated | 9 | Only semantic-snapshot and serializer/adoption subsets; no universal authority or occurrence claim; Lane K not covered Next: capsule exporter/importer identity; separate authority evidence closure |
| pipavlo82/recomputable-verification-receipts (main) | 287c0ea1c2578c1833405bc2476975f95addbada | Verification profiles bind proposition/evidence/result and separate semantic outcome from recomputation status | artifact/policy/decision/event bindings under exact Verification Profile; signed verdict authenticity versus judgment correctness | profile author and receipt producer; external signed artifact producer | recomputer and receipt consumer | rvr.digest-binding.v0 (adjacent recompute-kit lane, not this whole repo) / partially mapped; separate RSI digest lane only | 0 | This repo signed-verdict BIP-340 profile is distinct from the unimplemented authentication of RSI amendment vectors Next: separately approved signed-verdict binding adapter |
| damonzwicker/erc8309-companion-drafts (main) | f5f36778e7cbf6c26fd61a7d66b70b9108447746 | Resolution-policy layer above divergence-preserving base; Profile A resolves nothing | observation-set/envelope/verdict binding; resolution versus agreement; layer-qualified unresolved and independence declarations | companion profile author; resolution consumer | reference consumer and adjacent RVR layer |  / mapped but unvalidated | 0 | Current draft v0.3.9 versus consumer SPEC_VERSION 0.3.3; no blanket latest-draft compliance claim Next: envelope/consumer composition and status preservation |
| babyblueviper1/invinoveritas (main) | 76d19dc394b208d01ba368382b3e5f4f2c18f0ee | Reference Profile A/B consumer and signed verdict producer; historical/current sources kept distinct | observation state to envelope/verdict with disclosed limitations; signed verdict artifact bindings | vantage-resolution consumer; verdict producer | downstream receipt/recompute consumers |  / mapped but unvalidated | 0 | Canonical HEAD advanced; inspected vantage_resolution.py bytes unchanged from prior pin; live execution not checked Next: signed observation set to consumer verdict binding |


**trustless-ai/agent-ercs evidence:** [S012: trustless-ai/agent-ercs/README.md](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/README.md); [S015: trustless-ai/agent-ercs/contracts/settlement/ConsultEscrow/ConsultEscrow.sol](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/settlement/ConsultEscrow/ConsultEscrow.sol); [S016: trustless-ai/agent-ercs/contracts/verify/ERC8274/IAgentVerifier.sol](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/verify/ERC8274/IAgentVerifier.sol); [S017: trustless-ai/agent-ercs/contracts/verify/ERC8354/PolicyAction.sol](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/verify/ERC8354/PolicyAction.sol); [S013: trustless-ai/agent-ercs/contracts/execution/ERC8301/IAgentWorkflow.sol](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/execution/ERC8301/IAgentWorkflow.sol); [S014: trustless-ai/agent-ercs/contracts/identity/ERC8323/IAgentSourceBinding.sol](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/identity/ERC8323/IAgentSourceBinding.sol)

**trustless-ai/agent-sdk evidence:** [S020: trustless-ai/agent-sdk/README.md](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/README.md); [S019: trustless-ai/agent-sdk/INTEGRATIONS.md](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/INTEGRATIONS.md); [S024: trustless-ai/agent-sdk/python/src/agent_sdk/settlement/erc8203/recompute.py](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/python/src/agent_sdk/settlement/erc8203/recompute.py); [S022: trustless-ai/agent-sdk/python/src/agent_sdk/reputation/erc8275/conventions.py](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/python/src/agent_sdk/reputation/erc8275/conventions.py); [S025: trustless-ai/agent-sdk/python/src/agent_sdk/verify/erc8354/recompute.py](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/python/src/agent_sdk/verify/erc8354/recompute.py)

**trustless-ai/recompute-kit evidence:** [S038: trustless-ai/recompute-kit/README.md](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/README.md); [S047: trustless-ai/recompute-kit/conformance/serializer-bindings/README.md](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/serializer-bindings/README.md); [S048: trustless-ai/recompute-kit/mcp/receiptos.py](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/mcp/receiptos.py); [S045: trustless-ai/recompute-kit/conformance/provenance-anchor-v0/provenance-anchor-v0.spec.md](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/provenance-anchor-v0/provenance-anchor-v0.spec.md); [S044: trustless-ai/recompute-kit/conformance/pq-key-binding-v1-profile/README.md](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/pq-key-binding-v1-profile/README.md)

**trustless-ai/ccip-router evidence:** [S028: trustless-ai/ccip-router/README.md](https://github.com/trustless-ai/ccip-router/blob/6bd66611b88a4751a0acc233c718aa9a13294de4/README.md); [S027: trustless-ai/ccip-router/INTEGRATION.md](https://github.com/trustless-ai/ccip-router/blob/6bd66611b88a4751a0acc233c718aa9a13294de4/INTEGRATION.md); [S031: trustless-ai/ccip-router/src/integrations/tseiProfileA.ts](https://github.com/trustless-ai/ccip-router/blob/6bd66611b88a4751a0acc233c718aa9a13294de4/src/integrations/tseiProfileA.ts); [S029: trustless-ai/ccip-router/conformance/tsei-profile-a-v0/README.md](https://github.com/trustless-ai/ccip-router/blob/6bd66611b88a4751a0acc233c718aa9a13294de4/conformance/tsei-profile-a-v0/README.md); [S030: trustless-ai/ccip-router/contracts/CommitRevealSettlerV2.sol](https://github.com/trustless-ai/ccip-router/blob/6bd66611b88a4751a0acc233c718aa9a13294de4/contracts/CommitRevealSettlerV2.sol)

**trustless-ai/semantic-abi evidence:** [S049: trustless-ai/semantic-abi/README.md](https://github.com/trustless-ai/semantic-abi/blob/d15c666dfccff17f7350fe97d2fc7b71cb2cbaee/README.md); [S052: trustless-ai/semantic-abi/schema/manifest-v0.md](https://github.com/trustless-ai/semantic-abi/blob/d15c666dfccff17f7350fe97d2fc7b71cb2cbaee/schema/manifest-v0.md); [S051: trustless-ai/semantic-abi/runner/src/linker.mjs](https://github.com/trustless-ai/semantic-abi/blob/d15c666dfccff17f7350fe97d2fc7b71cb2cbaee/runner/src/linker.mjs); [S050: trustless-ai/semantic-abi/runner/src/evaluate.mjs](https://github.com/trustless-ai/semantic-abi/blob/d15c666dfccff17f7350fe97d2fc7b71cb2cbaee/runner/src/evaluate.mjs)

**trustless-ai/trustless-agent-substrate evidence:** [S053: trustless-ai/trustless-agent-substrate/README.md](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/README.md); [S058: trustless-ai/trustless-agent-substrate/src/core/workflow/sourceGate.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/src/core/workflow/sourceGate.ts); [S059: trustless-ai/trustless-agent-substrate/src/core/workflow/sourceVerifier.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/src/core/workflow/sourceVerifier.ts); [S057: trustless-ai/trustless-agent-substrate/src/core/workflow/operationService.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/src/core/workflow/operationService.ts); [S060: trustless-ai/trustless-agent-substrate/test/unit/workflow/sourceGate.test.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/test/unit/workflow/sourceGate.test.ts); [S056: trustless-ai/trustless-agent-substrate/src/clients/workflow/agentSdkClient.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/src/clients/workflow/agentSdkClient.ts)

**trustless-ai/pq-agent-binding evidence:** [S033: trustless-ai/pq-agent-binding/README.md](https://github.com/trustless-ai/pq-agent-binding/blob/4f934ad31e96979002d818cd8a5f12909c1b6713/README.md); [S034: trustless-ai/pq-agent-binding/spec/v1-temporal-authority.md](https://github.com/trustless-ai/pq-agent-binding/blob/4f934ad31e96979002d818cd8a5f12909c1b6713/spec/v1-temporal-authority.md)

**trustless-ai/verify-layer evidence:** [S062: trustless-ai/verify-layer/README.md](https://github.com/trustless-ai/verify-layer/blob/84afc4b738dc37269089c858404eed8086435f5d/README.md); [S063: trustless-ai/verify-layer/verify.mjs](https://github.com/trustless-ai/verify-layer/blob/84afc4b738dc37269089c858404eed8086435f5d/verify.mjs)

**trustless-ai/primitives evidence:** [S035: trustless-ai/primitives/README.md](https://github.com/trustless-ai/primitives/blob/6b39e9540d4bd0a78decb588c0a8e328c303f208/README.md); [S036: trustless-ai/primitives/check.py](https://github.com/trustless-ai/primitives/blob/6b39e9540d4bd0a78decb588c0a8e328c303f208/check.py); [S037: trustless-ai/primitives/primitives.json](https://github.com/trustless-ai/primitives/blob/6b39e9540d4bd0a78decb588c0a8e328c303f208/primitives.json)

**trustless-ai/.github evidence:** [S011: trustless-ai/.github/profile/README.md](https://github.com/trustless-ai/.github/blob/63fcf1911eeb129e71919a3f629e8fc08dc56b9d/profile/README.md)

**pipavlo82/crystal-receipt evidence:** [S005: pipavlo82/crystal-receipt/README.md](https://github.com/pipavlo82/crystal-receipt/blob/45b46bf7df3a60b32583291f577a36bf19d22f00/README.md); [S006: pipavlo82/crystal-receipt/conformance/counterfactual-audit-boundary-v0/SPEC.md](https://github.com/pipavlo82/crystal-receipt/blob/45b46bf7df3a60b32583291f577a36bf19d22f00/conformance/counterfactual-audit-boundary-v0/SPEC.md); [S007: pipavlo82/crystal-receipt/conformance/tsei-invariant-discrimination-v0/README.md](https://github.com/pipavlo82/crystal-receipt/blob/45b46bf7df3a60b32583291f577a36bf19d22f00/conformance/tsei-invariant-discrimination-v0/README.md); [S008: pipavlo82/crystal-receipt/conformance/tsei-invariant-discrimination-v0/public-receipts/tsei-ia-real-v2-20260824-02.production-grounding.json](https://github.com/pipavlo82/crystal-receipt/blob/45b46bf7df3a60b32583291f577a36bf19d22f00/conformance/tsei-invariant-discrimination-v0/public-receipts/tsei-ia-real-v2-20260824-02.production-grounding.json)

**pipavlo82/recomputable-verification-receipts evidence:** [S009: pipavlo82/recomputable-verification-receipts/README.md](https://github.com/pipavlo82/recomputable-verification-receipts/blob/287c0ea1c2578c1833405bc2476975f95addbada/README.md); [S010: pipavlo82/recomputable-verification-receipts/profiles/invinoveritas-signed-verdict-v1/SPEC.md](https://github.com/pipavlo82/recomputable-verification-receipts/blob/287c0ea1c2578c1833405bc2476975f95addbada/profiles/invinoveritas-signed-verdict-v1/SPEC.md)

**damonzwicker/erc8309-companion-drafts evidence:** [S004: damonzwicker/erc8309-companion-drafts/8309-vantage-authority-companion-v0.3.9.md](https://github.com/damonzwicker/erc8309-companion-drafts/blob/f5f36778e7cbf6c26fd61a7d66b70b9108447746/8309-vantage-authority-companion-v0.3.9.md)

**babyblueviper1/invinoveritas evidence:** [S001: babyblueviper1/invinoveritas/README.md](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/README.md); [S003: babyblueviper1/invinoveritas/integrations/conformance/erc-8309-vantage/services/vantage_resolution.py](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/integrations/conformance/erc-8309-vantage/services/vantage_resolution.py); [S002: babyblueviper1/invinoveritas/integrations/conformance/erc-8309-vantage/README.md](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/integrations/conformance/erc-8309-vantage/README.md)

## Cross-repo edges and ownership

Each edge states whether local validity can coexist with a broken inter-component relation. The verifier column names responsibility; it does not mean that verifier was executed by this synthesis.

### E01 — accepted semantic snapshot equivalence

| Field | Value |
| --- | --- |
| Producer → consumer | pipavlo82/crystal-receipt → pipavlo82/relational-security-invariants |
| Kind / status | source-backed integration/dependency / validated bounded profile |
| Declares | frozen Crystal spec |
| Produces evidence | pipavlo82/crystal-receipt |
| Verifies | native TypeScript versus Python predictor |
| Consumes / can overclaim | pipavlo82/relational-security-invariants / pipavlo82/relational-security-invariants |
| Required relation / dependent claim | accepted semantic snapshot equivalence / semantic identity preserved |
| Both locally correct while relation wrong? | Both snapshots process successfully but one protected value differs |
| RSI coverage | 4 checks; CR-M1..3 |
| Source | [S006: pipavlo82/crystal-receipt/conformance/counterfactual-audit-boundary-v0/SPEC.md](https://github.com/pipavlo82/crystal-receipt/blob/45b46bf7df3a60b32583291f577a36bf19d22f00/conformance/counterfactual-audit-boundary-v0/SPEC.md) |

### E02 — profile transition and verdict digest bindings

| Field | Value |
| --- | --- |
| Producer → consumer | trustless-ai/recompute-kit → pipavlo82/relational-security-invariants |
| Kind / status | source-backed integration/dependency / validated bounded profile |
| Declares | pinned amendment/verdict specs |
| Produces evidence | trustless-ai/recompute-kit |
| Verifies | pinned Python reference versus separate predictor |
| Consumes / can overclaim | pipavlo82/relational-security-invariants / pipavlo82/relational-security-invariants |
| Required relation / dependent claim | profile transition and verdict digest bindings / digest binding only |
| Both locally correct while relation wrong? | Both commitments are valid but verdict points to stale effective profile |
| RSI coverage | 10 checks; RVR-M1..6; see pinned evidence/rvr specs |
| Source | [S064: trustless-ai/recompute-kit/conformance/profile-amendment-v0/profile-amendment-v0.spec.md](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/profile-amendment-v0/profile-amendment-v0.spec.md); [S065: trustless-ai/recompute-kit/conformance/profile-amendment-v0/amendment_gate.py](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/profile-amendment-v0/amendment_gate.py); [S068: trustless-ai/recompute-kit/conformance/verdict-profile-binding-v0/verdict-profile-binding-v0.spec.md](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/verdict-profile-binding-v0/verdict-profile-binding-v0.spec.md) |

### E03 — schema serializer record to producer adoption/effective boundary

| Field | Value |
| --- | --- |
| Producer → consumer | trustless-ai/recompute-kit → pipavlo82/crystal-receipt |
| Kind / status | source-backed integration/dependency / partially validated |
| Declares | registry serializer contract and explicit immutable record |
| Produces evidence | trustless-ai/recompute-kit |
| Verifies | native adopted encoder, registry checker and separate RSI predictor |
| Consumes / can overclaim | pipavlo82/crystal-receipt / pipavlo82/crystal-receipt |
| Required relation / dependent claim | schema serializer record to producer adoption/effective boundary / forward serializer coverage, not provenance authority |
| Both locally correct while relation wrong? | Valid bytes under another serializer or before adoption cannot inherit current binding |
| RSI coverage | 7 TSEI checks; finite pinned chronology; TSEI-M1..6 |
| Source | [S047: trustless-ai/recompute-kit/conformance/serializer-bindings/README.md](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/serializer-bindings/README.md); [S005: pipavlo82/crystal-receipt/README.md](https://github.com/pipavlo82/crystal-receipt/blob/45b46bf7df3a60b32583291f577a36bf19d22f00/README.md) |

### E04 — supplied history to as-of governing binding

| Field | Value |
| --- | --- |
| Producer → consumer | trustless-ai/recompute-kit → pipavlo82/relational-security-invariants |
| Kind / status | source-backed integration/dependency / validated v0 policy subset only |
| Declares | pinned recompute-kit v0 cutoff policy, not v1 retroactively |
| Produces evidence | trustless-ai/recompute-kit |
| Verifies | source cutoff_enforce versus separate predictor |
| Consumes / can overclaim | pipavlo82/relational-security-invariants / pipavlo82/relational-security-invariants |
| Required relation / dependent claim | supplied history to as-of governing binding / conditional eligibility, no anchor/transition authentication |
| Both locally correct while relation wrong? | Locally valid old key or stale snapshot is not current authority |
| RSI coverage | 7 checks; PQ-M1..7; exact v0 source pin in evidence/pq; v1 sources are boundary context only |
| Source | [S072: trustless-ai/recompute-kit/conformance/pq-key-binding-v0/pq-key-binding-v0.spec.md](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/pq-key-binding-v0/pq-key-binding-v0.spec.md); [S080: trustless-ai/recompute-kit/conformance/pq-key-binding-v0/cutoff_enforce.py](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/pq-key-binding-v0/cutoff_enforce.py); [S074: trustless-ai/recompute-kit/conformance/pq-key-binding-v0/pq-key-binding-v0.rotation-vectors.json](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/pq-key-binding-v0/pq-key-binding-v0.rotation-vectors.json); [S079: trustless-ai/recompute-kit/conformance/pq-key-binding-v0/deep_recompute.py](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/pq-key-binding-v0/deep_recompute.py) |

### E05 — exact public receipt bytes to signed Profile A observation

| Field | Value |
| --- | --- |
| Producer → consumer | pipavlo82/crystal-receipt → trustless-ai/ccip-router |
| Kind / status | source-backed integration/dependency / mapped unvalidated |
| Declares | CCIP TSEI observation contract |
| Produces evidence | pipavlo82/crystal-receipt |
| Verifies | gateway signature recovery / downstream consumer |
| Consumes / can overclaim | trustless-ai/ccip-router / trustless-ai/ccip-router |
| Required relation / dependent claim | exact public receipt bytes to signed Profile A observation / receipt observation identity, not TSEI authority |
| Both locally correct while relation wrong? | Receipt is valid JSON but digest/instance endpoint differs; sourcePeer is not signer |
| RSI coverage | No RSI transport/ingestion fixture |
| Source | [S031: trustless-ai/ccip-router/src/integrations/tseiProfileA.ts](https://github.com/trustless-ai/ccip-router/blob/6bd66611b88a4751a0acc233c718aa9a13294de4/src/integrations/tseiProfileA.ts); [S029: trustless-ai/ccip-router/conformance/tsei-profile-a-v0/README.md](https://github.com/trustless-ai/ccip-router/blob/6bd66611b88a4751a0acc233c718aa9a13294de4/conformance/tsei-profile-a-v0/README.md) |

### E06 — preserved observation set to Profile A consumer envelope

| Field | Value |
| --- | --- |
| Producer → consumer | trustless-ai/ccip-router → babyblueviper1/invinoveritas |
| Kind / status | source-backed integration/dependency / mapped unvalidated |
| Declares | base reference and companion profiles |
| Produces evidence | trustless-ai/ccip-router |
| Verifies | reference consumer |
| Consumes / can overclaim | babyblueviper1/invinoveritas / babyblueviper1/invinoveritas |
| Required relation / dependent claim | preserved observation set to Profile A consumer envelope / divergence surfaced with disclosed limitations |
| Both locally correct while relation wrong? | Both attestations validate but distinct observations are collapsed to agreement |
| RSI coverage | Existing RVR digest fixtures do not execute this end-to-end edge |
| Source | [S027: trustless-ai/ccip-router/INTEGRATION.md](https://github.com/trustless-ai/ccip-router/blob/6bd66611b88a4751a0acc233c718aa9a13294de4/INTEGRATION.md); [S003: babyblueviper1/invinoveritas/integrations/conformance/erc-8309-vantage/services/vantage_resolution.py](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/integrations/conformance/erc-8309-vantage/services/vantage_resolution.py) |

### E07 — declared resolution profile to evaluation/verdict interpretation

| Field | Value |
| --- | --- |
| Producer → consumer | damonzwicker/erc8309-companion-drafts → babyblueviper1/invinoveritas |
| Kind / status | source-backed integration/dependency / mapped unvalidated |
| Declares | versioned companion |
| Produces evidence | damonzwicker/erc8309-companion-drafts |
| Verifies | reference consumer tests, not run here |
| Consumes / can overclaim | babyblueviper1/invinoveritas / babyblueviper1/invinoveritas |
| Required relation / dependent claim | declared resolution profile to evaluation/verdict interpretation / profile-qualified resolution, not agreement/finality |
| Both locally correct while relation wrong? | Consumer uses a coherent old profile while downstream assumes current one |
| RSI coverage | No whole current-draft conformance assertion |
| Source | [S004: damonzwicker/erc8309-companion-drafts/8309-vantage-authority-companion-v0.3.9.md](https://github.com/damonzwicker/erc8309-companion-drafts/blob/f5f36778e7cbf6c26fd61a7d66b70b9108447746/8309-vantage-authority-companion-v0.3.9.md); [S003: babyblueviper1/invinoveritas/integrations/conformance/erc-8309-vantage/services/vantage_resolution.py](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/integrations/conformance/erc-8309-vantage/services/vantage_resolution.py) |

### E08 — exact historical signed verdict artifact to RVR verification profile

| Field | Value |
| --- | --- |
| Producer → consumer | babyblueviper1/invinoveritas → pipavlo82/recomputable-verification-receipts |
| Kind / status | source-backed integration/dependency / mapped unvalidated |
| Declares | RVR signed-verdict v1 profile |
| Produces evidence | babyblueviper1/invinoveritas |
| Verifies | specified BIP-340/event/digest procedure; not executed in this synthesis |
| Consumes / can overclaim | pipavlo82/recomputable-verification-receipts / pipavlo82/recomputable-verification-receipts |
| Required relation / dependent claim | exact historical signed verdict artifact to RVR verification profile / artifact authenticity under pinned key, not judgment correctness |
| Both locally correct while relation wrong? | Valid signed artifact attached to different policy/claim/evidence identity |
| RSI coverage | Not the RSI amendment authentication lane |
| Source | [S010: pipavlo82/recomputable-verification-receipts/profiles/invinoveritas-signed-verdict-v1/SPEC.md](https://github.com/pipavlo82/recomputable-verification-receipts/blob/287c0ea1c2578c1833405bc2476975f95addbada/profiles/invinoveritas-signed-verdict-v1/SPEC.md) |

### E09 — temporal authority design to captured-admission v1 profile

| Field | Value |
| --- | --- |
| Producer → consumer | trustless-ai/pq-agent-binding → trustless-ai/recompute-kit |
| Kind / status | source-backed integration/dependency / mapped unvalidated |
| Declares | PQ v1 section 10 |
| Produces evidence | trustless-ai/pq-agent-binding |
| Verifies | captured-admission checker plus required external profile obligations |
| Consumes / can overclaim | trustless-ai/recompute-kit / trustless-ai/recompute-kit |
| Required relation / dependent claim | temporal authority design to captured-admission v1 profile / derived post-cutover authority; legacy inheritance stays weaker |
| Both locally correct while relation wrong? | Correct local sequence/vector output does not prove complete anchored manifest history |
| RSI coverage | RSI v0 policy does not cover v1 admission/manifest closure |
| Source | [S034: trustless-ai/pq-agent-binding/spec/v1-temporal-authority.md](https://github.com/trustless-ai/pq-agent-binding/blob/4f934ad31e96979002d818cd8a5f12909c1b6713/spec/v1-temporal-authority.md); [S044: trustless-ai/recompute-kit/conformance/pq-key-binding-v1-profile/README.md](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/pq-key-binding-v1-profile/README.md) |

### E10 — workflow task/reply/run preimage to recomputed hash

| Field | Value |
| --- | --- |
| Producer → consumer | trustless-ai/agent-ercs → trustless-ai/agent-sdk |
| Kind / status | source-backed integration/dependency / mapped unvalidated |
| Declares | ERC8301 interface preimage |
| Produces evidence | trustless-ai/agent-ercs |
| Verifies | SDK recompute; workflow implementation |
| Consumes / can overclaim | trustless-ai/agent-sdk / trustless-ai/agent-sdk |
| Required relation / dependent claim | workflow task/reply/run preimage to recomputed hash / task/reply identity, not action occurrence |
| Both locally correct while relation wrong? | Well-formed task from another run can be hashed correctly but not belong to this run |
| RSI coverage | No RSI task/reply fixture |
| Source | [S013: trustless-ai/agent-ercs/contracts/execution/ERC8301/IAgentWorkflow.sol](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/execution/ERC8301/IAgentWorkflow.sol); [S021: trustless-ai/agent-sdk/python/src/agent_sdk/execution/erc8301/recompute.py](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/python/src/agent_sdk/execution/erc8301/recompute.py) |

### E11 — job/result commitment and attestor to settlement

| Field | Value |
| --- | --- |
| Producer → consumer | trustless-ai/agent-ercs → trustless-ai/agent-sdk |
| Kind / status | source-backed integration/dependency / mapped unvalidated |
| Declares | ConsultEscrow release implementation |
| Produces evidence | trustless-ai/agent-ercs |
| Verifies | EIP191 recovery and on-chain job commitment |
| Consumes / can overclaim | trustless-ai/agent-sdk / trustless-ai/agent-sdk |
| Required relation / dependent claim | job/result commitment and attestor to settlement / release eligibility for exact job |
| Both locally correct while relation wrong? | Same valid signature/result reused for different job |
| RSI coverage | No RSI escrow execution |
| Source | [S015: trustless-ai/agent-ercs/contracts/settlement/ConsultEscrow/ConsultEscrow.sol](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/settlement/ConsultEscrow/ConsultEscrow.sol); [S018: trustless-ai/agent-ercs/test/settlement/ConsultEscrow/ConsultEscrow.t.sol](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/test/settlement/ConsultEscrow/ConsultEscrow.t.sol); [S024: trustless-ai/agent-sdk/python/src/agent_sdk/settlement/erc8203/recompute.py](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/python/src/agent_sdk/settlement/erc8203/recompute.py) |

### E12 — policy action envelope to action/verdict commitment

| Field | Value |
| --- | --- |
| Producer → consumer | trustless-ai/agent-ercs → trustless-ai/agent-sdk |
| Kind / status | source-backed integration/dependency / mapped unvalidated |
| Declares | PolicyAction canonical preimage |
| Produces evidence | trustless-ai/agent-ercs |
| Verifies | SDK pure computation; future guard/prover |
| Consumes / can overclaim | trustless-ai/agent-sdk / trustless-ai/agent-sdk |
| Required relation / dependent claim | policy action envelope to action/verdict commitment / action commitment identity, not policy proof or executed action |
| Both locally correct while relation wrong? | Valid digest for different chain/domain/target remains a wrong action authorization |
| RSI coverage | No RSI guard/execution fixture |
| Source | [S017: trustless-ai/agent-ercs/contracts/verify/ERC8354/PolicyAction.sol](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/verify/ERC8354/PolicyAction.sol); [S025: trustless-ai/agent-sdk/python/src/agent_sdk/verify/erc8354/recompute.py](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/python/src/agent_sdk/verify/erc8354/recompute.py) |

### E13 — reviewed SDK binding to context-bound invocation

| Field | Value |
| --- | --- |
| Producer → consumer | trustless-ai/agent-sdk → trustless-ai/trustless-agent-substrate |
| Kind / status | source-backed integration/dependency / mapped unvalidated |
| Declares | reviewed TAS manifest and Profile |
| Produces evidence | trustless-ai/agent-sdk |
| Verifies | TAS operation gate and wallet/block checks |
| Consumes / can overclaim | trustless-ai/trustless-agent-substrate / trustless-ai/trustless-agent-substrate |
| Required relation / dependent claim | reviewed SDK binding to context-bound invocation / permitted invocation; external handle is not completed action |
| Both locally correct while relation wrong? | Valid SDK method invoked under wrong wallet or contract context |
| RSI coverage | No RSI TAS runtime fixture |
| Source | [S056: trustless-ai/trustless-agent-substrate/src/clients/workflow/agentSdkClient.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/src/clients/workflow/agentSdkClient.ts); [S057: trustless-ai/trustless-agent-substrate/src/core/workflow/operationService.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/src/core/workflow/operationService.ts); [S055: trustless-ai/trustless-agent-substrate/manifests/agent-sdk.v1.json](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/manifests/agent-sdk.v1.json) |

### E14 — workflow source/deployment identity to current execution gate

| Field | Value |
| --- | --- |
| Producer → consumer | trustless-ai/agent-ercs → trustless-ai/trustless-agent-substrate |
| Kind / status | source-backed integration/dependency / mapped unvalidated |
| Declares | Profile-selected workflow and source verifier |
| Produces evidence | trustless-ai/agent-ercs |
| Verifies | TAS fingerprint/context gate |
| Consumes / can overclaim | trustless-ai/trustless-agent-substrate / trustless-ai/trustless-agent-substrate |
| Required relation / dependent claim | workflow source/deployment identity to current execution gate / source verification applicable to this invocation |
| Both locally correct while relation wrong? | Individually verified source and deployment refer to different workflow contexts |
| RSI coverage | No RSI deployment/context fixture |
| Source | [S058: trustless-ai/trustless-agent-substrate/src/core/workflow/sourceGate.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/src/core/workflow/sourceGate.ts); [S059: trustless-ai/trustless-agent-substrate/src/core/workflow/sourceVerifier.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/src/core/workflow/sourceVerifier.ts); [S060: trustless-ai/trustless-agent-substrate/test/unit/workflow/sourceGate.test.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/test/unit/workflow/sourceGate.test.ts); [S013: trustless-ai/agent-ercs/contracts/execution/ERC8301/IAgentWorkflow.sol](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/execution/ERC8301/IAgentWorkflow.sol) |

### E15 — capsule root to portable object/import identity

| Field | Value |
| --- | --- |
| Producer → consumer | trustless-ai/recompute-kit → pipavlo82/crystal-receipt |
| Kind / status | source-backed integration/dependency / mapped unvalidated |
| Declares | ReceiptOS portable boundary and exporter byte contract |
| Produces evidence | trustless-ai/recompute-kit |
| Verifies | exporter root recomputation and recipient verifier |
| Consumes / can overclaim | pipavlo82/crystal-receipt / pipavlo82/crystal-receipt |
| Required relation / dependent claim | capsule root to portable object/import identity / identity/integrity only |
| Both locally correct while relation wrong? | Correct capsule root does not establish proof validity or downstream admission |
| RSI coverage | CR semantic-snapshot profile does not validate exporter/importer seam |
| Source | [S048: trustless-ai/recompute-kit/mcp/receiptos.py](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/mcp/receiptos.py); [S005: pipavlo82/crystal-receipt/README.md](https://github.com/pipavlo82/crystal-receipt/blob/45b46bf7df3a60b32583291f577a36bf19d22f00/README.md) |

### E16 — settled outcome evidence to reputation convention/value

| Field | Value |
| --- | --- |
| Producer → consumer | trustless-ai/agent-ercs → trustless-ai/agent-sdk |
| Kind / status | declared/candidate composition / declared composition; event extraction unverified |
| Declares | ERC8275 convention pin and event-derived role |
| Produces evidence | trustless-ai/agent-ercs |
| Verifies | SDK value checker; event authority/extraction not established here |
| Consumes / can overclaim | trustless-ai/agent-sdk / trustless-ai/agent-sdk |
| Required relation / dependent claim | settled outcome evidence to reputation convention/value / convention-correct value, not complete settled history |
| Both locally correct while relation wrong? | Correct arithmetic over wrong event set/convention yields unsupported standing |
| RSI coverage | No RSI event-to-reputation fixture |
| Source | [S022: trustless-ai/agent-sdk/python/src/agent_sdk/reputation/erc8275/conventions.py](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/python/src/agent_sdk/reputation/erc8275/conventions.py); [S023: trustless-ai/agent-sdk/python/src/agent_sdk/reputation/erc8275/recompute.py](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/python/src/agent_sdk/reputation/erc8275/recompute.py); [S042: trustless-ai/recompute-kit/conformance/erc8275-win-rate-bps-v0/erc8275-win-rate-bps-v0.spec.md](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/erc8275-win-rate-bps-v0/erc8275-win-rate-bps-v0.spec.md) |

### E17 — recipe existence to registry discovery status

| Field | Value |
| --- | --- |
| Producer → consumer | trustless-ai/recompute-kit → trustless-ai/primitives |
| Kind / status | source-backed integration/dependency / mapped unvalidated |
| Declares | registry check kind |
| Produces evidence | trustless-ai/recompute-kit |
| Verifies | GitHub lookup in checker |
| Consumes / can overclaim | trustless-ai/primitives / trustless-ai/primitives |
| Required relation / dependent claim | recipe existence to registry discovery status / reference reachable, not conformance |
| Both locally correct while relation wrong? | Recipe exists but is stale or semantically failing; existence PASS still holds |
| RSI coverage | No RSI index-status fixture |
| Source | [S036: trustless-ai/primitives/check.py](https://github.com/trustless-ai/primitives/blob/6b39e9540d4bd0a78decb588c0a8e328c303f208/check.py); [S037: trustless-ai/primitives/primitives.json](https://github.com/trustless-ai/primitives/blob/6b39e9540d4bd0a78decb588c0a8e328c303f208/primitives.json) |

### E18 — verifier repository reference to index availability

| Field | Value |
| --- | --- |
| Producer → consumer | trustless-ai/verify-layer → trustless-ai/primitives |
| Kind / status | discovery edge / mapped unvalidated |
| Declares | registry index |
| Produces evidence | trustless-ai/verify-layer |
| Verifies | GitHub existence check |
| Consumes / can overclaim | trustless-ai/primitives / trustless-ai/primitives |
| Required relation / dependent claim | verifier repository reference to index availability / discovery only, not proof authority |
| Both locally correct while relation wrong? | Repo is reachable while header verification is absent |
| RSI coverage | No RSI index-status fixture |
| Source | [S037: trustless-ai/primitives/primitives.json](https://github.com/trustless-ai/primitives/blob/6b39e9540d4bd0a78decb588c0a8e328c303f208/primitives.json); [S036: trustless-ai/primitives/check.py](https://github.com/trustless-ai/primitives/blob/6b39e9540d4bd0a78decb588c0a8e328c303f208/check.py); [S062: trustless-ai/verify-layer/README.md](https://github.com/trustless-ai/verify-layer/blob/84afc4b738dc37269089c858404eed8086435f5d/README.md) |

### E19 — signed decision artifact to typed claim/authority evaluation

| Field | Value |
| --- | --- |
| Producer → consumer | babyblueviper1/invinoveritas → trustless-ai/semantic-abi |
| Kind / status | source-backed integration/dependency / mapped unvalidated by RSI |
| Declares | Semantic ABI manifest and source adapter contract |
| Produces evidence | babyblueviper1/invinoveritas |
| Verifies | Semantic ABI linker/adapter |
| Consumes / can overclaim | trustless-ai/semantic-abi / trustless-ai/semantic-abi |
| Required relation / dependent claim | signed decision artifact to typed claim/authority evaluation / typed compatibility and bounded observation, not universal truth |
| Both locally correct while relation wrong? | Authentic signed verdict remains distinct from correct judgment |
| RSI coverage | Semantic ABI has its own adapter path; not rerun/modified here |
| Source | [S049: trustless-ai/semantic-abi/README.md](https://github.com/trustless-ai/semantic-abi/blob/d15c666dfccff17f7350fe97d2fc7b71cb2cbaee/README.md); [S052: trustless-ai/semantic-abi/schema/manifest-v0.md](https://github.com/trustless-ai/semantic-abi/blob/d15c666dfccff17f7350fe97d2fc7b71cb2cbaee/schema/manifest-v0.md) |

### E20 — declared ecosystem role to component implementation

| Field | Value |
| --- | --- |
| Producer → consumer | trustless-ai/.github → trustless-ai/agent-ercs |
| Kind / status | discovery edge / README/architecture only |
| Declares | organization role map |
| Produces evidence | trustless-ai/.github |
| Verifies | reader must inspect actual component and audit/deployment evidence |
| Consumes / can overclaim | trustless-ai/agent-ercs / trustless-ai/agent-ercs |
| Required relation / dependent claim | declared ecosystem role to component implementation / discovery/navigation only |
| Both locally correct while relation wrong? | Organization says production/audited while a selected surface is interface-only |
| RSI coverage | No executable RSI coverage claimed |
| Source | [S011: trustless-ai/.github/profile/README.md](https://github.com/trustless-ai/.github/blob/63fcf1911eeb129e71919a3f629e8fc08dc56b9d/profile/README.md); [S012: trustless-ai/agent-ercs/README.md](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/README.md) |


## Additional source-backed seams not asserted as deployed cross-repo wiring

- verify-layer stateRoot → account → storage slot is an implemented intra-verifier relation; its future wallet composition is proposed, not proven deployed here.
- Communication-chain returned calldata → executed action is an unsupported promotion: the inspected function hashes a tool response, not a transaction receipt.
- ERC8323 permanent source-token provenance and live ownership are separate interface relations; no registry implementation was executed.
- Provenance-anchor pre-existence and origination are distinct source claims; real origination positive remains pending in the inspected spec.

## Inspected source inventory

| Evidence | Repo / exact commit / path | Class | SHA-256 |
| --- | --- | --- | --- |
| S012 | [trustless-ai/agent-ercs @ 01283ca57305f915afb560d23359a27fd748eb5a / README.md](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/README.md) | README/architecture only | f91be29279f4f0854122a3aadfe575e22a5a9e0129e7b4591c3207eb7013cbc4 |
| S020 | [trustless-ai/agent-sdk @ e41b117893fb56bc869922de378daf91aad63def / README.md](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/README.md) | README/architecture only | db05f2cfcaf6c8f99a5ecde2cb55406bb9114394eb18d799841d7f150d2d63bf |
| S019 | [trustless-ai/agent-sdk @ e41b117893fb56bc869922de378daf91aad63def / INTEGRATIONS.md](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/INTEGRATIONS.md) | README/architecture only | 3d8c7a0a736d8f91a437cdfeb3abadca770cc5c4041cd534894de41ae1d88811 |
| S038 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / README.md](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/README.md) | README/architecture only | 7e1b9266733d35bfef66dc475a210a02e1338e727a9388a66ab9b3261b502569 |
| S028 | [trustless-ai/ccip-router @ 6bd66611b88a4751a0acc233c718aa9a13294de4 / README.md](https://github.com/trustless-ai/ccip-router/blob/6bd66611b88a4751a0acc233c718aa9a13294de4/README.md) | README/architecture only | 8b0c88866f5299d0ae93c1b911a42e763d407fdf7fb07b619c7979ca9d69665f |
| S027 | [trustless-ai/ccip-router @ 6bd66611b88a4751a0acc233c718aa9a13294de4 / INTEGRATION.md](https://github.com/trustless-ai/ccip-router/blob/6bd66611b88a4751a0acc233c718aa9a13294de4/INTEGRATION.md) | README/architecture only | e7cafbfd206eb9a84d2195979b02b938c9c1c2d221f7ca8fc4c8163c1617a20c |
| S029 | [trustless-ai/ccip-router @ 6bd66611b88a4751a0acc233c718aa9a13294de4 / conformance/tsei-profile-a-v0/README.md](https://github.com/trustless-ai/ccip-router/blob/6bd66611b88a4751a0acc233c718aa9a13294de4/conformance/tsei-profile-a-v0/README.md) | README/architecture only | 9613ce4502c8234c236f8818e5f7e557d386edd484afe62a39bb0d9e32236125 |
| S031 | [trustless-ai/ccip-router @ 6bd66611b88a4751a0acc233c718aa9a13294de4 / src/integrations/tseiProfileA.ts](https://github.com/trustless-ai/ccip-router/blob/6bd66611b88a4751a0acc233c718aa9a13294de4/src/integrations/tseiProfileA.ts) | implementation | c67e9fef196db9041daaa26f93720c7811691dc71f21404eb31df28d2e607693 |
| S049 | [trustless-ai/semantic-abi @ d15c666dfccff17f7350fe97d2fc7b71cb2cbaee / README.md](https://github.com/trustless-ai/semantic-abi/blob/d15c666dfccff17f7350fe97d2fc7b71cb2cbaee/README.md) | README/architecture only | f20050889a9e9b2a03fb450add57a0e707ded53c9e0836c7ba23579e5c4e7794 |
| S052 | [trustless-ai/semantic-abi @ d15c666dfccff17f7350fe97d2fc7b71cb2cbaee / schema/manifest-v0.md](https://github.com/trustless-ai/semantic-abi/blob/d15c666dfccff17f7350fe97d2fc7b71cb2cbaee/schema/manifest-v0.md) | spec | 1361dbd123ae3f270ed39d1236b91d49d3ccdb9161dcfbdec4579a50be4f0a02 |
| S051 | [trustless-ai/semantic-abi @ d15c666dfccff17f7350fe97d2fc7b71cb2cbaee / runner/src/linker.mjs](https://github.com/trustless-ai/semantic-abi/blob/d15c666dfccff17f7350fe97d2fc7b71cb2cbaee/runner/src/linker.mjs) | implementation | bae8e519361989bfadbb5d226cb9940255cd954c60b40ba42136a2b11161d391 |
| S050 | [trustless-ai/semantic-abi @ d15c666dfccff17f7350fe97d2fc7b71cb2cbaee / runner/src/evaluate.mjs](https://github.com/trustless-ai/semantic-abi/blob/d15c666dfccff17f7350fe97d2fc7b71cb2cbaee/runner/src/evaluate.mjs) | implementation | a2f1c3caaaeeb37b7067618f7ee0b98bddece859baee7dfbfc68a44be58699b0 |
| S053 | [trustless-ai/trustless-agent-substrate @ a344ef80f7c52c03b9183814d1874b8054639c3e / README.md](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/README.md) | README/architecture only | 6a50e66550d96afbc93673fa980efab5d9e1b12dd06102cf743476ff7693e529 |
| S054 | [trustless-ai/trustless-agent-substrate @ a344ef80f7c52c03b9183814d1874b8054639c3e / docs/tas/IMPLEMENTATION.md](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/docs/tas/IMPLEMENTATION.md) | README/architecture only | 0324aa556a20bb7109fa70caeb5771050bcee29e75a004b3980e0ad68c06caee |
| S058 | [trustless-ai/trustless-agent-substrate @ a344ef80f7c52c03b9183814d1874b8054639c3e / src/core/workflow/sourceGate.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/src/core/workflow/sourceGate.ts) | implementation | b25f179911fb28f5877185055a6d016e92722545c838a64ebdcc621aad4286c3 |
| S059 | [trustless-ai/trustless-agent-substrate @ a344ef80f7c52c03b9183814d1874b8054639c3e / src/core/workflow/sourceVerifier.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/src/core/workflow/sourceVerifier.ts) | implementation | 0947eca9d928a3fd30e9b547550c3c037245f42d3ca635514499d2d340067bf5 |
| S057 | [trustless-ai/trustless-agent-substrate @ a344ef80f7c52c03b9183814d1874b8054639c3e / src/core/workflow/operationService.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/src/core/workflow/operationService.ts) | implementation | a8771c4514a3481667cf4c3dafa7adacc626797be8aa5bad7e3d0975869f31f5 |
| S033 | [trustless-ai/pq-agent-binding @ 4f934ad31e96979002d818cd8a5f12909c1b6713 / README.md](https://github.com/trustless-ai/pq-agent-binding/blob/4f934ad31e96979002d818cd8a5f12909c1b6713/README.md) | README/architecture only | 6c66159be16269f16d3c8d62d0ea639ba3ea36c855a4eb399c7790264478eb1c |
| S034 | [trustless-ai/pq-agent-binding @ 4f934ad31e96979002d818cd8a5f12909c1b6713 / spec/v1-temporal-authority.md](https://github.com/trustless-ai/pq-agent-binding/blob/4f934ad31e96979002d818cd8a5f12909c1b6713/spec/v1-temporal-authority.md) | README/architecture only | 2d0e2df322c42f23994941d77567c253ee2dd3ca1790c4bd0103079471abf6a5 |
| S062 | [trustless-ai/verify-layer @ 84afc4b738dc37269089c858404eed8086435f5d / README.md](https://github.com/trustless-ai/verify-layer/blob/84afc4b738dc37269089c858404eed8086435f5d/README.md) | README/architecture only | 9bb10a5646701d5c516b7b818bd58f327f530c50f0b60a8455ec36a2b0c883d9 |
| S063 | [trustless-ai/verify-layer @ 84afc4b738dc37269089c858404eed8086435f5d / verify.mjs](https://github.com/trustless-ai/verify-layer/blob/84afc4b738dc37269089c858404eed8086435f5d/verify.mjs) | implementation | ece05db266d1eb86ff71f47aa5a0666ada611dfd496ef0982e570406a28fb2d2 |
| S035 | [trustless-ai/primitives @ 6b39e9540d4bd0a78decb588c0a8e328c303f208 / README.md](https://github.com/trustless-ai/primitives/blob/6b39e9540d4bd0a78decb588c0a8e328c303f208/README.md) | README/architecture only | a63d40430eb09ae303dd16c6b8347177cdb36e89421fd40e78de94f61381efd2 |
| S036 | [trustless-ai/primitives @ 6b39e9540d4bd0a78decb588c0a8e328c303f208 / check.py](https://github.com/trustless-ai/primitives/blob/6b39e9540d4bd0a78decb588c0a8e328c303f208/check.py) | implementation | 1a5bd8fbc8c332943dd4123573425f3f2667bae511e2bbd4540acda52343699c |
| S037 | [trustless-ai/primitives @ 6b39e9540d4bd0a78decb588c0a8e328c303f208 / primitives.json](https://github.com/trustless-ai/primitives/blob/6b39e9540d4bd0a78decb588c0a8e328c303f208/primitives.json) | registry | 5709f7ea1c9923077ac6f4e9443f87c48c45fa2ac0509f678c1bf445f353641f |
| S011 | [trustless-ai/.github @ 63fcf1911eeb129e71919a3f629e8fc08dc56b9d / profile/README.md](https://github.com/trustless-ai/.github/blob/63fcf1911eeb129e71919a3f629e8fc08dc56b9d/profile/README.md) | README/architecture only | a947d75afe6e0dd1e6b9f74d779620f6a28bc47fd0a6581010ed3ca4b65339c5 |
| S005 | [pipavlo82/crystal-receipt @ 45b46bf7df3a60b32583291f577a36bf19d22f00 / README.md](https://github.com/pipavlo82/crystal-receipt/blob/45b46bf7df3a60b32583291f577a36bf19d22f00/README.md) | README/architecture only | 9d1f24afba889edf6ce618989bcf746a81f84c0c9240ac603c27caf3b3c4eed0 |
| S004 | [damonzwicker/erc8309-companion-drafts @ f5f36778e7cbf6c26fd61a7d66b70b9108447746 / 8309-vantage-authority-companion-v0.3.9.md](https://github.com/damonzwicker/erc8309-companion-drafts/blob/f5f36778e7cbf6c26fd61a7d66b70b9108447746/8309-vantage-authority-companion-v0.3.9.md) | spec | 6401eba79926af05af740ccaa3efe4a94981a38b9b7527850104713130dea191 |
| S001 | [babyblueviper1/invinoveritas @ 76d19dc394b208d01ba368382b3e5f4f2c18f0ee / README.md](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/README.md) | README/architecture only | 6a596b14ceeba6788853f4ed10d0fe86199796f93fc6f9cf79505fd5ce8395ee |
| S009 | [pipavlo82/recomputable-verification-receipts @ 287c0ea1c2578c1833405bc2476975f95addbada / README.md](https://github.com/pipavlo82/recomputable-verification-receipts/blob/287c0ea1c2578c1833405bc2476975f95addbada/README.md) | README/architecture only | c3292b9877143da1a127d1c9534c22975208b6fd1ec0658ccf7d6f16edc04193 |
| S015 | [trustless-ai/agent-ercs @ 01283ca57305f915afb560d23359a27fd748eb5a / contracts/settlement/ConsultEscrow/ConsultEscrow.sol](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/settlement/ConsultEscrow/ConsultEscrow.sol) | implementation | 373e1f6feab886d1115eceef391cebce97a16b51d4bdfdfb1e5bd4bdb3bd07f5 |
| S018 | [trustless-ai/agent-ercs @ 01283ca57305f915afb560d23359a27fd748eb5a / test/settlement/ConsultEscrow/ConsultEscrow.t.sol](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/test/settlement/ConsultEscrow/ConsultEscrow.t.sol) | test/vector | 6514b07c495618755a03d5206eff67804bd62fc70189e97316e26e5f455f78cc |
| S016 | [trustless-ai/agent-ercs @ 01283ca57305f915afb560d23359a27fd748eb5a / contracts/verify/ERC8274/IAgentVerifier.sol](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/verify/ERC8274/IAgentVerifier.sol) | implementation | 115942e5c66f76e8447f9cae51f80d6820a09c22609022bcd8443455b49baa36 |
| S017 | [trustless-ai/agent-ercs @ 01283ca57305f915afb560d23359a27fd748eb5a / contracts/verify/ERC8354/PolicyAction.sol](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/verify/ERC8354/PolicyAction.sol) | implementation | 9698c60db69fbae636164c22620407a0868589d7a1466fed5d1b4e213f4ec64f |
| S013 | [trustless-ai/agent-ercs @ 01283ca57305f915afb560d23359a27fd748eb5a / contracts/execution/ERC8301/IAgentWorkflow.sol](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/execution/ERC8301/IAgentWorkflow.sol) | implementation | 3b70fa7cb571a345f1fea244dbd57b6d5f8e5062923107f962e13854fb7ad429 |
| S014 | [trustless-ai/agent-ercs @ 01283ca57305f915afb560d23359a27fd748eb5a / contracts/identity/ERC8323/IAgentSourceBinding.sol](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/identity/ERC8323/IAgentSourceBinding.sol) | implementation | 09520190130278f6ef613a5f9e2421c650fda3ec56f01dd20a9c938488da7b85 |
| S023 | [trustless-ai/agent-sdk @ e41b117893fb56bc869922de378daf91aad63def / python/src/agent_sdk/reputation/erc8275/recompute.py](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/python/src/agent_sdk/reputation/erc8275/recompute.py) | implementation | 0beb1da0890ea72a5d927718f97d5cae7f70eaa41dae13d159261ad5057181c3 |
| S022 | [trustless-ai/agent-sdk @ e41b117893fb56bc869922de378daf91aad63def / python/src/agent_sdk/reputation/erc8275/conventions.py](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/python/src/agent_sdk/reputation/erc8275/conventions.py) | implementation | e0530c05a0351be77ed759f869093b0edb9100845826b05d7f85f03ac13692e9 |
| S026 | [trustless-ai/agent-sdk @ e41b117893fb56bc869922de378daf91aad63def / python/tests/reputation/erc8275/test_recompute.py](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/python/tests/reputation/erc8275/test_recompute.py) | test/vector | 377c2fb48d54ed0f34df032f44166ca1ef2cac1def13bb715dbee64f0d730c35 |
| S025 | [trustless-ai/agent-sdk @ e41b117893fb56bc869922de378daf91aad63def / python/src/agent_sdk/verify/erc8354/recompute.py](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/python/src/agent_sdk/verify/erc8354/recompute.py) | implementation | 6217f347c0ab337b41f0b5fe672f40c9330f8fc9cd8ba6c831febf33d79ea9de |
| S021 | [trustless-ai/agent-sdk @ e41b117893fb56bc869922de378daf91aad63def / python/src/agent_sdk/execution/erc8301/recompute.py](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/python/src/agent_sdk/execution/erc8301/recompute.py) | implementation | a29e539bcd1f643cc867f8d353fe4270b5f28f274896602e9c75b90f335f5f33 |
| S042 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/erc8275-win-rate-bps-v0/erc8275-win-rate-bps-v0.spec.md](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/erc8275-win-rate-bps-v0/erc8275-win-rate-bps-v0.spec.md) | spec | ba71b0787a80abed00d12bf3a5ad54ce08b162b3c104d3b9a947284e36c65fe6 |
| S043 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/erc8275-win-rate-bps-v0/erc8275-win-rate-bps-v0.vectors.json](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/erc8275-win-rate-bps-v0/erc8275-win-rate-bps-v0.vectors.json) | test/vector | 01d354ec0cf5f1b5de88526fdb22461c72ed296ae5d289efbb26ba4ec7c88c49 |
| S045 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/provenance-anchor-v0/provenance-anchor-v0.spec.md](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/provenance-anchor-v0/provenance-anchor-v0.spec.md) | spec | 528adff80003446b66249daf0b485bb42b628e541d55eeff0558bf5a1b38bd3e |
| S041 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/companion-envelope-v0/companion-envelope-v0.spec.md](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/companion-envelope-v0/companion-envelope-v0.spec.md) | spec | 9ba69fb49e55be03de5749117b004464f0f8f4b12f052b063461c7030f1ee4c4 |
| S047 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/serializer-bindings/README.md](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/serializer-bindings/README.md) | README/architecture only | 4b0e9b4b80fdd08c5eccde02f1d7986072ab812a59076bb5dfb2db9154f69ccc |
| S044 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/pq-key-binding-v1-profile/README.md](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/pq-key-binding-v1-profile/README.md) | README/architecture only | 75c77408d9e3d8796249a0a54118bf151d97cf81150a869410fe02f11da33ada |
| S048 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / mcp/receiptos.py](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/mcp/receiptos.py) | implementation | 9895f203ce8c85e83b03ed6ee089834ba00256cc747db2cb7f941a1a9f724cc5 |
| S030 | [trustless-ai/ccip-router @ 6bd66611b88a4751a0acc233c718aa9a13294de4 / contracts/CommitRevealSettlerV2.sol](https://github.com/trustless-ai/ccip-router/blob/6bd66611b88a4751a0acc233c718aa9a13294de4/contracts/CommitRevealSettlerV2.sol) | implementation | bae65a5eb8ad01f0fc836771f14d571771dd76fe7faa4a440457d7afe5b33cbd |
| S032 | [trustless-ai/ccip-router @ 6bd66611b88a4751a0acc233c718aa9a13294de4 / src/mesh/messages.ts](https://github.com/trustless-ai/ccip-router/blob/6bd66611b88a4751a0acc233c718aa9a13294de4/src/mesh/messages.ts) | implementation | 93b5a70dfd39a4ce64df65cadbbc47ee08b8982de8680f532bc8d8a50ccdafc9 |
| S006 | [pipavlo82/crystal-receipt @ 45b46bf7df3a60b32583291f577a36bf19d22f00 / conformance/counterfactual-audit-boundary-v0/SPEC.md](https://github.com/pipavlo82/crystal-receipt/blob/45b46bf7df3a60b32583291f577a36bf19d22f00/conformance/counterfactual-audit-boundary-v0/SPEC.md) | spec | 9c17bd826c4a789464dab80c78a136153f3d9ce2f253198d0cf386bdef3a6d0b |
| S007 | [pipavlo82/crystal-receipt @ 45b46bf7df3a60b32583291f577a36bf19d22f00 / conformance/tsei-invariant-discrimination-v0/README.md](https://github.com/pipavlo82/crystal-receipt/blob/45b46bf7df3a60b32583291f577a36bf19d22f00/conformance/tsei-invariant-discrimination-v0/README.md) | README/architecture only | b2dc0105767b26d2f53dcf4b6ef4c3ba37f4b5eb7798ce8fb5a370f2fa91d549 |
| S008 | [pipavlo82/crystal-receipt @ 45b46bf7df3a60b32583291f577a36bf19d22f00 / conformance/tsei-invariant-discrimination-v0/public-receipts/tsei-ia-real-v2-20260824-02.production-grounding.json](https://github.com/pipavlo82/crystal-receipt/blob/45b46bf7df3a60b32583291f577a36bf19d22f00/conformance/tsei-invariant-discrimination-v0/public-receipts/tsei-ia-real-v2-20260824-02.production-grounding.json) | deployment/reference (reported) | 09349e8257da2b94227f7af7f8e4dcdcca9e715dc460e1f419e53a14a22e5a07 |
| S060 | [trustless-ai/trustless-agent-substrate @ a344ef80f7c52c03b9183814d1874b8054639c3e / test/unit/workflow/sourceGate.test.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/test/unit/workflow/sourceGate.test.ts) | test/vector | 7709401c4d88836903cc4ae9a385bf722fe98efcf3497b8dd7e952b1f7d23077 |
| S061 | [trustless-ai/trustless-agent-substrate @ a344ef80f7c52c03b9183814d1874b8054639c3e / test/unit/workflow/sourceVerifier.test.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/test/unit/workflow/sourceVerifier.test.ts) | test/vector | f2532ab87b7dff15ee31b2ac1b4c4ac463977bb3f0c33fcd8896f2fb3e13a360 |
| S056 | [trustless-ai/trustless-agent-substrate @ a344ef80f7c52c03b9183814d1874b8054639c3e / src/clients/workflow/agentSdkClient.ts](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/src/clients/workflow/agentSdkClient.ts) | implementation | 817d87bc4f71425e089448e946a661acfdebaf7cd154515ad1a4b08431cbe251 |
| S055 | [trustless-ai/trustless-agent-substrate @ a344ef80f7c52c03b9183814d1874b8054639c3e / manifests/agent-sdk.v1.json](https://github.com/trustless-ai/trustless-agent-substrate/blob/a344ef80f7c52c03b9183814d1874b8054639c3e/manifests/agent-sdk.v1.json) | registry | a5d756d16fc25f030da07a6cac2849942bd5be06bcfaa4cbda74c424350c6d6b |
| S039 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/communication-chain-v0/communication-chain-v0.vectors.json](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/communication-chain-v0/communication-chain-v0.vectors.json) | test/vector | d9d63cc82903d89c220f62f22035ff1901619124707a2acccd293cfc5c2dec6e |
| S040 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/communication-chain-v0/gate.ts](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/communication-chain-v0/gate.ts) | implementation | 6f5c3b10ff65d8b2b5bcbb0b1597b3e455fd6c338345deceedd7e30cb655775c |
| S010 | [pipavlo82/recomputable-verification-receipts @ 287c0ea1c2578c1833405bc2476975f95addbada / profiles/invinoveritas-signed-verdict-v1/SPEC.md](https://github.com/pipavlo82/recomputable-verification-receipts/blob/287c0ea1c2578c1833405bc2476975f95addbada/profiles/invinoveritas-signed-verdict-v1/SPEC.md) | spec | 754957d1f2f83f25a3aac6dfc48577b316f194c006671139129e6d4e5bbafb52 |
| S003 | [babyblueviper1/invinoveritas @ 76d19dc394b208d01ba368382b3e5f4f2c18f0ee / integrations/conformance/erc-8309-vantage/services/vantage_resolution.py](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/integrations/conformance/erc-8309-vantage/services/vantage_resolution.py) | implementation | 8dd0bad03e6bc0335d6a690e3fb7eb448a4ccb1b6389115aab65474a21e55858 |
| S002 | [babyblueviper1/invinoveritas @ 76d19dc394b208d01ba368382b3e5f4f2c18f0ee / integrations/conformance/erc-8309-vantage/README.md](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/integrations/conformance/erc-8309-vantage/README.md) | README/architecture only | 0d0523e60bfb2fb643dade1bf1825a829757fd88b480a980d1eafd4f5d3d4a64 |
| S046 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/provenance-anchor-v0/provenance-anchor-v0.vectors.json](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/provenance-anchor-v0/provenance-anchor-v0.vectors.json) | test/vector | b5417c3225edb7e2a587abcf290be8ca9c8f3e259efa03569853dff5661a1946 |
| S024 | [trustless-ai/agent-sdk @ e41b117893fb56bc869922de378daf91aad63def / python/src/agent_sdk/settlement/erc8203/recompute.py](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/python/src/agent_sdk/settlement/erc8203/recompute.py) | implementation | 6960e4dd22a8dd62cc0171ceefc1b014bfe8f28b2a0cd8df14214cc803f4c980 |
| S064 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/profile-amendment-v0/profile-amendment-v0.spec.md](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/profile-amendment-v0/profile-amendment-v0.spec.md) | normative conformance spec | 6088753df1f0c428f14ccb954179ff5441af1684d2f289761e872a7a3a17c50b |
| S065 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/profile-amendment-v0/amendment_gate.py](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/profile-amendment-v0/amendment_gate.py) | reference implementation | 1ea58b0e847b41244d925aae541cca7a113814eb62888d67eef6a2a4dc0c80f7 |
| S066 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/profile-amendment-v0/profile-amendment-v0.reference.mjs](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/profile-amendment-v0/profile-amendment-v0.reference.mjs) | reference implementation | 915343ece23fb7b2a84906bfe1b6700be4d53bec61cecb04a2f09ee3f57d3ad7 |
| S067 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/profile-amendment-v0/profile-amendment-v0.vectors.json](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/profile-amendment-v0/profile-amendment-v0.vectors.json) | vector | 79cd891adcb9019da5f4b3c81e01e8c083ba036d4ae25577f53873b17a105f74 |
| S068 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/verdict-profile-binding-v0/verdict-profile-binding-v0.spec.md](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/verdict-profile-binding-v0/verdict-profile-binding-v0.spec.md) | normative conformance spec | a58aa6f4e88043b10c385f75368fd8f7429234d947a3f7c1122d67a19f41c309 |
| S069 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/verdict-profile-binding-v0/verdict_binding_gate.py](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/verdict-profile-binding-v0/verdict_binding_gate.py) | reference implementation | 4cdad8693974dbdcbf8ffc7a48850ec8ea6bf767f10dc0fbd3435754d37deefa |
| S070 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/verdict-profile-binding-v0/verdict-profile-binding-v0.reference.mjs](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/verdict-profile-binding-v0/verdict-profile-binding-v0.reference.mjs) | reference implementation | 20e86353e6a97f5c38d0883920a117fd6e8684a0cb23bc6b5bd1ead03d03957f |
| S071 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/verdict-profile-binding-v0/verdict-profile-binding-v0.vectors.json](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/verdict-profile-binding-v0/verdict-profile-binding-v0.vectors.json) | vector | 4a50b2fb74de7974ca197b1c627413bfc39f41363ed786ae79465ab9ee751f0a |
| S072 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/pq-key-binding-v0/pq-key-binding-v0.spec.md](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/pq-key-binding-v0/pq-key-binding-v0.spec.md) | normative spec | 877499e8dae1d20e6e3f056cc48337f08755af63fef0c66d58ca44e628928af0 |
| S073 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/pq-key-binding-v0/pq-key-binding-v0.rotation.json](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/pq-key-binding-v0/pq-key-binding-v0.rotation.json) | signed-object artifact | 150817aef5862ef601f487ef2f038917bfe78fa302bdf546607a40a7215adee6 |
| S074 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/pq-key-binding-v0/pq-key-binding-v0.rotation-vectors.json](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/pq-key-binding-v0/pq-key-binding-v0.rotation-vectors.json) | vector | 2c046fdaaebe1a8e71b99b191cbd8efa48abe7b6449e5f4b32cc30f1750d6b1a |
| S075 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/pq-key-binding-v0/pq-key-binding-v0.revocation.json](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/pq-key-binding-v0/pq-key-binding-v0.revocation.json) | signed-object artifact | b97752168fd1071a7a00c72cd584f2e14f24a7314719bdbabc0b089e630151bc |
| S076 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/pq-key-binding-v0/pq-key-binding-v0.revocation-vectors.json](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/pq-key-binding-v0/pq-key-binding-v0.revocation-vectors.json) | vector | 3481360d3ffa5e785ca640a06994a9724ab6e7cee1a2e033102e70b91f31cac0 |
| S077 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/pq-key-binding-v0/pq-key-binding-v0.cutoff-vectors.json](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/pq-key-binding-v0/pq-key-binding-v0.cutoff-vectors.json) | vector | 7cfd7e8906b0afbfa1d000e99177ab797b2f757dc2d71364ff79cc48fbc506f7 |
| S078 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/pq-key-binding-v0/pq-key-binding-v0.vectors.json](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/pq-key-binding-v0/pq-key-binding-v0.vectors.json) | vector | 9ee62960f0fade98ee107ee600feac3bca9b6b1157c273568ee060efec235823 |
| S079 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/pq-key-binding-v0/deep_recompute.py](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/pq-key-binding-v0/deep_recompute.py) | reference implementation | 8b43d22524a2f9c18ee90e302afd84a604b5b5cb949d4325203a86479187ba46 |
| S080 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/pq-key-binding-v0/cutoff_enforce.py](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/pq-key-binding-v0/cutoff_enforce.py) | reference implementation | a11d528b97bd88b7850a679122e1bbaec162bf98f6164587c23e47f9174df528 |
| S081 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/pq-key-binding-v0/gate.py](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/pq-key-binding-v0/gate.py) | reference implementation | 36347585715c22d8862aae34e6d5ab84b5e9283e08fa8366382fba9935e66d43 |
| S082 | [trustless-ai/recompute-kit @ 15f7f59ac47b3358492bd5741143c418b5d657f5 / conformance/pq-key-binding-v0/suite.json](https://github.com/trustless-ai/recompute-kit/blob/15f7f59ac47b3358492bd5741143c418b5d657f5/conformance/pq-key-binding-v0/suite.json) | manifest | bcd7a1eeeb9e9b392cb917d900313636051c5b4eac18bf12a0d8ded02a9df6dc |
