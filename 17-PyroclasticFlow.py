#https://adventofcode.com/2022/day/17
from functools import reduce 

RIGHT, LEFT = '>', '<'
wall   =    0b100000001
bottom =    0b111111111
shapes =  [[0b000111100],
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

def is_valid(rock_row, chamber_row): 
    return rock_row & chamber_row == 0

def move_row(rock_row, direction):
    return rock_row >> 1 if direction == RIGHT else rock_row << 1

# move shape three times using walls, then start checking down
# keep moving one by one until contact down, then merge rows inside chamber, add rest
def move_rock(rock, chamber, direction):
    moved = [move_row(row, direction) for row in rock]
    # zip will truncate chamber, assuming chmaber will always be bigger and start with top
    valid = [is_valid(r,c) for r,c in zip(moved, chamber)]
    return moved if all(valid) else rock

def pre_moves(rock, directions):
    walls = [wall for i in range(len(rock))]
    for d in directions:
        rock = move_rock(rock,walls,d)
    return rock



def test_pre_moves_are_blocked0(): assert pre_moves(shapes[0],[RIGHT,RIGHT,RIGHT]) == [0b000011110]
def test_pre_moves_are_blocked1(): assert pre_moves(shapes[1],[RIGHT,RIGHT,RIGHT]) == [0b000000100,0b000001110,0b000000100]
def test_pre_moves_are_blocked2(): assert pre_moves(shapes[2],[RIGHT,RIGHT,RIGHT]) == [0b000000010,0b000000010,0b000001110]
def test_overlap_is_not_valid(): assert is_valid(0b000000011, 0b000000001) == False
def test_no_overlap_is_valid():  assert is_valid(0b100000000, 0b010000000) == True
def test_move_row_right_one_space(): assert move_row(0b000010000, RIGHT) == 0b000001000
def test_move_row_left_one_space():  assert move_row(0b000010000, LEFT) == 0b000100000
# def test_move_right(): assert False
# def test_move_right(): assert False
# def test_move_right(): assert False
# def test_move_right(): assert False
# def test_move_right(): assert False


# rock if moved left  = `<<`
# rock if moved right = `>>`
# test moved rock with: rock `&` cavern, 0 == pass, anything else is a fail / collision
# merge moved rock with: rock `|` cavern, result replaces cavern 

# rock array with integers represent rocks occupied pieces
# falling_rock = lower left corner coordiant 
# chamber = array that grows