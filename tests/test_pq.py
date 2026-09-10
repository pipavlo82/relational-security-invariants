"""Conditional PQ policy conformance, never an authentication proof."""
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
from extensions.pq import composition, complete_composition
from profiles.pq import source, relation, expectation
from adapters.pq import model
ROOT = Path(__file__).resolve().parents[1]


class PQTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="pq-test-"); self.root = Path(self.tmp.name)
        for directory in ("evidence/pq", "profiles/pq", "corpora/pq"):
            shutil.copytree(ROOT/directory, self.root/directory, ignore=shutil.ignore_patterns("__pycache__"))
        (self.root/"extensions").mkdir(); shutil.copy2(ROOT/"extensions/pq.corpus.v0.json", self.root/"extensions/pq.corpus.v0.json")
        self.fixtures, self.expectations, self.adapters, self.relations = composition(self.root)

    def tearDown(self): self.tmp.cleanup()

    def fixture(self, n): return load(self.root/("corpora/pq/fixtures/PQ-RSI-%03d.json" % n))

    def run_domain(self): return execute(self.root, self.fixtures, self.expectations, self.adapters, self.relations)

    def normal(self, result):
        if not result["admissions"] or any(r.get("diagnostic_kind") or r.get("result",{}).get("errors") for r in result["rows"]):
            raise RuntimeError("mapped decision not reached normally")

    def observed(self, n, case=None):
        result=self.run_domain(); self.normal(result)
        row=next(r["result"] for r in result["rows"] if r["fixture_source_id"] == "PQ-RSI-%03d" % n and (case is None or r["result"]["key"].endswith("/"+case)))
        return row,row["observed"]["outputs"]

    def test_pipeline(self):
        r=self.run_domain();self.normal(r)
        self.assertEqual(r["totals"],{"PASS":7,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":0})

    def test_before_cutoff(self):
        row,o=self.observed(1)
        self.assertEqual(o["policy"]["resolved"],"kya-l4-genesis")
        self.assertEqual(o["policy"]["rule"],"anchored_before_cutoff")
        self.assertEqual(o["current_binding"]["name"],"kya-l4-genesis")
        self.assertTrue(o["claim_admissible"]);self.assertEqual(row["status"],"PASS")

    def test_old_key_after_cutoff(self):
        row,o=self.observed(2)
        self.assertTrue(self.fixture(2)["cases"][0]["inputs"]["artifact"]["pq_companion"]["valid"])
        self.assertEqual(o["policy"]["resolved"],"kya-l4-rotation-1")
        self.assertEqual(o["policy"]["decision"],"REJECT")
        self.assertFalse(o["claim_admissible"]);self.assertEqual(row["status"],"PASS")

    def test_new_key_after_cutoff(self):
        row,o=self.observed(3)
        self.assertEqual(o["policy"]["resolved"],"kya-l4-rotation-1")
        self.assertEqual(o["policy"]["rule"],"valid_pq_companion")
        self.assertEqual(o["policy"]["decision"],"ADMIT")
        self.assertEqual(o["authenticated_transition_validation"]["status"],"UNSUPPORTED")
        self.assertEqual(row["status"],"PASS")

    def test_historical_anchor(self):
        row,o=self.observed(4,"historical_anchor")
        self.assertEqual(o["current_binding"]["name"],"kya-l4-rotation-1")
        self.assertEqual(o["policy"]["resolved"],"kya-l4-genesis")
        self.assertTrue(o["historical_eligibility"])
        self.assertEqual(o["policy"]["decision"],"ADMIT");self.assertEqual(row["status"],"PASS")

    def test_signing_not_anchor(self):
        row,o=self.observed(4,"created_at_is_not_anchor")
        self.assertEqual(o["policy"]["decision"],"REJECT")
        self.assertFalse(o["historical_eligibility"])
        self.assertFalse(o["claim_admissible"]);self.assertEqual(row["status"],"PASS")

    def test_stale_snapshot(self):
        row,o=self.observed(5)
        self.assertEqual(o["policy"]["decision"],"ADMIT")
        self.assertFalse(o["snapshot_matches"])
        self.assertFalse(o["claim_admissible"]);self.assertEqual(row["status"],"PASS")

    def test_no_crypto_promotion(self):
        row,o=self.observed(7)
        self.assertEqual(o["policy"]["decision"],"ADMIT")
        self.assertEqual(o["authenticated_transition_validation"]["status"],"UNSUPPORTED")
        self.assertFalse(o["claim_admissible"]);self.assertEqual(row["status"],"PASS")

    def test_metadata_not_authentication(self):
        row,o=self.observed(7)
        self.assertTrue(o["transition_metadata"]["predecessor_present"])
        self.assertTrue(o["transition_metadata"]["signature_fields_present"])
        self.assertFalse(o["claim_admissible"]);self.assertEqual(row["status"],"PASS")

    def test_algorithm_label(self):
        row,o=self.observed(7);a=o["algorithm_identity"]
        self.assertEqual(a["artifact_algorithm"],"SLH-DSA-SHA2-192s")
        self.assertEqual(a["reported_label"],"ML-DSA")
        self.assertFalse(a["label_matches_artifact"])
        self.assertEqual(a["algorithm_specific_verification"],"UNSUPPORTED");self.assertEqual(row["status"],"PASS")

    def test_anchor_evidence_not_verified(self):
        _,o=self.observed(4,"historical_anchor")
        self.assertTrue(o["historical_eligibility"])
        self.assertEqual(o["anchor_validation"]["status"],"UNSUPPORTED")

    def test_source_pin(self):
        p=source.verify_source(self.root)
        self.assertEqual(p["commit"],"15f7f59ac47b3358492bd5741143c418b5d657f5")
        self.assertEqual(next(f["sha256"] for f in p["files"] if f["path"].endswith("cutoff_enforce.py")),"a11d528b97bd88b7850a679122e1bbaec162bf98f6164587c23e47f9174df528")

    def test_source_digest_drift(self):
        p=self.root/"evidence/pq/cutoff_enforce.py";p.write_bytes(p.read_bytes()+b"\n")
        r=self.run_domain();self.assertEqual(r["admissions"],{})
        self.assertEqual(r["totals"],{"PASS":0,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":6})

    def test_wrong_source_commit(self):
        p=self.root/source.SOURCE_PIN_PATH;v=load(p);v["commit"]="0"*40;p.write_bytes(encode(v))
        with patch.object(source,"SOURCE_PIN_SHA256",raw_digest(encode(v))):
            with self.assertRaisesRegex(source.SourceUnavailable,"SOURCE_COMMIT"):source.verify_source(self.root)

    def test_source_deferred_labels(self):
        text=(self.root/"evidence/pq/deep_recompute.py").read_text(encoding="utf8")
        self.assertIn('continuity_signature (ML-DSA)',text)
        self.assertIn('pq_companion_signature (ML-DSA)',text)
        rotation=json.loads((self.root/"evidence/pq/pq-key-binding-v0.rotation.json").read_bytes())
        self.assertEqual(rotation["statement"]["algorithm"],"SLH-DSA-SHA2-192s")

    def test_intended_rotation_anchor_recorded(self):
        vectors=json.loads((self.root/"evidence/pq/pq-key-binding-v0.rotation-vectors.json").read_bytes())
        self.assertIn("intended on-chain anchor",vectors["description"])

    def test_source_vector_reproduction(self):
        admit,resolve,rotation,history=model.functions(self.root)
        for name in ("cutoff","rotation","revocation"):
            vectors=json.loads((self.root/("evidence/pq/pq-key-binding-v0."+name+"-vectors.json")).read_bytes())
            # Source revocation adapter is tested directly, independently of registered corpus scope.
            _,blobs=source.read_sources(self.root);scope={"__name__":"source_test"}
            exec(compile(blobs["evidence/pq/cutoff_enforce.py"],"source_test","exec"),scope)
            for c in vectors["cases"]:
                bindings=scope["apply_revocations"](c.get("bindings",vectors["bindings"]),c.get("revocations",vectors.get("revocations",[])))
                cutoff=c.get("consumer_cutoff",vectors["consumer_cutoff"])
                actual=admit(bindings,cutoff,c["artifact"])
                self.assertEqual({k:actual[k] for k in c["expected"]},c["expected"])
                inp={"bindings":bindings,"consumer_cutoff":cutoff,"artifact":c["artifact"],"current_asof":c["artifact"]["anchor_time"],"snapshot_key":actual["resolved_pq_pubkey"],"claim":"policy_eligibility","reported_algorithm":"ML-DSA"}
                self.assertEqual(expectation.derive(inp,relation.RELATION_ID)["outputs"]["policy"],actual)

    def test_profile_exact_version(self):
        self.assertEqual(self.relations.resolve(relation.PROFILE_ID,"0",relation.RELATION_ID).version,"0")
        p=self.root/"corpora/pq/fixtures/PQ-RSI-001.json";v=load(p);v["relation_profile_version"]="1";p.write_bytes(encode(v))
        self.assertEqual(self.run_domain()["totals"]["UNSUPPORTED"],6)

    def test_slots(self):
        for n in (1,2,3,4,5,7):
            f=self.fixture(n);validate_envelope(f)
            for c in f["cases"]:relation.validate_inputs(c["inputs"])
        with self.assertRaises(ValueError):relation.validate_inputs({})

    def test_transport(self):
        for bad in (1.5,"\u00e9"):
            v=self.fixture(1)["cases"][0]["inputs"];v["current_asof"]=bad
            with self.assertRaises(ValueError):relation.validate_inputs(v)

    def test_ambiguous_history_rejected(self):
        v=self.fixture(1)["cases"][0]["inputs"];v["bindings"][1]["binding_anchor_time"]=v["bindings"][0]["binding_anchor_time"]
        with self.assertRaises(ValueError):relation.validate_inputs(v)

    def test_modified_history_not_authority(self):
        v=self.fixture(3)["cases"][0]["inputs"];v["bindings"][0]["secp256k1_pubkey"]="other-subject"
        out=model.evaluate(self.root,{"inputs":v})["outputs"]
        self.assertFalse(out["history_matches_pin"]);self.assertFalse(out["claim_admissible"])
        # This is exact-history identity only, not general subject-signature verification.

    def test_predictor_independent(self):
        f=self.fixture(3);before=expectation.predict(f)
        with patch.object(model,"evaluate",side_effect=RuntimeError("actual broken")),patch.object(model,"functions",side_effect=RuntimeError("actual broken")):
            self.assertEqual(expectation.predict(f),before)

    def test_predictor_no_file_channel(self):
        f=self.fixture(7);before=expectation.predict(f)
        with patch("builtins.open",side_effect=RuntimeError("no row channel")),patch.object(Path,"read_bytes",side_effect=RuntimeError("no row channel")):
            self.assertEqual(expectation.predict(f),before)

    def test_tamper_atomic(self):
        profile=self.expectations.resolve(expectation.EXPECTATION_ID);p=self.root/profile.expectations_path;v=load(p)
        next(iter(v["expectations"][-1]["prediction"].values()))["observation"]["outputs"]["authenticated_transition_validation"]["status"]="VERIFIED"
        p.write_bytes(encode(v));self.expectations=ExpectationRegistry([replace(profile,expectations_digest=raw_digest(encode(v)))])
        with patch.object(model,"functions",side_effect=RuntimeError("must not run")):r=self.run_domain()
        self.assertEqual(r["admissions"],{});self.assertEqual(r["totals"]["UNSUPPORTED"],6)

    def test_actual_no_expectation_access(self):
        v=self.fixture(3)["cases"][0]["inputs"]
        (self.root/"profiles/pq/expectations.v0.json").unlink()
        actual=model.evaluate(self.root,{"inputs":v})
        self.assertEqual(self.relations.resolve(relation.PROFILE_ID,"0",relation.RELATION_ID).evaluate_relation(relation.RELATION_ID,v),actual)

    def test_fault_preserves_expected(self):
        old=self.run_domain();self.normal(old);a=self.adapters.resolve(model.ADAPTER_ID,expectation.EXPECTATION_ID)
        def faulty(request):
            v=a.evaluate(request);v["outputs"]["authenticated_transition_validation"]["status"]="VERIFIED";return v
        self.adapters=AdapterRegistry([replace(a,evaluate=faulty)]);new=self.run_domain();self.normal(new)
        self.assertEqual([r["result"]["expected"] for r in old["rows"]],[r["result"]["expected"] for r in new["rows"]])
        self.assertEqual(new["totals"]["FAIL"],7)

    def test_ids_not_truth(self):
        f=self.fixture(2);before=list(expectation.predict(f).values());f["id"]="authenticated";f["cases"][0]["case_id"]="ADMIT"
        self.assertEqual(list(expectation.predict(f).values()),before)

    def test_deterministic(self):self.assertEqual(encode(self.run_domain()),encode(self.run_domain()))

    def test_static_independence(self):
        text=(ROOT/"profiles/pq/expectation.py").read_text()
        for term in ("adapters.","functions(","exec("):self.assertNotIn(term,text)
        for name in ("adapters/pq/model.py","profiles/pq/relation.py"):
            self.assertNotIn("expectations.v0.json",(ROOT/name).read_text())

    def test_core_anti_coupling(self):
        for directory in ("runner","rsi"):
            for p in (ROOT/directory).glob("*.py"):
                for term in ("pq_pubkey","cutoff","slh-dsa","ml-dsa","tsei","crystal","rvr"):
                    self.assertNotIn(term,p.read_text().lower(),str(p))

    def test_same_pipeline_four_domains(self):
        from extensions.tsei import complete_composition as previous
        old=execute(ROOT,*previous(ROOT));new=execute(ROOT,*complete_composition(ROOT));self.normal(new)
        self.assertEqual(new["totals"],{"PASS":64,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":0})
        ids={r["fixture_id"] for r in old["rows"]}
        self.assertEqual([r for r in new["rows"] if r["fixture_id"] in ids],old["rows"])
        for ident in ("crystal-receipt.v0","rvr.digest-binding.v0","tsei.serializer-adoption.v0",expectation.EXPECTATION_ID):self.assertIn(ident,new["admissions"])

    def test_protected_prior_files(self):
        pins=load(ROOT/"research/pq-policy-asof-source-map-v0.json")["protected_hashes"]
        for p,d in pins.items():self.assertEqual(raw_digest((ROOT/p).read_bytes()),d,p)

    def test_setup_vacuous(self):
        from runner.mutation_registry import Mutation,MutationRegistry,MutationTrace,CheckEvent
        m=Mutation("probe","policy","decision",lambda c:MutationTrace(True,(CheckEvent("decision","ERROR","test"),)),"test")
        self.assertEqual(MutationRegistry([m]).execute({"policy"})["totals"]["VACUOUS"],1)
