"""Conditional cutoff/as-of interpretation, with independent capability boundaries."""
from rsi.codec import domain
from runner.relation_profile import Relation, RelationProfile
from profiles.pq.source import SOURCE_PIN_SHA256, verify_source
PROFILE_ID = "pq.policy-asof.v0"
RELATION_ID = "policy-cutoff-asof"
VERSION = "0"
REQUIRED = ("bindings", "consumer_cutoff", "artifact", "current_asof", "snapshot_key", "claim", "reported_algorithm")


def obj(value, required, optional=()):
    if type(value) is not dict or not set(required) <= value.keys() or set(value) - set(required) - set(optional):
        raise ValueError("input object shape")


def validate_inputs(value):
    domain(value); obj(value, REQUIRED)
    if type(value["bindings"]) is not list or not value["bindings"]: raise ValueError("binding history required")
    times = []
    for b in value["bindings"]:
        obj(b, ("name", "secp256k1_pubkey", "pq_pubkey", "binding_anchor_time"), ("revoked_at",))
        for key in ("name", "secp256k1_pubkey", "pq_pubkey"):
            if type(b[key]) is not str or not b[key]: raise ValueError("binding identity")
        for key in ("binding_anchor_time", "revoked_at"):
            if key in b and (type(b[key]) is not int or b[key] < 0): raise ValueError("binding time")
        times.append(b["binding_anchor_time"])
    if len(set(times)) != len(times): raise ValueError("ambiguous simultaneous bindings outside this profile")
    a = value["artifact"]; obj(a, ("anchor_time", "anchored", "pq_companion"), ("created_at",))
    for key in ("anchor_time", "created_at"):
        if key in a and (type(a[key]) is not int or a[key] < 0): raise ValueError("artifact time")
    if type(a["anchored"]) is not bool: raise ValueError("supplied anchor evidence flag")
    c = a["pq_companion"]
    if c is not None:
        obj(c, ("present", "valid", "pq_pubkey"))
        if type(c["present"]) is not bool or type(c["valid"]) is not bool or type(c["pq_pubkey"]) is not str: raise ValueError("companion evidence shape")
    for key in ("consumer_cutoff", "current_asof"):
        if type(value[key]) is not int or value[key] < 0: raise ValueError("policy time")
    for key in ("snapshot_key", "reported_algorithm"):
        if type(value[key]) is not str or not value[key]: raise ValueError("selected identity")
    if value["claim"] not in ("policy_eligibility", "authenticated_transition"): raise ValueError("claim scope")


def validate_outputs(result):
    out = result["outputs"]
    obj(out, ("policy", "current_binding", "snapshot_matches", "history_matches_pin", "historical_eligibility", "anchor_validation", "authenticated_transition_validation", "transition_metadata", "algorithm_identity", "requested_claim", "claim_admissible"))
    for key in ("snapshot_matches", "history_matches_pin", "historical_eligibility", "claim_admissible"):
        if type(out[key]) is not bool: raise ValueError("output boolean")
    obj(out["policy"], ("resolved", "resolved_pq_pubkey", "resolution_reason", "decision", "rule"))
    obj(out["current_binding"], ("name", "pq_pubkey", "reason"))
    for value in (*out["policy"].values(), *out["current_binding"].values()):
        if value is not None and type(value) is not str: raise ValueError("output string")
    for key in ("anchor_validation", "authenticated_transition_validation"):
        obj(out[key], ("status", "reason"))
        if any(type(v) is not str for v in out[key].values()): raise ValueError("capability shape")
    obj(out["transition_metadata"], ("predecessor_present", "signature_fields_present"))
    if any(type(v) is not bool for v in out["transition_metadata"].values()): raise ValueError("metadata shape")
    obj(out["algorithm_identity"], ("artifact_algorithm", "reported_label", "label_matches_artifact", "algorithm_specific_verification"))
    if type(out["algorithm_identity"]["label_matches_artifact"]) is not bool: raise ValueError("algorithm shape")
    for key in ("artifact_algorithm", "reported_label", "algorithm_specific_verification"):
        if type(out["algorithm_identity"][key]) is not str: raise ValueError("algorithm string")
    if type(out["requested_claim"]) is not str: raise ValueError("claim string")


def make_profile(root):
    def validate(value):
        verify_source(root); validate_inputs(value)
    def interpret(value, context):
        from adapters.pq.model import evaluate
        return evaluate(root, {"inputs": value})
    return RelationProfile(PROFILE_ID, VERSION, (Relation(RELATION_ID, REQUIRED, (), validate, interpret, validate_outputs),), SOURCE_PIN_SHA256)
