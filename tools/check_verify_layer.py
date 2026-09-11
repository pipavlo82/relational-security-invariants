"""Deterministic verify-layer source, outcomes, and preservation report."""
from pathlib import Path
import argparse,sys,ast
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from tools.protected_maintenance import mismatches, approved_changes
from rsi.codec import load,encode,raw_digest
from profiles.verify_layer.source import verify_source
from runner.relation_runtime import execute
from extensions.verify_layer import composition,complete_composition
from extensions.consult_escrow import complete_composition as previous

def check(root=ROOT):
    baseline=load(root/'evidence/verify-layer/protected-baseline.v0.json')
    drift=mismatches(root,baseline['hashes'])
    maintenance=approved_changes(root,baseline['hashes'])
    if drift:raise ValueError('PROTECTED_DRIFT '+str(drift))
    prior=execute(root,*previous(root))
    if raw_digest(encode(prior))!=baseline['previous_report_sha256']:raise ValueError('PRIOR_OUTCOME_DIFF')
    current=execute(root,*composition(root));combined=execute(root,*complete_composition(root))
    if current['totals']!={'PASS':6,'FAIL':0,'INVALID_FIXTURE':0,'UNSUPPORTED':0}:raise ValueError('VL_RESULTS')
    if combined['totals']!={'PASS':85,'FAIL':0,'INVALID_FIXTURE':0,'UNSUPPORTED':0}:raise ValueError('COMBINED_RESULTS')
    branches=[]
    for p in [*(root/'runner').glob('*.py'),root/'rsi/run.py',root/'rsi/oracle.py']:
        for n in ast.walk(ast.parse(p.read_text())):
            if isinstance(n,(ast.If,ast.IfExp)) and any(t in ast.unparse(n.test).lower() for t in ('verify-layer','verify_layer','account-proof-root-balance')):branches.append(p.as_posix())
    if branches:raise ValueError('CORE_COUPLING')
    return {'schema':'rsi-domain-validation.v0','domain':'verify-layer','scope':'proof-root-context-trust','rsi_head_before':baseline['head'],'source':verify_source(root),'source_map':load(root/'research/verify-layer-source-map-v0.json'),'relations':['account-proof-root-balance'],'trust_assumptions':['RPC-TRUSTED header; no wired light client','finalized is a supplied query tag, not independently verified finality','account address is trie path, not deployment execution identity'],'fixtures':current['totals'],'combined':combined['totals'],'header_authority':{'status':'UNSUPPORTED'},'downstream_claim_validation':{'status':'PARTIAL','supported':'RPC claimed balance agrees with MPT account balance under supplied root','unsupported':'independent chain authority and downstream semantic/action claims'},'legacy_compatibility':{'outcome_diff':0},'prior_domain_compatibility':{'outcome_diff':0},'protected_hashes':len(baseline['hashes']),'protected_hashes_match':not maintenance,'approved_post_v0_maintenance':maintenance,'anti_coupling':'PASS','generic_core_changed':False,'semantic_exceptions_added':0,'limitations':['Account lane only; storage, consensus, finality, chain and full deployment semantics excluded.','Header/root supplied by RPC. No production downstream wallet consumer tested.','Language-separated Python MPT/RLP/Keccak oracle versus pinned JavaScript source; author independence and exhaustive proof assurance not established.','ASCII hex quantities/bytes, exact wei decimal strings; source ETH float display explicitly excluded.','Six source-backed cases; block/chain/as-of rejection mutations are inapplicable because source does not independently bind those fields.']}

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'artifacts/verify-layer-validation.json');p.add_argument('--mutations',type=Path);a=p.parse_args();r=check()
    if a.mutations:
        m=load(a.mutations)
        if m['totals']!={'KILLED':6,'SURVIVED':0,'VACUOUS':0,'NOT_APPLIED':0}:raise ValueError('MUTATION_GATE')
        r['mutations']=m
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(encode(r));print(r['fixtures'],r['protected_hashes'])
if __name__=='__main__':main()
