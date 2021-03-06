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

from psamm.lpsolver import lp

try:
    from psamm.lpsolver import cplex
except ImportError:
    cplex = None

requires_solver = unittest.skipIf(cplex is None, 'solver not available')


@requires_solver
class TestCplexProblem(unittest.TestCase):
    def setUp(self):
        self.solver = cplex.Solver()

    def test_objective_reset_on_set_linear_objective(self):
        prob = self.solver.create_problem()
        prob.define('x', 'y', lower=0, upper=10)
        prob.add_linear_constraints(prob.var('x') + prob.var('y') <= 12)
        prob.set_objective_sense(lp.ObjectiveSense.Maximize)

        # Solve first time, maximize x
        prob.set_linear_objective(2*prob.var('x'))
        result = prob.solve()
        self.assertAlmostEqual(result.get_value('x'), 10)

        # Solve second time, maximize y
        # If the objective is not properly cleared,
        # the second solve will still maximize x.
        prob.set_linear_objective(prob.var('y'))
        result = prob.solve()
        self.assertAlmostEqual(result.get_value('y'), 10)

    def test_result_to_bool_conversion_on_optimal(self):
        '''Run a feasible LP problem and check that the result evaluates to True'''
        prob = self.solver.create_problem()
        prob.define('x', 'y', lower=0, upper=10)
        prob.add_linear_constraints(prob.var('x') + prob.var('y') <= 12)
        prob.set_objective_sense(lp.ObjectiveSense.Maximize)

        prob.set_linear_objective(2*prob.var('x'))
        result = prob.solve()
        self.assertTrue(result)

    def test_result_to_bool_conversion_on_infeasible(self):
        '''Run an infeasible LP problem and check that the result evaluates to False'''
        prob = self.solver.create_problem()
        prob.define('x', 'y', 'z', lower=0, upper=10)
        prob.add_linear_constraints(2*prob.var('x') == -prob.var('y'),
                                    prob.var('x') + prob.var('z') >= 6,
                                    prob.var('z') <= 3)
        prob.set_objective_sense(lp.ObjectiveSense.Maximize)
        prob.set_linear_objective(2*prob.var('x'))
        result = prob.solve()
        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
