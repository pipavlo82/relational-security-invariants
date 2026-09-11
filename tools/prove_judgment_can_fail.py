"""Mapped Judgment mutations; real EVM setup failures are VACUOUS, never kills."""
import argparse,sys,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from rsi.codec import encode,load
from runner.mutation_registry import Mutation,MutationTrace,CheckEvent,MutationRegistry
from tools.prove_expectations_can_fail import copy_repo,track_phases,ExecutionResult
DEFINITIONS=(('JEX-M1', "out['binding_established']=all(c[k]['pass'] is True for k in ('canonical_envelope','chain_invariant','admission_invariant'))  # J-M1", "out['binding_established']=out['signature_valid']", 'test_terminal_substitution'), ('JEX-M2', "out['chain_bound']=c['chain_invariant']['pass']  # J-M2", "out['chain_bound']=True", 'test_action_ref'), ('JEX-M3', "out['admission_bound']=c['admission_invariant']['pass']  # J-M3", "out['admission_bound']=out['signature_valid']", 'test_other_signed_envelope'), ('JEX-M4', "out['ordering_established_under_declared_anchor']=c['anchoring_precedence']['pass']  # J-M4", "out['ordering_established_under_declared_anchor']=c['anchoring_existence']['pass']", 'test_late_anchor'), ('JEX-M5', "out['execution_occurrence']='UNSUPPORTED'  # J-M5", "out['execution_occurrence']='ESTABLISHED'", 'test_execution_unsupported'), ('JEX-M6', "out['action_authorization']='UNSUPPORTED'  # J-M6", "out['action_authorization']='ESTABLISHED'", 'test_authorization_not_inherited'), ('JEX-M7', "out['anchor_authority']='UNSUPPORTED'  # J-M7", "out['anchor_authority']='ESTABLISHED'", 'test_anchor_not_authority'), ('JEX-M8', "out['binding_established']=out['binding_established']  # J-M8", "out['binding_established']=out['binding_established'] and not v['anchor']['accepted_anchor_point'].get('note','').startswith('Display-only') if v['anchor'] else out['binding_established']", 'test_mirror'))

def child(output,test=None):
    name='tests.test_judgment.JudgmentTests'+('.'+test if test else '')
    suite=unittest.defaultTestLoader.loadTestsFromName(name);track_phases(suite);r=ExecutionResult();suite.run(r)
    output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(encode({'rows':r.rows,'tests_run':r.testsRun}))
    return 0 if r.wasSuccessful() else 1
def exercise(d):
    with tempfile.TemporaryDirectory(prefix='judgment-mutant-') as tmp:
        root=Path(tmp)/'repo';copy_repo(root);ident,old,new,mapped=d;p=root/'adapters/judgment/model.py';s=p.read_text()
        if s.count(old)!=1:return MutationTrace(False)
        p.write_text(s.replace(old,new,1),newline='\n');out=root/'artifacts/judgment-child.json'
        r=subprocess.run([sys.executable,'-B','tools/prove_judgment_can_fail.py','--child',str(out),'--test',mapped],cwd=root,capture_output=True,timeout=180)
        if r.returncode not in (0,1) or not out.exists():return MutationTrace(True,errors=('CHILD_SETUP',))
        return MutationTrace(True,tuple(CheckEvent(x['id'],x['status'],x.get('phase','test')) for x in load(out)['rows']))
def registry():return MutationRegistry(Mutation(d[0],'erc8299.judgment-record-binding.v0','tests.test_judgment.JudgmentTests.'+d[3],lambda context,d=d:exercise(d),'test') for d in DEFINITIONS)
def main():
    p=argparse.ArgumentParser();p.add_argument('--child',type=Path);p.add_argument('--test');p.add_argument('--output',type=Path,default=ROOT/'artifacts/judgment-mutations.json');a=p.parse_args()
    if a.child:return child(a.child,a.test)
    if child(ROOT/'artifacts/judgment-mutation-baseline.json'):raise SystemExit('Judgment baseline failed')
    r=registry().execute({'erc8299.judgment-record-binding.v0'});a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(encode(r));print(r['totals']);return int(r['totals']['KILLED']!=8)
if __name__=='__main__':raise SystemExit(main())
