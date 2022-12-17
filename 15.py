# https://adventofcode.com/2022/day/15
# each sensor has an origin and a Manhattan distance (from origin to closest beacon)
# thus we know that there is no beacon between that sensor and any other point with a Manhattan distance <= above
import re
from functools import reduce 

split_on = 'Sensor at x=|, y=|: closest beacon is at x='

def parse(filename):
    parse_line = lambda row: [int(c) for c in re.split(split_on, row.strip()) if c != '']
    return [parse_line(row) for row in open(filename, 'r').readlines()]

example = parse('15example.txt')
actual  = parse('15.txt')


def sensor_scan_distances(sensor_beacon_pairs):
    manhatten_distance = lambda x1, y1, x2, y2: abs(x1 - x2) + abs(y1 - y2)
    return [(a, b, manhatten_distance(a, b, c, d)) for a, b, c, d in sensor_beacon_pairs]

def merge_segments(a1,a2,b1,b2):
    if a2 >= b1 : return [[min(a1,b1), max(a2,b2)]]   # assumes sorted points
    return[[a1,a2],[b1,b2]] # no interaction

def intersecting_segment(x1, y1, distance, y2):
    diff = distance - abs(y1 - y2)
    return sorted([x1 - diff, x1 + diff])

def intersecting_segments(scan_line, sensor_dists):
    def reducer(acc, segment):
        ms = merge_segments(*acc[-1], *segment)
        return acc[:-1] + ms

    all_segments = sorted([intersecting_segment(x, y, d, scan_line) for x, y, d in sensor_dists])
    return reduce(reducer, all_segments[1:], [all_segments[0]])

def segment_point_count(one,two):
    return abs(one - two) + 1

def beacons_by_row(row, sensor_beacon_pairs):
    return set([bx for _,_,bx,by in sensor_beacon_pairs if row == by])

def beacon_in_segment(b, s1, s2):
    return s1 <= b and b <= s2

def beacons_in_segment(beacons, s1, s2):
    return sum([beacon_in_segment(b,s1,s2) for b in beacons])

def part1(row, sensor_beacon_pairs):
    bbrs = beacons_by_row(row, sensor_beacon_pairs)
    iss  = intersecting_segments(row, sensor_scan_distances(sensor_beacon_pairs))
    #dont count beacons
    point_count  = sum([segment_point_count(*s) for s in iss])
    beacon_count = sum([beacons_in_segment(bbrs, *s) for s in iss]) 
    print(point_count, beacon_count, bbrs)
    return point_count - beacon_count

# tests ###############################################################################################################
assert parse('15example.txt') == [  [2, 18, -2, 15], [9, 16, 10, 16], [13, 2, 15, 3], [12, 14, 10, 16], 
                                    [10, 20, 10, 16], [14, 17, 10, 16], [8, 7, 2, 10], [2, 0, 2, 10],  
                                    [0, 11, 2, 10],   [20, 14, 25, 17], [17, 20, 21, 22], [16, 7, 15, 3],  
                                    [14, 3, 15, 3], [20, 1, 15, 3]], 'parse file check against example file'

assert sensor_scan_distances([(0,0, 5, 5),(0,0,-5, 5),(0,0,-5,-5),(0,0, 5,-5)]) == [(0, 0, 10), (0, 0, 10), (0, 0, 10), 
                                                        (0, 0, 10)], 'sensor_scan_distance check for all 4 quadrents'

assert sensor_scan_distances(example) == [(2, 18, 7), (9, 16, 1),  (13, 2, 3),  (12, 14, 4), (10, 20, 4), (14, 17, 5), (8, 7, 9), (2, 0, 10), 
                              (0, 11, 3), (20, 14, 8), (17, 20, 6), (16, 7, 5),  (14, 3, 1),  
                              (20, 1, 7)], 'sensor_scan_distance check against example file'

assert merge_segments(0,5,1,6) == [[0,6]], 'overlap to right'
assert merge_segments(1,6,0,5) == [[0,6]], 'overlap to left'
assert merge_segments(2,5,1,6) == [[1,6]], 'inside'
assert merge_segments(0,7,1,6) == [[0,7]], 'wraps'
assert merge_segments(0,5,7,10) == [[0,5],[7,10]], 'no overlap'

assert intersecting_segments(10, [(8, 7, 9)]) == [[2,14]], 'already_scanned_segment example check for sensor at 8,7'
assert intersecting_segments(10,sensor_scan_distances(example)) == [[-2, 24]], 'example scan row'
assert part1(10, example) == 26, 'part 1 example answer'

# answers #############################################################################################################
print('Part 1: ', part1(2000000, actual))

