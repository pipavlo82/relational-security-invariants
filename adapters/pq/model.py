"""Execute the pinned offline enforcer; never verify signatures by metadata."""
from copy import deepcopy
import json
from profiles.pq.source import read_sources
from profiles.pq.relation import RELATION_ID, validate_inputs
ADAPTER_ID = "pq.policy-asof.v0"


def functions(root):
    _, blobs = read_sources(root)
    scope = {"__name__": "rsi_pinned_policy"}
    exec(compile(blobs["evidence/pq/cutoff_enforce.py"], "pinned_cutoff_enforce.py", "exec"), scope)
    deep = {"__name__": "rsi_pinned_deep_hash"}
    exec(compile(blobs["evidence/pq/deep_recompute.py"], "pinned_deep_recompute.py", "exec"), deep)
    rotation = json.loads(blobs["evidence/pq/pq-key-binding-v0.rotation.json"])
    checks, deferred = deep["check_rotation"](rotation)
    if not all(ok for _, ok in checks) or len(deferred) != 2: raise RuntimeError("rotation hash/deferred-lane source mismatch")
    history = json.loads(blobs["evidence/pq/pq-key-binding-v0.rotation-vectors.json"])["bindings"]
    return scope["admit"], scope["resolve_in_force"], rotation, history


def evaluate(root, request):
    inputs = deepcopy(request["inputs"]); validate_inputs(inputs)
    admit, resolve, rotation, history = functions(root)
    evaluation_artifact = deepcopy(inputs["artifact"])  # PQ-M2
    # created_at is intentionally ignored, as in the source enforcer.
    anchored_artifact = evaluation_artifact  # PQ-M3
    policy = admit(inputs["bindings"], inputs["consumer_cutoff"], anchored_artifact)  # PQ-M1
    current, why = resolve(inputs["bindings"], inputs["current_asof"])
    snapshot_matches = inputs["snapshot_key"] == policy["resolved_pq_pubkey"]  # PQ-M4
    history_matches = inputs["bindings"] == history
    historical = inputs["artifact"]["anchored"] and inputs["artifact"]["anchor_time"] < inputs["consumer_cutoff"] and policy["decision"] == "ADMIT"
    metadata = {"predecessor_present": bool(rotation["statement"].get("predecessor_content_address")),
                "signature_fields_present": bool(rotation.get("continuity_signature") and rotation.get("pq_companion_signature"))}
    crypto = {"status": "UNSUPPORTED", "reason": "offline_source_defers_signature_verification"}  # PQ-M5
    artifact_algorithm = rotation["statement"]["algorithm"]  # PQ-M7
    admissible = policy["decision"] == "ADMIT" and snapshot_matches and history_matches if inputs["claim"] == "policy_eligibility" else False  # PQ-M6
    return {"relation_id": RELATION_ID, "relation_state": "conditional_policy_observed", "outputs": {
        "policy": policy, "current_binding": {"name": current["name"] if current else None, "pq_pubkey": current["pq_pubkey"] if current else None, "reason": why},
        "snapshot_matches": snapshot_matches, "history_matches_pin": history_matches,
        "historical_eligibility": historical,
        "anchor_validation": {"status": "UNSUPPORTED", "reason": "anchor_evidence_is_supplied_policy_input_not_recomputed_here"},
        "authenticated_transition_validation": crypto, "transition_metadata": metadata,
        "algorithm_identity": {"artifact_algorithm": artifact_algorithm, "reported_label": inputs["reported_algorithm"], "label_matches_artifact": inputs["reported_algorithm"] == artifact_algorithm, "algorithm_specific_verification": "UNSUPPORTED"},
        "requested_claim": inputs["claim"], "claim_admissible": admissible,
    }}
