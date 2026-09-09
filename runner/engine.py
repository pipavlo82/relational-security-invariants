"""Independent fixture preconditions and observed-output conformance checks."""
from copy import deepcopy
from adapters.generic.artifacts import authenticates, digest, signature_valid
from adapters.generic import models as generic
from adapters.messaging import models as messaging
from runner.schema_subset import Invalid

STATES = ('PASS', 'FAIL', 'INVALID_FIXTURE', 'UNSUPPORTED')
MODELS = {
    'signer_subject': generic.signer_subject,
    'auth_before_commit': messaging.auth_before_commit,
    'atomic_consumption': messaging.atomic_consumption,
    'context_binding': generic.context_binding,
    'status_evidence': generic.status_evidence,
    'ingestion_equivalence': generic.ingestion_equivalence,
}
CHECKS = {
    'signer_subject': 'unauthorized_subject_rejected',
    'auth_before_commit': 'unauthenticated_state_unchanged',
    'atomic_consumption': 'one_position_one_consumer',
    'context_binding': 'foreign_context_rejected',
    'status_evidence': 'unjustified_status_rejected',
    'ingestion_equivalence': 'all_equivalent_paths_reject',
}


def totals(results, states=STATES):
    counts = {s: 0 for s in states}
    for result in results:
        counts[result['status']] += 1
    return counts


def differences(a, b, prefix=''):
    if type(a) is dict and type(b) is dict and set(a) == set(b):
        out = []
        for k in sorted(a):
            out.extend(differences(a[k], b[k], prefix + '.' + k if prefix else k))
        return out
    return [] if a == b else [prefix]


def local_checks(kind, c):
    if kind in ('signer_subject', 'context_binding', 'ingestion_equivalence'):
        return {'structure': True, 'signature': signature_valid(c['artifact'])}
    if kind == 'auth_before_commit':
        return {'ciphertext_structure': len(bytes.fromhex(c['ciphertext'])) >= 17, 'state_structure': True}
    if kind == 'atomic_consumption':
        return {'operation_structure': len({o['consumer'] for o in c['operations']}) == len(c['operations']),
                'position_structure': all(o['position'] == c['revision'] for o in c['operations'])}
    return {'request_structure': True, 'evidence_structure': True}


def relation(kind, c):
    # Relation oracle is independent of adapter decisions and never mutated.
    if kind == 'signer_subject':
        return c['artifact']['body']['subject'] == c['artifact']['signer']
    if kind == 'auth_before_commit':
        return authenticates(c['ciphertext'])
    if kind == 'atomic_consumption':
        positions = [o['position'] for o in c['operations']]
        return len(positions) == len(set(positions))
    if kind == 'context_binding':
        return c['context'] == c['artifact']['body']['context']
    if kind == 'status_evidence':
        return any(e['success'] and (e['subject'], e['scope'], e['operation']) ==
                   (c['request']['subject'], c['request']['scope'], c['request']['operation']) for e in c['evidence'])
    return c['artifact']['body']['role'] == 'member'


def preconditions(f):
    kind = f['protected_relation']
    a, b = (f[p]['components'] for p in ('control', 'mutation'))
    if sorted(differences(a, b)) != sorted(f['mutation']['changed_fields']):
        raise Invalid('changed_fields does not exactly describe the input differences')
    for phase in ('control', 'mutation'):
        c = f[phase]['components']
        checks = local_checks(kind, c)
        declared = f[phase]['local_validity' if phase == 'control' else 'preserve_local_validity']
        if set(checks) != set(declared) or not all(checks.values()):
            raise Invalid(phase + ': declared local validity not preserved')
        if relation(kind, c) is not f[phase]['relation_expected']:
            raise Invalid(phase + ': relation oracle contradicts fixture')
    if kind == 'signer_subject' and not (a['artifact']['signer'] == 'victim' and b['artifact']['signer'] == 'attacker' and a['artifact']['body']['subject'] == 'victim'):
        raise Invalid('signer fixture must model attacker signing a victim-shaped object')
    if kind == 'atomic_consumption':
        if len(a['operations']) != 1 or len(b['operations']) != 2 or a['operations'][0] != b['operations'][0]:
            raise Invalid('atomic fixture requires one control and two competing consumers')
    if kind == 'status_evidence':
        if len(a['evidence']) != 2 or {e['kind'] for e in a['evidence']} != {'recipient_ack','durable_publication'}:
            raise Invalid('status fixture requires both evidence channels')
        if b['evidence'] != [dict(e, success=False) for e in a['evidence']] or not all(e['success'] for e in a['evidence']):
            raise Invalid('status fixture must fail every evidence channel and preserve bindings')
    if 'initial_state_digest' in f:
        initial = a['state'] if kind == 'auth_before_commit' else {'revision': a['revision']} if kind == 'atomic_consumption' else {}
        if f['initial_state_digest'] != digest(initial):
            raise Invalid('initial state digest does not bind the actual initial state')


