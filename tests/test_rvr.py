"""Source-backed digest binding through the unchanged generic pipeline."""
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
from extensions.rvr import composition, complete_composition
from profiles.rvr import source, relation, expectation
from adapters.rvr import model

ROOT = Path(__file__).resolve().parents[1]


class RVRTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="rvr-test-")
        self.root = Path(self.tmp.name)
        for path in ("evidence/rvr", "profiles/rvr", "corpora/rvr"):
            shutil.copytree(ROOT / path, self.root / path, ignore=shutil.ignore_patterns("__pycache__"))
        (self.root / "extensions").mkdir()
        shutil.copy2(ROOT / "extensions/rvr.corpus.v0.json", self.root / "extensions/rvr.corpus.v0.json")
        self.fixtures, self.expectations, self.adapters, self.relations = composition(self.root)

    def tearDown(self):
        self.tmp.cleanup()

    def run_domain(self):
        return execute(self.root, self.fixtures, self.expectations, self.adapters, self.relations)

    def fixture(self, ident):
        return load(self.root / ("corpora/rvr/fixtures/" + ident + ".json"))

    def normal(self, result):
        # ERROR, not AssertionError: setup/source/admission faults are VACUOUS.
        if not result["admissions"] or any(r.get("diagnostic_kind") or r.get("result", {}).get("errors") for r in result["rows"]):
            raise RuntimeError("mapped relation decision did not execute normally")

    def observed(self, result, key):
        self.normal(result)
        return next(r["result"] for r in result["rows"] if r["result"]["key"] == key)

    def test_pipeline(self):
        result = self.run_domain(); self.normal(result)
        self.assertEqual(result["totals"], {"PASS": 10, "FAIL": 0, "INVALID_FIXTURE": 0, "UNSUPPORTED": 0})

    def test_no_amendment(self):
        row = self.observed(self.run_domain(), "RVR-RSI-001/no_amendment")
        out = row["observed"]["outputs"]; t = out["transition"]
        self.assertEqual(t["effective_profile_commitment"], t["prior_profile_commitment"])
        self.assertEqual(t["transition_status"], "unresolved")
        self.assertEqual(out["substantive_resolution"], "not_evaluated")
        self.assertFalse(out["claim_admissible"])
        self.assertEqual(row["status"], "PASS")

    def test_unbound_substitution(self):
        result = self.run_domain()
        for key in ("unbound_substitution", "wrong_party_digest"):
            row = self.observed(result, "RVR-RSI-002/" + key); t = row["observed"]["outputs"]["transition"]
            self.assertNotEqual(t["prior_profile_commitment"], t["new_profile_commitment"])
            self.assertEqual(t["effective_profile_commitment"], t["prior_profile_commitment"])
            self.assertEqual(t["transition_status"], "unresolved")
            self.assertEqual(row["status"], "PASS")

    def test_bilateral_binding(self):
        row = self.observed(self.run_domain(), "RVR-RSI-003/bilateral_binding"); out = row["observed"]["outputs"]
        self.assertEqual(out["transition"]["transition_status"], "permitted")
        self.assertEqual(out["transition"]["effective_profile_commitment"], out["transition"]["new_profile_commitment"])
        self.assertEqual(out["crypto_authentication"]["status"], "UNSUPPORTED")
        self.assertEqual(row["status"], "PASS")

    def test_correct_verdict(self):
        row = self.observed(self.run_domain(), "RVR-RSI-004/correct_verdict"); out = row["observed"]["outputs"]
        self.assertEqual(out["verdict_binding"]["resolution_status"], "bound")
        self.assertEqual(out["verdict_binding"]["bound_profile_commitment"], out["transition"]["effective_profile_commitment"])
        self.assertEqual(out["substantive_resolution"], "not_evaluated")
        self.assertEqual(row["status"], "PASS")

    def test_wrong_verdict(self):
        row = self.observed(self.run_domain(), "RVR-RSI-005/stale_profile_locally_digest_bound"); out = row["observed"]["outputs"]
        self.assertEqual(out["transition"]["transition_status"], "permitted")
        self.assertEqual(out["verdict_binding"]["resolution_status"], "unresolved")
        self.assertIsNone(out["verdict_binding"]["bound_profile_commitment"])
        self.assertFalse(out["claim_admissible"])
        self.assertEqual(row["status"], "PASS")

    def test_layer_separation(self):
        row = self.observed(self.run_domain(), "RVR-RSI-001/retained_profile_bound_verdict"); out = row["observed"]["outputs"]
        self.assertEqual(out["transition"]["transition_status"], "unresolved")
        self.assertEqual(out["verdict_binding"]["resolution_status"], "bound")
        self.assertEqual(out["substantive_resolution"], "not_evaluated")
        self.assertEqual(row["status"], "PASS")

    def test_no_crypto_promotion(self):
        row = self.observed(self.run_domain(), "RVR-RSI-006/no_crypto_promotion"); out = row["observed"]["outputs"]
        self.assertEqual(out["transition"]["transition_status"], "permitted")
        self.assertEqual(out["verdict_binding"]["resolution_status"], "bound")
        self.assertEqual(out["crypto_authentication"], {"status": "UNSUPPORTED", "reason": "no_pinned_signature_verification_lane"})
        self.assertFalse(out["claim_admissible"])
        self.assertEqual(row["status"], "PASS")

    def test_pubkeys_not_authentication(self):
        inputs = self.fixture("RVR-RSI-006")["cases"][0]["inputs"]
        self.assertTrue(all(a["pubkey"] for a in inputs["transition"]["authorizations"].values()))
        row = self.observed(self.run_domain(), "RVR-RSI-006/no_crypto_promotion")
        self.assertFalse(row["observed"]["outputs"]["claim_admissible"])

    def test_signed_digest_not_authentication(self):
        inputs = self.fixture("RVR-RSI-006")["cases"][0]["inputs"]
        row = self.observed(self.run_domain(), "RVR-RSI-006/no_crypto_promotion"); out = row["observed"]["outputs"]
        for a in inputs["transition"]["authorizations"].values():
            self.assertEqual(a["signed_digest"], out["transition"]["amendment_cc"])
        self.assertEqual(out["crypto_authentication"]["status"], "UNSUPPORTED")

    def test_permitted_label_not_authority(self):
        value = self.fixture("RVR-RSI-002"); before = list(expectation.predict(value).values())
        value["id"] = "permitted"; value["cases"][0]["case_id"] = "cryptographically-authorized"
        self.assertEqual(list(expectation.predict(value).values()), before)
        t, _ = model.reference_functions(self.root)
        task = deepcopy(value["cases"][0]["inputs"]["transition"]); task["name"] = "permitted"
        task["expect"] = {"transition_status": "permitted"}
        self.assertEqual(t(task)["transition_status"], "unresolved")

    def test_source_pin(self):
        pin = source.verify_source(self.root)
        self.assertEqual(pin["commit"], source.SOURCE_COMMIT)
        self.assertEqual(next(f["sha256"] for f in pin["files"] if f["path"].endswith("amendment_gate.py")), "1ea58b0e847b41244d925aae541cca7a113814eb62888d67eef6a2a4dc0c80f7")

    def test_source_digest_mismatch(self):
        p = self.root / "evidence/rvr/amendment_gate.py"; p.write_bytes(p.read_bytes() + b"\n")
        result = self.run_domain()
        self.assertEqual(result["totals"], {"PASS": 0, "FAIL": 0, "INVALID_FIXTURE": 0, "UNSUPPORTED": 6})
        self.assertEqual(result["admissions"], {})

    def test_wrong_commit(self):
        p = self.root / source.SOURCE_PIN_PATH; value = load(p); value["commit"] = "0" * 40; p.write_bytes(encode(value))
        with patch.object(source, "SOURCE_PIN_SHA256", raw_digest(encode(value))):
            with self.assertRaisesRegex(source.SourceUnavailable, "SOURCE_COMMIT"):
                source.verify_source(self.root)

    def test_current_companion_recorded(self):
        evidence = load(ROOT / "research/rvr-digest-binding-source-map-v0.json")
        self.assertEqual(evidence["companion_delta"]["current_commit"], "f5f36778e7cbf6c26fd61a7d66b70b9108447746")
        self.assertEqual(evidence["companion_delta"]["file_byte_diff"], 0)

    def test_profile_resolution(self):
        self.assertEqual(self.relations.resolve(relation.PROFILE_ID, "0", relation.RELATION_ID).profile_id, relation.PROFILE_ID)

    def test_unknown_version(self):
        p = self.root / "corpora/rvr/fixtures/RVR-RSI-001.json"; value = load(p); value["relation_profile_version"] = "1"; p.write_bytes(encode(value))
        result = self.run_domain(); self.assertEqual(result["totals"]["UNSUPPORTED"], 6)
        self.assertEqual(result["admissions"], {})

    def test_missing_slot(self):
        profile = self.relations.resolve(relation.PROFILE_ID, "0", relation.RELATION_ID)
        with self.assertRaises(ValueError):
            profile.validate(relation.RELATION_ID, {})

    def test_malformed_local_inputs(self):
        value = self.fixture("RVR-RSI-002")["cases"][0]["inputs"]; value["transition"]["in_force_profile"] = []
        with self.assertRaises(ValueError):
            relation.validate_inputs(value)

    def test_transport_not_coerced(self):
        for bad in (1.5, "\u00e9"):
            value = self.fixture("RVR-RSI-003")["cases"][0]["inputs"]; value["transition"]["in_force_profile"]["extra"] = bad
            with self.assertRaises(ValueError): relation.validate_inputs(value)

    def test_no_universal_fake_fields(self):
        for path in (self.root / "corpora/rvr/fixtures").glob("*.json"):
            value = load(path); validate_envelope(value)
            for case in value["cases"]:
                self.assertFalse(set(case["inputs"]) & {"proof", "policy", "state", "signature"})
                relation.validate_inputs(case["inputs"])

    def test_negative_preserves_local_digest(self):
        value = self.fixture("RVR-RSI-005")["cases"][0]["inputs"]
        relation.validate_inputs(value)
        self.assertEqual(expectation.commitment(value["verdict"]["verdict_core"]), value["verdict"]["resolver_sig"]["signed_digest"])
        self.assertEqual(value["verdict"]["verdict_core"]["effective_profile_commitment"], expectation.commitment(value["transition"]["in_force_profile"]))

    def test_source_vector_derivation(self):
        t, v = model.reference_functions(self.root)
        for vector in json.loads((self.root / "evidence/rvr/profile-amendment-v0.vectors.json").read_bytes())["vectors"]:
            actual = t(deepcopy(vector))
            predicted = expectation.derive({"transition": vector}, relation.RELATION_ID)["outputs"]["transition"]
            self.assertEqual(actual, vector["expect"])
            self.assertEqual(predicted, vector["expect"])
        task = self.fixture("RVR-RSI-003")["cases"][0]["inputs"]["transition"]
        for vector in json.loads((self.root / "evidence/rvr/verdict-profile-binding-v0.vectors.json").read_bytes())["vectors"]:
            actual = v(deepcopy(vector))
            predicted = expectation.derive({"transition": task, "verdict": vector}, relation.RELATION_ID)["outputs"]["verdict_binding"]
            self.assertEqual(actual, vector["expect"])
            self.assertEqual(predicted, vector["expect"])

    def test_predictor_independent(self):
        value = self.fixture("RVR-RSI-003"); before = expectation.predict(value)
        with patch.object(model, "reference_functions", side_effect=RuntimeError("actual broken")), patch.object(model, "evaluate", side_effect=RuntimeError("actual broken")):
            self.assertEqual(expectation.predict(value), before)

    def test_predictor_no_file_authority(self):
        value = self.fixture("RVR-RSI-006"); before = expectation.predict(value)
        with patch("builtins.open", side_effect=RuntimeError("no file channel")), patch.object(Path, "read_bytes", side_effect=RuntimeError("no artifact channel")):
            self.assertEqual(expectation.predict(value), before)

    def test_tamper_atomic(self):
        profile = self.expectations.resolve(expectation.EXPECTATION_ID); p = self.root / profile.expectations_path; artifact = load(p)
        row = next(iter(artifact["expectations"][-1]["prediction"].values()))
        row["observation"]["outputs"]["crypto_authentication"]["status"] = "VERIFIED"
        p.write_bytes(encode(artifact)); self.expectations = ExpectationRegistry([replace(profile, expectations_digest=raw_digest(encode(artifact)))])
        with patch.object(model, "reference_functions", side_effect=RuntimeError("must not execute")):
            result = self.run_domain()
        self.assertEqual(result["admissions"], {})
        self.assertEqual(result["totals"], {"PASS": 0, "FAIL": 0, "INVALID_FIXTURE": 0, "UNSUPPORTED": 6})

    def test_actual_no_expectation_access(self):
        value = self.fixture("RVR-RSI-003")["cases"][0]["inputs"]
        (self.root / "profiles/rvr/expectations.v0.json").unlink()
        actual = model.evaluate(self.root, {"inputs": value})
        profile = self.relations.resolve(relation.PROFILE_ID, "0", relation.RELATION_ID)
        self.assertEqual(actual, profile.evaluate_relation(relation.RELATION_ID, value))

    def test_captured_pinned_bytes_executed(self):
        original = model.read_sources
        def captured(root):
            result = original(root)
            (Path(root) / "evidence/rvr/amendment_gate.py").write_bytes(b"not executable")
            return result
        inputs = self.fixture("RVR-RSI-003")["cases"][0]["inputs"]
        with patch.object(model, "read_sources", side_effect=captured):
            self.assertEqual(model.evaluate(self.root, {"inputs": inputs})["outputs"]["transition"]["transition_status"], "permitted")

    def test_fault_does_not_change_expectation(self):
        baseline = self.run_domain(); self.normal(baseline)
        adapter = self.adapters.resolve(model.ADAPTER_ID, expectation.EXPECTATION_ID)
        def faulty(request):
            result = adapter.evaluate(request); result["outputs"]["crypto_authentication"]["status"] = "VERIFIED"; return result
        self.adapters = AdapterRegistry([replace(adapter, evaluate=faulty)])
        result = self.run_domain(); self.normal(result)
        self.assertEqual([r["result"]["expected"] for r in baseline["rows"]], [r["result"]["expected"] for r in result["rows"]])
        self.assertEqual(result["totals"]["FAIL"], 10)

    def test_deterministic(self):
        self.assertEqual(encode(self.run_domain()), encode(self.run_domain()))

    def test_static_independence(self):
        text = (ROOT / "profiles/rvr/expectation.py").read_text()
        for forbidden in ("adapters.", "reference_functions", "exec("):
            self.assertNotIn(forbidden, text)
        for path in ("adapters/rvr/model.py", "profiles/rvr/relation.py"):
            self.assertNotIn("expectations.v0.json", (ROOT / path).read_text())

    def test_generic_hashes_and_legacy_bytes(self):
        pins = load(ROOT / "research/rvr-digest-binding-source-map-v0.json")["protected_hashes"]
        self.assertEqual(mismatches(ROOT,pins),[])

    def test_core_anti_coupling(self):
        for directory in ("runner", "rsi"):
            for path in (ROOT / directory).glob("*.py"):
                text = path.read_text().lower()
                for term in ("rvr", "8309", "signed_digest", "amendment_cc", "crystal", "receiptos"):
                    self.assertNotIn(term, text, str(path))

    def test_same_generic_pipeline_two_domains(self):
        from extensions.crystal_receipt import complete_composition as previous
        old = execute(ROOT, *previous(ROOT)); new = execute(ROOT, *complete_composition(ROOT))
        self.normal(new)
        self.assertEqual(new["totals"], {"PASS": 50, "FAIL": 0, "INVALID_FIXTURE": 0, "UNSUPPORTED": 0})
        self.assertEqual([r for r in new["rows"] if not r["fixture_id"].startswith("rvr:")], old["rows"])
        self.assertIn("crystal-receipt.v0", new["admissions"])
        self.assertIn(expectation.EXPECTATION_ID, new["admissions"])

    def test_source_failure_vacuous(self):
        from runner.mutation_registry import Mutation, MutationRegistry, MutationTrace, CheckEvent
        m = Mutation("probe", "binding", "decision", lambda c: MutationTrace(True, (CheckEvent("decision", "ERROR", "test"),)), "test")
        self.assertEqual(MutationRegistry([m]).execute({"binding"})["totals"]["VACUOUS"], 1)
