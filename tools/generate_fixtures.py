"""Definition-derived synthetic fixtures. --check never overwrites committed evidence.
Public deterministic test keys only; absolutely not for production secrets.
"""
import argparse
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization
from rsi.codec import encode, raw_digest
from rsi.corpus import FAMILIES
from rsi.oracle import predict, local_validity

def key(label):
    return Ed25519PrivateKey.from_private_bytes(sha256(("RSI PUBLIC TEST KEY: " + label).encode()).digest())

def public(label):
    return key(label).public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw).hex()

def signed(body, label="alice", pretty=False):
    raw = json.dumps(body, indent=2, sort_keys=False).encode() if pretty else encode(body)
    return {"payload_hex": raw.hex(), "public_key_hex": public(label), "signature_hex": key(label).sign(raw).hex()}

def base(domain, op):
    body = {"domain": domain, "operation_id": domain + "-001", "scope": domain + ":scope-a", "policy_version": "policy.v1", "payload": "synthetic public data"}
    req = {"operation": op, "state": {"revision": 0, "head": "initial"},
           "proof": signed(body), "policy": {"subject_key": public("alice"), "scope": body["scope"],
           "policy_version": "policy.v1", "evidence_key": public("witness"),
           "evidence_kinds": ["recipient_ack", "durable_publication"] if domain == "message" else ["journal_commit", "settlement_receipt"]}}
    if op == "consume":
        req["schedule"] = [{"kind": kind, "worker": worker} for worker in ["a", "b"] for kind in ["read", "commit"]]
    if op == "ingest":
        req["paths"] = ["live", "snapshot", "import", "restore"]
    if op == "confirm":
        receipt = {"operation_id": body["operation_id"], "scope": body["scope"], "kind": req["policy"]["evidence_kinds"][0]}
        req["evidence"] = [signed(receipt, "witness")]
    return req

def build():
    files, expectations = {}, {}
    for ident, (relation, mutation_model, operation) in FAMILIES.items():
        requests = {"messaging": base("message", operation), "generic": base("receipt", operation)}
        bad, mirror = deepcopy(requests), deepcopy(requests)
        for adapter, req in bad.items():
            if ident == "RSI-001":
                req["policy"]["subject_key"] = public("bob")
            elif ident == "RSI-003":
                sig = bytes.fromhex(req["proof"]["signature_hex"])
                req["proof"]["signature_hex"] = (bytes([sig[0] ^ 1]) + sig[1:]).hex()
            elif ident == "RSI-004":
                req["schedule"] = [{"kind": kind, "worker": worker} for kind in ["read", "commit"] for worker in ["a", "b"]]
            elif ident == "RSI-006":
                req["policy"]["scope"] += ":other"
            elif ident == "RSI-008":
                req["evidence"] = []
            elif ident == "RSI-009":
                req["policy"]["policy_version"] = "policy.v2"
        for req in mirror.values():
            body = json.loads(bytes.fromhex(req["proof"]["payload_hex"]))
            req["proof"] = signed(body, pretty=True)
            if "evidence" in req:
                req["evidence"] = [signed(json.loads(bytes.fromhex(p["payload_hex"])), "witness", pretty=True) for p in req["evidence"]]
        cases = []
        for name, reqs in [("control", requests), ("mutation", bad), ("mirror_positive", mirror)]:
            valid = not (ident == "RSI-003" and name == "mutation")
            cases.append({"name": name, "local_validity_expected": valid, "requests": reqs})
            for adapter, req in reqs.items():
                expectations[ident + "/" + name + "/" + adapter] = {"local_validity": local_validity(req), "observation": predict(req)}
        fixture = {"schema": "relation-binding-fixture.v0", "id": ident, "protected_relation": relation,
            "mutation_model": mutation_model, "profile_version": "rsi-reference-profile.v0", "cases": cases}
        files["fixtures/" + ident + "-" + relation.replace("_", "-") + ".json"] = encode(fixture)
    files["oracle/expected.v0.json"] = encode({"schema": "rsi-oracle-set.v0", "expectations": expectations})
    pins = {name: raw_digest(raw) for name, raw in files.items()}
    for name in ["schema/relation-binding-fixture.v0.schema.json", "schema/observation.v0.schema.json"]:
        pins[name] = raw_digest((ROOT/name).read_bytes())
    files["manifest.json"] = encode({"schema": "rsi-corpus.v0", "serializer": "rsi-json-ascii.v0", "fixture_ids": sorted(FAMILIES), "files": pins})
    return files

def main():
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--write", action="store_true")
    mode.add_argument("--check", action="store_true")
    args = parser.parse_args()
    different = []
    for name, raw in build().items():
        path = ROOT/name
        if args.write:
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        elif not path.exists() or path.read_bytes() != raw:
            different.append(name)
    if different:
        print("GENERATION_MISMATCH " + ", ".join(different))
        return 1
    print("GENERATION_OK")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
