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
DEFINITIONS = (('VL-M1', 'adapters/verify_layer/model.py', "bound=actual['boundToHeader']  # VL-M1", "bound=True\n    actual['verified']=actual['claimMatchesProof']", 'test_wrong_root'), ('VL-M2', 'adapters/verify_layer/model.py', "header=actual['headerAuthority']  # VL-M2", "header='SUPPORTED' if actual['verified'] else 'UNSUPPORTED'", 'test_no_header_promotion'), ('VL-M5', 'adapters/verify_layer/model.py', "variant='canonical'  # VL-M5", "variant='address'", 'test_wrong_account'), ('VL-M6', 'adapters/verify_layer/model.py', "downstream=actual['downstreamAuthority']  # VL-M6", "downstream='SUPPORTED' if actual['verified'] else 'UNSUPPORTED'", 'test_no_downstream_promotion'), ('VL-M7', 'adapters/verify_layer/model.py', 'mirror=actual  # VL-M7', "mirror=actual\n    if any(x[2:]!=x[2:].lower() for x in request['inputs']['response']['accountProof']):mirror['verified']=False", 'test_mirror'), ('VL-M9', 'adapters/verify_layer/model.py', "claim=actual['claimMatchesProof']  # VL-M9", "claim=True\n    actual['verified']=actual['boundToHeader']", 'test_wrong_claim'))

def child(output):
    suite=unittest.defaultTestLoader.loadTestsFromName("tests.test_verify_layer.VerifyLayerTests")
    track_phases(suite);result=ExecutionResult();suite.run(result)
    output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(encode({"rows":result.rows,"tests_run":result.testsRun}))
    return 0 if result.wasSuccessful() else 1

def exercise(definition):
    with tempfile.TemporaryDirectory(prefix="vl-mutant-") as temp:
        root=Path(temp)/"repo";copy_repo(root)
        ident,file,old,new,mapped=definition;path=root/file;source=path.read_text()
        if source.count(old)!=1:return MutationTrace(False)
        path.write_text(source.replace(old,new,1),newline="\n")
        output=root/"artifacts/vl-child.json"
        p=subprocess.run([sys.executable,"-B","tools/prove_verify_layer_can_fail.py","--child",str(output)],cwd=root,capture_output=True,timeout=180)
        if p.returncode not in (0,1) or not output.exists():return MutationTrace(True,errors=("CHILD_SETUP",))
        return MutationTrace(True,tuple(CheckEvent(r["id"],r["status"],r.get("phase","test")) for r in load(output)["rows"]))

def registry():
    return MutationRegistry(Mutation(d[0],"verify-layer.proof-context.v0","tests.test_verify_layer.VerifyLayerTests."+d[4],lambda context,d=d:exercise(d),"test") for d in DEFINITIONS)

def main():
    p=argparse.ArgumentParser();p.add_argument("--child",type=Path);p.add_argument("--output",type=Path,default=ROOT/"artifacts/verify-layer-mutations.json");args=p.parse_args()
    if args.child:return child(args.child)
    if child(ROOT/"artifacts/verify-layer-mutation-baseline.json"):raise SystemExit("VL baseline failed")
    result=registry().execute({"verify-layer.proof-context.v0"});args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(encode(result));print(result["totals"])
    return 0 if result["totals"]["KILLED"]==6 else 1
if __name__=="__main__":raise SystemExit(main())
