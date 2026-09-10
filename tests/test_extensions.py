"""Architecture-only registration tests; no external domain implementation."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import ast
import json
import shutil
import tempfile
import unittest
from rsi.codec import encode, load, raw_digest
from rsi.corpus import validator
from rsi.oracle import predict, local_validity
from rsi.run import evaluate
from runner.fixture_registry import Corpus, CorpusError, FixtureRegistry, identity
from runner.expectation_registry import ExpectationRegistry, FixtureSource
from runner.expectation_contract import FixtureDocument, fixture_set_digest
from runner.adapter_registry import Adapter, AdapterRegistry
from runner.extension_runtime import execute
from runner.mutation_registry import Mutation, MutationTrace, CheckEvent, MutationRegistry
from extensions.defaults import composition
from extensions.mutations import registry as mutations
from adapters.generic import model

ROOT=Path(__file__).resolve().parents[1]

class ExtensionTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix="rsi-extension-test-")
        self.root=Path(self.tmp.name)
        for name in ("fixtures","schema","oracle","profiles","extensions"):
            shutil.copytree(ROOT/name,self.root/name,ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy2(ROOT/"manifest.json",self.root/"manifest.json")
        self.corpora,self.profiles,self.adapters=composition(self.root)
    def tearDown(self):self.tmp.cleanup()
    def manifest(self, change):
        path=self.root/"extensions/core.corpus.v0.json"
        value=load(path);change(value);path.write_bytes(encode(value))
        validate=validator(self.root/"schema/registered-fixture.v0.schema.json").validate
        return FixtureRegistry([Corpus("core","extensions/core.corpus.v0.json",raw_digest(path.read_bytes()),validate)])
    def run_with(self,corpora=None,profiles=None,adapters=None):
        return execute(self.root,corpora or self.corpora,profiles or self.profiles,adapters or self.adapters)
    def test_documented_registration_schema(self):
        from jsonschema import Draft202012Validator
        schema=load(self.root/"schema/fixture-corpus.v0.schema.json")
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(load(self.root/"extensions/core.corpus.v0.json"))
    def test_arbitrary_identity(self):self.assertEqual(identity("future-lab:CASE_123.a"),"future-lab:CASE_123.a")
    def test_invalid_identities(self):
        for value in ("",":a","a:","A:a","a:a/b","a:a:b","a:a ","a:Р вЂњР’В©"):
            with self.subTest(value=value),self.assertRaises(CorpusError):identity(value)
    def test_duplicate_canonical_identity(self):
        corpora=self.manifest(lambda m:m["fixtures"].append(deepcopy(m["fixtures"][0])))
        result=self.run_with(corpora=corpora)
        self.assertEqual(result["totals"]["PASS"],0)
        self.assertIn("duplicate",result["discovery"]["errors"][0]["error"])
    def test_duplicate_corpus_registration(self):
        c=next(iter(self.corpora._corpora.values()))
        with self.assertRaises(CorpusError):FixtureRegistry([c,c])
    def test_registration_order_invariant(self):
        before=self.run_with()
        corpora=self.manifest(lambda m:m["fixtures"].reverse())
        after=self.run_with(corpora=corpora)
        self.assertEqual(before["rows"],after["rows"])
    def test_missing_declared_file(self):
        path=load(self.root/"extensions/core.corpus.v0.json")["fixtures"][0]["path"]
        (self.root/path).unlink()
        result=self.run_with()
        self.assertEqual(result["totals"],{"PASS":0,"FAIL":0,"INVALID_FIXTURE":1,"UNSUPPORTED":5})
    def test_malformed_fixture(self):
        path=load(self.root/"extensions/core.corpus.v0.json")["fixtures"][0]["path"]
        (self.root/path).write_bytes(b"{bad")
        self.assertEqual(self.run_with()["totals"]["INVALID_FIXTURE"],1)
    def test_schema_invalid_fixture_before_unknown_profile(self):
        path=load(self.root/"extensions/core.corpus.v0.json")["fixtures"][0]["path"]
        fixture=load(self.root/path);fixture["protected_relation"]="not-a-relation"
        (self.root/path).write_bytes(encode(fixture))
        self.assertEqual(self.run_with(profiles=ExpectationRegistry())["totals"]["INVALID_FIXTURE"],1)
    def test_unexpected_json_not_skipped(self):
        (self.root/"fixtures/extra.JSON").write_bytes(b"{}\n")
        result=self.run_with()
        self.assertEqual(result["totals"]["PASS"],0)
        self.assertIn("extra.JSON",result["discovery"]["errors"][0]["error"])
    def test_nested_unexpected_json_not_skipped(self):
        (self.root/"fixtures/nested").mkdir()
        (self.root/"fixtures/nested/extra.json").write_bytes(b"{}\n")
        self.assertTrue(self.run_with()["discovery"]["errors"])
    def test_empty_registry_fails_closed(self):
        self.assertEqual(self.run_with(corpora=FixtureRegistry())["totals"],{"PASS":0,"FAIL":0,"INVALID_FIXTURE":1,"UNSUPPORTED":0})
    def test_directory_links_not_silently_skipped(self):
        from unittest.mock import patch
        path=self.root/"fixtures/link";path.mkdir()
        original=Path.is_symlink
        with patch.object(Path,"is_symlink",lambda p:p==path or original(p)):
            result=self.run_with()
        self.assertTrue(any("filesystem link" in e["error"] for e in result["discovery"]["errors"]))
        self.assertEqual(result["totals"]["PASS"],0)
    def test_manifest_tampering(self):
        p=self.root/"extensions/core.corpus.v0.json";p.write_bytes(p.read_bytes()+b" ")
        self.assertIn("digest",self.run_with()["discovery"]["errors"][0]["error"])
    def test_manifest_cannot_name_import(self):
        corpora=self.manifest(lambda m:m.update(import_path="arbitrary.module"))
        self.assertTrue(self.run_with(corpora=corpora)["discovery"]["errors"])
    def test_path_escape(self):
        corpora=self.manifest(lambda m:m["fixtures"][0].update(path="../escape.json"))
        self.assertTrue(self.run_with(corpora=corpora)["discovery"]["errors"])
    def test_source_identity_mismatch(self):
        corpora=self.manifest(lambda m:m["fixtures"][0].update(fixture_source_id="wrong"))
        self.assertEqual(self.run_with(corpora=corpora)["totals"]["INVALID_FIXTURE"],1)
    def test_duplicate_path(self):
        corpora=self.manifest(lambda m:m["fixtures"][1].update(path=m["fixtures"][0]["path"]))
        self.assertTrue(self.run_with(corpora=corpora)["discovery"]["errors"])
    def test_known_adapter(self):self.assertIsNotNone(self.adapters.resolve("generic","core.synthetic.v0"))
    def test_unknown_adapter_visible(self):
        corpora=self.manifest(lambda m:[f["adapter_bindings"].update(generic="unregistered") for f in m["fixtures"]])
        result=self.run_with(corpora=corpora)
        self.assertEqual(result["totals"],{"PASS":18,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":18})
        self.assertEqual(len(result["rows"]),36)
    def test_duplicate_adapter(self):
        a=self.adapters.resolve("generic","core.synthetic.v0")
        with self.assertRaises(ValueError):AdapterRegistry([a,a])
    def test_adapter_order(self):
        ids=self.adapters.identities()
        reverse=AdapterRegistry([self.adapters.resolve(i,"core.synthetic.v0") for i in reversed(ids)])
        self.assertEqual(encode(self.run_with()),encode(self.run_with(adapters=reverse)))
    def test_adapter_identity_not_semantic(self):
        original=self.adapters.resolve("generic","core.synthetic.v0")
        adapters=AdapterRegistry([replace(original,adapter_id="anything.v7"),self.adapters.resolve("messaging","core.synthetic.v0")])
        corpora=self.manifest(lambda m:[f["adapter_bindings"].update(generic="anything.v7") for f in m["fixtures"]])
        self.assertEqual(self.run_with(corpora=corpora,adapters=adapters)["totals"]["PASS"],36)
    def test_context_adapter(self):
        calls=[]
        def actual(request,context):
            calls.append(deepcopy(context));context.clear()
            return model.run(request)
        adapters=AdapterRegistry([Adapter("generic",("core.synthetic.v0",),actual,"1",True),self.adapters.resolve("messaging","core.synthetic.v0")])
        self.assertEqual(self.run_with(adapters=adapters)["totals"]["PASS"],36)
        self.assertTrue(all(c=={"adapter_id":"generic","adapter_version":"1","expectation_profile_id":"core.synthetic.v0"} for c in calls))
    def test_unknown_profile_visible(self):
        result=self.run_with(profiles=ExpectationRegistry())
        self.assertEqual(result["totals"],{"PASS":0,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":6})
        self.assertTrue(all(r["fixture_id"].startswith("core:") for r in result["rows"]))
    def test_profile_scope_cannot_be_partially_selected(self):
        corpora=self.manifest(lambda m:m["fixtures"][0].update(expectation_profile_id="absent"))
        self.assertEqual(self.run_with(corpora=corpora)["totals"]["UNSUPPORTED"],6)
    def test_invalid_expectation_blocks_all(self):
        profile=self.profiles.resolve("core.synthetic.v0")
        p=self.root/profile.expectations_path;p.write_bytes(p.read_bytes()+b" ")
        result=self.run_with()
        self.assertEqual(result["totals"],{"PASS":0,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":6})
        self.assertTrue(all("PROFILE_ERROR" in r["errors"][0] for r in result["rows"]))
    def test_undeclared_adapter_slot_blocks_profile(self):
        corpora=self.manifest(lambda m:m["fixtures"][0]["adapter_bindings"].pop("generic"))
        self.assertEqual(self.run_with(corpora=corpora)["totals"]["UNSUPPORTED"],6)
    def test_fail_is_executed_mismatch(self):
        def reject(request):
            return {"results":[{"label":"operation","decision":"REJECT","before":request["state"],"after":request["state"],"effects":[],"position":None}]}
        adapters=AdapterRegistry([Adapter("generic",("core.synthetic.v0",),reject),self.adapters.resolve("messaging","core.synthetic.v0")])
        result=self.run_with(adapters=adapters)
        self.assertGreater(result["totals"]["FAIL"],0)
        self.assertTrue(all(r["result"]["observed"] is not None for r in result["rows"] if r["status"]=="FAIL"))
    def test_execution_crash_not_semantic_fail(self):
        def crash(request):raise RuntimeError("setup")
        adapters=AdapterRegistry([Adapter("generic",("core.synthetic.v0",),crash),self.adapters.resolve("messaging","core.synthetic.v0")])
        result=self.run_with(adapters=adapters)
        self.assertEqual(result["totals"],{"PASS":18,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":18})
        self.assertTrue(all(r["diagnostic_kind"]=="EXECUTION_ERROR" for r in result["rows"] if r["status"]=="UNSUPPORTED"))
    def test_legacy_case_records_identical(self):
        old={r["key"]:r for r in evaluate(self.root)["evidence"]["cases"]}
        new={r["result"]["key"]:r["result"] for r in self.run_with()["rows"]}
        self.assertEqual(encode(old),encode(new))
    def test_direct_adapter_matches_registry(self):
        from adapters.messaging import model as other
        implementations={"generic":model.run,"messaging":other.run}
        for fixture in sorted((self.root/"fixtures").glob("*.json")):
            for case in load(fixture)["cases"]:
                for adapter,request in case["requests"].items():
                    self.assertEqual(implementations[adapter](deepcopy(request)),self.adapters.resolve(adapter,"core.synthetic.v0").invoke(deepcopy(request),{}))
    def test_identity_only_schema_projection(self):
        old=load(self.root/"schema/relation-binding-fixture.v0.schema.json")
        new=load(self.root/"schema/registered-fixture.v0.schema.json")
        for schema in (old,new):
            schema.pop("$id")
            schema["properties"].pop("id")
            schema["properties"]["cases"]["items"]["properties"].pop("requests")
        self.assertEqual(old,new)
    def test_native_four_counts(self):self.assertEqual(set(self.run_with()["totals"]),{"PASS","FAIL","INVALID_FIXTURE","UNSUPPORTED"})
    def test_deterministic_report(self):self.assertEqual(encode(self.run_with()),encode(self.run_with()))
    def make_arbitrary(self,namespace="lab",profile_id="lab.profile.v0"):
        fixture=load(sorted((self.root/"fixtures").glob("*.json"))[0])
        fixture["id"]=namespace+":unit"
        for case in fixture["cases"]:case["requests"]={"port":case["requests"]["generic"]}
        directory=self.root/namespace;directory.mkdir(exist_ok=True)
        path=namespace+"/fixture.json";(self.root/path).write_bytes(encode(fixture))
        original=self.profiles.resolve("core.synthetic.v0")
        def predictor(value):
            return {value["id"]+"/"+c["name"]:{"local_validity":local_validity(c["requests"]["port"]),"observation":predict(c["requests"]["port"])} for c in value["cases"]}
        def plan(value):return [{"row_id":value["id"]+"/"+c["name"],"adapter_id":"port","request":c["requests"]["port"]} for c in value["cases"]]
        docs=(FixtureDocument(fixture["id"],encode(fixture)),)
        artifact={"schema":"rsi-expectations.v0","profile_id":profile_id,"profile_version":"0","fixture_set_digest":fixture_set_digest(docs),"expectations":[{"fixture_id":fixture["id"],"prediction":predictor(fixture)}]}
        ap="oracle/"+namespace+".json";(self.root/ap).write_bytes(encode(artifact))
        validate=validator(self.root/"schema/registered-fixture.v0.schema.json").validate
        profile=replace(original,profile_id=profile_id,fixture_scope=(FixtureSource(fixture["id"],path),),predictor=predictor,plan=plan,validate_fixture=validate,validate_scope=lambda root:None,expectations_path=ap,expectations_digest=raw_digest(encode(artifact)))
        manifest={"schema":"rsi-fixture-corpus.v0","corpus_id":namespace,"namespace":namespace,"fixture_directory":namespace,"fixtures":[{"fixture_id":fixture["id"],"fixture_source_id":fixture["id"],"path":path,"expectation_profile_id":profile_id,"adapter_bindings":{"port":"test-adapter"}}]}
        mp="extensions/"+namespace+".json";(self.root/mp).write_bytes(encode(manifest))
        corpus=Corpus(namespace,mp,raw_digest(encode(manifest)),validate)
        adapter=Adapter("test-adapter",(profile_id,),lambda request:model.run(request))
        return corpus,profile,adapter
    def test_new_namespaced_corpus_profile_adapter_without_core_edit(self):
        c,p,a=self.make_arbitrary()
        result=execute(self.root,FixtureRegistry([c]),ExpectationRegistry([p]),AdapterRegistry([a]))
        self.assertEqual(result["totals"],{"PASS":3,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":0})
    def test_registered_nested_corpus_is_not_an_unexpected_file(self):
        c,p,a=self.make_arbitrary()
        nested=self.root/"fixtures/lab";nested.mkdir()
        shutil.copy2(self.root/"lab/fixture.json",nested/"fixture.json")
        path="fixtures/lab/fixture.json"
        manifest=load(self.root/c.manifest_path)
        manifest["fixture_directory"]="fixtures/lab";manifest["fixtures"][0]["path"]=path
        (self.root/c.manifest_path).write_bytes(encode(manifest))
        c=replace(c,manifest_digest=raw_digest(encode(manifest)))
        p=replace(p,fixture_scope=(FixtureSource("lab:unit",path),))
        corpora=FixtureRegistry([*self.corpora._corpora.values(),c])
        profiles=ExpectationRegistry([self.profiles.resolve("core.synthetic.v0"),p])
        adapters=AdapterRegistry([a,*self.adapters._adapters.values()])
        result=execute(self.root,corpora,profiles,adapters)
        self.assertEqual(result["totals"],{"PASS":39,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":0})
    def test_duplicate_identity_across_corpora(self):
        c,p,a=self.make_arbitrary()
        manifest=load(self.root/c.manifest_path);manifest["corpus_id"]="second"
        path="extensions/second.json";(self.root/path).write_bytes(encode(manifest))
        second=replace(c,corpus_id="second",manifest_path=path,manifest_digest=raw_digest(encode(manifest)))
        result=execute(self.root,FixtureRegistry([c,second]),ExpectationRegistry([p]),AdapterRegistry([a]))
        self.assertEqual(result["totals"]["PASS"],0)
        self.assertTrue(any("duplicate canonical" in e["error"] for e in result["discovery"]["errors"]))
    def test_same_local_id_two_namespaces(self):
        c1,p1,a=self.make_arbitrary("lab-one","one.v0")
        c2,p2,_=self.make_arbitrary("lab-two","two.v0")
        a=replace(a,supported_profiles=(p1.profile_id,p2.profile_id))
        result=execute(self.root,FixtureRegistry([c1,c2]),ExpectationRegistry([p1,p2]),AdapterRegistry([a]))
        reverse=execute(self.root,FixtureRegistry([c2,c1]),ExpectationRegistry([p2,p1]),AdapterRegistry([a]))
        self.assertEqual(encode(result),encode(reverse));self.assertEqual(result["totals"]["PASS"],6)
    def test_fixture_namespace_and_profile_text_do_not_choose_outcome(self):
        c,p,a=self.make_arbitrary("rejection","expected-reject.v99")
        result=execute(self.root,FixtureRegistry([c]),ExpectationRegistry([p]),AdapterRegistry([a]))
        self.assertEqual(result["totals"]["PASS"],3)
        self.assertEqual(result["rows"][0]["result"]["observed"]["results"][0]["decision"],"ACCEPT")
    def test_static_anti_coupling(self):
        forbidden={"crystal","receiptos","rvr","tsei","pq","semantic","messaging","generic"}
        for path in [*(ROOT/"runner").glob("*.py"),ROOT/"rsi/run.py",ROOT/"rsi/oracle.py"]:
            tree=ast.parse(path.read_text())
            for node in ast.walk(tree):
                if isinstance(node,(ast.If,ast.IfExp)):
                    for child in ast.walk(node.test):
                        if isinstance(child,ast.Constant) and type(child.value) is str:
                            self.assertFalse(any(word in child.value.lower() for word in forbidden),(path,child.value))

class MutationRegistryTests(unittest.TestCase):
    def mutation(self,trace):return Mutation("arbitrary:M1","target","check",lambda context:trace,"decision")
    def result(self,trace,targets=("target",)):
        return MutationRegistry([self.mutation(trace)]).execute(targets)
    def test_sixteen_explicit_registrations(self):
        ids=mutations().identities();self.assertEqual(len(ids),16)
        self.assertEqual(len(set(ids)),16);self.assertTrue(all("EXP-M"+str(n) in ids for n in range(1,5)))
    def test_duplicate_mutation(self):
        m=self.mutation(MutationTrace(False))
        with self.assertRaises(ValueError):MutationRegistry([m,m])
    def test_unknown_target_not_applied(self):self.assertEqual(self.result(MutationTrace(True),())["mutations"][0]["status"],"NOT_APPLIED")
    def test_unmapped_not_applied(self):self.assertEqual(self.result(MutationTrace(True))["mutations"][0]["status"],"NOT_APPLIED")
    def test_survived(self):self.assertEqual(self.result(MutationTrace(True,(CheckEvent("check","PASS","decision"),)))["mutations"][0]["status"],"SURVIVED")
    def test_killed(self):self.assertEqual(self.result(MutationTrace(True,(CheckEvent("check","FAIL","decision"),)))["mutations"][0]["status"],"KILLED")
    def test_setup_error_vacuous(self):self.assertEqual(self.result(MutationTrace(True,errors=("setup",)))["mutations"][0]["status"],"VACUOUS")
    def test_setup_assertion_vacuous(self):self.assertEqual(self.result(MutationTrace(True,(CheckEvent("check","FAIL","setup"),)))["mutations"][0]["status"],"VACUOUS")
    def test_teardown_cannot_kill(self):self.assertEqual(self.result(MutationTrace(True,(CheckEvent("check","FAIL","teardown"),)))["mutations"][0]["status"],"VACUOUS")
    def test_implementation_crash(self):
        def crash(context):raise SyntaxError("bad setup")
        m=replace(self.mutation(MutationTrace(False)),implementation=crash)
        self.assertEqual(MutationRegistry([m]).execute(["target"])["mutations"][0]["status"],"VACUOUS")
    def test_unrelated_failure_not_kill(self):
        r=self.result(MutationTrace(True,(CheckEvent("other","FAIL","decision"),CheckEvent("check","PASS","decision"))))
        self.assertEqual(r["mutations"][0]["status"],"SURVIVED");self.assertEqual(r["mutations"][0]["collateral"],["other"])
    def test_error_before_mapped_failure_vacuous(self):
        r=self.result(MutationTrace(True,(CheckEvent("other","ERROR","setup"),CheckEvent("check","FAIL","decision"))))
        self.assertEqual(r["mutations"][0]["status"],"VACUOUS")
    def test_order_and_identity_invariant(self):
        a=self.mutation(MutationTrace(True,(CheckEvent("check","FAIL","decision"),)))
        b=replace(a,mutation_id="unrelated-label")
        self.assertEqual(encode(MutationRegistry([a,b]).execute(["target"])),encode(MutationRegistry([b,a]).execute(["target"])))
    def test_setup_cannot_be_registered_as_expected_failure_phase(self):
        with self.assertRaises(ValueError):MutationRegistry([replace(self.mutation(MutationTrace(False)),expected_failure_phase="setup")])
    def test_prior_setup_assertion_blocks_kill(self):
        r=self.result(MutationTrace(True,(CheckEvent("other","FAIL","setup"),CheckEvent("check","FAIL","decision"))))
        self.assertEqual(r["mutations"][0]["status"],"VACUOUS")
    def test_four_explicit_counts(self):self.assertEqual(set(self.result(MutationTrace(False))["totals"]),{"KILLED","SURVIVED","VACUOUS","NOT_APPLIED"})

if __name__=="__main__":unittest.main()
