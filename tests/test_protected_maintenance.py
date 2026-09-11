"""Maintenance accepts only recorded byte transitions, never arbitrary drift."""
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from tools.protected_maintenance import MANIFEST, mismatches, approved_changes

ROOT = Path(__file__).resolve().parents[1]


class MaintenanceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / MANIFEST).parent.mkdir(parents=True)
        (self.root / MANIFEST).write_bytes((ROOT / MANIFEST).read_bytes())
        self.data = json.loads((ROOT / MANIFEST).read_bytes())

    def test_exact_document_transition(self):
        (self.root / 'README.md').write_bytes((ROOT / 'README.md').read_bytes())
        pins = {'README.md': self.data['changes']['README.md']['before_sha256']}
        self.assertEqual(mismatches(self.root, pins), [])
        self.assertEqual(approved_changes(self.root, pins), ['README.md'])

    def test_third_document_digest_rejected(self):
        (self.root / 'README.md').write_bytes(b'unreviewed documentation')
        pins = {'README.md': self.data['changes']['README.md']['before_sha256']}
        self.assertEqual(mismatches(self.root, pins), ['README.md'])

    def test_wrong_historical_digest_rejected(self):
        (self.root / 'README.md').write_bytes((ROOT / 'README.md').read_bytes())
        self.assertEqual(mismatches(self.root, {'README.md': '0' * 64}), ['README.md'])

    def test_unrelated_semantic_drift_rejected(self):
        (self.root / 'rsi').mkdir()
        (self.root / 'rsi/codec.py').write_bytes(b'changed semantic code')
        self.assertEqual(mismatches(self.root, {'rsi/codec.py': '0' * 64}), ['rsi/codec.py'])

    def test_manifest_cannot_expand_into_core(self):
        self.data['changes']['rsi/codec.py'] = self.data['changes']['README.md']
        (self.root / MANIFEST).write_text(json.dumps(self.data))
        with self.assertRaisesRegex(ValueError, 'INVALID_MAINTENANCE_MANIFEST'):
            mismatches(self.root, {})

    def test_recorded_new_files_exact(self):
        for name, entry in self.data['changes'].items():
            self.assertEqual(hashlib.sha256((ROOT / name).read_bytes()).hexdigest(),
                             entry['after_sha256'], name)

    def test_unchanged_and_missing_file(self):
        (self.root / 'example').write_bytes(b'unchanged')
        pins = {'example': hashlib.sha256(b'unchanged').hexdigest()}
        self.assertEqual(mismatches(self.root, pins), [])
        self.assertEqual(approved_changes(self.root, pins), [])
        (self.root / 'example').unlink()
        self.assertEqual(mismatches(self.root, pins), ['example'])
