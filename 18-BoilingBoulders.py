#https:/entofcode.com/2022/day/18
from collections import deque
from functools import reduce

def parse_file(filename):
    return set([ tuple([int(c) 
                    for c in l.split(',')]) 
                    for l in open(filename,'r').readlines()])
max_width = 100
examples = parse_file('examples/18')
inputs   = parse_file('inputs/18')

def neighbors(x,y,z): 
    return [(x+1,y,z),(x-1,y,z),
            (x,y+1,z),(x,y-1,z),
            (x,y,z+1),(x,y,z-1)]

def count_exposed_sides(points):
    empty_neighbors_per_point = (sum(n not in points for n in neighbors(*p)) for p in points)
    return sum(empty_neighbors_per_point)

def bound_ranges(points):
    minmax = lambda nx,mx,ny,my,nz,mz,x,y,z: (min(nx,x), max(mx,x), min(ny,y), max(my,y), min(nz,z), max(mz,z))
    nx,mx,ny,my,nz,mz = reduce(lambda acc,p: minmax(*acc,*p), points, (max_width,-max_width,max_width,-max_width,max_width,-max_width))
    return (nx-1,mx+1,ny-1,my+1,nz-1,mz+1)

def is_inbounds(nx,xx,ny,xy,nz,xz):
    return lambda x,y,z: nx <= x and x <= xx and ny <= y and y <= xy and nz <= z and z <= xz            

def define_bounds(points):
    nx,xx,ny,xy,nz,xz = bound_ranges(points)
    all_points = set([(x,y,z) for x in range(nx,xx + 1) for y in range(ny, xy + 1) for z in range(nz, xz + 1)]) 
    return all_points, is_inbounds(nx,xx,ny,xy,nz,xz)

def count_external_sides(points):
    all_points, is_inbounds = define_bounds(points)
    visited = set()
    d = deque([(0,0,0)])    #outside sphere point
    while(d):
        p = d.popleft()
        if p in visited: continue
        
        visited.add(p)
        if p in points: continue        
        
        d.extend(n for n in neighbors(*p) if is_inbounds(*n) and n not in visited)

    return count_exposed_sides(all_points - (visited - points))


# tests ###############################################################
def test_inputs(): assert examples == {(2,2,2), (1,2,2), (3,2,2), (2,1,2), (2,3,2), (2,2,1), (2,2,3), (2,2,4), (2,2,6), (1,2,5), (3,2,5), (2,1,5), (2,3,5)}
def test_count_exposed_sides(): assert count_exposed_sides(examples) == 64
def test_count_external_sides(): assert count_external_sides(examples) == 58

# answers #############################################################
print('Part 1: ', count_exposed_sides(inputs))
print('Part 2: ', count_external_sides(inputs))

