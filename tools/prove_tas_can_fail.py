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
DEFINITIONS = (('TAS-M1', 'adapters/tas/model.py', 'transported=value  # TAS-M1', "transported=value\n    if transported['accepted'] is not None: transported['current']['workflowAddress']=transported['accepted']['workflowAddress']", 'test_target_substitution'), ('TAS-M3', 'adapters/tas/model.py', 'member_input=accepted  # TAS-M3', "member_input=accepted\n    member_input['member']['agent_id']=member_input['agent_id']", 'test_member_substitution'), ('TAS-M4', 'adapters/tas/model.py', 'accepted=transported  # TAS-M4', "accepted=transported\n    if accepted['accepted'] is None: accepted['accepted']=deepcopy(accepted['current'])", 'test_no_accepted_context'), ('TAS-M5', 'adapters/tas/model.py', "occurrence='UNSUPPORTED'  # TAS-M5", "occurrence='EXECUTED' if actual['dispatched'] is not None else 'UNSUPPORTED'", 'test_no_execution_promotion'), ('TAS-M6', 'adapters/tas/model.py', 'mirror=actual  # TAS-M6', "mirror=actual\n    if value['accepted'] is not None and value['accepted'] != value['current']: mirror={'error':'WORKFLOW_SOURCE_VERIFICATION_REQUIRED','dispatched':None}", 'test_mirror'))

def child(output):
    suite=unittest.defaultTestLoader.loadTestsFromName("tests.test_tas.TASTests")
    track_phases(suite);result=ExecutionResult();suite.run(result)
    output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(encode({"rows":result.rows,"tests_run":result.testsRun}))
    return 0 if result.wasSuccessful() else 1

def exercise(definition):
    with tempfile.TemporaryDirectory(prefix="tas-mutant-") as temp:
        root=Path(temp)/"repo";copy_repo(root)
        ident,file,old,new,mapped=definition;path=root/file;source=path.read_text()
        if source.count(old)!=1:return MutationTrace(False)
        path.write_text(source.replace(old,new,1),newline="\n")
        output=root/"artifacts/tas-child.json"
        p=subprocess.run([sys.executable,"-B","tools/prove_tas_can_fail.py","--child",str(output)],cwd=root,capture_output=True,timeout=180)
        if p.returncode not in (0,1) or not output.exists():return MutationTrace(True,errors=("CHILD_SETUP",))
        return MutationTrace(True,tuple(CheckEvent(r["id"],r["status"],r.get("phase","test")) for r in load(output)["rows"]))

def registry():
    return MutationRegistry(Mutation(d[0],"tas.context-invocation.v0","tests.test_tas.TASTests."+d[4],lambda context,d=d:exercise(d),"test") for d in DEFINITIONS)

def main():
    p=argparse.ArgumentParser();p.add_argument("--child",type=Path);p.add_argument("--output",type=Path,default=ROOT/"artifacts/tas-mutations.json");args=p.parse_args()
    if args.child:return child(args.child)
    if child(ROOT/"artifacts/tas-mutation-baseline.json"):raise SystemExit("TAS baseline failed")
    result=registry().execute({"tas.context-invocation.v0"});args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(encode(result));print(result["totals"])
    return 0 if result["totals"]["KILLED"]==5 else 1
if __name__=="__main__":raise SystemExit(main())
