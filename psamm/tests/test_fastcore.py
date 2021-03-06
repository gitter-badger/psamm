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

from psamm.metabolicmodel import MetabolicModel
from psamm.database import DictDatabase
from psamm import fastcore
from psamm.datasource.modelseed import parse_reaction

try:
    from psamm.lpsolver import cplex
except ImportError:
    cplex = None

requires_solver = unittest.skipIf(cplex is None, 'solver not available')


@requires_solver
class TestFastcoreSimpleVlassisModel(unittest.TestCase):
    """Test fastcore using the simple model in [Vlassis14]_."""

    def setUp(self):
        # TODO use mock model instead of actual model
        self.database = DictDatabase()
        self.database.set_reaction('rxn_1', parse_reaction('=> (2) |A|'))
        self.database.set_reaction('rxn_2', parse_reaction('|A| <=> |B|'))
        self.database.set_reaction('rxn_3', parse_reaction('|A| => |D|'))
        self.database.set_reaction('rxn_4', parse_reaction('|A| => |C|'))
        self.database.set_reaction('rxn_5', parse_reaction('|C| => |D|'))
        self.database.set_reaction('rxn_6', parse_reaction('|D| =>'))
        self.model = MetabolicModel.load_model(
            self.database, self.database.reactions)
        self.solver = cplex.Solver()

    def test_lp10(self):
        result = fastcore.lp10(self.model, { 'rxn_6' },
                               { 'rxn_1', 'rxn_3', 'rxn_4', 'rxn_5' },
                               solver=self.solver, epsilon=0.001, scaling=1e3)
        supp = set(fastcore.support(result, 0.999*0.001))
        self.assertEqual(supp, { 'rxn_1', 'rxn_3', 'rxn_6' })

    def test_lp10_weighted(self):
        weights = { 'rxn_3': 1 }
        result = fastcore.lp10(self.model, { 'rxn_6' },
                               { 'rxn_1', 'rxn_3', 'rxn_4', 'rxn_5' },
                               solver=self.solver, epsilon=0.001, scaling=1e3,
                               weights=weights)
        supp = set(fastcore.support(result, 0.999*0.001))
        self.assertEqual(supp, { 'rxn_1', 'rxn_3', 'rxn_6' })

        weights = { 'rxn_3': 3 }
        result = fastcore.lp10(self.model, { 'rxn_6' },
                               { 'rxn_1', 'rxn_3', 'rxn_4', 'rxn_5' },
                               solver=self.solver, epsilon=0.001, scaling=1e3,
                               weights=weights)
        supp = set(fastcore.support(result, 0.999*0.001))
        self.assertEqual(supp, { 'rxn_1', 'rxn_4', 'rxn_5', 'rxn_6' })

    def test_lp7(self):
        result = fastcore.lp7(self.model, set(self.model.reactions), 0.001,
                              solver=self.solver)
        supp = set(fastcore.support_positive(result, 0.001*0.999))
        self.assertEqual(supp, { 'rxn_1', 'rxn_3', 'rxn_4', 'rxn_5', 'rxn_6' })

        result = fastcore.lp7(self.model, {'rxn_5'}, 0.001, solver=self.solver)
        supp = set(fastcore.support_positive(result, 0.001*0.999))
        self.assertEqual(supp, { 'rxn_1', 'rxn_4', 'rxn_5', 'rxn_6' })

    def test_find_sparse_mode_singleton(self):
        core = { 'rxn_1' }
        mode = set(fastcore.find_sparse_mode(
            self.model, core, set(self.model.reactions) - core,
            solver=self.solver, epsilon=0.001, scaling=1e3))
        self.assertEqual(mode, { 'rxn_1', 'rxn_3', 'rxn_6' })

        core = { 'rxn_2' }
        mode = set(fastcore.find_sparse_mode(
            self.model, core, set(self.model.reactions) - core,
            solver=self.solver, epsilon=0.001, scaling=1e3))
        self.assertEqual(mode, set())

        core = { 'rxn_3' }
        mode = set(fastcore.find_sparse_mode(
            self.model, core, set(self.model.reactions) - core,
            solver=self.solver, epsilon=0.001, scaling=1e3))
        self.assertEqual(mode, { 'rxn_1', 'rxn_3', 'rxn_6' })

        core = { 'rxn_4' }
        mode = set(fastcore.find_sparse_mode(
            self.model, core, set(self.model.reactions) - core,
            solver=self.solver, epsilon=0.001, scaling=1e3))
        self.assertEqual(mode, { 'rxn_1', 'rxn_4', 'rxn_5', 'rxn_6' })

        core = { 'rxn_5' }
        mode = set(fastcore.find_sparse_mode(
            self.model, core, set(self.model.reactions) - core,
            solver=self.solver, epsilon=0.001, scaling=1e3))
        self.assertEqual(mode, { 'rxn_1', 'rxn_4', 'rxn_5', 'rxn_6' })

        core = { 'rxn_6' }
        mode = set(fastcore.find_sparse_mode(
            self.model, core, set(self.model.reactions) - core,
            solver=self.solver, epsilon=0.001, scaling=1e3))
        self.assertEqual(mode, { 'rxn_1', 'rxn_3', 'rxn_6' })

    def test_find_sparse_mode_weighted(self):
        core = { 'rxn_1' }
        weights = { 'rxn_3': 1 }
        mode = set(fastcore.find_sparse_mode(
            self.model, core, set(self.model.reactions) - core,
            solver=self.solver, epsilon=0.001, scaling=1e3, weights=weights))
        self.assertEqual(mode, { 'rxn_1', 'rxn_3', 'rxn_6' })

        weights = { 'rxn_3': 3 }
        mode = set(fastcore.find_sparse_mode(
            self.model, core, set(self.model.reactions) - core,
            solver=self.solver, epsilon=0.001, scaling=1e3, weights=weights))
        self.assertEqual(mode, { 'rxn_1', 'rxn_4', 'rxn_5', 'rxn_6' })

    def test_fastcc_inconsistent(self):
        self.assertEqual(
            set(fastcore.fastcc(self.model, 0.001, solver=self.solver)),
            { 'rxn_2' })

    def test_fastcc_is_consistent_on_inconsistent(self):
        self.assertFalse(fastcore.fastcc_is_consistent(
            self.model, 0.001, solver=self.solver))

    def test_fastcc_is_consistent_on_consistent(self):
        self.model.remove_reaction('rxn_2')
        self.assertTrue(fastcore.fastcc_is_consistent(
            self.model, 0.001, solver=self.solver))

    def test_fastcc_consistent_subset(self):
        self.assertEqual(fastcore.fastcc_consistent_subset(
            self.model, 0.001, solver=self.solver),
            set(['rxn_1', 'rxn_3', 'rxn_4', 'rxn_5', 'rxn_6']))

    def test_fastcore_global_inconsistent(self):
        self.database.set_reaction('rxn_7', parse_reaction('|E| <=>'))
        self.model.add_reaction('rxn_7')
        with self.assertRaises(fastcore.FastcoreError):
            fastcore.fastcore(self.model, { 'rxn_7' }, 0.001,
                              solver=self.solver)


