VALID_CONNECTIVES = {
    'and', '&', 'or', '|', '!', 'not', 'xor', '^',
    'implies', '->', 'if-and-only-if', '<->',
    'nand', '!&', 'nor', '~'
}

from compute import is_truth_variable

def standard(item):
    if not item in VALID_CONNECTIVES:
        return ValueError("Invalid Connective")
    # 'and ∧, or ∨, nand ⊼, xor ⊻, implies →, biimplies ↔, nor ⊽, negation ¬''
    if item in ['and', '&']:
        item = '∧'
    elif item in ['or', '|']:
        item = '∨'
    elif item in ['!', 'not', '~']:
        item = '¬'
    elif item in ['xor', '^']:
        item = '⊻'
    elif item in ['implies', '->']:
        item = '→'
    elif item in ['if-and-only-if', '<->']:
        item = '↔'
    elif item in ['nand', '!&']:
        item = '⊼'
    elif item in ['nor']:
        item = '⊽'
    return item

def format(formula):
    """
    Goals:
    first, convert the input string into a list of strings
    -> each list item is either a connective
    -> or a variable
    --> a parenthetical should be treated as one variable
    ---> because we will have columns for every variable in our final truth table

    put everything in this list into a set. 
    Use the difference() function for sets to separate out the variables from connectives

    then, standardize all the connectives to the notation used in 15-051 DMP's grader

    last, generate a truth table.

    After all of that, create a simple function equivalence(A, B)
    that determines whether two expressions A and B are equivalent by truth table

    """
    # Remove all whitespaces
    formula = formula.replace(" ", "")
    print(f'STRIPPED: {formula}')
    # Tokenize the input formula and standardize connectives
    i = 0
    tokens = []
    variables = set()
    while i < len(formula):
        if formula[i:i+2] in VALID_CONNECTIVES:
            tokens.append(standard(formula[i:i+2]))
            i += 2
        elif formula[i:i+3] in VALID_CONNECTIVES:
            tokens.append(standard(formula[i:i+3]))
            i += 3
        elif formula[i:i+4] in VALID_CONNECTIVES:
            tokens.append(standard(formula[i:i+4]))
            i += 4
        else:
            tokens.append(formula[i])
            if formula[i].isalpha() or is_truth_variable(formula[i]):
                variables.add(formula[i])
            i += 1
    print(f'TOKENS: {tokens}')
    formula = "".join(tokens)

    return (formula, variables)

def intro():
    print("Hello! This is a logic parser!")
    print("PLEASE READ THE INPUT RULES CAREFULLY")
    print("")
    print("")
    print("VARIABLES")
    print("- only use letters of the alphabet for variable names")
    print("- do NOT use numbers for variable names.")
    print("- variable names should be 1 character long")
    print("- you may input '0' or '1' for False or True respectively")
    print("")
    print("")
    print("VALID CONNECTIVES")
    print("Here are the symbols you should use:")
    print("")
    print("for disjunction, type '|' or 'or',")
    print("for conjunction, type '&' or 'and',")
    print("for negation, type '~' or '!' or 'not',")
    print("for exclusive or, type '^' or 'xor',")
    print("for implication, type '->' or 'implies',")
    print("for biimplication, type '<->' or 'if-and-only-if',")
    print("for NAND, type '!&' or 'nand',")
    print("for NOR, type 'nor'.")
    print("")
    print("")
    print("NOTES")
    print("- implication will associate to the right.")
    print("")
    print("You don't have to be perfect with your inputs, because")
    print("Spaces will be removed and reformatted to fit the parser.")
    print("However, if you input a formula using words (e.g., A and B)")
    print("Please use spaces to set off your connectives.")
    print("")
    INPUT = input("Paste in logical expression.")
    return INPUT