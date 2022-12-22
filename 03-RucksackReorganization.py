lines     = lambda fn: open(fn, 'r').read().splitlines()
priority  = lambda c: ord(c) - 38 if ord(c) < 97 else ord(c) - 96
split_mid = lambda s: [s[:len(s)//2],s[len(s)//2:]]
dupes     = lambda ss: ''.join(list(set(ss[0]) & set(ss[1])))
flatmap   = lambda f,lss: [f(l) for ls in lss for l in ls]
group     = lambda n,ls: [ls[i:i+n] for i in range(0, len(ls), n)]
answer    = lambda ss: sum([priority(dupes(s)) for s in ss])

part1    = lambda ls: answer([split_mid(l) for l in ls ])
part2    = lambda ls: answer([[a, dupes([b,c])] for a,b,c in group(3,ls)])

actuals = lines('./inputs/03')
print('Part 1: ',part1(actuals))
print('Part 2: ',part2(actuals))

###########################################################################
assert priority("A") == 27, 'case dependent scoring:A'
assert priority("Z") == 52, 'case dependent scoring:Z'
assert priority("a") ==  1, 'case dependent scoring:a'
assert priority("z") == 26, 'case dependent scoring:z'