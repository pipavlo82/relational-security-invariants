"""Deterministic ConsultEscrow source, outcomes, and preservation report."""
from pathlib import Path
import argparse,sys,ast
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from tools.protected_maintenance import mismatches, approved_changes
from rsi.codec import load,encode,raw_digest
from profiles.consult_escrow.source import verify_source
from runner.relation_runtime import execute
from extensions.consult_escrow import composition,complete_composition
from extensions.tas import complete_composition as previous

def check(root=ROOT):
    baseline=load(root/'evidence/consult-escrow/protected-baseline.v0.json')
    drift=mismatches(root,baseline['hashes'])
    maintenance=approved_changes(root,baseline['hashes'])
    if drift:raise ValueError('PROTECTED_DRIFT '+str(drift))
    prior=execute(root,*previous(root))
    if raw_digest(encode(prior))!=baseline['previous_report_sha256']:raise ValueError('PRIOR_OUTCOME_DIFF')
    current=execute(root,*composition(root));combined=execute(root,*complete_composition(root))
    if current['totals']!={'PASS':7,'FAIL':0,'INVALID_FIXTURE':0,'UNSUPPORTED':0}:raise ValueError('CE_RESULTS')
    if combined['totals']!={'PASS':79,'FAIL':0,'INVALID_FIXTURE':0,'UNSUPPORTED':0}:raise ValueError('COMBINED_RESULTS')
    branches=[]
    for p in [*(root/'runner').glob('*.py'),root/'rsi/run.py',root/'rsi/oracle.py']:
        for n in ast.walk(ast.parse(p.read_text())):
            if isinstance(n,(ast.If,ast.IfExp)) and any(t in ast.unparse(n.test).lower() for t in ('consult','escrow','job-bound-release')):branches.append(p.as_posix())
    if branches:raise ValueError('CORE_COUPLING')
    return {'schema':'rsi-domain-validation.v0','domain':'consult-escrow','scope':'job-bound-authorization-to-release','rsi_head_before':baseline['head'],'source':verify_source(root),'inspected_consumer_sources':load(root/'research/consult-escrow-source-map-v0.json')['files'][-2:],'relations':['job-bound-release'],'signature_scope':{'bound_fields':['jobId','resultHash'],'state_bound_fields':['provider','amount','attestor','consumer','deadline','status'],'unbound_fields':['chainId','contract address','caller','signed amount','signed recipient','release nonce','signature expiry','milestone','policy','action selector']},'fixtures':current['totals'],'combined':combined['totals'],'settlement_execution':{'status':'SUPPORTED','scope':'isolated EVM retained state, provider balance delta and Released log only','mainnet_occurrence':'UNSUPPORTED','simulation_without_retained_state':'UNSUPPORTED'},'legacy_compatibility':{'outcome_diff':0},'prior_domain_compatibility':{'outcome_diff':0},'protected_hashes':len(baseline['hashes']),'protected_hashes_match':not maintenance,'approved_post_v0_maintenance':maintenance,'anti_coupling':'PASS','generic_core_changed':False,'semantic_exceptions_added':0,'limitations':['No signed deployment/chain domain; same-job cross-instance replay resistance is not established. No exploitability conclusion.','Amount and provider are immutable job-state values, not signed release parameters. No fabricated amount/recipient rejection fixtures.','Deadline enables refund; it is not signature expiry or a release cutoff. Only Released replay is covered here.','Local EVM calls, not transaction inclusion/finality or mainnet receipt verification. EOAs only; hostile recipient, reentrancy and payment-failure paths not covered.','Independent Python integer Keccak/secp256k1 and state obligations versus Solidity bytecode on JavaScript EVM. Author independence and production-grade crypto assurance not established.','ASCII carrier with validated hex and uint256 decimal strings; EVM BigInt conversion is exact. No floating point or raw binary JSON coercion.','SDK comment incorrectly says resultText is emitted; contract/interface emit resultHash. Text availability and pre-outcome ordering are not established.']}
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'artifacts/consult-escrow-validation.json');p.add_argument('--mutations',type=Path);a=p.parse_args();r=check()
    if a.mutations:
        m=load(a.mutations)
        if m['totals']!={'KILLED':5,'SURVIVED':0,'VACUOUS':0,'NOT_APPLIED':0}:raise ValueError('MUTATION_GATE')
        r['mutations']=m
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(encode(r));print(r['fixtures'],r['protected_hashes'])
if __name__=='__main__':main()
