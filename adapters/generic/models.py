"""Reference systems receive components only, never fixture expectations."""
from .artifacts import signature_valid


def signer_subject(c):
    artifact = c["artifact"]
    authorized = artifact["signer"] == artifact["body"]["subject"]
    accepted = signature_valid(artifact) and authorized
    return {"outcome": "ACCEPT" if accepted else "REJECT", "authority_promotion": accepted}


def context_binding(c):
    bound = c["artifact"]["body"]["context"] == c["context"]
    accepted = signature_valid(c["artifact"]) and bound
    return {"outcome": "ACCEPT" if accepted else "REJECT", "provenance_promotion": accepted}


def status_evidence(c):
    matching = [e for e in c["evidence"] if all(e[k] == c["request"][k] for k in ("subject", "scope", "operation")) and e["success"]]
    justified = bool(matching)
    return {"outcome": "ACCEPT" if justified else "REJECT", "status": "confirmed" if justified else "failed", "status_promotion": justified}


def ingestion_equivalence(c):
    outcomes = {}
    for path in c["paths"]:
        authorized = c["artifact"]["body"]["role"] == "member"
        accepted = signature_valid(c["artifact"]) and authorized
        outcomes[path] = "ACCEPT" if accepted else "REJECT"
    return {"outcome": "ACCEPT" if all(v == "ACCEPT" for v in outcomes.values()) else "REJECT", "paths": outcomes, "policy_promotion": any(v == "ACCEPT" for v in outcomes.values())}
