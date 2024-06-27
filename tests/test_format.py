import format
# take in raw string input of user's formula
formula = format.intro() 
print(formula)
formula, vars = format.format(formula) 
print(formula)