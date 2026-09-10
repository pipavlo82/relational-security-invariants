from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import unittest, tempfile, shutil, inspect
from unittest.mock import patch
from rsi.codec import load,encode,raw_digest
from runner.relation_runtime import execute,resolve_fixture
from runner.expectation_contract import admit,load_fixtures,ProfileError
from runner.relation_profile_registry import UnavailableRelation
from extensions.verify_layer import composition,complete_composition
from profiles.verify_layer import relation,expectation,source
from adapters.verify_layer import model
ROOT=Path(__file__).resolve().parents[1]

class VerifyLayerTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='vl-test-');self.root=Path(self.tmp.name)
        for d in ('profiles/verify_layer','adapters/verify_layer','evidence/verify-layer','corpora/verify-layer'):
            shutil.copytree(ROOT/d,self.root/d,ignore=shutil.ignore_patterns('__pycache__'))
        (self.root/'extensions').mkdir();shutil.copy2(ROOT/'extensions/verify_layer.corpus.v0.json',self.root/'extensions/verify_layer.corpus.v0.json')
    def tearDown(self):self.tmp.cleanup()
    def run_domain(self):return execute(self.root,*composition(self.root))
    def observed(self,key):
        r=self.run_domain()
        if not r['admissions'] or any(x.get('diagnostic_kind') or x.get('result',{}).get('errors') for x in r['rows']):raise RuntimeError('mapped decision not reached')
        row=next(x['result'] for x in r['rows'] if x['result']['key']==key)
        return row,row['observed']['outputs']
    def fixture(self,n):return load(self.root/('corpora/verify-layer/fixtures/VL-RSI-%03d.json'%n))
    def test_pipeline(self):self.assertEqual(self.run_domain()['totals'],dict(PASS=6,FAIL=0,INVALID_FIXTURE=0,UNSUPPORTED=0))
    def test_control(self):
        r,o=self.observed('VL-RSI-001/control');self.assertTrue(o['verified']);self.assertTrue(o['boundToHeader']);self.assertTrue(o['claimMatchesProof']);self.assertEqual(r['status'],'PASS')
    def test_wrong_root(self):
        r,o=self.observed('VL-RSI-002/wrong_root');self.assertFalse(o['boundToHeader']);self.assertFalse(o['verified']);self.assertTrue(o['claimMatchesProof']);self.assertEqual(r['status'],'PASS')
    def test_wrong_account(self):
        r,o=self.observed('VL-RSI-005/wrong_account');self.assertFalse(o['verified']);self.assertEqual(o['stateTrust'],'MPT-REJECTED');self.assertEqual(r['status'],'PASS')
    def test_mirror(self):
        r,o=self.observed('VL-RSI-006/hex_case_mirror');self.assertEqual(o,self.observed('VL-RSI-001/control')[1]);self.assertEqual(r['status'],'PASS')
    def test_no_header_promotion(self):
        r,o=self.observed('VL-RSI-007/rpc_header_only');self.assertTrue(o['verified']);self.assertEqual(o['headerAuthority'],'UNSUPPORTED');self.assertEqual(o['headerTrust'],'RPC-TRUSTED');self.assertEqual(r['status'],'PASS')
    def test_wrong_claim(self):
        r,o=self.observed('VL-RSI-008/wrong_balance');self.assertTrue(o['boundToHeader']);self.assertFalse(o['claimMatchesProof']);self.assertFalse(o['verified']);self.assertEqual(r['status'],'PASS')
    def test_no_downstream_promotion(self):
        r,o=self.observed('VL-RSI-007/rpc_header_only');self.assertEqual(o['downstreamAuthority'],'UNSUPPORTED');self.assertEqual(r['status'],'PASS')
    def test_actual_independent_of_predictor(self):
        v=self.fixture(1)['cases'][0]['inputs']
        with patch.object(expectation,'derive',side_effect=RuntimeError('oracle unavailable')):self.assertTrue(model.evaluate(self.root,{'inputs':v})['outputs']['verified'])
    def test_predictor_independent_of_actual(self):
        f=self.fixture(1);old=expectation.predict(f)
        with patch.object(model,'evaluate',side_effect=RuntimeError('adapter broken')):self.assertEqual(expectation.predict(f),old)
    def test_no_shared_semantic_helper(self):
        text=inspect.getsource(expectation);self.assertNotIn('adapters.',text);self.assertNotIn('proof-runtime',text)
        self.assertNotIn('oracle',inspect.getsource(model));self.assertNotIn('expectation',inspect.getsource(model));self.assertNotIn('expectation',inspect.getsource(relation))
    def test_tamper_atomic(self):
        p=expectation.make_profile(self.root);f=load_fixtures(self.root,p);path=self.root/p.expectations_path;x=load(path)
        first=x['expectations'][0]['prediction'];first[next(iter(first))]['observation']['outputs']['verified']=False;path.write_bytes(encode(x))
        p=replace(p,expectations_digest=raw_digest(path.read_bytes()))
        with self.assertRaises(ProfileError) as e:admit(self.root,p,f)
        self.assertEqual(e.exception.code,'PREDICTION_MISMATCH')
    def test_source_digest(self):
        p=self.root/'evidence/verify-layer/verify.mjs';p.write_bytes(p.read_bytes()+b'\n')
        self.assertEqual(self.run_domain()['totals']['UNSUPPORTED'],6)
    def test_source_commit(self):
        p=self.root/'evidence/verify-layer/source-pin.v0.json';x=load(p);x['commit']='0'*40;p.write_bytes(encode(x))
        with self.assertRaises(source.SourceUnavailable):source.verify_source(self.root)
    def test_source_original_bytes(self):
        self.assertEqual(raw_digest((self.root/'evidence/verify-layer/verify.mjs').read_bytes()),'ece05db266d1eb86ff71f47aa5a0666ada611dfd496ef0982e570406a28fb2d2')
    def test_bundle_drift(self):
        p=self.root/'evidence/verify-layer/proof-runtime.mjs';p.write_bytes(p.read_bytes()+b'\n')
        with self.assertRaises(source.SourceUnavailable):source.verify_source(self.root)
    def test_version_exact(self):
        f=self.fixture(1);f['relation_profile_version']='1'
        with self.assertRaises(UnavailableRelation):resolve_fixture(f,composition(self.root)[3])
    def test_unknown_relation(self):
        f=self.fixture(1);f['relation_id']='chain-authority'
        with self.assertRaises(UnavailableRelation):resolve_fixture(f,composition(self.root)[3])
    def test_required_slot(self):
        v=self.fixture(1)['cases'][0]['inputs'];del v['header']
        with self.assertRaises(ValueError):relation.validate_inputs(v)
    def test_no_fake_universal_fields(self):self.assertFalse({'proof','policy','state'} & set(self.fixture(1)['cases'][0]['inputs']))
    def test_identity_opaque(self):
        f=self.fixture(1);a=expectation.predict(f);f['id']='reject-unknown';b=expectation.predict(f);self.assertEqual(list(a.values()),list(b.values()))
    def test_deterministic(self):self.assertEqual(encode(self.run_domain()),encode(self.run_domain()))
    def test_seven_family_pipeline(self):
        r=execute(ROOT,*complete_composition(ROOT));self.assertEqual(r['totals'],dict(PASS=85,FAIL=0,INVALID_FIXTURE=0,UNSUPPORTED=0))
    def test_local_validity_negative(self):
        for n in (2,5,8):relation.validate_inputs(self.fixture(n)['cases'][0]['inputs'])
    def test_transport_exact_balance(self):
        v=self.fixture(1)['cases'][0]['inputs'];relation.validate_inputs(v);self.assertGreater(int(v['response']['balance'],16),2**53);v['response']['balance']=int(v['response']['balance'],16)
        with self.assertRaises(ValueError):relation.validate_inputs(v)
    def test_transport_unicode(self):
        v=self.fixture(1)['cases'][0]['inputs'];v['address']='\u0430'
        with self.assertRaises(ValueError):relation.validate_inputs(v)
    def test_keccak_known_answer(self):
        from profiles.verify_layer.oracle import keccak
        self.assertEqual(keccak(b'').hex(),'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470')
        self.assertEqual(keccak(b'abc').hex(),'4e03657aea45a94fc7d47ba826c8d667c0d1e6e33a64a036ec44f58fa12d6c45')
    def test_proof_original_relation_remains_valid(self):
        from profiles.verify_layer.oracle import account
        a=self.fixture(1)['cases'][0]['inputs'];b=self.fixture(2)['cases'][0]['inputs'];self.assertEqual(a['response'],b['response']);self.assertIsNotNone(account(b['response']['accountProof'],a['address']))
    def test_source_function_body_preserved(self):
        original=(self.root/'evidence/verify-layer/verify.mjs').read_text(encoding='utf8');entry=(self.root/'evidence/verify-layer/build-entry.mjs').read_text(encoding='utf8')
        self.assertIn(original[original.index('// Core:'):original.index('const fmt')],entry)
        self.assertNotIn('alchemy_key',entry);self.assertNotIn('fetch(',entry)
    def test_float_display_excluded_explicitly(self):
        o=model.evaluate(self.root,{'inputs':self.fixture(1)['cases'][0]['inputs']})['outputs'];self.assertNotIn('provenBalanceEth',o);self.assertIsInstance(o['provenBalanceWei'],str)
    def test_unbound_rpc_context_not_claimed(self):
        a=self.fixture(1)['cases'][0]['inputs'];b=deepcopy(a);b['header']['number']='0x1'
        self.assertEqual(model.evaluate(self.root,{'inputs':a}),model.evaluate(self.root,{'inputs':b}))
    def test_core_anti_coupling(self):
        import ast
        for p in [*(ROOT/'runner').glob('*.py'),ROOT/'rsi/run.py',ROOT/'rsi/oracle.py']:
            for n in ast.walk(ast.parse(p.read_text())):
                if isinstance(n,(ast.If,ast.IfExp)):
                    text=ast.unparse(n.test).lower();self.assertFalse(any(t in text for t in ('verify-layer','verify_layer','account-proof-root-balance')),(str(p),text))
