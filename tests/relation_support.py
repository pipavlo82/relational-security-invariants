"""Test-only relation models. No external semantics or artifacts."""
from pathlib import Path
from rsi.codec import encode, raw_digest
from runner.relation_profile import Relation, RelationProfile
from runner.relation_profile_registry import RelationProfileRegistry
from runner.relation_runtime import validate_envelope, plan, execute
from runner.fixture_registry import Corpus, FixtureRegistry
from runner.expectation_registry import ExpectationProfile, ExpectationRegistry, FixtureSource
from runner.expectation_contract import FixtureDocument, fixture_set_digest
from runner.adapter_registry import Adapter, AdapterRegistry

def inputs(value):
    if any(type(v) not in (str, bool) for v in value.values()):
        raise ValueError("test slots require strings or flags")

def pair_inputs(value):
    if any(type(v) is not str for v in value.values()):raise ValueError("string endpoints and metadata required")

def historical_inputs(value):
    if type(value["anchor_proven"]) is not bool or any(type(value[k]) is not str for k in ("current","anchor","artifact")):
        raise ValueError("typed anchor evidence required")

def outputs(value):
    if not value["outputs"] or type(value["outputs"].get("claim")) is not bool:
        raise ValueError("explicit test claim required")

def pair(value, context):
    same = value["left"] == value["right"]  # RP-M5
    return {"relation_id":context["relation_id"], "relation_state":"equivalent" if same else "different", "outputs":{"claim":same}}

def rich(value, context):
    return {"relation_id":context["relation_id"], "relation_state":"pending", "outputs":{"effective":value["binding"], "resolution":"unresolved", "claim":False}}

def historical(value, context):
    eligible = value["anchor_proven"] and value["artifact"] == value["anchor"]  # RP-M6
    return {"relation_id":context["relation_id"], "relation_state":"eligible" if eligible else "ineligible", "outputs":{"claim":eligible}}

def model(profile_id="test.profile", version="0"):
    return RelationProfile(profile_id, version, (
        Relation("pair", ("left","right"), ("metadata",), pair_inputs, pair, outputs),
        Relation("rich", ("binding",), (), pair_inputs, rich, outputs),
        Relation("historical", ("current","anchor","artifact","anchor_proven"), (), historical_inputs, historical, outputs)))

def predict(fixture):
    # Independent derivation: never call relation evaluator or adapter.
    rows={}
    for case in fixture["cases"]:
        v=case["inputs"]; relation=fixture["relation_id"]
        if "left" in v:
            claim=len({v["left"],v["right"]})==1
            state={True:"equivalent",False:"different"}[claim]; out={"claim":claim}
        elif "binding" in v:
            state="pending";out={"effective":v["binding"],"resolution":"unresolved","claim":False}
        else:
            claim=bool(v["anchor_proven"]) and len({v["artifact"],v["anchor"]})==1
            state={True:"eligible",False:"ineligible"}[claim];out={"claim":claim}
        rows[fixture["id"]+"/"+case["case_id"]]={"local_validity":True,"observation":{"relation_id":relation,"relation_state":state,"outputs":out}}
    return rows

def fixture(relation="pair", data=None):
    return {"schema":"profiled-relation-fixture.v0","id":"sample","relation_profile_id":"test.profile","relation_profile_version":"0","relation_id":relation,"cases":[{"case_id":"one","inputs":data or {"left":"a","right":"a"}}]}

def prediction_shape(value):
    if type(value) is not dict or not value: raise ValueError("prediction mapping required")
    for entry in value.values():
        if set(entry)!={"local_validity","observation"} or type(entry["local_validity"]) is not bool: raise ValueError("prediction shape")

def run(root, value, relations=None, tamper=False, adapter=True, expectation=True, fixture_edit=None, ep_change=None, actual_override=None, setup=False):
    root=Path(root);(root/"fixtures").mkdir(exist_ok=True)
    raw=encode(value);(root/"fixtures/case.json").write_bytes(raw)
    recorded=predict(value)
    if tamper: next(iter(recorded.values()))["observation"]["outputs"]["claim"]=False
    artifact={"schema":"rsi-expectations.v0","profile_id":"test.expected","profile_version":"0","fixture_set_digest":fixture_set_digest([FixtureDocument(value["id"],raw)]),"expectations":[{"fixture_id":value["id"],"prediction":recorded}]}
    (root/"expectations.json").write_bytes(encode(artifact))
    ep=ExpectationProfile("test.expected","0",(FixtureSource(value["id"],"fixtures/case.json"),),predict,"expectations.json",raw_digest(encode(artifact)),validate_envelope,prediction_shape,lambda f:plan(f,"slot"),lambda root:None)
    if ep_change: ep=ep_change(ep)
    manifest={"schema":"rsi-fixture-corpus.v0","corpus_id":"test","namespace":"test","fixture_directory":"fixtures","fixtures":[{"fixture_id":"test:"+value["id"],"fixture_source_id":value["id"],"path":"fixtures/case.json","expectation_profile_id":"test.expected","adapter_bindings":{"slot":"test.actual"}}]}
    (root/"corpus.json").write_bytes(encode(manifest))
    fr=FixtureRegistry([Corpus("test","corpus.json",raw_digest(encode(manifest)),validate_envelope)])
    registry=relations if relations is not None else RelationProfileRegistry([model()])
    def actual(request):
        p=registry.resolve(request["relation_profile_id"],request["relation_profile_version"],request["relation_id"])
        return p.evaluate_relation(request["relation_id"],request["inputs"],{"relation_id":request["relation_id"]})
    if fixture_edit:
        fixture_edit(value);(root/"fixtures/case.json").write_bytes(encode(value))
    ar=AdapterRegistry([Adapter("test.actual",("test.expected",),actual_override or actual)] if adapter else [])
    er=ExpectationRegistry([ep] if expectation else [])
    if setup:return fr,er,ar,registry
    return execute(root,fr,er,ar,registry)
