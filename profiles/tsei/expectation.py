"""Independent obligations from the pinned registry contract and Git chronology.

Uses neither the producer/checker implementation nor observation functions.
The record digest below is an input identity, never a recorded expected outcome.
Only the ASCII/integer fixture subset is predicted; no general JS serializer claim.
"""
import hashlib
import json
from pathlib import Path
from rsi.codec import load
from runner.expectation_registry import ExpectationProfile, FixtureSource
from runner.relation_runtime import validate_envelope, plan
from profiles.tsei.source import verify_source

EXPECTATION_ID = "tsei.serializer-adoption.v0"
RECORD_IDENTITY = "2b89d1e62fd7146616c03a335e07cc956c1ae3a32a5595f1fca43cddaed073a5"


def serialization(value):
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode("ascii")


def derive(value, relation_id):
    # Independent membership obligations. No ordering of SHA strings or dates.
    producer_boundary = "45b46bf7df3a60b32583291f577a36bf19d22f00"
    landed_snapshots = {"1dfc527d8f9b3561d32ca510f8fefd8d290391f6", "15f7f59ac47b3358492bd5741143c418b5d657f5"}
    binding_obligations = (
        hashlib.sha256(serialization(value["binding_record"])).hexdigest() == RECORD_IDENTITY,
        value["binding_subject"] == "tsei.frozen-artifact",
        value["serializer_id"] == "encode-json-utf8-lf.v0",
    )
    record_available = value["registry_commit"] in landed_snapshots
    producer_conformant = value["producer_commit"] == producer_boundary
    historical = value["artifact_commit"] != producer_boundary
    coverage_obligations = (*binding_obligations, record_available, producer_conformant, not historical)
    covered = all(coverage_obligations)
    return {"relation_id": relation_id, "relation_state": "serializer_adoption_observed", "outputs": {
        "local_structure_valid": True, "record_verdict": "valid",
        "artifact_serialized_sha256": hashlib.sha256(serialization(value["artifact"])).hexdigest(),
        "serializer_binding": all(binding_obligations), "mechanism_active": True,
        "producer_adopted": producer_conformant, "record_introduced": record_available,
        "artifact_covered": covered,
        "artifact_binding_state": "historically_unversioned" if historical else ("bound" if covered else "binding_not_established"),
        "authority_validation": {"status": "UNSUPPORTED", "reason": "required authority recomputation operands unavailable in canonical public receipt package"},
        "requested_claim": value["claim"],
        "claim_admissible": value["claim"] == "serializer_binding" and all(coverage_obligations),
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
    meta = load(Path(root) / "profiles/tsei/expectation-profile.v0.json")
    if meta["profile_id"] != EXPECTATION_ID or meta["version"] != "0":
        raise ValueError("expectation identity")
    return ExpectationProfile(EXPECTATION_ID, "0", tuple(FixtureSource(**r) for r in meta["fixture_scope"]), predict,
        meta["expectations_path"], meta["expectations_digest"], validate_envelope, validate_prediction,
        lambda fixture: plan(fixture, "binding"), lambda directory: verify_source(directory))
