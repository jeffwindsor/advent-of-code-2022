import re
from functools import reduce 

def sensor_beacons(filename):
    split_on = 'Sensor at x=|, y=|: closest beacon is at x='
    parse_line = lambda row: [int(c) for c in re.split(split_on, row.strip()) if c != '']
    return [parse_line(row) for row in open(filename, 'r').readlines()]

def distances(sensor_beacons): 
    return [[sx,sy,abs(sx - bx) + abs(sy - by)] for sx,sy,bx,by in sensor_beacons]

def beacons(sensor_beacons): 
    return [[bx,by] for _,_,bx,by in sensor_beacons]

def sensored(y, sx, sy, d):
    dx = d - abs(sy - y)
    return [] if dx < 0 else [sx - dx, sx + dx]

def merge_segment(a1,a2,b1,b2): 
    return [[min(a1,b1), max(a2,b2)]] if (a2 + 1) >= b1 else [[a1,a2],[b1,b2]]

def merge_segments(segments):
    f = lambda acc, s: acc[:-1] + merge_segment(*acc[-1], *s)
    ss = sorted(s for s in segments if s)
    return ss if len(ss) < 2 else reduce(f, ss[1:], [ss[0]])

def points_by_y(points): 
    result = {}
    for x,y in points:
        if y not in result: result[y] = set()
        result[y].add(x)
    return result 

def point_count_inclusive(start, end): 
    return abs(start - end) + 1

def between_inclusive(value, start, end): 
    return start <= value and value <= end

def part1(scan_line, sensor_beacons):  
    sensor_distances  = distances(sensor_beacons)
    beacons_by_y      = points_by_y(beacons(sensor_beacons))

    scanline_sensored = merge_segments([sensored(scan_line, *sd) for sd in sensor_distances])
    scanline_beacons  = beacons_by_y[scan_line]
    
    sensored_points   = sum([point_count_inclusive(*s) for s in scanline_sensored])
    sensored_beacons  = sum([between_inclusive(b, *s) for s in scanline_sensored for b in scanline_beacons]) 
    return sensored_points - sensored_beacons

def part2(sensor_beacons):
    sensor_distances  = distances(sensor_beacons)
    beacons_by_y      = points_by_y(beacons(sensor_beacons))

    for scan_line in range(4_000_000, 0, -1):
        bs = [[]] if scan_line not in beacons_by_y else [[bx, scan_line] for bx in beacons_by_y[scan_line]]
        ss = [sensored(scan_line, *sd) for sd in sensor_distances]
        ms = merge_segments(ss + bs)
        if len(ms) > 1: 
            x = ms[0][1] + 1
            return (4000000 * x) + scan_line

# tests ###############################################################################################################
examples = sensor_beacons('./examples/15')
assert examples == [  
    [2, 18, -2, 15], [9, 16, 10, 16], [13, 2, 15, 3], [12, 14, 10, 16], [10, 20, 10, 16], [14, 17, 10, 16], [8, 7, 2, 10], 
    [2, 0, 2, 10], [0, 11, 2, 10], [20, 14, 25, 17], [17, 20, 21, 22], [16, 7, 15, 3], [14, 3, 15, 3], [20, 1, 15, 3]], \
    'parse file check against example file'

assert distances([(0, 0,  5,  5)]) == [[0, 0, 10]]
assert distances([(0, 0, -5,  5)]) == [[0, 0, 10]]
assert distances([(0, 0,  5, -5)]) == [[0, 0, 10]]
assert distances([(0, 0, -5, -5)]) == [[0, 0, 10]]

assert distances(examples) == [
    [2, 18, 7], [9, 16, 1],  [13, 2, 3],  [12, 14, 4], [10, 20, 4], [14, 17, 5], [8, 7, 9], [2, 0, 10], 
    [0, 11, 3], [20, 14, 8], [17, 20, 6], [16, 7, 5],  [14, 3, 1], [20, 1, 7]], \
    'check against example file'

assert beacons(examples) == [  
    [-2, 15],  [10, 16], [15, 3], [10, 16], [10, 16], [10, 16], [2, 10], 
    [2, 10],  [2, 10], [25, 17], [21, 22], [15, 3], [15, 3], [15, 3]], \
    'extract beacon coordinates'

assert sensored(100, 0, 0, 10)  == [], 'above'
assert sensored(-100, 0, 0, 10) == [], 'below'
assert sensored(10, 0, 0, 10)   == [0,0], 'top'
assert sensored(-10, 0, 0, 10)  == [0,0], 'bottom'
assert sensored(0, 0, 0, 10)    == [-10,10], 'middle'

assert merge_segment(0,5,1,6)  == [[0,6]], 'overlap'
assert merge_segment(0,5,6,8)  == [[0,8]], 'next to'
assert merge_segment(1,6,2,5)  == [[1,6]], 'inside'
assert merge_segment(0,7,1,6)  == [[0,7]], 'wraps'
assert merge_segment(0,7,0,7)  == [[0,7]], 'equal'
assert merge_segment(0,5,7,10) == [[0,5],[7,10]], 'no overlap'
assert merge_segments([ [10,12], [], [8, 8], [2, 7], [-2, 2], [11,15]]) == [[-2,8], [10,15]]
assert merge_segments([[],[]]) == []
assert merge_segments([[0,1],]) == [[0,1]]

assert points_by_y([[-2, 15],  [10, 16], [15, 3], [10, 16], [10, 16], [10, 16], [2, 10], 
    [2, 10],  [2, 10], [25, 17], [21, 22], [15, 3], [15, 3], [15, 16]]) == {
    15: {-2}, 16: {10, 15}, 3: {15}, 10: {2}, 17: {25}, 22: {21}}, \
    'only points with y are returned no dups'

assert point_count_inclusive(0,0) == 1 
assert point_count_inclusive(-1,2) == 4

assert between_inclusive(0,  0,    0) == True 
assert between_inclusive(0, -1,    2) == True
assert between_inclusive(0, 10,   15) == False
assert between_inclusive(0, -15, -10) == False

assert part1(10, examples) == 26, 'example'

# answers ###############################################################################################################
actuals = sensor_beacons('./inputs/15')
print('Part 1: ', part1(2_000_000, actuals))
print('Part 2: ', part2(actuals))