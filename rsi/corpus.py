"""Verify the complete stored corpus, byte contract and detached oracle before execution."""
from pathlib import Path
from jsonschema import Draft202012Validator
from rsi.codec import load, encode, raw_digest, ContractError
from rsi.oracle import predict, local_validity

FAMILIES = {
    "RSI-001": ("signer_to_subject", "relation_substitution", "admit"),
    "RSI-003": ("authentication_before_commit", "invalid_authentication", "transition"),
    "RSI-004": ("atomic_consumption", "concurrent_schedule", "consume"),
    "RSI-006": ("context_binding", "relation_substitution", "admit"),
    "RSI-008": ("evidence_bounded_status", "relation_substitution", "confirm"),
    "RSI-009": ("ingestion_equivalence", "cross_path", "ingest"),
}

def validator(path):
    schema = load(path)
    def visit(value):
        if isinstance(value, dict):
            if "$ref" in value and not value["$ref"].startswith("#/"):
                raise ContractError("external schema references forbidden")
            for child in value.values():
                visit(child)
        elif isinstance(value, list):
            for child in value:
                visit(child)
    visit(schema)
    Draft202012Validator.check_schema(schema)
    return Draft202012Validator(schema)

def safe_file(root, name):
    p = Path(name)
    if p.is_absolute() or ".." in p.parts or "\\" in name:
        raise ContractError("unsafe manifest path")
    target = (root / p).resolve()
    if not target.is_relative_to(root.resolve()) or not target.is_file():
        raise ContractError("missing or escaping pinned file")
    return target

def verify(root):
    root = Path(root)
    manifest = load(root / "manifest.json")
    if set(manifest) != {"schema", "serializer", "files", "fixture_ids"}:
        raise ContractError("unexpected manifest fields")
    if manifest["schema"] != "rsi-corpus.v0" or manifest["serializer"] != "rsi-json-ascii.v0":
        raise ContractError("unsupported manifest")
    if sorted(manifest["fixture_ids"]) != sorted(FAMILIES):
        raise ContractError("incomplete or duplicate fixture-id universe")
    pinned = manifest["files"]
    if type(pinned) is not dict:
        raise ContractError("invalid pin map")
    required = {"schema/relation-binding-fixture.v0.schema.json", "schema/observation.v0.schema.json", "oracle/expected.v0.json"}
    actual_fixtures = {p.relative_to(root).as_posix() for p in (root / "fixtures").glob("*.json")}
    expected_files = required | actual_fixtures
    if set(pinned) != expected_files or len(actual_fixtures) != len(FAMILIES):
        raise ContractError("pin inventory mismatch")
    for name, expected_hash in pinned.items():
        raw = safe_file(root, name).read_bytes()
        if raw_digest(raw) != expected_hash:
            raise ContractError("raw-byte pin mismatch: " + name)
        load(root / name)
    schema = validator(root / "schema/relation-binding-fixture.v0.schema.json")
    observation_schema = validator(root / "schema/observation.v0.schema.json")
    stored = load(root / "oracle/expected.v0.json")
    if set(stored) != {"schema", "expectations"} or stored["schema"] != "rsi-oracle-set.v0":
        raise ContractError("unsupported oracle set")
    fixtures, derived, seen = [], {}, set()
    mutation_path = {
        "RSI-001": ("policy", "subject_key"), "RSI-003": ("proof", "signature_hex"),
        "RSI-004": ("schedule",), "RSI-006": ("policy", "scope"),
        "RSI-008": ("evidence",), "RSI-009": ("policy", "policy_version"),
    }
    def erase_endpoint(request, parts):
        import copy
        result = copy.deepcopy(request)
        parent = result
        for component in parts[:-1]:
            parent = parent[component]
        parent[parts[-1]] = "<protected-endpoint>"
        return result
    for name in sorted(actual_fixtures):
        f = load(root / name)
        schema.validate(f)
        ident = f["id"]
        if ident in seen:
            raise ContractError("duplicate fixture id")
        seen.add(ident)
        relation, mutation_model, operation = FAMILIES[ident]
        if (f["protected_relation"], f["mutation_model"]) != (relation, mutation_model):
            raise ContractError("wrong protected relation or mutation class")
        if sorted(c["name"] for c in f["cases"]) != ["control", "mirror_positive", "mutation"]:
            raise ContractError("case roles missing or repeated")
        for c in f["cases"]:
            for adapter, req in c["requests"].items():
                if req["operation"] != operation:
                    raise ContractError("wrong operation for protected relation")
                valid = local_validity(req)
                required_local = not (ident == "RSI-003" and c["name"] == "mutation")
                if valid is not c["local_validity_expected"] or valid is not required_local:
                    raise ContractError("local validity claim or mutation-class obligation not reproduced")
                out = predict(req)
                observation_schema.validate(out)
                decisions = [e["decision"] for e in out["results"]]
                if c["name"] == "mutation" and all(d == "ACCEPT" for d in decisions):
                    raise ContractError("negative case without negative oracle obligation")
                if c["name"] != "mutation" and any(d != "ACCEPT" for d in decisions):
                    raise ContractError("positive control does not accept")
                key = ident + "/" + c["name"] + "/" + adapter
                derived[key] = {"local_validity": valid, "observation": out}
        roles = {case["name"]: case for case in f["cases"]}
        for adapter in ("messaging", "generic"):
            original = roles["control"]["requests"][adapter]
            changed = roles["mutation"]["requests"][adapter]
            if encode(original) == encode(changed):
                raise ContractError("mutation must change its protected endpoint or schedule")
            if encode(erase_endpoint(original, mutation_path[ident])) != encode(erase_endpoint(changed, mutation_path[ident])):
                raise ContractError("mutation changes unrelated inputs")
            if original["proof"]["payload_hex"] == roles["mirror_positive"]["requests"][adapter]["proof"]["payload_hex"]:
                raise ContractError("mirror must change signed representation")
            control = derived[ident + "/control/" + adapter]
            mirror = derived[ident + "/mirror_positive/" + adapter]
            if encode(control) != encode(mirror):
                raise ContractError("mirror changes protected output")
        fixtures.append(f)
    if seen != set(FAMILIES) or encode(derived) != encode(stored["expectations"]):
        raise ContractError("detached oracle not independently reproduced")
    return fixtures, derived
