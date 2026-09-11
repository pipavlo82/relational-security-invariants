"""Finite source-backed aggregate traces; native setup errors never count as kills."""
from dataclasses import replace
from pathlib import Path
import inspect,json,shutil,subprocess,tempfile,unittest
from unittest.mock import patch
from rsi.codec import load,encode,raw_digest
from runner.relation_runtime import execute,resolve_fixture
from runner.expectation_contract import admit,load_fixtures,ProfileError
from runner.relation_profile_registry import UnavailableRelation
from profiles.aggregate import relation,expectation,source
from adapters.aggregate import model
from extensions.aggregate import composition,complete_composition
ROOT=Path(__file__).resolve().parents[1]

class AggregateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=execute(ROOT,*composition(ROOT))
        if not cls.report['admissions'] or any(r.get('diagnostic_kind') or r.get('result',{}).get('errors') for r in cls.report['rows']):raise RuntimeError('mapped native decision not reached')
    def observed(self,n):
        r=next(r['result'] for r in self.report['rows'] if r['result']['key'].startswith(f'AGG-RSI-{n:03}/'))
        return r,r['observed']['outputs']
    def fixture(self,n):return load(ROOT/f'corpora/aggregate/fixtures/AGG-RSI-{n:03}.json')
    def clone(self):
        tmp=tempfile.TemporaryDirectory(prefix='aggregate-test-');self.addCleanup(tmp.cleanup);r=Path(tmp.name)
        for d in ('profiles/aggregate','adapters/aggregate','evidence/aggregate','corpora/aggregate'):shutil.copytree(ROOT/d,r/d,ignore=shutil.ignore_patterns('__pycache__'))
        (r/'extensions').mkdir();shutil.copy2(ROOT/'extensions/aggregate.corpus.v0.json',r/'extensions/aggregate.corpus.v0.json');return r
    def test_pipeline(self):self.assertEqual(self.report['totals'],dict(PASS=12,FAIL=0,INVALID_FIXTURE=0,UNSUPPORTED=0))
    def test_control(self):
        r,o=self.observed(1);self.assertEqual(o['realized'],'1000');self.assertTrue(o['conserved']);self.assertTrue(all(s['status']=='RETURN' for s in o['steps']));self.assertEqual(r['status'],'PASS')
    def test_edge_amplification(self):
        r,o=self.observed(2);self.assertTrue(all(s['local_draw_valid'] for s in o['steps'] if s['op']=='draw'));self.assertEqual(o['realized'],'2000');self.assertFalse(o['conserved']);self.assertEqual(o['log_origin'],'SUCCESSFUL_SOURCE_CALLS');self.assertEqual(r['status'],'PASS')
    def test_shared_root(self):
        r,o=self.observed(3);self.assertTrue(o['steps'][-1]['local_draw_valid']);self.assertEqual(o['steps'][-1]['error'],'RootBoundExceeded');self.assertEqual(o['realized'],'1000');self.assertEqual(r['status'],'PASS')
    def test_fanout_atomic(self):
        r,o=self.observed(4);self.assertEqual(o['steps'][-2]['error'],'RootBoundExceeded');self.assertEqual(o['steps'][-1]['status'],'RETURN');self.assertEqual(o['realized'],'2000');self.assertTrue(o['meters'][0]['meter_matches']);self.assertEqual(r['status'],'PASS')
    def test_diamond(self):
        r,o=self.observed(5);self.assertEqual(o['steps'][-1]['error'],'RootBoundExceeded');self.assertEqual(o['realized'],'1000');self.assertEqual(r['status'],'PASS')
    def test_revoke_no_refund(self):
        r,o=self.observed(6);self.assertEqual([s['error'] for s in o['steps'] if s['status']=='REVERT'],['PathRevoked','RootBoundExceeded']);self.assertEqual(o['realized'],'1000');self.assertTrue(o['meters'][0]['meter_matches']);self.assertEqual(r['status'],'PASS')
    def test_period_history(self):
        r,o=self.observed(7);self.assertEqual([m['spent_root'] for m in o['meters']],['1000','1000']);self.assertTrue(all(m['meter_matches'] for m in o['meters']));self.assertEqual(r['status'],'PASS')
    def test_mirror(self):
        r,o=self.observed(8);self.assertEqual(o,self.observed(1)[1]);self.assertEqual(r['status'],'PASS')
    def test_node_cap(self):
        r,o=self.observed(9);self.assertEqual(o['steps'][-1]['error'],'NodeBoundExceeded');self.assertEqual(o['realized'],'200');self.assertEqual(r['status'],'PASS')
    def test_capped_leaf(self):
        r,o=self.observed(10);self.assertEqual(o['steps'][1]['error'],'CappedNodeCannotDelegate');self.assertEqual(o['steps'][-1]['status'],'RETURN');self.assertEqual(r['status'],'PASS')
    def test_root_isolation(self):
        r,o=self.observed(11);self.assertEqual([m['spent_root'] for m in o['meters']],['1000','2000']);self.assertEqual(o['steps'][-1]['error'],'RootBoundExceeded');self.assertEqual(r['status'],'PASS')
    def test_ancestor_revoked(self):
        r,o=self.observed(12);self.assertEqual([s['error'] for s in o['steps'] if s['status']=='REVERT'],['PathRevoked','PathRevoked']);self.assertEqual(o['realized'],'1000');self.assertEqual(r['status'],'PASS')
    def test_unsupported_claims(self):
        for row in self.report['rows']:
            o=row['result']['observed']['outputs']
            for k in ('non_bypassability','asset_movement','cross_chain_conservation','subtree_budgets','authoritative_chain_state'):self.assertEqual(o[k],'UNSUPPORTED')
    def test_mirror_changes_time_only(self):
        a=self.fixture(1)['cases'][0]['inputs'];b=self.fixture(8)['cases'][0]['inputs'];self.assertNotEqual(a,b);a['observation_time']=b['observation_time']
        for x,y in zip(a['steps'],b['steps']):x['time']=y['time']
        self.assertEqual(a,b)
    def test_source_pins(self):
        p=source.verify_source(ROOT);self.assertEqual(len(p['files']),39)
        self.assertIn('728310aa69f5b22152b32f1ef31394b85f3eb8bb',json.dumps(p));self.assertIn('d94cacf89287a295823ce43e560a575c0cc25e21',json.dumps(p))
        self.assertEqual(raw_digest((ROOT/'evidence/aggregate/recompute-kit/aggregate-budget-v0.vectors.json').read_bytes()),'ac6f6efd485e887a7f82140ac5be234643af17efb24506d9cd40e87ecd2bcb85')
    def test_stale_source(self):
        r=self.clone();p=r/'evidence/aggregate/reference/src/AggregateBudgetCursor.sol';p.write_bytes(p.read_bytes()+b'\n');self.assertEqual(execute(r,*composition(r))['totals']['UNSUPPORTED'],12)
    def test_wrong_source_manifest(self):
        r=self.clone();p=r/'evidence/aggregate/source-pin.v0.json';p.write_bytes(p.read_bytes()+b' ')
        with self.assertRaises(source.SourceUnavailable):source.verify_source(r)
    def test_compiled_digest(self):
        r=self.clone();p=r/'evidence/aggregate/cursor.json';p.write_bytes(p.read_bytes()+b' ')
        with self.assertRaises(source.SourceUnavailable):source.verify_source(r)
    def test_tamper_atomic(self):
        r=self.clone();p=expectation.make_profile(r);f=load_fixtures(r,p);path=r/p.expectations_path;v=load(path);pred=v['expectations'][1]['prediction'];pred[next(iter(pred))]['observation']['outputs']['conserved']=True;path.write_bytes(encode(v));p=replace(p,expectations_digest=raw_digest(path.read_bytes()))
        with self.assertRaises(ProfileError) as e:admit(r,p,f)
        self.assertEqual(e.exception.code,'PREDICTION_MISMATCH')
    def test_actual_without_predictor(self):
        with patch.object(expectation,'derive',side_effect=RuntimeError('unavailable')):self.assertFalse(model.evaluate(ROOT,{'inputs':self.fixture(2)['cases'][0]['inputs']})['outputs']['conserved'])
    def test_predictor_without_actual(self):
        f=self.fixture(2);before=expectation.predict(f)
        with patch.object(model,'evaluate',side_effect=RuntimeError('unavailable')):self.assertEqual(expectation.predict(f),before)
    def test_dependency_separation(self):
        self.assertNotIn('adapters.',inspect.getsource(expectation));self.assertNotIn('subprocess',inspect.getsource(expectation));self.assertNotIn('expectation',inspect.getsource(model));self.assertNotIn('expectations.v0.json',(ROOT/'adapters/aggregate/execute.mjs').read_text())
        # The predictor function never reads a frozen row or a source-gate output.
        self.assertNotIn('load(',inspect.getsource(expectation.derive));self.assertNotIn('valueFor',inspect.getsource(expectation.derive))
    def test_exact_version(self):
        f=self.fixture(1);f['relation_profile_version']='latest'
        with self.assertRaises(UnavailableRelation):resolve_fixture(f,composition(ROOT)[3])
    def test_id_not_authority(self):
        f=self.fixture(2);a=list(expectation.predict(f).values());f['id']='anything';self.assertEqual(a,list(expectation.predict(f).values()))
    def test_transport(self):
        v=self.fixture(1)['cases'][0]['inputs'];v['roots'][0]['cap']='9007199254740993';relation.validate_inputs(v);v['roots'][0]['cap']=9007199254740993
        with self.assertRaises(ValueError):relation.validate_inputs(v)
    def test_arithmetic_scope(self):
        v=self.fixture(1)['cases'][0]['inputs'];v['steps'][-1]['amount']=str(2**256-1)
        with self.assertRaises(ValueError):relation.validate_inputs(v)
    def test_large_decimal_exact(self):
        v=self.fixture(1)['cases'][0]['inputs'];scale=2**100;v['roots'][0]['cap']=str(1000*scale)
        for s in v['steps']:
            if s['op']=='draw':s['amount']=str(int(s['amount'])*scale)
        relation.validate_inputs(v);self.assertEqual(model.evaluate(ROOT,{'inputs':v}),expectation.derive(v))
    def test_draw_period_cannot_be_hidden(self):
        v=self.fixture(7)['cases'][0]['inputs'];v['periods']=[1]
        with self.assertRaises(ValueError):relation.validate_inputs(v)
    def test_recompute_vectors_definition(self):
        rows=json.loads((ROOT/'evidence/aggregate/recompute-kit/aggregate-budget-v0.vectors.json').read_text(encoding='utf-8'))['vectors']
        inputs=[{k:v for k,v in r.items() if k in ('rootId','periodIndex','cap','log')} for r in rows]
        js="import {valueFor} from './evidence/aggregate/gate.mjs';let s='';for await(const c of process.stdin)s+=c;console.log(JSON.stringify(JSON.parse(s).map(v=>valueFor(v,false))));"
        p=subprocess.run(['node','--input-type=module','-e',js],input=json.dumps(inputs).encode(),cwd=ROOT,capture_output=True,check=True)
        actual=json.loads(p.stdout);self.assertEqual(len(actual),7)
        for v,a in zip(inputs,actual):
            amount=sum(int(e['amount']) for e in v['log'] if e['admitted'] and e['rootId'].lower()==v['rootId'].lower() and e['periodIndex']==v['periodIndex'])
            self.assertEqual(a,dict(admittedSum=str(amount),conserves=amount<=int(v['cap'])))
    def test_nine_family_pipeline(self):
        from extensions.capv import complete_composition as previous
        prior=execute(ROOT,*previous(ROOT));current=execute(ROOT,*complete_composition(ROOT));self.assertEqual(current['totals'],dict(PASS=111,FAIL=0,INVALID_FIXTURE=0,UNSUPPORTED=0))
        keys={r['result']['key'] for r in prior['rows']};self.assertEqual(prior['rows'],[r for r in current['rows'] if r['result']['key'] in keys])
    def test_no_core_or_prior_changes(self):
        p=json.loads((ROOT/'evidence/aggregate/protected-baseline.v0.json').read_bytes());self.assertEqual(len(p),498)
        for name,digest in p.items():self.assertEqual(raw_digest((ROOT/name).read_bytes()),digest,name)

if __name__=='__main__':unittest.main()
