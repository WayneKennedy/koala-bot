# SPDX-License-Identifier: CERN-OHL-S-2.0
import copy
import json
import pathlib
import tempfile
import unittest
from unittest.mock import patch

from build123d import Pos
from koala_hardware import part_versions as V
from koala_hardware.parts import pelvis


class PartVersions(unittest.TestCase):
    def test_ledger_matches_code(self):
        problems = V.check()
        self.assertEqual(problems, [], '\n'.join(problems))


class SocketFixture(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.socket = pelvis.root_socket()
        cls.original = V.fingerprint(cls.socket)
        # Moving all four nut pockets and bores keeps volume, outside dimensions
        # and topology counts unchanged: the concrete review regression.
        moved_centres = [(x + 0.5, y) for x, y in pelvis.nut_xy()]
        with patch.object(pelvis, 'nut_xy', return_value=moved_centres):
            cls.moved = V.fingerprint(pelvis.root_socket.__wrapped__())


class FingerprintRegression(SocketFixture):
    def test_root_socket_fixing_relocation_is_a_versioned_change(self):
        self.assertTrue(V._legacy_same(self.original, self.moved))
        self.assertFalse(V.same(self.original, self.moved))
        problems = V.check(
            {'root_socket': {'version': 1, 'fingerprint': self.moved}},
            {'root_socket': {'version': 1, 'fingerprint': self.original}})
        self.assertIn('geometry changed at v1', problems[0])

    def test_whole_part_translation_preserves_fingerprint(self):
        translated = V.fingerprint(Pos(102.37, -56.12, 17.05) * self.socket)
        self.assertTrue(V.same(self.original, translated))

    def test_face_order_and_numeric_noise_do_not_change_geometry(self):
        noisy = copy.deepcopy(self.original)
        noisy['face_geometry'].reverse()
        for descriptor in noisy['face_geometry']:
            for index in range(1, len(descriptor)):
                descriptor[index] += 0.0002
        self.assertTrue(V.same(self.original, noisy))


class LedgerUpdateRegression(SocketFixture):
    def setUp(self):
        directory = tempfile.TemporaryDirectory()
        self.addCleanup(directory.cleanup)
        self.directory = pathlib.Path(directory.name)
        self.manifest = self.directory / 'part-versions.json'
        patcher = patch.object(V, 'MANIFEST', self.manifest)
        patcher.start()
        self.addCleanup(patcher.stop)
        self.saved = {'root_socket': {
            'version': 2, 'since': '2026-09-19', 'fingerprint': self.original,
            'history': [{'version': 2, 'date': '2026-09-19', 'note': 'existing print'}]}}
        self.manifest.write_text(json.dumps(self.saved))

    def current(self, version, fingerprint=None):
        return {'root_socket': {'version': version,
                                'fingerprint': fingerprint or self.original}}

    def assert_update_rejected_without_writing(self, now, message, note='test revision'):
        previous = self.manifest.read_bytes()
        with patch.object(V, 'current', return_value=now):
            with self.assertRaisesRegex(SystemExit, message):
                V.update(note)
        self.assertEqual(self.manifest.read_bytes(), previous)

    def test_update_rejects_version_decrease_with_unchanged_geometry(self):
        self.assert_update_rejected_without_writing(self.current(1), 'versions never go down')

    def test_update_rejects_version_decrease_with_changed_geometry(self):
        now = {'new_part': {'version': 1, 'fingerprint': self.original},
               **self.current(1, self.moved)}
        self.assert_update_rejected_without_writing(now, 'versions never go down')

    def test_update_rejects_relocated_features_without_bump(self):
        self.assert_update_rejected_without_writing(self.current(2, self.moved),
                                                   'geometry changed without a version bump')

    def test_update_requires_note_for_version_change(self):
        self.assert_update_rejected_without_writing(self.current(3, self.moved),
                                                   'requires a note', note='  ')

    def test_bumped_update_retains_history(self):
        with patch.object(V, 'current', return_value=self.current(3, self.moved)):
            V.update('Move mounting pattern 0.5 mm for driver clearance')
        updated = V.load()['root_socket']
        self.assertEqual(updated['version'], 3)
        self.assertEqual(updated['history'][:-1], self.saved['root_socket']['history'])
        self.assertTrue(V.same(updated['fingerprint'], self.moved))

    def legacy_ledger(self):
        legacy = copy.deepcopy(self.saved)
        del legacy['root_socket']['fingerprint']['schema']
        del legacy['root_socket']['fingerprint']['face_geometry']
        self.manifest.write_text(json.dumps(legacy))
        return legacy

    def write_baseline(self, version=2):
        baseline = self.directory / 'baseline.json'
        baseline.write_text(json.dumps({'source_revision': 'a' * 40,
                                        'parts': self.current(version)}))
        return baseline

    def test_legacy_fingerprint_requires_explicit_migration(self):
        legacy = self.legacy_ledger()
        self.assertIn('legacy fingerprint', V.check(self.current(2), legacy)[0])
        self.assert_update_rejected_without_writing(self.current(2), 'legacy fingerprint')
        self.assert_update_rejected_without_writing(self.current(3), 'legacy fingerprint')

    def test_migration_records_historical_geometry_before_current_edits(self):
        self.legacy_ledger()
        with patch.object(V, 'current', side_effect=AssertionError('must use historical baseline')):
            V.migrate_baseline(self.write_baseline())
        migrated = V.load()['root_socket']
        self.assertEqual(migrated['version'], 2)
        self.assertEqual(migrated['history'], self.saved['root_socket']['history'])
        self.assertEqual(migrated['fingerprint_migrations'][0]['source_revision'], 'a' * 40)
        self.assert_update_rejected_without_writing(self.current(2, self.moved),
                                                   'geometry changed without a version bump')

    def test_migration_rejects_wrong_baseline_without_writing(self):
        self.legacy_ledger()
        previous = self.manifest.read_bytes()
        with self.assertRaisesRegex(SystemExit, 'baseline does not match'):
            V.migrate_baseline(self.write_baseline(version=3))
        self.assertEqual(self.manifest.read_bytes(), previous)

    def test_explicit_empty_ledger_is_not_replaced_with_disk_ledger(self):
        self.assertIn('not in part-versions.json', V.check(self.current(2), saved={})[0])
