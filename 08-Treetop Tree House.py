from functools import reduce

# raw input string
def read_inputs(filename): 
    with open(filename) as file: 
        return file.read().strip()

# returns (max row, max col, and points (r,c) mapped to height of tree)
def parse(inputs):
    result = {}
    for r, row in enumerate(inputs.split('\n')):
        for c, col in enumerate(row):
            result[(r,c)] = int(col)
    return (r,c,result)

# trees in 4 directions in order from tree at (row,col)
def views(row, col, max_row, max_col, location_heights):
    left  = reversed([location_heights[(row,c)] for c in range(0, col)])
    up    = reversed([location_heights[(r,col)] for r in range(0, row)])
    down  = [location_heights[(r,col)] for r in range(row + 1, max_row + 1)]
    right = [location_heights[(row,c)] for c in range(col + 1, max_col + 1)]
    return [left, right, up, down]
    
def on_edge(row, col, max_row, max_col): 
    return row == 0 or col == 0 or row == max_row or col == max_col

def edge_visible(row, col, max_row, max_col, location_heights):
    height = location_heights[(row,col)]
    vs = views(row, col, max_row, max_col, location_heights)
    return reduce(lambda acc,v: acc or v, [ max(sl) < height for sl in vs])

def view_count(height, location_heights):
    result = 0
    for h in location_heights:
        result += 1
        if h >= height: break
    return result

# number of trees in line of sight
def scenic_score(row, col, max_row, max_col, location_heights):
    height = location_heights[(row,col)]
    vs = views(row, col, max_row, max_col, location_heights)
    visible_trees = [view_count(height, location_heights) for location_heights in vs]
    return reduce(lambda acc,v: acc * v, visible_trees)
    

# count number of visible trees: those on the edge plus those with no line of sight 
def part1(filename):
    max_row, max_col, location_heights = parse(read_inputs(filename))
    locations = location_heights.keys()
    all_visible_locations = [ 
        on_edge(r, c, max_row, max_col) 
        or edge_visible(r, c, max_row, max_col, location_heights)
        for r,c in locations]
    return sum(all_visible_locations)

def part2(filename):
    max_row, max_col, location_heights = parse(read_inputs(filename))
    locations = location_heights.keys()
    all_scenic_scores = [
        scenic_score(r, c, max_row, max_col, location_heights) 
        for r,c in locations]
    return max(all_scenic_scores)
    
#tests
max_row,max_col,location_heights = parse(read_inputs('08-example.txt'))
assert edge_visible(1,1,max_row,max_col,location_heights) == True, 'top-left 5 is visible'
assert edge_visible(1,2,max_row,max_col,location_heights) == True, 'top-middle 5 is visible'
assert edge_visible(1,3,max_row,max_col,location_heights) == False, 'top-right 1 is not visible'
assert edge_visible(2,1,max_row,max_col,location_heights) == True, 'left-middle 5 is visible'

assert part1('08-example.txt') == 21

assert scenic_score(1,2,max_row,max_col,location_heights) == 4, ''
assert scenic_score(3,2,max_row,max_col,location_heights) == 8, ''
assert part2('08-example.txt') == 8

# answers
print(f'Part 1: {part1("08.txt")}')
print(f'Part 2: {part2("08.txt")}')