from math import lcm
## data #####################################################################################
def parse_operation_line(l): 
    match l[len('  Operation: new = old '):].split(' '):
        case ['*','old']: return lambda v: v * v
        case ['*', x]:    return lambda v: v * int(x)
        case ['+', x]:    return lambda v: v + int(x)

parse_block = lambda ls: [
        [int(i) for i in ls[1][len('  Starting items: '):].split(', ')],
        parse_operation_line(ls[2]),
        int(ls[3][len('  Test: divisible by '):]),
        int(ls[4][len('    If true: throw to monkey '):]),
        int(ls[5][len('    If false: throw to monkey '):]),
        0]
parse = lambda filename: [ parse_block(block.splitlines()) for block in open(filename).read().split('\n\n')]
examples = lambda: parse('./examples/11')
actuals  = lambda: parse('./inputs/11')

## functions #####################################################################################
worry_relief = lambda w: w//3
no_relief = lambda w : w

def run_rounds(rounds, worry_adjustment, monkies):
    value_lcm = lcm(*[monkey[2] for monkey in monkies])
    for r in range(rounds):
        for monkey in monkies:
            items, inspect, test_modulo, test_true, test_false = monkey[0], monkey[1], monkey[2], monkey[3], monkey[4]
            for item in items:
                value = worry_adjustment( inspect(item) % value_lcm )
                to_monkey = test_true if value % test_modulo == 0 else test_false
                monkies[to_monkey][0].append(value)
            monkey[5] += len(items)
            monkey[0] = [] 
    return monkies

def answer(n, worry_func, monkies):
    sorted_counts = sorted([ m[5] for m in run_rounds(n, worry_func, monkies)])
    return sorted_counts[-1] * sorted_counts[-2]

part1 = lambda ms: answer(20, worry_relief, ms)
part2 = lambda ms: answer(10000, no_relief, ms)


## tests #####################################################################################
#import cProfile
#cProfile.run('answer(1000, no_relief, examples())')
assert [ m[0] for m in run_rounds( 1, worry_relief, examples())]  == [[20, 23, 27, 26], [2080, 25, 167, 207, 401, 1046], [], []]
assert [ m[0] for m in run_rounds(20, worry_relief, examples())]  == [[10, 12, 14, 26, 34], [245, 93, 53, 199, 115], [], []]

assert answer(   20, worry_relief, examples()) == 10605
assert answer(    1, no_relief,    examples()) == 6 * 4
assert answer(   20, no_relief,    examples()) == 103 * 99
assert answer( 1000, no_relief,    examples()) == 5192 * 5204
assert answer(10000, no_relief,    examples()) == 52166 * 52013

## answers #####################################################################################
print(f'Part 1: {part1(actuals())}')
print(f'Part 1: {part2(actuals())}')

