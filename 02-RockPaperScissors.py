# https://adventofcode.com/2022/day/2
from functools import reduce

score  = lambda scores: (lambda acc,round: acc + scores[round])
part1 = score({ 'C X':7, 'A Y':8, 'B Z':9, 'A X':4, 'B Y':5, 'C Z':6, 'B X':1, 'C Y':2, 'A Z':3 })
part2 = score({ 'A X':3, 'B X':1, 'C X':2, 'A Y':4, 'B Y':5, 'C Y':6, 'A Z':8, 'B Z':9, 'C Z':7 })

rounds = [ line.strip() for line in open('./inputs/02','r').readlines() ]
print('Part 1: ', reduce(part1, rounds, 0))
print('Part 2: ', reduce(part2, rounds, 0))