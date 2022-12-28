#!/usr/bin/env python3
#https://adventofcode.com/2022/day/20

def parse_file(filename):
    return [int(i) for i in open(filename, 'r').read().split('\n')]

# tests (pytest) ##############################################################
def test_parse_file(): assert parse_file('examples/20') == [1, 2, -3, 3, -2, 0, 4]
