#%%
from collections import namedtuple

Command = namedtuple('Command', ['flip_on' ,'ranges'])
#%%
def command(line):
    flip_string, coords_string = line.split()
    flip_on = False
    if flip_string == "on":
        flip_on = True
    coords_string = coords_string.replace('=',',').replace('..',',').split(',')
    x_range = int(coords_string[1]),int(coords_string[2])
    y_range = int(coords_string[4]),int(coords_string[5])
    z_range = int(coords_string[7]),int(coords_string[8])
    return Command(flip_on,[x_range,y_range,z_range])
#%%
inp =  [line.strip() for line in open('../inputs/small_day22.txt')]
commands = [command(line) for line in inp][::-1]

# %%
def inside(o_range,i_range) -> bool:
    for value in i_range:
        if value < o_range[1] or value > o_range[0]:
            return True
    return False
def get_overlap_range(o_range,i_range):
    new = []
    new.append(i_range[0] if i_range[0] > o_range[0] else o_range[0])
    new.append(i_range[1] if i_range[1] < o_range[1] else o_range[1])
    return new

def overlap(ranges1,ranges2) -> list:
    xs1,xs2 = ranges1[0],ranges2[0]
    ys1,ys2 = ranges1[1],ranges2[1]
    zs1,zs2 = ranges1[2],ranges2[2]
    # exit with None if no overlap
    new_block = []
    if inside(xs1,xs2):
        new_block.append(get_overlap_range(xs1,xs2))
    elif inside(xs2,xs1):
        new_block.append(get_overlap_range(xs2,xs1))
    else:
        return None
    
    if inside(ys1,ys2):
        new_block.append(get_overlap_range(ys1,ys2))
    elif inside(ys2,ys1):
        new_block.append(get_overlap_range(ys2,ys1))
    else:
        return None

    if inside(zs1,zs2):
        new_block.append(get_overlap_range(zs1,zs2))
    elif inside(zs2,zs1):
        new_block.append(get_overlap_range(zs2,zs1))
    else:
        return None
    return new_block
    
def cube_num(ranges):
    xs,ys,zs = ranges
    return (xs[1]-xs[0])*(ys[1]-ys[0])*(zs[1]-zs[0])
# %%
for i, com in enumerate(commands):
    pass
# %%
