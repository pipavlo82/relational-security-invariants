"""Pinned declared-edge boundaries and additive registration gates."""
from copy import deepcopy
from dataclasses import replace
from pathlib import Path
import ast, inspect, shutil, subprocess, tempfile, unittest
from unittest.mock import patch
from jsonschema.exceptions import ValidationError
from rsi.codec import load, encode, raw_digest
from runner.relation_runtime import execute, resolve_fixture
from runner.expectation_contract import admit, load_fixtures, ProfileError
from runner.relation_profile_registry import UnavailableRelation
from extensions.semantic_abi import composition, complete_composition
from profiles.semantic_abi import relation, expectation, source, oracle
from adapters.semantic_abi import model
ROOT=Path(__file__).resolve().parents[1]


class SemanticAbiTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='sabi-test-')
        self.root=Path(self.tmp.name)
        for d in ('profiles/semantic_abi','adapters/semantic_abi','evidence/semantic-abi','corpora/semantic-abi'):
            shutil.copytree(ROOT/d,self.root/d,ignore=shutil.ignore_patterns('__pycache__'))
        (self.root/'extensions').mkdir()
        shutil.copy2(ROOT/'extensions/semantic_abi.corpus.v0.json',self.root/'extensions/semantic_abi.corpus.v0.json')
    def tearDown(self):self.tmp.cleanup()
    def fixture(self,n):return load(self.root/f'corpora/semantic-abi/fixtures/SABI-RSI-{n:03d}.json')
    def inputs(self,n):return self.fixture(n)['cases'][0]['inputs']
    def run_domain(self):return execute(self.root,*composition(self.root))
    def observed(self,n):
        report=self.run_domain()
        if not report['admissions'] or any(r.get('diagnostic_kind') or r.get('result',{}).get('errors') for r in report['rows']):
            raise RuntimeError('mapped decision not reached')
        f=self.fixture(n);key=f['id']+'/'+f['cases'][0]['case_id']
        r=next(r['result'] for r in report['rows'] if r['result']['key']==key)
        return r,r['observed']['outputs']
    def decision(self,n,wanted):
        r,o=self.observed(n)
        self.assertIs(o['edge_compatible'],wanted)
        self.assertEqual(r['status'],'PASS')
    def test_pipeline(self):self.assertEqual(self.run_domain()['totals'],dict(PASS=16,FAIL=0,INVALID_FIXTURE=0,UNSUPPORTED=0))
    def test_control(self):self.decision(1,True)
    def test_claim(self):self.decision(2,False)
    def test_scope(self):self.decision(3,False)
    def test_authority(self):self.decision(4,False)
    def test_time_value(self):self.decision(5,False)
    def test_time_kind(self):self.decision(6,False)
    def test_recomputation(self):self.decision(7,True)
    def test_no_universal_recomputation(self):self.decision(8,False)
    def test_recomputation_scope(self):self.decision(9,False)
    def test_recomputation_time(self):self.decision(10,False)
    def test_no_reverse_coercion(self):self.decision(11,False)
    def test_no_cross_claim_mixing(self):self.decision(12,False)
    def test_component_mirror(self):
        self.decision(13,True)
        self.assertEqual(self.observed(1)[1],self.observed(13)[1])
    def test_explicit_boundary(self):
        self.decision(14,False);self.assertTrue(self.observed(14)[1]['explicit_boundary_hit'])
    def test_reason_mirror(self):self.assertEqual(self.observed(14)[1],self.observed(15)[1])
    def test_positive_precedence(self):
        self.decision(16,True);self.assertFalse(self.observed(16)[1]['explicit_boundary_hit'])
    def test_no_truth_promotion(self):self.assertEqual(self.observed(1)[1]['claim_truth'],'UNSUPPORTED')
    def test_no_execution_promotion(self):self.assertEqual(self.observed(1)[1]['execution_occurrence'],'UNSUPPORTED')
    def test_actual_does_not_call_predictor(self):
        with patch.object(expectation,'derive',side_effect=RuntimeError('unavailable')):
            self.assertTrue(model.evaluate(self.root,{'inputs':self.inputs(1)})['outputs']['edge_compatible'])
    def test_predictor_does_not_call_actual(self):
        f=self.fixture(1);before=expectation.predict(f)
        with patch.object(model,'evaluate',side_effect=RuntimeError('unavailable')):self.assertEqual(expectation.predict(f),before)
    def test_semantic_dependency_separation(self):
        tree=ast.parse(inspect.getsource(oracle))
        self.assertFalse(any(isinstance(n,(ast.Import,ast.ImportFrom)) for n in ast.walk(tree)))
        self.assertNotIn('oracle',inspect.getsource(model))
        self.assertNotIn('expectation',inspect.getsource(model))
        self.assertNotIn('adapters.',inspect.getsource(expectation))
    def test_tamper_even_if_digest_repinned(self):
        p=expectation.make_profile(self.root);f=load_fixtures(self.root,p)
        path=self.root/p.expectations_path;x=load(path)
        row=x['expectations'][0]['prediction'];row[next(iter(row))]['observation']['outputs']['edge_compatible']=False
        path.write_bytes(encode(x));p=replace(p,expectations_digest=raw_digest(path.read_bytes()))
        with self.assertRaises(ProfileError) as err:admit(self.root,p,f)
        self.assertEqual(err.exception.code,'PREDICTION_MISMATCH')
    def test_source_drift(self):
        p=self.root/'evidence/semantic-abi/runner/src/linker.mjs';p.write_bytes(p.read_bytes()+b'\n')
        self.assertEqual(self.run_domain()['totals']['UNSUPPORTED'],16)
    def test_source_commit_drift(self):
        p=self.root/'evidence/semantic-abi/source-pin.v0.json';x=load(p);x['commit']='0'*40;p.write_bytes(encode(x))
        with self.assertRaises(source.SourceUnavailable):source.verify_source(self.root)
    def test_source_original_bytes(self):
        self.assertEqual(raw_digest((self.root/'evidence/semantic-abi/runner/src/linker.mjs').read_bytes()),'bae8e519361989bfadbb5d226cb9940255cd954c60b40ba42136a2b11161d391')
    def test_exact_version(self):
        f=self.fixture(1);f['relation_profile_version']='1'
        with self.assertRaises(UnavailableRelation):resolve_fixture(f,composition(self.root)[3])
    def test_unknown_relation(self):
        f=self.fixture(1);f['relation_id']='execution-authority'
        with self.assertRaises(UnavailableRelation):resolve_fixture(f,composition(self.root)[3])
    def test_temporal_shape(self):
        for mode in ('both','neither'):
            v=self.inputs(1)
            if mode=='both':v['requirement']['issued_at']='receipt.verified_at'
            else:del v['requirement']['verification_time']
            with self.subTest(mode=mode),self.assertRaises(ValidationError):relation.validate_inputs(self.root,v)
    def test_invalid_coordinates(self):
        for key,value in [('scope',''),('authority_class','UNKNOWN'),('claim_type',123),('verification_time',None)]:
            v=self.inputs(1);v['requirement'][key]=value
            with self.subTest(key=key),self.assertRaises(ValidationError):relation.validate_inputs(self.root,v)
    def test_transport_unicode(self):
        v=self.inputs(1);v['producer']['component']='\u0430'
        with self.assertRaises(ValueError):relation.validate_inputs(self.root,v)
    def test_transport_unsafe_number(self):
        v=self.inputs(1);v['requirement']['verification_time']=2**60
        with self.assertRaises(ValueError):relation.validate_inputs(self.root,v)
    def test_identity_opaque(self):
        f=self.fixture(1);a=expectation.predict(f);f['id']='unrelated-identifier'
        self.assertEqual(list(a.values()),list(expectation.predict(f).values()))
    def test_claim_order(self):
        v=self.inputs(12);a=model.evaluate(self.root,{'inputs':v})
        v['producer']['establishes'].reverse()
        self.assertEqual(a,model.evaluate(self.root,{'inputs':v}))
        self.assertEqual(a,oracle.derive(v))
    def test_deterministic(self):self.assertEqual(encode(self.run_domain()),encode(self.run_domain()))
    def test_negative_cases_are_well_formed(self):
        for n in range(1,17):relation.validate_inputs(self.root,self.inputs(n))
    def test_substitutions_hold_producer_constant(self):
        control=self.inputs(1)
        for n in range(2,11):
            self.assertEqual(self.inputs(n)['producer'],control['producer'],n)
        for n,key in [(2,'claim_type'),(3,'scope'),(4,'authority_class'),(5,'verification_time')]:
            candidate=self.inputs(n)['requirement']
            self.assertEqual({k for k in candidate if candidate[k]!=control['requirement'][k]},{key})


