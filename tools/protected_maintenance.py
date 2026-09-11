"""Exact post-v0 documentation/checker transitions; never a semantic allowlist.

Frozen baseline manifests are not rewritten. Any third digest still fails.
This helper belongs to maintenance checks, not conformance or expectation logic.
"""
import hashlib
import json

MANIFEST = 'research/post-v0-readme-maintenance-v1.json'
ALLOWED = frozenset({
    'README.md',
    'tests/test_rvr.py', 'tests/test_tsei.py', 'tests/test_pq.py',
    'tools/check_rvr_digest_binding.py', 'tools/check_tsei_serializer_adoption.py',
    'tools/check_pq_policy_asof.py',
    'tests/test_capv.py', 'tests/test_aggregate.py', 'tests/test_judgment.py',
    'tools/check_tas_context_invocation.py', 'tools/check_consult_escrow.py',
    'tools/check_verify_layer.py',
})


def _changes(root):
    data = json.loads((root / MANIFEST).read_bytes())
    if (data['schema'] != 'rsi-protected-maintenance.v1'
            or data['base_commit'] != '8d8e31291ecf96284212a353efb66f606cff2953'
            or set(data['changes']) != ALLOWED):
        raise ValueError('INVALID_MAINTENANCE_MANIFEST')
    for item in data['changes'].values():
        if set(item) != {'before_sha256', 'after_sha256'}:
            raise ValueError('INVALID_MAINTENANCE_ENTRY')
        for digest in item.values():
            if (not isinstance(digest, str) or len(digest) != 64
                    or any(c not in '0123456789abcdef' for c in digest)):
                raise ValueError('INVALID_MAINTENANCE_DIGEST')
    return data['changes']


def _audit(root, pins):
    changes = _changes(root)
    rejected, accepted = [], []
    for name, expected in pins.items():
        path = root / name
        actual = hashlib.sha256(path.read_bytes()).hexdigest() if path.is_file() else None
        if actual == expected:
            continue
        record = changes.get(name)
        if (record is not None and expected == record['before_sha256']
                and actual == record['after_sha256']):
            accepted.append(name)
        else:
            rejected.append(name)
    return rejected, accepted


def mismatches(root, pins):
    return _audit(root, pins)[0]


def approved_changes(root, pins):
    return _audit(root, pins)[1]
