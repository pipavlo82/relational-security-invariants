from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import unittest, tempfile, shutil, inspect
from unittest.mock import patch
from rsi.codec import load,encode,raw_digest
from runner.relation_runtime import execute,resolve_fixture
from runner.expectation_contract import admit,load_fixtures,ProfileError
from runner.relation_profile_registry import UnavailableRelation
from extensions.tas import composition,complete_composition
from profiles.tas import relation,expectation,source
from adapters.tas import model
ROOT=Path(__file__).resolve().parents[1]
class TASTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='tas-test-');self.root=Path(self.tmp.name)
        for d in ('profiles/tas','adapters/tas','evidence/tas','corpora/tas'):
            shutil.copytree(ROOT/d,self.root/d,ignore=shutil.ignore_patterns('__pycache__'))
        (self.root/'extensions').mkdir();shutil.copy2(ROOT/'extensions/tas.corpus.v0.json',self.root/'extensions/tas.corpus.v0.json')
    def tearDown(self):self.tmp.cleanup()
    def run_domain(self):return execute(self.root,*composition(self.root))
    def observed(self,key):
        r=self.run_domain()
        if not r['admissions'] or any(x.get('diagnostic_kind') or x.get('result',{}).get('errors') for x in r['rows']):raise RuntimeError('mapped decision not reached')
        row=next(x['result'] for x in r['rows'] if x['result']['key']==key)
        return row,row['observed']['outputs']
    def fixture(self,n):return load(self.root/('corpora/tas/fixtures/TAS-RSI-%03d.json'%n))
    def test_pipeline(self):self.assertEqual(self.run_domain()['totals'],dict(PASS=8,FAIL=0,INVALID_FIXTURE=0,UNSUPPORTED=0))
    def test_control(self):
        r,o=self.observed('TAS-RSI-001/control');self.assertTrue(o['invocation_admitted']);self.assertEqual(r['status'],'PASS')
    def test_no_accepted_context(self):
        r,o=self.observed('TAS-RSI-001/not_accepted');self.assertFalse(o['invocation_admitted']);self.assertEqual(r['status'],'PASS')
    def test_target_substitution(self):
        r,o=self.observed('TAS-RSI-002/workflow_substitution');self.assertIsNone(o['native']['dispatched']);self.assertEqual(o['native']['error'],'WORKFLOW_SOURCE_VERIFICATION_REQUIRED');self.assertEqual(r['status'],'PASS')
    def test_scope_substitution(self):
        r,o=self.observed('TAS-RSI-004/fingerprint_substitution');self.assertFalse(o['invocation_admitted']);self.assertEqual(r['status'],'PASS')
    def test_member_substitution(self):
        r,o=self.observed('TAS-RSI-004/member_substitution');self.assertEqual(o['native']['error'],'AUTHORIZATION_DENIED');self.assertFalse(o['invocation_admitted']);self.assertEqual(r['status'],'PASS')
    def test_exact_member_block(self):
        r,o=self.observed('TAS-RSI-004/member_stale_block');self.assertEqual(o['native']['error'],'AUTHORIZATION_DENIED');self.assertEqual(r['status'],'PASS')
    def test_mirror(self):
        r,o=self.observed('TAS-RSI-005/new_exact_block');self.assertTrue(o['invocation_admitted']);self.assertEqual(r['status'],'PASS')
    def test_no_execution_promotion(self):
        r,o=self.observed('TAS-RSI-006/dispatch_is_not_execution');self.assertTrue(o['invocation_admitted']);self.assertEqual(o['execution_occurrence'],'UNSUPPORTED');self.assertEqual(r['status'],'PASS')
    def test_actual_independent_of_predictor(self):
        v=self.fixture(1)['cases'][0]['inputs']
        with patch.object(expectation,'derive',side_effect=RuntimeError('oracle unavailable')):self.assertTrue(model.evaluate(self.root,{'inputs':v})['outputs']['invocation_admitted'])
    def test_predictor_independent_of_actual(self):
        f=self.fixture(1);old=expectation.predict(f)
        with patch.object(model,'evaluate',side_effect=RuntimeError('adapter broken')):self.assertEqual(expectation.predict(f),old)
    def test_predictor_no_adapter_import(self):
        s=inspect.getsource(expectation);self.assertNotIn('adapters.',s);self.assertNotIn('source-runtime',s)
    def test_actual_no_expected_access(self):
        self.assertNotIn('expectation',inspect.getsource(model));self.assertNotIn('expectation',inspect.getsource(relation))
    def test_tamper_atomic(self):
        p=expectation.make_profile(self.root);f=load_fixtures(self.root,p);path=self.root/p.expectations_path;x=load(path)
        first=x['expectations'][0]['prediction'];first[next(iter(first))]['observation']['outputs']['execution_occurrence']='PROVEN';path.write_bytes(encode(x))
        p=replace(p,expectations_digest=raw_digest(path.read_bytes()))
        with self.assertRaises(ProfileError) as e:admit(self.root,p,f)
        self.assertEqual(e.exception.code,'PREDICTION_MISMATCH')
    def test_source_digest(self):
        p=self.root/'evidence/tas/source-runtime.mjs';p.write_bytes(p.read_bytes()+b'\n')
        self.assertEqual(self.run_domain()['totals']['UNSUPPORTED'],5)
    def test_source_commit(self):
        p=self.root/'evidence/tas/source-pin.v0.json';x=load(p);x['commit']='0'*40;p.write_bytes(encode(x))
        with self.assertRaises(source.SourceUnavailable):source.verify_source(self.root)
    def test_version_exact(self):
        f=self.fixture(1);f['relation_profile_version']='1'
        with self.assertRaises(UnavailableRelation):resolve_fixture(f,composition(self.root)[3])
    def test_unknown_relation(self):
        f=self.fixture(1);f['relation_id']='another'
        with self.assertRaises(UnavailableRelation):resolve_fixture(f,composition(self.root)[3])
    def test_required_slot(self):
        v=self.fixture(1)['cases'][0]['inputs'];del v['member']
        with self.assertRaises(ValueError):relation.validate_inputs(v)
    def test_no_fake_universal_fields(self):
        self.assertFalse({'proof','policy','state'} & set(self.fixture(1)['cases'][0]['inputs']))
    def test_identity_opaque(self):
        f=self.fixture(1);a=expectation.predict(f);f['id']='not-a-verdict';b=expectation.predict(f)
        self.assertEqual(list(a.values()),list(b.values()))
    def test_deterministic(self):self.assertEqual(encode(self.run_domain()),encode(self.run_domain()))
    def test_five_family_pipeline(self):
        r=execute(ROOT,*complete_composition(ROOT));self.assertEqual(r['totals'],dict(PASS=72,FAIL=0,INVALID_FIXTURE=0,UNSUPPORTED=0))
    def test_schema_valid(self):resolve_fixture(self.fixture(1),composition(self.root)[3])
    def test_unbound_task_not_reinterpreted(self):
        v=self.fixture(1)['cases'][0]['inputs'];v['task_hash']='0x'+'2'*64
        o=model.evaluate(self.root,{'inputs':v})['outputs'];self.assertTrue(o['invocation_admitted']);self.assertEqual(o['native']['dispatched']['arguments'],['0x'+'2'*64])
    def test_unknown_method_not_dispatched(self):
        v=self.fixture(1)['cases'][0]['inputs'];v['tool_name']='unregistered-tool'
        o=model.evaluate(self.root,{'inputs':v})['outputs'];self.assertEqual(o['native']['error'],'MANIFEST_BINDING_UNSUPPORTED')
    def test_local_validity_negative(self):relation.validate_inputs(self.fixture(2)['cases'][0]['inputs'])
    def test_transport_unicode(self):
        v=self.fixture(1)['cases'][0]['inputs'];v['task_hash']='\u0430'
        with self.assertRaises(ValueError):relation.validate_inputs(v)
    def test_member_required(self):
        v=self.fixture(1)['cases'][0]['inputs'];v['member']['is_member']=False
        self.assertEqual(model.evaluate(self.root,{'inputs':v})['outputs']['native']['error'],'AUTHORIZATION_DENIED')
