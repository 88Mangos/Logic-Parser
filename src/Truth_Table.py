import numpy as np
import pandas as pd
import itertools

# truth table has to
# take in formula
# create empty truth table using prop_vars
# create truth assignments sigma
# assign the sigma's values into the formula and compute

import compute
import format
from format import is_connective, is_truth_variable

class Truth_Table():
    def __init__(self, formula):
        self.formula, self.vars = format.format(formula)
        self.table = pd.DataFrame()
        self.vars = sorted(self.vars)
    
    def __eq__(self, other):
        return self.table['results'].all() == other.table['results'].all()

    def generate_sigma(self):
        """
        use self.prop_vars
        if the number of variables is n,
        the number of possible truth assignemnts,
        denoted sigma,
        is 2**n.
        each truth assignment has length n.
        """
        n = len(self.vars)
        sigmas = [np.array(p, dtype=np.uint8) for p in itertools.product([0, 1], repeat=n)]
        sigmas = np.array(sigmas)
        assert sigmas.shape == (2**n, n)
        return sigmas

    def assign(self, sigma):
        assert sigma.shape == (len(self.vars),)
        assignment = {}
        i=0
        for i in range(len(self.vars)):
            assignment[self.vars[i]] = sigma[i] 

        # print(f'Assignment {assignment}')

        replaced_formula = ""
        for i in range(len(self.formula)):
            token = self.formula[i]
            if is_connective(token) or is_truth_variable(token):
                replaced_formula+=token
            elif token in self.vars:
                replaced_formula+=str(assignment[token])

        for var in self.vars:
            assert replaced_formula.find(var) == -1

        return replaced_formula

    def sigma_to_key(self, sigma):
        key = ""
        for i in sigma:
            key += str(i)
        return key

    def solve(self):
        results = {}
        sigmas = self.generate_sigma()

        table = {}
        for i in range(len(self.vars)):
            table[self.vars[i]] = []

        for sigma in sigmas:
            for i in range(len(self.vars)):
                var = self.vars[i]
                table[var].append(sigma[i])

            formula = self.assign(sigma)
            formula = compute.remove_parentheses(formula)
            result = compute.compute(formula)
            key = self.sigma_to_key(sigma)

            # print(f"SIGMA: {key}")
            # print(f"RESULT: {result}")

            results[key] = result

        table['sigma'] = results.keys()
        table['results'] = results.values()

        # print(f'Table: {table}')

        self.table = pd.DataFrame(table)
        return result
    
    def show(self):
        print(self.table)

    def save(self, path):
        self.table.to_excel(path)