class SemanticAbiArchitectureTests(unittest.TestCase):
    def test_prior_composition_unchanged(self):
        from extensions.judgment import complete_composition as prior
        old=execute(ROOT,*prior(ROOT));new=execute(ROOT,*complete_composition(ROOT))
        self.assertEqual(old['totals'],dict(PASS=123,FAIL=0,INVALID_FIXTURE=0,UNSUPPORTED=0))
        self.assertEqual(new['totals'],dict(PASS=139,FAIL=0,INVALID_FIXTURE=0,UNSUPPORTED=0))
        for row in old['rows']:self.assertIn(row,new['rows'])
    def test_upstream_tests(self):
        p=subprocess.run(['node','--test','evidence/semantic-abi/runner/test/linker.test.mjs'],cwd=ROOT,capture_output=True)
        self.assertEqual(p.returncode,0,p.stdout.decode()+p.stderr.decode())
    def test_core_anti_coupling(self):
        for p in [*(ROOT/'runner').glob('*.py'),ROOT/'rsi/run.py',ROOT/'rsi/oracle.py']:
            for n in ast.walk(ast.parse(p.read_text())):
                if isinstance(n,(ast.If,ast.IfExp)):
                    self.assertFalse(any(t in ast.unparse(n.test).lower() for t in ('semantic-abi','semantic_abi','claim-authority-scope-time-binding')))
