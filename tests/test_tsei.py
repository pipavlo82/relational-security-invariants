"""Real serializer/binding evidence through the unchanged conformance pipeline."""
from tools.protected_maintenance import mismatches
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import json
import shutil
import tempfile
import unittest
from unittest.mock import patch
from rsi.codec import encode, load, raw_digest
from runner.relation_runtime import execute, validate_envelope
from runner.expectation_registry import ExpectationRegistry
from runner.adapter_registry import AdapterRegistry
from extensions.tsei import composition, complete_composition
from profiles.tsei import source, relation, expectation
from adapters.tsei import model

ROOT = Path(__file__).resolve().parents[1]


class TSEITests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="tsei-test-")
        self.root = Path(self.tmp.name)
        for directory in ("evidence/tsei", "profiles/tsei", "corpora/tsei"):
            shutil.copytree(ROOT / directory, self.root / directory, ignore=shutil.ignore_patterns("__pycache__"))
        (self.root / "extensions").mkdir()
        shutil.copy2(ROOT / "extensions/tsei.corpus.v0.json", self.root / "extensions/tsei.corpus.v0.json")
        self.fixtures, self.expectations, self.adapters, self.relations = composition(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def fixture(self, n):
        return load(self.root / ("corpora/tsei/fixtures/TSEI-RSI-%03d.json" % n))

    def run_domain(self):
        return execute(self.root, self.fixtures, self.expectations, self.adapters, self.relations)

    def normal(self, result):
        if not result["admissions"] or any(r.get("diagnostic_kind") or r.get("result", {}).get("errors") for r in result["rows"]):
            raise RuntimeError("mapped decision did not execute normally")

    def observed(self, n, result=None):
        result = self.run_domain() if result is None else result
        self.normal(result)
        row = next(r["result"] for r in result["rows"] if r["fixture_source_id"] == "TSEI-RSI-%03d" % n)
        return row, row["observed"]["outputs"]

    def test_pipeline(self):
        result = self.run_domain(); self.normal(result)
        self.assertEqual(result["totals"], {"PASS": 7, "FAIL": 0, "INVALID_FIXTURE": 0, "UNSUPPORTED": 0})

    def test_serializer_control(self):
        row, out = self.observed(1)
        self.assertTrue(out["local_structure_valid"])
        self.assertTrue(out["serializer_binding"])
        self.assertTrue(out["artifact_covered"])
        self.assertEqual(out["artifact_serialized_sha256"], "81103aa69250ea56e887eaab3cd9bf363d341563f05d0676be389c3e40a72871")
        self.assertEqual(row["status"], "PASS")

    def test_wrong_serializer(self):
        row, out = self.observed(2)
        self.assertTrue(out["local_structure_valid"])
        self.assertEqual(out["record_verdict"], "valid")
        self.assertFalse(out["serializer_binding"])
        self.assertFalse(out["claim_admissible"])
        self.assertEqual(row["status"], "PASS")

    def test_mechanism_not_adoption(self):
        row, out = self.observed(3)
        self.assertTrue(out["mechanism_active"])
        self.assertFalse(out["producer_adopted"])
        self.assertFalse(out["record_introduced"])
        self.assertFalse(out["artifact_covered"])
        self.assertEqual(row["status"], "PASS")

    def test_adoption_not_record(self):
        row, out = self.observed(4)
        self.assertTrue(out["producer_adopted"])
        self.assertFalse(out["record_introduced"])
        self.assertFalse(out["artifact_covered"])
        self.assertEqual(row["status"], "PASS")

    def test_record_introduction(self):
        row, out = self.observed(5)
        self.assertTrue(out["record_introduced"])
        self.assertTrue(out["producer_adopted"])
        self.assertTrue(out["artifact_covered"])
        self.assertEqual(row["status"], "PASS")

    def test_nonretroactivity(self):
        row, out = self.observed(6)
        self.assertTrue(out["record_introduced"])
        self.assertTrue(out["producer_adopted"])
        self.assertFalse(out["artifact_covered"])
        self.assertFalse(out["claim_admissible"])
        self.assertEqual(out["artifact_binding_state"], "historically_unversioned")
        self.assertEqual(out["artifact_serialized_sha256"], "0ef9ee8f579b091d7287f05955661b04c386726e1b38c2009fa46005a09e0107")
        self.assertEqual(row["status"], "PASS")

    def test_no_authority_promotion(self):
        row, out = self.observed(7)
        self.assertTrue(out["artifact_covered"])
        self.assertEqual(out["authority_validation"]["status"], "UNSUPPORTED")
        self.assertFalse(out["claim_admissible"])
        self.assertEqual(row["status"], "PASS")

    def test_reported_labels_not_authority(self):
        inputs = self.fixture(7)["cases"][0]["inputs"]
        self.assertEqual(inputs["reported_status"], "PROVEN")
        self.assertEqual(inputs["reported_provenance"], "VALID_PROVENANCE")
        row, out = self.observed(7)
        self.assertFalse(out["claim_admissible"])
        self.assertEqual(row["status"], "PASS")

    def test_label_changes_have_no_authority_effect(self):
        inputs = self.fixture(7)["cases"][0]["inputs"]
        actual = model.evaluate(self.root, {"inputs": inputs})
        for labels in ({}, {"reported_status": "PROVEN"}, {"reported_provenance": "VALID_PROVENANCE"}, {"source_class": "AUTHORITATIVE"}):
            changed = {k:v for k,v in inputs.items() if k not in relation.OPTIONAL}; changed.update(labels)
            self.assertEqual(model.evaluate(self.root, {"inputs": changed}), actual)

    def test_receipt_withholds_operands(self):
        pin, blobs = source.read_sources(self.root)
        receipt = json.loads(blobs["tsei-ia-real-v2-20260824-02.production-grounding.json"])
        self.assertEqual(receipt["artifact_grounding"]["independent_grounding"], "PROVEN")
        self.assertEqual(receipt["artifact_grounding"]["oracle_input_state"], "VALID_PROVENANCE")
        missing = receipt["public_disclosure"]["does_not_disclose"]
        for item in ("nonce_bytes", "oracle_bytes", "object_a_bytes", "object_b_bytes", "case_level_attribution_sets"):
            self.assertIn(item, missing)

    def test_source_pin(self):
        pin = source.verify_source(self.root)
        self.assertEqual(pin["chronology"]["mechanism"]["commit"], source.MECHANISM)
        self.assertEqual(pin["chronology"]["producer_adoption"]["commit"], source.ADOPTION)
        self.assertEqual(pin["chronology"]["record_introduction"]["commit"], source.INTRODUCTION)
        self.assertEqual(pin["chronology"]["mechanism"]["record_tree_entries"], [])

    def test_wrong_digest(self):
        p = self.root / "evidence/tsei/recompute-kit-tsei.frozen-artifact.json"
        p.write_bytes(p.read_bytes() + b"\n")
        result = self.run_domain()
        self.assertEqual(result["totals"], {"PASS": 0, "FAIL": 0, "INVALID_FIXTURE": 0, "UNSUPPORTED": 7})
        self.assertEqual(result["admissions"], {})

    def test_wrong_adoption_commit(self):
        p = self.root / source.SOURCE_PIN_PATH; pin = load(p)
        pin["chronology"]["producer_adoption"]["commit"] = "0" * 40; p.write_bytes(encode(pin))
        with patch.object(source, "SOURCE_PIN_SHA256", raw_digest(encode(pin))):
            with self.assertRaisesRegex(source.SourceUnavailable, "SOURCE_CHRONOLOGY"):
                source.verify_source(self.root)

    def test_wrong_record_introduction(self):
        p = self.root / source.SOURCE_PIN_PATH; pin = load(p)
        pin["chronology"]["record_introduction"]["commit"] = "0" * 40; p.write_bytes(encode(pin))
        with patch.object(source, "SOURCE_PIN_SHA256", raw_digest(encode(pin))):
            with self.assertRaisesRegex(source.SourceUnavailable, "SOURCE_CHRONOLOGY"):
                source.verify_source(self.root)

    def test_wrong_source_head(self):
        p = self.root / source.SOURCE_PIN_PATH; pin = load(p)
        pin["repositories"]["trustless-ai/recompute-kit"] = "0" * 40; p.write_bytes(encode(pin))
        with patch.object(source, "SOURCE_PIN_SHA256", raw_digest(encode(pin))):
            with self.assertRaisesRegex(source.SourceUnavailable, "SOURCE_COMMIT"):
                source.verify_source(self.root)

    def test_unknown_snapshot_unsupported(self):
        value = self.fixture(1)["cases"][0]["inputs"]; value["producer_commit"] = "0" * 40
        with self.assertRaises(source.SourceUnavailable):
            self.relations.resolve(relation.PROFILE_ID, "0", relation.RELATION_ID).validate(relation.RELATION_ID, value)

    def test_profile_resolution(self):
        profile = self.relations.resolve(relation.PROFILE_ID, "0", relation.RELATION_ID)
        self.assertEqual(profile.version, "0")

    def test_unknown_version(self):
        p = self.root / "corpora/tsei/fixtures/TSEI-RSI-001.json"; value = load(p); value["relation_profile_version"] = "1"; p.write_bytes(encode(value))
        result = self.run_domain()
        self.assertEqual(result["totals"]["UNSUPPORTED"], 7)
        self.assertEqual(result["admissions"], {})

    def test_slots(self):
        profile = self.relations.resolve(relation.PROFILE_ID, "0", relation.RELATION_ID)
        for n in range(1,8):
            value = self.fixture(n); validate_envelope(value)
            inputs = value["cases"][0]["inputs"]; profile.validate(relation.RELATION_ID, inputs)
            self.assertFalse(set(inputs) & {"proof", "policy", "state", "signature"})
        with self.assertRaises(ValueError): profile.validate(relation.RELATION_ID, {})

    def test_malformed_record(self):
        value = self.fixture(1)["cases"][0]["inputs"]; del value["binding_record"]["effective_commit"]
        from jsonschema import ValidationError
        with self.assertRaises(ValidationError):
            self.relations.resolve(relation.PROFILE_ID, "0", relation.RELATION_ID).validate(relation.RELATION_ID, value)

    def test_transport_not_coerced(self):
        for bad in (1.5, "\u00e9"):
            value = self.fixture(1)["cases"][0]["inputs"]; value["artifact"]["extra"] = bad
            with self.assertRaises(ValueError): relation.validate_inputs(value)

    def test_wrong_serializer_preserves_local_bytes(self):
        a = self.fixture(1)["cases"][0]["inputs"]; b = self.fixture(2)["cases"][0]["inputs"]
        self.assertEqual({k:v for k,v in a.items() if k != "serializer_id"}, {k:v for k,v in b.items() if k != "serializer_id"})
        result = self.run_domain(); _, x = self.observed(1,result); _, y = self.observed(2,result)
        self.assertEqual(x["artifact_serialized_sha256"], y["artifact_serialized_sha256"])
        self.assertTrue(x["local_structure_valid"] and y["local_structure_valid"])

    def test_source_qualification(self):
        _, blobs = source.read_sources(self.root)
        actual = model.produce(blobs["crystal-receipt-encode-json-utf8-lf-v0.ts"], blobs["recompute-kit-encode-json-utf8-lf-v0.vectors.json"],
            (ROOT / "adapters/tsei/encoder.mjs").read_bytes(), encode({"artifact": {"b":1,"a":2}}))
        self.assertEqual(actual["qualified"], 48)
        self.assertEqual(actual["artifact_serialized_sha256"], "81103aa69250ea56e887eaab3cd9bf363d341563f05d0676be389c3e40a72871")

    def test_pinned_record_references_resolve(self):
        pin, blobs = source.read_sources(self.root)
        record = json.loads(blobs["recompute-kit-tsei.frozen-artifact.json"])
        refs = [record["serializer_contract"]["spec"], record["serializer_contract"]["vectors"], record["producer_conformance"]["implementation"]]
        for ref in refs:
            match = next(f for f in pin["files"] if "github.com/"+f["repo"] == ref["repository"] and f["commit"] == ref["revision"] and f["path"] == ref["path"])
            self.assertEqual(match["sha256"], ref["sha256"])

    def test_predictor_independent(self):
        value = self.fixture(1); before = expectation.predict(value)
        with patch.object(model, "evaluate", side_effect=RuntimeError("actual broken")), patch.object(model, "produce", side_effect=RuntimeError("actual broken")):
            self.assertEqual(expectation.predict(value), before)

    def test_predictor_no_file_authority(self):
        value = self.fixture(7); before = expectation.predict(value)
        with patch("builtins.open", side_effect=RuntimeError("no expected channel")), patch.object(Path, "read_bytes", side_effect=RuntimeError("no expected channel")):
            self.assertEqual(expectation.predict(value), before)

    def test_tamper_atomic(self):
        profile = self.expectations.resolve(expectation.EXPECTATION_ID); p = self.root / profile.expectations_path; value = load(p)
        row = next(iter(value["expectations"][-1]["prediction"].values()))
        row["observation"]["outputs"]["authority_validation"]["status"] = "PROVEN"
        p.write_bytes(encode(value)); self.expectations = ExpectationRegistry([replace(profile, expectations_digest=raw_digest(encode(value)))])
        with patch.object(model, "produce", side_effect=RuntimeError("must not execute")):
            result = self.run_domain()
        self.assertEqual(result["admissions"], {})
        self.assertEqual(result["totals"], {"PASS": 0, "FAIL": 0, "INVALID_FIXTURE": 0, "UNSUPPORTED": 7})

    def test_actual_no_expected_access(self):
        inputs = self.fixture(1)["cases"][0]["inputs"]
        (self.root / "profiles/tsei/expectations.v0.json").unlink()
        actual = model.evaluate(self.root, {"inputs": inputs})
        profile = self.relations.resolve(relation.PROFILE_ID, "0", relation.RELATION_ID)
        self.assertEqual(profile.evaluate_relation(relation.RELATION_ID, inputs), actual)

    def test_identifiers_not_truth(self):
        value = self.fixture(2); before = list(expectation.predict(value).values())
        value["id"] = "PROVEN"; value["cases"][0]["case_id"] = "authoritative"
        self.assertEqual(before, list(expectation.predict(value).values()))

    def test_fault_preserves_expectations(self):
        baseline = self.run_domain(); self.normal(baseline)
        adapter = self.adapters.resolve(model.ADAPTER_ID, expectation.EXPECTATION_ID)
        def faulty(request):
            value = adapter.evaluate(request); value["outputs"]["authority_validation"]["status"] = "PROVEN"; return value
        self.adapters = AdapterRegistry([replace(adapter, evaluate=faulty)])
        result = self.run_domain(); self.normal(result)
        self.assertEqual([r["result"]["expected"] for r in baseline["rows"]], [r["result"]["expected"] for r in result["rows"]])
        self.assertEqual(result["totals"]["FAIL"], 7)

    def test_deterministic(self):
        self.assertEqual(encode(self.run_domain()), encode(self.run_domain()))

    def test_static_independence(self):
        text = (ROOT / "profiles/tsei/expectation.py").read_text()
        for term in ("adapters.", "record_verdict(", "produce(", "exec("):
            self.assertNotIn(term, text)
        for path in ("adapters/tsei/model.py", "profiles/tsei/relation.py"):
            self.assertNotIn("expectations.v0.json", (ROOT / path).read_text())

    def test_core_anti_coupling(self):
        for directory in ("runner", "rsi"):
            for path in (ROOT / directory).glob("*.py"):
                text = path.read_text().lower()
                for term in ("tsei", "effective_commit", "registry_contract_commit", "valid_provenance", "crystal", "receiptos", "rvr"):
                    self.assertNotIn(term, text, str(path))

    def test_same_pipeline_three_domains(self):
        from extensions.rvr import complete_composition as previous
        old = execute(ROOT, *previous(ROOT)); new = execute(ROOT, *complete_composition(ROOT)); self.normal(new)
        self.assertEqual(new["totals"], {"PASS": 57, "FAIL": 0, "INVALID_FIXTURE": 0, "UNSUPPORTED": 0})
        old_ids = {r["fixture_id"] for r in old["rows"]}
        self.assertEqual([r for r in new["rows"] if r["fixture_id"] in old_ids], old["rows"])
        for ident in ("crystal-receipt.v0", "rvr.digest-binding.v0", expectation.EXPECTATION_ID):
            self.assertIn(ident, new["admissions"])

    def test_setup_is_vacuous(self):
        from runner.mutation_registry import Mutation, MutationRegistry, MutationTrace, CheckEvent
        m = Mutation("probe", "binding", "decision", lambda c: MutationTrace(True, (CheckEvent("decision", "ERROR", "test"),)), "test")
        self.assertEqual(MutationRegistry([m]).execute({"binding"})["totals"]["VACUOUS"], 1)

    def test_binding_shape_vectors(self):
        _, blobs = source.read_sources(self.root)
        vectors = json.loads(blobs["recompute-kit-binding-record.vectors.json"])
        cases = vectors["cases"]
        self.assertEqual(len(cases), 15)
        for case in cases:
            self.assertEqual(model.record_verdict(blobs, case["record"]), case["expected_verdict"])

    def test_schema_valid_record_is_not_pinned_binding(self):
        value = self.fixture(1)["cases"][0]["inputs"]
        value["binding_record"]["binding_subject"] = "other.valid-schema"
        value["source_class"] = "AUTHORITATIVE"
        out = model.evaluate(self.root, {"inputs":value})["outputs"]
        self.assertTrue(out["local_structure_valid"])
        self.assertFalse(out["serializer_binding"])
        self.assertFalse(out["claim_admissible"])
        self.assertEqual(out["authority_validation"]["status"], "UNSUPPORTED")

    def test_protected_prior_files(self):
        baseline = load(ROOT / "research/tsei-serializer-adoption-source-map-v0.json")["protected_hashes"]
        self.assertEqual(mismatches(ROOT,baseline),[])
