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
DEFINITIONS = (('SABI-M1', 'adapters/semantic_abi/execute.mjs', '// SABI-M1 claim', 'requirement.claim_type=producer.establishes[0].claim_type;', 'test_claim'), ('SABI-M2', 'adapters/semantic_abi/execute.mjs', '// SABI-M2 scope', 'requirement.scope=producer.establishes[0].scope;', 'test_scope'), ('SABI-M3', 'adapters/semantic_abi/execute.mjs', '// SABI-M3 authority', 'requirement.authority_class=producer.establishes[0].authority_class;', 'test_authority'), ('SABI-M4', 'adapters/semantic_abi/execute.mjs', '// SABI-M4 time value', "for (const k of ['issued_at','verification_time']) if (k in requirement && k in producer.establishes[0]) requirement[k]=producer.establishes[0][k];", 'test_time_value'), ('SABI-M5', 'adapters/semantic_abi/execute.mjs', '// SABI-M5 time kind', "const pk=['issued_at','verification_time'].find(k=>k in producer.establishes[0]); const rk=['issued_at','verification_time'].find(k=>k in requirement); const rv=requirement[rk]; delete requirement[rk]; requirement[pk]=rv;", 'test_time_kind'), ('SABI-M6', 'adapters/semantic_abi/execute.mjs', '// SABI-M6 universal recomputation', "if (producer.establishes[0].authority_class==='INDEPENDENT_RECOMPUTATION' && requirement.authority_class==='SEMANTIC_VERIFICATION') compatible=true;", 'test_no_universal_recomputation'), ('SABI-M7', 'adapters/semantic_abi/execute.mjs', '// SABI-M7 mirror', "if (producer.component!=='demo./verify') compatible=false;", 'test_component_mirror'), ('SABI-M8', 'adapters/semantic_abi/execute.mjs', '// SABI-M8 cross-claim mixing', 'if (Object.keys(requirement).every(k=>producer.establishes.some(c=>c[k]===requirement[k]))) compatible=true;', 'test_no_cross_claim_mixing'), ('SABI-M9', 'adapters/semantic_abi/model.py', "o['claim_truth']='UNSUPPORTED'  # SABI-M9", "o['claim_truth']='SUPPORTED' if o['edge_compatible'] else 'UNSUPPORTED'", 'test_no_truth_promotion'), ('SABI-M10', 'adapters/semantic_abi/model.py', "o['execution_occurrence']='UNSUPPORTED'  # SABI-M10", "o['execution_occurrence']='SUPPORTED' if o['edge_compatible'] else 'UNSUPPORTED'", 'test_no_execution_promotion'))

def child(output):
    suite=unittest.defaultTestLoader.loadTestsFromName("tests.test_semantic_abi.SemanticAbiTests")
    track_phases(suite);result=ExecutionResult();suite.run(result)
    output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(encode({"rows":result.rows,"tests_run":result.testsRun}))
    return 0 if result.wasSuccessful() else 1

def exercise(definition):
    with tempfile.TemporaryDirectory(prefix="sabi-mutant-") as temp:
        root=Path(temp)/"repo";copy_repo(root)
        ident,file,old,new,mapped=definition;path=root/file;source=path.read_text()
        if source.count(old)!=1:return MutationTrace(False)
        path.write_text(source.replace(old,new,1),newline="\n")
        output=root/"artifacts/sabi-child.json"
        p=subprocess.run([sys.executable,"-B","tools/prove_semantic_abi_can_fail.py","--child",str(output)],cwd=root,capture_output=True,timeout=180)
        if p.returncode not in (0,1) or not output.exists():return MutationTrace(True,errors=("CHILD_SETUP",))
        return MutationTrace(True,tuple(CheckEvent(r["id"],r["status"],r.get("phase","test")) for r in load(output)["rows"]))

def registry():
    return MutationRegistry(Mutation(d[0],"semantic-abi.claim-edge.v0","tests.test_semantic_abi.SemanticAbiTests."+d[4],lambda context,d=d:exercise(d),"test") for d in DEFINITIONS)

def main():
    p=argparse.ArgumentParser();p.add_argument("--child",type=Path);p.add_argument("--output",type=Path,default=ROOT/"artifacts/semantic-abi-mutations.json");args=p.parse_args()
    if args.child:return child(args.child)
    if child(ROOT/"artifacts/semantic-abi-mutation-baseline.json"):raise SystemExit("SABI baseline failed")
    result=registry().execute({"semantic-abi.claim-edge.v0"});args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(encode(result));print(result["totals"])
    return 0 if result["totals"]["KILLED"]==10 else 1
if __name__=="__main__":raise SystemExit(main())
