from copy import deepcopy
import importlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

from rsi.codec import encode, decode, digest, load, raw_digest, ContractError
from rsi.corpus import verify, validator, FAMILIES
from rsi.oracle import predict, local_validity
from rsi.run import evaluate
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from generate_fixtures import build, signed, public
from prove_can_fail import exercise, self_controls

class CodecTests(unittest.TestCase):
    def test_explicit_bytes(self):
        self.assertEqual(encode({"b": 1, "a": "x"}), b'{"a":"x","b":1}\n')
    def test_duplicate_key(self):
        with self.assertRaises(ContractError): decode(b'{"a":1,"a":2}')
    def test_float(self):
        with self.assertRaises(ContractError): decode(b'{"a":1.0}')
    def test_negative_zero(self):
        with self.assertRaises(ContractError): decode(b'{"a":-0.0}')
    def test_nan(self):
        with self.assertRaises(ContractError): decode(b'{"a":NaN}')
    def test_unsafe_integer(self):
        with self.assertRaises(ContractError): encode(2**53)
    def test_unicode(self):
        with self.assertRaises(ContractError): encode({"a":"\u00e9"})
    def test_surrogate(self):
        with self.assertRaises(ContractError): decode(b'{"a":"\\ud800"}')
    def test_unterminated_lf(self):
        with self.assertRaises(ContractError): decode(b'{"a":1}', canonical=True)
    def test_crlf(self):
        with self.assertRaises(ContractError): decode(b'{"a":1}\r\n', canonical=True)
    def test_double_lf(self):
        with self.assertRaises(ContractError): decode(b'{"a":1}\n\n', canonical=True)
    def test_bool_not_integer(self):
        self.assertNotEqual(encode(True), encode(1))
    def test_non_string_key(self):
        with self.assertRaises(ContractError): encode({1:"x"})

class CorpusTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)/"repo"
        shutil.copytree(ROOT, self.root, ignore=shutil.ignore_patterns(".git", ".venv", "artifacts", "__pycache__"))
        self.fixture = next((self.root/"fixtures").glob("RSI-001-*.json"))
    def tearDown(self): self.temp.cleanup()
    def repin(self, path):
        m = load(self.root/"manifest.json")
        m["files"][path.relative_to(self.root).as_posix()] = raw_digest(path.read_bytes())
        (self.root/"manifest.json").write_bytes(encode(m))
    def change(self, fn, repin=True):
        f = load(self.fixture); fn(f); self.fixture.write_bytes(encode(f))
        if repin: self.repin(self.fixture)
    def test_complete_corpus(self):
        fixtures, oracle = verify(self.root)
        self.assertEqual(len(fixtures),6); self.assertEqual(len(oracle),36)
    def test_definition_derived_regeneration(self):
        for p, content in build().items():
            self.assertEqual((ROOT/p).read_bytes(),content,p)
    def test_raw_tamper(self):
        self.fixture.write_bytes(self.fixture.read_bytes()+b" ")
        with self.assertRaises(ContractError): verify(self.root)
    def test_repin_cannot_hide_noncanonical(self):
        self.fixture.write_bytes(b" "+self.fixture.read_bytes()); self.repin(self.fixture)
        with self.assertRaises(ContractError): verify(self.root)
    def test_missing_fixture(self):
        self.fixture.unlink()
        with self.assertRaises(ContractError): verify(self.root)
    def test_unregistered_fixture(self):
        (self.root/"fixtures/extra.json").write_bytes(self.fixture.read_bytes())
        with self.assertRaises(ContractError): verify(self.root)
    def test_oracle_tamper_with_updated_pin(self):
        path=self.root/"oracle/expected.v0.json"; data=load(path)
        data["expectations"]["RSI-001/mutation/messaging"]["observation"]["results"][0]["decision"]="ACCEPT"
        path.write_bytes(encode(data)); self.repin(path)
        with self.assertRaises(ContractError): verify(self.root)
    def test_relation_label_mismatch(self):
        self.change(lambda f:f.update(protected_relation="context_binding"))
        with self.assertRaises(ContractError): verify(self.root)
    def test_expected_label_in_challenge(self):
        self.change(lambda f:f["cases"][0]["requests"]["messaging"].update(expected="ACCEPT"))
        with self.assertRaises(Exception): verify(self.root)
    def test_bool_revision(self):
        self.change(lambda f:f["cases"][0]["requests"]["messaging"]["state"].update(revision=True))
        with self.assertRaises(Exception): verify(self.root)
    def test_local_validity_lie(self):
        self.change(lambda f:f["cases"][0].update(local_validity_expected=False))
        with self.assertRaises(ContractError): verify(self.root)
    def test_duplicate_case(self):
        self.change(lambda f:f["cases"][2].update(name="control"))
        with self.assertRaises(ContractError): verify(self.root)
    def test_mutation_disappears(self):
        self.change(lambda f:f["cases"][1].update(requests=deepcopy(f["cases"][0]["requests"])))
        with self.assertRaises(ContractError): verify(self.root)
    def test_mutation_cannot_change_unrelated_state(self):
        self.change(lambda f:f["cases"][1]["requests"]["messaging"]["state"].update(head="different"))
        with self.assertRaises(ContractError): verify(self.root)
    def test_mirror_must_change_representation(self):
        self.change(lambda f:f["cases"][2].update(requests=deepcopy(f["cases"][0]["requests"])))
        with self.assertRaises(ContractError): verify(self.root)
    def test_manifest_path_escape(self):
        m=load(self.root/"manifest.json"); m["files"]["../outside"]="0"*64
        (self.root/"manifest.json").write_bytes(encode(m))
        with self.assertRaises(ContractError): verify(self.root)
    def test_document_id_is_not_schema(self):
        self.change(lambda f:f.update(schema="RSI-core-v0"))
        with self.assertRaises(Exception): verify(self.root)
    def test_schema_external_ref(self):
        path=self.root/"schema/relation-binding-fixture.v0.schema.json"; s=load(path);s["$ref"]="https://invalid.invalid/schema"
        path.write_bytes(encode(s)); self.repin(path)
        with self.assertRaises(ContractError): verify(self.root)

class SemanticsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fs,_ = verify(ROOT)
        cls.requests={(f["id"],c["name"],a):r for f in fs for c in f["cases"] for a,r in c["requests"].items()}
    def req(self, ident, name="control", adapter="messaging"):
        return deepcopy(self.requests[ident,name,adapter])
    def each(self, request):
        for adapter in ["messaging","generic"]:
            module=importlib.import_module("adapters."+adapter+".model")
            actual=module.run(deepcopy(request));self.assertEqual(actual,predict(request),adapter)
            yield actual
    def test_all_36_actual_evaluations(self):
        report=evaluate(); self.assertEqual(report["evidence"]["counts"],{"PASS":36,"FAIL":0,"RUNNER_ERROR":0})
    def test_deterministic_evidence(self):
        self.assertEqual(encode(evaluate()),encode(evaluate()))
    def test_signature_valid_does_not_authorize_subject(self):
        req=self.req("RSI-001","mutation"); self.assertTrue(local_validity(req))
        for out in self.each(req):self.assertEqual(out["results"][0]["decision"],"REJECT")
    def test_auth_rejection_no_state_or_effect(self):
        req=self.req("RSI-003","mutation");self.assertFalse(local_validity(req))
        for out in self.each(req):
            e=out["results"][0];self.assertEqual(e["before"],e["after"]);self.assertEqual(e["effects"],[])
    def test_atomic_race(self):
        for out in self.each(self.req("RSI-004","mutation")):
            self.assertEqual([e["decision"] for e in out["results"]],["ACCEPT","CONFLICT"])
            self.assertEqual([e["position"] for e in out["results"]],[0,None])
    def test_atomic_refresh(self):
        for out in self.each(self.req("RSI-004")):
            self.assertEqual([e["position"] for e in out["results"]],[0,1])
    def test_context_mutation_still_authentic(self):
        req=self.req("RSI-006","mutation");self.assertTrue(local_validity(req))
        for out in self.each(req):self.assertEqual(out["results"][0]["decision"],"REJECT")
    def test_status_absence_is_unverifiable_not_false(self):
        for out in self.each(self.req("RSI-008","mutation")):
            self.assertEqual(out["results"][0]["decision"],"UNVERIFIABLE")
    def test_evidence_wrong_operation(self):
        req=self.req("RSI-008");proof=req["evidence"][0];body=json.loads(bytes.fromhex(proof["payload_hex"]))
        body["operation_id"]="other";req["evidence"]=[signed(body,"witness")]
        self.assertTrue(local_validity(req))
        for out in self.each(req):self.assertEqual(out["results"][0]["decision"],"UNVERIFIABLE")
    def test_evidence_wrong_scope(self):
        req=self.req("RSI-008");body=json.loads(bytes.fromhex(req["evidence"][0]["payload_hex"]))
        body["scope"]="other";req["evidence"]=[signed(body,"witness")]
        for out in self.each(req):self.assertEqual(out["results"][0]["decision"],"UNVERIFIABLE")
    def test_evidence_wrong_issuer(self):
        req=self.req("RSI-008");body=json.loads(bytes.fromhex(req["evidence"][0]["payload_hex"]))
        req["evidence"]=[signed(body,"mallory")]
        for out in self.each(req):self.assertEqual(out["results"][0]["decision"],"UNVERIFIABLE")
    def test_evidence_wrong_kind(self):
        req=self.req("RSI-008");body=json.loads(bytes.fromhex(req["evidence"][0]["payload_hex"]))
        body["kind"]="attempted";req["evidence"]=[signed(body,"witness")]
        for out in self.each(req):self.assertEqual(out["results"][0]["decision"],"UNVERIFIABLE")
    def test_ingress_paths(self):
        for out in self.each(self.req("RSI-009","mutation")):
            self.assertEqual([e["decision"] for e in out["results"]],["REJECT"]*4)
    def test_mirror_changes_raw_bytes_not_outcome(self):
        for ident in FAMILIES:
            for adapter in ["messaging","generic"]:
                c=self.req(ident,adapter=adapter);m=self.req(ident,"mirror_positive",adapter)
                self.assertNotEqual(c["proof"]["payload_hex"],m["proof"]["payload_hex"])
                self.assertEqual(predict(c),predict(m))
    def test_adapter_never_receives_oracle_labels(self):
        import adapters.messaging.model as module
        original=module.run
        def guarded(req):
            self.assertFalse({"id","expected","name","role","mutation","local_validity_expected"} & set(req))
            return original(req)
        with patch.object(module,"run",side_effect=guarded):
            self.assertEqual(evaluate()["evidence"]["counts"]["PASS"],36)
    def test_adapter_exception_is_not_kill(self):
        with patch("adapters.messaging.model.run",side_effect=RuntimeError("synthetic fault")):
            c=evaluate()["evidence"]["counts"]
            self.assertEqual(c,{"PASS":18,"FAIL":0,"RUNNER_ERROR":18})
    def test_always_reject_fails_positive_controls(self):
        def reject(req):
            return {"results":[{"label":"operation","decision":"REJECT","before":req["state"],"after":req["state"],"effects":[],"position":None}]}
        with patch("adapters.messaging.model.run",side_effect=reject):
            rows=evaluate()["evidence"]["cases"]
            self.assertTrue(all(r["status"]=="FAIL" for r in rows if "/control/messaging" in r["key"]))
    def test_mutating_challenge_is_runner_error(self):
        def mutate(req):
            req["state"]["head"]="altered"
            return predict(req)
        with patch("adapters.messaging.model.run",side_effect=mutate):
            self.assertEqual(evaluate()["evidence"]["counts"]["RUNNER_ERROR"],18)
    def test_invalid_adapter_output_is_runner_error(self):
        with patch("adapters.messaging.model.run",return_value={"pass":True}):
            self.assertEqual(evaluate()["evidence"]["counts"]["RUNNER_ERROR"],18)
    def test_incomplete_schedule(self):
        req=self.req("RSI-004");req["schedule"]=[{"kind":"read","worker":"a"}]
        with self.assertRaises(ContractError):predict(req)
        for adapter in ["messaging","generic"]:
            with self.assertRaises(ContractError):importlib.import_module("adapters."+adapter+".model").run(req)

class ClassifierTests(unittest.TestCase):
    def test_classifier_negative_controls(self):
        for row in self_controls():
            self.assertTrue(row["ok"],row)

if __name__ == "__main__": unittest.main()
