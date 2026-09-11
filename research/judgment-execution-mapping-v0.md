# ERC-8299 Phase 3G source and relation mapping

This is an application-specific, supplied-record binding lane under the current draft L4 composition. It is not a complete ERC-8299 implementation or proof of action occurrence.

## Source preflight

Ethereum master `84b46e7d69d08dbd8876503e435fd299211c26b8` does not contain ERCS/erc-8299.md. Open PR #1810 resolves to TMerlini/ERCs:erc-wyriwe at `c0e13d17940a6eabe4d842e623fd0f871550ef7b`. The older TMerlini/wyriwe main at `a375af0a91e6cc724851eee2ab6916ba9fe10854` is separately recorded. Current PR L4 permits deployment-specific SHA256/JCS or Keccak/ABI; the earlier Keccak-only formula must not be applied to the current SDK off-chain helper.

The Trustless AI SDK L4 helper computes proposal/verdict hashes but does not verify a terminal action or require a proposal key in a caller-supplied field list. Its MockJudgmentExecutionAttestation checks a 32-byte struct digest, explicitly not EIP-712 recovery. Neither is used as a production execution oracle. Agent-ercs is interface evidence.

The directly linked public reference, babyblueviper1/invinoveritas at `76d19dc394b208d01ba368382b3e5f4f2c18f0ee`, supplies an offline verifier, real BIP340/NIP01 admission signatures and exact portable records. This is the executable 3G lane. No private producer/runtime or live paid API is required.

## Protected relations

- SHA256 of exact supplied canonical envelope bytes equals the declared envelope digest.
- NIP01 event ID and BIP340 signature verify; signed artifact_hash equals that envelope digest.
- The signer differs from the actor and belongs to the supplied trust-policy list. This is policy membership, not independently established real-world identity independence.
- Pre-action and terminal envelope digests match the same envelope, and action_ref joins exactly.
- Under the declared anchor inputs, admission digest joins and anchor time strictly precedes the supplied anchor terminal time. Existence and precedence/not-assessable remain separate.

## Explicit missing relations and trust assumptions

The source does not recompute raw_input -> canonical_bytes_utf8, resolve Bitcoin/OTS proofs, verify terminal occurrence, enforce the terminal result label, check the verdict decision as approval, or reconcile anchor.terminal_outcome_time with chain.terminal.terminal_outcome_time. Its overall_pass can be true for a cryptographically valid reject verdict and a reported not_executed terminal. These observations do not prove an exploit; they bound what the reference predicate checks.

The draft conformance transform for conditional approvals (for example, halve the size) is not implemented in this lane. No generic conditional-action verifier, on-chain EIP-712 judgment verifier, live settlement, consensus finality or economic outcome is validated. The profile emits UNSUPPORTED for action authorization, execution occurrence, anchor authority, judgment soundness and raw-to-canonical derivation. Source check booleans are preserved as source results, never relabeled as established authority.

## Exact files

