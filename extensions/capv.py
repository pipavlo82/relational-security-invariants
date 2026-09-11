"""Additive CAPV registration; all previous registries remain unchanged."""
from pathlib import Path
from runner.fixture_registry import Corpus,FixtureRegistry
from runner.expectation_registry import ExpectationRegistry
from runner.adapter_registry import Adapter,AdapterRegistry
from runner.relation_profile_registry import RelationProfileRegistry
from runner.relation_runtime import validate_envelope
from profiles.capv.relation import make_profile as relation_profile
from profiles.capv.expectation import make_profile as expectation_profile,EXPECTATION_ID
from adapters.capv.model import evaluate,ADAPTER_ID
CORPUS_SHA256='710082ab547091855bb5fc1065e19e60ceff2017bc44b5a94216d1211fdea335'
def register(root,fixtures,expectations,adapters,relations):
    root=Path(root)
    fixtures.register(Corpus('capv-expiry-generation','extensions/capv.corpus.v0.json',CORPUS_SHA256,validate_envelope))
    expectations.register(expectation_profile(root))
    existing=[next(a for p in expectations.identities() if (a:=adapters.resolve(ident,p)) is not None) for ident in adapters.identities()]
    adapters=AdapterRegistry([*existing,Adapter(ADAPTER_ID,(EXPECTATION_ID,),lambda request:evaluate(root,request))])
    relations.register(relation_profile(root))
    return fixtures,expectations,adapters,relations
def composition(root):return register(root,FixtureRegistry(),ExpectationRegistry(),AdapterRegistry(),RelationProfileRegistry())
def complete_composition(root):
    from extensions.verify_layer import complete_composition as previous
    f,e,a,r,compatibility=previous(root)
    return (*register(root,f,e,a,r),compatibility)
