normalize = lambda p: (p[0]-500, p[1])
paths = lambda filename: [[ normalize(eval(l)) for l in b.split(' -> ')] 
                                    for b in open(filename, 'r').readlines()]
examples = paths('14-example.txt')
actuals  = paths('14.txt')

START_COL, START_ROW = 0,0

def display(rocks):
    print()
    rows, cols = [r for c,r in rocks], [c for c,r in rocks]
    result = ""
    for r in range(min(rows), max(rows) + 1): #(min(rows),max(rows)):
        result += f'\n {str(r).zfill(3)}'
        for c in range(min(cols), max(cols) + 1):
            icon = '#' if (c,r) in rocks  else '.'
            result += icon
    print(result)

def all_points(start, end): 
    (c1,r1),(c2,r2) = start, end
    cs,rs = sorted([c1,c2]), sorted([r1,r2])
    return set((c,r) 
            for c in range(cs[0],cs[1]+1)
            for r in range(rs[0],rs[1]+1))

def rocks_from(paths):
    pair = lambda xs: zip(xs, xs[1:])
    return set([point for path in paths 
                      for line in zip(path, path[1:]) 
                      for point in all_points(*line)])

def drop(continue_check, rocks):
    sc, sr = START_COL,START_ROW
    while(continue_check(sr,rocks)):
        if (sc,sr+1) not in rocks:        # down
            sr += 1                       # fall down
            continue
        if (sc-1,sr+1) not in rocks:      # down left
            sc -= 1
            sr += 1                       # fall down-left
            continue
        if (sc+1,sr+1) not in rocks:      # down right   
            sc += 1
            sr += 1                       # fall down-right
            continue
        rocks.add((sc,sr))                # add sand
        sc,sr = START_COL,START_ROW
        continue
    return rocks


def part1(paths):
    rocks = rocks_from(paths)
    bottom = max([r for c,r in rocks])
    sands = drop(lambda r,_: r <= bottom, rocks.copy())
    return len(sands) - len(rocks)

def part2(paths):
    rocks = rocks_from(paths)
    bottom = max([r for c,r in rocks]) + 2
    cols   = [c for c,r in rocks]
    floor  = all_points((min(cols) - bottom, bottom),(max(cols) + bottom, bottom))  # cover a triangle of build up
    rocks  = rocks | floor

    valid_position = lambda _,rocks: (START_COL,START_ROW) not in rocks 
    sands = drop(valid_position, rocks.copy())
    return len(sands) - len(rocks)

print('Part 1: ', part1(actuals))
print('Part 2: ', part2(actuals))