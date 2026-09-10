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
DEFINITIONS = (('CE-M1', 'adapters/consult_escrow/model.py', "variant='canonical'  # CE-M1 CE-M5 CE-M8", "variant='job'", 'test_wrong_job'), ('CE-M5', 'adapters/consult_escrow/model.py', "variant='canonical'  # CE-M1 CE-M5 CE-M8", "variant='signature'", 'test_wrong_attestor'), ('CE-M6', 'adapters/consult_escrow/model.py', "occurrence=actual['execution_occurrence']  # CE-M6", "occurrence='LOCAL_EVM' if actual['release_eligible'] else 'UNSUPPORTED'", 'test_no_execution_promotion'), ('CE-M7', 'adapters/consult_escrow/model.py', 'mirror=actual  # CE-M7', "mirror=actual\n    if request['inputs']['relayer'].endswith('10d1'): mirror['release_eligible']=False", 'test_mirror'), ('CE-M8', 'adapters/consult_escrow/model.py', "variant='canonical'  # CE-M1 CE-M5 CE-M8", "variant='replay'", 'test_replay'))

def child(output):
    suite=unittest.defaultTestLoader.loadTestsFromName("tests.test_consult_escrow.ConsultEscrowTests")
    track_phases(suite);result=ExecutionResult();suite.run(result)
    output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(encode({"rows":result.rows,"tests_run":result.testsRun}))
    return 0 if result.wasSuccessful() else 1

def exercise(definition):
    with tempfile.TemporaryDirectory(prefix="ce-mutant-") as temp:
        root=Path(temp)/"repo";copy_repo(root)
        ident,file,old,new,mapped=definition;path=root/file;source=path.read_text()
        if source.count(old)!=1:return MutationTrace(False)
        path.write_text(source.replace(old,new,1),newline="\n")
        output=root/"artifacts/ce-child.json"
        p=subprocess.run([sys.executable,"-B","tools/prove_consult_escrow_can_fail.py","--child",str(output)],cwd=root,capture_output=True,timeout=180)
        if p.returncode not in (0,1) or not output.exists():return MutationTrace(True,errors=("CHILD_SETUP",))
        return MutationTrace(True,tuple(CheckEvent(r["id"],r["status"],r.get("phase","test")) for r in load(output)["rows"]))

def registry():
    return MutationRegistry(Mutation(d[0],"consult-escrow.release-binding.v0","tests.test_consult_escrow.ConsultEscrowTests."+d[4],lambda context,d=d:exercise(d),"test") for d in DEFINITIONS)

def main():
    p=argparse.ArgumentParser();p.add_argument("--child",type=Path);p.add_argument("--output",type=Path,default=ROOT/"artifacts/consult-escrow-mutations.json");args=p.parse_args()
    if args.child:return child(args.child)
    if child(ROOT/"artifacts/consult-escrow-mutation-baseline.json"):raise SystemExit("CE baseline failed")
    result=registry().execute({"consult-escrow.release-binding.v0"});args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(encode(result));print(result["totals"])
    return 0 if result["totals"]["KILLED"]==5 else 1
if __name__=="__main__":raise SystemExit(main())
