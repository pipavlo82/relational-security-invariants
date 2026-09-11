"""ASCII records and opaque signed content; no universal fields added."""
import json,re
from rsi.codec import domain
from runner.relation_profile import Relation,RelationProfile
from profiles.judgment.source import verify_source,SOURCE_PIN_SHA256
PROFILE_ID='erc8299.judgment-record-binding.v0';VERSION='0';RELATION_ID='signed-verdict-terminal-record-binding'
def validate_inputs(v):
    domain(v)
    if set(v)!={'record'} or not isinstance(v['record'],dict):raise ValueError('record')
    f=v['record']
    if set(f)!={'canonical_envelope','chain','admission','anchor','trust_policy'}:raise ValueError('record slots')
    ce=f['canonical_envelope'];pre=f['chain']['pre_action'];term=f['chain']['terminal'];ev=f['admission']['verdict_event']
    def hx(s,n):
        if type(s) is not str or re.fullmatch('[0-9a-f]{'+str(n)+'}',s) is None:raise ValueError('hex')
    for s in (ce['expected_envelope_hash'],pre['envelope_hash'],term['executed_envelope_hash'],pre['actor_pubkey'],ev['pubkey'],ev['id']):hx(s,64)
    hx(ev['sig'],128)
    for s in f['trust_policy']['independent_verifier_pubkeys']:hx(s,64)
    if type(ce['canonical_bytes_utf8']) is not str or type(ev['content']) is not str:raise ValueError('exact text')
    # Signed content remains exact opaque ASCII text: embedded decimal confidence is never coerced.
    if type(json.loads(ev['content'])) is not dict:raise ValueError('signed object')
    for x in (ev['created_at'],ev['kind'],term['terminal_outcome_time']):
        if type(x) is not int or not 0<=x<2**53:raise ValueError('safe integer')
    anc=f['anchor']
    if anc is not None:
        hx(anc['commitment_digest'],64)
        for x in (anc['accepted_anchor_point']['block_time'],anc['terminal_outcome_time']):
            if type(x) is not int or not 0<=x<2**53:raise ValueError('anchor time')
def validate_outputs(r):
    o=r['outputs'];domain(o)
    if type(o['binding_established']) is not bool or type(o['source_checks']) is not dict:raise ValueError('output')
def make_profile(root):
    def validate(v):verify_source(root);validate_inputs(v)
    def actual(v,c):
        from adapters.judgment.model import evaluate
        return evaluate(root,{'inputs':v})
    return RelationProfile(PROFILE_ID,VERSION,(Relation(RELATION_ID,('record',),(),validate,actual,validate_outputs),),SOURCE_PIN_SHA256)
