import format
from format import OP_NOT, OP_AND, OP_NAND, OP_XOR, OP_OR, OP_NOR, OP_IMPLIES, OP_BIIMPLIES
from format import is_truth_variable, is_connective

# define operations
# I know this isn't the most efficient; simple booleans are easier, but I'm coding the principle
def NOT(a):
    if (a=='0'): return '1'
    elif (a=='1'): return '0'

def AND(a, b):
    if (a=='1' and b=='1'):
        return '1'
    return '0'

def NAND(a,b):
    return NOT(AND(a,b))

def XOR(a,b):
    return AND(OR(a,b), NOT(AND(a,b)))

def OR(a,b):
    if (a=='0' and b=='0'):
        return '0'
    return '1'

def NOR(a,b):
    return NOT(OR(a,b))

def IMPLIES(a,b):
    # use identity that a -> b is equivalent to ~a | b
    return OR(NOT(a), b)

def BIIMPLIES(a,b):
    # use identity that it's just implies(a,b) AND implies(b,a)
    return AND(IMPLIES(a,b), IMPLIES(b,a))

def compute(formula): # return truth value of a formula that has no parentheses
    """
    b/c there's no parentheses, the tokenized formula is just the formula
    Thus, there's no need to tokenize since a string is just a list of chars
    """

    # base case: formula is just a truth value
    if is_truth_variable(formula):
        return formula
    
    # first: negation
    simplified = ""
    i=0
    while i < len(formula):
        if formula[i] == OP_NOT:
            simplified += NOT(formula[i+1])
            i+=1
        else: 
            simplified += formula[i]
        i+=1
    
    # store and reset our simplified form
    formula = simplified
    simplified = ""
    if is_truth_variable(formula):
        return formula

    # second pass: conjunctions
    i=0
    while i < len(formula):
        if formula[i] == OP_AND:
            simplified=simplified[:-1] # pop the last addition to simplified, which is a var in this expr
            simplified += AND(formula[i-1],formula[i+1])
            i+=2 # skip the AND sign and the next var.
        elif formula[i] == OP_NAND:
            simplified=simplified[:-1] 
            simplified += NAND(formula[i-1],formula[i+1])
            i+=2 
        else: 
            simplified += formula[i]
        i+=1

    # store and reset our simplified form
    formula = simplified
    simplified = ""
    if is_truth_variable(formula):
        return formula

    # third pass: exclusive or
    i=0
    while i < len(formula):
        if formula[i] == OP_XOR:
            simplified=simplified[:-1]
            simplified += XOR(formula[i-1],formula[i+1])
            i+=2 
        else: 
            simplified += formula[i]
        i+=1

    # store and reset our simplified form
    formula = simplified
    simplified = ""
    if is_truth_variable(formula):
        return formula

    # fourth pass: disjunctions
    i=0
    while i < len(formula):
        if formula[i] == OP_OR:
            simplified=simplified[:-1]
            simplified += OR(formula[i-1],formula[i+1])
            i+=2 
        elif formula[i] == OP_NOR:
            simplified=simplified[:-1]
            simplified += NOR(formula[i-1],formula[i+1])
            i+=2 
        else: 
            simplified += formula[i]
        i+=1

    # store and reset our simplified form
    formula = simplified
    simplified = ""
    if is_truth_variable(formula):
        return formula

    # f pass: implications
    i=0
    while i < len(formula):
        if formula[i] == OP_IMPLIES:
            simplified=simplified[:-1]
            simplified += IMPLIES(formula[i-1],formula[i+1])
            i+=2 
        else: 
            simplified += formula[i]
        i+=1

    # store and reset our simplified form
    formula = simplified
    simplified = ""
    if is_truth_variable(formula):
        return formula

    # fifth pass: biimplications
    i=0
    while i < len(formula):
        if formula[i] == OP_BIIMPLIES:
            simplified=simplified[:-1] 
            simplified += BIIMPLIES(formula[i-1],formula[i+1])
            i+=2
        else: 
            simplified += formula[i]
        i+=1

    # store and reset our simplified form
    formula = simplified
    simplified = ""
    if is_truth_variable(formula):
        return formula
    
    return ValueError(f"What happened to formula: {formula}?")

def remove_parentheses(formula):
    tokens = format.tokenize(formula)
    out_tokens = []
    """
    simplify the formula down
    so the tokens are only prop_vars and connectives. No parentheticals.
    """
    for token in tokens:
        # case 1: token isn't a parenthetical
        if not (token[0] == '('):
            out_tokens.append(token)
            continue
        # case 2: token is parenthetical
        else:
            inner_formula = token.join()
            assert inner_formula[len(inner_formula)-1] == ')' # make sure the parenthetical is closed

            inner_formula = inner_formula[1:len(inner_formula)-2] # remove the start and end parentheses
            # case 2a: parenthetical inner formula has no more parentheticals
            # -> do nothing
            # case 2b: parenthetical inner formula has more parentheticals
            if inner_formula.find('(' != -1):
                inner_formula = remove_parentheses(inner_formula) # recursively process the inner formula
            out_tokens.append(compute(inner_formula))
            continue
    
    # join the tokens back into a string
    return "".join(tokens)