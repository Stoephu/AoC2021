# %%
strings = [line.strip() for line in open('../inputs/day5.txt')]

# %%
def tuplefy(coord):
    a,b = x if len(x := coord.split(',')) == 2 else print(x)
    return (int(a), int(b))
linecoords = [[tuplefy(coords)  for coords in line.split(" -> ")] for line in strings]
# %%
def straight(coords):
    (a,b),(c,d)=coords
    return (a == c) or (b==d)
straights = [coords for coords in linecoords if straight(coords)]
# %%
def generateLine(coords):
    a,b = coords
    xs = list(range(a[0],b[0]+1)) if a[0] < b[0] else list(range(b[0],a[0]+1))[::-1]
    ys = list(range(a[1],b[1]+1)) if a[1] < b[1] else list(range(b[1],a[1]+1))[::-1]
    line = []
    if len(xs)==1:
        line = [(xs[0],y) for y in ys]
    elif len(ys)==1:
        line = [(x, ys[0]) for x in xs]
    else:
        line = zip(xs,ys)
    return line


# %%
def countHits(lines):
    coordsHit =  {}
    coordWithMoreThanToo = 0
    for st in lines:
        line = generateLine(st)
        for point in line:
            if point in coordsHit:
                if coordsHit[point] == 1: coordWithMoreThanToo += 1
                coordsHit[point] = coordsHit[point] + 1
            else:
                coordsHit[point] = 1
    return coordWithMoreThanToo
print(countHits(straights))
# %%
print(countHits(linecoords))