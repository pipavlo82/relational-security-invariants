"""Deterministic source/compatibility gate; no domain semantics in core."""
from pathlib import Path
import argparse,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from rsi.codec import load,encode,raw_digest
from profiles.tas.source import verify_source
from runner.relation_runtime import execute
from extensions.tas import composition,complete_composition
from extensions.pq import complete_composition as previous

def check(root=ROOT):
    baseline=load(root/'evidence/tas/protected-baseline.v0.json')
    mismatches=[p for p,h in baseline['hashes'].items() if raw_digest((root/p).read_bytes())!=h]
    if mismatches:raise ValueError('PROTECTED_DRIFT '+str(mismatches))
    prior=execute(root,*previous(root))
    if raw_digest(encode(prior))!=baseline['previous_report_sha256']:raise ValueError('PRIOR_OUTCOME_DIFF')
    current=execute(root,*composition(root));combined=execute(root,*complete_composition(root))
    if current['totals']!={'PASS':8,'FAIL':0,'INVALID_FIXTURE':0,'UNSUPPORTED':0}:raise ValueError('TAS_RESULTS')
    if combined['totals']!={'PASS':72,'FAIL':0,'INVALID_FIXTURE':0,'UNSUPPORTED':0}:raise ValueError('COMBINED_RESULTS')
    return {'schema':'rsi-domain-validation.v0','domain':'tas','scope':'verified-context-to-invocation','source':verify_source(root),'relations':['verified-workflow-dispatch'],'fixtures':current['totals'],'combined':combined['totals'],'authorization_execution_boundary':{'context_verified':'supplied accepted source context; authenticity not recomputed','invocation_binding_validated':True,'execution_occurrence_validation':'UNSUPPORTED'},'protected_hashes':len(baseline['hashes']),'protected_hashes_match':True,'prior_outcome_diff':0,'generic_core_changed':False,'semantic_exceptions_added':0,'limitations':['Controlled membership/resolver/SDK ports; no chain, wallet ownership proof or action execution.','Only read getTask dispatch and digit-only source-test EVM addresses. No call-intent commitment, method/argument authorization or nonce guarantee.','TypeScript source compiled with pinned esbuild/viem; separately implemented Python obligations; author independence not established.','ASCII/safe-integer carrier, large agent identity remains source-defined decimal string.']}
def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'artifacts/tas-validation.json');a=p.parse_args();r=check();a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(encode(r));print(r['fixtures'],r['protected_hashes'])
if __name__=='__main__':main()
