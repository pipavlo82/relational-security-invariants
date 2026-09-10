from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import ast
import json
import shutil
import tempfile
import unittest
from unittest.mock import patch

from rsi.codec import encode, decode, digest, load, raw_digest
from rsi.oracle import predict, local_validity
from rsi.run import evaluate
from profiles.synthetic import make_profile, predict_fixture
from profiles.defaults import registries
from runner.expectation_registry import ExpectationRegistry, RegistryError
from runner.expectation_contract import admit, load_fixtures, fixture_set_digest, ProfileError, FixtureDocument
from runner.adapter_registry import Adapter, AdapterRegistry
from runner.execution import run_profile, run_registered, summary

ROOT = Path(__file__).resolve().parents[1]

class ExpectationTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="rsi-expectation-test-")
        self.root = Path(self.tmp.name)
        for name in ("schema","fixtures","oracle","profiles"):
            shutil.copytree(ROOT/name,self.root/name,ignore=shutil.ignore_patterns("__pycache__"))
        shutil.copy2(ROOT/"manifest.json",self.root/"manifest.json")
        self.profile = make_profile(self.root)
        self.docs = load_fixtures(self.root,self.profile)
    def tearDown(self): self.tmp.cleanup()

    def rewrite(self, mutate):
        path=self.root/self.profile.expectations_path
        value=load(path);mutate(value);path.write_bytes(encode(value))
        return replace(self.profile,expectations_digest=raw_digest(path.read_bytes()))

    @staticmethod
    def corrupt(value):
        row=value["expectations"][-1]["prediction"]
        key=next(iter(row))
        event=row[key]["observation"]["results"][0]
        event["decision"]="REJECT" if event["decision"]=="ACCEPT" else "ACCEPT"

    def test_current_pinned_set_admitted(self):
        admitted=admit(self.root,self.profile,self.docs)
        self.assertEqual(admitted.fixture_ids(),tuple(sorted(d.fixture_id for d in self.docs)))
        old=load(self.root/"oracle/expected.v0.json")["expectations"]
        merged={key:value for ident in admitted.fixture_ids() for key,value in admitted.for_fixture(ident).items()}
        self.assertEqual(encode(old),encode(merged))

    def test_predictor_exactly_preserved(self):
        for doc in self.docs:
            fixture=doc.value();wrapped=predict_fixture(fixture)
            for case in fixture["cases"]:
                for adapter,request in case["requests"].items():
                    key=fixture["id"]+"/"+case["name"]+"/"+adapter
                    self.assertEqual(encode(wrapped[key]),encode({"local_validity":local_validity(request),"observation":predict(request)}))

    def test_modified_value_rejected(self):
        profile=self.rewrite(self.corrupt)
        with self.assertRaises(ProfileError) as cm: admit(self.root,profile,self.docs)
        self.assertEqual(cm.exception.code,"PREDICTION_MISMATCH")

    def test_artifact_digest_checked(self):
        self.rewrite(self.corrupt)
        with self.assertRaises(ProfileError) as cm: admit(self.root,self.profile,self.docs)
        self.assertEqual(cm.exception.code,"ARTIFACT_DIGEST")

    def test_missing_row_rejected(self):
        profile=self.rewrite(lambda a:a["expectations"].pop())
        with self.assertRaises(ProfileError) as cm:admit(self.root,profile,self.docs)
        self.assertEqual(cm.exception.code,"ROW_SET")

    def test_extra_row_rejected(self):
        def extra(a):
            row=deepcopy(a["expectations"][0]);row["fixture_id"]="unexpected";a["expectations"].append(row)
        with self.assertRaises(ProfileError) as cm:admit(self.root,self.rewrite(extra),self.docs)
        self.assertEqual(cm.exception.code,"ROW_SET")

    def test_duplicate_row_rejected(self):
        profile=self.rewrite(lambda a:a["expectations"].append(deepcopy(a["expectations"][0])))
        with self.assertRaises(ProfileError) as cm:admit(self.root,profile,self.docs)
        self.assertEqual(cm.exception.code,"DUPLICATE_ROW")

    def test_fixture_bytes_bound(self):
        value=self.docs[0].value()
        for c in value["cases"]:
            for req in c["requests"].values():req["state"]["head"]="other-initial-state"
        changed=(replace(self.docs[0],raw=encode(value)),)+self.docs[1:]
        with self.assertRaises(ProfileError) as cm:admit(self.root,self.profile,changed)
        self.assertEqual(cm.exception.code,"FIXTURE_SET_DIGEST")

    def test_fixture_add_remove_replace_invalidates_binding(self):
        original=fixture_set_digest(self.docs)
        self.assertNotEqual(original,fixture_set_digest(self.docs[:-1]))
        self.assertNotEqual(original,fixture_set_digest(self.docs+(FixtureDocument("added",encode({"id":"added"})),)))
        self.assertNotEqual(original,fixture_set_digest((replace(self.docs[0],raw=self.docs[0].raw+b"\n"),)+self.docs[1:]))
        with self.assertRaises(ValueError):fixture_set_digest(self.docs+(self.docs[0],))

    def test_fixture_order_independent_digest(self):
        self.assertEqual(fixture_set_digest(self.docs),fixture_set_digest(tuple(reversed(self.docs))))

    def test_fixture_scope_cannot_be_reduced(self):
        with self.assertRaises(ProfileError):admit(self.root,self.profile,self.docs[:-1])

    def test_atomic_admission(self):
        profile=self.rewrite(self.corrupt)
        with self.assertRaises(ProfileError) as cm:admit(self.root,profile,self.docs)
        self.assertEqual(cm.exception.code,"PREDICTION_MISMATCH")

    def test_profile_failure_prevents_all_adapter_execution(self):
        profile=self.rewrite(self.corrupt)
        calls=[]
        adapters=AdapterRegistry([Adapter(name,(profile.profile_id,),lambda req:calls.append(req)) for name in ("messaging","generic")])
        result=run_profile(self.root,profile.profile_id,ExpectationRegistry([profile]),adapters)
        self.assertEqual(calls,[])
        self.assertEqual(summary(result["cases"]),{"PASS":0,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":1})
        self.assertEqual(result["profile_error"],"PROFILE_ERROR:PREDICTION_MISMATCH")

    def test_admitted_rows_are_detached(self):
        admitted=admit(self.root,self.profile,self.docs);ident=self.docs[0].fixture_id
        original=admitted.for_fixture(ident);changed=admitted.for_fixture(ident);changed.clear()
        self.assertEqual(admitted.for_fixture(ident),original)

    def test_predictor_only_receives_fixture_and_runs_before_artifact_load(self):
        import runner.expectation_contract as contract
        events=[];old=contract.safe_path
        def path(root,name):
            if name==self.profile.expectations_path:events.append("artifact")
            return old(root,name)
        def predictor(fixture):
            self.assertFalse({"expectations","prediction","expected"}&set(fixture))
            events.append("predict");return self.profile.predictor(fixture)
        with patch.object(contract,"safe_path",side_effect=path):
            admit(self.root,replace(self.profile,predictor=predictor),self.docs)
        self.assertEqual(events,["predict"]*6+["artifact"])

    def test_predictor_failure_is_profile_error(self):
        def crash(f):raise RuntimeError("setup")
        with self.assertRaises(ProfileError) as cm:admit(self.root,replace(self.profile,predictor=crash),self.docs)
        self.assertEqual(cm.exception.code,"PREDICTOR_ERROR")

    def test_predictor_mutating_input_rejected(self):
        def mutate(f):
            answer=self.profile.predictor(f);f["id"]="changed";return answer
        with self.assertRaises(ProfileError):admit(self.root,replace(self.profile,predictor=mutate),self.docs)

    def test_same_predictor_and_adapter_rejected(self):
        adapters=AdapterRegistry([Adapter(name,(self.profile.profile_id,),self.profile.predictor) for name in ("messaging","generic")])
        result=run_profile(self.root,self.profile.profile_id,ExpectationRegistry([self.profile]),adapters)
        self.assertEqual(result["profile_error"],"PROFILE_ERROR:SELF_VALIDATION")

    def test_actual_cannot_supply_expected(self):
        def bad(req):
            return {"results":[{"label":"operation","decision":"REJECT","before":req["state"],"after":req["state"],"effects":[],"position":None}]}
        adapters=AdapterRegistry([Adapter(name,(self.profile.profile_id,),bad) for name in ("messaging","generic")])
        result=run_profile(self.root,self.profile.profile_id,ExpectationRegistry([self.profile]),adapters)
        positives=[r for r in result["cases"] if "/control/" in r["key"]]
        self.assertTrue(all(r["status"]=="FAIL" for r in positives))

    def test_unknown_profile_unsupported(self):
        result=run_profile(self.root,"unknown.v0",ExpectationRegistry([self.profile]),AdapterRegistry())
        self.assertEqual(result["cases"][0]["status"],"UNSUPPORTED")
        self.assertEqual(result["profile_error"],"UNKNOWN_PROFILE")

    def test_duplicate_profile_rejected(self):
        with self.assertRaises(RegistryError):ExpectationRegistry([self.profile,self.profile])

    def test_duplicate_fixture_registration_rejected(self):
        with self.assertRaises(RegistryError):ExpectationRegistry([replace(self.profile,fixture_scope=self.profile.fixture_scope+(self.profile.fixture_scope[0],))])

    def test_registration_order_invariant(self):
        other=replace(self.profile,profile_id="architecture.other.v0")
        _,adapters=registries(self.root)
        a=ExpectationRegistry([self.profile,other]);b=ExpectationRegistry([other,self.profile])
        self.assertEqual(a.identities(),b.identities())
        self.assertEqual(encode(run_registered(self.root,a,adapters)),encode(run_registered(self.root,b,adapters)))

    def test_new_profile_without_core_change(self):
        artifact=load(self.root/self.profile.expectations_path)
        artifact["profile_id"]="architecture.alternate.v0"
        path=self.root/"oracle/test-expectations.json";path.write_bytes(encode(artifact))
        profile=replace(self.profile,profile_id=artifact["profile_id"],expectations_path="oracle/test-expectations.json",expectations_digest=raw_digest(path.read_bytes()),validate_scope=lambda root:None)
        _,defaults=registries(self.root)
        adapters=AdapterRegistry([replace(defaults.resolve(name,self.profile.profile_id),supported_profiles=(profile.profile_id,)) for name in ("generic","messaging")])
        result=run_profile(self.root,profile.profile_id,ExpectationRegistry([profile]),adapters)
        self.assertEqual(summary(result["cases"]),{"PASS":36,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":0})

    def test_unknown_adapter_preserved(self):
        result=run_profile(self.root,self.profile.profile_id,ExpectationRegistry([self.profile]),AdapterRegistry())
        self.assertEqual(len(result["cases"]),36)
        self.assertTrue(all(r["status"]=="UNSUPPORTED" for r in result["cases"]))

    def test_malformed_fixture_distinct_from_profile_error(self):
        (self.root/self.profile.fixture_scope[0].path).write_text('{}')
        result=run_profile(self.root,self.profile.profile_id,ExpectationRegistry([self.profile]),AdapterRegistry())
        self.assertEqual(result["cases"][0]["status"],"INVALID_FIXTURE")
        self.assertEqual(result["profile_error"],"FIXTURE_INVALID")

    def test_all_four_top_states_serialized(self):
        states=("PASS","FAIL","INVALID_FIXTURE","UNSUPPORTED")
        self.assertEqual(json.loads(json.dumps(summary([]))),{s:0 for s in states})
        self.assertEqual(summary([{"status":s} for s in states]),{s:1 for s in states})

    def test_all_36_rows_unchanged(self):
        original=load(self.root/"oracle/expected.v0.json")["expectations"]
        report=evaluate(self.root)
        self.assertEqual(report["totals"],{"PASS":36,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":0})
        for row in report["evidence"]["cases"]:
            self.assertEqual(encode(row["expected"]),encode(original[row["key"]]["observation"]))
            self.assertEqual(row["expected"],row["observed"])

    def test_expectation_schema_validates(self):
        from jsonschema import Draft202012Validator
        schema=json.loads((ROOT/"schema/expectations.v0.schema.json").read_text())
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(load(self.root/self.profile.expectations_path))

    def test_core_has_no_domain_or_fixture_id_conditions(self):
        for relative in ("runner/execution.py","runner/expectation_contract.py","runner/expectation_registry.py","rsi/run.py"):
            tree=ast.parse((ROOT/relative).read_text())
            for node in ast.walk(tree):
                if isinstance(node,(ast.If,ast.IfExp,ast.Compare)):
                    text=ast.unparse(node.test if isinstance(node,(ast.If,ast.IfExp)) else node)
                    self.assertFalse(any(x in text for x in ('RSI-001','messaging','generic','startswith("CR-','startswith(\'CR-')),relative)

    def test_plan_mismatch_prevents_execution(self):
        calls=[]
        profile=replace(self.profile,plan=lambda f:[])
        result=run_profile(self.root,profile.profile_id,ExpectationRegistry([profile]),AdapterRegistry())
        self.assertEqual(result["profile_error"],"PROFILE_ERROR:PLAN_MISMATCH")

    def test_expectation_identity_checked(self):
        profile=self.rewrite(lambda a:a.update(profile_id="wrong.profile"))
        with self.assertRaises(ProfileError) as cm:admit(self.root,profile,self.docs)
        self.assertEqual(cm.exception.code,"PROFILE_IDENTITY")

    def test_expectation_path_escape_rejected(self):
        with self.assertRaises(ProfileError):admit(self.root,replace(self.profile,expectations_path="../outside.json"),self.docs)

class MutationClassificationTests(unittest.TestCase):
    def check_phase_assertion(self, phase):
        from tools.prove_expectations_can_fail import track_phases, ExecutionResult, classify
        class Probe(unittest.TestCase):
            def setUp(self):
                if phase == "setup": self.fail("setup assertion")
            def test_body(self):
                if phase == "test": self.fail("mapped assertion")
            def tearDown(self):
                if phase == "teardown": self.fail("teardown assertion")
        test = Probe("test_body")
        suite = unittest.TestSuite([test]); track_phases(suite)
        result = ExecutionResult(); suite.run(result)
        return classify(result.rows, test.id())
    def test_setup_assertion_cannot_kill(self):
        self.assertEqual(self.check_phase_assertion("setup"), "VACUOUS")
    def test_teardown_assertion_cannot_kill(self):
        self.assertEqual(self.check_phase_assertion("teardown"), "VACUOUS")
    def test_body_assertion_can_kill(self):
        self.assertEqual(self.check_phase_assertion("test"), "KILLED")
    def test_setup_error_is_vacuous(self):
        from tools.prove_expectations_can_fail import classify
        self.assertEqual(classify([{"id":"mapped","status":"ERROR"}],"mapped"),"VACUOUS")
    def test_missing_execution_is_vacuous(self):
        from tools.prove_expectations_can_fail import classify
        self.assertEqual(classify([],"mapped"),"VACUOUS")
    def test_unapplied_target(self):
        from tools.prove_expectations_can_fail import classify
        self.assertEqual(classify([],"mapped",applied=False),"NOT_APPLIED")
    def test_collateral_is_not_kill(self):
        from tools.prove_expectations_can_fail import classify
        self.assertEqual(classify([{"id":"mapped","status":"PASS"},{"id":"other","status":"FAIL"}],"mapped"),"SURVIVED")
    def test_mapped_assertion_is_kill(self):
        from tools.prove_expectations_can_fail import classify
        self.assertEqual(classify([{"id":"mapped","status":"FAIL"}],"mapped"),"KILLED")

if __name__=="__main__":unittest.main()
