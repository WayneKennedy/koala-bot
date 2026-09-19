# SPDX-License-Identifier: CERN-OHL-S-2.0
import unittest
from koala_hardware import part_versions as V


class PartVersions(unittest.TestCase):
    def test_ledger_matches_code(self):
        problems=V.check()
        self.assertEqual(problems,[],'\n'.join(problems))
