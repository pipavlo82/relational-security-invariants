# Crystal Receipt external derivation: post-v0 coordinator comparison

Four of four frozen external derivation states agree with the exact pre-existing RSI expectation rows, a replay of the pinned source adapter, the separately implemented predictor, and the H2 leg. No semantic disagreement or missing case was observed. This is an exposed coordinator's mechanical comparison; an external POST_COMMIT_VERIFIER has not yet performed the comparison.

| Case | Toshikatsu | Source adapter | Predictor | H2 | Frozen expectation |
|---|---|---|---|---|---|
| case-001 | PRESERVED | PRESERVED | PRESERVED | PRESERVED | PRESERVED |
| case-002 | VIOLATED | VIOLATED | VIOLATED | VIOLATED | VIOLATED |
| case-003 | PRESERVED | PRESERVED | PRESERVED | PRESERVED | PRESERVED |
| case-004 | PRESERVED | PRESERVED | PRESERVED | PRESERVED | PRESERVED |

The external harness also reproduced all submitted states and matched both complete canonical snapshot strings. case-001 maps to external audit timestamp removal; case-002 to semantic value substitution; case-003 to identical-input control; case-004 to external audit timestamp change. These mappings were committed before reviewer submission. A conformance PASS is distinct from a preserved relation.

## Pins and chronology

- Current RSI base: 7390f20f1c11f815db47bc8244efd72b4754b45c.
- Executed historical RSI v0: 8d8e31291ecf96284212a353efb66f606cff2953. The tag remains unchanged.
- Source: pipavlo82/crystal-receipt@45b46bf7df3a60b32583291f577a36bf19d22f00.
- Distributed pack: c3f293d8b76d9b1646fbdbed6eddbece52c0a269; HASHES.sha256 SHA-256 7043e00225a908cbccf8b5ea01f3b205a5983a1a562977d2118174c58b7533b3; PACK_MANIFEST.json SHA-256 fd1b54c809e87d19bde82d86bbc4e9aec56055021a95322898b5b81052cfb220.
- Submitted freeze-v2: ogasurfproject-jpg/crystal-receipt-derivation@1fa7700ecac0690edf6116dabb4938bc3712f7c9; DERIVATION.json SHA-256 c05b65cbca87433bceb1cd0d3a50600cbb71bbbbb673d576715700100d508ec1.
- First submission preserved separately at freeze-v1 9e0fc16830a613af0a18716291a5d5b64226b0ac. Only exposure wording differs; cases, method and code remain unchanged.
- Manifest acknowledgment: b942ab118b4705a226e517b280a44e50b26c71cc; raw file SHA-256 e256a75a8b6278d20debddfa8db72a0b12226ec5591c4e36c31dfbca32626bf9.
- Witnessed receipt and acknowledgment were captured before this comparison. OTS path verifies to block 966764 using agreeing public-provider headers; no local full-chain consensus verification.
- Exact frozen expectation SHA-256: 268b0e5dd6087cc60bf9c99ca5c20c0b135983d595ff632659c81b18634a4ba3.
- Input-origin record SHA-256: b130cd433276cdcee8cce6ecf2820d85acad1943e05bf316a31751429531546e. Its bytes open the pre-existing commitment in the pack.

At comparison capture, no external reveal had been sent. The prepared disclosure bundle is not itself a reveal event. Registry receipt/acknowledgment/comparison events preserve all prior events and initial null fields. Subsequent publication and disclosure are recorded by append-only events, with exact commit, recipient, payload hash and time.

## Execution and reproducibility

The v0 tree and frozen pack were exported with git archive into a separate workspace. The original H2 harness re-executed all A/B/C/D legs and atomic expectation admission. Source hash checks remained active.

The external derive.mjs was inspected before execution. Its only executable import is node:fs. A local copy replaces exactly the hard-coded /mnt/user-data/uploads input-root literal with the isolated pack path; no semantic branch or source artifact changes. Original and adapted code digests are in comparison.json.

