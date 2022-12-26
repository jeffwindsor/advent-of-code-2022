#https://adventofcode.com/2022/day/18

# set points
# search for next to it

def parse_inputs(filename):
    return set([ tuple([int(c) for c in l.split(',')]) for l in open(filename,'r').readlines()])


examples = parse_inputs('examples/18')
actuals = parse_inputs('inputs/18')


def neighbors(x, y, z): 
    return [(x + 1, y, z),(x - 1, y, z),
            (x, y + 1, z),(x, y - 1, z),
            (x, y, z + 1),(x, y, z - 1)]


def count_sides_exposed_to_air(points):
    return sum([ sum([(n not in points) for n in neighbors(*p)]) 
                       for p in points] )



# answers #############################################################
print('Part 1: ', count_sides_exposed_to_air(actuals))


# tests ###############################################################
def test_answer(): assert answer(examples) == 64
def test_inputs(): assert examples == {
    (2,2,2),
    (1,2,2),
    (3,2,2),
    (2,1,2),
    (2,3,2),
    (2,2,1),
    (2,2,3),
    (2,2,4),
    (2,2,6),
    (1,2,5),
    (3,2,5),
    (2,1,5),
    (2,3,5)}