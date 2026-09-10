"""Relation dependency admission around the unchanged extension pipeline."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from jsonschema import Draft202012Validator
from rsi.codec import encode, load, raw_digest
from runner.extension_runtime import execute as execute_extensions, diagnostic
from runner.execution import summary
from runner.expectation_contract import ProfileError, safe_path
from runner.expectation_registry import ExpectationRegistry, UnknownProfile
from runner.relation_profile import identifier
from runner.relation_profile_registry import RelationProfileRegistry, UnavailableRelation

SCHEMA = "profiled-relation-fixture.v0"
SCHEMA_PATH = Path(__file__).resolve().parents[1] / "schema/profiled-relation-fixture.v0.schema.json"


def validate_envelope(value):
    Draft202012Validator(load(SCHEMA_PATH)).validate(value)
    ids = [c["case_id"] for c in value["cases"]]
    if not all(identifier(v) for v in ids + [value[k] for k in ("id", "relation_profile_id", "relation_profile_version", "relation_id")]):
        raise ValueError("invalid exact identifier")
    if len(set(ids)) != len(ids):
        raise ValueError("duplicate case identity")


def resolve_fixture(value, registry):
    validate_envelope(value)
    profile = registry.resolve(value["relation_profile_id"], value["relation_profile_version"],
                               value["relation_id"], value.get("relation_profile_sha256"))
    for case in value["cases"]:
        profile.validate(value["relation_id"], case["inputs"])
    return profile


def plan(value, adapter_id):
    return [{"row_id": value["id"] + "/" + c["case_id"], "adapter_id": adapter_id,
             "request": {"relation_profile_id": value["relation_profile_id"],
                         "relation_profile_version": value["relation_profile_version"],
                         "relation_id": value["relation_id"], "inputs": deepcopy(c["inputs"])}}
            for c in value["cases"]]


class SnapshotDiscovery:
    def __init__(self, value):
        self.value = value
    def discover(self, root):
        return deepcopy(self.value)


def execute(root, fixtures, expectations, adapters, relations=None, compatibility=()):
    registry = relations if relations is not None else RelationProfileRegistry()
    discovered = fixtures.discover(root)
    if discovered["errors"]:
        return execute_extensions(root, SnapshotDiscovery(discovered), expectations, adapters)
    blocked, ready, bindings = [], [], {}
    for record in discovered["fixtures"]:
        if record["status"] == "INVALID_FIXTURE":
            ready.append(record)
            continue
        try:
            value = load(safe_path(root, record["path"]))
            if value.get("schema") == SCHEMA:
                profile = resolve_fixture(value, registry)  # RP-M1 required resolution
                bindings[(record["expectation_profile_id"], record["fixture_source_id"])] = (value, profile, record["fixture_sha256"])
            else:
                # Explicit compatibility registrations own their legacy validation.
                for binding in compatibility:
                    if binding.matches(record):
                        binding.validate(value, registry)
            ready.append(record)
        except UnavailableRelation as exc:
            blocked.append(diagnostic(record, "UNSUPPORTED", str(exc)))
        except Exception as exc:
            blocked.append(diagnostic(record, "INVALID_FIXTURE", type(exc).__name__))
    bad_profiles = {r["profile_id"] for r in blocked}
    survivors = []
    for record in ready:
        if record["expectation_profile_id"] in bad_profiles:
            blocked.append(diagnostic(record, "UNSUPPORTED", "RELATION_PROFILE_SET_INCOMPLETE"))
        else:
            survivors.append(record)
    wrapped = []
    for ident in sorted({r["expectation_profile_id"] for r in survivors}):
        try:
            original = expectations.resolve(ident)
        except UnknownProfile:
            continue
        owned = {r["fixture_source_id"]: bindings[(ident, r["fixture_source_id"])] for r in survivors
                 if r["expectation_profile_id"] == ident and (ident, r["fixture_source_id"]) in bindings}
        def validation(value, original=original, owned=owned):
            original.validate_fixture(value)
            if value["id"] in owned:
                saved, profile, pin = owned[value["id"]]
                if raw_digest(encode(value)) != pin:
                    raise ValueError("fixture changed after relation validation")
                resolve_fixture(value, registry)
        def scope(directory, original=original, owned=owned):
            original.validate_scope(directory)
            for value, profile, pin in owned.values():
                if any(original.predictor is r.evaluate for r in profile.relations):
                    raise ProfileError("SELF_VALIDATION", "relation evaluator cannot be expectation predictor")
        def bound_plan(value, original=original, owned=owned):
            tasks = original.plan(value)
            if value["id"] in owned:
                expected = {t["row_id"]: encode(t["request"]) for t in plan(value, "slot")}
                if {t["row_id"]: encode(t["request"]) for t in tasks} != expected:
                    raise ProfileError("RELATION_INPUT_BINDING", "plan changed relation inputs")
            return tasks
        def prediction(value, original=original, owned=owned):
            original.validate_prediction(value)
            checks = {t["row_id"]: (profile, fixture["relation_id"])
                      for fixture, profile, pin in owned.values() for t in original.plan(fixture)}
            for key, entry in value.items():
                if key in checks:
                    profile, relation_id = checks[key]
                    profile.validate_result(relation_id, entry["observation"])
        wrapped.append(replace(original, validate_fixture=validation, validate_scope=scope,
                               plan=bound_plan, validate_prediction=prediction))
    result = execute_extensions(root, SnapshotDiscovery({"fixtures": survivors, "errors": []}),
                                ExpectationRegistry(wrapped), adapters)  # RP-M7 admission remains mandatory
    result["rows"].extend(blocked)
    result["rows"].sort(key=lambda r: (r["fixture_id"], r.get("result", {}).get("key", "")))
    result["totals"] = summary(result["rows"])
    result["discovery"] = discovered
    return result


def main():
    import argparse
    from extensions.relations import composition
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",type=Path,default=Path("artifacts/relations.json"))
    args=parser.parse_args()
    root=Path(__file__).resolve().parents[1]
    result=execute(root,*composition(root))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_bytes(encode(result))
    print(result["totals"])
    return 0 if not any(result["totals"][s] for s in ("FAIL","INVALID_FIXTURE","UNSUPPORTED")) else 1

if __name__=="__main__":raise SystemExit(main())
