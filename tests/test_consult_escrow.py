from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import unittest, tempfile, shutil, inspect
from unittest.mock import patch
from rsi.codec import load,encode,raw_digest
from runner.relation_runtime import execute,resolve_fixture
from runner.expectation_contract import admit,load_fixtures,ProfileError
from runner.relation_profile_registry import UnavailableRelation
from extensions.consult_escrow import composition,complete_composition
from profiles.consult_escrow import relation,expectation,source
from adapters.consult_escrow import model
ROOT=Path(__file__).resolve().parents[1]

class ConsultEscrowTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='ce-test-');self.root=Path(self.tmp.name)
        for d in ('profiles/consult_escrow','adapters/consult_escrow','evidence/consult-escrow','corpora/consult-escrow'):
            shutil.copytree(ROOT/d,self.root/d,ignore=shutil.ignore_patterns('__pycache__'))
        (self.root/'extensions').mkdir();shutil.copy2(ROOT/'extensions/consult_escrow.corpus.v0.json',self.root/'extensions/consult_escrow.corpus.v0.json')
    def tearDown(self):self.tmp.cleanup()
    def run_domain(self):return execute(self.root,*composition(self.root))
    def observed(self,key):
        r=self.run_domain()
        if not r['admissions'] or any(x.get('diagnostic_kind') or x.get('result',{}).get('errors') for x in r['rows']):raise RuntimeError('mapped decision not reached')
        row=next(x['result'] for x in r['rows'] if x['result']['key']==key)
        return row,row['observed']['outputs']
    def fixture(self,n):return load(self.root/('corpora/consult-escrow/fixtures/CE-RSI-%03d.json'%n))
    def test_pipeline(self):self.assertEqual(self.run_domain()['totals'],dict(PASS=7,FAIL=0,INVALID_FIXTURE=0,UNSUPPORTED=0))
    def test_control(self):
        r,o=self.observed('CE-RSI-001/control');self.assertTrue(o['release_eligible']);self.assertEqual(r['status'],'PASS');self.assertEqual(o['provider_delta'],'1000000000000000000');self.assertEqual(o['released_event']['provider'],self.fixture(1)['cases'][0]['inputs']['provider']);self.assertEqual(o['escrow_status'],'Released')
    def test_wrong_attestor(self):
        r,o=self.observed('CE-RSI-001/wrong_attestor');self.assertFalse(o['release_eligible']);self.assertEqual(o['error'],'bad attestor sig');self.assertEqual(r['status'],'PASS')
    def test_wrong_job(self):
        r,o=self.observed('CE-RSI-002/wrong_job');self.assertFalse(o['release_eligible']);self.assertEqual(o['error'],'bad attestor sig');self.assertEqual(o['provider_delta'],'0');self.assertEqual(r['status'],'PASS')
    def test_wrong_result(self):
        r,o=self.observed('CE-RSI-002/wrong_result');self.assertFalse(o['release_eligible']);self.assertEqual(r['status'],'PASS')
    def test_replay(self):
        r,o=self.observed('CE-RSI-006/replayed_release');self.assertFalse(o['release_eligible']);self.assertEqual(o['error'],'not open');self.assertEqual(o['provider_delta'],'0');self.assertEqual(r['status'],'PASS')
    def test_mirror(self):
        r,o=self.observed('CE-RSI-007/relayer_mirror');self.assertTrue(o['release_eligible']);self.assertEqual(r['status'],'PASS');self.assertEqual(o,self.observed('CE-RSI-001/control')[1])
    def test_no_execution_promotion(self):
        r,o=self.observed('CE-RSI-008/preflight_only');self.assertTrue(o['release_eligible']);self.assertEqual(o['execution_occurrence'],'UNSUPPORTED');self.assertEqual(o['provider_delta'],'0');self.assertIsNone(o['released_event']);self.assertEqual(o['escrow_status'],'Open');self.assertEqual(r['status'],'PASS')
    def test_actual_independent_of_predictor(self):
        v=self.fixture(1)['cases'][0]['inputs']
        with patch.object(expectation,'derive',side_effect=RuntimeError('oracle unavailable')):self.assertTrue(model.evaluate(self.root,{'inputs':v})['outputs']['release_eligible'])
    def test_predictor_independent_of_actual(self):
        f=self.fixture(1);old=expectation.predict(f)
        with patch.object(model,'evaluate',side_effect=RuntimeError('adapter broken')):self.assertEqual(expectation.predict(f),old)
    def test_no_shared_semantic_helper(self):
        text=inspect.getsource(expectation);self.assertNotIn('adapters.',text);self.assertNotIn('evm-runtime',text)
        self.assertNotIn('crypto',inspect.getsource(model));self.assertNotIn('expectation',inspect.getsource(model));self.assertNotIn('expectation',inspect.getsource(relation))
    def test_tamper_atomic(self):
        p=expectation.make_profile(self.root);f=load_fixtures(self.root,p);path=self.root/p.expectations_path;x=load(path)
        first=x['expectations'][0]['prediction'];first[next(iter(first))]['observation']['outputs']['release_eligible']=False;path.write_bytes(encode(x))
        p=replace(p,expectations_digest=raw_digest(path.read_bytes()))
        with self.assertRaises(ProfileError) as e:admit(self.root,p,f)
        self.assertEqual(e.exception.code,'PREDICTION_MISMATCH')
    def test_source_digest(self):
        p=self.root/'evidence/consult-escrow/canonical.json';p.write_bytes(p.read_bytes()+b'\n')
        self.assertEqual(self.run_domain()['totals']['UNSUPPORTED'],5)
    def test_source_commit(self):
        p=self.root/'evidence/consult-escrow/source-pin.v0.json';x=load(p);x['commit']='0'*40;p.write_bytes(encode(x))
        with self.assertRaises(source.SourceUnavailable):source.verify_source(self.root)
    def test_source_original_bytes(self):
        import hashlib
        self.assertEqual(hashlib.sha256((self.root/'evidence/consult-escrow/ConsultEscrow.sol').read_bytes()).hexdigest(),'373e1f6feab886d1115eceef391cebce97a16b51d4bdfdfb1e5bd4bdb3bd07f5')
    def test_version_exact(self):
        f=self.fixture(1);f['relation_profile_version']='1'
        with self.assertRaises(UnavailableRelation):resolve_fixture(f,composition(self.root)[3])
    def test_unknown_relation(self):
        f=self.fixture(1);f['relation_id']='another'
        with self.assertRaises(UnavailableRelation):resolve_fixture(f,composition(self.root)[3])
    def test_required_slot(self):
        v=self.fixture(1)['cases'][0]['inputs'];del v['signature']
        with self.assertRaises(ValueError):relation.validate_inputs(v)
    def test_no_fake_universal_fields(self):self.assertFalse({'proof','policy','state'} & set(self.fixture(1)['cases'][0]['inputs']))
    def test_identity_opaque(self):
        f=self.fixture(1);a=expectation.predict(f);f['id']='not-a-verdict';b=expectation.predict(f);self.assertEqual(list(a.values()),list(b.values()))
    def test_deterministic(self):self.assertEqual(encode(self.run_domain()),encode(self.run_domain()))
    def test_six_family_pipeline(self):
        r=execute(ROOT,*complete_composition(ROOT));self.assertEqual(r['totals'],dict(PASS=79,FAIL=0,INVALID_FIXTURE=0,UNSUPPORTED=0))
    def test_local_validity_negative(self):
        for c in self.fixture(2)['cases']:relation.validate_inputs(c['inputs'])
    def test_transport_exact_uint256(self):
        v=self.fixture(1)['cases'][0]['inputs'];relation.validate_inputs(v);self.assertGreater(int(v['amount']),2**53);v['amount']=int(v['amount'])
        with self.assertRaises(ValueError):relation.validate_inputs(v)
    def test_transport_out_of_range(self):
        v=self.fixture(1)['cases'][0]['inputs'];v['deadline']=str(2**256)
        with self.assertRaises(ValueError):relation.validate_inputs(v)
    def test_transport_unicode(self):
        v=self.fixture(1)['cases'][0]['inputs'];v['job_id']='\u0430'
        with self.assertRaises(ValueError):relation.validate_inputs(v)
    def test_keccak_known_answer(self):
        from profiles.consult_escrow.crypto import keccak
        self.assertEqual(keccak(b'').hex(),'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470')
        self.assertEqual(keccak(b'abc').hex(),'4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45')
    def test_signature_valid_on_original_job_only(self):
        from profiles.consult_escrow.crypto import signer
        a=self.fixture(1)['cases'][0]['inputs'];b=self.fixture(2)['cases'][0]['inputs']
        self.assertEqual(a['signature'],b['signature']);self.assertEqual(signer(a['job_id'],a['result_hash'],a['signature']),a['attestor']);self.assertNotEqual(signer(b['job_id'],b['result_hash'],b['signature']),b['attestor'])
    def test_recovery_v_matters(self):
        v=self.fixture(1)['cases'][0]['inputs'];v['signature']=v['signature'][:-2]+('1b' if v['signature'].endswith('1c') else '1c')
        self.assertEqual(model.evaluate(self.root,{'inputs':v}),expectation.derive(v,'job-bound-release'));self.assertFalse(expectation.derive(v,'job-bound-release')['outputs']['release_eligible'])
    def test_state_bound_amount_recipient(self):
        v=self.fixture(1)['cases'][0]['inputs'];o=model.evaluate(self.root,{'inputs':v})['outputs'];self.assertEqual(o['released_event']['amount'],v['amount']);self.assertEqual(o['released_event']['provider'],v['provider'])
    def test_no_signed_amount_recipient_claim(self):
        abi=load(self.root/'evidence/consult-escrow/canonical.json',canonical=False)['abi'];release=next(x for x in abi if x.get('name')=='release');self.assertEqual([x['name'] for x in release['inputs']],['jobId','resultHash','signature'])
    def test_core_anti_coupling(self):
        import ast
        for p in [*(ROOT/'runner').glob('*.py'),ROOT/'rsi/run.py',ROOT/'rsi/oracle.py']:
            for n in ast.walk(ast.parse(p.read_text())):
                if isinstance(n,(ast.If,ast.IfExp)):
                    text=ast.unparse(n.test).lower();self.assertFalse(any(t in text for t in ('consult','escrow','job-bound-release')),(str(p),text))
