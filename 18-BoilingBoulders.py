#https://adventofcode.com/2022/day/18
from collections import deque
from functools import reduce
# set points
# search for next to it

def parse_inputs(filename):
    return set([ tuple([int(c) for c in l.split(',')]) for l in open(filename,'r').readlines()])


examples = parse_inputs('examples/18')
actuals = parse_inputs('inputs/18')


def neighbors(x, y, z): 
    return [(x + 1, y, z),(x - 1, y, z),
            (x, y + 1, z),(x, y - 1, z),
            (x, y, z + 1),(x, y, z - 1)]


def count_sides_exposed_to_air(points):
    return sum([ sum([(n not in points) for n in neighbors(*p)]) 
                       for p in points] )

def in_bounds(minx,maxx,miny,maxy,minz,maxz,x,y,z):
    return minx <= x and x <= maxx and miny <= y and y <= maxy and minz <= z and z <= maxz

def minmax(minx,maxx,miny,maxy,minz,maxz,x,y,z):
    return (min(minx,x) - 1 , max(maxx,x) + 1, min(miny,y) - 1, max(maxy,y) + 1, min(minz,z) - 1, max(maxz,z) + 1)
    
def count_external_sides(points):
    m = 10000000
    minx,maxx,miny,maxy,minz,maxz = reduce(lambda acc,p: minmax(*acc,*p), points, (m,-m,m,-m,m,-m))
        
    visited = set()
    
    d = deque()    #outside sphere point
    d.append((0,0,0))
    while(d):
        p = d.popleft()
        if p in visited: 
            continue
        
        visited.add(p)
        if p in points: 
            continue
        
        d.extend([(x,y,z) for x,y,z in neighbors(*p) if in_bounds(minx,maxx,miny,maxy,minz,maxz,x,y,z)])

    all_points = set([(x,y,z) for x in range(minx,maxx + 1) for y in range(miny, maxy + 1) for z in range(minz, maxz + 1)])
    filled = all_points - (visited - points)
    return count_sides_exposed_to_air(filled)

# answers #############################################################
print('Part 1: ', count_sides_exposed_to_air(actuals))


# tests ###############################################################
def test_count_external_sides(): assert count_external_sides(examples) == 58
def test_count_sides_exposed_to_air(): assert count_sides_exposed_to_air(examples) == 64

def test_inputs(): assert examples == {
    (2,2,2),
    (1,2,2),
    (3,2,2),
    (2,1,2),
    (2,3,2),
    (2,2,1),
    (2,2,3),
    (2,2,4),
    (2,2,6),
    (1,2,5),
    (3,2,5),
    (2,1,5),
    (2,3,5)}