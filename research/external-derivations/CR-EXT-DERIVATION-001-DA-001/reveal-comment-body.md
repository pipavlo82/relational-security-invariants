@ogasurfproject-jpg Thanks, Toshikatsu - your acknowledgment is pinned.

The local coordinator comparison agrees with your frozen submission on all four cases, including the complete canonical snapshots. The historical RSI adapter, predictor and H2 replay agree as well. This is a coordinator result; a separate external POST_COMMIT_VERIFIER comparison is still pending.

Below is the post-freeze disclosure for this four-case exercise only. Please preserve your original derivation and freeze tags. Any follow-up belongs in a separate comment or commit.

Frozen submission: 1fa7700ecac0690edf6116dabb4938bc3712f7c9
DERIVATION.json SHA-256: c05b65cbca87433bceb1cd0d3a50600cbb71bbbbb673d576715700100d508ec1
Acknowledgment: b942ab118b4705a226e517b280a44e50b26c71cc
Historical RSI v0: 8d8e31291ecf96284212a353efb66f606cff2953
Source-only pack remains unchanged: c3f293d8b76d9b1646fbdbed6eddbece52c0a269

This disclosure ends the pre-reveal stage for you. It does not change the v0 claim or establish strict unaffiliated/framework-wide independence.

For exact byte checks, the disclosed text files use UTF-8 and one final LF. The input-origin record must hash to the commitment already present in your pack.

<details>
<summary>input-origin-record.json - SHA-256 b130cd433276cdcee8cce6ecf2820d85acad1943e05bf316a31751429531546e</summary>

```json
{
  "cases": [
    {
      "case_id": "case-001",
      "h2_vector": "CR-H2-G4",
      "left_artifact": "V-SEM-MANIFEST-INVARIANT.json#/semantic_artifact",
      "left_manifest": "V-SEM-MANIFEST-INVARIANT.json#/manifest_variants/0",
      "right_artifact": "V-SEM-MANIFEST-INVARIANT.json#/semantic_artifact",
      "right_manifest": "V-SEM-MANIFEST-INVARIANT.json#/manifest_variants/2",
      "rsi_case": "audit_timestamp_removed",
      "rsi_fixture": "CR-RSI-002"
    },
    {
      "case_id": "case-002",
      "h2_vector": "CR-H2-G2",
      "left_artifact": "V-SEM-MUTATION-DIFFERS.json#/baseline_semantic_artifact",
      "left_manifest": "V-SEM-MANIFEST-INVARIANT.json#/manifest_variants/2",
      "right_artifact": "V-SEM-MUTATION-DIFFERS.json#/mutated_semantic_artifact",
      "right_manifest": "V-SEM-MANIFEST-INVARIANT.json#/manifest_variants/2",
      "rsi_case": "relation_substitution",
      "rsi_fixture": "CR-RSI-001"
    },
    {
      "case_id": "case-003",
      "h2_vector": "CR-H2-G1",
      "left_artifact": "V-SEM-MUTATION-DIFFERS.json#/baseline_semantic_artifact",
      "left_manifest": "V-SEM-MANIFEST-INVARIANT.json#/manifest_variants/2",
      "right_artifact": "V-SEM-MUTATION-DIFFERS.json#/baseline_semantic_artifact",
      "right_manifest": "V-SEM-MANIFEST-INVARIANT.json#/manifest_variants/2",
      "rsi_case": "control",
      "rsi_fixture": "CR-RSI-001"
    },
    {
      "case_id": "case-004",
      "h2_vector": "CR-H2-G3",
      "left_artifact": "V-SEM-MANIFEST-INVARIANT.json#/semantic_artifact",
      "left_manifest": "V-SEM-MANIFEST-INVARIANT.json#/manifest_variants/0",
      "right_artifact": "V-SEM-MANIFEST-INVARIANT.json#/semantic_artifact",
      "right_manifest": "V-SEM-MANIFEST-INVARIANT.json#/manifest_variants/1",
      "rsi_case": "audit_timestamp_changed",
      "rsi_fixture": "CR-RSI-002"
    }
  ],
  "schema": "crystal-input-selection.v1",
  "source_commit": "45b46bf7df3a60b32583291f577a36bf19d22f00",
  "source_files": [
    {
      "git_blob": "3dfde347ab90321930566f4a6594fa177b0d7654",
      "kind": "frozen_vector",
      "local_path": "evidence/crystal-receipt/V-SEM-MUTATION-DIFFERS.json",
      "path": "conformance/counterfactual-audit-boundary-v0/vectors/V-SEM-MUTATION-DIFFERS.json",
      "sha256": "c92915e29cda954db6c0aaa44bbcb958c741e51a86fd7bca7bd9f767434c433d"
    },
    {
      "git_blob": "501e3cf3971e2fe0aae0a789c84b7907c50a85b1",
      "kind": "frozen_vector",
      "local_path": "evidence/crystal-receipt/V-SEM-MANIFEST-INVARIANT.json",
      "path": "conformance/counterfactual-audit-boundary-v0/vectors/V-SEM-MANIFEST-INVARIANT.json",
      "sha256": "9330a797b15b74d8c3372b866e9bc9f9e842e142de9a6f6b47581bbf92004749"
    }
  ],
  "source_repo": "pipavlo82/crystal-receipt"
}
```

