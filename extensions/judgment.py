"""Additive Judgment record registration; all previous registries remain unchanged."""
from pathlib import Path
from runner.fixture_registry import Corpus,FixtureRegistry
from runner.expectation_registry import ExpectationRegistry
from runner.adapter_registry import Adapter,AdapterRegistry
from runner.relation_profile_registry import RelationProfileRegistry
from runner.relation_runtime import validate_envelope
from profiles.judgment.relation import make_profile as relation_profile
from profiles.judgment.expectation import make_profile as expectation_profile,EXPECTATION_ID
from adapters.judgment.model import evaluate,ADAPTER_ID
CORPUS_SHA256='783615ef63e80caec0ee9bcbf0648f65ec14504d42a3a2dc4d45b8afadea2c26'
def register(root,fixtures,expectations,adapters,relations):
    root=Path(root)
    fixtures.register(Corpus('judgment-record','extensions/judgment.corpus.v0.json',CORPUS_SHA256,validate_envelope))
    expectations.register(expectation_profile(root))
    existing=[next(a for p in expectations.identities() if (a:=adapters.resolve(ident,p)) is not None) for ident in adapters.identities()]
    adapters=AdapterRegistry([*existing,Adapter(ADAPTER_ID,(EXPECTATION_ID,),lambda request:evaluate(root,request))])
    relations.register(relation_profile(root))
    return fixtures,expectations,adapters,relations
def composition(root):return register(root,FixtureRegistry(),ExpectationRegistry(),AdapterRegistry(),RelationProfileRegistry())
def complete_composition(root):
    from extensions.aggregate import complete_composition as previous
    f,e,a,r,compatibility=previous(root)
    return (*register(root,f,e,a,r),compatibility)
