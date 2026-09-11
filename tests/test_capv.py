from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import inspect,json,shutil,tempfile,unittest
from unittest.mock import patch
from rsi.codec import load,encode,raw_digest
from runner.relation_runtime import execute,resolve_fixture
from runner.expectation_contract import admit,load_fixtures,ProfileError
from runner.relation_profile_registry import UnavailableRelation
from profiles.capv import relation,expectation,source
from adapters.capv import model
from extensions.capv import composition,complete_composition
ROOT=Path(__file__).resolve().parents[1]

class CAPVTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=execute(ROOT,*composition(ROOT))
        if not cls.report['admissions'] or any(r.get('diagnostic_kind') or r.get('result',{}).get('errors') for r in cls.report['rows']):raise RuntimeError('mapped EVM decision not reached')
    def observed(self,key):
        r=next(r['result'] for r in self.report['rows'] if r['result']['key']==key)
        return r,r['observed']['outputs']
    def fixture(self,n):return load(ROOT/f'corpora/capv/fixtures/CAPV-RSI-{n:03}.json')
    def clone(self):
        tmp=tempfile.TemporaryDirectory(prefix='capv-test-');self.addCleanup(tmp.cleanup);r=Path(tmp.name)
        for d in ('profiles/capv','adapters/capv','evidence/capv','corpora/capv'):shutil.copytree(ROOT/d,r/d,ignore=shutil.ignore_patterns('__pycache__'))
        (r/'extensions').mkdir();shutil.copy2(ROOT/'extensions/capv.corpus.v0.json',r/'extensions/capv.corpus.v0.json');return r
    def test_pipeline(self):self.assertEqual(self.report['totals'],dict(PASS=14,FAIL=0,INVALID_FIXTURE=0,UNSUPPORTED=0))
    def test_normative_obligation(self):
        r,o=self.observed('CAPV-RSI-001/normative_obligation');self.assertTrue(o['normative_expiry_public']);self.assertFalse(o['expiry_public']);self.assertEqual(o['canonical_asset_alignment'],'MISMATCH');self.assertEqual(r['status'],'PASS')
    def test_old_control(self):
        r,o=self.observed('CAPV-RSI-002/old_control');self.assertTrue(o['proof_verifies']);self.assertTrue(o['adapter_verifies']);self.assertEqual(o['public_input_count'],39);self.assertEqual(r['status'],'PASS')
    def test_old_substitution(self):
        r,o=self.observed('CAPV-RSI-003/old_expiry_substitution');self.assertTrue(o['proof_verifies']);self.assertFalse(o['expiry_bound_to_this_proof']);self.assertEqual(r['status'],'PASS')
    def test_fresh_not_bound(self):
        r,o=self.observed('CAPV-RSI-004/fresh_not_bound');self.assertTrue(o['expiry_fresh']);self.assertFalse(o['expiry_bound_to_this_proof']);self.assertEqual(o['guard_acceptance'],'UNSUPPORTED');self.assertEqual(r['status'],'PASS')
    def test_fixed_control(self):
        r,o=self.observed('CAPV-RSI-005/fixed_control');self.assertTrue(o['proof_verifies']);self.assertTrue(o['adapter_verifies']);self.assertTrue(o['expiry_public']);self.assertTrue(o['expiry_bound_to_this_proof']);self.assertEqual(o['public_input_count'],40);self.assertEqual(r['status'],'PASS')
    def test_fixed_substitution(self):
        r,o=self.observed('CAPV-RSI-006/fixed_expiry_substitution');self.assertTrue(o['expiry_public']);self.assertTrue(o['expiry_fresh']);self.assertFalse(o['proof_verifies']);self.assertFalse(o['adapter_verifies']);self.assertEqual(r['status'],'PASS')
    def test_generation(self):
        for key in ('fixed_with_sdk_proof','sdk_with_fixed_proof'):
            r,o=self.observed('CAPV-RSI-007/'+key);self.assertFalse(o['proof_program_matches']);self.assertFalse(o['proof_verifies']);self.assertEqual(r['status'],'PASS')
    def test_nonretroactivity(self):
        r,o=self.observed('CAPV-RSI-008/historical_consumer');self.assertTrue(o['consumer_generation_matches']);self.assertTrue(o['proof_verifies']);self.assertFalse(o['expiry_public']);self.assertEqual(o['program_generation'],source.OLD);self.assertEqual(r['status'],'PASS')
        r,o=self.observed('CAPV-RSI-008/future_generation_not_historical');self.assertTrue(o['proof_verifies']);self.assertFalse(o['consumer_generation_matches']);self.assertEqual(r['status'],'PASS')
    def test_asset_mismatch(self):
        r,o=self.observed('CAPV-RSI-009/canonical_asset_mismatch');self.assertFalse(o['canonical_asset_expiry_public']);self.assertTrue(o['normative_expiry_public']);self.assertEqual(r['status'],'PASS')
    def test_mirror(self):
        r,o=self.observed('CAPV-RSI-010/timestamp_mirror');self.assertEqual(o,self.observed('CAPV-RSI-005/fixed_control')[1]);self.assertEqual(r['status'],'PASS')
    def test_program_key(self):
        for g in ('sdk','fixed'):
            r,o=self.observed('CAPV-RSI-011/'+g+'_wrong_program_key');self.assertTrue(o['proof_verifies']);self.assertFalse(o['program_key_matches_vk']);self.assertFalse(o['adapter_verifies']);self.assertEqual(r['status'],'PASS')
    def test_only_expiry_changes(self):
        for a,b in [(2,3),(5,6)]:
            x=self.fixture(a)['cases'][0]['inputs'];y=self.fixture(b)['cases'][0]['inputs'];self.assertNotEqual(x,y);x['verdict']['expiry']=y['verdict']['expiry'];self.assertEqual(x,y)
    def test_only_observation_changes(self):
        a=self.fixture(5)['cases'][0]['inputs'];b=self.fixture(10)['cases'][0]['inputs'];a['observation_time']=b['observation_time'];self.assertEqual(a,b)
    def test_source_pins(self):
        p=source.verify_source(ROOT);self.assertEqual(p['sdk_commit'],'e41b117893fb56bc869922de378daf91aad63def');self.assertEqual(p['generations']['fixed'],'d950ac1422cf79bafff11fcfb62c3e8b4ce3d782')
    def test_sdk_vendor_identity(self):
        for a,b in [('HonkVerifier.sol','src/verifier/HonkVerifier.sol'),('fixtures/allowlist.proof','test/fixtures/allowlist.proof'),('fixtures/allowlist.public_inputs','test/fixtures/allowlist.public_inputs')]:self.assertEqual((ROOT/'evidence/capv/sdk'/a).read_bytes(),(ROOT/'evidence/capv/old'/b).read_bytes())
    def test_stale_source(self):
        r=self.clone();p=r/'evidence/capv/fixed/noir/src/main.nr';p.write_bytes(p.read_bytes()+b'\n');self.assertEqual(execute(r,*composition(r))['totals']['UNSUPPORTED'],11)
    def test_wrong_generation_pin(self):
        r=self.clone();p=r/'evidence/capv/source-pin.v0.json';v=load(p);v['generations']['sdk']=source.FIXED;p.write_bytes(encode(v))
        with self.assertRaises(source.SourceUnavailable):source.verify_source(r)
    def test_compiled_digest(self):
        r=self.clone();p=r/'evidence/capv/fixed.json';p.write_bytes(p.read_bytes()+b' ')
        with self.assertRaises(source.SourceUnavailable):source.verify_source(r)
    def test_tamper_atomic(self):
        r=self.clone();p=expectation.make_profile(r);f=load_fixtures(r,p);path=r/p.expectations_path;v=load(path);pred=v['expectations'][0]['prediction'];pred[next(iter(pred))]['observation']['outputs']['expiry_public']=True;path.write_bytes(encode(v));p=replace(p,expectations_digest=raw_digest(path.read_bytes()))
        with self.assertRaises(ProfileError) as e:admit(r,p,f)
        self.assertEqual(e.exception.code,'PREDICTION_MISMATCH')
    def test_actual_without_predictor(self):
        with patch.object(expectation,'derive',side_effect=RuntimeError('unavailable')):self.assertTrue(model.evaluate(ROOT,{'inputs':self.fixture(5)['cases'][0]['inputs']})['outputs']['proof_verifies'])
    def test_predictor_without_actual(self):
        f=self.fixture(5);before=expectation.predict(f)
        with patch.object(model,'evaluate',side_effect=RuntimeError('unavailable')):self.assertEqual(expectation.predict(f),before)
    def test_predictor_without_frozen_rows(self):
        r=self.clone();(r/'profiles/capv/expectations.v0.json').unlink();self.assertEqual(expectation.predict_at(r,self.fixture(5)),expectation.predict(self.fixture(5)))
    def test_dependency_separation(self):
        self.assertNotIn('adapters.',inspect.getsource(expectation));self.assertNotIn('subprocess',inspect.getsource(expectation));self.assertNotIn('expectation',inspect.getsource(model));self.assertNotIn('expectations.v0.json',(ROOT/'adapters/capv/execute.mjs').read_text())
    def test_exact_version(self):
        f=self.fixture(1);f['relation_profile_version']='latest'
        with self.assertRaises(UnavailableRelation):resolve_fixture(f,composition(ROOT)[3])
    def test_id_not_authority(self):
        f=self.fixture(3);a=list(expectation.predict(f).values());f['id']='anything';self.assertEqual(a,list(expectation.predict(f).values()))
    def test_transport(self):
        v=self.fixture(5)['cases'][0]['inputs'];v['verdict']['expiry']='9007199254740993';relation.validate_inputs(v)
        v['verdict']['expiry']=9007199254740993
        with self.assertRaises(ValueError):relation.validate_inputs(v)
    def test_expiry_boundary(self):
        v=self.fixture(5)['cases'][0]['inputs'];v['observation_time']=v['verdict']['expiry'];o=model.evaluate(ROOT,{'inputs':v})['outputs'];self.assertFalse(o['expiry_fresh']);self.assertTrue(o['expiry_bound_to_this_proof']);self.assertTrue(o['proof_verifies'])
    def test_unsupported_claims(self):
        for row in self.report['rows']:
            o=row['result']['observed']['outputs']
            for k in ('guard_acceptance','domain_root_acceptability','executor_authorization','execution_occurrence'):self.assertEqual(o[k],'UNSUPPORTED')
    def test_eight_family_pipeline(self):
        from extensions.verify_layer import complete_composition as previous
        prior=execute(ROOT,*previous(ROOT));current=execute(ROOT,*complete_composition(ROOT))
        self.assertEqual(current['totals'],dict(PASS=99,FAIL=0,INVALID_FIXTURE=0,UNSUPPORTED=0))
        # Ordered prior rows remain exactly equal, including their observations and admissions.
        prior_keys={r['result']['key'] for r in prior['rows']}
        self.assertEqual(prior['rows'],[r for r in current['rows'] if r['result']['key'] in prior_keys])
    def test_no_core_changes(self):
        p=load(ROOT/'evidence/capv/protected-baseline.v0.json')
        for name,digest in p.items():self.assertEqual(raw_digest((ROOT/name).read_bytes()),digest,name)

if __name__=='__main__':unittest.main()
