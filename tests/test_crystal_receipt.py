"""Real frozen evidence through relation/expectation/adapter execution."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import ast
import json
import shutil
import tempfile
import unittest
from unittest.mock import patch
from rsi.codec import encode,load,raw_digest
from runner.relation_runtime import execute
from runner.expectation_registry import ExpectationRegistry
from runner.adapter_registry import AdapterRegistry
from extensions.crystal_receipt import composition
from profiles.crystal_receipt import source,expectation,relation
from adapters.crystal_receipt import model
ROOT=Path(__file__).resolve().parents[1]

class CrystalTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix="crystal-tests-")
        self.root=Path(self.tmp.name)
        for name in ("evidence/crystal-receipt","profiles/crystal_receipt","adapters/crystal_receipt","corpora/crystal-receipt"):
            shutil.copytree(ROOT/name,self.root/name,ignore=shutil.ignore_patterns("__pycache__"))
        (self.root/"extensions").mkdir()
        shutil.copy2(ROOT/"extensions/crystal-receipt.corpus.v0.json",self.root/"extensions/crystal-receipt.corpus.v0.json")
        self.fixtures,self.expectations,self.adapters,self.relations=composition(self.root)
    def tearDown(self):self.tmp.cleanup()
    def run_crystal(self):return execute(self.root,self.fixtures,self.expectations,self.adapters,self.relations)
    def case(self,ident,name):
        value=load(self.root/("corpora/crystal-receipt/fixtures/"+ident+".json"))
        return next(c for c in value["cases"] if c["case_id"]==name)
    def normal(self,result):
        # A setup/adapter/source failure is ERROR, never a semantic mutant kill.
        if not result["admissions"] or any(r.get("diagnostic_kind") or r.get("result",{}).get("errors") for r in result["rows"]):
            raise RuntimeError("source/admission/adapter setup did not complete normally")
    def test_pipeline(self):
        result=self.run_crystal();self.normal(result)
        self.assertEqual(result["totals"],{"PASS":4,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":0})
    def test_negative(self):
        result=self.run_crystal();self.normal(result)
        row=next(r["result"] for r in result["rows"] if r["result"]["key"]=="CR-RSI-001/relation_substitution")
        self.assertEqual(row["observed"]["outputs"]["baseline_outcome"],"accepted_snapshot")
        self.assertEqual(row["observed"]["outputs"]["candidate_outcome"],"accepted_snapshot")
        self.assertFalse(row["observed"]["outputs"]["semantic_identity_preserved"])
        self.assertEqual(row["status"],"PASS")
    def test_mirror(self):
        result=self.run_crystal();self.normal(result)
        rows=[r["result"] for r in result["rows"] if r["fixture_source_id"]=="CR-RSI-002"]
        self.assertEqual(len(rows),2)
        for row in rows:
            self.assertTrue(row["observed"]["outputs"]["semantic_identity_preserved"])
            self.assertEqual(row["status"],"PASS")
    def test_source_pin(self):self.assertEqual(source.verify_source(self.root)["commit"],source.SOURCE_COMMIT)
    def test_source_digest_mismatch(self):
        p=self.root/"evidence/crystal-receipt/counterfactual-audit-boundary.ts";p.write_bytes(p.read_bytes()+b"\n")
        result=self.run_crystal();self.assertEqual(result["totals"]["UNSUPPORTED"],2);self.assertEqual(result["admissions"],{})
    def test_missing_source(self):
        (self.root/"evidence/crystal-receipt/canonicalize.ts").unlink()
        self.assertEqual(self.run_crystal()["totals"]["UNSUPPORTED"],2)
    def test_source_commit(self):
        p=self.root/source.SOURCE_PIN_PATH;value=load(p);value["commit"]="0"*40;p.write_bytes(encode(value))
        with patch.object(source,"SOURCE_PIN_SHA256",raw_digest(encode(value))):
            with self.assertRaisesRegex(source.SourceUnavailable,"SOURCE_COMMIT"):source.verify_source(self.root)
    def test_profile_resolution(self):self.assertEqual(self.relations.resolve(relation.PROFILE_ID,"0",relation.RELATION_ID).profile_id,relation.PROFILE_ID)
    def test_unknown_version(self):
        p=self.root/"corpora/crystal-receipt/fixtures/CR-RSI-001.json";v=load(p);v["relation_profile_version"]="1";p.write_bytes(encode(v))
        result=self.run_crystal();self.assertEqual(result["totals"]["UNSUPPORTED"],2);self.assertEqual(result["admissions"],{})
    def test_required_slots(self):
        p=self.relations.resolve(relation.PROFILE_ID,"0",relation.RELATION_ID)
        with self.assertRaises(ValueError):p.validate(relation.RELATION_ID,{"baseline":{}})
    def test_no_fake_fields(self):
        value=self.case("CR-RSI-001","control")["inputs"]
        self.assertEqual(set(value),{"baseline","candidate"})
        for endpoint in value.values():self.assertEqual(set(endpoint),{"semantic_artifact","manifest"})
    def test_one_semantic_value_substituted(self):
        a=self.case("CR-RSI-001","control")["inputs"];b=self.case("CR-RSI-001","relation_substitution")["inputs"]
        self.assertEqual(a["baseline"],b["baseline"]);self.assertEqual(a["candidate"]["manifest"],b["candidate"]["manifest"])
        left=a["candidate"]["semantic_artifact"];right=b["candidate"]["semantic_artifact"]
        self.assertEqual([k for k in left if left[k]!=right[k]],["expected_conformance_observation"])
    def test_actual_timestamp_change(self):
        v=self.case("CR-RSI-002","audit_timestamp_changed")["inputs"]
        self.assertNotEqual(v["baseline"]["manifest"],v["candidate"]["manifest"])
        self.assertEqual(v["baseline"]["semantic_artifact"],v["candidate"]["semantic_artifact"])
    def test_frozen_mirror_derivation(self):
        vector=json.loads((self.root/"evidence/crystal-receipt/V-SEM-MANIFEST-INVARIANT.json").read_text())
        fixture=load(self.root/"corpora/crystal-receipt/fixtures/CR-RSI-002.json")
        predicted=expectation.predict(fixture)
        for row in predicted.values():self.assertEqual(row["observation"]["outputs"]["canonical_candidate"],vector["expected"]["canonical_snapshot_json"])
    def test_predictor_independent(self):
        fixture=load(self.root/"corpora/crystal-receipt/fixtures/CR-RSI-001.json")
        before=expectation.predict(fixture)
        with patch.object(model,"capture",side_effect=RuntimeError("adapter broken")),patch.object(relation,"observed",side_effect=RuntimeError("actual broken")):
            self.assertEqual(expectation.predict(fixture),before)
    def test_tampered_expectation_atomic(self):
        profile=self.expectations.resolve(expectation.EXPECTATION_ID);p=self.root/profile.expectations_path;artifact=load(p)
        row=next(iter(artifact["expectations"][0]["prediction"].values()));row["observation"]["outputs"]["semantic_identity_preserved"]=False
        p.write_bytes(encode(artifact));self.expectations=ExpectationRegistry([replace(profile,expectations_digest=raw_digest(encode(artifact)))])
        with patch.object(model,"capture",side_effect=RuntimeError("must not execute")):
            result=self.run_crystal()
        self.assertEqual(result["totals"],{"PASS":0,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":2});self.assertEqual(result["admissions"],{})
    def test_actual_cannot_read_expectations(self):
        value=self.case("CR-RSI-001","control")["inputs"]
        (self.root/"profiles/crystal_receipt/expectations.v0.json").unlink()
        observed=model.evaluate(self.root,{"inputs":value})
        self.assertTrue(observed["outputs"]["semantic_identity_preserved"])
        p=self.relations.resolve(relation.PROFILE_ID,"0",relation.RELATION_ID)
        self.assertEqual(p.evaluate_relation(relation.RELATION_ID,value),observed)
    def test_fixture_id_no_truth(self):
        fixture=load(self.root/"corpora/crystal-receipt/fixtures/CR-RSI-001.json");before=list(expectation.predict(fixture).values());fixture["id"]="arbitrary-reject-name"
        self.assertEqual(list(expectation.predict(fixture).values()),before)
    def test_output_determinism(self):self.assertEqual(encode(self.run_crystal()),encode(self.run_crystal()))
    def test_unsupported_transport(self):
        value=self.case("CR-RSI-001","control")["inputs"]
        for unsupported in (1.5,"\u00e9",{"nested":"value"}):
            v=deepcopy(value);v["candidate"]["semantic_artifact"]["extra"]=unsupported
            with self.assertRaises(ValueError):relation.validate_inputs(v)
    def test_reserved_metadata_not_stripped(self):
        v=self.case("CR-RSI-001","control")["inputs"];v["candidate"]["semantic_artifact"]["audit_timestamp"]="bad"
        with self.assertRaises(ValueError):relation.validate_inputs(v)
    def test_static_independence(self):
        source_text=(ROOT/"profiles/crystal_receipt/expectation.py").read_text()
        self.assertNotIn("adapters.",source_text);self.assertNotIn(".observed",source_text);self.assertNotIn(".capture",source_text)
        for path in ("adapters/crystal_receipt/model.py","profiles/crystal_receipt/relation.py"):
            self.assertNotIn("expectations.v0.json",(ROOT/path).read_text())
    def test_generic_modules_unchanged(self):
        pins=json.loads((ROOT/"artifacts/crystal-phase2a/before.json").read_text()) if (ROOT/"artifacts/crystal-phase2a/before.json").exists() else load(ROOT/"research/crystal-receipt-source-map-v0.json")["generic_hashes"]
        for path,pin in pins.items():
            if path.startswith(("runner/","rsi/","schema/")):
                self.assertEqual(raw_digest((ROOT/path).read_bytes()),pin,path)
    def test_no_core_domain_terms(self):
        for p in (ROOT/"runner").glob("*.py"):
            text=p.read_text().lower()
            for term in ("crystal","receiptos","audit_timestamp","semantic snapshot","lane k"):
                self.assertNotIn(term,text,str(p))

    def test_pinned_bytes_are_executed(self):
        original=model.read_sources
        def captured(root):
            result=original(root)
            (Path(root)/"evidence/crystal-receipt/counterfactual-audit-boundary.ts").write_bytes(b"not executable")
            return result
        inputs=self.case("CR-RSI-001","control")["inputs"]
        with patch.object(model,"read_sources",side_effect=captured):
            self.assertTrue(model.evaluate(self.root,{"inputs":inputs})["outputs"]["semantic_identity_preserved"])
        with self.assertRaises(source.SourceUnavailable):source.verify_source(self.root)
    def test_source_failure_cannot_be_mutation_kill(self):
        from runner.mutation_registry import Mutation,MutationRegistry,MutationTrace,CheckEvent
        mutation=Mutation("check","target","semantic",lambda c:MutationTrace(True,(CheckEvent("semantic","ERROR","test"),)),"test")
        self.assertEqual(MutationRegistry([mutation]).execute({"target"})["totals"]["VACUOUS"],1)
    def test_adapter_fault_does_not_change_admitted_expected(self):
        baseline=self.run_crystal();self.normal(baseline)
        original=self.adapters.resolve(model.ADAPTER_ID,expectation.EXPECTATION_ID)
        def faulty(request):
            result=original.evaluate(request);result["outputs"]["semantic_identity_preserved"]=True;result["relation_state"]="semantic_snapshots_match";return result
        self.adapters=AdapterRegistry([replace(original,evaluate=faulty)])
        result=self.run_crystal();self.normal(result)
        self.assertEqual([r["result"]["expected"] for r in result["rows"]],[r["result"]["expected"] for r in baseline["rows"]])
        self.assertEqual(result["totals"]["FAIL"],1)
    def test_frozen_negative_inputs(self):
        vector=json.loads((self.root/"evidence/crystal-receipt/V-SEM-MUTATION-DIFFERS.json").read_text())
        value=self.case("CR-RSI-001","relation_substitution")["inputs"]
        self.assertEqual(value["baseline"]["semantic_artifact"],vector["baseline_semantic_artifact"])
        self.assertEqual(value["candidate"]["semantic_artifact"],vector["mutated_semantic_artifact"])

    def test_combined_registration(self):
        from extensions.crystal_receipt import complete_composition
        result=execute(ROOT,*complete_composition(ROOT))
        self.assertEqual(result["totals"],{"PASS":40,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":0})
