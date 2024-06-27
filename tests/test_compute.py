import compute
tests = {
    # negations
    '¬1':'0',
    '¬0':'1',

    # and, nand
    '0∧0':'0',
    '1∧0':'0',
    '0∧1':'0',
    '1∧1':'1',

    '0⊼0':'1',
    '1⊼0':'1',
    '0⊼1':'1',
    '1⊼1':'0',

    # xor
    '0⊻0':'0',
    '1⊻0':'1',
    '0⊻1':'1',
    '1⊻1':'0',

    # or, nor
    '0∨0':'0',
    '1∨0':'1',
    '0∨1':'1',
    '1∨1':'1',

    '0⊽0':'1',
    '1⊽0':'0',
    '0⊽1':'0',
    '1⊽1':'0',

    # implies
    '0→0':'1',
    '1→0':'0',
    '0→1':'1',
    '1→1':'1',
    
    # biimplies
    '0↔0':'1',
    '1↔0':'0',
    '0↔1':'0',
    '1↔1':'1',

    # compounds
    '¬1∨0': '0',
    '¬1∨1': '1',
    '1∨0∧1': '1',
    '0∨0∧1': '0',
}

for key in tests:
    truth = tests[key]
    computed = compute.compute(key)
    # print(f'EXPRESSION: {key}')
    # print(f'TRUTH: {truth}')
    # print(f'COMPUTED: {computed}')
    assert computed == truth