</details>

<details>
<summary>expectations.v0.json - SHA-256 268b0e5dd6087cc60bf9c99ca5c20c0b135983d595ff632659c81b18634a4ba3</summary>

```json
{"expectations":[{"fixture_id":"CR-RSI-001","prediction":{"CR-RSI-001/control":{"local_validity":true,"observation":{"outputs":{"baseline_outcome":"accepted_snapshot","candidate_outcome":"accepted_snapshot","canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"relation_id":"counterfactual_audit_boundary.semantic_snapshot_equivalence.v0","relation_state":"semantic_snapshots_match"}},"CR-RSI-001/relation_substitution":{"local_validity":true,"observation":{"outputs":{"baseline_outcome":"accepted_snapshot","candidate_outcome":"accepted_snapshot","canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"incorrectly promote observation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":false},"relation_id":"counterfactual_audit_boundary.semantic_snapshot_equivalence.v0","relation_state":"canonical_snapshots_differ"}}}},{"fixture_id":"CR-RSI-002","prediction":{"CR-RSI-002/audit_timestamp_changed":{"local_validity":true,"observation":{"outputs":{"baseline_outcome":"accepted_snapshot","candidate_outcome":"accepted_snapshot","canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"relation_id":"counterfactual_audit_boundary.semantic_snapshot_equivalence.v0","relation_state":"semantic_snapshots_match"}},"CR-RSI-002/audit_timestamp_removed":{"local_validity":true,"observation":{"outputs":{"baseline_outcome":"accepted_snapshot","candidate_outcome":"accepted_snapshot","canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"relation_id":"counterfactual_audit_boundary.semantic_snapshot_equivalence.v0","relation_state":"semantic_snapshots_match"}}}}],"fixture_set_digest":"e44ae7b06472331cb5d68d2e16abfaee10400f51fb3dca4ac7fba6f5b0ab18d8","profile_id":"crystal-receipt.v0","profile_version":"0","schema":"rsi-expectations.v0"}
```

</details>

<details>
<summary>h2-replay.json - SHA-256 6941f4f653342606baf787e881bb0f704c0fd741662452d4c86b0d4d048797ca</summary>

