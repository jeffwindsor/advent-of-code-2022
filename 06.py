
def get_inputs(file_name):
    with open(file_name) as file:
        result = file.read().strip()
    return result

def find_unique_seq(size,input):
    for i in range(size,len(input)):
        if len(set(input[i - size:i])) == size: return i

def part1(input): return find_unique_seq(4,input)
def part2(input): return find_unique_seq(14,input)

# test cases
assert part1('bvwbjplbgvbhsrlpgdmjqwftvncz') == 5
assert part1('nppdvjthqldpwncqszvftbrmjlhg') == 6
assert part1('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg') == 10
assert part1('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') == 11

assert part2('mjqjpqmgbljsphdztnvjfqwrcgsmlb') ==  19
assert part2('bvwbjplbgvbhsrlpgdmjqwftvncz') ==  23
assert part2('nppdvjthqldpwncqszvftbrmjlhg') ==  23
assert part2('nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg') ==  29
assert part2('zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw') ==  26

#answer
part1('1: ', get_inputs('06.txt')) 
part2('2: ',get_inputs('06.txt'))

