"""H2 comparison harness. This is NOT the clean-room semantic implementation."""
from copy import deepcopy
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
DIRECTORY = Path('reproducers/crystal-receipt-cleanroom')


def compact(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True).encode('ascii')


def vectors(root=ROOT):
    root = Path(root)
    data = json.loads((root / DIRECTORY / 'golden-vectors.v0.json').read_bytes())['vectors']
    for vector in data:
        raw = (root / DIRECTORY / vector['input_path']).read_bytes()
        if hashlib.sha256(raw).hexdigest() != vector['input_sha256'] or json.loads(raw) != vector['input']:
            raise ValueError('H2 input drift')
        unsigned = {k: v for k, v in vector.items() if k != 'vector_sha256'}
        if hashlib.sha256(compact(unsigned)).hexdigest() != vector['vector_sha256']:
            raise ValueError('H2 golden vector drift')
    return data


def third_leg(raw, root=ROOT, definition=None):
    """Only raw input and a definition file cross the subprocess boundary."""
    node = shutil.which('node')
    if node is None:
        raise RuntimeError('Node runtime required')
    command = [node, str(Path(root) / DIRECTORY / 'reproduce.mjs')]
    if definition is not None:
        command += ['--definition', str(definition)]
    result = subprocess.run(command, input=raw, capture_output=True, timeout=20)
    if result.returncode:
        raise ValueError(result.stderr.decode('utf-8', 'replace'))
    return json.loads(result.stdout)


def projection(observation):
    return {key: observation['outputs'][key] for key in
            ('canonical_baseline', 'canonical_candidate', 'semantic_identity_preserved')}


def compare(root=ROOT):
    root = Path(root)
    goldens = vectors(root)
    # Finish EVERY third-leg computation before importing/calling A or B,
    # admitting D, or comparing any manually derived golden answer.
    third = {v['id']: third_leg((root / DIRECTORY / v['input_path']).read_bytes(), root) for v in goldens}

    from adapters.crystal_receipt.model import evaluate
    from profiles.crystal_receipt.expectation import make_profile, predict
    from runner.expectation_contract import load_fixtures, admit

    profile = make_profile(root)
    documents = load_fixtures(root, profile)
    admitted = admit(root, profile, documents)
    fixtures = {d.fixture_id: d.value() for d in documents}
    predicted = {ident: predict(fixture) for ident, fixture in fixtures.items()}
    matrix = []
    for vector in goldens:
        ident, case_id = vector['existing_admitted_row'].split('/')
        original = next(c['inputs'] for c in fixtures[ident]['cases'] if c['case_id'] == case_id)
        if original != vector['input']:
            raise ValueError('H2 input does not match its exact frozen admitted case')
        key = vector['existing_admitted_row']
        actual = projection(evaluate(root, {'inputs': deepcopy(vector['input'])}))
        predictor = projection(predicted[ident][key]['observation'])
        frozen = projection(admitted.for_fixture(ident)[key]['observation'])
        clean = third[vector['id']]
        same = actual == predictor == clean == frozen == vector['definition_expected']
        matrix.append({'vector': vector['id'], 'actual': actual, 'predictor': predictor,
                       'third_leg': clean, 'frozen_expectation': frozen,
                       'definition_golden': vector['definition_expected'], 'all_equal': same,
                       'status': 'THIRD_LEG_AGREES' if same else 'THIRD_LEG_DISAGREES',
                       'semantic_notes': vector['derivation'], 'admitted_row': key,
                       'input_sha256': vector['input_sha256']})

    experiments = []
    for experiment, index in [('H2-M1', 2), ('H2-M1', 3), ('H2-M2', 1)]:
        vector = goldens[index]
        # Local input-projection doubles only; production sources stay frozen.
        # Both doubles intentionally encode the SAME incorrect assumption via
        # their separate actual and prediction paths. C keeps the original input.
        a_input = deepcopy(vector['input'])
        if experiment == 'H2-M1':
            for endpoint in a_input.values():
                endpoint['semantic_artifact']['_h2_external_manifest'] = compact(endpoint['manifest']).decode('ascii')
        else:
            a_input['candidate']['semantic_artifact'] = deepcopy(a_input['baseline']['semantic_artifact'])
        actual_double = projection(evaluate(root, {'inputs': a_input}))

        b_input = {}
        for name in ('baseline', 'candidate'):
            original = vector['input'][name]
            semantic = dict(original['semantic_artifact'])
            if experiment == 'H2-M1':
                semantic['_h2_external_manifest'] = json.dumps(original['manifest'], sort_keys=True, separators=(',', ':'))
            elif name == 'candidate':
                semantic = dict(vector['input']['baseline']['semantic_artifact'])
            b_input[name] = {'semantic_artifact': semantic, 'manifest': dict(original['manifest'])}
        fixture = deepcopy(next(iter(fixtures.values())))
        fixture['id'] = 'h2-double'
        fixture['cases'] = [{'case_id': 'input-projection', 'inputs': b_input}]
        predictor_double = projection(next(iter(predict(fixture).values()))['observation'])
        clean = third[vector['id']]
        caught = (actual_double == predictor_double and clean != actual_double and
                  clean['semantic_identity_preserved'] != actual_double['semantic_identity_preserved'])
        experiments.append({'experiment': experiment, 'vector': vector['id'],
                            'actual_double': actual_double, 'predictor_double': predictor_double,
                            'third_leg_unchanged': clean, 'pair_agrees': actual_double == predictor_double,
                            'status': 'COMMON_MODE_CAUGHT' if caught else 'INDEPENDENCE_NOT_ESTABLISHED'})
    return {'schema': 'crystal-cleanroom-comparison.v0', 'matrix': matrix, 'experiments': experiments,
            'third_leg_computed_before_comparison': True, 'global_mutation_taxonomy_changed': False}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT / 'artifacts/crystal-cleanroom.json')
    args = parser.parse_args()
    result = compare()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(compact(result) + b'\n')
    print(json.dumps({'vectors': len(result['matrix']), 'all_equal': all(r['all_equal'] for r in result['matrix']),
                      'experiments': [r['status'] for r in result['experiments']]}))
    return int(not all(r['all_equal'] for r in result['matrix']) or
               not all(r['status'] == 'COMMON_MODE_CAUGHT' for r in result['experiments']))


if __name__ == '__main__':
    sys.path.insert(0, str(ROOT))
    raise SystemExit(main())
