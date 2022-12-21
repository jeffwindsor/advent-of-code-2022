def parse(filename):
    data = open(filename).read().strip()
    sensors, beacons = set(), set()
    for line in data.split("\n"):
        parts = line.split()
        sx, sy = int(parts[2][2:-1]), int(parts[3][2:-1])
        bx, by = int(parts[8][2:-1]), int(parts[9][2:])
        d = abs(sx - bx) + abs(sy - by)
        sensors.add((sx, sy, d))
        beacons.add((bx, by))
    return sensors, beacons

examples = parse("15example.txt")
actuals = parse("15.txt")


def possible(x, y, sensors, beacons):
    for sx, sy, d in sensors:
        if abs(x - sx) + abs(y - sy) <= d and (x, y) not in beacons:
            return False
    return True

def p1(y, sensors, beacons):
    ct = 0
    print('range: ', min(x-d for x, _, d in sensors), max(x+d for x, _, d in sensors))
    for x in range(min(x-d for x, _, d in sensors), max(x+d for x, _, d in sensors)):
        if not possible(x, y, sensors, beacons) and (x, y) not in beacons:
            ct += 1
    return ct

def p2():
    for sx, sy, d in sensors:
        for dx in range(d + 2):
            dy = (d + 1) - dx
            for mx, my in [(-1, 1), (1, -1), (-1, -1), (1, 1)]:
                x, y = sx + (dx * mx), sy + (dy * my)
                if not(0 <= 4_000_000 and 0<=y<=4_000_000):
                    continue
                if possible(x, y):
                    return x * 4_000_000 + y

####################################################################################
import re
from functools import reduce 
def parserx(filename):
    split_on = 'Sensor at x=|, y=|: closest beacon is at x='
    parse_line = lambda row: [int(c) for c in re.split(split_on, row.strip()) if c != '']
    return [parse_line(row) for row in open(filename, 'r').readlines()]
example, actual = parserx('15example.txt'), parserx('15.txt')

def sensor_scan_distances(sensor_beacon_pairs):
    manhatten_distance = lambda x1, y1, x2, y2: abs(x1 - x2) + abs(y1 - y2)
    return [(a, b, manhatten_distance(a, b, c, d)) for a, b, c, d in sensor_beacon_pairs]

def merge(a1,a2,b1,b2):
    if a2 >= b1 : return [[min(a1,b1), max(a2,b2)]]   # assumes sorted points
    return[[a1,a2],[b1,b2]] # no interaction

def intersecting_segment(x1, y1, distance, y2):
    diff = distance - abs(y1 - y2)
    return sorted([x1 - diff, x1 + diff])

def intersecting_segments(scan_line, sensor_dists):
    return sorted([intersecting_segment(x, y, d, scan_line) for x, y, d in sensor_dists])

def merged_segments(segments):
    reducer = lambda acc, segment: acc[:-1] + merge(*acc[-1], *segment)
    return reduce(reducer, segments[1:], [segments[0]])

def beacons_by_row(row, sensor_beacon_pairs):
    return set([bx for _,_,bx,by in sensor_beacon_pairs if row == by])

def beacon_in_segment(b, s1, s2):
    return s1 <= b and b <= s2

def beacons_in_segment(beacons, s1, s2):
    return sum([beacon_in_segment(b,s1,s2) for b in beacons])

def part1(row, sensor_beacon_pairs):
    bbrs = beacons_by_row(row, sensor_beacon_pairs)
    iss  = intersecting_segments(row, sensor_scan_distances(sensor_beacon_pairs))
    ms   = merged_segments(iss)
    point_count  = sum([abs(a - b) + 1 for a,b in ms])
    beacon_count = sum([beacons_in_segment(bbrs, *s) for s in ms]) 
    #dont count beacons
    return point_count - beacon_count

####################################################################################
##[[-1_333_634, 4_922_594]] vs correct of [-518_660, 4_432_766]

#part1(2_000_000,actual) 

# points = p1(2_000_000,*actuals)
# segs = []
# current = [points[0], points[0]]
# for p in points[1:]:
#     if p == current[1] + 1:
#         current[1] = p
#     else:
#         segs += current
#         current = [p,p]
# segs += current
# print(segs)

print(f"Part 1: {p1(2_000_000,*actuals)}")  
# range:  -1234227 5594946
# Part 1: 4951427
#print(f"Part 2: {p2()}")