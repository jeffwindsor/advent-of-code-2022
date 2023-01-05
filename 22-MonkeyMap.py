#!/usr/bin/env python

from re import split
from enum import Enum

def parse_inputs(filename):
    board, moves = open(filename,'r').read().split('\n\n')

    #split board into rows (padded with spaces to max row length, so our indexes work later)
    board = board.splitlines()
    max_col = max([len(row) for row in board])
    board = [row.ljust(max_col,' ') for row in board]

    moves = [m for m in split(r'(\d+)', moves) if m]
    return board, moves

class Direction(Enum): 
    RIGHT = 0
    DOWN  = 1
    LEFT  = 2
    UP    = 3

def step_function(direction, board):
    max_row, max_col = len(board), len(board[0])
    match direction:
        case Direction.RIGHT:   return lambda r,c: (r, (c + 1) % max_col)
        case Direction.DOWN:    return lambda r,c: ((r + 1) % max_row, c)
        case Direction.LEFT:    return lambda r,c: (r, (c - 1) % max_col)    
        case Direction.UP:      return lambda r,c: ((r - 1) % max_row, c)
        case _ : raise Exception(f'Unknown Direction: {direction}') 

def move(row, col, direction, number_of_tiles, board):
    step = step_function(direction, board)
    for _ in range(number_of_tiles):
        row_next, col_next = step(row, col)
        while True:
            match board[row_next][col_next]:
                case '.': row,col = row_next,col_next; break;
                case '#': break
                case ' ': row_next,col_next = step(row_next,col_next)
    return (row,col,direction)

def rotate(row,col,current_direction,rotating):
    new_direction = (current_direction.value + (-1 if rotating == 'L' else 1)) % 4
    return (row, col, Direction(new_direction))

def score(row, col, direction): 
    return (1000 * (row + 1)) + (4 * (col + 1)) + direction.value

def part1(board, moves):
    me = (0, board[0].index('.'), Direction.RIGHT)
    #print(f'Board: {len(board)} rows and {len(board[0])} cols') 
    #print('Start: ',me)
    for m in moves:
        me = move(*me, int(m), board) if m.isnumeric() else rotate(*me, m)
        #print('Move: ',m,me)
    #print('End: ',me)
    return score(*me)


examples = parse_inputs('examples/22')
inputs = parse_inputs('inputs/22')

print('Part 1: ', part1(*inputs))

# tests ===========================================================================================
def test_parse_inputs(): assert examples == (
    ['        ...#', '        .#..', '        #...', '        ....', '...#.......#', '........#...',
     '..#....#....', '..........#.', '        ...#....', '        .....#..', '        .#......', 
     '        ......#.'],
    ['10', 'R', '5', 'L', '5', 'R', '10', 'L', '4', 'R', '5', 'L', '5']
)
def test_rotate_left(): assert (0,0,Direction.UP) == rotate(0,0,Direction.RIGHT,'L') 
def test_rotate_right(): assert (0,0,Direction.RIGHT) == rotate(0,0,Direction.UP,'R')
def test_move_right_wraps_around_and_skips_spaces(): assert (0,3,Direction.RIGHT) == move(*(0,2,Direction.RIGHT),9,['  ....'])
def test_move_left_wraps_around_and_skips_spaces(): assert (0,5,Direction.LEFT) == move(*(0,2,Direction.LEFT),9,['  ....']) 
def test_move_right_stops_at_wall(): assert (0,5,Direction.RIGHT) == move(*(0,3,Direction.RIGHT),9,['  #...'])
def test_move_left_stops_at_wall(): assert (0,4,Direction.LEFT) == move(*(0,2,Direction.LEFT),9,['  .#..']) 

def test_part1_example(): assert 6032 == part1(*examples)