```json
{"experiments":[{"actual_double":{"canonical_baseline":"{\"_h2_external_manifest\":\"{\\\"audit_timestamp\\\":\\\"2026-07-27T12:00:00Z\\\"}\",\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"_h2_external_manifest\":\"{\\\"audit_timestamp\\\":\\\"2026-08-05T12:00:00Z\\\"}\",\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":false},"experiment":"H2-M1","pair_agrees":true,"predictor_double":{"canonical_baseline":"{\"_h2_external_manifest\":\"{\\\"audit_timestamp\\\":\\\"2026-07-27T12:00:00Z\\\"}\",\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"_h2_external_manifest\":\"{\\\"audit_timestamp\\\":\\\"2026-08-05T12:00:00Z\\\"}\",\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":false},"status":"COMMON_MODE_CAUGHT","third_leg_unchanged":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"vector":"CR-H2-G3"},{"actual_double":{"canonical_baseline":"{\"_h2_external_manifest\":\"{\\\"audit_timestamp\\\":\\\"2026-07-27T12:00:00Z\\\"}\",\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"_h2_external_manifest\":\"{}\",\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":false},"experiment":"H2-M1","pair_agrees":true,"predictor_double":{"canonical_baseline":"{\"_h2_external_manifest\":\"{\\\"audit_timestamp\\\":\\\"2026-07-27T12:00:00Z\\\"}\",\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"_h2_external_manifest\":\"{}\",\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":false},"status":"COMMON_MODE_CAUGHT","third_leg_unchanged":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"vector":"CR-H2-G4"},{"actual_double":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"experiment":"H2-M2","pair_agrees":true,"predictor_double":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"status":"COMMON_MODE_CAUGHT","third_leg_unchanged":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"incorrectly promote observation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":false},"vector":"CR-H2-G2"}],"global_mutation_taxonomy_changed":false,"matrix":[{"actual":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"admitted_row":"CR-RSI-001/control","all_equal":true,"definition_golden":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"frozen_expectation":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"input_sha256":"0f88c70b0c915c7e056d2421c04b3011be15de31a6a35d5d6669ec9dae7abb00","predictor":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"semantic_notes":"Identical retained pairs.","status":"THIRD_LEG_AGREES","third_leg":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"vector":"CR-H2-G1"},{"actual":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"incorrectly promote observation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":false},"admitted_row":"CR-RSI-001/relation_substitution","all_equal":true,"definition_golden":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"incorrectly promote observation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":false},"frozen_expectation":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"incorrectly promote observation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":false},"input_sha256":"3efc9a11e5402d29765773c7c0d171807bbd564705a6276215bf3ecead1252f4","predictor":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"incorrectly promote observation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":false},"semantic_notes":"One retained semantic value changes.","status":"THIRD_LEG_AGREES","third_leg":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"incorrectly promote observation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":false},"vector":"CR-H2-G2"},{"actual":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"admitted_row":"CR-RSI-002/audit_timestamp_changed","all_equal":true,"definition_golden":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"frozen_expectation":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"input_sha256":"722f0d82d914e731d5b4132ff68105f1c01155d1f2fbafa7dab4477818863fe4","predictor":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"semantic_notes":"Only external audit metadata changes.","status":"THIRD_LEG_AGREES","third_leg":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"vector":"CR-H2-G3"},{"actual":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"admitted_row":"CR-RSI-002/audit_timestamp_removed","all_equal":true,"definition_golden":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"frozen_expectation":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"input_sha256":"785ec77ed32aae1add1264f2e850ca794f2b35c0379b82015b1b4cec4ba09cef","predictor":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"semantic_notes":"Only external audit metadata is removed.","status":"THIRD_LEG_AGREES","third_leg":{"canonical_baseline":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","canonical_candidate":"{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}","semantic_identity_preserved":true},"vector":"CR-H2-G4"}],"schema":"crystal-cleanroom-comparison.v0","third_leg_computed_before_comparison":true}
```

</details>

<details>
<summary>coordinator-comparison.json - SHA-256 6a1ce37f0ce7bb173e069d4874212770c3f5eb76bf56870c89b33007a756b9f3</summary>

