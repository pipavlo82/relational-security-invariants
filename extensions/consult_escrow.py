"""Static domain registration; existing default and first-domain tables frozen."""
from pathlib import Path
from runner.fixture_registry import Corpus, FixtureRegistry
from runner.expectation_registry import ExpectationRegistry
from runner.adapter_registry import Adapter, AdapterRegistry
from runner.relation_profile_registry import RelationProfileRegistry
from runner.relation_runtime import validate_envelope
from profiles.consult_escrow.relation import make_profile as relation_profile
from profiles.consult_escrow.expectation import make_profile as expectation_profile, EXPECTATION_ID
from adapters.consult_escrow.model import evaluate, ADAPTER_ID

CORPUS_SHA256 = "fa278237740376716e66bbe873752ef708ff62df10dc1d5f7c795ab3a9682f40"


def register(root, fixtures, expectations, adapters, relations):
    root = Path(root)
    fixtures.register(Corpus("consult-escrow-release", "extensions/consult_escrow.corpus.v0.json", CORPUS_SHA256, validate_envelope))
    expectations.register(expectation_profile(root))
    existing = [next(a for p in expectations.identities() if (a := adapters.resolve(ident, p)) is not None) for ident in adapters.identities()]
    adapters = AdapterRegistry([*existing, Adapter(ADAPTER_ID, (EXPECTATION_ID,), lambda request: evaluate(root, request))])
    relations.register(relation_profile(root))
    return fixtures, expectations, adapters, relations


def composition(root):
    return register(root, FixtureRegistry(), ExpectationRegistry(), AdapterRegistry(), RelationProfileRegistry())


def complete_composition(root):
    from extensions.tas import complete_composition as previous
    fixtures, expectations, adapters, relations, compatibility = previous(root)
    return (*register(root, fixtures, expectations, adapters, relations), compatibility)
