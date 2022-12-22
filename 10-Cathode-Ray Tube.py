import itertools

def get_inputs(filename): 
    with open(filename) as file: input_text = file.read().strip()
    commands = [ line.split(' ') for line in input_text.split('\n') ]
    # convert 'noop' to 0, and 'addx n' to [0, n]
    add_to_x_by_cycle = [ [0] if c[0] == 'noop' else [0,int(c[1])] for c in commands]
    flattened = [x for xs in add_to_x_by_cycle for x in xs]
    return flattened

def accumulate_(initial, inputs):
    # accumulate function but with initial value, dont return the initial value
    result = list(itertools.accumulate([initial] + inputs, lambda x,y: x + y))
    return result[1:]

def signal_strengths(interval, xs):
    indexed_xs = list(enumerate([0,0] + list(xs)))  # add pre steps: one for "during cycle" and one for index by 1 
    return [ i * x for i,x in indexed_xs[interval::(interval * 2)]]

def within_cusor(crt,sprite_center): 
    return sprite_center - 1 <= crt and crt <= sprite_center + 1

def part1(inputs):
    xs = accumulate_(1, inputs)
    return sum(signal_strengths(20, xs))

def part2(inputs):
    width, xs = 40, accumulate_(1, [0] + inputs) # add one for index by 1, mod index by width  
    results = [ '#' if within_cusor(index % width,sprite_center) else '.' for index,sprite_center in enumerate(xs)]
    return ''.join(results[:width * 6])


# tests
pre1 = get_inputs('10-example1.txt')
pre2 = get_inputs('10-example2.txt')
assert list(accumulate_(1, pre1)) == [1,1,4,4,-1], 'accumulate_ returns correct x values'
assert list(signal_strengths(20, accumulate_(1, pre2))) == [420,1140,1800,2940,2880,3960], 'part 1 : signal strength example'
assert part1(pre2) == 13140, 'part 1: sum signal strength example'

expected = "##..##..##..##..##..##..##..##..##..##..###...###...###...###...###...###...###.####....####....####....####....####....#####.....#####.....#####.....#####.....######......######......######......###########.......#######.......#######....."
assert part2(pre2) == expected, 'part 2: crt output example'

# answers
def print_answer(prefix, answer):
    print(prefix)
    for i in range(6):
        start = i * 40
        print(answer[start: start + 40])

print_answer("example: ", part2(pre2))

day = get_inputs('10.txt')
print("Part 1: ", part1(day))
print_answer("Part 2:", part2(day))