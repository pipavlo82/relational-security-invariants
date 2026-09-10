"""Real-domain mapped mutations; setup/source errors are VACUOUS."""
import argparse
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from rsi.codec import encode,load
from runner.mutation_registry import Mutation,MutationTrace,CheckEvent,MutationRegistry
from tools.prove_expectations_can_fail import copy_repo,track_phases,ExecutionResult
DEFINITIONS = (('PQ-M1', 'adapters/pq/model.py', 'policy = admit(inputs["bindings"], inputs["consumer_cutoff"], anchored_artifact)  # PQ-M1', 'policy = admit(inputs["bindings"], inputs["consumer_cutoff"], anchored_artifact)\n    if (anchored_artifact.get("pq_companion") or {}).get("valid"): policy["decision"] = "ADMIT"', 'test_old_key_after_cutoff'), ('PQ-M2', 'adapters/pq/model.py', 'evaluation_artifact = deepcopy(inputs["artifact"])  # PQ-M2', 'evaluation_artifact = deepcopy(inputs["artifact"])\n    evaluation_artifact["anchor_time"] = inputs["current_asof"]', 'test_historical_anchor'), ('PQ-M3', 'adapters/pq/model.py', 'anchored_artifact = evaluation_artifact  # PQ-M3', 'anchored_artifact = deepcopy(evaluation_artifact)\n    if anchored_artifact.get("created_at", inputs["consumer_cutoff"]) < inputs["consumer_cutoff"]: anchored_artifact["anchored"] = True', 'test_signing_not_anchor'), ('PQ-M4', 'adapters/pq/model.py', 'snapshot_matches = inputs["snapshot_key"] == policy["resolved_pq_pubkey"]  # PQ-M4', 'snapshot_matches = True', 'test_stale_snapshot'), ('PQ-M5', 'adapters/pq/model.py', 'crypto = {"status": "UNSUPPORTED", "reason": "offline_source_defers_signature_verification"}  # PQ-M5', 'crypto = {"status": "VERIFIED" if policy["decision"] == "ADMIT" else "UNSUPPORTED", "reason": "offline_source_defers_signature_verification"}', 'test_no_crypto_promotion'), ('PQ-M6', 'adapters/pq/model.py', 'admissible = policy["decision"] == "ADMIT" and snapshot_matches and history_matches if inputs["claim"] == "policy_eligibility" else False  # PQ-M6', 'admissible = policy["decision"] == "ADMIT" and snapshot_matches and history_matches if inputs["claim"] == "policy_eligibility" else metadata["predecessor_present"] and metadata["signature_fields_present"]', 'test_metadata_not_authentication'), ('PQ-M7', 'adapters/pq/model.py', 'artifact_algorithm = rotation["statement"]["algorithm"]  # PQ-M7', 'artifact_algorithm = inputs["reported_algorithm"]', 'test_algorithm_label'))

def child(output):
    suite=unittest.defaultTestLoader.loadTestsFromName("tests.test_pq.PQTests")
    track_phases(suite);result=ExecutionResult();suite.run(result)
    output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(encode({"rows":result.rows,"tests_run":result.testsRun}))
    return 0 if result.wasSuccessful() else 1

def exercise(definition):
    with tempfile.TemporaryDirectory(prefix="pq-mutant-") as temp:
        root=Path(temp)/"repo";copy_repo(root)
        ident,file,old,new,mapped=definition;path=root/file;source=path.read_text()
        if source.count(old)!=1:return MutationTrace(False)
        path.write_text(source.replace(old,new,1),newline="\n")
        output=root/"artifacts/pq-child.json"
        p=subprocess.run([sys.executable,"-B","tools/prove_pq_can_fail.py","--child",str(output)],cwd=root,capture_output=True,timeout=180)
        if p.returncode not in (0,1) or not output.exists():return MutationTrace(True,errors=("CHILD_SETUP",))
        return MutationTrace(True,tuple(CheckEvent(r["id"],r["status"],r.get("phase","test")) for r in load(output)["rows"]))

def registry():
    return MutationRegistry(Mutation(d[0],"pq.policy-asof.v0","tests.test_pq.PQTests."+d[4],lambda context,d=d:exercise(d),"test") for d in DEFINITIONS)

def main():
    p=argparse.ArgumentParser();p.add_argument("--child",type=Path);p.add_argument("--output",type=Path,default=ROOT/"artifacts/pq-mutations.json");args=p.parse_args()
    if args.child:return child(args.child)
    if child(ROOT/"artifacts/pq-mutation-baseline.json"):raise SystemExit("PQ baseline failed")
    result=registry().execute({"pq.policy-asof.v0"});args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(encode(result));print(result["totals"])
    return 0 if result["totals"]["KILLED"]==7 else 1
if __name__=="__main__":raise SystemExit(main())