```json
{
  "agreement_count": 4,
  "comparison_actor": "Exposed RSI coordinator/Codex; not an external POST_COMMIT_VERIFIER.",
  "derivation_sha256": "c05b65cbca87433bceb1cd0d3a50600cbb71bbbbb673d576715700100d508ec1",
  "disagreement_count": 0,
  "external_harness_local_sha256": "f8722c66f0e54f44938824373795e5a255606d852145fd4e36e98c77430ec0eb",
  "external_harness_original_sha256": "6975ae8047202127b862cb08768dc6023a493b286b277d9eb3fe4bdbe73365b3",
  "external_reveal": "NOT_SENT",
  "external_verifier_comparison": "NOT_PERFORMED",
  "frozen_expectations_sha256": "268b0e5dd6087cc60bf9c99ca5c20c0b135983d595ff632659c81b18634a4ba3",
  "harness_adaptation": "Only /mnt/user-data/uploads input root literal replaced; original bytes retained.",
  "matrix": [
    {
      "actual": "PRESERVED",
      "agreement": true,
      "all_local_canonical_outputs_equal": true,
      "case_id": "case-001",
      "external_canonical_outputs_match": true,
      "external_derivation": "PRESERVED",
      "external_harness": "PRESERVED",
      "frozen_expectation": "PRESERVED",
      "frozen_relation_state": "semantic_snapshots_match",
      "h2_input_matches": true,
      "h2_vector": "CR-H2-G4",
      "input_origin_matches": true,
      "input_sha256": "085ec6afc0480276f640512141be82673f9467da85b5a65c67ccb6934251274d",
      "local_outputs": {
        "canonical_baseline": "{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}",
        "canonical_candidate": "{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}",
        "semantic_identity_preserved": true
      },
      "predictor": "PRESERVED",
      "rsi_row": "CR-RSI-002/audit_timestamp_removed",
      "third_leg": "PRESERVED"
    },
    {
      "actual": "VIOLATED",
      "agreement": true,
      "all_local_canonical_outputs_equal": true,
      "case_id": "case-002",
      "external_canonical_outputs_match": true,
      "external_derivation": "VIOLATED",
      "external_harness": "VIOLATED",
      "frozen_expectation": "VIOLATED",
      "frozen_relation_state": "canonical_snapshots_differ",
      "h2_input_matches": true,
      "h2_vector": "CR-H2-G2",
      "input_origin_matches": true,
      "input_sha256": "b7be51d3fb4db37e3ef4f3da5dab76066d1406eaadda0f760d43c5f5a7621df2",
      "local_outputs": {
        "canonical_baseline": "{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}",
        "canonical_candidate": "{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"incorrectly promote observation\",\"profile_id\":\"counterfactual-review-v0\"}",
        "semantic_identity_preserved": false
      },
      "predictor": "VIOLATED",
      "rsi_row": "CR-RSI-001/relation_substitution",
      "third_leg": "VIOLATED"
    },
    {
      "actual": "PRESERVED",
      "agreement": true,
      "all_local_canonical_outputs_equal": true,
      "case_id": "case-003",
      "external_canonical_outputs_match": true,
      "external_derivation": "PRESERVED",
      "external_harness": "PRESERVED",
      "frozen_expectation": "PRESERVED",
      "frozen_relation_state": "semantic_snapshots_match",
      "h2_input_matches": true,
      "h2_vector": "CR-H2-G1",
      "input_origin_matches": true,
      "input_sha256": "b01b23c5d1f95793751fb3c6b2561e499c771ab889d49ae709441180d315f5b8",
      "local_outputs": {
        "canonical_baseline": "{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}",
        "canonical_candidate": "{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}",
        "semantic_identity_preserved": true
      },
      "predictor": "PRESERVED",
      "rsi_row": "CR-RSI-001/control",
      "third_leg": "PRESERVED"
    },
    {
      "actual": "PRESERVED",
      "agreement": true,
      "all_local_canonical_outputs_equal": true,
      "case_id": "case-004",
      "external_canonical_outputs_match": true,
      "external_derivation": "PRESERVED",
      "external_harness": "PRESERVED",
      "frozen_expectation": "PRESERVED",
      "frozen_relation_state": "semantic_snapshots_match",
      "h2_input_matches": true,
      "h2_vector": "CR-H2-G3",
      "input_origin_matches": true,
      "input_sha256": "6405cf6e29159fca8da0c38fd737da172283c4488d59795ac53778c8b8541ebe",
      "local_outputs": {
        "canonical_baseline": "{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}",
        "canonical_candidate": "{\"challenge_id\":\"observed_not_validated\",\"expected_conformance_observation\":\"preserve semantic non-elevation\",\"profile_id\":\"counterfactual-review-v0\"}",
        "semantic_identity_preserved": true
      },
      "predictor": "PRESERVED",
      "rsi_row": "CR-RSI-002/audit_timestamp_changed",
      "third_leg": "PRESERVED"
    }
  ],
  "missing_cases": [],
  "node_version": "v22.15.0",
  "origin_record_sha256": "b130cd433276cdcee8cce6ecf2820d85acad1943e05bf316a31751429531546e",
  "pack_commit": "c3f293d8b76d9b1646fbdbed6eddbece52c0a269",
  "round_id": "CR-EXT-DERIVATION-001-DA-001",
  "rsi_v0_commit": "8d8e31291ecf96284212a353efb66f606cff2953",
  "schema": "rsi-post-v0-external-mechanical-comparison.v1",
  "status": "COORDINATOR_COMPARISON_COMPLETE",
  "strict_blind_derivation": "NOT_ESTABLISHED",
  "v0_author_independence": "UNKNOWN"
}
```

</details>

Source-vector provenance and selectors are in input-origin-record.json. The cited public source commit is 45b46bf7df3a60b32583291f577a36bf19d22f00. Frozen expectations detect drift from admitted semantics; they do not prove that the original expectations were independently derived.
