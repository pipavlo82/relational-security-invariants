"""Mapped Aggregate mutations; real EVM setup failures are VACUOUS, never kills."""
import argparse,sys,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from rsi.codec import encode,load
from runner.mutation_registry import Mutation,MutationTrace,CheckEvent,MutationRegistry
from tools.prove_expectations_can_fail import copy_repo,track_phases,ExecutionResult
DEFINITIONS=(('AGG-M1', 'tamper=False  # AGG-M1', 'tamper=True', 'test_edge_amplification'), ('AGG-M2', "variant=v['engine']  # AGG-SOURCE-MUTATION", "variant='root' if v['engine']=='cursor' else 'edge'", 'test_shared_root'), ('AGG-M3', "variant=v['engine']  # AGG-SOURCE-MUTATION", "variant='refund' if v['engine']=='cursor' else 'edge'", 'test_revoke_no_refund'), ('AGG-M4', "variant=v['engine']  # AGG-SOURCE-MUTATION", "variant='period' if v['engine']=='cursor' else 'edge'", 'test_period_history'), ('AGG-M5', "variant=v['engine']  # AGG-SOURCE-MUTATION", "variant='delegate' if v['engine']=='cursor' else 'edge'", 'test_capped_leaf'), ('AGG-M6', "variant=v['engine']  # AGG-SOURCE-MUTATION", "variant='revoked' if v['engine']=='cursor' else 'edge'", 'test_ancestor_revoked'), ('AGG-M7', "variant=v['engine']  # AGG-SOURCE-MUTATION", "variant='nodecap' if v['engine']=='cursor' else 'edge'", 'test_node_cap'), ('AGG-M8', "out['non_bypassability']='UNSUPPORTED'  # AGG-M8", "out['non_bypassability']='ESTABLISHED'", 'test_unsupported_claims'), ('AGG-M9', "out['conserved']=out['conserved']  # AGG-M9", "out['conserved']=out['conserved'] and v['observation_time']=='101'", 'test_mirror'))

def child(output,test=None):
    name='tests.test_aggregate.AggregateTests'+('.'+test if test else '')
    suite=unittest.defaultTestLoader.loadTestsFromName(name);track_phases(suite);r=ExecutionResult();suite.run(r)
    output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(encode({'rows':r.rows,'tests_run':r.testsRun}))
    return 0 if r.wasSuccessful() else 1
def exercise(d):
    with tempfile.TemporaryDirectory(prefix='aggregate-mutant-') as tmp:
        root=Path(tmp)/'repo';copy_repo(root);ident,old,new,mapped=d;p=root/'adapters/aggregate/model.py';s=p.read_text()
        if s.count(old)!=1:return MutationTrace(False)
        p.write_text(s.replace(old,new,1),newline='\n');out=root/'artifacts/aggregate-child.json'
        r=subprocess.run([sys.executable,'-B','tools/prove_aggregate_can_fail.py','--child',str(out),'--test',mapped],cwd=root,capture_output=True,timeout=180)
        if r.returncode not in (0,1) or not out.exists():return MutationTrace(True,errors=('CHILD_SETUP',))
        return MutationTrace(True,tuple(CheckEvent(x['id'],x['status'],x.get('phase','test')) for x in load(out)['rows']))
def registry():return MutationRegistry(Mutation(d[0],'erc8312.aggregate-budget.v0','tests.test_aggregate.AggregateTests.'+d[3],lambda context,d=d:exercise(d),'test') for d in DEFINITIONS)
def main():
    p=argparse.ArgumentParser();p.add_argument('--child',type=Path);p.add_argument('--test');p.add_argument('--output',type=Path,default=ROOT/'artifacts/aggregate-mutations.json');a=p.parse_args()
    if a.child:return child(a.child,a.test)
    if child(ROOT/'artifacts/aggregate-mutation-baseline.json'):raise SystemExit('Aggregate baseline failed')
    r=registry().execute({'erc8312.aggregate-budget.v0'});a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(encode(r));print(r['totals']);return int(r['totals']['KILLED']!=9)
if __name__=='__main__':raise SystemExit(main())
