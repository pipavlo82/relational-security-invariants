"""Explicit Crystal Receipt registration; existing default corpora stay frozen."""
from pathlib import Path
from runner.fixture_registry import Corpus,FixtureRegistry
from runner.expectation_registry import ExpectationRegistry
from runner.adapter_registry import Adapter,AdapterRegistry
from runner.relation_profile_registry import RelationProfileRegistry
from runner.relation_runtime import validate_envelope
from profiles.crystal_receipt.relation import make_profile as relation_profile
from profiles.crystal_receipt.expectation import make_profile as expectation_profile,EXPECTATION_ID
from adapters.crystal_receipt.model import evaluate,ADAPTER_ID
CORPUS_SHA256="a5c78c6e2dbdecd36a73acf9970599274313b6c0b7c4ee7d144d5d3aaee8ca33"

def register(root,fixtures,expectations,adapters,relations):
    root=Path(root)
    fixtures.register(Corpus("crystal-receipt","extensions/crystal-receipt.corpus.v0.json",CORPUS_SHA256,validate_envelope))
    expectations.register(expectation_profile(root))
    existing=[]
    for ident in adapters.identities():
        existing.append(next(a for p in expectations.identities() if (a:=adapters.resolve(ident,p)) is not None))
    adapters=AdapterRegistry([*existing,Adapter(ADAPTER_ID,(EXPECTATION_ID,),lambda request:evaluate(root,request))])
    relations.register(relation_profile(root))
    return fixtures,expectations,adapters,relations

def composition(root):
    values=FixtureRegistry(),ExpectationRegistry(),AdapterRegistry(),RelationProfileRegistry()
    return register(root,*values)

def complete_composition(root):
    from extensions.relations import composition as legacy
    fixtures,expectations,adapters,relations,compatibility=legacy(root)
    return (*register(root,fixtures,expectations,adapters,relations),compatibility)
