#!/usr/bin/env python3
#https://adventofcode.com/2022/day/21

def parse_inputs(filename):
    pairs = [l.strip().split(': ') for l in open(filename,'r').readlines()]
    values = dict([(k,int(v)) for k,v in pairs if v.isnumeric()])
    expressions = dict([(k,v.split(' ')) for k,v in pairs if not v.isnumeric()])
    return values, expressions

def solve(expression, values):
    l,op,r = expression
    if l in values and r in values:
        return eval(f'{values[l]} {op} {values[r]}')
    return None

def part1(values,expressions):
    # while(expressions):
    for i in range(100):
        remove_these_from_expressions = []
        for k,v in expressions.items():
            result = solve(v, values)
            print(k,v,result)
            if result is not None:
                # move to value dict if solved
                values[k] = result
                remove_these_from_expressions.append(k)
                
        # stop condition
        if 'root' in values: 
            return values['root'] 

        # remove all solved expressions
        for k in remove_these_from_expressions:
            del expressions[k]
            
    print(expressions)

# answers #########################################################################################

examples = parse_inputs('examples/21')
inputs   = parse_inputs('inputs/21')

print('Part 1: ', part1(*inputs))


# tests ###########################################################################################
def test_part1_example():
    assert part1(*examples) == 152
    
# def test_parse_file():
#     assert examples == ({'dbpl': 5, 'zczc': 2, 'dvpt': 3, 'lfqf': 4, 'humn': 5, 'ljgn': 2, 'sllz': 4,
#         'hmdt': 32}, {'root': ['pppw', '+', 'sjmn'], 'cczh': ['sllz', '+', 'lgvd'], 'ptdq': ['humn', '-', 'dvpt'], 
#         'sjmn': ['drzm', '*', 'dbpl'], 'pppw': ['cczh', '/', 'lfqf'], 'lgvd': ['ljgn', '*', 'ptdq'],
#         'drzm': ['hmdt', '-', 'zczc']})