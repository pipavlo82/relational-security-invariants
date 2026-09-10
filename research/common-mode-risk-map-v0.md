# H1 common-mode risk map

Plausible interpretation blind spots, not demonstrated invalidity. Frozen expected rows and hard-coded assertions catch many later simultaneous edits. They cannot establish their own independent semantic origin.

| Domain | Risk | Third leg | Hardening |
|---|---|---|---|
| Crystal Receipt | Same chosen semantic-object projection and external metadata exclusion; a shared scope mistake outside frozen examples is invisible | PARTIAL: Frozen SPEC, V-SEM-MANIFEST-INVARIANT, mutation vector, direct canonical-string assertions | Independently derive canonical-byte vectors from SPEC; review projection separately |
| RVR digest-binding | Same layer/status interpretation; both could originally mistake retained A for resolution or signed_digest equality for authentication | PARTIAL: 14 source vectors and explicit unsupported/layer assertions; shared upstream provenance | Third-party obligation table and definition-derived commitment bytes |
| TSEI serializer/adoption | Shared exact snapshot whitelist; predictor mechanism_active=True relies on admissible scope. Same misread adoption/introduction boundary can evade pair comparison | PARTIAL: 48 serializer vectors, fixed digests and Git/record evidence; chronology interpretation still shared | Independent Git-parent/record chronology reconstruction and boundary truth table |
| PQ policy/as-of | Same supplied anchored/valid flags, history and cutoff interpretation; absent independent anchor or signature truth | PARTIAL: 21 source policy vectors and direct historical/unsupported assertions; common source lineage | Definition-derived cutoff equality/revocation/as-of boundary cases |
| TAS context/dispatch | Same accepted/current/member records and getTask projection; no independent context producer or actual SDK execution | PARTIAL: Pinned production source and direct dispatch/member assertions; no full external third leg | Independent manifest-to-call-envelope vectors and alternate membership input producer |
| ConsultEscrow | Same job/result/signature fixture and setup projection; missing release scenarios can escape both. Unbound amount/recipient signature scope must remain explicit | PARTIAL: Keccak KATs, fixed signatures, source contract; EVM is actual leg, not automatically a third full oracle | Externally generated EIP-191 recovery and job-state golden traces |
| verify-layer | Same supplied proof/header and trust projection; no canonical header verification. Shared absence/root-first interpretation needs broader trie corpus | PARTIAL: Real supplied proof, Keccak KATs and direct root/account/balance assertions; no independent authoritative header | External inclusion/non-inclusion/embedded-node vectors and separate trust-tier obligations |
| Legacy/synthetic | Generator imports oracle to create golden rows; shared codec/digest/crypto and finite-model conventions can agree on same original error | PARTIAL: Contract and direct scenario assertions; expected artifact is oracle-generated, not independent origin | Definition-derived finite truth table plus alternative codec/crypto vectors |

H1-E1: pair-only dual promotion agreed, real frozen admission rejected (7 UNSUPPORTED, PREDICTION_MISMATCH, zero adapter calls). No new mutation registration or taxonomy. Experiment result is also embedded in audit JSON.

## Every existing mutation

Domain/legacy mutations are relation-load-bearing and sensitive to one-sided drift; they are common-mode-blind to an original shared assumption. Admission mutations test a different protection. RP mutations are not evidence of domain oracle independence. None is intended setup-only; fresh execution classification is recorded separately. A killed mutation does not prove completeness.

