# RSI v0 closure audit

Audited implementation HEAD: `e61a7f9116e51e5942274ea1cdaf043334c339f8`. Phase 3G exact-HEAD CI is green. This document records completed local audit gates; the annotated `v0` tag is created only after the research-only closure commit also passes exact-HEAD CI.

## Bounded final claim

RSI v0 demonstrates the same generic conformance architecture across ten bounded, source-pinned real relation families. It discriminates selected locally valid substitutions and claim promotions using separately implemented expectation predictors, frozen admission and 84 mapped killed mutations, without domain-specific generic core branches. This is an implementation-facing cross-repository conformance plane for the validated surfaces, not universal security or ecosystem-wide verification.

## Gates

| Gate | Verified result |
|---|---|
| Tests / optimized | 539 / 539 PASS |
| Generic conformance | 123 PASS; all other statuses 0 |
| Mutation gate | 84 KILLED; SURVIVED/VACUOUS/NOT_APPLIED 0 |
| Prior outcomes / mutation records | 111 / 76, exact differences 0 |
| Protected files | 572 unchanged from 3G baseline |
| Pipeline | 10 real families + legacy, 11 admitted expectation profiles |
| Generic core/schema/comparator/taxonomy | unchanged; semantic exceptions 0 |
| Anti-coupling | 17 generic Python files, no domain-specific branches |
| Source integrity | All 10 source verifiers PASS; exact pinned generations retained |

## Validated surfaces

| Family | Exact bounded relation | Actual / predictor route | Unsupported stronger surface |
|---|---|---|---|
| Crystal Receipt | semantic-snapshot equivalence | TypeScript source / Python predictor + H2 JS reproducer | Provenance authority, Lane K, broad ReceiptOS semantics |
| RVR | profile-transition and verdict digest binding | Python source / separate Python predictor | Cryptographic signatures / authenticated transition chain |
| TSEI | serializer/adoption/record-introduction boundary | Pinned source binding artifacts / Python predictor | Provenance authority: Object A/B, oracle, nonce and attribution operands unavailable |
| PQ | policy cutoff / governing as-of binding | Pinned Python policy / separate Python predictor | Authenticated transition chain, independent anchor verification; SLH-DSA artifact / ML-DSA label mismatch preserved |
| TAS | accepted source context -> getTask read dispatch | TypeScript source gate / Python obligations | Arbitrary method/action authorization, source-context authenticity, execution occurrence |
| ConsultEscrow | contract-local jobId/resultHash -> release | Solidity local EVM / Python crypto-state obligations | Cross-deployment/chain replay security, chain inclusion/finality, hostile recipients, end-to-end payments |
| verify-layer | account proof/root and supplied RPC-context binding | JavaScript source MPT verifier / Python MPT-RLP predictor | Consensus/header authority, finality, storage lane, broad downstream claim |
| ERC-8354 CAPV | expiry proof binding vs freshness across pinned program generations | Real old/fixed verifiers / public-input generation predictor | Full Guard acceptance, executor authorization, domain/root policy and execution occurrence |
| ERC-8312 Aggregate Budget | root/period admitted-budget conservation vs per-edge validity | Solidity cursor + TypeScript admitted-log gate / history-sum predictor | Non-bypassability, asset movement, cross-chain/subtree budgets and authoritative chain state |
| ERC-8299 reference application | signed verdict -> supplied terminal-record binding | Python source BIP340/joins / separate Python equation-join predictor | Action authorization/occurrence, anchor authority, judgment soundness, raw-to-canonical transform and conditional execution |

## Status discipline

3G closes only the signed-verdict / supplied-terminal-record reference lane. It does not close complete ERC-8299 execution semantics. The source control is signed reject and its join checks pass; this is not permission to execute.

ERC-8380 Phase 3D remains BLOCKED on the pinned alignment evidence. Full RVR authentication and TSEI provenance authority remain unsupported. Their exclusion is part of the v0 scope, not a claim that missing capabilities were completed.

Local conformance PASS means observed behavior matches admitted semantics. Internal UNSUPPORTED capabilities remain explicit even when all top-level checks PASS. Deliberate counterexample fixtures (CAPV old generation, Aggregate per-edge model) are witnessed limitations, not security approvals or claims that current upstream is vulnerable.

## Independence wording

The global release wording is **separately implemented expectation predictor**. Earlier reports are frozen historical artifacts; any unqualified independent-predictor phrasing is read under the H1/H2 caveats and this release wording policy. Separate files/languages do not establish independent algorithms, sources, authors or oracle truth.

H1 scores remain: Crystal 10, RVR 9, TSEI 8, PQ 9, TAS 9, ConsultEscrow 11, verify-layer 10; legacy 5. Crystal H2 stays 10/15 MODERATE despite catching H2-M1/H2-M2. JEX is 9/15 MODERATE as a new review judgment; CAPV/Aggregate have documented separate execution/derivation routes, not retroactively assigned H1 scores. Author independence UNKNOWN throughout.

Frozen expectations detect divergence from previously admitted semantics; they do not by themselves prove that the original expectation was independently derived.

## Transport and trust limits

ASCII/safe integers are the generic transport contract. Exact validated string/hex representations carry large amounts, identifiers and proof bytes where a domain declares that encoding. The generic codec is not full JCS. No silent Unicode/float/binary coercion is permitted. Shared codec/admission remains a common-mode risk even with separate semantic evaluators.

Pin verification checks the historical generations actually used. Current upstream changes do not retroactively rewrite frozen consumer semantics. Normative text, reference implementations, tests, declarations and supplied trust inputs remain separate evidence classes.

## Reproduction and evidence

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
python -O -m unittest discover -s tests -v
python tools/run_judgment.py --include-previous --output artifacts/v0.json
python tools/check_crystal_cleanroom.py --output artifacts/h2.json
```

Use Node 22.15.0 and Python 3.12 or 3.13, matching CI. Per-domain prove_* tools and run_registered_mutations reproduce the matrix; each mutation must reach its declared assertion, with setup errors classified VACUOUS.

See [machine-readable audit](rsi-v0-closure-audit.json), [all exact source closures](rsi-v0-source-pins.json), [mutation matrix](rsi-v0-mutation-matrix.md), [unsupported surfaces](rsi-v0-unsupported-surfaces.md), and the per-domain research reports.

## Release rule

No tag exists merely because this document says local gates passed. Delivery must verify origin/main equals the audited final commit, every required workflow is successful on that exact SHA, the tree is clean, and no pre-existing v0 tag is overwritten. The annotated v0 tag records the bounded claim and CI evidence. No GitHub release or additional domain is created.
