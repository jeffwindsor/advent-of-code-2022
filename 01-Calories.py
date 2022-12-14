# https://adventofcode.com/2022/day/1
def calories_per_elf(filename):
    return sorted([sum([int(x) for x in line.split('\n')])
                   for line in open(filename, 'r').read().split('\n\n')], reverse=True)


calories = calories_per_elf('./inputs/01')
print(f'Part 1: {calories[0]}')
print(f'Part 2: {sum(calories[:3])}')
