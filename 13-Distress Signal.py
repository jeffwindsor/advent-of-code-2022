from itertools import chain
from math import prod

inputs = lambda filename: [[ eval(l) for l in b.split('\n')] 
                                     for b in open(filename, 'r').read().split('\n\n')]
examples = inputs('13-example.txt')
actuals = inputs('13.txt')

def compare(l, r):
    match l, r:
        case int(), int():  return l - r                 # rule 1: ordered (-), even 0, non-ordered (+)
        case list(), list():
            for pair in zip(l, r):                       # rule 2.a: compare integers, return if ordered (-) or non-ordered (+)
                result = compare(*pair)
                if result != 0: return result
            return len(l) - len(r)                       # rule 2.b: ordered (-), even 0, non-ordered (+)
        case int(), list(): return compare([l], r)       # rule 3 left
        case list(), int(): return compare(l, [r])       # rule 3 right

flatten  = chain.from_iterable
dividers = [[[2]],[[6]]]
index_of = lambda ps, x: sum(compare(p, x) <= 0 for p in ps)

part1 = lambda ps: sum(i for i, pair in enumerate(ps, 1) if compare(*pair) < 0)
part2 = lambda ps, ds: prod(index_of(flatten(ps + ds), d) for d in ds)

print('Part 1: ', part1(actuals))
print('Part 2: ', part2(actuals, dividers))
