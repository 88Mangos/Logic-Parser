OP_NOT = '¬'
OP_AND = '∧'
OP_NAND = '⊼'
OP_XOR = '⊻'
OP_OR = '∨' 
OP_NOR = '⊽' 
OP_IMPLIES = '→'
OP_BIIMPLIES = '↔' 

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
    
    print(formula)
    return ValueError("What happened???")

def assign(formula, sigma):
    # given a formula
    # find its prop_vars
    # replace them with 1 or 0 depending on what they should be in sigma.
    pass

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
            assert is_truth_variable(formula[i]) # make sure it's a 0 or 1; prop_vars don't have other values.
            tokens.append(formula[i])
            i+=1
            continue
        
    assert len(tokens) <= len(formula) 
    # if everything in formula is a prop_var or connective, the lengths are equal;
    # if formula has parentheticals, length of tokens is shorter than length of formula.

    return tokens

def remove_parentheses(formula):
    tokens = tokenize(formula)
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