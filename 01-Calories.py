# https://adventofcode.com/2022/day/1
def calories_per_elf(filename): return sorted([sum([int(x) 
    for x in l.split('\n')]) 
    for l in open(filename, 'r').read().split('\n\n')], reverse=True)

calories = calories_per_elf('01.txt')
print(f'Part 1: {calories[0]}')         
print(f'Part 2: {sum(calories[:3])}')