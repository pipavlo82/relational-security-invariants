from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import ast
import tempfile
import unittest
from rsi.codec import encode
from tests.relation_support import fixture, model, run
from runner.relation_runtime import validate_envelope, resolve_fixture
from runner.relation_profile_registry import RelationProfileRegistry, UnavailableRelation

ROOT=Path(__file__).resolve().parents[1]
class RelationTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name)
    def tearDown(self):self.tmp.cleanup()
    def execute(self,value=None,**kwargs):return run(self.root,value or fixture(),**kwargs)
    def test_valid(self):self.assertEqual(self.execute()["totals"],{"PASS":1,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":0})
    def test_unknown_profile(self):
        v=fixture();v["relation_profile_id"]="absent"
        actual=lambda request:{"relation_id":"pair","relation_state":"equivalent","outputs":{"claim":True}}
        result=self.execute(v,actual_override=actual)
        self.assertEqual(result["totals"]["UNSUPPORTED"],1)
        self.assertEqual(result["admissions"],{})
    def test_version(self):
        v=fixture();v["relation_profile_version"]="99"
        result=self.execute(v)
        self.assertEqual(result["totals"]["UNSUPPORTED"],1)
        self.assertEqual(result["admissions"],{})
    def test_no_latest(self):
        v=fixture();del v["relation_profile_version"]
        with self.assertRaises(Exception):validate_envelope(v)
    def test_unknown_relation(self):
        v=fixture();v["relation_id"]="unknown"
        with self.assertRaises(UnavailableRelation):resolve_fixture(v,RelationProfileRegistry([model()]))
    def test_duplicate(self):
        with self.assertRaises(ValueError):RelationProfileRegistry([model(),model()])
    def test_order(self):
        a,b=model(),model("other","1")
        self.assertEqual(RelationProfileRegistry([a,b]).identities(),RelationProfileRegistry([b,a]).identities())
    def test_version_identity(self):self.assertEqual(len(RelationProfileRegistry([model(),model(version="1")]).identities()),2)
    def test_descriptor(self):
        with self.assertRaises(UnavailableRelation):RelationProfileRegistry([model()]).resolve("test.profile","0","pair","a"*64)
    def test_missing_slot(self):
        with self.assertRaises(ValueError):model().validate("pair",{"left":"a"})
    def test_extra_slot(self):
        with self.assertRaises(ValueError):model().validate("pair",{"left":"a","right":"a","unexpected":"a"})
    def test_malformed_slot(self):
        with self.assertRaises(ValueError):model().validate("pair",{"left":[],"right":"a"})
    def test_duplicate_case(self):
        v=fixture();v["cases"]*=2
        with self.assertRaises(ValueError):validate_envelope(v)
    def test_no_universal_slots(self):
        v=fixture();validate_envelope(v)
        self.assertEqual(set(v["cases"][0]["inputs"]),{"left","right"})
        self.assertEqual(self.execute(v)["totals"]["PASS"],1)
    def test_mirror(self):
        v=fixture();v["cases"].append({"case_id":"two","inputs":{"left":"a","right":"a","metadata":"changed"}})
        result=self.execute(v)
        self.assertEqual(result["totals"]["PASS"],2)
        self.assertEqual(result["rows"][0]["result"]["observed"],result["rows"][1]["result"]["observed"])
    def test_substitution(self):
        result=self.execute(fixture(data={"left":"a","right":"b"}))
        self.assertEqual(result["totals"]["PASS"],1)
        self.assertFalse(result["rows"][0]["result"]["observed"]["outputs"]["claim"])
    def test_rich(self):
        result=self.execute(fixture("rich",{"binding":"A"}))
        self.assertEqual(result["totals"]["PASS"],1)
        observed=result["rows"][0]["result"]["observed"]
        self.assertEqual(observed["relation_state"],"pending")
        self.assertEqual(observed["outputs"],{"effective":"A","resolution":"unresolved","claim":False})
    def test_historical(self):
        result=self.execute(fixture("historical",{"current":"B","anchor":"A","artifact":"A","anchor_proven":True}))
        self.assertEqual(result["totals"]["PASS"],1)
        self.assertTrue(result["rows"][0]["result"]["observed"]["outputs"]["claim"])
    def test_unproven_anchor(self):
        r=self.execute(fixture("historical",{"current":"B","anchor":"A","artifact":"A","anchor_proven":False}))
        self.assertFalse(r["rows"][0]["result"]["observed"]["outputs"]["claim"])
    def test_tamper(self):self.assertEqual(self.execute(tamper=True)["totals"]["UNSUPPORTED"],1)
    def test_unknown_adapter(self):self.assertEqual(self.execute(adapter=False)["totals"]["UNSUPPORTED"],1)
    def test_unknown_expectation(self):self.assertEqual(self.execute(expectation=False)["totals"]["UNSUPPORTED"],1)
    def test_deterministic(self):self.assertEqual(encode(self.execute()),encode(self.execute()))
    def test_opaque_fixture_id(self):
        v=fixture();v["id"]="reject-nothing"
        self.assertEqual(self.execute(v)["totals"]["PASS"],1)
    def test_static_opacity(self):
        for name in ("relation_runtime.py","relation_profile.py","relation_profile_registry.py"):
            source=(ROOT/"runner"/name).read_text();tree=ast.parse(source)
            self.assertFalse(any(isinstance(n,ast.Attribute) and n.attr in ("startswith","endswith") for n in ast.walk(tree)))
            for term in ("crystal","receiptos","rvr","8309","tsei","mldsa","interpoll"):
                self.assertNotIn(term,source.lower())

    def test_profile_id_opaque(self):
        v=fixture();v["relation_profile_id"]="accept-unresolved"
        r=self.execute(v,relations=RelationProfileRegistry([model("accept-unresolved")]))
        self.assertEqual(r["totals"]["PASS"],1)
    def test_relation_id_opaque(self):
        v=fixture();v["relation_id"]="reject-prefix"
        original=model();profile=replace(original,relations=(replace(original.relations[0],relation_id="reject-prefix"),))
        self.assertEqual(self.execute(v,relations=RelationProfileRegistry([profile]))["totals"]["PASS"],1)
    def test_case_id_opaque(self):
        v=fixture();v["cases"][0]["case_id"]="reject"
        self.assertEqual(self.execute(v)["totals"]["PASS"],1)
    def test_invalid_inputs_pipeline(self):
        result=self.execute(fixture_edit=lambda v:v["cases"][0]["inputs"].pop("right"))
        self.assertEqual(result["totals"]["INVALID_FIXTURE"],1)
        self.assertEqual(result["admissions"],{})
    def test_schema_invalid_pipeline(self):
        result=self.execute(fixture_edit=lambda v:v.pop("relation_profile_version"))
        self.assertEqual(result["totals"]["INVALID_FIXTURE"],1)
    def test_atomic_cases(self):
        v=fixture();v["cases"].append({"case_id":"two","inputs":{"left":"b","right":"b"}})
        result=self.execute(v,tamper=True)
        self.assertEqual(result["totals"]["PASS"],0)
        self.assertEqual(result["admissions"],{})
    def test_adapter_mismatch_is_fail(self):
        actual=lambda request:{"relation_id":"pair","relation_state":"different","outputs":{"claim":False}}
        result=self.execute(actual_override=actual)
        self.assertEqual(result["totals"],{"PASS":0,"FAIL":1,"INVALID_FIXTURE":0,"UNSUPPORTED":0})
    def test_plan_cannot_change_inputs(self):
        from runner.relation_runtime import plan
        def change(ep):
            def altered(value):
                tasks=plan(value,"slot");tasks[0]["request"]["inputs"]["right"]="other";return tasks
            return replace(ep,plan=altered)
        self.assertEqual(self.execute(ep_change=change)["totals"]["UNSUPPORTED"],1)
    def test_mutating_validator_rejected(self):
        original=model();relation=replace(original.relations[0],validate_inputs=lambda v:v.update(left="other"))
        profile=replace(original,relations=(relation,))
        with self.assertRaises(ValueError):profile.validate("pair",{"left":"a","right":"a"})
    def test_mutating_evaluator_rejected(self):
        original=model();relation=replace(original.relations[0],evaluate=lambda v,c:v.update(left="other"))
        profile=replace(original,relations=(relation,))
        with self.assertRaises(ValueError):profile.evaluate_relation("pair",{"left":"a","right":"a"})
    def test_slots_overlap_rejected(self):
        p=model();r=replace(p.relations[0],optional_slots=("left",))
        with self.assertRaises(ValueError):RelationProfileRegistry([replace(p,relations=(r,))])
    def test_result_identity_rejected(self):
        with self.assertRaises(ValueError):model().validate_result("pair",{"relation_id":"other","relation_state":"pending","outputs":{"claim":False}})
    def test_boolean_state_rejected(self):
        with self.assertRaises(ValueError):model().validate_result("pair",{"relation_id":"pair","relation_state":True,"outputs":{"claim":False}})
    def test_legacy_pipeline_exact(self):
        from extensions.defaults import composition
        from runner.extension_runtime import execute as old
        from extensions.relations import composition as composed
        from runner.relation_runtime import execute as new
        self.assertEqual(old(ROOT,*composition(ROOT)),new(ROOT,*composed(ROOT)))
    def test_mutation_registration(self):
        from tools.prove_relations_can_fail import registry
        self.assertEqual(registry().identities(),tuple("RP-M"+str(i) for i in range(1,8)))

    def test_alias_namespaces_independent_profiles(self):
        from rsi.codec import load,raw_digest
        from runner.fixture_registry import Corpus,FixtureRegistry
        from runner.expectation_registry import ExpectationRegistry
        from runner.adapter_registry import AdapterRegistry
        from runner.relation_runtime import execute
        corpora=[];profiles=[];adapters=[]
        for name,right in (("first","a"),("second","b")):
            directory=self.root/name;directory.mkdir()
            fr,er,ar,rr=run(directory,fixture(data={"left":"a","right":right}),setup=True)
            manifest=load(directory/"corpus.json")
            manifest.update(corpus_id=name,namespace=name,fixture_directory=name+"/fixtures")
            row=manifest["fixtures"][0]
            row.update(fixture_id=name+":sample",path=name+"/fixtures/case.json",expectation_profile_id=name)
            row["adapter_bindings"]={"slot":name}
            (directory/"corpus.json").write_bytes(encode(manifest))
            corpora.append(Corpus(name,name+"/corpus.json",raw_digest(encode(manifest)),validate_envelope))
            ep=er.resolve("test.expected");artifact=load(directory/"expectations.json");artifact["profile_id"]=name
            (directory/"expectations.json").write_bytes(encode(artifact))
            profiles.append(replace(ep,profile_id=name,fixture_scope=tuple(replace(f,path=name+"/"+f.path) for f in ep.fixture_scope),expectations_path=name+"/expectations.json",expectations_digest=raw_digest(encode(artifact))))
            original=ar.resolve("test.actual","test.expected")
            adapters.append(replace(original,adapter_id=name,supported_profiles=(name,)))
        result=execute(self.root,FixtureRegistry(corpora),ExpectationRegistry(profiles),AdapterRegistry(adapters),rr)
        self.assertEqual(result["totals"]["PASS"],2)
        claims=[r["result"]["observed"]["outputs"]["claim"] for r in result["rows"]]
        self.assertEqual(claims,[True,False])
    def test_invalid_identifier_newline(self):
        v=fixture();v["cases"][0]["case_id"]="case\n"
        with self.assertRaises(ValueError):validate_envelope(v)
    def test_unknown_relation_pipeline(self):
        v=fixture();v["relation_id"]="not-registered"
        result=self.execute(v)
        self.assertEqual(result["totals"]["UNSUPPORTED"],1)
        self.assertEqual(result["admissions"],{})
    def test_profile_order_outcomes(self):
        a,b=model(),model("unused","1")
        self.assertEqual(self.execute(relations=RelationProfileRegistry([a,b])),self.execute(relations=RelationProfileRegistry([b,a])))
    def test_descriptor_exact_match(self):
        v=fixture();v["relation_profile_sha256"]="a"*64
        p=replace(model(),descriptor_sha256="a"*64)
        self.assertEqual(self.execute(v,relations=RelationProfileRegistry([p]))["totals"]["PASS"],1)
    def test_pin_mismatch_pipeline(self):
        v=fixture();v["relation_profile_sha256"]="b"*64
        self.assertEqual(self.execute(v)["totals"]["UNSUPPORTED"],1)
    def test_no_latest_with_available_versions(self):
        v=fixture();v["relation_profile_version"]="2"
        rr=RelationProfileRegistry([model(),model(version="1")])
        self.assertEqual(self.execute(v,relations=rr)["totals"]["UNSUPPORTED"],1)
    def test_output_validator_mutation(self):
        p=model();r=replace(p.relations[0],validate_outputs=lambda v:v.update(relation_state="changed"))
        with self.assertRaises(ValueError):replace(p,relations=(r,)).evaluate_relation("pair",{"left":"a","right":"a"},{"relation_id":"pair"})
    def test_result_is_detached(self):
        p=model();inputs={"left":"a","right":"a"}
        first=p.evaluate_relation("pair",inputs,{"relation_id":"pair"});first["outputs"]["claim"]=False
        self.assertTrue(p.evaluate_relation("pair",inputs,{"relation_id":"pair"})["outputs"]["claim"])
    def test_protected_legacy_hashes(self):
        import json,hashlib
        report=json.loads((ROOT/"research/relation-profile-implementation-v0.json").read_text())
        for path,pin in report["protected_legacy_sha256"].items():
            self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),pin,path)
