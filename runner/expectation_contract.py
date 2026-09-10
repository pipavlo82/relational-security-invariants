"""Atomic admission. Pinned declarations alone are not an oracle."""
from dataclasses import dataclass
from pathlib import Path
from rsi.codec import encode, decode, digest, raw_digest

class FixtureError(ValueError):
    pass

class ProfileError(ValueError):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code

@dataclass(frozen=True)
class FixtureDocument:
    fixture_id: str
    raw: bytes

    def value(self):
        return decode(self.raw, canonical=True)


def safe_path(root, relative):
    p = Path(relative)
    root = Path(root).resolve()
    if p.is_absolute() or ".." in p.parts or "\\" in relative or ":" in relative:
        raise ValueError("unsafe local evidence path")
    result = (root / p).resolve()
    if not result.is_relative_to(root):
        raise ValueError("evidence path escapes root")
    return result


def fixture_set_digest(fixtures):
    ids = [f.fixture_id for f in fixtures]
    if len(ids) != len(set(ids)) or not ids:
        raise FixtureError("duplicate or empty fixture set")
    return digest([{"fixture_id": f.fixture_id, "sha256": raw_digest(f.raw)}
                   for f in sorted(fixtures, key=lambda f: f.fixture_id)])


def load_fixtures(root, profile):
    documents = []
    for source in sorted(profile.fixture_scope, key=lambda s: s.fixture_id):
        try:
            raw = safe_path(root, source.path).read_bytes()
            value = decode(raw, canonical=True)
            if type(value) is not dict or value.get("id") != source.fixture_id:
                raise ValueError("registered fixture identity mismatch")
            profile.validate_fixture(value)
            documents.append(FixtureDocument(source.fixture_id, raw))
        except Exception as exc:
            raise FixtureError(source.fixture_id + ": " + str(exc)) from exc
    return tuple(documents)


class AdmittedExpectations:
    """Serialized immutable storage; callers only receive detached copies."""
    def __init__(self, profile_id, rows):
        self.profile_id = profile_id
        self._serialized = encode(rows)

    def for_fixture(self, fixture_id):
        return decode(self._serialized)[fixture_id]

    def fixture_ids(self):
        return tuple(sorted(decode(self._serialized)))


def admit(root, profile, fixtures):
    actual_ids = {f.fixture_id for f in fixtures}
    if actual_ids != {s.fixture_id for s in profile.fixture_scope}:
        raise ProfileError("FIXTURE_SCOPE", "registered fixture set differs")
    bound_digest = fixture_set_digest(fixtures)
    # Compute before reading the expectation artifact. Only detached fixture
    # data is passed to predictors; no artifact, root or expectation row.
    recomputed = {}
    try:
        for fixture in sorted(fixtures, key=lambda f: f.fixture_id):
            value = fixture.value()
            before = encode(value)
            prediction = profile.predictor(value)
            if encode(value) != before:
                raise ValueError("predictor mutated its challenge")
            profile.validate_prediction(prediction)
            recomputed[fixture.fixture_id] = decode(encode(prediction))
    except Exception as exc:
        raise ProfileError("PREDICTOR_ERROR", str(exc)) from exc
    try:
        raw = safe_path(root, profile.expectations_path).read_bytes()
        if raw_digest(raw) != profile.expectations_digest:
            raise ProfileError("ARTIFACT_DIGEST", "expectation artifact digest differs")
        artifact = decode(raw, canonical=True)
        fields = {"schema", "profile_id", "profile_version", "fixture_set_digest", "expectations"}
        if type(artifact) is not dict or set(artifact) != fields or artifact["schema"] != "rsi-expectations.v0":
            raise ValueError("unsupported expectation envelope")
        if artifact["profile_id"] != profile.profile_id or artifact["profile_version"] != profile.version:
            raise ProfileError("PROFILE_IDENTITY", "expectation profile identity differs")
        if artifact["fixture_set_digest"] != bound_digest:
            raise ProfileError("FIXTURE_SET_DIGEST", "expectations bind a different fixture set")
        if type(artifact["expectations"]) is not list:
            raise ValueError("expectations must be a list")
        rows = {}
        for row in artifact["expectations"]:
            if type(row) is not dict or set(row) != {"fixture_id", "prediction"}:
                raise ValueError("invalid expectation row shape")
            ident = row["fixture_id"]
            if type(ident) is not str or ident in rows:
                raise ProfileError("DUPLICATE_ROW", "duplicate or invalid fixture identity")
            profile.validate_prediction(row["prediction"])
            rows[ident] = row["prediction"]
        if set(rows) != actual_ids:
            raise ProfileError("ROW_SET", "missing or extra expectation row")
    except ProfileError:
        raise
    except Exception as exc:
        raise ProfileError("ARTIFACT_INVALID", str(exc)) from exc
    mismatches, staged = [], {}
    for ident in sorted(actual_ids):
        recorded = rows[ident]
        if encode(recomputed[ident]) != encode(recorded):  # EXP-M3
            mismatches.append(ident)
        else:
            staged[ident] = recorded
    if mismatches:  # EXP-M4: one mismatch prevents admission of every row
        raise ProfileError("PREDICTION_MISMATCH", "independent prediction disagrees: " + ",".join(mismatches))
    return AdmittedExpectations(profile.profile_id, staged)
