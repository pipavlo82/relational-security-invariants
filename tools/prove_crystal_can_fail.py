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
DEFINITIONS=(
("CR-M1","profiles/crystal_receipt/relation.py",'same = value["baseline"] == value["candidate"]  # CR-M1','same = True  # CR-M1',"test_negative"),
("CR-M2","adapters/crystal_receipt/model.py",'return observed(value)  # mapped relation decision','result=observed(value)\n    if request["inputs"]["baseline"]["manifest"] != request["inputs"]["candidate"]["manifest"]:\n        result["relation_state"]="canonical_snapshots_differ"\n        result["outputs"]["semantic_identity_preserved"]=False\n    return result',"test_mirror"),
("CR-M3","adapters/crystal_receipt/model.py",'return observed(value)  # mapped relation decision','result=observed(value)\n    result["relation_state"]="semantic_snapshots_match"\n    result["outputs"]["semantic_identity_preserved"]=True\n    return result',"test_negative"))

def child(output):
    suite=unittest.defaultTestLoader.loadTestsFromName("tests.test_crystal_receipt.CrystalTests")
    track_phases(suite);result=ExecutionResult();suite.run(result)
    output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(encode({"rows":result.rows,"tests_run":result.testsRun}))
    return 0 if result.wasSuccessful() else 1

def exercise(definition):
    with tempfile.TemporaryDirectory(prefix="crystal-mutant-") as temp:
        root=Path(temp)/"repo";copy_repo(root)
        ident,file,old,new,mapped=definition;path=root/file;source=path.read_text()
        if source.count(old)!=1:return MutationTrace(False)
        path.write_text(source.replace(old,new,1),newline="\n")
        output=root/"artifacts/crystal-child.json"
        p=subprocess.run([sys.executable,"-B","tools/prove_crystal_can_fail.py","--child",str(output)],cwd=root,capture_output=True,timeout=120)
        if p.returncode not in (0,1) or not output.exists():return MutationTrace(True,errors=("CHILD_SETUP",))
        return MutationTrace(True,tuple(CheckEvent(r["id"],r["status"],r.get("phase","test")) for r in load(output)["rows"]))

def registry():
    return MutationRegistry(Mutation(d[0],"crystal-receipt.v0","tests.test_crystal_receipt.CrystalTests."+d[4],lambda context,d=d:exercise(d),"test") for d in DEFINITIONS)

def main():
    p=argparse.ArgumentParser();p.add_argument("--child",type=Path);p.add_argument("--output",type=Path,default=ROOT/"artifacts/crystal-mutations.json");args=p.parse_args()
    if args.child:return child(args.child)
    if child(ROOT/"artifacts/crystal-mutation-baseline.json"):raise SystemExit("Crystal baseline failed")
    result=registry().execute({"crystal-receipt.v0"});args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(encode(result));print(result["totals"])
    return 0 if result["totals"]["KILLED"]==3 else 1
if __name__=="__main__":raise SystemExit(main())
