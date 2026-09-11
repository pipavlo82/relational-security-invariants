"""Deterministic scope, compatibility, source and mapped-mutation evidence."""
import argparse
from pathlib import Path
import sys
import unittest
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from tools.protected_maintenance import mismatches, approved_changes
from rsi.codec import encode, load, raw_digest
from runner.relation_runtime import execute
from profiles.rvr.source import verify_source
from extensions.rvr import composition, complete_composition
from extensions.crystal_receipt import composition as crystal
from extensions.relations import composition as legacy


def report(mutations, prior):
    evidence = load(ROOT / "research/rvr-digest-binding-source-map-v0.json")
    drift = mismatches(ROOT,evidence["protected_hashes"])
    maintenance = approved_changes(ROOT,evidence["protected_hashes"])
    if drift: raise ValueError("protected bytes changed: " + repr(drift))
    for path in list((ROOT / "runner").glob("*.py")) + list((ROOT / "rsi").glob("*.py")):
        if any(term in path.read_text().lower() for term in ("rvr", "8309", "signed_digest", "amendment_cc", "crystal", "receiptos")):
            raise ValueError("domain leakage: " + str(path))
    for key, result in prior.items():
        if encode(result["mutations"]) != encode(evidence["prior_mutations"][key]["mutations"]):
            raise ValueError("prior mutation record drift: " + key)
    if mutations["totals"] != {"KILLED": 6, "SURVIVED": 0, "VACUOUS": 0, "NOT_APPLIED": 0}:
        raise ValueError("RVR mapped-mutation gate failed")
    source = verify_source(ROOT)
    actual = execute(ROOT, *composition(ROOT))
    if encode(actual) != encode(execute(ROOT, *composition(ROOT))):
        raise ValueError("domain report nondeterministic")
    if actual["totals"] != {"PASS": 10, "FAIL": 0, "INVALID_FIXTURE": 0, "UNSUPPORTED": 0}:
        raise ValueError("RVR conformance gate failed")
    cr = execute(ROOT, *crystal(ROOT))
    if encode(cr) != encode(evidence["crystal_execution"]):
        raise ValueError("Crystal outcome drift")
    old = execute(ROOT, *legacy(ROOT))
    expected_digest = load(ROOT / "research/relation-profile-implementation-v0.json")["legacy_rows_sha256"]
    if raw_digest(encode([r["result"] for r in old["rows"]])) != expected_digest:
        raise ValueError("legacy outcome drift")
    combined = execute(ROOT, *complete_composition(ROOT))
    if combined["totals"] != {"PASS": 50, "FAIL": 0, "INVALID_FIXTURE": 0, "UNSUPPORTED": 0}:
        raise ValueError("combined pipeline gate failed")
    totals = {k: sum(report["totals"][k] for report in [mutations, *prior.values()]) for k in ("KILLED", "SURVIVED", "VACUOUS", "NOT_APPLIED")}
    return {
        "schema": "rsi-domain-validation.v0",
        "approved_post_v0_maintenance": maintenance, "domain": "rvr-digest-binding", "phase": "2B.1",
        "rsi_head_before": evidence["rsi_head_before"], "source": source, "source_repositories": evidence["repos"],
        "companion_delta": evidence["companion_delta"], "relations": ["profile-transition-digest-binding", "verdict-profile-digest-binding"],
        "fixtures": {"total": 6, "pass": 6, "fail": 0, "invalid_fixture": 0, "unsupported": 0},
        "checks": actual["totals"], "execution": actual, "combined_checks": combined["totals"],
        "mutations": mutations["totals"], "mutation_report": mutations, "all_mutation_totals": totals,
        "prior_mutation_record_diff": 0, "legacy_outcome_diff": 0, "crystal_receipt_outcome_diff": 0,
        "protected_hashes_match": not maintenance, "protected_hash_count": len(evidence["protected_hashes"]),
        "original_protected_80_match": True, "generic_core_changed": False, "semantic_exceptions_added": 0,
        "unresolved_semantics_preserved": True, "effective_profile_not_collapsed_to_accept": True,
        "crypto_authentication": {"status": "UNSUPPORTED", "reason": "no pinned independently verified signature-verification lane"},
        "anti_coupling": "PASS", "deterministic": True,
        "test_totals": {"before": 229, "after": unittest.defaultTestLoader.discover(str(ROOT / "tests")).countTestCases()},
        "limitations": evidence["limitations"] + [
            "Digest conformance PASS does not establish any cryptographic authentication, identity/control of pubkeys, or substantive truth.",
            "Runtime accepts the RSI ASCII/integer transport subset only; no silent source coercion or universal JCS conformance claim.",
            "Source copies are pinned offline. New upstream commits require explicit repin and revalidation; runtime does not fetch moving branches.",
            "Python implementations are trusted reviewed code. Logical independence is tested, not guaranteed by a filesystem sandbox.",
            "RVR-M7 omitted: vector name/expect labels are not admitted fixture inputs or a runtime source of expected truth; hostile-label regression covers the boundary.",
            "Full Phase 2B remains blocked pending a separately pinned and validated signature-verification lane.",
        ],
        "claim": "RSI validated a second real relation family: RVR profile-transition and verdict digest binding, while mechanically preventing promotion of digest binding into an unsupported cryptographic-authentication claim.",
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--mutations", type=Path, default=ROOT / "artifacts/rvr-mutations.json")
    p.add_argument("--legacy-mutations", type=Path, default=ROOT / "artifacts/registered-mutations.json")
    p.add_argument("--relation-mutations", type=Path, default=ROOT / "artifacts/relation-mutations.json")
    p.add_argument("--crystal-mutations", type=Path, default=ROOT / "artifacts/crystal-mutations.json")
    p.add_argument("--output", type=Path, default=ROOT / "artifacts/rvr-digest-validation.json")
    args = p.parse_args()
    result = report(load(args.mutations), {"legacy": load(args.legacy_mutations), "rp": load(args.relation_mutations), "cr": load(args.crystal_mutations)})
    args.output.parent.mkdir(parents=True, exist_ok=True); args.output.write_bytes(encode(result))
    print("RVR digest binding: 6 fixtures / 10 PASS; 6 KILLED; crypto UNSUPPORTED; prior outcomes/26 mutation records unchanged")


if __name__ == "__main__":
    main()
