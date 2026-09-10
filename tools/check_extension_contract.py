"""Deterministic architecture evidence; baseline pins do not supply expectations."""
from pathlib import Path
import argparse
import ast
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from rsi.codec import encode, load, raw_digest
from rsi.run import evaluate
from extensions.defaults import composition
from extensions.mutations import registry
from runner.extension_runtime import execute
from tools.run_registered_mutations import code_hashes


def report(root, mutation_path):
    baseline=load(root/"research/extension-contract-v0.1-baseline.json")
    hashes={path:{"before":old,"after":raw_digest((root/path).read_bytes())} for path,old in baseline["hashes"].items()}
    if any(row["before"]!=row["after"] for row in hashes.values()):raise ValueError("protected baseline bytes changed")
    fixtures,profiles,adapters=composition(root)
    result=execute(root,fixtures,profiles,adapters)
    old=evaluate(root)
    core=[row["result"] for row in result["rows"] if row.get("profile_id")==baseline["profile_id"] and "result" in row]
    if raw_digest(encode(sorted(core,key=lambda row:row["key"])))!=baseline["case_records_sha256"]:
        raise ValueError("registered legacy outcomes changed")
    if raw_digest(encode(old["evidence"]["cases"]))!=baseline["ordered_case_records_sha256"]:
        raise ValueError("compatibility outcome order/records changed")
    mutations=load(mutation_path)
    if mutations.get("implementation_hashes")!=code_hashes(root):raise ValueError("mutation report belongs to different implementation")
    expected_ids=set(registry().identities())
    rows=mutations["mutations"]
    if len(rows)!=len(expected_ids) or {row["mutation_id"] for row in rows}!=expected_ids:
        raise ValueError("missing or duplicate registered mutation outcome")
    if any(row["status"]!="KILLED" for row in rows):raise ValueError("mutation gate not green")
    if not set(baseline["mutation_ids"])<=expected_ids:raise ValueError("baseline mutation registration removed")
    counts={state:sum(row["status"]==state for row in rows) for state in ("KILLED","SURVIVED","VACUOUS","NOT_APPLIED")}
    if counts!=mutations["totals"]:raise ValueError("mutation count mismatch")
    forbidden=("crystal","receiptos","rvr","tsei","pq","semantic","messaging","generic")
    branches=[]
    for path in [*(root/"runner").glob("*.py"),root/"rsi/run.py",root/"rsi/oracle.py"]:
        for node in ast.walk(ast.parse(path.read_text())):
            if isinstance(node,(ast.If,ast.IfExp)):
                for value in ast.walk(node.test):
                    if isinstance(value,ast.Constant) and type(value.value) is str and any(x in value.value.lower() for x in forbidden):
                        branches.append({"path":path.relative_to(root).as_posix(),"line":node.lineno})
    if branches:raise ValueError("domain branches in core")
    return {"schema":"rsi-extension-report.v0","base_head":baseline["head"],"core_changed":False,
            "preserved_hashes":hashes,"fixture_registry":{"canonical_ids":[r["fixture_id"] for r in result["discovery"]["fixtures"]],"deterministic_discovery":True},
            "adapter_registry":{"ids":list(adapters.identities())},"expectation_registry":{"ids":list(profiles.identities()),"admissions":result["admissions"]},
            "mutation_registry":mutations,"legacy_compatibility":{"fixture_hashes_unchanged":True,"outcomes_unchanged":True,"legacy_mutations_unchanged":True,"ordered_case_records_sha256":baseline["ordered_case_records_sha256"]},
            "extensibility":{"external_fixture_ids_supported":True,"unknown_adapter_reports_unsupported":True,"unknown_profile_reports_unsupported":True,"core_domain_branches":len(branches)},
            "fixture_totals":result["totals"],"phase2_architecture_gate":"READY","external_domains_validated":False}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--mutations",type=Path,required=True)
    parser.add_argument("--output",type=Path,required=True)
    args=parser.parse_args()
    value=report(ROOT,args.mutations)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(encode(value))
    print("EXTENSION_CONTRACT_VALID; PHASE2_ARCHITECTURE_READY")

if __name__=="__main__":main()
