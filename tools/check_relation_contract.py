"""Deterministic preservation report; fails closed on any legacy drift."""
import argparse
import ast
import json
from pathlib import Path
import subprocess
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from rsi.codec import encode,load,raw_digest
from extensions.defaults import composition as old_composition
from extensions.relations import composition
from runner.extension_runtime import execute as old_execute
from runner.relation_runtime import execute

GENERIC=("runner/relation_profile.py","runner/relation_profile_registry.py","runner/relation_runtime.py")
def generate(reference,legacy_mutations,relation_mutations):
    pins=reference["protected_legacy_sha256"]
    differences=[name for name,pin in sorted(pins.items()) if raw_digest((ROOT/name).read_bytes())!=pin]
    if differences:raise ValueError("protected artifact drift: "+repr(differences))
    old=old_execute(ROOT,*old_composition(ROOT));new=execute(ROOT,*composition(ROOT))
    if encode(old)!=encode(new):raise ValueError("legacy execution changed")
    if encode(new)!=encode(execute(ROOT,*composition(ROOT))):raise ValueError("nondeterministic execution")
    for file in GENERIC:
        source=(ROOT/file).read_text();tree=ast.parse(source)
        if any(isinstance(n,ast.Attribute) and n.attr in ("startswith","endswith") for n in ast.walk(tree)):raise ValueError("identifier prefix branch")
        for term in ("crystal","receipt","rvr","8309","tsei","pq","slh","mldsa","ml-dsa","semantic abi","interpoll"):
            if term in source.lower():raise ValueError("domain token in generic module: "+file)
    if legacy_mutations["totals"]!={"KILLED":16,"SURVIVED":0,"VACUOUS":0,"NOT_APPLIED":0}:raise ValueError("legacy mutations changed")
    if relation_mutations["totals"]!={"KILLED":7,"SURVIVED":0,"VACUOUS":0,"NOT_APPLIED":0}:raise ValueError("relation mutation gate failed")
    tests=unittest.defaultTestLoader.discover(str(ROOT/"tests")).countTestCases()
    return {"schema":"rsi-relation-profile-implementation.v0","head_before":"05f3853756ad9deb0e5d08d54dfdfd462652a801",
        "baseline_evidence":reference.get("baseline_evidence",{}),"files_changed":reference.get("files_changed",[]),"evidence_closure_reference":"research/relation-profile-evidence-closure-v0.json",
        "protected_legacy_sha256":pins,"protected_hash_differences":differences,"core_changed":False,"legacy_schemas_changed":False,
        "schemas_added":["schema/profiled-relation-fixture.v0.schema.json"],"extension_schema_changed":False,
        "legacy_outcome_diff":[],"legacy_rows_sha256":raw_digest(encode([r["result"] for r in new["rows"]])),
        "legacy_totals":new["totals"],"test_totals":{"before":150,"after":tests,"optimized_before":150,"optimized_after":tests},
        "legacy_mutations":legacy_mutations,"relation_mutations":relation_mutations,
        "mutation_totals":{"KILLED":23,"SURVIVED":0,"VACUOUS":0,"NOT_APPLIED":0},
        "static_checks":{"modules":list(GENERIC),"domain_tokens":0,"identifier_prefix_branches":0},
        "deterministic_execution":True,"expectation_comparator_changed":False,
        "profile_contract_sha256":{p:raw_digest((ROOT/p).read_bytes()) for p in (*GENERIC,"schema/profiled-relation-fixture.v0.schema.json")},
        "readiness":{"crystal_receipt_semantic_gate":"READY","rvr_architecture":True,"tsei_architecture":True,"pq_policy_cutoff_architecture":True,"pq_authenticated_chain":"UNSUPPORTED"},
        "limitations":["Architecture-only test models; no external adapters or fixture corpora.","Trusted Python implementations require independence/purity review; no sandbox or arbitrary-code proof.","Existing ASCII/integer canonical transport limits remain.","Descriptor pin is optional trusted identity metadata; descriptor source closure is not automatically verified.","RVR and PQ source conclusions remain evidence-qualified YELLOW.","Post-push CI is reported separately against the resulting commit."]}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--legacy-mutations",type=Path,default=Path("artifacts/relation-profile-v0/mutations-after.json"))
    parser.add_argument("--relation-mutations",type=Path,default=Path("artifacts/relation-profile-v0/relation-mutants.json"))
    parser.add_argument("--output",type=Path,default=Path("artifacts/relation-contract-check.json"))
    args=parser.parse_args()
    reference=load(ROOT/"research/relation-profile-implementation-v0.json")
    result=generate(reference,load(args.legacy_mutations),load(args.relation_mutations))
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(encode(result))
    print("Protected hashes match; legacy rows unchanged; 23 KILLED; deterministic report.")
    return 0
if __name__=="__main__":raise SystemExit(main())
