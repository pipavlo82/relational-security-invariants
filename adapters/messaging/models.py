"""Tentative commit and a deterministic two-worker stale-read schedule."""
from copy import deepcopy
from adapters.generic.artifacts import authenticates, digest


def auth_before_commit(c):
    durable = deepcopy(c["state"])
    tentative = {"revision": durable["revision"] + 1, "session": "bootstrapped"}
    authenticated = authenticates(c["ciphertext"])
    may_commit = authenticated
    if may_commit:
        durable = tentative
    return {"outcome": "ACCEPT" if authenticated else "REJECT", "state_commit": durable != c["state"], "final_state_digest": digest(durable), "tentative_created": True}


def atomic_consumption(c):
    revision = c["revision"]
    # Both workers read before either tries to commit. Commit/CAS order is
    # deterministic; runner checks both worker orders. No real threads or clocks.
    observations = [(op["consumer"], op["position"]) for op in c["operations"]]
    decisions = []
    consumed = []
    for consumer, observed in observations:
        available = observed == revision
        if available:
            consumed.append({"consumer": consumer, "position": observed})
            revision += 1
        decisions.append("ACCEPT" if available else "REJECT")
    return {"outcome": "ACCEPT" if all(d == "ACCEPT" for d in decisions) else "REJECT", "decisions": decisions, "consumed": consumed, "final_revision": revision}
