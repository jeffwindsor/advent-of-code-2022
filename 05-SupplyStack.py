import re

def get_inputs(file_name):
    with open(file_name) as file:
        ss,ms = file.read().split('\n\n')
    
    moves = [[ int(i) 
                for i in re.split('move | from | to ', m) if i] # strip out verbage and convert to [number to move, from stack, to stack]
                for m in ms.split('\n') ]
    stackInputs = [ list(s[1::4])                               # [1::4] start at 1, pull out every 4th character from stack input row
                    for s in ss.split('\n')[:-1]]               # [:-1] drops the last stack row (the indexes)
    stacks = [ ''.join([row[c]                                  # rotate inputs to make a stack string/stack
                for row in stackInputs if row[c] != ' ']) 
                for c in range(len(stackInputs[0]))]
    return (moves,stacks)


def move_container(crane, m, stacks):
    c,f,t = m[0], m[1] - 1, m[2] - 1      
    stacks[t] = crane(stacks[f][:c]) + stacks[t]
    stacks[f] = stacks[f][c:]
    return stacks 

def move_containers(crane,inputs):
    moves,stacks = inputs
    for move in moves:
        move_container(crane,move,stacks)
    return stacks

crate_mover_9000 = lambda stack: stack[::-1]
crate_mover_9001 = lambda stack: stack
take_top         = lambda stacks: ''.join([s[0] for s in stacks])
actuals  = get_inputs('05.txt')
examples = get_inputs('05-example.txt')
print('Part 1', take_top(move_containers(crate_mover_9000, actuals)))
print('Part 2', take_top(move_containers(crate_mover_9001, actuals)))


assert get_inputs('05-example.txt') == ([[1,2,1],[3,1,3],[2,2,1],[1,1,2]] ,['NZ', 'DCM', 'P'])
assert crate_mover_9000('ABC') == 'CBA'
assert crate_mover_9001('ABC') == 'ABC'
assert take_top(['JK','DEF','GHICBA']) == 'JDG'
assert move_container(crate_mover_9000, [3,1,3],['ABC','DEF','GHI']) == ['','DEF','CBAGHI']
assert move_container(crate_mover_9001, [3,1,3],['ABC','DEF','GHI']) == ['','DEF','ABCGHI']
assert take_top(move_containers(crate_mover_9000, examples)) == 'CMZ'
# assert take_top(move_containers(crate_mover_9001, examples)) == 'MCD'