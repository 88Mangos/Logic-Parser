VALID_CONNECTIVES = {
    'and', '&', 'or', '|', '!', 'not', 'xor', '^',
    'implies', '->', 'if-and-only-if', '<->',
    'nand', '!&', 'nor', '~'
}

OP_NOT = '¬'
OP_AND = '∧'
OP_NAND = '⊼'
OP_XOR = '⊻'
OP_OR = '∨' 
OP_NOR = '⊽' 
OP_IMPLIES = '→'
OP_BIIMPLIES = '↔' 

def is_connective(token):
    # all valid connectives after formatting
    # organized in descending binding order (earlier items evaluted first)
    return token in ['¬' # negation
                     '∧', # and
                     '⊼', # nand
                     '⊻', # xor
                     '∨', # or
                     '⊽', # nor
                     '→', # implies
                     '↔', # biimplies
                    ]

def is_truth_variable(token):
    return token in ['0','1']

def standard(item):
    if not item in VALID_CONNECTIVES:
        return ValueError("Invalid Connective")
    # and ∧, or ∨, nand ⊼, xor ⊻, implies →, biimplies ↔, nor ⊽, negation ¬
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
    formula = "".join(tokens)

    return (formula, variables)

def tokenize(formula):
    # split input string
    # return: list of strings
    # only containing prop_vars, connectives, and parentheticals.
    tokens = []
    i=0
    while i<len(formula):
        # case 1: the character is a connective
        if is_connective(formula[i]):
            tokens.append(formula[i])
            i+=1
            continue
        # case 2: character signals beginning of parenthetical
        # it's possible that the next closing parentheses isn't the paired one.
        # thus, once we find (, we look for the ) from the back of the formula
        elif formula[i][0] == '(':
            j=len(formula) 
            # find the closing parentheses of the parenthetical, 
            # starting from back ensures we've paired our parentheses
            while True:
                j-=1
                if formula[j] == ')':
                    break
            tokens.append(formula[i:j+1])
            i=j+1 # increment i to the next token
            continue
        # case 3: character is a prop_var
        else:
            tokens.append(formula[i])
            i+=1
            continue
        
    assert len(tokens) <= len(formula) 
    # if everything in formula is a prop_var or connective, the lengths are equal;
    # if formula has parentheticals, length of tokens is shorter than length of formula.

    return tokens