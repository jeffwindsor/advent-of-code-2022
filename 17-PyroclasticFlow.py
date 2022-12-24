#https://adventofcode.com/2022/day/17
# rock if moved left  = `<<`
# rock if moved right = `>>`
# test moved rock with: rock `&` cavern, 0 == pass, anything else is a fail / collision
# merge moved rock with: rock `|` cavern, result replaces cavern 

# rock array with integers represent rocks occupied pieces
# falling_rock = lower left corner coordiant 
# chamber = array that grows

from functools import reduce
from itertools import cycle
# from collections import deque

RIGHT, LEFT = '>', '<'
empty = 0b000000000
wall = 0b100000001
bottom = 0b111111111
shapes = [[0b000111100],
          [0b000010000,
           0b000111000,
           0b000010000],
          [0b000001000,
           0b000001000,
           0b000111000],
          [0b000100000,
           0b000100000,
           0b000100000,
           0b000100000],
          [0b000110000,
           0b000110000]]


def input(filename):
    return open(filename, 'r').read()


def overlaps(xs, ys):
    return [x & y != 0 for x, y in zip(xs, ys)]


def fire_jet(rock, chamber, direction):
    moved = [rock_row >> 1 if direction == RIGHT else rock_row << 1
             for rock_row in rock]
    return rock if any(overlaps(moved, chamber)) else moved


def merge(rock, chamber, index):
    # add rock to chamber
    for ir, r in enumerate(rock):
        chamber[index + ir] = r | chamber[index + ir]
    # remove any walls above top rock
    for i, c in enumerate(chamber):
        if c != wall:
            return chamber[i:]


def drop_rock(rock, chamber, jets):
    rl = len(rock)
    # extend walls up to rock which is 3 above highest point
    chamber = [wall for i in range(3 + rl)] + chamber
    i = 0
    while True:
        rock = fire_jet(rock, chamber[i:i + rl], next(jets))
        # test dropping to next level is without overlaps, if not merge rock to chamber
        if any(overlaps(rock, chamber[i + 1:i + rl + 1])):
            return merge(rock, chamber, i)
        i += 1


def height(rock_count_limit, input):
    jets, rocks, chamber = cycle(input), cycle(shapes), [bottom]
    rock_count = 0
    while rock_count < rock_count_limit:
        chamber = drop_rock(next(rocks), chamber, jets)
        rock_count += 1
    # return height of chamber, dont forget to remove the floor
    return len(chamber) - 1


examples = input('./examples/17')
actuals = input('./inputs/17')

print('Part1: ', height(2022, actuals))
# print('Part1: ', height(2022,actuals))


# tests ###########################################################################################
def test_reading_input():
    assert examples == '>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>'


def test_jet_pushes_rock_one_space_right():
    assert fire_jet([0b000010000], [wall], RIGHT) == [0b000001000]


def test_jet_pushes_rock_one_space_left():
    assert fire_jet([0b000010000], [wall], LEFT) == [0b000100000]


def test_jet_cannot_push_rock_into_occupied_space_right():
    assert fire_jet([0b000000010], [wall], RIGHT) == [0b000000010]


def test_jet_cannot_push_rock_into_occupied_space_left():
    assert fire_jet([0b010000000], [wall], LEFT) == [0b010000000]


def test_merge_adds_rock_to_chamber(): 
    assert merge(shapes[1], [wall for i in range(3)], 0) == [
        0b100010001, 
        0b100111001, 
        0b100010001]


def test_merge_removes_top_walls():
    assert merge(shapes[1], [wall for i in range(6)], 2) == [
        0b100010001,
        0b100111001,
        0b100010001,
        wall]


def test_rocks_stop_dropping_at_floor():
    assert drop_rock(shapes[0], [bottom], iter('>>><')) == [
        0b100111101,
        bottom]


def test_rocks_can_tuck_under():
    assert drop_rock(shapes[1], [
        0b111110001,
        wall,
        wall,
        bottom
    ], iter('>>>>>><')) == [
        0b111111001,
        0b100011101,
        0b100001001,
        bottom]


def test_dropping_rocks():
    assert height(2022, examples) == 3068

# def test_dropping_rocks2(): assert height(1000000000000,examples) == 1514285714288