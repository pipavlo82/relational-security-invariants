"""Usage: python -m runner.validate_fixtures [--schema-only] [files ...]."""
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from runner.schema_subset import Invalid, check_schema, load, validate
from runner.engine import preconditions, run_fixture, totals


def schema():
    s = load(ROOT / 'schema/relation-binding-fixture.v0.schema.json')
    check_schema(s)
    return s


def collect(paths, schema_only=False, schema_path=None):
    results = []
    try:
        s = load(schema_path) if schema_path else schema()
        check_schema(s)
    except Exception as exc:
        return {'mode':'schema' if schema_only else 'conformance','results':[{'id':'schema','status':'INVALID_FIXTURE','error':str(exc)}],
                'totals':{'PASS':0,'FAIL':0,'INVALID_FIXTURE':1,'UNSUPPORTED':0}}
    loaded = []
    for path in paths:
        try:
            f = load(path)
            validate(f, s)
            preconditions(f)
            loaded.append((path, f))
        except Exception as exc:
            results.append({'id':path.name,'status':'INVALID_FIXTURE','error':str(exc)})
    ids = [f['id'] for _, f in loaded]
    for path, f in loaded:
        if ids.count(f['id']) != 1:
            results.append({'id':f['id'],'status':'INVALID_FIXTURE','error':'duplicate fixture id'})
        elif schema_only:
            results.append({'id':f['id'],'status':'PASS'})
        else:
            results.append(run_fixture(f))
    if not paths:
        results.append({'id':'suite','status':'INVALID_FIXTURE','error':'no fixtures selected'})
    return {'mode':'schema' if schema_only else 'conformance','results':results,'totals':totals(results)}


def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument('--schema-only', action='store_true')
    p.add_argument('--schema', type=Path)
    p.add_argument('files', nargs='*', type=Path)
    args = p.parse_args(argv)
    report = collect(args.files or sorted((ROOT/'fixtures').glob('*.json')), args.schema_only, args.schema)
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0 if all(r['status'] == 'PASS' for r in report['results']) else 1


if __name__ == '__main__':
    sys.exit(main())
