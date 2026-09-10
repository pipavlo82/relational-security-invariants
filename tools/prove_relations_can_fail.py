"""Controlled source mutations, classified through the shared registry."""
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

# Explicit check/target mappings, never inferred from identifiers.
DEFINITIONS=(
("RP-M1","runner/relation_runtime.py",'profile = registry.resolve(value["relation_profile_id"], value["relation_profile_version"],\n                               value["relation_id"], value.get("relation_profile_sha256"))','profile = registry.resolve(next(iter(registry._profiles))[0], value["relation_profile_version"], value["relation_id"], value.get("relation_profile_sha256"))',"test_unknown_profile"),
("RP-M2","runner/relation_profile_registry.py",'self._profiles.get((profile_id, version))','next((p for (i,v),p in self._profiles.items() if i == profile_id), None)',"test_version"),
("RP-M3","runner/relation_profile_registry.py",'profile = self._profiles.get((profile_id, version))','profile = self._profiles.get((profile_id, version)) if not relation_id.startswith("reject") else None',"test_static_opacity"),
("RP-M4","runner/relation_profile.py",'self.validate_result(relation_id, result)','result["relation_state"] = "true"\n        self.validate_result(relation_id, result)',"test_rich"),
("RP-M5","tests/relation_support.py",'same = value["left"] == value["right"]  # RP-M5','same = value["left"] == value["right"] and "metadata" not in value  # RP-M5',"test_mirror"),
("RP-M6","tests/relation_support.py",'value["artifact"] == value["anchor"]  # RP-M6','value["artifact"] == value["current"]  # RP-M6',"test_historical"),
("RP-M7","runner/expectation_contract.py",'if encode(recomputed[ident]) != encode(recorded):  # EXP-M3','if False:  # disabled independent equality',"test_tamper"))

def child(output):
    suite=unittest.defaultTestLoader.loadTestsFromName("tests.test_relation_profiles.RelationTests")
    track_phases(suite);result=ExecutionResult();suite.run(result)
    output.parent.mkdir(parents=True,exist_ok=True)
    output.write_bytes(encode({"rows":result.rows,"tests_run":result.testsRun}))
    return 0 if result.wasSuccessful() else 1

def exercise(definition):
    ident,file,old,new,test=definition
    with tempfile.TemporaryDirectory(prefix="rsi-relation-mutant-") as temp:
        root=Path(temp)/"repo";copy_repo(root)
        path=root/file;source=path.read_text()
        if source.count(old)!=1:return MutationTrace(False)
        path.write_text(source.replace(old,new,1),newline="\n")
        output=root/"artifacts/child.json"
        process=subprocess.run([sys.executable,"-B","tools/prove_relations_can_fail.py","--child",str(output)],cwd=root,capture_output=True,timeout=90)
        if not output.exists():return MutationTrace(True,errors=("SETUP_OR_IMPORT",))
        if process.returncode not in (0,1):return MutationTrace(True,errors=("CHILD_PROCESS",))
        rows=load(output)["rows"]
        events=tuple(CheckEvent(r["id"],r["status"],r.get("phase","test")) for r in rows)
        return MutationTrace(True,events)

def registry():
    return MutationRegistry(Mutation(d[0],"relation-contract","tests.test_relation_profiles.RelationTests."+d[4],lambda context,d=d:exercise(d),"test") for d in DEFINITIONS)

def main():
    parser=argparse.ArgumentParser();parser.add_argument("--child",type=Path);parser.add_argument("--output",type=Path,default=Path("artifacts/relation-mutations.json"));args=parser.parse_args()
    if args.child:return child(args.child)
    baseline=ROOT/"artifacts/relation-test-baseline.json"
    if child(baseline):raise SystemExit("architecture baseline failed")
    result=registry().execute({"relation-contract"})
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(encode(result));print(result["totals"])
    return 0 if result["totals"]["KILLED"]==len(DEFINITIONS) else 1
if __name__=="__main__":raise SystemExit(main())
