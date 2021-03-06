#!/usr/bin/env python
# This file is part of PSAMM.
#
# PSAMM is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# PSAMM is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with PSAMM.  If not, see <http://www.gnu.org/licenses/>.
#
# Copyright 2014-2015  Jon Lund Steffensen <jon_steffensen@uri.edu>

import unittest

from psamm.formula import Formula, Atom, Radical


class TestFormula(unittest.TestCase):
    def test_formula_merge_same_formulas_with_same_atoms(self):
        f = Formula({Atom('H'): 2, Atom('O'): 1}) | Formula({Atom('N'): 1, Atom('O'): 2})
        self.assertEquals(f, Formula({Atom('H'): 2, Atom('N'): 1, Atom('O'): 3}))

    def test_formula_merge_formulas_that_cancel_out(self):
        f = Formula({Atom('H'): 3}) | Formula({Atom('H'): -3})
        self.assertEquals(f, Formula())

    def test_formula_multiply_number(self):
        f = Formula({Atom('H'): 2, Atom('O'): 1}) * 4
        self.assertEquals(f, Formula({Atom('H'): 8, Atom('O'): 4}))

    def test_formula_multiply_one(self):
        f = Formula({Atom('H'): 2, Atom('O'): 1}) * 1
        self.assertEquals(f, f)

    def test_formula_multiply_zero(self):
        f = Formula({Atom('H'): 2, Atom('O'): 1}) * 0
        self.assertEquals(f, Formula())

    def test_formula_right_multiply_number(self):
        f = 2 * Formula({Atom('H'): 2, Atom('O'): 1})
        self.assertEquals(f, Formula({Atom('H'): 4, Atom('O'): 2}))

    def test_formula_repeat(self):
        f = Formula({Atom('H'): 2, Atom('O'): 1}).repeat(4)
        self.assertEquals(f, Formula({ Formula({Atom('H'): 2, Atom('O'): 1}): 4 }))

    def test_formula_equals_other_formula(self):
        f = Formula({Atom('H'): 2, Atom('O'): 1})
        self.assertEquals(f, Formula({Atom('O'): 1, Atom('H'): 2}))

    def test_formula_not_equals_other_with_distinct_elements(self):
        f = Formula({Atom('Au'): 1})
        self.assertNotEquals(f, Formula({Atom('Ag'): 1}))

    def test_formula_not_equals_other_with_different_number(self):
        f = Formula({Atom('Au'): 1})
        self.assertNotEquals(f, Formula({Atom('Au'): 2}))

    def test_formula_parse_with_final_digit(self):
        f = Formula.parse('H2O2')
        self.assertEquals(f, Formula({Atom('H'): 2, Atom('O'): 2}))

    def test_formula_parse_with_implicit_final_digit(self):
        f = Formula.parse('H2O')
        self.assertEquals(f, Formula({Atom('H'): 2, Atom('O'): 1}))

    def test_formula_parse_with_implicit_digit(self):
        f = Formula.parse('C2H5NO2')
        self.assertEquals(f, Formula({Atom('C'): 2, Atom('H'): 5, Atom('N'): 1, Atom('O'): 2}))

    def test_formula_parse_with_wide_element(self):
        f = Formula.parse('ZnO')
        self.assertEquals(f, Formula({Atom('Zn'): 1, Atom('O'): 1}))

    def test_formula_parse_with_wide_count(self):
        f = Formula.parse('C6H10O2')
        self.assertEquals(f, Formula({Atom('C'): 6, Atom('H'): 10, Atom('O'): 2}))

    def test_formula_parse_with_implicitly_counted_subgroup(self):
        f = Formula.parse('C2H6O2(CH)')
        self.assertEquals(f, Formula({Atom('C'): 2, Atom('H'): 6, Atom('O'): 2,
                                      Formula({Atom('C'): 1, Atom('H'): 1}): 1}))

    def test_formula_parse_with_counted_subgroup(self):
        f = Formula.parse('C2H6O2(CH)2')
        self.assertEquals(f, Formula({Atom('C'): 2, Atom('H'): 6, Atom('O'): 2,
                                      Formula({Atom('C'): 1, Atom('H'): 1}): 2}))

    def test_formula_parse_with_two_identical_counted_subgroups(self):
        f = Formula.parse('C2H6O2(CH)2(CH)2')
        self.assertEquals(f, Formula({Atom('C'): 2, Atom('H'): 6, Atom('O'): 2,
                                      Formula({Atom('C'): 1, Atom('H'): 1}): 4}))

    def test_formula_parse_with_two_distinct_counted_subgroups(self):
        f = Formula.parse('C2H6O2(CH)2(CH2)2')
        self.assertEquals(f, Formula({Atom('C'): 2, Atom('H'): 6, Atom('O'): 2,
                                      Formula({Atom('C'): 1, Atom('H'): 1}): 2,
                                      Formula({Atom('C'): 1, Atom('H'): 2}): 2}))

    def test_formula_parse_with_wide_counted_subgroup(self):
        f = Formula.parse('C2(CH)10NO2')
        self.assertEquals(f, Formula({Atom('C'): 2, Atom('N'): 1, Atom('O'): 2,
                                        Formula({Atom('C'): 1, Atom('H'): 1}): 10}))

    def test_formula_parse_with_radical(self):
        f = Formula.parse('C2H4NO2R')
        self.assertEquals(f, Formula({Atom('C'): 2, Atom('H'): 4, Atom('N'): 1,
                                        Atom('O'): 2, Radical('R'): 1}))

    def test_formula_parse_with_numbered_radical(self):
        f = Formula.parse('C2H4NO2(R1)')
        self.assertEquals(f, Formula({Atom('C'): 2, Atom('H'): 4, Atom('N'): 1,
                                        Atom('O'): 2, Radical('R1'): 1}))

    def test_formula_balance_missing_on_one_side(self):
        f1, f2 = Formula.balance(Formula.parse('H2O'), Formula.parse('OH'))
        self.assertEquals(f1, Formula())
        self.assertEquals(f2, Formula({Atom('H'): 1}))

    def test_formula_balance_missing_on_both_sides(self):
        f1, f2 = Formula.balance(Formula.parse('C3H6OH'), Formula.parse('CH6O2'))
        self.assertEquals(f1, Formula({Atom('O'): 1}))
        self.assertEquals(f2, Formula({Atom('C'): 2, Atom('H'): 1}))

    def test_formula_balance_subgroups_cancel_out(self):
        f1, f2 = Formula.balance(Formula.parse('H2(CH2)n'), Formula.parse('CH3O(CH2)n'))
        self.assertEquals(f1, Formula({Atom('C'): 1, Atom('H'): 1, Atom('O'): 1}))
        self.assertEquals(f2, Formula())


if __name__ == '__main__':
    unittest.main()
