"""H2 evidence checks, separate from the global conformance/mutation taxonomy."""
from copy import deepcopy
from dataclasses import replace
import json
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from unittest.mock import patch

from tools.check_crystal_cleanroom import ROOT, DIRECTORY, compact, vectors, third_leg, compare


class CrystalCleanroomTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.goldens = vectors()
        cls.report = compare()

    def test_control(self):
        self.assertTrue(self.report['matrix'][0]['all_equal'])

    def test_semantic_substitution(self):
        row = self.report['matrix'][1]
        self.assertTrue(row['all_equal'])
        self.assertFalse(row['third_leg']['semantic_identity_preserved'])

    def test_timestamp_changed(self):
        row = self.report['matrix'][2]
        self.assertTrue(row['all_equal'])
        self.assertTrue(row['third_leg']['semantic_identity_preserved'])

    def test_timestamp_removed(self):
        self.assertTrue(self.report['matrix'][3]['all_equal'])

    def test_h2_m1_common_mode_caught(self):
        rows = [r for r in self.report['experiments'] if r['experiment'] == 'H2-M1']
        self.assertEqual(len(rows), 2)
        for row in rows:
            self.assertEqual(row['actual_double'], row['predictor_double'])
            self.assertEqual(row['status'], 'COMMON_MODE_CAUGHT')
            self.assertNotEqual(row['actual_double']['semantic_identity_preserved'],
                                row['third_leg_unchanged']['semantic_identity_preserved'])

    def test_h2_m2_common_mode_caught(self):
        row = next(r for r in self.report['experiments'] if r['experiment'] == 'H2-M2')
        self.assertEqual(row['status'], 'COMMON_MODE_CAUGHT')
        self.assertTrue(row['actual_double']['semantic_identity_preserved'])
        self.assertFalse(row['third_leg_unchanged']['semantic_identity_preserved'])

    def test_source_pin_drift(self):
        with tempfile.TemporaryDirectory() as temp:
            definition = Path(temp) / 'SPEC.md'
            definition.write_bytes((ROOT / 'evidence/crystal-receipt/SPEC.md').read_bytes() + b'\n')
            with self.assertRaisesRegex(ValueError, 'DEFINITION_PIN_DRIFT'):
                third_leg(compact(self.goldens[0]['input']), definition=definition)

    def test_static_dependency_separation(self):
        code = (ROOT / DIRECTORY / 'reproduce.mjs').read_text(encoding='utf-8')
        imports = re.findall(r"from\s+['\"]([^'\"]+)['\"]", code)
        self.assertEqual(imports, ['node:fs', 'node:crypto'])
        for forbidden in ('adapters.', 'adapters/', 'profiles.crystal_receipt',
                          'profiles/crystal_receipt', 'expectations.v0.json',
                          'counterfactual-audit-boundary.ts', 'canonicalize.ts',
                          'rsi.codec', 'golden-vectors', 'CR-RSI-', 'CR-H2-', 'import('):
            self.assertNotIn(forbidden, code)

    def test_standalone_without_other_legs_or_rows(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / DIRECTORY).mkdir(parents=True)
            shutil.copy2(ROOT / DIRECTORY / 'reproduce.mjs', root / DIRECTORY / 'reproduce.mjs')
            definition = root / 'definition.md'
            shutil.copy2(ROOT / 'evidence/crystal-receipt/SPEC.md', definition)
            for vector in self.goldens:
                self.assertEqual(third_leg(compact(vector['input']), root, definition),
                                 vector['definition_expected'])

    def test_goldens_and_report_deterministic(self):
        self.assertEqual(vectors(), self.goldens)
        self.assertEqual(compact(compare()), compact(self.report))

    def test_golden_digest_tamper(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            shutil.copytree(ROOT / DIRECTORY, root / DIRECTORY)
            path = root / DIRECTORY / 'golden-vectors.v0.json'
            value = json.loads(path.read_bytes())
            value['vectors'][0]['definition_expected']['semantic_identity_preserved'] = False
            path.write_bytes(compact(value))
            with self.assertRaisesRegex(ValueError, 'golden vector drift'):
                vectors(root)

    def test_no_unsafe_or_silent_transport_coercion(self):
        good = deepcopy(self.goldens[0]['input'])
        malformed = []
        for value in (1.5, 9007199254740993, '\u00e9', {'nested': 'value'}, True, None, []):
            candidate = deepcopy(good)
            candidate['candidate']['semantic_artifact']['unsupported'] = value
            malformed.append(compact(candidate))
        candidate = deepcopy(good)
        candidate['candidate']['semantic_artifact']['audit_timestamp'] = 'reserved'
        malformed.append(compact(candidate))
        malformed += [b'{"baseline":{},"baseline":{},"candidate":{}}',
                      b'{"baseline":{},"candidate":{},"expected":"true"}',
                      compact(good) + b' garbage']
        for raw in malformed:
            with self.subTest(raw=raw):
                with self.assertRaises(ValueError):
                    third_leg(raw)

    def test_ascii_escaping_and_key_order(self):
        # Manually specified canonical tokens, not a production serializer oracle.
        value = {'baseline': {'semantic_artifact': {'z': 'quote"', 'a': 'slash\\'}, 'manifest': {}},
                 'candidate': {'semantic_artifact': {'a': 'slash\\', 'z': 'quote"'}, 'manifest': {}}}
        result = third_leg(compact(value))
        self.assertEqual(result['canonical_baseline'], '{"a":"slash\\\\","z":"quote\\\""}')
        self.assertEqual(result['canonical_baseline'], result['canonical_candidate'])

    def test_frozen_tamper_still_blocks_atomic_admission(self):
        from profiles.crystal_receipt.expectation import make_profile
        from runner.expectation_contract import load_fixtures, admit, ProfileError
        from rsi.codec import encode, raw_digest
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for directory in ('evidence/crystal-receipt', 'profiles/crystal_receipt', 'corpora/crystal-receipt'):
                shutil.copytree(ROOT / directory, root / directory)
            profile = make_profile(root)
            fixtures = load_fixtures(root, profile)
            path = root / profile.expectations_path
            artifact = json.loads(path.read_bytes())
            row = next(iter(artifact['expectations'][0]['prediction'].values()))
            row['observation']['outputs']['semantic_identity_preserved'] = False
            raw = encode(artifact)
            path.write_bytes(raw)
            profile = replace(profile, expectations_digest=raw_digest(raw))
            with self.assertRaisesRegex(ProfileError, 'prediction disagrees'):
                admit(root, profile, fixtures)

    def test_third_leg_finishes_before_other_semantic_paths(self):
        from profiles.crystal_receipt import expectation
        original_third, original_profile = third_leg, expectation.make_profile
        events = []
        def record_third(*args, **kwargs):
            result = original_third(*args, **kwargs)
            events.append('C')
            return result
        def record_profile(*args, **kwargs):
            self.assertEqual(events, ['C'] * 4)
            events.append('admission')
            return original_profile(*args, **kwargs)
        with patch('tools.check_crystal_cleanroom.third_leg', side_effect=record_third), \
             patch.object(expectation, 'make_profile', side_effect=record_profile):
            compare()

    def test_existing_crystal_conformance_unchanged(self):
        from extensions.crystal_receipt import composition
        from runner.relation_runtime import execute
        self.assertEqual(execute(ROOT, *composition(ROOT))['totals'],
                         {'PASS': 4, 'FAIL': 0, 'INVALID_FIXTURE': 0, 'UNSUPPORTED': 0})
