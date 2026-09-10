"""Compatibility profile. Original predictor and corpus guarantees stay intact."""
from pathlib import Path
from rsi.codec import encode, load
from rsi.oracle import predict, local_validity
from rsi.corpus import verify, validator
from runner.expectation_registry import ExpectationProfile, FixtureSource

PROFILE_ID = "core.synthetic.v0"
# Historical execution order is explicit configuration, not registry order.
ADAPTER_ORDER = ("messaging", "generic")


def predict_fixture(fixture):
    result = {}
    for case in fixture["cases"]:
        for adapter, request in case["requests"].items():
            key = fixture["id"] + "/" + case["name"] + "/" + adapter
            result[key] = {"local_validity": local_validity(request), "observation": predict(request)}
    return result


def plan_fixture(fixture):
    return [{"row_id":fixture["id"] + "/" + case["name"] + "/" + adapter,
             "adapter_id":adapter,"request":case["requests"][adapter]}
            for case in fixture["cases"] for adapter in ADAPTER_ORDER]


def make_profile(root):
    root = Path(root)
    meta = load(root/"profiles/core.synthetic.v0.json")
    required = {"schema", "profile_id", "version", "fixture_scope", "expectations_path", "expectations_digest"}
    if set(meta) != required or meta["schema"] != "rsi-expectation-profile.v0" or meta["profile_id"] != PROFILE_ID or meta["version"] != "0":
        raise ValueError("invalid static synthetic profile registration")
    fixture_validator = validator(root/"schema/relation-binding-fixture.v0.schema.json")
    output_validator = validator(root/"schema/observation.v0.schema.json")
    def validate_prediction(value):
        if type(value) is not dict or not value:
            raise ValueError("expected nonempty prediction mapping")
        for key, entry in value.items():
            if type(key) is not str or not key or type(entry) is not dict or set(entry) != {"local_validity", "observation"} or type(entry["local_validity"]) is not bool:
                raise ValueError("invalid prediction record")
            output_validator.validate(entry["observation"])
    return ExpectationProfile(meta["profile_id"], meta["version"],
        tuple(FixtureSource(**item) for item in meta["fixture_scope"]), predict_fixture,
        meta["expectations_path"],meta["expectations_digest"],fixture_validator.validate,
        validate_prediction,plan_fixture,lambda directory: verify(directory))
