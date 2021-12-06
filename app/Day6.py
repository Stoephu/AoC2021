# %%
inp =  [line.strip() for line in open('../inputs/day6.txt')]
# %%
ints = [int(x) for x in inp[0].split(',')]

# %%
# featuring Elli
initial = dict([(x,0) for x in range(0,9)])
# %%
for x in ints:
    initial[x] += 1

def simulate(days, _state):
    state = _state.copy()
    for day in range(days):
        temp = 0
        for x in range(0,9):
            if x == 0:
                temp = state[x]
            else:
                state[x-1] = state[x]
        state[6] += temp
        state[8] = temp
        #print(f'{day=}', f'{state=}')
    return state

print(initial)
print(end := simulate(80, initial))
print(sum(end.values()))
# %%
print(initial)
print(end := simulate(256, initial))
print(sum(end.values()))