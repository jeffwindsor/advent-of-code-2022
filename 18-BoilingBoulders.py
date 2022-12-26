#https:/entofcode.com/2022/day/18
from collections import deque
from functools import reduce
# set ponts

# search for next to it

def parse_file(filename):
    return set([ tuple([int(c) 
                    for c in l.split(',')]) 
                    for l in open(filename,'r').readlines()])

examples = parse_file('examples/18')
inputs   = parse_file('inputs/18')


def neighbors(x, y, z): 
    return [(x + 1, y, z),(x - 1, y, z),
            (x, y + 1, z),(x, y - 1, z),
            (x, y, z + 1),(x, y, z - 1)]

def count_exposed_sides(points):
    return sum([sum([(n not in points) 
                for n in neighbors(*p)]) 
                for p in points] )

def define_bounds(points):
    mm = 1_000_000
    minmax = lambda nx,mx,ny,my,nz,mz,x,y,z:(min(nx,x)-1, max(mx,x)+1, min(ny,y)-1, max(my,y)+1, min(nz,z)-1, max(mz,z)+1)
    nx,xx,ny,xy,nz,xz = reduce(lambda acc,p: minmax(*acc,*p), points, (mm,-mm,mm,-mm,mm,-mm))
    all_points = set([(x,y,z) for x in range(nx,xx + 1) for y in range(ny, xy + 1) for z in range(nz, xz + 1)])
    is_inbounds = lambda x,y,z: nx <= x and x <= xx and ny <= y and y <= xy and nz <= z and z <= xz    
    return all_points, is_inbounds

def count_external_sides(points):
    all_points, is_inbounds = define_bounds(points)
    
    visited = set()
    d = deque([(0,0,0)])    #outside sphere point
    while(d):
        p = d.popleft()
        if p in visited: continue
        
        visited.add(p)
        if p in points: continue        
        
        d.extend(n for n in neighbors(*p) if is_inbounds(*n))

    filled = all_points - (visited - points)
    return count_exposed_sides(filled)

# answers #############################################################
print('Part 1: ', count_exposed_sides(inputs))
print('Part 2: ', count_external_sides(inputs))


# tests ###############################################################
def test_count_external_sides(): assert count_external_sides(examples) == 58
def test_count_exposed_sides(): assert count_exposed_sides(examples) == 64

def test_inputs(): assert examples == {(2,2,2), (1,2,2), (3,2,2), (2,1,2), (2,3,2), (2,2,1), (2,2,3), (2,2,4), (2,2,6), (1,2,5), (3,2,5), (2,1,5), (2,3,5)}
