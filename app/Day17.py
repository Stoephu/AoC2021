# %%
import numpy as np
inp = [line.strip() for line in open('../inputs/small.txt')]

# %%
split = inp[0].split()
x_range_string = split[2]
y_range_string = split[3]
x_range_split = x_range_string.replace(',', '').split('=')[1].split('..')
x_range = (int(x_range_split[0]), int(x_range_split[1]))
y_range_split = y_range_string.replace(',', '').split('=')[1].split('..')
y_range = (int(y_range_split[0]), int(y_range_split[1]))

# %%
# -- Part 1 --

e = abs(y_range[0])
y_max = sum([n for n in range(e)])
print(y_max)

# %%
# -- Part 2 --


def time_x_stop(x_stop):
    return x if (x := -1 + np.sqrt(1 + 4*0.5*x_stop)).is_integer() else None


y_para_posi = range(abs(y_range[1]), abs(y_range[0])+1)
x_stop_posibilities = [int(v_0) for x in range(
    x_range[0], x_range[1]+1) if (v_0 := time_x_stop(x))]


def enters(v_0, ranges):
    distance = 0
    for n in reversed(range(0, v_0+1)):
        distance += n
        if distance in ranges:
            return n
        if distance > max(ranges):
            return None


def y_enters(v_0, ranges):
    distance = 0
    while True:
        distance += v_0
        v_0 += 1
        if distance in ranges:
            return v_0
        if distance > max(ranges):
            return None


x_pass_posibilities = [v_0-v_last for v_0 in range(
    x_stop_posibilities[0], x_range[1]+1) if (v_last := enters(v_0, range(x_range[0], x_range[1]+1)))]

y_direct_posi = [v_last-v_0 for v_0 in range(
    0, abs(y_range[0])+1) if (v_last := y_enters(v_0, y_para_posi))]
# %%
result = len(y_para_posi) + \
    len([True for y_posi in y_para_posi if y_posi in x_pass_posibilities])
result += len([True for y in y_direct_posi if y in x_pass_posibilities])
# %%
