"""Generation-specific proof relation; no universal Guard acceptance."""
import re
from runner.relation_profile import Relation,RelationProfile
from rsi.codec import domain
from profiles.capv.source import verify_source,SOURCE_PIN_SHA256,SDK,OLD,FIXED
PROFILE_ID='capv.expiry-generation.v0';VERSION='0';RELATION_ID='proof-public-input-generation-binding'
REQUIRED=('program_generation','proof_generation','program_key','verdict','observation_time','consumer_pin')
FIELDS=('agentId','domainId','policyRoot','actionCommitment','executor','expiry','nullifier','decision','policyKind')
def validate_inputs(v):
    domain(v)
    if type(v) is not dict or set(v)!=set(REQUIRED):raise ValueError('slots')
    for k in ('program_generation','proof_generation'):
        if v[k] not in ('sdk','fixed'):raise ValueError('generation')
    if v['consumer_pin'] not in ('direct',SDK):raise ValueError('consumer pin')
    def hx(s,width):
        if type(s) is not str or re.fullmatch('0x[0-9a-f]{'+str(width)+'}',s) is None:raise ValueError('hex width')
    def number(s,bits):
        if type(s) is not str or re.fullmatch('0|[1-9][0-9]*',s) is None or int(s)>=2**bits:raise ValueError('decimal string')
    hx(v['program_key'],64);number(v['observation_time'],64)
    d=v['verdict']
    if type(d) is not dict or set(d)!=set(FIELDS):raise ValueError('Verdict fields')
    for k in ('domainId','policyRoot','actionCommitment','nullifier'):hx(d[k],64)
    hx(d['executor'],40)
    number(d['agentId'],256);number(d['expiry'],64);number(d['decision'],8);number(d['policyKind'],8)
def validate_outputs(r):
    o=r['outputs'];domain(o)
    required={'program_generation','vk_hash','public_input_count','expiry_public','proof_verifies','adapter_verifies','program_key_matches_vk','proof_program_matches','consumer_generation_matches','expiry_fresh','expiry_bound_to_this_proof','normative_expiry_public','canonical_asset_expiry_public','canonical_asset_alignment','guard_acceptance','domain_root_acceptability','executor_authorization','execution_occurrence'}
    required.update(('verifier_result','adapter_result'))
    if set(o)!=required:raise ValueError('output slots')
    for k in ('verifier_result','adapter_result'):
        if o[k] not in ('TRUE','FALSE','REVERT'):raise ValueError('source result kind')
    for k in ('expiry_public','proof_verifies','adapter_verifies','program_key_matches_vk','proof_program_matches','consumer_generation_matches','expiry_fresh','expiry_bound_to_this_proof','normative_expiry_public','canonical_asset_expiry_public'):
        if type(o[k]) is not bool:raise ValueError('boolean output')
def make_profile(root):
    def validate(v):verify_source(root);validate_inputs(v)
    def evaluate(v,c):
        from adapters.capv.model import evaluate as actual
        return actual(root,{'inputs':v})
    return RelationProfile(PROFILE_ID,VERSION,(Relation(RELATION_ID,REQUIRED,(),validate,evaluate,validate_outputs),),SOURCE_PIN_SHA256)
