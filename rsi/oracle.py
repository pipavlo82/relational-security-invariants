"""Trusted reference predicates over inputs. Never imports the target adapters.
Expected events come from these predicates, never from a target run. This
finite executable model is reviewed code, not a universal semantic oracle.
"""
from copy import deepcopy
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from rsi.codec import decode, digest, ContractError

# Separate verification path from adapters; same crypto library and codec.
def inspect(proof):
    raw = bytes.fromhex(proof["payload_hex"])
    body = decode(raw)
    try:
        key = Ed25519PublicKey.from_public_bytes(bytes.fromhex(proof["public_key_hex"]))
        key.verify(bytes.fromhex(proof["signature_hex"]), raw)
        valid = True
    except InvalidSignature:
        valid = False
    return body, valid

def local_validity(req):
    return all(inspect(p)[1] for p in [req["proof"]] + req.get("evidence", []))

def predict(req):
    body, authenticated = inspect(req["proof"])
    policy, start = req["policy"], req["state"]
    allow = (authenticated and req["proof"]["public_key_hex"] == policy["subject_key"]
             and body["scope"] == policy["scope"]
             and body["policy_version"] == policy["policy_version"])
    next_state = {"revision": start["revision"] + 1, "head": digest(body)}
    def event(label, decision, before=None, after=None, effects=None, position=None):
        return {"label": label, "decision": decision, "before": deepcopy(start if before is None else before),
                "after": deepcopy(start if after is None else after),
                "effects": effects or [], "position": position}
    op = req["operation"]
    if op in ("admit", "transition", "ingest"):
        labels = req["paths"] if op == "ingest" else ["operation"]
        effect = "transitioned" if op == "transition" else "admitted"
        return {"results": [event(label, "ACCEPT" if allow else "REJECT",
                    after=next_state if allow else start, effects=[effect] if allow else []) for label in labels]}
    if op == "confirm":
        if not allow:
            return {"results": [event("operation", "REJECT")]}
        evidence_exists = False
        for proof in req["evidence"]:
            evidence, valid = inspect(proof)
            evidence_exists |= (valid and proof["public_key_hex"] == policy["evidence_key"]
                and evidence["scope"] == body["scope"]
                and evidence["operation_id"] == body["operation_id"]
                and evidence["kind"] in policy["evidence_kinds"])
        return {"results": [event("operation", "ACCEPT" if evidence_exists else "UNVERIFIABLE",
                    after=next_state if evidence_exists else start,
                    effects=["confirmed"] if evidence_exists else [])]}
    if op == "consume":
        if not allow:
            raise ContractError("unsupported unauthenticated consume scenario")
        history, reads, used, state = [], {}, set(), deepcopy(start)
        for step in req["schedule"]:
            worker = step["worker"]
            if step["kind"] == "read":
                if worker in reads:
                    raise ContractError("schedule has duplicate read")
                reads[worker] = state["revision"]
            else:
                if worker not in reads or worker in used:
                    raise ContractError("schedule has invalid commit")
                used.add(worker)
                previous = deepcopy(state)
                allocated = reads[worker] if reads[worker] == state["revision"] else None
                if allocated is not None:
                    state = {"revision": state["revision"] + 1, "head": worker}
                history.append(event(worker, "ACCEPT" if allocated is not None else "CONFLICT",
                    before=previous, after=state,
                    effects=["consumed"] if allocated is not None else [], position=allocated))
        if set(reads) != used:
            raise ContractError("schedule never completed")
        return {"results": history}
    raise ContractError("unknown oracle operation")