compare_external.py validates all pack hashes, both submitted code/data hashes, input-origin commitment, exact source vector hashes, one-to-one inventory, source selectors, H2 input equality, external source references and frozen expectation bytes. It then mechanically compares submitted states, rerun external harness states/canonical strings and the replayed RSI/H2 rows. It does not originate the external derivation.

Reproduction requires Node 22.15.0 or a compatible runtime and the historical RSI Python dependencies recorded in runtime.json. Run the historical tools/check_crystal_cleanroom.py first, then compare_external.py with --rsi-root, --pack-root, --submission-root, --origin-record, --h2-replay and --output-dir. Each argument is an explicit path; no external repository access is needed once the pinned trees and included evidence are materialized.

## Validation

- Crystal/H2 regressions: 45 tests pass normally and 45 under python -O.
- Normal and optimized mechanical comparison JSON bytes identical.
- H2 replay: four matching vectors and all three recorded common-mode experiment instances caught.
- 641 existing tracked files unchanged. The sole modified prior file is the append-only registry; its original events remain unchanged.
- Prior domain semantics, frozen result files, generic core/schema/comparator/taxonomy and v0 remain unchanged.
- At the initial targeted-comparison capture, the full framework and mutation suites had not been rerun. The later publication gate is recorded separately below.

## Independence and evidence limits

Role: BLIND_DERIVER_WITH_DISCLOSED_AFFILIATION. Toshikatsu discloses technical collaboration with the Trustless AI circle and the intermediary, with no RSI/Crystal role or financial ties reported. These disclosures and no-answer-exposure claims are self-reported.

The submission declares AI assistance, another guardian session and loaded standing account memory. A fresh isolated environment is therefore not fully established. Model pretraining and claimed memory contents are not independently auditable here. No strict unaffiliated or fully independent classification is granted.

The supplied canonicalizer is explicitly ported in the external harness; it is not an independently designed serializer. JavaScript/TypeScript share a runtime and source algorithm. Four-case agreement does not prove absence of common-mode errors in other inputs.

H2 and this coordinator comparison do not establish external verifier independence. Baby Blue Viper remains a candidate; coauthorship with Toshikatsu must accompany any later comparison they perform.

Frozen expectations detect divergence from previously admitted semantics; they do not by themselves prove that the original expectation was independently derived.

Mutation kills prove mapped decisions are load-bearing; they do NOT prove independently derived semantic expectations.

v0 author independence remains UNKNOWN. No framework-wide inference, provenance authority, Lane K, broader ReceiptOS, non-ASCII/numeric/host-object, or full source-domain claim is made.

## Bounded result

A frozen, AI-assisted external derivation with disclosed affiliation agrees on all four pinned Crystal Receipt semantic-snapshot cases with RSI v0's admitted expectations, executed source adapter, separately implemented predictor and H2. This is post-v0 evidence and does not retroactively upgrade v0 or establish strict author independence.

## Subsequent local publication gate

All 546 unit tests pass normally and all 546 pass under python -O. The 123 conformance PASS rows and all 84 KILLED mutation records are byte-identical to the pre-existing baseline reports. All other conformance and mutation statuses remain zero. The 641 protected prior files and the original registry events are unchanged; only new post-v0 evidence and appended registry events are added. Existing anti-coupling checks pass.

The first full run failed one classifier control because its unchanged child runner exceeded the 30-second limit. Diagnostic logs preserve that failure and the successful retry. No timeout, test or semantic implementation was changed. The later complete gate used a direct Remote Desktop Commander driver. The underlying Windows/runtime delay is not conclusively diagnosed.

The publication-validation directory records commands, normal/optimized logs, conformance, all mutation reports, byte comparisons and the failed-run history. Captured evidence bytes are marked -text to prevent Git line-ending normalization; newly authored technical text uses LF. A prepared disclosure body is frozen in this evidence commit; preparation is not delivery. Actual publication, CI and recipient disclosure are appended only after they occur.
