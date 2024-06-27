import intro
from Truth_Table import Truth_Table
import os
CWD = os.getcwd()

# take in raw string input of user's formula
# formula = intro.intro() 
# print(formula)
# table = Truth_Table(formula)
# table.solve()
# table.show()
# table.save(f'{CWD}/table.xlsx')

a_implies_b = Truth_Table('A -> B')
a_implies_b.solve()
equivalent = Truth_Table('~A or B')
equivalent.solve()

assert a_implies_b == equivalent
