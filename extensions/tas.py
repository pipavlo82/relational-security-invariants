"""Static domain registration; existing default and first-domain tables frozen."""
from pathlib import Path
from runner.fixture_registry import Corpus, FixtureRegistry
from runner.expectation_registry import ExpectationRegistry
from runner.adapter_registry import Adapter, AdapterRegistry
from runner.relation_profile_registry import RelationProfileRegistry
from runner.relation_runtime import validate_envelope
from profiles.tas.relation import make_profile as relation_profile
from profiles.tas.expectation import make_profile as expectation_profile, EXPECTATION_ID
from adapters.tas.model import evaluate, ADAPTER_ID

CORPUS_SHA256 = "342a79ee363fac9d559c7870ccb64b88920750fc02510af727ec4c82f479ec5d"


def register(root, fixtures, expectations, adapters, relations):
    root = Path(root)
    fixtures.register(Corpus("tas-context-invocation", "extensions/tas.corpus.v0.json", CORPUS_SHA256, validate_envelope))
    expectations.register(expectation_profile(root))
    existing = [next(a for p in expectations.identities() if (a := adapters.resolve(ident, p)) is not None) for ident in adapters.identities()]
    adapters = AdapterRegistry([*existing, Adapter(ADAPTER_ID, (EXPECTATION_ID,), lambda request: evaluate(root, request))])
    relations.register(relation_profile(root))
    return fixtures, expectations, adapters, relations


def composition(root):
    return register(root, FixtureRegistry(), ExpectationRegistry(), AdapterRegistry(), RelationProfileRegistry())


def complete_composition(root):
    from extensions.pq import complete_composition as previous
    fixtures, expectations, adapters, relations, compatibility = previous(root)
    return (*register(root, fixtures, expectations, adapters, relations), compatibility)
