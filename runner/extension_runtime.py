"""Registered discovery coordinates the existing admission and comparator."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
from runner.fixture_registry import FixtureRegistry
from runner.expectation_registry import ExpectationRegistry, UnknownProfile
from runner.expectation_contract import ProfileError
from runner.adapter_registry import Adapter
from runner.execution import run_profile, summary
from rsi.codec import encode


def diagnostic(record, status, reason):
    return {"fixture_id":record["fixture_id"],"fixture_source_id":record["fixture_source_id"],
            "profile_id":record["expectation_profile_id"],"status":status,"errors":[reason]}


class ContextAdapters:
    def __init__(self, registry, predictor):
        self.registry, self.predictor = registry, predictor
    def resolve(self, adapter_id, profile_id):
        target = self.registry.resolve(adapter_id, profile_id)
        if target is None:
            return None
        if target.evaluate is self.predictor:
            raise ProfileError("SELF_VALIDATION", "predictor cannot be the adapter")
        if not target.contextual:
            return target
        context = {"adapter_id":adapter_id,"adapter_version":target.version,"expectation_profile_id":profile_id}
        return Adapter(target.adapter_id, target.supported_profiles,
                       lambda request: target.invoke(request, deepcopy(context)), target.version)


def execute(root, fixtures, profiles, adapters):
    discovered = fixtures.discover(root)
    records = discovered["fixtures"]
    rows, admissions = [], {}
    if discovered["errors"]:
        # Ambiguous discovery is a configuration failure: execute nothing.
        rows.extend(discovered["errors"])
        rows.extend(diagnostic(r, "UNSUPPORTED", "CORPUS_CONFIGURATION_FAILED") for r in records)
    else:
        for profile_id in sorted({r["expectation_profile_id"] for r in records}):
            group = [r for r in records if r["expectation_profile_id"] == profile_id]
            invalid = [r for r in group if r["status"] == "INVALID_FIXTURE"]
            if invalid:
                rows.extend(diagnostic(r,"INVALID_FIXTURE" if r in invalid else "UNSUPPORTED",
                                       "FIXTURE_INVALID" if r in invalid else "PROFILE_FIXTURE_SET_INCOMPLETE") for r in group)
                continue
            try:
                profile = profiles.resolve(profile_id)
            except UnknownProfile:
                rows.extend(diagnostic(r,"UNSUPPORTED","UNKNOWN_PROFILE") for r in group)
                continue
            if {(r["fixture_source_id"],r["path"]) for r in group} != {(s.fixture_id,s.path) for s in profile.fixture_scope} or len(group) != len(profile.fixture_scope):
                rows.extend(diagnostic(r,"UNSUPPORTED","PROFILE_ERROR:REGISTRATION_SCOPE") for r in group)
                continue
            by_source = {r["fixture_source_id"]:r for r in group}
            owners, targets = {}, {}
            def plan(value):
                record = by_source[value["id"]]
                tasks = deepcopy(profile.plan(value))
                bindings = record["adapter_bindings"]
                if {t["adapter_id"] for t in tasks} != set(bindings):
                    raise ProfileError("ADAPTER_BINDING", "declared slots and execution plan differ")
                for task in tasks:
                    key = task["row_id"]
                    if key in owners:
                        raise ProfileError("CHECK_IDENTITY", "duplicate check identity in profile")
                    owners[key] = record
                    task["adapter_id"] = bindings[task["adapter_id"]]
                    targets[key] = task["adapter_id"]
                return tasks
            bound = replace(profile, plan=plan)
            result = run_profile(root,profile_id,ExpectationRegistry([bound]),ContextAdapters(adapters,profile.predictor))
            if result["profile_error"]:
                rows.extend(diagnostic(r,"UNSUPPORTED",result["profile_error"]) for r in group)
                continue
            admissions[profile_id] = result["expectation_admission"]
            for case in result["cases"]:
                owner = owners[case["key"]]
                # Compatibility record remains untouched inside the result.
                rows.append({"fixture_id":owner["fixture_id"],"fixture_source_id":owner["fixture_source_id"],
                             "profile_id":profile_id,"adapter_id":targets[case["key"]],
                             "status":"UNSUPPORTED" if case["status"] == "RUNNER_ERROR" else case["status"],
                             "diagnostic_kind":"EXECUTION_ERROR" if case["status"] == "RUNNER_ERROR" else None,
                             "result":case})
    rows.sort(key=lambda r:(r.get("fixture_id", ""),r.get("profile_id", ""),r.get("result",{}).get("key", ""),r.get("corpus_id", "")))
    return {"schema":"rsi-extension-report.v0","rows":rows,"totals":summary(rows),
            "discovery":discovered,"admissions":admissions}


def main():
    import argparse
    from extensions.defaults import composition
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    try:
        report = execute(root, *composition(root))
    except Exception as exc:
        report = {"schema":"rsi-extension-report.v0","rows":[{"status":"INVALID_FIXTURE","diagnostic_kind":"REGISTRATION_ERROR","error":type(exc).__name__}],
                  "totals":{"PASS":0,"FAIL":0,"INVALID_FIXTURE":1,"UNSUPPORTED":0}}
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_bytes(encode(report))
    print(encode(report["totals"]).decode())
    return 0 if not any(report["totals"][s] for s in ("FAIL","INVALID_FIXTURE","UNSUPPORTED")) else 1

if __name__ == "__main__":
    raise SystemExit(main())
