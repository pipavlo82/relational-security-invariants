"""Deterministic real-domain evidence report; no source loading from network."""
import argparse
import json
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from rsi.codec import encode,load,raw_digest
from extensions.crystal_receipt import composition,complete_composition
from runner.relation_runtime import execute
from profiles.crystal_receipt.source import verify_source
from profiles.crystal_receipt.relation import PROFILE_ID
from extensions.relations import composition as legacy_composition

def report(mutations):
    source=verify_source(ROOT);source_map=load(ROOT/"research/crystal-receipt-source-map-v0.json")
    pins={**source_map["protected_legacy_hashes"],**source_map["generic_hashes"]}
    if any(raw_digest((ROOT/p).read_bytes())!=h for p,h in pins.items()):raise ValueError("protected hash mismatch")
    actual=execute(ROOT,*composition(ROOT))
    if encode(actual)!=encode(execute(ROOT,*composition(ROOT))):raise ValueError("non-deterministic domain execution")
    if actual["totals"]!={"PASS":4,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":0}:raise ValueError("domain conformance failure")
    if mutations["totals"]!={"KILLED":3,"SURVIVED":0,"VACUOUS":0,"NOT_APPLIED":0}:raise ValueError("domain mutation gate failure")
    combined=execute(ROOT,*complete_composition(ROOT))
    if combined["totals"]!={"PASS":40,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":0}:raise ValueError("combined corpus failure")
    legacy=execute(ROOT,*legacy_composition(ROOT))
    old=load(ROOT/"research/relation-profile-implementation-v0.json")
    if raw_digest(encode([r["result"] for r in legacy["rows"]]))!=old["legacy_rows_sha256"]:raise ValueError("legacy outcome drift")
    for file in source_map["generic_hashes"]:
        if file.startswith("runner/") and file.endswith(".py"):
            text=(ROOT/file).read_text().lower()
            if any(t in text for t in ("crystal","receipt","receiptos","audit_timestamp","semantic snapshot","lane k")):raise ValueError("core semantic leakage")
    return {"schema":"rsi-domain-validation.v0","domain":"crystal-receipt","rsi_head_before":"30e13ba3a39915c91a607f70975c669ead7a231e",
      "source":source,"relation_profiles":[PROFILE_ID],"fixtures":{"total":2,"pass":2,"fail":0,"invalid_fixture":0,"unsupported":0},
      "checks":actual["totals"],"combined_checks":combined["totals"],"execution":actual,"mutations":{k.lower():v for k,v in mutations["totals"].items()},"mutation_report":mutations,
      "legacy_compatibility":{"outcome_diff":0,"protected_hashes_match":True,"legacy_checks":legacy["totals"],"legacy_mutations":23},
      "protected_sha256":pins,"tests":{"before":200,"after":unittest.defaultTestLoader.discover(str(ROOT/"tests")).countTestCases()},
      "generic_core_changed":False,"semantic_exceptions_added":0,"anti_coupling":"PASS","deterministic":True,
      "omitted_candidates":source_map["omitted_candidates"],"limitations":[
        "Only flat printable ASCII string semantic artifacts and external audit timestamp dictionaries are covered.",
        "Both substituted snapshots are accepted; only their semantic identity equivalence is denied.",
        "No provenance authority, admission seam or Lane K process-isolation claim is made.",
        "Pinned source copies execute offline; a live upstream drift check is an explicit preflight, not runtime network loading.",
        "Trusted Python/Node implementations require source review; absence of an expectation input channel is not a filesystem sandbox.",
        "First real external domain only; not cross-domain validation or complete ReceiptOS coverage."],
      "claim":"RSI admitted its first real external domain, Crystal Receipt / ReceiptOS, through the existing Relation Profile, Extension, and Expectation contracts without changing RSI core semantics."}

def main():
    p=argparse.ArgumentParser();p.add_argument("--mutations",type=Path,default=ROOT/"artifacts/crystal-phase2a/cr-mutations.json");p.add_argument("--output",type=Path,default=ROOT/"artifacts/crystal-validation.json");args=p.parse_args()
    result=report(load(args.mutations));args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(encode(result));print("Crystal Receipt: 2 fixtures / 4 PASS; 3 KILLED; protected hashes and legacy outcomes unchanged")
if __name__=="__main__":main()
