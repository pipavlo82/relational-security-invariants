"""Mapped CAPV mutations; real EVM setup failures are VACUOUS, never kills."""
import argparse,sys,subprocess,tempfile,unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from rsi.codec import encode,load
from runner.mutation_registry import Mutation,MutationTrace,CheckEvent,MutationRegistry
from tools.prove_expectations_can_fail import copy_repo,track_phases,ExecutionResult
DEFINITIONS=(
 ('CAPV-M1','bound=expiry_public and crypt  # CAPV-M1','bound=fresh and crypt','test_fresh_not_bound'),
 ('CAPV-M2','variant=generation  # CAPV-M2',"variant='fixed-drop' if generation=='fixed' else generation",'test_fixed_control'),
 ('CAPV-M3',"generation=v['program_generation']  # CAPV-M3","generation=v['proof_generation']",'test_generation'),
 ('CAPV-M4',"consumer_generation='sdk'  # CAPV-M4","consumer_generation='fixed'\n        generation='fixed'",'test_nonretroactivity'),
 ('CAPV-M5',"key=v['program_key']  # CAPV-M5","key=v['program_key']\n    if generation=='sdk':variant='sdk-key'",'test_program_key'),
 ('CAPV-M6','crypt=crypt  # CAPV-M6',"crypt=crypt and v['observation_time']=='1700000000'",'test_mirror'),
)
def child(output,test=None):
    name='tests.test_capv.CAPVTests'+('.'+test if test else '')
    suite=unittest.defaultTestLoader.loadTestsFromName(name);track_phases(suite);r=ExecutionResult();suite.run(r)
    output.parent.mkdir(parents=True,exist_ok=True);output.write_bytes(encode({'rows':r.rows,'tests_run':r.testsRun}))
    return 0 if r.wasSuccessful() else 1
def exercise(d):
    with tempfile.TemporaryDirectory(prefix='capv-mutant-') as tmp:
        root=Path(tmp)/'repo';copy_repo(root);ident,old,new,mapped=d;p=root/'adapters/capv/model.py';s=p.read_text()
        if s.count(old)!=1:return MutationTrace(False)
        p.write_text(s.replace(old,new,1),newline='\n');out=root/'artifacts/capv-child.json'
        r=subprocess.run([sys.executable,'-B','tools/prove_capv_can_fail.py','--child',str(out),'--test',mapped],cwd=root,capture_output=True,timeout=180)
        if r.returncode not in (0,1) or not out.exists():return MutationTrace(True,errors=('CHILD_SETUP',))
        return MutationTrace(True,tuple(CheckEvent(x['id'],x['status'],x.get('phase','test')) for x in load(out)['rows']))
def registry():return MutationRegistry(Mutation(d[0],'capv.expiry-generation.v0','tests.test_capv.CAPVTests.'+d[3],lambda context,d=d:exercise(d),'test') for d in DEFINITIONS)
def main():
    p=argparse.ArgumentParser();p.add_argument('--child',type=Path);p.add_argument('--test');p.add_argument('--output',type=Path,default=ROOT/'artifacts/capv-mutations.json');a=p.parse_args()
    if a.child:return child(a.child,a.test)
    if child(ROOT/'artifacts/capv-mutation-baseline.json'):raise SystemExit('CAPV baseline failed')
    r=registry().execute({'capv.expiry-generation.v0'});a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_bytes(encode(r));print(r['totals']);return int(r['totals']['KILLED']!=6)
if __name__=='__main__':raise SystemExit(main())
