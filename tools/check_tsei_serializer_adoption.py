"""Deterministic domain closure report; never fabricates test or CI execution."""
import argparse
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.protected_maintenance import mismatches, approved_changes
from rsi.codec import encode, load, raw_digest
from runner.relation_runtime import execute
from extensions.tsei import composition, complete_composition
from profiles.tsei.source import verify_source


def report(root, mutations):
    mapping = load(root / "research/tsei-serializer-adoption-source-map-v0.json")
    pin = verify_source(root)
    isolated = execute(root, *composition(root))
    combined = execute(root, *complete_composition(root))
    old_ids = {r["fixture_id"] for r in mapping["prior_rows"]}
    prior = [r for r in combined["rows"] if r["fixture_id"] in old_ids]
    drift = mismatches(root,mapping["protected_hashes"])
    maintenance = approved_changes(root,mapping["protected_hashes"])
    if drift: raise ValueError("PROTECTED_DRIFT: " + repr(drift))
    if prior != mapping["prior_rows"]: raise ValueError("PRIOR_OUTCOME_DRIFT")
    if isolated["totals"] != {"PASS":7,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":0}: raise ValueError("DOMAIN_FAILED")
    if combined["totals"] != {"PASS":57,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":0}: raise ValueError("COMBINED_FAILED")
    if mutations["totals"] != {"KILLED":6,"SURVIVED":0,"VACUOUS":0,"NOT_APPLIED":0}: raise ValueError("MUTATION_GATE")
    if {r["mutation_id"] for r in mutations["mutations"]} != {"TSEI-M"+str(n) for n in range(1,7)}: raise ValueError("MUTATION_INVENTORY")
    forbidden = ("tsei", "effective_commit", "registry_contract_commit", "valid_provenance", "crystal", "receiptos", "rvr")
    for directory in ("runner", "rsi"):
        for path in sorted((root/directory).glob("*.py")):
            if any(term in path.read_text().lower() for term in forbidden): raise ValueError("CORE_COUPLING")
    return {"schema":"rsi-domain-validation.v0", "domain":"tsei", "scope":"serializer-adoption-only",
        "rsi_head_before":mapping["rsi_head_before"], "source":pin,
        "relations":["serializer-binding","producer-adoption","authoritative-record-introduction","non-retroactivity"],
        "authority_validation":mapping["authority_validation"],
        "fixtures":{"total":7, **{k.lower():v for k,v in isolated["totals"].items()}},
        "rows":isolated["rows"], "mutations":{k.lower():v for k,v in mutations["totals"].items()},
        "mutation_records":mutations["mutations"], "combined_totals":combined["totals"],
        "legacy_compatibility":{"outcome_diff":0}, "crystal_receipt_compatibility":{"outcome_diff":0}, "rvr_compatibility":{"outcome_diff":0},
        "protected_hashes_match":not maintenance, "approved_post_v0_maintenance":maintenance, "protected_hash_count":len(mapping["protected_hashes"]),
        "generic_core_changed":False,"semantic_exceptions_added":0,"anti_coupling":"PASS",
        "retroactivity_prevented":True,"presence_not_authority":True,
        "phase_status":"LOCAL_VALIDATED_CI_SEPARATE", "full_phase_2c":"BLOCKED",
        "limitations":["Authority operands withheld; no provenance recomputation.",
          "Exact finite source snapshots only; unknown snapshots require repin and revalidation.",
          "ASCII/integer RSI fixture transport only. Full tagged serializer vectors run outside fixture transport without coercion.",
          "Trusted Python predictor and wrapper independence requires continued review.",
          "Snapshot cases test binding policy at pinned coordinates, not attestation of arbitrary artifact origin.",
          "Historical sample is a public synthetic preflight artifact, not a real authority oracle.",
          "CI and unit execution results are recorded separately; this deterministic checker does not infer them."]}


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--mutations",type=Path,default=ROOT/"artifacts/tsei-mutations.json")
    parser.add_argument("--output",type=Path,default=ROOT/"artifacts/tsei-validation.json")
    args=parser.parse_args(); value=report(ROOT,load(args.mutations))
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(encode(value))
    print(value["combined_totals"],value["mutations"])
    return 0
if __name__=="__main__":raise SystemExit(main())
