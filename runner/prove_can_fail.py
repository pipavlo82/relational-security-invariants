"""Mechanically replace one enforcing assignment in an isolated source copy."""
import argparse
import hashlib
import inspect
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from runner.engine import CHECKS, MODELS, run_fixture, totals
from runner.schema_subset import load, validate
from runner.validate_fixtures import schema

STATES = ('KILLED','SURVIVED','VACUOUS','NOT_APPLIED')
PATCHES = {
    'signer_subject': ('authorized = artifact["signer"] == artifact["body"]["subject"]', 'authorized = True'),
    'auth_before_commit': ('may_commit = authenticated', 'may_commit = True'),
    'atomic_consumption': ('available = observed == revision', 'available = True'),
    'context_binding': ('bound = c["artifact"]["body"]["context"] == c["context"]', 'bound = True'),
    'status_evidence': ('justified = bool(matching)', 'justified = True'),
    'ingestion_equivalence': ('authorized = c["artifact"]["body"]["role"] == "member"', 'authorized = c["artifact"]["body"]["role"] == "member" or path != "live"'),
}


def classify(baseline, mutated, check_id, applied=True):
    if not applied:
        return 'NOT_APPLIED'
    if baseline['status'] != 'PASS':
        return 'VACUOUS'
    if mutated.get('execution_error'):
        return 'NOT_APPLIED'
    control = [x for x in mutated.get('checks',[]) if x['phase'] == 'control']
    mapped = [x for x in mutated.get('checks',[]) if x['phase'] == 'mutation' and x['id'] == check_id and x['executed']]
    if not control or not all(x['executed'] and x['passed'] for x in control) or not mapped:
        return 'VACUOUS'
    return 'KILLED' if mutated['status'] == 'FAIL' and any(not x['passed'] for x in mapped) else 'SURVIVED'


def prove(f, patch=None):
    result = {'id':f.get('id','unknown'), 'status':'NOT_APPLIED'}
    try:
        validate(f, schema())
        kind = f['protected_relation']
        baseline = run_fixture(f)
        result['baseline'] = baseline
        if baseline['status'] != 'PASS':
            result['status'] = 'VACUOUS'
            return result
        function = MODELS[kind]
        source = inspect.getsource(function)
        before, after = patch if patch is not None else PATCHES[kind]
        if before == after or source.count(before) != 1:
            result['reason'] = 'mutation anchor absent, ambiguous, or unchanged'
            return result
        mutated_source = source.replace(before, after, 1)
        namespace = dict(function.__globals__)
        exec(compile(mutated_source, '<rsi-mutant:' + kind + '>', 'exec'), namespace)
        mutated = run_fixture(f, adapter=namespace[function.__name__])
        result.update({'check_id':CHECKS[kind], 'source_sha256':hashlib.sha256(source.encode()).hexdigest(),
                       'mutant_sha256':hashlib.sha256(mutated_source.encode()).hexdigest(),
                       'replacement':{'before':before,'after':after}, 'mutated':mutated,
                       'status':classify(baseline, mutated, CHECKS[kind])})
    except Exception as exc:
        result['error'] = type(exc).__name__ + ': ' + str(exc)
    return result


def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('files',nargs='*',type=Path)
    args = parser.parse_args(argv)
    paths = args.files or sorted((ROOT/'fixtures').glob('*.json'))
    results = []
    for path in paths:
        try:
            results.append(prove(load(path)))
        except Exception as exc:
            results.append({'id':path.name,'status':'NOT_APPLIED','error':str(exc)})
    ids = [r['id'] for r in results]
    for r in results:
        if ids.count(r['id']) != 1:
            r.update(status='NOT_APPLIED', error='duplicate fixture id')
    if not paths:
        results.append({'id':'suite','status':'NOT_APPLIED','error':'no fixtures selected'})
    print(json.dumps({'results':results,'totals':totals(results,STATES)},indent=2,sort_keys=True))
    return 0 if all(r['status']=='KILLED' for r in results) else 1


if __name__ == '__main__':
    sys.exit(main())
