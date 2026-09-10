"""Independent source policy obligations; no implementation-under-test calls.

Anchored/valid flags are supplied evidence, not signatures or chain reads verified
by this profile. Expected authority claims remain explicitly unsupported.
"""
import hashlib
import json
from pathlib import Path
from rsi.codec import load
from runner.expectation_registry import ExpectationProfile, FixtureSource
from runner.relation_runtime import validate_envelope, plan
from profiles.pq.source import verify_source
EXPECTATION_ID = "pq.policy-asof.v0"
HISTORY_SHA256 = "0b7aafcd913f9ca99ca0c922d779db2b8784e058c5de66b7d07abd6a5eb7cd4b"


def governing(history, time):
    candidates = sorted((b for b in history if b["binding_anchor_time"] <= time and ("revoked_at" not in b or time < b["revoked_at"])), key=lambda b: b["binding_anchor_time"], reverse=True)
    return candidates[0] if candidates else None


def derive(value, relation_id):
    artifact = value["artifact"]
    selected = governing(value["bindings"], artifact["anchor_time"])
    current = governing(value["bindings"], value["current_asof"])
    comp = artifact["pq_companion"] or {}
    before = artifact["anchored"] and artifact["anchor_time"] < value["consumer_cutoff"]
    companion_obligations = (selected is not None, comp.get("present", False), comp.get("valid", False), comp.get("pq_pubkey") == (selected["pq_pubkey"] if selected else None))
    if selected is None: decision, rule = "REJECT", "no_in_force_binding"
    elif before: decision, rule = "ADMIT", "anchored_before_cutoff"
    elif all(companion_obligations): decision, rule = "ADMIT", "valid_pq_companion"
    else: decision, rule = "REJECT", "post_cutoff_no_valid_companion"
    history_hash = hashlib.sha256((json.dumps(value["bindings"], sort_keys=True, separators=(",", ":")) + "\n").encode("ascii")).hexdigest()
    matches = value["snapshot_key"] == (selected["pq_pubkey"] if selected else None)
    pinned = history_hash == HISTORY_SHA256
    return {"relation_id": relation_id, "relation_state": "conditional_policy_observed", "outputs": {
        "policy": {"resolved": selected["name"] if selected else None, "resolved_pq_pubkey": selected["pq_pubkey"] if selected else None, "resolution_reason": "resolved_at_anchor_time" if selected else "no_in_force_binding", "decision": decision, "rule": rule},
        "current_binding": {"name": current["name"] if current else None, "pq_pubkey": current["pq_pubkey"] if current else None, "reason": "resolved_at_anchor_time" if current else "no_in_force_binding"},
        "snapshot_matches": matches, "history_matches_pin": pinned,
        "historical_eligibility": bool(before and decision == "ADMIT"),
        "anchor_validation": {"status": "UNSUPPORTED", "reason": "anchor_evidence_is_supplied_policy_input_not_recomputed_here"},
        "authenticated_transition_validation": {"status": "UNSUPPORTED", "reason": "offline_source_defers_signature_verification"},
        "transition_metadata": {"predecessor_present": True, "signature_fields_present": True},
        "algorithm_identity": {"artifact_algorithm": "SLH-DSA-SHA2-192s", "reported_label": value["reported_algorithm"], "label_matches_artifact": value["reported_algorithm"] == "SLH-DSA-SHA2-192s", "algorithm_specific_verification": "UNSUPPORTED"},
        "requested_claim": value["claim"], "claim_admissible": value["claim"] == "policy_eligibility" and decision == "ADMIT" and matches and pinned,
    }}


def predict(fixture):
    return {fixture["id"] + "/" + case["case_id"]: {"local_validity": True,
        "observation": derive(case["inputs"], fixture["relation_id"])} for case in fixture["cases"]}


def validate_prediction(value):
    if type(value) is not dict or not value:
        raise ValueError("prediction mapping required")
    for row in value.values():
        if type(row) is not dict or set(row) != {"local_validity", "observation"} or row["local_validity"] is not True:
            raise ValueError("locally valid observation required")


def make_profile(root):
    meta = load(Path(root) / "profiles/pq/expectation-profile.v0.json")
    if meta["profile_id"] != EXPECTATION_ID or meta["version"] != "0":
        raise ValueError("expectation identity")
    return ExpectationProfile(EXPECTATION_ID, "0", tuple(FixtureSource(**r) for r in meta["fixture_scope"]), predict,
        meta["expectations_path"], meta["expectations_digest"], validate_envelope, validate_prediction,
        lambda fixture: plan(fixture, "binding"), lambda directory: verify_source(directory))
