"""Additive Aggregate Budget registration; all previous registries remain unchanged."""
from pathlib import Path
from runner.fixture_registry import Corpus,FixtureRegistry
from runner.expectation_registry import ExpectationRegistry
from runner.adapter_registry import Adapter,AdapterRegistry
from runner.relation_profile_registry import RelationProfileRegistry
from runner.relation_runtime import validate_envelope
from profiles.aggregate.relation import make_profile as relation_profile
from profiles.aggregate.expectation import make_profile as expectation_profile,EXPECTATION_ID
from adapters.aggregate.model import evaluate,ADAPTER_ID
CORPUS_SHA256='7a8123f6c10dd77a7335399d55f8923ddb3eff1dfbfbd45b0a1bcbbb382916eb'
def register(root,fixtures,expectations,adapters,relations):
    root=Path(root)
    fixtures.register(Corpus('aggregate-budget','extensions/aggregate.corpus.v0.json',CORPUS_SHA256,validate_envelope))
    expectations.register(expectation_profile(root))
    existing=[next(a for p in expectations.identities() if (a:=adapters.resolve(ident,p)) is not None) for ident in adapters.identities()]
    adapters=AdapterRegistry([*existing,Adapter(ADAPTER_ID,(EXPECTATION_ID,),lambda request:evaluate(root,request))])
    relations.register(relation_profile(root))
    return fixtures,expectations,adapters,relations
def composition(root):return register(root,FixtureRegistry(),ExpectationRegistry(),AdapterRegistry(),RelationProfileRegistry())
def complete_composition(root):
    from extensions.capv import complete_composition as previous
    f,e,a,r,compatibility=previous(root)
    return (*register(root,f,e,a,r),compatibility)
