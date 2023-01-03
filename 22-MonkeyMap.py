#!/usr/bin/env python
import re
from enum import Enum

def parse_inputs(filename):
    board, moves = open(filename,'r').read().split('\n\n')
    board = board.splitlines()
    moves = [m for m in re.split(r'(\d+)', moves) if m]
    return board, moves

TILE,WALL = '.','#'
class Direction(Enum): RIGHT=0;DOWN=1;LEFT=2;UP=3 # = 0,1,2,3
ROW_START, COL_START,DIRECTION_START = 1,1,Direction(Direction.RIGHT)

def move(row, col, direction, number_of_tiles, board):
    l = len(board[row])
    match direction:
        case Direction.LEFT: pass
        case Direction.RIGHT: pass
        case Direction.UP: pass
        case Direction.DOWN: pass    

def rotate(row,col,current_direction,rotating):
    match rotating:
        case 'L': return (row,col,Direction((current_direction.value - 1) % 4))
        case 'R': return (row,col,Direction((current_direction.value + 1) % 4))

def score(row, col, direction): 
    return (1000 * (row + ROW_START)) + (4 * (col + COL_START)) + direction.value

def part1(board, moves):
    me = find_starting_place(board)
    for m in moves:
        me = rotate(*me,m) if m.isnumeric() else move(*me,m,board)


examples = parse_inputs('examples/22')
# tests ===========================================================================================
def test_parse_inputs(): assert examples == (
    ['        ...#', '        .#..', '        #...', '        ....', '...#.......#', '........#...',
     '..#....#....', '..........#.', '        ...#....', '        .....#..', '        .#......', 
     '        ......#.'],
    ['10', 'R', '5', 'L', '5', 'R', '10', 'L', '4', 'R', '5', 'L', '5']
)
def test_rotate_left(): assert (0,0,Direction.UP) == rotate(0,0,Direction.RIGHT,'L') 
def test_rotate_right(): assert (0,0,Direction.RIGHT) == rotate(0,0,Direction.UP,'R')
def test_move_right_wraps_around_and_skips_spaces(): assert (0,7,Direction.RIGHT) == move(*(0,2,Direction.RIGHT),9,[['  ....']])
def test_move_left_wraps_around_and_skips_spaces(): assert (0,9,Direction.LEFT) == move(*(0,2,Direction.LEFT),9,[['  ....']]) 