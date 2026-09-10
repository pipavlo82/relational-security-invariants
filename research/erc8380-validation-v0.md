# ERC-8380 Phase 3D вЂ” BLOCKED at source preflight

No ERC-8380 implementation, fixture, expectation profile, adapter or mutation was added. No security PASS was created from a mock verifier or from expected incomplete behavior. No eighth-family reuse claim is made.

RSI HEAD before/after: `45a00875702ed733dfe77c8ba7c30e9a9a93644c`. Only six uncommitted research reports are added. No commit/push, external change, forum post, tag, release or PR.

## Exact blocker

Current linked reference main 50f2ae1ddb85f02e55c7b48ae8c609b1fdda31c5 contains Noir hash helpers that return only salt. Current ERC draft 7068f2a2853504475d966c06c8e04ec6d546dbb8 requires tagged Keccak over the complete capability envelope and a nullifier derived from that salt. The exact proving relation is therefore not established. Reference main additionally uses ERC-1953 tags while the PR uses ERC-8380 tags. Neither changing the source nor silently selecting a replacement mock is authorized.

The previous missing-nullifier-input issue is fixed at the declaration/wiring layer: cap.nullifier is input 8 of nine. Executor and expiry are in the current Solidity/draft preimage. That does not repair the placeholder Noir hash implementation. The correct status is FIXED wiring / UNSUPPORTED end-to-end proving, not an assertion that the old fresh-nullifier exploit still reproduces.

The source test BindingVerifier registers exact input vectors. Its first-spend, second-spend and substitution cases remain upstream contract-harness evidence, not RSI execution or cryptographic proof verification. The generated Honk verifier correctly accounts for nine user inputs plus eight pairing entries; a superficial 17-versus-9 mismatch is explicitly excluded from the findings.

## Finality and consumption

At-most-once is a conditional contract-state property; exactly-once is unsupported because submission/action need not occur. Source burn and target call share transaction rollback. No first/second spend, reorg, canonical inclusion or finality threshold was independently executed in this stopped phase.

The finality clarification is acknowledged in live posts 31/33, but remains a promised text update at the inspected PR HEAD. Irreversible off-chain effects remain unsupported. This pending wording is distinguished from the material proving-lane blocker.

## Preservation / validation

The baseline was rerun: 430 tests PASS normally and 430 PASS under python -O. All 85 prior conformance checks PASS; FAIL / INVALID_FIXTURE / UNSUPPORTED are zero. Before/after structured outcomes are byte-identical (outcome diff 0). All 389 pre-change tracked-file SHA-256 hashes match; no generic/prior-domain semantic file changed. Static anti-coupling checks found no new ERC-8380 branches in generic core. Semantic exceptions added: zero. The previously validated 61 mutation records remain frozen; their mutation suites were not rerun after this source-preflight STOP. No new mutation was registered or classified.

Existing exact-HEAD CI remains green across all six workflows. No new CI was triggered. Working tree intentionally contains only the requested six research artifacts.

## Required closure evidence

A current, source-pinned Keccak circuit and verifier/prover artifact set must establish the exact commitment and nullifier, with an explicit full-byte/field encoding, known-valid proof and substitution vectors. Align or explicitly separate the ERC-1953 and ERC-8380 domain lanes. Do not treat mock-vector admission as that proof. Finality text/policy, if later supplied, remains a separate capability.

A separately approved contract-harness-only scope could test the Guard's checks and atomic consumed state without claiming cryptographic derivation. This task did not automatically substitute that narrower scope.

Detailed source hashes/posts, relation ownership and candidate dispositions are in erc8380-source-map-v0.json, erc8380-mapping-v0.md, erc8380-relation-ownership-v0.md and erc8380-finality-boundary-v0.md.
