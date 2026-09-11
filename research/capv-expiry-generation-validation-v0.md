# Phase 3E validation: CAPV expiry / program generations

Local validation is complete. Phase closure additionally requires green CI for the exact pushed commit; this pre-commit report does not claim that future delivery gate has already passed.

Base: `7b1eed97a54e6f16b9c57368e0de824756f9979f`. No generic/core or prior-domain file changed.

| Gate | Verified result |
|---|---|
| Normal / optimized suites | 477 / 477 PASS (446 / 446 before) |
| Combined conformance | 99 PASS; all other statuses 0 |
| CAPV | 11 fixtures, 14 passing conformance cases |
| CAPV mutations | M1-M6 KILLED; other statuses 0 |
| All mutations | 67 KILLED, including 61 unchanged prior records |
| Prior conformance | 85; exact complete-report and ordered-row diffs 0 |
| Protected hashes | 422 unchanged |
| Source/build hashes | 30 external files, 41 execution-closure files verified |
| Determinism | repeat report and offline clean-copy report byte-identical |
| Rebuild | compiled bytecode and bundled runtime byte-identical |
| Anti-coupling | PASS; zero CAPV references in 17 protected generic files |
| Semantic exceptions | 0 |

## Observed matrix

TRUE/FALSE/REVERT retain the native verifier/adapter outcome distinction. Expiry-bound means this exact proof verifies with expiry in its executed projection, not overall Guard authorization.

| Case | Public inputs | Verifier | Adapter | Fresh | Expiry bound | Consumer generation matches |
|---|---:|---|---|---|---|---|
| CAPV-RSI-001/normative_obligation | 39 | TRUE | TRUE | True | False | True |
| CAPV-RSI-002/old_control | 39 | TRUE | TRUE | True | False | True |
| CAPV-RSI-003/old_expiry_substitution | 39 | TRUE | TRUE | True | False | True |
| CAPV-RSI-004/fresh_not_bound | 39 | TRUE | TRUE | True | False | True |
| CAPV-RSI-005/fixed_control | 40 | TRUE | TRUE | True | True | True |
| CAPV-RSI-006/fixed_expiry_substitution | 40 | REVERT | REVERT | True | False | True |
| CAPV-RSI-007/fixed_with_sdk_proof | 40 | REVERT | REVERT | True | False | True |
| CAPV-RSI-007/sdk_with_fixed_proof | 39 | REVERT | REVERT | True | False | True |
| CAPV-RSI-008/future_generation_not_historical | 40 | TRUE | TRUE | True | True | False |
| CAPV-RSI-008/historical_consumer | 39 | TRUE | TRUE | True | False | True |
| CAPV-RSI-009/canonical_asset_mismatch | 39 | TRUE | TRUE | True | False | True |
| CAPV-RSI-010/timestamp_mirror | 40 | TRUE | TRUE | True | True | True |
| CAPV-RSI-011/fixed_wrong_program_key | 40 | TRUE | FALSE | True | True | True |
| CAPV-RSI-011/sdk_wrong_program_key | 39 | TRUE | FALSE | True | False | True |

## Interpretation

Old and fixed controls use real public proof fixtures. Only expiry changes in each substitution pair. Old verification remains true; fixed verification reverts. The timestamp mirror changes only observation time, with both observations before the same bound expiry. Wrong programKey cases keep raw cryptographic validity while the adapter rejects. Cross-generation proof swaps both revert.

Conformance PASS on an explicitly observed missing binding is not certification of normative security compliance. Canonical ERC text requires expiry to be public; its pinned Noir asset omits it. The SDK discloses its historical limitation, and current upstream has fixed it. No general current-upstream vulnerability or exploit claim is made.

## Evidence and limitations

Exact pins, paths, hashes, evidence classes and per-case derivation are in [the source map](capv-expiry-generation-source-map-v0.json). The [mapping](capv-expiry-generation-mapping-v0.md) explains source ownership, projection ordering, independence and mutation decisions. [Offline reproduction](../evidence/capv/REPRODUCING.md) requires no proving service or local untracked dependencies.

The Python predictor is separately implemented and compares candidate field words against the pinned fixture definition. It is not an independent Honk verifier. Source bytes, codec and source-pin checks are shared; author independence remains UNKNOWN. No third leg is claimed. Large values use exact decimal/hex strings, while proof blobs remain pinned binary files.

Guard acceptance, root/domain acceptability, executor authorization, execution occurrence, live deployment configuration, proof generation and whole proof-system security remain UNSUPPORTED. Existing RVR/TSEI/PQ/TAS and other unsupported boundaries are unchanged.

## Recommended closure wording

RSI distinguishes CAPV on-chain expiry freshness from cryptographic expiry binding, and preserves program-generation identity across the pre-fix and expiry-bound ERC-8354 artifacts. Under the pinned pre-fix verifier, expiry substitution survives proof verification; under the pinned fixed verifier, the same protected substitution is rejected. The result is generation-specific and does not retroactively upgrade historical consumers.

This wording becomes the Phase 3E closure claim only after exact-HEAD CI passes. It is not ecosystem-wide ERC-8354 validation.
