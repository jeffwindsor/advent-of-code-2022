from collections import deque

def parse(filename):
    lines = [ l.strip() for l in open(filename, 'r').readlines()]
    rows, cols = len(lines), len(lines[0])
    start_point, end_point = (0,0), (0,0)
    for r in range(rows):
        for c in range(cols):
            if lines[r][c] == 'S': 
                start_point = (r,c)
                lines[r] = lines[r].replace('S','a')
            if lines[r][c] == 'E': 
                end_point = (r,c)
                lines[r] = lines[r].replace('E','z') 
    return [start_point, end_point, rows, cols, lines]

actual  = lambda row,col,rows,cols: 0 <= row and row < rows and 0 <= col and col < cols
allowed = lambda from_h, to_h: ord(to_h) -  ord(from_h) <= 1

def neighbors_from_heights(heights, rows, cols):   
    def inner(p):
        current = heights[p[0]][p[1]]
        cross_points   = [(p[0] + 1, p[1]), (p[0]-1, p[1]), (p[0], p[1] + 1), (p[0], p[1] - 1)]
        actual_points  = [(r,c) for r,c in cross_points if actual(r,c,rows,cols)]
        allowed_points = [(r,c) for r,c in actual_points if allowed(current, heights[r][c])]
        return allowed_points
    return inner

def dijkstras_shortest_path(neighbors, complete, start_point):
    visited,visit_queue = {}, deque()
    visit_queue.append((start_point,0))

    while len(visit_queue) > 0:
        p, steps = visit_queue.pop()
        if complete(p): return steps # reached dest
        if p in visited and visited[p] <= steps: continue # we found this already
        
        visited[p] = steps
        for np in neighbors(p):
            visit_queue.appendleft((np, steps+1))

    return 1000000000000

def part1(start_point, end, rows, cols, heights):
    complete = lambda point: point == end
    neighbors = neighbors_from_heights(heights, rows, cols)
    return dijkstras_shortest_path(neighbors, complete, start_point)

def part2(start_point, end_point, rows, cols, heights):
    list_of_as = []
    for row in range(rows):
        for col in range(cols):
            if heights[row][col] == 'a': list_of_as.append((row,col)) 

    return min([dijkstras_shortest_path(
        neighbors_from_heights(heights, rows, cols),
        lambda point: point == end_point,
        a_point) for a_point in list_of_as])

## data #######################################################################
examples = parse('./examples/12')
actuals  = parse('./inputs/12')

## test #######################################################################
start_point, end_point, rows, cols, heights = examples
nf = neighbors_from_heights(heights,rows,cols)
assert start_point == (0,0)
assert end_point == (2,5)
assert rows == 5
assert cols == 8
assert heights == ['aabqponm','abcryxxl','accszzxk','acctuvwj','abdefghi']
assert allowed('c','b') and allowed('c','c') and allowed('c','d')
assert allowed('c','e') == False
assert nf((0,0)) == [(1, 0), (0, 1)]
assert nf((1,0)) == [(2, 0), (0, 0), (1, 1)]
assert nf((1,1)) == [(2, 1), (0, 1), (1, 2), (1, 0)]
assert part1(*examples) == 31

## answers ####################################################################
print(f"Part 1: {part1(*actuals)}")
print(f"Part 2: {part2(*actuals)}")