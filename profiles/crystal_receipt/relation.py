"""Bounded accepted semantic-snapshot equivalence, not artifact authorization."""
from runner.relation_profile import Relation,RelationProfile
from profiles.crystal_receipt.source import SOURCE_PIN_SHA256,verify_source
PROFILE_ID="crystal-receipt.semantic-snapshot.v0"
RELATION_ID="counterfactual_audit_boundary.semantic_snapshot_equivalence.v0"
VERSION="0"

def printable(value):
    return type(value) is str and all(32<=ord(c)<=126 for c in value)

def validate_inputs(value):
    for endpoint in ("baseline","candidate"):
        envelope=value[endpoint]
        if type(envelope) is not dict or set(envelope)!={"semantic_artifact","manifest"}:raise ValueError("explicit artifact/manifest separation required")
        artifact=envelope["semantic_artifact"]
        if type(artifact) is not dict or not artifact or any(not printable(k) or not printable(v) for k,v in artifact.items()):raise ValueError("profile covers flat printable ASCII string artifacts only")
        if "audit_timestamp" in artifact:raise ValueError("reserved audit metadata is not semantic input")
        manifest=envelope["manifest"]
        if type(manifest) is not dict or set(manifest)-{"audit_timestamp"} or any(not printable(v) for v in manifest.values()):raise ValueError("bounded external audit manifest required")

def observed(value):
    # Source helpers already accepted and captured both concrete snapshots.
    same = value["baseline"] == value["candidate"]  # CR-M1
    return {"relation_id":RELATION_ID,"relation_state":"semantic_snapshots_match" if same else "canonical_snapshots_differ",
            "outputs":{"baseline_outcome":value["baseline_outcome"],"candidate_outcome":value["candidate_outcome"],
                       "canonical_baseline":value["baseline"],"canonical_candidate":value["candidate"],"semantic_identity_preserved":same}}

def validate_outputs(value):
    outputs=value["outputs"]
    if set(outputs)!={"baseline_outcome","candidate_outcome","canonical_baseline","canonical_candidate","semantic_identity_preserved"}:raise ValueError("invalid observation slots")
    if any(outputs[k]!="accepted_snapshot" for k in ("baseline_outcome","candidate_outcome")):raise ValueError("profile requires accepted snapshots")
    if any(type(outputs[k]) is not str or not outputs[k].isascii() for k in ("canonical_baseline","canonical_candidate")):raise ValueError("invalid canonical snapshot")
    if type(outputs["semantic_identity_preserved"]) is not bool or value["relation_state"] not in ("semantic_snapshots_match","canonical_snapshots_differ"):raise ValueError("invalid relation state")

def make_profile(root):
    def validate(value):verify_source(root);validate_inputs(value)
    def interpret(value,context):
        # Runtime import is a fixed trusted module, never fixture-selected.
        from adapters.crystal_receipt.model import capture
        return observed(capture(root,value))
    return RelationProfile(PROFILE_ID,VERSION,(Relation(RELATION_ID,("baseline","candidate"),(),validate,interpret,validate_outputs),),SOURCE_PIN_SHA256)
