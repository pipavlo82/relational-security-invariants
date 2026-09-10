"""Project-neutral admission -> execution -> exact comparison."""
from copy import deepcopy
from rsi.codec import digest, encode
from runner.expectation_contract import load_fixtures, admit, fixture_set_digest, FixtureError, ProfileError
from runner.expectation_registry import UnknownProfile

TOP_STATES = ("PASS", "FAIL", "INVALID_FIXTURE", "UNSUPPORTED")


def summary(rows):
    counts = {s: 0 for s in TOP_STATES}
    for row in rows:
        state = row["status"]
        # Preserve diagnostic execution errors; a checker that crashes did not
        # successfully execute its contract. Profile availability is separate.
        counts["FAIL" if state == "RUNNER_ERROR" else state] += 1
    return counts


def unavailable(profile_id, code, message, status="UNSUPPORTED"):
    return {"cases": [{"key": profile_id, "status": status, "errors": [code], "message": message}], "profile_error": code}


def run_profile(root, profile_id, profiles, adapters):
    try:
        profile = profiles.resolve(profile_id)
    except UnknownProfile:
        return unavailable(profile_id, "UNKNOWN_PROFILE", "expectation profile is not registered")
    try:
        fixtures = load_fixtures(root, profile)
    except FixtureError as exc:
        return unavailable(profile_id, "FIXTURE_INVALID", str(exc), "INVALID_FIXTURE")
    try:
        profile.validate_scope(root)
        admitted = admit(root, profile, fixtures)
        # Validate every plan before any adapter executes. Plans are independent
        # of expectation rows; row identity is only an exact lookup key.
        plans = []
        for fixture in fixtures:
            plan = deepcopy(profile.plan(fixture.value()))
            if type(plan) is not list or any(type(task) is not dict or set(task) != {"row_id", "adapter_id", "request"} or type(task["row_id"]) is not str or not task["row_id"] or type(task["adapter_id"]) is not str or not task["adapter_id"] for task in plan):
                raise ProfileError("PLAN_MISMATCH", "invalid execution plan")
            encode(plan)
            ids = [task["row_id"] for task in plan]
            if len(ids) != len(set(ids)) or set(ids) != set(admitted.for_fixture(fixture.fixture_id)):
                raise ProfileError("PLAN_MISMATCH", "execution plan and admitted rows differ")
            for task in plan:
                target = adapters.resolve(task["adapter_id"], profile_id)
                if target is not None and target.evaluate is profile.predictor:
                    raise ProfileError("SELF_VALIDATION", "predictor and adapter must be separate implementations")
            plans.append((fixture, plan))
    except ProfileError as exc:
        return unavailable(profile_id, "PROFILE_ERROR:" + exc.code, str(exc))
    except Exception as exc:
        return unavailable(profile_id, "PROFILE_ERROR:VALIDATION", str(exc))
    rows = []
    for fixture, plan in plans:
        expected_rows = admitted.for_fixture(fixture.fixture_id)
        for task in plan:
            reference = expected_rows[task["row_id"]]
            adapter = adapters.resolve(task["adapter_id"], profile_id)
            if adapter is None:
                rows.append({"key": task["row_id"], "status": "UNSUPPORTED", "errors": ["UNKNOWN_ADAPTER"]})
                continue
            request = deepcopy(task["request"])
            input_digest = digest(request)
            actual, errors = None, []
            try:
                actual = adapter.evaluate(request)
                profile.validate_prediction({task["row_id"]: {"local_validity": reference["local_validity"], "observation": actual}})
                if digest(request) != input_digest:
                    raise RuntimeError("adapter mutated its supplied challenge")
                state = "PASS" if encode(actual) == encode(reference["observation"]) else "FAIL"
            except Exception as exc:
                actual, state, errors = None, "RUNNER_ERROR", [type(exc).__name__]
            rows.append({"key":task["row_id"], "status":state, "input_digest":input_digest,
                         "local_validity":reference["local_validity"], "expected":reference["observation"],
                         "observed":actual, "errors":errors})
    return {"cases": rows, "profile_error": None, "expectation_admission": {"profile_id":profile.profile_id,"profile_version":profile.version,"fixture_set_digest":fixture_set_digest(fixtures),"expectations_sha256":profile.expectations_digest}}


def run_registered(root, profiles, adapters):
    """Independent atomic admission per profile, in stable registration order."""
    results = {ident: run_profile(root, ident, profiles, adapters) for ident in profiles.identities()}
    return {"profiles": results, "totals": summary([row for result in results.values() for row in result["cases"]])}
