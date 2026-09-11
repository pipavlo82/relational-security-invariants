"""Real signed records; separately test relation failure and stronger unsupported claims."""
from dataclasses import replace
from pathlib import Path
import inspect,json,shutil,tempfile,unittest
from unittest.mock import patch
from tools.protected_maintenance import mismatches
from rsi.codec import load,encode,raw_digest
from runner.relation_runtime import execute,resolve_fixture
from runner.expectation_contract import admit,load_fixtures,ProfileError
from runner.relation_profile_registry import UnavailableRelation
from profiles.judgment import expectation,relation,source
from adapters.judgment import model
from extensions.judgment import composition,complete_composition
ROOT=Path(__file__).resolve().parents[1]

class JudgmentTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=execute(ROOT,*composition(ROOT))
        if not cls.report['admissions'] or any(r.get('diagnostic_kind') or r.get('result',{}).get('errors') for r in cls.report['rows']):raise RuntimeError('mapped source evaluation not reached')
    def observed(self,n):return next(r['result']['observed']['outputs'] for r in self.report['rows'] if r['result']['key'].startswith(f'JEX-RSI-{n:03}/'))
    def fixture(self,n):return load(ROOT/f'corpora/judgment/fixtures/JEX-RSI-{n:03}.json')
    def clone(self):
        t=tempfile.TemporaryDirectory(prefix='judgment-test-');self.addCleanup(t.cleanup);r=Path(t.name)
        for p in ('profiles/judgment','adapters/judgment','corpora/judgment','evidence/judgment'):shutil.copytree(ROOT/p,r/p,ignore=shutil.ignore_patterns('__pycache__'))
        (r/'extensions').mkdir();shutil.copy2(ROOT/'extensions/judgment.corpus.v0.json',r/'extensions/judgment.corpus.v0.json');return r
    def test_pipeline(self):self.assertEqual(self.report['totals'],dict(PASS=12,FAIL=0,INVALID_FIXTURE=0,UNSUPPORTED=0))
    def test_control(self):
        o=self.observed(1);self.assertTrue(o['signature_valid']);self.assertTrue(o['binding_established']);self.assertEqual(o['verdict_decision'],'reject')
    def test_terminal_substitution(self):
        o=self.observed(2);self.assertTrue(o['signature_valid']);self.assertTrue(o['admission_bound']);self.assertFalse(o['binding_established']);self.assertFalse(o['chain_bound'])
    def test_action_ref(self):
        o=self.observed(3);self.assertTrue(o['signature_valid']);self.assertFalse(o['chain_bound']);self.assertEqual(o['source_failure'],'chain_join_failed')
    def test_other_signed_envelope(self):
        o=self.observed(4);self.assertTrue(o['signature_valid']);self.assertFalse(o['admission_bound']);self.assertEqual(o['source_failure'],'verdict_binding_failed')
    def test_identity_self(self):
        o=self.observed(5);self.assertTrue(o['signature_valid']);self.assertFalse(o['admission_bound']);self.assertEqual(o['source_failure'],'admission_not_independent')
    def test_identity_not_policy_listed(self):
        o=self.observed(6);self.assertTrue(o['signature_valid']);self.assertFalse(o['admission_bound']);self.assertEqual(o['source_failure'],'key_different_but_identity_unproven')
    def test_late_anchor(self):self.assertFalse(self.observed(7)['ordering_established_under_declared_anchor'])
    def test_no_anchor(self):
        o=self.observed(8);self.assertIsNone(o['ordering_established_under_declared_anchor']);self.assertEqual(o['source_checks']['anchoring_precedence']['code'],'not_assessable')
    def test_mirror(self):self.assertEqual(self.observed(1),self.observed(9))
    def test_declared_hash(self):self.assertEqual(self.observed(10)['source_failure'],'envelope_hash_mismatch')
    def test_existence_not_precedence(self):
        o=self.observed(11);self.assertTrue(o['source_checks']['anchoring_existence']['pass']);self.assertFalse(o['ordering_established_under_declared_anchor'])
    def test_execution_unsupported(self):
        for i in (1,12):self.assertTrue(self.observed(i)['binding_established']);self.assertEqual(self.observed(i)['execution_occurrence'],'UNSUPPORTED')
        self.assertEqual(self.observed(1),self.observed(12))
    def test_authorization_not_inherited(self):
        o=self.observed(1);self.assertTrue(o['source_overall']);self.assertEqual(o['verdict_decision'],'reject');self.assertEqual(o['action_authorization'],'UNSUPPORTED')
    def test_anchor_not_authority(self):
        o=self.observed(1);self.assertTrue(o['source_checks']['anchoring_existence']['pass']);self.assertEqual(o['anchor_authority'],'UNSUPPORTED')
    def test_source_pins(self):
        p=source.verify_source(ROOT);self.assertEqual(len(p['files']),20)
        self.assertIn('76d19dc394b208d01ba368382b3e5f4f2c18f0ee',json.dumps(p));self.assertIn('c0e13d17940a6eabe4d842e623fd0f871550ef7b',json.dumps(p))
    def test_wrong_source_digest(self):
        r=self.clone();p=r/'evidence/judgment/reference/verifier.py';p.write_bytes(p.read_bytes()+b'\n')
        self.assertEqual(execute(r,*composition(r))['totals']['UNSUPPORTED'],12)
    def test_stale_manifest(self):
        r=self.clone();p=r/'evidence/judgment/source-pin.v0.json';p.write_bytes(p.read_bytes()+b' ')
        with self.assertRaises(source.SourceUnavailable):source.verify_source(r)
    def test_atomic_tamper(self):
        r=self.clone();p=expectation.make_profile(r);f=load_fixtures(r,p);path=r/p.expectations_path;v=load(path);pred=v['expectations'][1]['prediction'];pred[next(iter(pred))]['observation']['outputs']['binding_established']=True;path.write_bytes(encode(v));p=replace(p,expectations_digest=raw_digest(path.read_bytes()))
        with self.assertRaises(ProfileError) as e:admit(r,p,f)
        self.assertEqual(e.exception.code,'PREDICTION_MISMATCH')
    def test_actual_without_predictor(self):
        with patch.object(expectation,'derive',side_effect=RuntimeError('unavailable')):self.assertFalse(model.evaluate(ROOT,{'inputs':self.fixture(2)['cases'][0]['inputs']})['outputs']['binding_established'])
    def test_predictor_without_actual(self):
        f=self.fixture(2);before=expectation.predict(f)
        with patch.object(model,'evaluate',side_effect=RuntimeError('unavailable')):self.assertEqual(expectation.predict(f),before)
    def test_dependency_separation(self):
        self.assertNotIn('adapters.',inspect.getsource(expectation));self.assertNotIn('expectation',inspect.getsource(model))
        self.assertNotIn('evidence/',(ROOT/'profiles/judgment/signature.py').read_text());self.assertNotIn('expectations.v0.json',(ROOT/'adapters/judgment/execute.py').read_text())
    def test_no_annotation_or_id_authority(self):
        f=self.fixture(1);a=list(expectation.predict(f).values());f['id']='unrelated';self.assertEqual(a,list(expectation.predict(f).values()))
        for v in self.fixture(1)['cases']:self.assertNotIn('expected_overall',v['inputs']['record'])
    def test_exact_profile_version(self):
        f=self.fixture(1);f['relation_profile_version']='latest'
        with self.assertRaises(UnavailableRelation):resolve_fixture(f,composition(ROOT)[3])
    def test_signature_tamper(self):
        v=self.fixture(1)['cases'][0]['inputs'];v['record']['admission']['verdict_event']['sig']='00'*64;relation.validate_inputs(v)
        a=model.evaluate(ROOT,{'inputs':v});self.assertEqual(a,expectation.derive(v));self.assertFalse(a['outputs']['signature_valid']);self.assertFalse(a['outputs']['binding_established'])
    def test_exact_signed_bytes_and_large_amount(self):
        src=json.loads((ROOT/'evidence/judgment/reference/fixtures/positive.json').read_bytes());v=self.fixture(1)['cases'][0]['inputs'];self.assertEqual(v['record']['admission']['verdict_event'],src['admission']['verdict_event']);self.assertEqual(v['record']['canonical_envelope']['raw_input']['amount'],str(2**256-1))
    def test_transport_rejects_float_and_unicode(self):
        for value in (0.95,'\u00e9',2**53):
            v=self.fixture(1)['cases'][0]['inputs'];v['record']['chain']['terminal']['result']=value
            with self.assertRaises(ValueError):relation.validate_inputs(v)
    def test_source_assumptions_are_not_verified(self):
        o=self.observed(1);self.assertEqual(o['raw_to_canonical_derivation'],'UNSUPPORTED');self.assertEqual(o['judgment_soundness'],'UNSUPPORTED')
    def test_ten_family_pipeline(self):
        r=execute(ROOT,*complete_composition(ROOT));self.assertEqual(r['totals'],dict(PASS=123,FAIL=0,INVALID_FIXTURE=0,UNSUPPORTED=0))
        self.assertEqual(len(r['admissions']),11)
    def test_prior_files_unchanged_and_no_core_branch(self):
        p=load(ROOT/'evidence/judgment/protected-baseline.v0.json');self.assertEqual(len(p),572)
        self.assertEqual(mismatches(ROOT,p),[])
        for f in p:
            if f.startswith(('runner/','rsi/')) and f.endswith('.py'):
                t=(ROOT/f).read_text();self.assertNotIn('profiles.judgment',t);self.assertNotIn('erc8299',t)
