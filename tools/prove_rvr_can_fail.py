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
DEFINITIONS = (('RVR-M1', 'adapters/rvr/model.py', 'transition = transition_fn(inputs["transition"])  # RVR-M1', 'transition = transition_fn(inputs["transition"])\n    transition["transition_status"] = "permitted"\n    transition["effective_profile_commitment"] = transition["new_profile_commitment"]', 'test_unbound_substitution'), ('RVR-M2', 'adapters/rvr/model.py', 'substantive = "not_evaluated"  # RVR-M2', 'substantive = "resolved" if transition["effective_profile_commitment"] == transition["prior_profile_commitment"] else "not_evaluated"', 'test_no_amendment'), ('RVR-M3', 'adapters/rvr/model.py', 'verdict = verdict_fn(value)  # RVR-M3', 'verdict = verdict_fn(value)\n        verdict["resolution_status"] = "bound"\n        verdict["bound_profile_commitment"] = transition["effective_profile_commitment"]', 'test_wrong_verdict'), ('RVR-M4', 'adapters/rvr/model.py', 'layers = {"transition": transition, "verdict_binding": verdict}  # RVR-M4', 'layers = {"transition": transition, "verdict_binding": verdict}\n    if verdict is not None and transition["transition_status"] == "unresolved":\n        verdict["resolution_status"] = "unresolved"', 'test_layer_separation'), ('RVR-M5', 'adapters/rvr/model.py', 'crypto = {"status": "UNSUPPORTED", "reason": "no_pinned_signature_verification_lane"}  # RVR-M5', 'crypto = {"status": "VERIFIED" if transition["transition_status"] == "permitted" else "UNSUPPORTED", "reason": "no_pinned_signature_verification_lane"}', 'test_no_crypto_promotion'), ('RVR-M6', 'adapters/rvr/model.py', 'admissible = digest_bound if claim == "digest_binding" else False  # RVR-M6', 'admissible = digest_bound if claim == "digest_binding" else all(a.get("pubkey") for a in inputs["transition"].get("authorizations", {}).values())', 'test_pubkeys_not_authentication'))

def child(output):
    suite=unittest.defaultTestLoader.loadTestsFromName("tests.test_rvr.RVRTests")
    track_phases(suite);result=ExecutionResult();suite.run(result)
    output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(encode({"rows":result.rows,"tests_run":result.testsRun}))
    return 0 if result.wasSuccessful() else 1

def exercise(definition):
    with tempfile.TemporaryDirectory(prefix="rvr-mutant-") as temp:
        root=Path(temp)/"repo";copy_repo(root)
        ident,file,old,new,mapped=definition;path=root/file;source=path.read_text()
        if source.count(old)!=1:return MutationTrace(False)
        path.write_text(source.replace(old,new,1),newline="\n")
        output=root/"artifacts/rvr-child.json"
        p=subprocess.run([sys.executable,"-B","tools/prove_rvr_can_fail.py","--child",str(output)],cwd=root,capture_output=True,timeout=120)
        if p.returncode not in (0,1) or not output.exists():return MutationTrace(True,errors=("CHILD_SETUP",))
        return MutationTrace(True,tuple(CheckEvent(r["id"],r["status"],r.get("phase","test")) for r in load(output)["rows"]))

def registry():
    return MutationRegistry(Mutation(d[0],"rvr.digest-binding.v0","tests.test_rvr.RVRTests."+d[4],lambda context,d=d:exercise(d),"test") for d in DEFINITIONS)

def main():
    p=argparse.ArgumentParser();p.add_argument("--child",type=Path);p.add_argument("--output",type=Path,default=ROOT/"artifacts/rvr-mutations.json");args=p.parse_args()
    if args.child:return child(args.child)
    if child(ROOT/"artifacts/rvr-mutation-baseline.json"):raise SystemExit("RVR baseline failed")
    result=registry().execute({"rvr.digest-binding.v0"});args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(encode(result));print(result["totals"])
    return 0 if result["totals"]["KILLED"]==6 else 1
if __name__=="__main__":raise SystemExit(main())
