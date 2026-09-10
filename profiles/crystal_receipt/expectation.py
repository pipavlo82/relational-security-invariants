"""Independent SPEC derivation; does not import/call production helpers or adapter."""
import json
from pathlib import Path
from rsi.codec import load
from runner.expectation_registry import ExpectationProfile,FixtureSource
from runner.relation_runtime import validate_envelope,plan
from profiles.crystal_receipt.source import verify_source
EXPECTATION_ID="crystal-receipt.v0"

def predict(fixture):
    rows={}
    for case in fixture["cases"]:
        inputs=case["inputs"]
        left=inputs["baseline"]["semantic_artifact"]
        right=inputs["candidate"]["semantic_artifact"]
        # SPEC: own string keys ascending; accepted string values preserved;
        # external manifest is not part of semantic identity.
        canonical_left=json.dumps(left,sort_keys=True,separators=(",",":"),ensure_ascii=True)
        canonical_right=json.dumps(right,sort_keys=True,separators=(",",":"),ensure_ascii=True)
        equivalent=set(left)==set(right) and all(left[key]==right[key] for key in left)
        observation={"relation_id":fixture["relation_id"],"relation_state":"semantic_snapshots_match" if equivalent else "canonical_snapshots_differ",
          "outputs":{"baseline_outcome":"accepted_snapshot","candidate_outcome":"accepted_snapshot","canonical_baseline":canonical_left,"canonical_candidate":canonical_right,"semantic_identity_preserved":equivalent}}
        rows[fixture["id"]+"/"+case["case_id"]]={"local_validity":True,"observation":observation}
    return rows

def validate_prediction(value):
    if type(value) is not dict or not value:raise ValueError("prediction mapping required")
    for entry in value.values():
        if type(entry) is not dict or set(entry)!={"local_validity","observation"} or entry["local_validity"] is not True:raise ValueError("accepted local components required")
        if type(entry["observation"]) is not dict:raise ValueError("structured observation required")

def make_profile(root):
    meta=load(Path(root)/"profiles/crystal_receipt/expectation-profile.v0.json")
    if meta["profile_id"]!=EXPECTATION_ID or meta["version"]!="0":raise ValueError("expectation registration identity")
    return ExpectationProfile(EXPECTATION_ID,"0",tuple(FixtureSource(**r) for r in meta["fixture_scope"]),predict,
        meta["expectations_path"],meta["expectations_digest"],validate_envelope,validate_prediction,
        lambda fixture:plan(fixture,"snapshot"),lambda root:verify_source(root))
