"""Independent predicate obligations from the two pinned Rule/Scope sections.

No reference evaluator, relation evaluator, adapter or expectation row is read
by predict(). The absence/no-op status additionally follows the pinned reference
behavior; it is not an inference that no change means acceptance.
"""
import hashlib
import json
from pathlib import Path
from rsi.codec import load
from runner.expectation_registry import ExpectationProfile, FixtureSource
from runner.relation_runtime import validate_envelope, plan
from profiles.rvr.source import verify_source

EXPECTATION_ID = "rvr.digest-binding.v0"


def commitment(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf8")).hexdigest()


def derive(inputs, relation_id):
    task = inputs["transition"]
    prior, new = (commitment(task[k]) for k in ("in_force_profile", "proposed_profile"))
    amendment = task.get("amendment")
    digest = None
    failures = []
    if amendment is None:
        failures.append("no amendment")
    else:
        declared = {"schema": "profile-amendment.v0", **{k: amendment[k] for k in ("prior_profile_commitment", "new_profile_commitment", "escrow_ref")}}
        digest = commitment(declared)
        obligations = {"prior_profile_commitment": prior, "new_profile_commitment": new, "escrow_ref": task["escrow_ref"]}
        failures.extend(k for k, wanted in obligations.items() if amendment[k] != wanted)
        for party in ("buyer", "supplier"):
            record = task.get("authorizations", {}).get(party, {})
            if record.get("signed_digest") != digest:
                failures.append(party)
    permitted = not failures
    effective = new if permitted else prior
    transition = {"prior_profile_commitment": prior, "new_profile_commitment": new, "amendment_cc": digest,
                  "transition_status": "permitted" if permitted else "unresolved", "effective_profile_commitment": effective}
    verdict = None
    binding = True
    if inputs.get("verdict") is not None:
        supplied = inputs["verdict"]
        core = supplied["verdict_core"]
        core_digest = commitment(core)
        obligations = (core.get("effective_profile_commitment") == effective,
                       (supplied.get("resolver_sig") or {}).get("signed_digest") == core_digest)
        binding = all(obligations)
        verdict = {"verdict_core_cc": core_digest, "resolution_status": "bound" if binding else "unresolved",
                   "bound_profile_commitment": effective if binding else None}
    requested = inputs.get("claim", "digest_binding")
    return {"relation_id": relation_id, "relation_state": "digest_binding_observed", "outputs": {
        "transition": transition, "verdict_binding": verdict, "substantive_resolution": "not_evaluated",
        "crypto_authentication": {"status": "UNSUPPORTED", "reason": "no_pinned_signature_verification_lane"},
        "requested_claim": requested, "claim_admissible": requested == "digest_binding" and permitted and binding,
    }}


def predict(fixture):
    return {fixture["id"] + "/" + case["case_id"]: {"local_validity": True,
            "observation": derive(case["inputs"], fixture["relation_id"])} for case in fixture["cases"]}


def validate_prediction(value):
    if type(value) is not dict or not value:
        raise ValueError("prediction mapping required")
    for entry in value.values():
        if type(entry) is not dict or set(entry) != {"local_validity", "observation"} or entry["local_validity"] is not True:
            raise ValueError("locally valid structured observation required")


def make_profile(root):
    meta = load(Path(root) / "profiles/rvr/expectation-profile.v0.json")
    if meta["profile_id"] != EXPECTATION_ID or meta["version"] != "0":
        raise ValueError("expectation registration identity")
    return ExpectationProfile(EXPECTATION_ID, "0", tuple(FixtureSource(**r) for r in meta["fixture_scope"]), predict,
        meta["expectations_path"], meta["expectations_digest"], validate_envelope, validate_prediction,
        lambda fixture: plan(fixture, "binding"), lambda root: verify_source(root))
