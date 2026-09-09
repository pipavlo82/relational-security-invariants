"""Synthetic signed-message admission/session model; NOT a Signal or E2EE implementation.
Inputs contain no fixture ids, expected outcomes, or mutation labels.
"""
from copy import deepcopy
from rsi.codec import ContractError, digest
from rsi.wire import unpack, valid_signature

class MessagingModel:
    def __init__(self, state):
        self.state = deepcopy(state)

    def allowed(self, proof, policy):
        _, body = unpack(proof)
        if not valid_signature(proof):
            return False
        subject_ok = proof["public_key_hex"] == policy["subject_key"]  # M001
        scope_ok = body["scope"] == policy["scope"]  # M006
        return subject_ok and scope_ok and body["policy_version"] == policy["policy_version"]

    def emit(self, label, before, decision, effects=None, position=None):
        return {"label": label, "decision": decision, "before": before,
                "after": deepcopy(self.state), "effects": effects or [], "position": position}

    def admit(self, req, label):
        before = deepcopy(self.state)
        ok = self.allowed(req["proof"], req["policy"])
        if ok:
            _, body = unpack(req["proof"])
            self.state = {"revision": before["revision"] + 1, "head": digest(body)}
        return self.emit(label, before, "ACCEPT" if ok else "REJECT", ["admitted"] if ok else [])

    def run(self, req):
        op = req["operation"]
        if op == "admit":
            return {"results": [self.admit(req, "operation")]}
        if op == "transition":
            before = deepcopy(self.state)
            _, body = unpack(req["proof"])
            candidate = {"revision": before["revision"] + 1, "head": digest(body)}
            authenticated = self.allowed(req["proof"], req["policy"])  # M003
            if not authenticated:
                return {"results": [self.emit("operation", before, "REJECT")]}
            self.state = candidate
            return {"results": [self.emit("operation", before, "ACCEPT", ["transitioned"])]}
        if op == "consume":
            if not self.allowed(req["proof"], req["policy"]):
                raise ContractError("consume capability must authenticate")
            reads, committed, events = {}, set(), []
            for step in req["schedule"]:
                worker = step["worker"]
                if step["kind"] == "read":
                    if worker in reads:
                        raise ContractError("worker read twice")
                    reads[worker] = self.state["revision"]
                else:
                    if worker not in reads or worker in committed:
                        raise ContractError("invalid commit schedule")
                    committed.add(worker)
                    before = deepcopy(self.state)
                    if self.state["revision"] != reads[worker]:  # M004
                        events.append(self.emit(worker, before, "CONFLICT"))
                        continue
                    self.state = {"revision": self.state["revision"] + 1, "head": worker}
                    events.append(self.emit(worker, before, "ACCEPT", ["consumed"], reads[worker]))
            if committed != set(reads):
                raise ContractError("unfinished schedule")
            return {"results": events}
        if op == "confirm":
            before = deepcopy(self.state)
            _, body = unpack(req["proof"])
            if not self.allowed(req["proof"], req["policy"]):
                return {"results": [self.emit("operation", before, "REJECT")]}
            qualified = []
            for proof in req["evidence"]:
                _, receipt = unpack(proof)
                qualified.append(valid_signature(proof)
                    and proof["public_key_hex"] == req["policy"]["evidence_key"]
                    and receipt["operation_id"] == body["operation_id"]
                    and receipt["scope"] == body["scope"]
                    and receipt["kind"] in req["policy"]["evidence_kinds"])
            if not any(qualified):  # M008
                return {"results": [self.emit("operation", before, "UNVERIFIABLE")]}
            self.state = {"revision": before["revision"] + 1, "head": digest(body)}
            return {"results": [self.emit("operation", before, "ACCEPT", ["confirmed"])]}
        if op == "ingest":
            initial, events = deepcopy(self.state), []
            for path in req["paths"]:
                self.state = deepcopy(initial)
                before = deepcopy(self.state)
                ok = self.allowed(req["proof"], req["policy"])  # M009
                if ok:
                    _, body = unpack(req["proof"])
                    self.state = {"revision": before["revision"] + 1, "head": digest(body)}
                events.append(self.emit(path, before, "ACCEPT" if ok else "REJECT", ["admitted"] if ok else []))
            return {"results": events}
        raise ContractError("unsupported operation")

def run(request):
    return MessagingModel(request["state"]).run(request)
