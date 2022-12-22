import re
parse    = lambda filename: [re.split('-|,', l.strip()) for l in open(filename).read().splitlines()]
contains = lambda a1,a2,b1,b2: (a1 <= b1 and b2 <= a2) or (b1 <= a1 and a2 <= b2)
overlaps = lambda a1,a2,b1,b2: (a1 <= b1 <= a2) or (a1 <= b2 <= a2) or (b1 <= a1 <= b2) or (b1 <= a2 <= b2) 
part1    = lambda inputs: sum([contains(i[0],i[1],i[2],i[3]) for i in inputs])
part2    = lambda inputs: sum([overlaps(i[0],i[1],i[2],i[3]) for i in inputs])
actuals  = parse('./inputs/04')

print('Part 1: ', part1(actuals))
print('Part 2: ', part2(actuals))

##########################################################################
assert contains(1,4,2,3) == True, 'left'
assert contains(2,3,1,4) == True, 'right'
assert contains(1,4,1,4) == True, 'equal'
assert contains(1,4,2,5) == False, 'partial'
assert overlaps(2,4,1,2) == True and overlaps(1,2,2,4) == True, 'edge1'
assert overlaps(1,4,1,4) == True, 'equal'
assert overlaps(1,4,2,3) == True and overlaps(2,3,1,4) == True, 'envelops'
assert overlaps(1,2,3,4) == False and overlaps(3,4,1,2) == False, 'outside'