"""Trusted composition for relation-aware execution; data cannot import code."""
from extensions.defaults import composition as legacy
from profiles.legacy_relation import registration
from runner.relation_profile_registry import RelationProfileRegistry

def composition(root):
    fixtures,expectations,adapters=legacy(root)
    profile,binding=registration(root)
    return fixtures,expectations,adapters,RelationProfileRegistry([profile]),(binding,)
