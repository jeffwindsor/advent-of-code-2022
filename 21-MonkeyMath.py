#!/usr/bin/env python3
#https://adventofcode.com/2022/day/21

import sympy

def parse_inputs(filename):
    return dict([l.strip().split(': ') for l in open(filename,'r').readlines()])

def substitute(children, nodes):
    match children.split(' '):
        case [lh, op, rh]: 
            slh = substitute(nodes[lh], nodes) if lh in nodes else lh
            srh = substitute(nodes[rh], nodes) if rh in nodes else rh
            return f'({slh} {op} {srh})'
        
        case [n]:
            return int(n)

def part1(nodes): 
    expression = substitute(nodes['root'], nodes).replace(' ','')
    return eval(expression)

def part2(nodes):
    del nodes['humn']
    root = nodes['root'].replace('+','-')
    expression = substitute(root, nodes).replace(' ','')
    solution = sympy.solve(expression, sympy.Symbol('humn'))
    return solution[0]

# answers #########################################################################################

print('Part 1e: ', part1(parse_inputs('examples/21')))
print('Part 2e: ', part2(parse_inputs('examples/21')))

print('Part 1i: ', part1(parse_inputs('inputs/21')))
print('Part 2i: ', part2(parse_inputs('inputs/21')))

# tests ###########################################################################################
def test_part1_example():
    assert part1(parse_inputs('examples/21')) == 152
    
def test_part2_example():
    assert part2(*parse_inputs('examples/21')) == 301
