import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from adapters.generic.artifacts import signature_valid, signed
from adapters.generic.models import status_evidence
from runner.engine import CHECKS, STATES, run_fixture, totals
from runner.prove_can_fail import STATES as MUTATION_STATES, PATCHES, classify, prove
from runner.schema_subset import Invalid, check_schema, load, validate
from runner.validate_fixtures import ROOT, collect, schema

FIXTURES = {f['id']:f for f in (load(p) for p in sorted((ROOT/'fixtures').glob('*.json')))}


class SchemaTests(unittest.TestCase):
    def setUp(self):
        self.s = schema()
        self.f = copy.deepcopy(FIXTURES['RSI-001'])

    def test_missing_protected_relation(self):
        del self.f['protected_relation']
        with self.assertRaises(Invalid): validate(self.f, self.s)

    def test_missing_expected_has_no_default(self):
        del self.f['expected']
        with self.assertRaises(Invalid): validate(self.f, self.s)

    def test_missing_relation_expected_has_no_default(self):
        del self.f['mutation']['relation_expected']
        with self.assertRaises(Invalid): validate(self.f, self.s)

    def test_invalid_expected_states(self):
        for state in ('ALLOW','PASS','UNKNOWN','',None,True,{},[]):
            with self.subTest(state=state):
                self.f['expected']=state
                with self.assertRaises(Invalid): validate(self.f, self.s)

    def test_unknown_fields_at_every_structural_level(self):
        for path in ((),('control',),('mutation',),('evaluator',),('control','components'),('control','components','artifact'),('control','components','artifact','body')):
            f=copy.deepcopy(self.f)
            target=f
            for key in path: target=target[key]
            target['unknown']=True
            with self.subTest(path=path), self.assertRaises(Invalid): validate(f,self.s)

    def test_wrong_component_shape(self):
        self.f['control']['components']=[]
        with self.assertRaises(Invalid): validate(self.f,self.s)

    def test_wrong_fixture_relation_mapping(self):
        self.f['protected_relation']='context_binding'
        with self.assertRaises(Invalid): validate(self.f,self.s)

    def test_numeric_boolean_not_coerced(self):
        self.f['mutation']['relation_expected']=0
        with self.assertRaises(Invalid): validate(self.f,self.s)

    def test_expected_constraints_cannot_be_weakened(self):
        self.f['failure_if']=[]
        with self.assertRaises(Invalid): validate(self.f,self.s)
        f=copy.deepcopy(FIXTURES['RSI-004'])
        f['final_state_constraints']['max_successful_consumers']=2
        with self.assertRaises(Invalid): validate(f,self.s)

    def test_unknown_schema_keywords_reject(self):
        for name in ('$ref','default','if','not','unevaluatedProperties'):
            with self.subTest(name=name), self.assertRaises(Invalid):
                check_schema({'type':'string',name:{}})

    def test_malformed_schema_shapes_reject(self):
        for s in (True,{}, {'type':'object'}, {'type':'array'}, {'type':['string']}, {'type':'string','items':{'type':'string'}}, {'type':'integer','minimum':True}, {'oneOf':[]}, {'type':'string','pattern':'['}):
            with self.subTest(schema=s), self.assertRaises(Invalid): check_schema(s)

    def test_duplicate_keys_and_non_json_numbers_reject(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'bad.json'
            for raw in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
                path.write_text(raw)
                with self.assertRaises(Invalid): load(path)

    def test_oneof_requires_exactly_one_match(self):
        with self.assertRaises(Invalid): validate('a',{'oneOf':[{'type':'string'},{'type':'string'}]})


class SemanticsTests(unittest.TestCase):
    def test_signature_is_real_and_body_tampering_fails(self):
        artifact=copy.deepcopy(FIXTURES['RSI-001']['mutation']['components']['artifact'])
        self.assertTrue(signature_valid(artifact))
        artifact['body']['payload']='tampered'
        self.assertFalse(signature_valid(artifact))

    def test_broken_local_validity_is_invalid_fixture(self):
        f=copy.deepcopy(FIXTURES['RSI-001'])
        f['mutation']['components']['artifact']['signature']='00'*64
        self.assertEqual(run_fixture(f)['status'],'INVALID_FIXTURE')

    def test_unchanged_mutation_is_invalid_fixture(self):
        f=copy.deepcopy(FIXTURES['RSI-006'])
        f['mutation']['components']=copy.deepcopy(f['control']['components'])
        self.assertEqual(run_fixture(f)['status'],'INVALID_FIXTURE')

    def test_extra_relation_change_is_invalid(self):
        f=copy.deepcopy(FIXTURES['RSI-001'])
        body=dict(f['mutation']['components']['artifact']['body'],context='other')
        f['mutation']['components']['artifact']=signed('attacker',body)
        self.assertEqual(run_fixture(f)['status'],'INVALID_FIXTURE')

    def test_valid_mutant_relation_is_invalid_fixture(self):
        f=copy.deepcopy(FIXTURES['RSI-001'])
        f['mutation']['components']['artifact']=signed('attacker',dict(f['control']['components']['artifact']['body'],subject='attacker'))
        f['mutation']['changed_fields'].append('artifact.body.subject')
        self.assertEqual(run_fixture(f)['status'],'INVALID_FIXTURE')

    def test_initial_state_digest_is_checked(self):
        f=copy.deepcopy(FIXTURES['RSI-003'])
        f['initial_state_digest']='0'*64
        self.assertEqual(run_fixture(f)['status'],'INVALID_FIXTURE')

    def test_unknown_evaluator_is_unsupported(self):
        f=copy.deepcopy(FIXTURES['RSI-001'])
        f['evaluator']['name']='unimplemented'
        validate(f,schema())
        self.assertEqual(run_fixture(f)['status'],'UNSUPPORTED')

    def test_status_evidence_binds_every_coordinate(self):
        for field in ('subject','scope','operation'):
            c=copy.deepcopy(FIXTURES['RSI-008']['control']['components'])
            for e in c['evidence']: e[field]='unrelated'
            with self.subTest(field=field):
                self.assertEqual(status_evidence(c)['outcome'],'REJECT')
        c=copy.deepcopy(FIXTURES['RSI-008']['control']['components'])
        c['evidence'][0]['success']=False
        self.assertEqual(status_evidence(c)['status'],'confirmed')

    def test_atomic_both_commit_orders_checked(self):
        r=run_fixture(FIXTURES['RSI-004'])
        a=r['observations']['mutation']['observed']['consumed']
        b=r['observations']['reverse_schedule']['consumed']
        self.assertEqual(a,[{'consumer':'worker-a','position':7}])
        self.assertEqual(b,[{'consumer':'worker-b','position':7}])

    def test_three_levels_are_separate(self):
        for f in FIXTURES.values():
            r=run_fixture(f)
            for phase,expected in (('control',True),('mutation',False)):
                o=r['observations'][phase]
                self.assertTrue(all(o['component_validity'].values()))
                self.assertIs(o['relation_validity'],expected)
                self.assertIs(o['claim_validity'],expected)


class MutationTests(unittest.TestCase):
    def test_missing_anchor_not_applied(self):
        r=prove(FIXTURES['RSI-001'],('missing anchor','True'))
        self.assertEqual(r['status'],'NOT_APPLIED')

    def test_identical_source_not_applied(self):
        before=PATCHES['signer_subject'][0]
        self.assertEqual(prove(FIXTURES['RSI-001'],(before,before))['status'],'NOT_APPLIED')

    def test_syntax_error_not_killed(self):
        before=PATCHES['signer_subject'][0]
        self.assertEqual(prove(FIXTURES['RSI-001'],(before,'authorized = ('))['status'],'NOT_APPLIED')

    def test_import_failure_not_killed(self):
        before=PATCHES['signer_subject'][0]
        self.assertEqual(prove(FIXTURES['RSI-001'],(before,'import rsi_missing_dependency_123'))['status'],'NOT_APPLIED')

    def test_crash_before_decision_not_killed(self):
        before=PATCHES['signer_subject'][0]
        r=prove(FIXTURES['RSI-001'],(before,'authorized = 1 / 0'))
        self.assertEqual(r['status'],'NOT_APPLIED')
        self.assertTrue(r['mutated']['execution_error'])

    def test_semantically_unchanged_patch_survives(self):
        before=PATCHES['signer_subject'][0]
        self.assertEqual(prove(FIXTURES['RSI-001'],(before,before+' and True'))['status'],'SURVIVED')

    def test_bad_baseline_vacuous(self):
        f=copy.deepcopy(FIXTURES['RSI-006'])
        f['mutation']['components']['context']='room-a'
        self.assertEqual(prove(f)['status'],'VACUOUS')

    def test_nonexecuted_or_unmapped_failure_vacuous(self):
        baseline={'status':'PASS'}
        for checks in ([],[{'phase':'mutation','id':'mapped','executed':False,'passed':False}],
                       [{'phase':'control','id':'control','executed':True,'passed':True},{'phase':'mutation','id':'other','executed':True,'passed':False}]):
            self.assertEqual(classify(baseline,{'status':'FAIL','checks':checks},'mapped'),'VACUOUS')

    def test_control_regression_is_not_a_kill(self):
        before=PATCHES['signer_subject'][0]
        self.assertEqual(prove(FIXTURES['RSI-001'],(before,'authorized = False'))['status'],'VACUOUS')


class ReportTests(unittest.TestCase):
    def test_all_result_states_serialized_independently(self):
        for states in (STATES,MUTATION_STATES):
            empty=json.loads(json.dumps(totals([],states)))
            self.assertEqual(empty,{s:0 for s in states})
            mixed=totals([{'status':s} for s in states]+[{'status':states[0]}],states)
            self.assertEqual(mixed,{s:2 if s==states[0] else 1 for s in states})

    def test_empty_suite_fails(self):
        self.assertEqual(collect([])['totals']['INVALID_FIXTURE'],1)

    def test_duplicate_fixture_ids_reject(self):
        p=sorted((ROOT/'fixtures').glob('*.json'))[0]
        self.assertEqual(collect([p,p])['totals'],{'PASS':0,'FAIL':0,'INVALID_FIXTURE':2,'UNSUPPORTED':0})

    def test_bad_schema_returns_structured_failure(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'schema.json'
            p.write_text('{"$ref":"https://not-fetched.invalid/schema"}')
            r=collect(list((ROOT/'fixtures').glob('*.json')),schema_path=p)
            self.assertEqual(r['totals']['INVALID_FIXTURE'],1)

    def test_cli_invalid_fixture_nonzero_and_json(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'bad.json'
            p.write_text('{}')
            r=subprocess.run([sys.executable,'-m','runner.validate_fixtures',str(p)],cwd=ROOT,capture_output=True,text=True)
            self.assertNotEqual(r.returncode,0)
            self.assertEqual(json.loads(r.stdout)['totals']['INVALID_FIXTURE'],1)

    def test_cli_unsupported_nonzero(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'unknown.json'
            f=copy.deepcopy(FIXTURES['RSI-001'])
            f['evaluator']['version']='future'
            p.write_text(json.dumps(f))
            r=subprocess.run([sys.executable,'-m','runner.validate_fixtures',str(p)],cwd=ROOT,capture_output=True,text=True)
            self.assertNotEqual(r.returncode,0)
            self.assertEqual(json.loads(r.stdout)['totals']['UNSUPPORTED'],1)

    def test_reports_deterministic(self):
        paths=sorted((ROOT/'fixtures').glob('*.json'))
        self.assertEqual(collect(paths),collect(paths))
        self.assertEqual(prove(FIXTURES['RSI-004']),prove(FIXTURES['RSI-004']))


# Separate named test cases make the six-fixture coverage visible in test totals.
for ident, fixture in FIXTURES.items():
    def positive(self, f=fixture):
        validate(f,schema())
        self.assertEqual(run_fixture(f)['status'],'PASS')
    def kills(self, f=fixture):
        r=prove(f)
        self.assertEqual(r['status'],'KILLED',r)
        self.assertNotEqual(r['source_sha256'],r['mutant_sha256'])
        mapped=[c for c in r['mutated']['checks'] if c['id']==CHECKS[f['protected_relation']] and c['phase']=='mutation']
        self.assertTrue(mapped)
        self.assertTrue(all(c['executed'] and not c['passed'] for c in mapped))
        self.assertFalse(r['mutated'].get('execution_error',False))
    setattr(SchemaTests,'test_fixture_'+ident.replace('-','_'),positive)
    setattr(MutationTests,'test_kill_'+ident.replace('-','_'),kills)

if __name__=='__main__': unittest.main()