def check(ident, phase, passed):
    return {'id': ident, 'phase': phase, 'executed': True, 'passed': bool(passed)}


def judge(kind, phase, c, out):
    checks = [check('expected_outcome', phase, out['outcome'] == ('ACCEPT' if phase == 'control' else 'REJECT'))]
    if phase == 'control':
        if kind == 'auth_before_commit':
            checks.append(check('control_commits_authenticated_state', phase, out['state_commit'] and out['tentative_created'] and out['final_state_digest'] == digest({'revision':c['state']['revision']+1, 'session':'bootstrapped'})))
        elif kind == 'atomic_consumption':
            checks.append(check('control_consumes_once', phase, out['decisions'] == ['ACCEPT'] and out['consumed'] == c['operations'] and out['final_revision'] == c['revision']+1))
        elif kind == 'status_evidence':
            checks.append(check('control_confirms', phase, out['status'] == 'confirmed' and out['status_promotion']))
        elif kind == 'ingestion_equivalence':
            checks.append(check('control_all_paths_accept', phase, out['paths'] == {p:'ACCEPT' for p in c['paths']} and out['policy_promotion']))
        else:
            flag = 'authority_promotion' if kind == 'signer_subject' else 'provenance_promotion'
            checks.append(check('control_promotes', phase, out[flag]))
        return checks
    if kind == 'signer_subject':
        safe = out['outcome'] == 'REJECT' and out['authority_promotion'] is False
    elif kind == 'auth_before_commit':
        safe = out['outcome'] == 'REJECT' and out['state_commit'] is False and out['final_state_digest'] == digest(c['state']) and out['tentative_created'] is True
    elif kind == 'atomic_consumption':
        consumed = out['consumed']
        safe = (len(consumed) <= 1 and len(out['decisions']) == 2 and out['decisions'].count('ACCEPT') == len(consumed)
                and out['decisions'].count('REJECT') >= 1 and all(item in c['operations'] for item in consumed)
                and out['final_revision'] == c['revision'] + len(consumed))
    elif kind == 'context_binding':
        safe = out['outcome'] == 'REJECT' and out['provenance_promotion'] is False
    elif kind == 'status_evidence':
        safe = out['outcome'] == 'REJECT' and out['status'] == 'failed' and out['status_promotion'] is False
    else:
        safe = out['paths'] == {p:'REJECT' for p in c['paths']} and out['policy_promotion'] is False
    checks.append(check(CHECKS[kind], phase, safe))
    return checks


def run_fixture(f, adapter=None):
    kind = f['protected_relation']
    try:
        preconditions(f)
    except (Invalid, KeyError, TypeError, ValueError) as exc:
        return {'id': f['id'], 'status': 'INVALID_FIXTURE', 'error': str(exc), 'checks': []}
    if f['evaluator'] != {'name':'reference','version':'0'}:
        return {'id': f['id'], 'status':'UNSUPPORTED', 'error':'evaluator not implemented', 'checks':[]}
    adapter = adapter or MODELS[kind]
    result = {'id':f['id'], 'status':'FAIL', 'policy_version':f['policy_version'], 'evaluator':f['evaluator'], 'checks':[], 'fixture_digest':digest(f), 'observations':{}}
    try:
        for phase in ('control', 'mutation'):
            c = f[phase]['components']
            out = adapter(deepcopy(c))
            result['observations'][phase] = {'component_validity':local_checks(kind,c), 'relation_validity':relation(kind,c),
                                           'claim_validity':all(local_checks(kind,c).values()) and relation(kind,c), 'observed':out}
            result['checks'].extend(judge(kind, phase, c, out))
        if kind == 'atomic_consumption':
            c = deepcopy(f['mutation']['components'])
            c['operations'].reverse()
            out = adapter(c)
            result['observations']['reverse_schedule'] = out
            result['checks'].extend(judge(kind, 'mutation', c, out))
        result['status'] = 'PASS' if all(x['passed'] for x in result['checks']) else 'FAIL'
    except Exception as exc:
        # Adapter/setup/output-contract exceptions are failures, never mutation kills.
        result['error'] = type(exc).__name__ + ': ' + str(exc)
        result['execution_error'] = True
    return result
