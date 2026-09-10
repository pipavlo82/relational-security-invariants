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
DEFINITIONS = (('TSEI-M1', 'adapters/tsei/model.py', 'bound = exact_record and verdict == "valid" and inputs["binding_subject"] == record["binding_subject"] and inputs["serializer_id"] == record["serializer_contract"]["id"]  # TSEI-M1', 'bound = verdict == "valid"', 'test_wrong_serializer'), ('TSEI-M2', 'adapters/tsei/model.py', 'adopted = inputs["producer_commit"] == record["effective_commit"]["commit"]  # TSEI-M2', 'adopted = mechanism', 'test_mechanism_not_adoption'), ('TSEI-M3', 'adapters/tsei/model.py', 'introduced = inputs["registry_commit"] in (chronology["record_introduction"]["commit"], pin["repositories"]["trustless-ai/recompute-kit"])  # TSEI-M3', 'introduced = adopted', 'test_adoption_not_record'), ('TSEI-M4', 'adapters/tsei/model.py', 'covered = bound and adopted and introduced and after_effective  # TSEI-M4', 'covered = bound and adopted and introduced', 'test_nonretroactivity'), ('TSEI-M5', 'adapters/tsei/model.py', 'authority = {"status": "UNSUPPORTED", "reason": REASON}  # TSEI-M5', 'authority = {"status": "PROVEN" if covered else "UNSUPPORTED", "reason": REASON}', 'test_no_authority_promotion'), ('TSEI-M6', 'adapters/tsei/model.py', 'admissible = covered if claim == "serializer_binding" else False  # TSEI-M6', 'admissible = covered if claim == "serializer_binding" else inputs.get("reported_status") == "PROVEN" or inputs.get("reported_provenance") == "VALID_PROVENANCE"', 'test_reported_labels_not_authority'))

def child(output):
    suite=unittest.defaultTestLoader.loadTestsFromName("tests.test_tsei.TSEITests")
    track_phases(suite);result=ExecutionResult();suite.run(result)
    output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(encode({"rows":result.rows,"tests_run":result.testsRun}))
    return 0 if result.wasSuccessful() else 1

def exercise(definition):
    with tempfile.TemporaryDirectory(prefix="tsei-mutant-") as temp:
        root=Path(temp)/"repo";copy_repo(root)
        ident,file,old,new,mapped=definition;path=root/file;source=path.read_text()
        if source.count(old)!=1:return MutationTrace(False)
        path.write_text(source.replace(old,new,1),newline="\n")
        output=root/"artifacts/tsei-child.json"
        p=subprocess.run([sys.executable,"-B","tools/prove_tsei_can_fail.py","--child",str(output)],cwd=root,capture_output=True,timeout=180)
        if p.returncode not in (0,1) or not output.exists():return MutationTrace(True,errors=("CHILD_SETUP",))
        return MutationTrace(True,tuple(CheckEvent(r["id"],r["status"],r.get("phase","test")) for r in load(output)["rows"]))

def registry():
    return MutationRegistry(Mutation(d[0],"tsei.serializer-adoption.v0","tests.test_tsei.TSEITests."+d[4],lambda context,d=d:exercise(d),"test") for d in DEFINITIONS)

def main():
    p=argparse.ArgumentParser();p.add_argument("--child",type=Path);p.add_argument("--output",type=Path,default=ROOT/"artifacts/tsei-mutations.json");args=p.parse_args()
    if args.child:return child(args.child)
    if child(ROOT/"artifacts/tsei-mutation-baseline.json"):raise SystemExit("TSEI baseline failed")
    result=registry().execute({"tsei.serializer-adoption.v0"});args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(encode(result));print(result["totals"])
    return 0 if result["totals"]["KILLED"]==6 else 1
if __name__=="__main__":raise SystemExit(main())
