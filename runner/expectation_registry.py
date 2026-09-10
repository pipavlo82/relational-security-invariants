"""Explicit registration of trusted code, never names imported from input."""
from dataclasses import dataclass
import re

class RegistryError(ValueError):
    pass

class UnknownProfile(LookupError):
    pass

@dataclass(frozen=True)
class FixtureSource:
    fixture_id: str
    path: str

@dataclass(frozen=True)
class ExpectationProfile:
    profile_id: str
    version: str
    fixture_scope: tuple
    predictor: object
    expectations_path: str
    expectations_digest: str
    validate_fixture: object
    validate_prediction: object
    plan: object
    validate_scope: object

class ExpectationRegistry:
    def __init__(self, profiles=()):
        self._profiles = {}
        for profile in profiles:
            self.register(profile)

    def register(self, profile):
        if not isinstance(profile, ExpectationProfile):
            raise RegistryError("expected trusted ExpectationProfile")
        if not re.fullmatch(r"[a-z0-9][a-z0-9._-]{0,127}", profile.profile_id):
            raise RegistryError("invalid profile identity")
        if profile.profile_id in self._profiles:
            raise RegistryError("duplicate profile identity")
        if not isinstance(profile.version, str) or not profile.version or not profile.version.isascii():
            raise RegistryError("invalid profile version")
        if type(profile.fixture_scope) is not tuple or not profile.fixture_scope:
            raise RegistryError("explicit nonempty immutable fixture scope required")
        ids = [f.fixture_id for f in profile.fixture_scope]
        paths = [f.path for f in profile.fixture_scope]
        if len(ids) != len(set(ids)) or len(paths) != len(set(paths)):
            raise RegistryError("duplicate fixture identity/path")
        if any(not isinstance(x, str) or not x or not x.isascii() for x in ids + paths):
            raise RegistryError("invalid fixture identity/path")
        if not re.fullmatch(r"[0-9a-f]{64}", profile.expectations_digest):
            raise RegistryError("invalid expectation digest")
        for name in ("predictor", "validate_fixture", "validate_prediction", "plan", "validate_scope"):
            if not callable(getattr(profile, name)):
                raise RegistryError("registration must supply trusted callable: " + name)
        self._profiles[profile.profile_id] = profile

    def resolve(self, profile_id):
        try:
            return self._profiles[profile_id]
        except KeyError:
            raise UnknownProfile(profile_id) from None

    def identities(self):
        return tuple(sorted(self._profiles))
