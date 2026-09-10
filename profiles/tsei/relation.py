"""One composed relation with independent serializer and chronology coordinates."""
import json
from jsonschema import Draft7Validator
from rsi.codec import domain
from runner.relation_profile import Relation, RelationProfile
from profiles.tsei.source import SOURCE_PIN_SHA256, read_sources, verify_snapshots

PROFILE_ID = "tsei.serializer-adoption.v0"
RELATION_ID = "serializer-adoption-boundary"
VERSION = "0"
REQUIRED = ("binding_subject", "serializer_id", "binding_record", "registry_commit", "producer_commit", "artifact_commit", "artifact", "claim")
OPTIONAL = ("reported_status", "reported_provenance", "source_class")


def validate_inputs(value):
    domain(value)
    if type(value) is not dict or not set(REQUIRED) <= value.keys() or set(value) - set(REQUIRED + OPTIONAL):
        raise ValueError("missing or undeclared input")
    for k in (*REQUIRED[:2], "registry_commit", "producer_commit", "artifact_commit", "claim", *OPTIONAL):
        if k in value and (type(value[k]) is not str or not value[k]):
            raise ValueError("nonempty string required")
    if type(value["binding_record"]) is not dict or type(value["artifact"]) is not dict:
        raise ValueError("record/artifact object required")
    if value["claim"] not in ("serializer_binding", "provenance_authority"):
        raise ValueError("unsupported claim shape")


def validate_outputs(result):
    out = result["outputs"]
    booleans = ("local_structure_valid", "serializer_binding", "mechanism_active", "producer_adopted", "record_introduced", "artifact_covered", "claim_admissible")
    strings = ("record_verdict", "artifact_serialized_sha256", "artifact_binding_state", "requested_claim")
    if set(out) != set(booleans + strings + ("authority_validation",)):
        raise ValueError("output shape")
    if any(type(out[k]) is not bool for k in booleans) or any(type(out[k]) is not str for k in strings):
        raise ValueError("output types")
    capability = out["authority_validation"]
    if type(capability) is not dict or set(capability) != {"status", "reason"} or any(type(v) is not str for v in capability.values()):
        raise ValueError("capability shape")
    # No truth checks here: independently admitted expectations own comparison.


def make_profile(root):
    def validate(value):
        _, blobs = read_sources(root)
        validate_inputs(value)
        Draft7Validator(json.loads(blobs["recompute-kit-binding-record.schema.json"])).validate(value["binding_record"])
        verify_snapshots(value)

    def interpret(value, context):
        from adapters.tsei.model import evaluate
        return evaluate(root, {"inputs": value})

    return RelationProfile(PROFILE_ID, VERSION, (Relation(RELATION_ID, REQUIRED, OPTIONAL, validate, interpret, validate_outputs),), SOURCE_PIN_SHA256)