| Repository @ commit | Path | SHA-256 | Evidence |
|---|---|---|---|
| TMerlini/ERCs@c0e13d17940a6eabe4d842e623fd0f871550ef7b | [ERCS/erc-8299.md](https://github.com/TMerlini/ERCs/blob/c0e13d17940a6eabe4d842e623fd0f871550ef7b/ERCS/erc-8299.md) | `5ea02730bdc94bd45983b3e5d22bafabf7e3aa6ca4dc1095d483b6776b7eccd3` | normative-draft |
| TMerlini/wyriwe@a375af0a91e6cc724851eee2ab6916ba9fe10854 | [ERC-draft.md](https://github.com/TMerlini/wyriwe/blob/a375af0a91e6cc724851eee2ab6916ba9fe10854/ERC-draft.md) | `ffab502599a80a773c0922190366425fce55c1c11ba775dd0030ebaa70c6370d` | historical-draft |
| trustless-ai/agent-sdk@e41b117893fb56bc869922de378daf91aad63def | [typescript/src/verify/ERC8299/recomputeL4.ts](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/typescript/src/verify/ERC8299/recomputeL4.ts) | `ebe3db999a718623fa6d9aeec702cee17e0b97bb72758b4789458c4f5dc27d13` | consumer |
| trustless-ai/agent-sdk@e41b117893fb56bc869922de378daf91aad63def | [typescript/src/verify/ERC8299/judgmentExecutionClient.ts](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/typescript/src/verify/ERC8299/judgmentExecutionClient.ts) | `5eaeff104991c6f286f1c10a430f6fa66d8c4ce12af199832a7d4f3f7de8c7bc` | consumer |
| trustless-ai/agent-sdk@e41b117893fb56bc869922de378daf91aad63def | [typescript/src/verify/ERC8299/README.md](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/typescript/src/verify/ERC8299/README.md) | `b9b3adb8fb7395b4a866f9da4cd226787ba6a26019e76c085f3bd1f87a0eb343` | consumer |
| trustless-ai/agent-sdk@e41b117893fb56bc869922de378daf91aad63def | [testkit/contracts/mocks/verify/ERC8299/MockJudgmentExecutionAttestation.sol](https://github.com/trustless-ai/agent-sdk/blob/e41b117893fb56bc869922de378daf91aad63def/testkit/contracts/mocks/verify/ERC8299/MockJudgmentExecutionAttestation.sol) | `9827ecca025a157c0744a78800e4d9887990d9b6ff679a4e0a899ac827eec005` | test-only-mock |
| trustless-ai/agent-ercs@01283ca57305f915afb560d23359a27fd748eb5a | [contracts/verify/ERC8299/IJudgmentExecutionAttestation.sol](https://github.com/trustless-ai/agent-ercs/blob/01283ca57305f915afb560d23359a27fd748eb5a/contracts/verify/ERC8299/IJudgmentExecutionAttestation.sol) | `ef689f54c87e41137b3b5ea6616e2ceb2738a40061123ea840c0d93e030d00c4` | interface |
| babyblueviper1/invinoveritas@76d19dc394b208d01ba368382b3e5f4f2c18f0ee | [integrations/conformance/README.md](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/integrations/conformance/README.md) | `98a2971ef1bcd64b4d4218ff4fc570692fc1475ab29c19d63c677a83251d46e3` | semantic-contract |
| babyblueviper1/invinoveritas@76d19dc394b208d01ba368382b3e5f4f2c18f0ee | [integrations/conformance/verifier.py](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/integrations/conformance/verifier.py) | `3d6c4633efb3ac782572faa1d9de81df66ed35e34cc42396a48f5a49dc832c29` | implementation |
| babyblueviper1/invinoveritas@76d19dc394b208d01ba368382b3e5f4f2c18f0ee | [integrations/conformance/_bip340_nostr.py](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/integrations/conformance/_bip340_nostr.py) | `1bd072b7989f2aa755b1e9f2d46b64969ad6d342f7d48bf556225fa65c330a0d` | implementation |
| babyblueviper1/invinoveritas@76d19dc394b208d01ba368382b3e5f4f2c18f0ee | [integrations/conformance/test_conformance.py](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/integrations/conformance/test_conformance.py) | `3aedc2957f4505c1819aa73773c87d54545eb901ee43c5fd3df53ae889c85464` | implementation |
| babyblueviper1/invinoveritas@76d19dc394b208d01ba368382b3e5f4f2c18f0ee | [integrations/conformance/fixtures/positive.json](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/integrations/conformance/fixtures/positive.json) | `4aff1f4d0cb0ecba209db73cb650b6a7b29fb3d591400b51a5b61eb75c0faee6` | test-vector |
| babyblueviper1/invinoveritas@76d19dc394b208d01ba368382b3e5f4f2c18f0ee | [integrations/conformance/fixtures/negative_chain_action_ref_split.json](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/integrations/conformance/fixtures/negative_chain_action_ref_split.json) | `bec9d26d9279b7523ad53dbcd2fb4e3ba5370d74016eb8fdc846ee9a02517ee5` | test-vector |
| babyblueviper1/invinoveritas@76d19dc394b208d01ba368382b3e5f4f2c18f0ee | [integrations/conformance/fixtures/negative_verdict_binding_failed.json](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/integrations/conformance/fixtures/negative_verdict_binding_failed.json) | `3d82d4ef1e8204ad0aef651d2cd284b5161c0071c1405ab6a80e5480f14e58f4` | test-vector |
| babyblueviper1/invinoveritas@76d19dc394b208d01ba368382b3e5f4f2c18f0ee | [integrations/conformance/fixtures/negative_admission_not_independent.json](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/integrations/conformance/fixtures/negative_admission_not_independent.json) | `be3f4a3acdfb706f5e46957908f5482a70b6d5c3e9f1bd1971eb7d4ab0695a69` | test-vector |
| babyblueviper1/invinoveritas@76d19dc394b208d01ba368382b3e5f4f2c18f0ee | [integrations/conformance/fixtures/negative_key_different_but_identity_unproven.json](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/integrations/conformance/fixtures/negative_key_different_but_identity_unproven.json) | `86d8aabdd0a0c3277c9b2b4909eecb9654531f44e853bd9be71e6ea085b56e9a` | test-vector |
| babyblueviper1/invinoveritas@76d19dc394b208d01ba368382b3e5f4f2c18f0ee | [integrations/conformance/fixtures/negative_late_commitment.json](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/integrations/conformance/fixtures/negative_late_commitment.json) | `365cd060f2446246917c625b7d0208ff15d0c9cd93b8ccc2a8b9ae4d2a4a2f6e` | test-vector |
| babyblueviper1/invinoveritas@76d19dc394b208d01ba368382b3e5f4f2c18f0ee | [integrations/conformance/fixtures/negative_ordering_unanchored.json](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/integrations/conformance/fixtures/negative_ordering_unanchored.json) | `c3e81e7c4ee5b367fd5c97c20550bd5c4d05acea74a06ab2c7f1013476b5dfea` | test-vector |
| babyblueviper1/invinoveritas@76d19dc394b208d01ba368382b3e5f4f2c18f0ee | [integrations/conformance/fixtures/negative_existence_only_anchor.json](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/integrations/conformance/fixtures/negative_existence_only_anchor.json) | `3100ff8719a8c5ed6bd6e4d1102ce54cb441a1f2dfa7354169436362bcfc1f4c` | test-vector |
| babyblueviper1/invinoveritas@76d19dc394b208d01ba368382b3e5f4f2c18f0ee | [integrations/conformance/fixtures/negative_canonical_envelope_mismatch.json](https://github.com/babyblueviper1/invinoveritas/blob/76d19dc394b208d01ba368382b3e5f4f2c18f0ee/integrations/conformance/fixtures/negative_canonical_envelope_mismatch.json) | `4354e9d35380230de4d7cacf8c01fd5a37f60d34370226ea6bbfbdd0e606f4df` | test-vector |

## Cases

Every signed negative preserves a real valid signature. Source fixture expected_* annotations are discarded. The manual invariant failure table is checked against the separately implemented predictor before expectations are frozen. The frozen rows are not a third independent oracle.

| Case | Input variation | Definition-derived failing relation |
|---|---|---|
| JEX-RSI-001 | bound_signed_record | none; only bounded joins established |
| JEX-RSI-002 | terminal_hash_substitution | chain_join_failed |
| JEX-RSI-003 | action_ref_substitution | chain_join_failed |
| JEX-RSI-004 | other_signed_envelope | verdict_binding_failed |
| JEX-RSI-005 | actor_is_signer | admission_not_independent |
| JEX-RSI-006 | unlisted_signer | key_different_but_identity_unproven |
| JEX-RSI-007 | late_declared_anchor | late_commitment |
| JEX-RSI-008 | no_anchor | ordering_unanchored |
| JEX-RSI-009 | anchor_note_mirror | none; only bounded joins established |
| JEX-RSI-010 | declared_hash_substitution | envelope_hash_mismatch |
| JEX-RSI-011 | existence_without_precedence | existence_only_anchor |
| JEX-RSI-012 | reported_execution_absent | none; only bounded joins established |

The mirror changes only accepted_anchor_point.note, a display note ignored by the pinned verifier. Case 11 omits a non-ASCII display note; this omission is explicit and touches no signed/protected byte. No silent Unicode or float normalization occurs. Signed content remains exact ASCII text, including the JSON decimal literal inside that opaque signed string; uint256 amount remains its exact decimal string. This transport is not full JCS, arbitrary Unicode or arbitrary JSON-number support.

## Independence

Actual: unmodified Python reference verifier and its vendored BIP340 implementation in a subprocess. Predictor: separately written Python hash/join predicates and elliptic-curve equation implementation. No shared semantic evaluator or signature helper; both use Python hashlib/json and the same source definitions/fixture origin. The relation schema, source availability checks and RSI codec/admission remain shared infrastructure. Author independence UNKNOWN; no procedural blindness or clean-room third leg claimed. Review score 9/15 MODERATE (3 code, 1 algorithm, 1 source, 2 third-leg source vectors, 2 selected mutation resistance); language independence NOT INDEPENDENT.

## Reproduction

```sh
python -m unittest tests.test_judgment -v
python tools/run_judgment.py --include-previous --output artifacts/judgment.json
python tools/prove_judgment_can_fail.py --output artifacts/judgment-mutations.json
```

The new lane itself uses only Python stdlib and pinned tracked files. The full prior-domain suite also requires the repository existing Python requirements and Node 22.15.0. Evaluation uses no network or user-home source paths.

## Bounded claim

RSI validates binding between a signed judgment, the supplied canonical proposal envelope and the supplied terminal record under the pinned ERC-8299 reference application. A valid signature does not transfer to a different envelope/action reference, establish approval, prove anchor authority or prove that an action occurred.

Local conformance PASS means the admitted observation matches the source behavior; it does not convert source assumptions or a source reject verdict into security approval.
