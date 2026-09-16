"""Declared claim-edge compatibility, never proof of declaration truth."""
from jsonschema import Draft202012Validator
from runner.relation_profile import Relation, RelationProfile
from rsi.codec import domain, decode
from profiles.semantic_abi.source import read_sources, SOURCE_PIN_SHA256
PROFILE_ID='semantic-abi.claim-edge.v0'
VERSION='0'
RELATION_ID='claim-authority-scope-time-binding'

def validate_inputs(root,v):
    domain(v)
    if type(v) is not dict or set(v)!={'producer','requirement'}:raise ValueError('slots')
    _,blobs=read_sources(root)
    schema=decode(blobs['evidence/semantic-abi/schema/manifest.schema.json'])
    def validate_kind(value,kind):
        Draft202012Validator({'$ref':'#/$defs/'+kind,'$defs':schema['$defs']}).validate(value)
    p=v['producer']
    if type(p) is not dict or set(p)!={'component','establishes','does_not_establish'}:raise ValueError('producer')
    if type(p['component']) is not str or not p['component']:raise ValueError('component')
    if type(p['establishes']) is not list or not 1<=len(p['establishes'])<=32:raise ValueError('claims')
    if type(p['does_not_establish']) is not list or len(p['does_not_establish'])>32:raise ValueError('boundaries')
    for c in p['establishes']:validate_kind(c,'evidenceClaim')
    for c in p['does_not_establish']:validate_kind(c,'negativeClaimBoundary')
    validate_kind(v['requirement'],'evidenceClaim')

def validate_outputs(r):
    o=r['outputs']
    if set(o)!={'edge_compatible','explicit_boundary_hit','claim_truth','execution_occurrence'}:raise ValueError('outputs')
    if any(type(o[k]) is not bool for k in ('edge_compatible','explicit_boundary_hit')):raise ValueError('boolean')
    if any(o[k] not in ('SUPPORTED','UNSUPPORTED') for k in ('claim_truth','execution_occurrence')):raise ValueError('authority status')

def make_profile(root):
    def evaluate(v,c):
        from adapters.semantic_abi.model import evaluate
        return evaluate(root,{'inputs':v})
    return RelationProfile(PROFILE_ID,VERSION,(Relation(RELATION_ID,('producer','requirement'),(),lambda v:validate_inputs(root,v),evaluate,validate_outputs),),SOURCE_PIN_SHA256)
