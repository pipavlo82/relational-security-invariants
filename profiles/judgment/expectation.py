"""Separately implemented expectation predictor over declared joins and BIP340.
Source-derived, same language and equations; no claim of a clean-room third leg.
"""
from pathlib import Path
import hashlib,json
from rsi.codec import load
from runner.expectation_registry import ExpectationProfile,FixtureSource
from runner.relation_runtime import validate_envelope,plan
from profiles.judgment.source import verify_source
from profiles.judgment.signature import valid
EXPECTATION_ID='erc8299.judgment-record-binding.v0'
def derive(v):
    f=v['record'];ce=f['canonical_envelope'];pre=f['chain']['pre_action'];term=f['chain']['terminal'];ev=f['admission']['verdict_event'];anchor=f.get('anchor')
    digest=hashlib.sha256(ce['canonical_bytes_utf8'].encode()).hexdigest();sig=valid(ev)
    content=json.loads(ev['content']);env=ce['expected_envelope_hash']==digest
    chain=all((pre['envelope_hash']==digest,term['executed_envelope_hash']==digest,pre['action_ref']==term['action_ref']))
    admission='admission_signature_invalid' if not sig else 'verdict_binding_failed' if content.get('artifact_hash')!=digest else 'admission_not_independent' if ev['pubkey']==pre['actor_pubkey'] else 'key_different_but_identity_unproven' if ev['pubkey'] not in f['trust_policy']['independent_verifier_pubkeys'] else None
    exists=anchor is not None and anchor['commitment_digest']==ev['id']
    existence_code=None if exists else 'ordering_unanchored' if anchor is None else 'anchor_commitment_mismatch'
    ordering=None if not exists else False if anchor.get('precedence') is False else anchor['accepted_anchor_point']['block_time']<anchor['terminal_outcome_time']
    ordering_code='not_assessable' if not exists else 'existence_only_anchor' if anchor.get('precedence') is False else None if ordering else 'late_commitment'
    checks=dict(canonical_envelope=dict(pass_=env,code=None if env else 'envelope_hash_mismatch'),chain_invariant=dict(pass_=chain,code=None if chain else 'chain_join_failed'),admission_invariant=dict(pass_=admission is None,code=admission),anchoring_existence=dict(pass_=exists,code=existence_code),anchoring_precedence=dict(pass_=ordering,code=ordering_code))
    checks={k:{'pass':s['pass_'],'code':s['code']} for k,s in checks.items()}
    out=dict(source_checks=checks,source_overall=all(s['pass'] is True for s in checks.values()),source_failure=next((s['code'] for s in checks.values() if s['pass'] is False),None),envelope_hash=digest,signature_valid=sig,binding_established=env and chain and admission is None,verdict_decision=content.get('verdict'),chain_bound=chain,admission_bound=admission is None,ordering_established_under_declared_anchor=ordering)
    for k in ('execution_occurrence','action_authorization','anchor_authority','judgment_soundness','raw_to_canonical_derivation'):out[k]='UNSUPPORTED'
    return dict(relation_id='signed-verdict-terminal-record-binding',relation_state='records_observed',outputs=out)
def predict(f):return {f['id']+'/'+c['case_id']:{'local_validity':True,'observation':derive(c['inputs'])} for c in f['cases']}
def validate_prediction(v):
    if type(v) is not dict or not v:raise ValueError('prediction')
    for row in v.values():
        if set(row)!={'local_validity','observation'} or row['local_validity'] is not True:raise ValueError('prediction row')
def make_profile(root):
    m=load(Path(root)/'profiles/judgment/expectation-profile.v0.json')
    if m['profile_id']!=EXPECTATION_ID or m['version']!='0':raise ValueError('profile pin')
    return ExpectationProfile(EXPECTATION_ID,'0',tuple(FixtureSource(**r) for r in m['fixture_scope']),predict,m['expectations_path'],m['expectations_digest'],validate_envelope,validate_prediction,lambda f:plan(f,'binding'),lambda r:verify_source(r))
