"""Deterministic domain closure report; never fabricates test or CI execution."""
import argparse
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from rsi.codec import encode, load, raw_digest
from runner.relation_runtime import execute
from extensions.pq import composition, complete_composition
from profiles.pq.source import verify_source


def report(root, mutations):
    mapping = load(root / "research/pq-policy-asof-source-map-v0.json")
    pin = verify_source(root)
    isolated = execute(root, *composition(root))
    combined = execute(root, *complete_composition(root))
    old_ids = {r["fixture_id"] for r in mapping["prior_rows"]}
    prior = [r for r in combined["rows"] if r["fixture_id"] in old_ids]
    drift = [path for path, digest in mapping["protected_hashes"].items() if raw_digest((root/path).read_bytes()) != digest]
    if drift: raise ValueError("PROTECTED_DRIFT: " + repr(drift))
    if prior != mapping["prior_rows"]: raise ValueError("PRIOR_OUTCOME_DRIFT")
    if isolated["totals"] != {"PASS":7,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":0}: raise ValueError("DOMAIN_FAILED")
    if combined["totals"] != {"PASS":64,"FAIL":0,"INVALID_FIXTURE":0,"UNSUPPORTED":0}: raise ValueError("COMBINED_FAILED")
    if mutations["totals"] != {"KILLED":7,"SURVIVED":0,"VACUOUS":0,"NOT_APPLIED":0}: raise ValueError("MUTATION_GATE")
    if {r["mutation_id"] for r in mutations["mutations"]} != {"PQ-M"+str(n) for n in range(1,8)}: raise ValueError("MUTATION_INVENTORY")
    forbidden = ("pq", "effective_commit", "registry_contract_commit", "valid_provenance", "crystal", "receiptos", "rvr")
    for directory in ("runner", "rsi"):
        for path in sorted((root/directory).glob("*.py")):
            if any(term in path.read_text().lower() for term in forbidden): raise ValueError("CORE_COUPLING")
    return {"schema":"rsi-domain-validation.v0", "domain":"pq-key-binding", "scope":"policy-cutoff-asof",
        "rsi_head_before":mapping["rsi_head_before"], "source":pin,
        "relations":["authority-at-asof","cutoff-policy","historical-artifact-eligibility","stale-binding-detection"],
        "authenticated_transition_validation":{"status":"UNSUPPORTED"},
        "anchor_validation":{"status":"UNSUPPORTED","reason":"supplied evidence flags, not independently verified anchors"},
        "algorithm_identity_mismatch":mapping["algorithm_identity_mismatch"],
        "fixtures":{"files":6,"total":7, **{k.lower():v for k,v in isolated["totals"].items()}},
        "rows":isolated["rows"], "mutations":{k.lower():v for k,v in mutations["totals"].items()},
        "mutation_records":mutations["mutations"], "combined_totals":combined["totals"],
        "legacy_compatibility":{"outcome_diff":0}, "crystal_receipt_compatibility":{"outcome_diff":0}, "rvr_compatibility":{"outcome_diff":0}, "tsei_compatibility":{"outcome_diff":0},
        "protected_hashes_match":True, "protected_hash_count":len(mapping["protected_hashes"]),
        "generic_core_changed":False,"semantic_exceptions_added":0,"anti_coupling":"PASS",
        "retroactivity_prevented":True,"presence_not_authority":True,
        "phase_status":"LOCAL_VALIDATED_CI_SEPARATE", "full_pq_authenticated_chain":"UNSUPPORTED",
        "limitations":["Policy results are conditional on supplied anchored/signature-validity flags; neither is independently authenticated here.",
          "Rotation policy anchor is intended in source vectors, not a proven deployed anchor.",
          "SLH-DSA artifact identity and inconsistent ML-DSA deferred labels are preserved; no algorithm-specific verification.",
          "Historical eligibility requires the governing anchor evidence condition, never created_at alone.",
          "Pinned history only; no general subject-signature authority validation.",
          "ASCII/integer fixture transport and trusted Python independence limitations remain.",
          "RVR crypto authentication, TSEI provenance authority and PQ authenticated continuity remain unsupported.",
          "CI and unit execution results are recorded separately."]}



def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--mutations",type=Path,default=ROOT/"artifacts/pq-mutations.json")
    parser.add_argument("--output",type=Path,default=ROOT/"artifacts/pq-validation.json")
    args=parser.parse_args(); value=report(ROOT,load(args.mutations))
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_bytes(encode(value))
    print(value["combined_totals"],value["mutations"])
    return 0
if __name__=="__main__":raise SystemExit(main())