@requires_solver
class TestFastcoreTinyBiomassModel(unittest.TestCase):
    """Test fastcore using a model with tiny values in biomass reaction

    This model is consistent mathematically since there is a flux solution
    within the flux bounds. However, the numerical nature of the fastcore
    algorithm requires an epsilon-parameter indicating the minimum flux that
    is considered non-zero. For this reason, some models with reactions where
    tiny stoichiometric values appear can be seen as inconsistent by
    fastcore.

    In this particular model, rxn_2 can take a maximum flux of 1000. At the
    same time rxn_1 will have to take a flux of 1e-4. This is the maximum
    possible flux for rxn_1 so running fastcore with an epsilon larger than
    1e-4 will indicate that the model is not consistent.
    """

    def setUp(self):
        # TODO use mock model instead of actual model
        self.database = DictDatabase()
        self.database.set_reaction('rxn_1', parse_reaction('=> |A|'))
        self.database.set_reaction('rxn_2',
            parse_reaction('(0.000001) |A| =>'))
        self.model = MetabolicModel.load_model(
            self.database, self.database.reactions)
        self.solver = cplex.Solver()

    def test_fastcc_is_consistent(self):
        self.assertTrue(fastcore.fastcc_is_consistent(
            self.model, 0.001, solver=self.solver))

    def test_fastcore_induced_model(self):
        core = { 'rxn_2' }
        self.assertEquals(set(fastcore.fastcore(
            self.model, core, 0.001, solver=self.solver)),
            { 'rxn_1', 'rxn_2' })

    def test_fastcore_induced_model_high_epsilon(self):
        core = { 'rxn_2' }
        self.assertEquals(set(fastcore.fastcore(
            self.model, core, 0.1, solver=self.solver)), { 'rxn_1', 'rxn_2' })


@requires_solver
class TestFlippingModel(unittest.TestCase):
    """Test fastcore on a model that has to flip"""

    def setUp(self):
        # TODO use mock model instead of actual model
        self.database = DictDatabase()
        self.database.set_reaction('rxn_1', parse_reaction('|A| <=>'))
        self.database.set_reaction('rxn_2', parse_reaction('|A| <=> |B|'))
        self.database.set_reaction('rxn_3', parse_reaction('|C| <=> |B|'))
        self.database.set_reaction('rxn_4', parse_reaction('|C| <=>'))
        self.model = MetabolicModel.load_model(
            self.database, self.database.reactions)
        self.solver = cplex.Solver()

    def test_fastcore_induced_model(self):
        core = { 'rxn_2', 'rxn_3' }
        self.assertEquals(set(
            fastcore.fastcore(self.model, core, 0.001, solver=self.solver)),
            { 'rxn_1', 'rxn_2', 'rxn_3', 'rxn_4' })


if __name__ == '__main__':
    unittest.main()
