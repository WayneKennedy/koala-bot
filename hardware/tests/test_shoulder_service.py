# SPDX-License-Identifier: CERN-OHL-S-2.0
"""Assembly path: load cassette nuts before A; remove the module outward."""
from math import sqrt
import unittest

from build123d import Compound, Plane, Pos, RegularPolygon, Rot, extrude, mirror
from koala_hardware import params as P, servo_iface as S
from koala_hardware.audit import clear, volume
from koala_hardware.parts import shoulder_mount as M, torso


class ShoulderService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.cassette = M.solid()
        cls.root = M.module()
        cls.servo = M.socket_frame() * S.socket_reference()
        cls.nuts = [
            Pos(20.1, y, z) * Rot(Y=90) * extrude(
                RegularPolygon(P.NUT_M3_AF / sqrt(3), 6), amount=P.NUT_M3_T)
            for y, z in P.SHOULDER_CASSETTE_BOLTS
        ]

    def test_all_four_nuts_load_on_bare_cassette_and_clear_when_seated(self):
        for index, nut in enumerate(self.nuts):
            for withdrawal in (0, 2.5, 6):
                clear(Pos(-withdrawal, 0, 0) * nut, self.cassette,
                      f'cassette nut {index} bare insertion at {withdrawal}')
            for name, obstacle in (('cassette', self.cassette),
                                   ('root', self.root), ('servo', self.servo)):
                clear(nut, obstacle, f'cassette nut {index} seated / {name}')

    def test_inner_nuts_must_be_loaded_before_root_is_attached(self):
        # A 2.4 mm nut must withdraw at least 2.5 mm to clear its pocket.
        # The fitted root obstructs that straight path for the inner nut row;
        # this is why the documented order is nuts, root, complete cassette.
        for nut, (y, z) in zip(self.nuts, P.SHOULDER_CASSETTE_BOLTS):
            if y == 17:
                overlap = (Pos(-2.5, 0, 0) * nut) & self.root
                self.assertGreater(volume(overlap), 0.01, (y, z))

    def test_complete_a_module_can_be_removed_laterally(self):
        right = Compound(children=[self.cassette, self.root, self.servo,
                                   M.root_fixings(), *self.nuts])
        left = mirror(right, Plane.XZ)
        frame = torso.solid()
        # Frame screws have been removed. The A/module/root fixings and captive
        # nuts remain; the moving carrier/downstream limb is outside this test.
        for hand, unit, opposite, direction in (('right', right, left, 1),
                                                ('left', left, right, -1)):
            for offset in (0, 5, 20, 80):
                moved = Pos(0, direction * offset, 0) * unit
                clear(moved, frame, f'{hand} cassette outward {offset} / torso')
                clear(moved, opposite, f'{hand} cassette outward {offset} / opposite A')
