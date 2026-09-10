"""Frozen historical source patches, explicitly registered outside the core."""
def definitions():
    records = []
    patches = {
      "messaging": {
        "RSI-001": ('subject_ok = proof["public_key_hex"] == policy["subject_key"]  # M001', 'subject_ok = True  # M001'),
        "RSI-003": ('authenticated = self.allowed(req["proof"], req["policy"])  # M003', 'self.state = candidate\n            authenticated = self.allowed(req["proof"], req["policy"])  # M003'),
        "RSI-004": ('if self.state["revision"] != reads[worker]:  # M004', 'if False:  # M004'),
        "RSI-006": ('scope_ok = body["scope"] == policy["scope"]  # M006', 'scope_ok = True  # M006'),
        "RSI-008": ('if not any(qualified):  # M008', 'if False:  # M008'),
        "RSI-009": ('ok = self.allowed(req["proof"], req["policy"])  # M009', 'ok = path == "import" or self.allowed(req["proof"], req["policy"])  # M009'),
      },
      "generic": {
        "RSI-001": ('if proof["public_key_hex"] != policy["subject_key"]:  # M001', 'if False:  # M001'),
        "RSI-003": ('permitted = self.permits(request["proof"], request["policy"])  # M003', 'if op == "transition":\n                self.store(candidate)\n            permitted = self.permits(request["proof"], request["policy"])  # M003'),
        "RSI-004": ('WHERE id=1 AND revision=?",  # M004', 'WHERE id=1 AND ? >= 0",  # M004'),
        "RSI-006": ('if record["scope"] != policy["scope"]:  # M006', 'if False:  # M006'),
        "RSI-008": ('if matches == 0:  # M008', 'if False:  # M008'),
        "RSI-009": ('permitted = self.permits(request["proof"], request["policy"])  # M009', 'permitted = path == "import" or self.permits(request["proof"], request["policy"])  # M009'),
      }}
    for adapter, family in patches.items():
        for ident, (old, new) in family.items():
            records.append({"id": ident + "/" + adapter, "target_adapter_id": adapter, "path": "adapters/" + adapter + "/model.py",
                "old": old, "new": new, "mapped_cases": [ident + "/mutation/" + adapter]})
    return records
