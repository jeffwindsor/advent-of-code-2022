def get_inputs(filename): 
    with open(filename) as file: 
        return file.read().strip()
        
def parse_cmd_args(args_input): return [arg.split(' ') for arg in args_input.strip().split('\n')]
def parse_cmd(cmd_input):       return [cmd_input[:2], parse_cmd_args(cmd_input[2:])]
def parse_cmds(inputs):         return [parse_cmd(i) for i in inputs.split('$ ') if i]

ROOT_PATH, PATH_SEP = '', '/'

def path(item): return item['path']
def size(item): return item['size']

def cd(index, current_dir, target):
    if target == "..":  
        current_path = path(current_dir)
        parent_path = current_path[:current_path.rfind(PATH_SEP)]
        return index[parent_path]
    elif target == "/": 
        return index[ROOT_PATH]
    else:
        target_path = f'{path(current_dir)}{PATH_SEP}{target}'
        if target_path in index: 
            return index[target_path]
        else:
            result = { 'path': target_path, 'directories':set(), 'size':0 }
            current_dir['directories'].add(target_path)
            index[path(result)] = result
            return result

def ls(current_dir, items):
    current_dir['size'] = sum([int(i) for (i,_) in items if i.isnumeric() ])
    return current_dir

def build(commands):
    index, root = start()
    d = root
    for cmd, args in commands:
        d = ls(d,args) if cmd == 'ls' else cd(index, d, args[0][0])
    return index

def start():
    root = { 'path': ROOT_PATH, 'directories':set(), 'size':0, }
    return ({ ROOT_PATH: root },root)

def totals(path_dir):
    path_totalsize = {}
    for p in sorted(path_dir.keys(), key=len, reverse=True):
        d = path_dir[p]
        path_totalsize[p] = size(d) + sum([ path_totalsize[sp] for sp in d['directories']])
    return path_totalsize

def part1(filename):
    path_totalsize = totals(build(parse_cmds(get_inputs(filename))))
    return sum([s for s in path_totalsize.values() if s <= 100000])

assert part1('./examples/07') == 95437
print("Part 1: ", part1('./inputs/07'))

def part2(filename):
    path_totalsize = totals(build(parse_cmds(get_inputs(filename))))
    root_size = path_totalsize['']
    needed_space = 30000000 - (70000000 - root_size)
    return min([s for s in path_totalsize.values() if s >= needed_space])

assert part2('./examples/07') == 24933642
print("Part 2: ", part2('./inputs/07'))

# PARSE
assert parse_cmds(get_inputs('./examples/07')) == [
    ['cd', [['/']]],
    ['ls', [['dir', 'a'], ['14848514', 'b.txt'], ['8504156', 'c.dat'], ['dir', 'd']]],
    ['cd', [['a']]],
    ['ls', [['dir', 'e'], ['29116', 'f'], ['2557', 'g'], ['62596', 'h.lst']]],
    ['cd', [['e']]],
    ['ls', [['584', 'i']]],
    ['cd', [['..']]],
    ['cd', [['..']]],
    ['cd', [['d']]],
    ['ls', [['4060174', 'j'], ['8033020', 'd.log'], ['5626152', 'd.ext'], ['7214296', 'k']]]
], 'part 1 test input'

# cd
index, root = start()
b = cd(index, root, "b")
c = cd(index, b, "c")

assert root == { 'path': '', 'directories':{'/b'}, 'size':0}, 'cd updates root directory set with b path'
assert b  == { 'path': '/b', 'directories':{'/b/c'}, 'size':0}, 'cd returns directory with correct path'
assert c  == { 'path': '/b/c', 'directories':set(), 'size':0}, 'cd returns directory with correct path'
assert index  == { '': root, '/b': b, '/b/c': c }, 'cd adds new b to path index'
assert cd(index, c, "..") == b, 'cd .. move up a directory'
assert cd(index, c, "/" ) == root, 'cd / returns root'

# ls
index, root = start()
ls(root, [['4060174', 'j'], ['dir', 'a'], ['8033020','d.log'], ['5626152','d.ext'], ['dir', 'd'], ['7214296','k']])
assert root == { 'path':'', 'directories':set(), 'size': 24933642}, 'ls only adds size'

# build
assert build(parse_cmds(get_inputs('./examples/07'))) == {
    '':     {'path': '', 'directories': {'/a', '/d'}, 'size': 23352670}, 
    '/a':   {'path': '/a', 'directories': {'/a/e'}, 'size': 94269}, 
    '/a/e': {'path': '/a/e', 'directories': set(), 'size': 584}, 
    '/d': {'path': '/d', 'directories': set(), 'size': 24933642}
    }