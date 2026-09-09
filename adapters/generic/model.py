"""Synthetic receipt journal backed by isolated in-memory SQLite.
This is a second target domain, NOT an independently authored verifier or a
production ReceiptOS adapter. No on-disk durability/crash-recovery claim.
"""
import sqlite3
from rsi.codec import ContractError, digest
from rsi.wire import unpack, valid_signature

class ReceiptJournal:
    def __init__(self, state):
        self.db = sqlite3.connect(":memory:")
        self.db.execute("CREATE TABLE state (id INTEGER PRIMARY KEY, revision INTEGER, head TEXT)")
        self.db.execute("INSERT INTO state VALUES (1, ?, ?)", (state["revision"], state["head"]))
        self.db.commit()

    def state(self):
        rev, head = self.db.execute("SELECT revision, head FROM state WHERE id=1").fetchone()
        return {"revision": rev, "head": head}

    def store(self, state):
        with self.db:
            self.db.execute("UPDATE state SET revision=?, head=? WHERE id=1", (state["revision"], state["head"]))

    def permits(self, proof, policy):
        _, record = unpack(proof)
        if not valid_signature(proof):
            return False
        if proof["public_key_hex"] != policy["subject_key"]:  # M001
            return False
        if record["scope"] != policy["scope"]:  # M006
            return False
        return record["policy_version"] == policy["policy_version"]

    def event(self, name, before, decision, effects=None, position=None):
        return {"label": name, "decision": decision, "before": before,
                "after": self.state(), "effects": effects or [], "position": position}

    def execute(self, request):
        op = request["operation"]
        before = self.state()
        _, body = unpack(request["proof"])
        candidate = {"revision": before["revision"] + 1, "head": digest(body)}
        if op in ("admit", "transition"):
            permitted = self.permits(request["proof"], request["policy"])  # M003
            if not permitted:
                return {"results": [self.event("operation", before, "REJECT")]}
            self.store(candidate)
            effect = "transitioned" if op == "transition" else "admitted"
            return {"results": [self.event("operation", before, "ACCEPT", [effect])]}
        if op == "consume":
            if not self.permits(request["proof"], request["policy"]):
                raise ContractError("invalid signed journal capability")
            observed, used, events = {}, set(), []
            for instruction in request["schedule"]:
                worker = instruction["worker"]
                if instruction["kind"] == "read":
                    if worker in observed:
                        raise ContractError("duplicate read")
                    observed[worker] = self.state()["revision"]
                    continue
                if worker not in observed or worker in used:
                    raise ContractError("commit without one unmatched read")
                used.add(worker)
                start = self.state()
                with self.db:
                    updated = self.db.execute(
                        "UPDATE state SET revision=revision+1, head=? WHERE id=1 AND revision=?",  # M004
                        (worker, observed[worker])).rowcount
                if updated == 1:
                    events.append(self.event(worker, start, "ACCEPT", ["consumed"], observed[worker]))
                else:
                    events.append(self.event(worker, start, "CONFLICT"))
            if used != set(observed):
                raise ContractError("unfinished schedule")
            return {"results": events}
        if op == "confirm":
            if not self.permits(request["proof"], request["policy"]):
                return {"results": [self.event("operation", before, "REJECT")]}
            matches = 0
            for attestation in request["evidence"]:
                _, data = unpack(attestation)
                if not valid_signature(attestation):
                    continue
                if attestation["public_key_hex"] != request["policy"]["evidence_key"]:
                    continue
                expected = (body["operation_id"], body["scope"])
                if (data["operation_id"], data["scope"]) == expected and data["kind"] in request["policy"]["evidence_kinds"]:
                    matches += 1
            if matches == 0:  # M008
                return {"results": [self.event("operation", before, "UNVERIFIABLE")]}
            self.store(candidate)
            return {"results": [self.event("operation", before, "ACCEPT", ["confirmed"])]}
        if op == "ingest":
            entries = []
            for path in request["paths"]:
                self.store(before)
                permitted = self.permits(request["proof"], request["policy"])  # M009
                if permitted:
                    self.store(candidate)
                entries.append(self.event(path, before, "ACCEPT" if permitted else "REJECT", ["admitted"] if permitted else []))
            return {"results": entries}
        raise ContractError("unsupported receipt-journal operation")

def run(request):
    journal = ReceiptJournal(request["state"])
    try:
        return journal.execute(request)
    finally:
        journal.db.close()
