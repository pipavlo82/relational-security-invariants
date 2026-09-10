"""Exact, deterministic lookup of statically supplied relation contracts."""
import re
from runner.relation_profile import Relation, RelationProfile, identifier


class UnavailableRelation(LookupError):
    pass


class RelationProfileRegistry:
    def __init__(self, profiles=()):
        self._profiles = {}
        for profile in profiles:
            self.register(profile)

    def register(self, profile):
        if not isinstance(profile, RelationProfile) or not identifier(profile.profile_id) or not identifier(profile.version):
            raise ValueError("invalid profile identity/version")
        if type(profile.relations) is not tuple or not profile.relations:
            raise ValueError("immutable nonempty relations required")
        if profile.descriptor_sha256 is not None and re.fullmatch(r"[0-9a-f]{64}", profile.descriptor_sha256) is None:
            raise ValueError("invalid descriptor pin")
        names = set()
        for relation in profile.relations:
            if not isinstance(relation, Relation) or not identifier(relation.relation_id) or relation.relation_id in names:
                raise ValueError("duplicate or invalid relation")
            names.add(relation.relation_id)
            if type(relation.required_slots) is not tuple or type(relation.optional_slots) is not tuple:
                raise ValueError("immutable slots required")
            slots = relation.required_slots + relation.optional_slots
            if len(set(slots)) != len(slots) or any(not identifier(s) for s in slots):
                raise ValueError("invalid or overlapping slots")
            if any(not callable(f) for f in (relation.validate_inputs, relation.evaluate, relation.validate_outputs)):
                raise ValueError("trusted contracts required")
        key = (profile.profile_id, profile.version)
        if key in self._profiles:
            raise ValueError("duplicate profile/version")
        self._profiles[key] = profile

    def identities(self):
        return tuple(sorted(self._profiles))

    def resolve(self, profile_id, version, relation_id, descriptor_sha256=None):
        profile = self._profiles.get((profile_id, version))  # RP-M2 exact version
        if profile is None or profile.relation(relation_id) is None:
            raise UnavailableRelation("unknown profile/version/relation")
        if descriptor_sha256 is not None and descriptor_sha256 != profile.descriptor_sha256:
            raise UnavailableRelation("descriptor identity differs")
        return profile
