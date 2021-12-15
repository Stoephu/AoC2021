# %%
inp =  [line.strip() for line in open('../inputs/small.txt')]
matchdict = {')':'(', ']':'[', '}':'{','>':'<'}
rmatchdict = {t[1]:t[0] for t in matchdict.items()}
def illegal(b, c):
    if c in matchdict:
        return matchdict[c] != b
    else:
        return False

def matches(b, c):
    if c in matchdict:
        return matchdict[c] == b
    else:
        return False

frstIllegal = []
for line in inp:
    stack = []
    for c in line:
        if len(stack) and illegal(stack[-1],c):
            frstIllegal.append(c)
            break
        else:
            if len(stack) and matches(stack[-1],c):
                stack.pop()
            else:
                stack.append(c)

scoring ={')':3, ']':57, '}':1197,'>':25137}

result = 0
for il in frstIllegal:
    result += scoring[il]

print(result)
# %%

fillerss = []
def fill (stack, fillers, c):
    print(f'{c=} and {stack=} ')
    if c:
        if len(stack) and illegal(stack[-1], c):
            f = rmatchdict[stack[-1]]
            print(f'{c=} and {f=} and {stack=}')
            fillers.append(f)
            fill(stack, fillers,f)
            fill(stack, fillers,c)
        elif len(stack) and matches(stack[-1], c):
            stack.pop()
        else:
            stack.append(c)
    else:
        f = rmatchdict[stack[-1]]
        fillers.append(f)
        fill(stack, fillers, f)

for line in inp:
    line = list(line)
    fillers = []
    stack = [line.pop(0)]
    while len(stack) or len(line):
        c = None
        if len(line): c=line.pop(0)
        fill(stack,fillers,c)
    fillerss.append(fillers)
print(fillerss)

scoring = {')':1, ']':2, '}':3,'>':4}
score = 0
for fillers in fillerss:
    _score = 0
    for c in fillers:
        _score *=5
        _score += scoring[c]
    score += _score
# %%