| ID | Primary classification | Mapped check | Definition |
|---|---|---|---|
| CE-M1 | relation-load-bearing | test_wrong_job | tools/prove_consult_escrow_can_fail.py |
| CE-M5 | relation-load-bearing | test_wrong_attestor | tools/prove_consult_escrow_can_fail.py |
| CE-M6 | relation-load-bearing | test_no_execution_promotion | tools/prove_consult_escrow_can_fail.py |
| CE-M7 | relation-load-bearing | test_mirror | tools/prove_consult_escrow_can_fail.py |
| CE-M8 | relation-load-bearing | test_replay | tools/prove_consult_escrow_can_fail.py |
| CR-M1 | relation-load-bearing | test_negative | tools/prove_crystal_can_fail.py |
| CR-M2 | relation-load-bearing | test_mirror | tools/prove_crystal_can_fail.py |
| CR-M3 | relation-load-bearing | test_negative | tools/prove_crystal_can_fail.py |
| EXP-M3 | independence-sensitive | tests.test_expectations.ExpectationTests.test_modified_value_rejected | tools/prove_expectations_can_fail.py |
| EXP-M4 | independence-sensitive | tests.test_expectations.ExpectationTests.test_atomic_admission | tools/prove_expectations_can_fail.py |
| PQ-M1 | relation-load-bearing | test_old_key_after_cutoff | tools/prove_pq_can_fail.py |
| PQ-M2 | relation-load-bearing | test_historical_anchor | tools/prove_pq_can_fail.py |
| PQ-M3 | relation-load-bearing | test_signing_not_anchor | tools/prove_pq_can_fail.py |
| PQ-M4 | relation-load-bearing | test_stale_snapshot | tools/prove_pq_can_fail.py |
| PQ-M5 | relation-load-bearing | test_no_crypto_promotion | tools/prove_pq_can_fail.py |
| PQ-M6 | relation-load-bearing | test_metadata_not_authentication | tools/prove_pq_can_fail.py |
| PQ-M7 | relation-load-bearing | test_algorithm_label | tools/prove_pq_can_fail.py |
| RP-M1 | not relevant | test_unknown_profile | tools/prove_relations_can_fail.py |
| RP-M2 | not relevant | test_version | tools/prove_relations_can_fail.py |
| RP-M3 | not relevant | test_static_opacity | tools/prove_relations_can_fail.py |
| RP-M4 | not relevant | test_rich | tools/prove_relations_can_fail.py |
| RP-M5 | not relevant | test_mirror | tools/prove_relations_can_fail.py |
| RP-M6 | not relevant | test_historical | tools/prove_relations_can_fail.py |
| RP-M7 | not relevant | test_tamper | tools/prove_relations_can_fail.py |
| RVR-M1 | relation-load-bearing | test_unbound_substitution | tools/prove_rvr_can_fail.py |
| RVR-M2 | relation-load-bearing | test_no_amendment | tools/prove_rvr_can_fail.py |
| RVR-M3 | relation-load-bearing | test_wrong_verdict | tools/prove_rvr_can_fail.py |
| RVR-M4 | relation-load-bearing | test_layer_separation | tools/prove_rvr_can_fail.py |
| RVR-M5 | relation-load-bearing | test_no_crypto_promotion | tools/prove_rvr_can_fail.py |
| RVR-M6 | relation-load-bearing | test_pubkeys_not_authentication | tools/prove_rvr_can_fail.py |
| TAS-M1 | relation-load-bearing | test_target_substitution | tools/prove_tas_can_fail.py |
| TAS-M3 | relation-load-bearing | test_member_substitution | tools/prove_tas_can_fail.py |
| TAS-M4 | relation-load-bearing | test_no_accepted_context | tools/prove_tas_can_fail.py |
| TAS-M5 | relation-load-bearing | test_no_execution_promotion | tools/prove_tas_can_fail.py |
| TAS-M6 | relation-load-bearing | test_mirror | tools/prove_tas_can_fail.py |
| TSEI-M1 | relation-load-bearing | test_wrong_serializer | tools/prove_tsei_can_fail.py |
| TSEI-M2 | relation-load-bearing | test_mechanism_not_adoption | tools/prove_tsei_can_fail.py |
| TSEI-M3 | relation-load-bearing | test_adoption_not_record | tools/prove_tsei_can_fail.py |
| TSEI-M4 | relation-load-bearing | test_nonretroactivity | tools/prove_tsei_can_fail.py |
| TSEI-M5 | relation-load-bearing | test_no_authority_promotion | tools/prove_tsei_can_fail.py |
| TSEI-M6 | relation-load-bearing | test_reported_labels_not_authority | tools/prove_tsei_can_fail.py |
| VL-M1 | relation-load-bearing | test_wrong_root | tools/prove_verify_layer_can_fail.py |
| VL-M2 | relation-load-bearing | test_no_header_promotion | tools/prove_verify_layer_can_fail.py |
| VL-M5 | relation-load-bearing | test_wrong_account | tools/prove_verify_layer_can_fail.py |
| VL-M6 | relation-load-bearing | test_no_downstream_promotion | tools/prove_verify_layer_can_fail.py |
| VL-M7 | relation-load-bearing | test_mirror | tools/prove_verify_layer_can_fail.py |
| VL-M9 | relation-load-bearing | test_wrong_claim | tools/prove_verify_layer_can_fail.py |
| RSI-001/messaging | relation-load-bearing | ['RSI-001/mutation/messaging'] | extensions/legacy_mutations.py |
| RSI-003/messaging | relation-load-bearing | ['RSI-003/mutation/messaging'] | extensions/legacy_mutations.py |
| RSI-004/messaging | relation-load-bearing | ['RSI-004/mutation/messaging'] | extensions/legacy_mutations.py |
| RSI-006/messaging | relation-load-bearing | ['RSI-006/mutation/messaging'] | extensions/legacy_mutations.py |
| RSI-008/messaging | relation-load-bearing | ['RSI-008/mutation/messaging'] | extensions/legacy_mutations.py |
| RSI-009/messaging | relation-load-bearing | ['RSI-009/mutation/messaging'] | extensions/legacy_mutations.py |
| RSI-001/generic | relation-load-bearing | ['RSI-001/mutation/generic'] | extensions/legacy_mutations.py |
| RSI-003/generic | relation-load-bearing | ['RSI-003/mutation/generic'] | extensions/legacy_mutations.py |
| RSI-004/generic | relation-load-bearing | ['RSI-004/mutation/generic'] | extensions/legacy_mutations.py |
| RSI-006/generic | relation-load-bearing | ['RSI-006/mutation/generic'] | extensions/legacy_mutations.py |
| RSI-008/generic | relation-load-bearing | ['RSI-008/mutation/generic'] | extensions/legacy_mutations.py |
| RSI-009/generic | relation-load-bearing | ['RSI-009/mutation/generic'] | extensions/legacy_mutations.py |
| EXP-M1 | independence-sensitive | atomic admission | extensions/mutations.py |
| EXP-M2 | independence-sensitive | atomic admission | extensions/mutations.py |


## Concrete shared preprocessing in PQ vector tests

`tests/test_pq.py:test_source_vector_reproduction` calls the source `apply_revocations` once and supplies its output to both source `admit` and the Python predictor. It also sets `snapshot_key` from actual `resolved_pq_pubkey`; the compared predictor output is the policy object. This demonstrates neither independent revocation preprocessing nor independent snapshot selection. Fixed vector expected fields remain a partial third leg. This is a precise test-evidence limitation, not invalidation of the registered policy/as-of scope. Add a separately derived pre/post-revocation history before claiming that preprocessing independently validated.
