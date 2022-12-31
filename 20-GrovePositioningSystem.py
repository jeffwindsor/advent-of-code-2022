#!/usr/bin/env python3
#https://adventofcode.com/2022/day/20
from itertools import cycle

class V:
    index:int
    value:int
    
    def __init__(self,i,v):
        self.index = i
        self.value = v
    
    # value comparison 
    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.value == other.value and self.index == other.index
        return False

    def __str__(self):
        return f'{self.index} {self.value}'
    
    
def parse_file(filename):
    return [int(v) for v in open(filename, 'r').read().split('\n')]

def move(start, number_of_places, max_index, vs):
    end = (start + number_of_places) % max_index
    if end == 0 and number_of_places < 0: end = max_index        #wtf special case
        
    step = 1 if start < end else -1
    for a in range(start, end, step):
        b = a + step 
        vs[a].index = b
        vs[b].index = a
        vs[a],vs[b] = vs[b],vs[a]

    return vs

def part1(values):
    indexed_values = [V(i,v) for i,v in enumerate(values)]
    results = indexed_values.copy()
    zero_value = indexed_values[values.index(0)]
    l = len(results)
    
    for v in indexed_values:
        move(v.index, v.value, l - 1, results)

    index = lambda n: ((n + zero_value.index + 1) % l) - 1
    return sum([results[index(1000)].value, results[index(2000)].value, results[index(3000)].value])

examples = parse_file('examples/20')
inputs = parse_file('inputs/20')

print('Part 1: ', part1(inputs))


# tests (pytest) ##############################################################
def test_example(): 
    assert part1( ) == 3 #[4,-3,2]
    
def test_parse_file(): 
    assert parse_file('examples/20') == [1, 2, -3, 3, -2, 0, 4]
    
def toV(vs): return [V(i,v) for i,v in enumerate(vs)]

# def test_move_1(): assert move(2,-3,toV([0,1,2,3,4])) == toV([0,1,2,3,4])

def test_example_move_1():
    assert move(0,1,6, toV([1, 2, -3, 3, -2, 0, 4]))  == toV([2, 1, -3, 3, -2, 0, 4])
    
def test_example_move_2():
    assert move(0,2,6, toV([2, 1, -3, 3, -2, 0, 4]))  == toV([1, -3, 2, 3, -2, 0, 4])
    
def test_example_move_3():
    assert move(1,-3,6, toV([1, -3, 2, 3, -2, 0, 4])) == toV([1, 2, 3, -2, -3, 0, 4])
    
def test_example_move_4():
    assert move(2,3,6, toV([1, 2, 3, -2, -3, 0, 4]))  == toV([1, 2, -2, -3, 0, 3, 4])
    
def test_example_move_5():
    assert move(2,-2,6, toV([1, 2, -2, -3, 0, 3, 4])) == toV([1, 2, -3, 0, 3, 4, -2])
    
def test_example_move_6():
    assert move(3,0,6, toV([1, 2, -3, 0, 3, 4, -2]))  == toV([1, 2, -3, 0, 3, 4, -2])
    
def test_example_move_7():
    assert move(5,4,6, toV([1, 2, -3, 0, 3, 4, -2]))  == toV([1, 2, -3, 4, 0, 3, -2])
       
