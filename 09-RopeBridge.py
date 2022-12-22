# expand move numbers to a string of directions 
def get_inputs(filename): 
    with open(filename) as file: 
        lines = file.read().strip()
    commands = [ left.split(' ') for left in lines.split('\n') ]
    return ''.join([ c[0] * int(c[1]) for c in commands ])

##############################################################
def add(x,y):      return (x[0] + y[0], x[1] + y[1])
def subtract(x,y): return (x[0] - y[0], x[1] - y[1])

# u2l2 u2l u2  u2r u2r2
# ul2  .   .   .   ur2
# l2   .   T   .   r2
# dl2  .   .   .   dr2
# d2l2 d2l d   d2r d2r2
start,left,right,up,down = (0,0),(0,-1),(0, 1),(1, 0),(-1, 0)
ul,ur,dl,dr     = add(up,left),add(up,right),add(down,left),add(down,right)
u2,d2,r2,l2     = add(up,up),add(down,down),add(right,right),add(left,left)
u2l,u2r,ul2,ur2 = add(u2,left),add(u2,right),add(up,l2),add(up,r2)
d2l,d2r,dl2,dr2 = add(d2,left),add(d2,right),add(down,l2),add(down,r2)
u2l2,u2r2       = add(u2l,left),add(u2r,right)
d2l2,d2r2       = add(d2l,left),add(d2r,right)
direction_move_map = {'U':up, 'D':down, 'L':left, 'R':right}
diff_move_map      = { u2l2:ul, u2l:ul, u2:up, u2r:ur, u2r2:ur, ul2:ul, 
                       ur2:ur, l2:left, r2:right, dl2:dl, dr2:dr, d2l2:dl, 
                       d2l:dl, d2:down, d2r:dr, d2r2:dr }

def move(p, m):
    return add(p, direction_move_map[m])

def follow(a,b):
    diff = subtract(a,b)
    return add(b, diff_move_map[diff]) if diff in diff_move_map else b

def part1(direction):
    knot1, knot2, history = start, start, {start}
    for direction in direction:
        knot1 = move(knot1,direction)
        followed = follow(knot1,knot2)
        if knot2 != followed: 
            history.add(followed)
            knot2 = followed
    return len(history)

def part2(direction):
    knots   = [start   for i in range(10)]
    history = {start}
    for direction in direction:
        knots[0] = move(knots[0],direction)
        for i in range(9):
            j = i + 1
            followed = follow(knots[i],knots[j])
            if j == 9 and knots[j] != followed: history.add(followed)
            knots[j] = followed
    return len(history)
            
################################################################
### test: input parsing to string
assert get_inputs('./examples/09') == 'RRRRUUUULLLDRRRRDLLLLLRR'

### test: movements of head
for m,result in [('U',up),('D',down),('L',left),('R',right)]:
    assert move(start,m) == result

### test: tail must move movements
assert react(u2, start,set()) == (u2,  up,  {up})
assert react(u2r,start,set()) == (u2r, ur, {ur})
assert react(ur2,start,set()) == (ur2, ur, {ur})
assert react(r2, start,set()) == (r2,  right,  {right})
assert react(dr2,start,set()) == (dr2, dr, {dr})
assert react(d2r,start,set()) == (d2r, dr, {dr})
assert react(d2, start,set()) == (d2,  down,  {down})
assert react(d2l,start,set()) == (d2l, dl, {dl})
assert react(dl2,start,set()) == (dl2, dl, {dl})
assert react(l2, start,set()) == (l2,  left,  {left})
assert react(ul2,start,set()) == (ul2, ul, {ul})
assert react(u2l,start,set()) == (u2l, ul, {ul})

### test: tail does not move
for h in [start, up, left, right, down, ur, ul, dr, dl]:
    assert react(h, start, set())  == (h, start, set())

### demo data
assert part1(get_inputs("09-example.txt")) == 13
assert part2(get_inputs("09-example.txt")) == 1

################################################################
### answers
print(f'Part 1: { part1(get_inputs("09.txt")) }')
print(f'Part 2: { part2(get_inputs("09.txt")) }')


# def print_knots(rows,cols,knots):
#     lines = ['.' * cols for row in range(rows)]
#     ki = len(knots)
#     for i in reversed(range(ki)):
#         r,c = knots[i]
#         l = lines[r]
#         lines[r] = f'{l[:c]}{i}{l[c+1:]}'
#     for l in reversed(lines):
#         print(l)