"""Explicit compatibility binding; legacy fixture interpretation is unchanged."""
from dataclasses import dataclass
from rsi.codec import load
from rsi.corpus import validator
from runner.relation_profile import Relation, RelationProfile

@dataclass(frozen=True)
class LegacyBinding:
    corpus_id: str
    profile_id: str
    version: str
    validate_fixture: object
    def matches(self, record):
        return record["corpus_id"] == self.corpus_id
    def validate(self, fixture, registry):
        self.validate_fixture(fixture)
        profile=registry.resolve(self.profile_id,self.version,fixture["protected_relation"])
        profile.validate(fixture["protected_relation"],{"fixture":fixture})

def registration(root):
    schema=load(root/"schema/relation-binding-fixture.v0.schema.json")
    validate=validator(root/"schema/relation-binding-fixture.v0.schema.json").validate
    def validate_input(value): validate(value["fixture"])
    def interpret(value, context):
        # Validation/interpretation only. Existing adapters still own actuals.
        validate(value["fixture"])
        return {"relation_id":value["fixture"]["protected_relation"],"relation_state":"delegated","outputs":{}}
    def validate_output(value):
        if value["relation_state"]!="delegated" or value["outputs"]!={}:raise ValueError("compatibility output")
    profile=RelationProfile("core.synthetic.v0","0",tuple(
        Relation(name,("fixture",),(),validate_input,interpret,validate_output)
        for name in schema["properties"]["protected_relation"]["enum"]))
    return profile,LegacyBinding("core",profile.profile_id,profile.version,validate)
