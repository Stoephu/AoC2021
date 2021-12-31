#%%
from collections import namedtuple

Command = namedtuple('Command', ['flip_on' ,'ranges'])
Range = namedtuple('Range', ['xs', 'ys', 'zs'])
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
    return Command(flip_on,Range(x_range,y_range,z_range))
#%%
inp =  [line.strip() for line in open('../inputs/small_day22.txt')]
commands = [command(line) for line in inp][::-1]

# %%
def inside(o_range,i_range) -> bool:
    min_val, max_val = i_range
    if min_val < o_range[1] and min_val >= o_range[0]:
        return True
    if max_val > o_range[0] and max_val <= o_range[1]:
        return True
    return False
def get_overlap_range(o_range,i_range):
    new = []
    new.append(i_range[0] if i_range[0] > o_range[0] else o_range[0])
    new.append(i_range[1] if i_range[1] < o_range[1] else o_range[1])
    return new

def overlap(ranges1,ranges2) -> list:
    xs1,xs2 = ranges1.xs,ranges2.xs
    ys1,ys2 = ranges1.ys,ranges2.ys
    zs1,zs2 = ranges1.zs,ranges2.zs
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
    return Range(*new_block)
    
def cube_num(ranges):
    xs,ys,zs = ranges
    return (xs[1]-xs[0])*(ys[1]-ys[0])*(zs[1]-zs[0])
# %%
def split_cube_from_off(on_range,off_range):
    print(f'split cube {on_range} {off_range}')
    compact_off = overlap(on_range,off_range)
    print(f'{compact_off=}')
    if not compact_off:
        return None
    top_cube = Range((compact_off.xs[1],on_range.xs[1]),compact_off.ys,compact_off.zs)
    bottom_cube = Range((on_range.xs[0],compact_off.xs[0]),compact_off.ys,compact_off.zs)
    front_cube = Range(compact_off.xs,(compact_off.ys[1],on_range.ys[1]),compact_off.zs)
    back_cube = Range(compact_off.xs,(on_range.ys[0],compact_off.ys[1]),compact_off.zs)
    left_cube = Range(compact_off.xs,compact_off.ys,(on_range.zs[0],compact_off.zs[0]))
    right_cube = Range(compact_off.xs,compact_off.ys,(compact_off.zs[1],on_range.zs[1]))
    t_f_edge = Range((compact_off.xs[1],on_range.xs[1]),(compact_off.ys[1],on_range.ys[1]),compact_off.zs)
    t_b_edge = Range((compact_off.xs[1],on_range.xs[1]),(on_range.ys[0],compact_off.ys[1]),compact_off.zs)
    t_l_edge = Range((compact_off.xs[1],on_range.xs[1]),compact_off.ys,(on_range.zs[0],compact_off.zs[0]))
    t_r_edge = Range((compact_off.xs[1],on_range.xs[1]),compact_off.ys,(compact_off.zs[1],on_range.zs[1]))
    l_f_edge = Range(compact_off.xs,(compact_off.ys[1],on_range.ys[1]),(on_range.zs[0],compact_off.zs[0]))
    r_f_edge = Range(compact_off.xs,(compact_off.ys[1],on_range.ys[1]),(compact_off.zs[1],on_range.zs[1]))
    l_b_edge = Range(compact_off.xs,(on_range.ys[0],compact_off.ys[1]),(on_range.zs[0],compact_off.zs[0]))
    r_b_edge = Range(compact_off.xs,(on_range.ys[0],compact_off.ys[1]),(compact_off.zs[1],on_range.zs[1]))
    b_f_edge = Range((on_range.xs[0],compact_off.xs[0]),(compact_off.ys[1],on_range.ys[1]),compact_off.zs)
    b_b_edge = Range((on_range.xs[0],compact_off.xs[0]),(on_range.ys[0],compact_off.ys[1]),compact_off.zs)
    b_l_edge = Range((on_range.xs[0],compact_off.xs[0]),compact_off.ys,(on_range.zs[0],compact_off.zs[0]))
    b_r_edge = Range((on_range.xs[0],compact_off.xs[0]),compact_off.ys,(compact_off.zs[1],on_range.zs[1]))
    t_f_l_corner =  Range((compact_off.xs[1],on_range.xs[1]),(compact_off.ys[1],on_range.ys[1]),(on_range.zs[0],compact_off.zs[0]))
    t_f_r_corner =  Range((compact_off.xs[1],on_range.xs[1]),(compact_off.ys[1],on_range.ys[1]),(compact_off.zs[1],on_range.zs[1]))
    f_b_l_corner = Range((compact_off.xs[1],on_range.xs[1]),(on_range.ys[0],compact_off.ys[1]),(on_range.zs[0],compact_off.zs[0]))
    f_b_r_corner = Range((compact_off.xs[1],on_range.xs[1]),(on_range.ys[0],compact_off.ys[1]),(compact_off.zs[1],on_range.zs[1]))
    b_f_l_corner =  Range((on_range.xs[0],compact_off.xs[0]),(compact_off.ys[1],on_range.ys[1]),(on_range.zs[0],compact_off.zs[0]))
    b_f_r_corner =  Range((on_range.xs[0],compact_off.xs[0]),(compact_off.ys[1],on_range.ys[1]),(compact_off.zs[1],on_range.zs[1]))
    b_b_l_corner = Range((on_range.xs[0],compact_off.xs[0]),(on_range.ys[0],compact_off.ys[1]),(on_range.zs[0],compact_off.zs[0]))
    b_b_r_corner = Range((on_range.xs[0],compact_off.xs[0]),(on_range.ys[0],compact_off.ys[1]),(compact_off.zs[1],on_range.zs[1]))
    cubes =  [top_cube,bottom_cube,front_cube,back_cube,left_cube,right_cube]
    edges = [t_f_edge,t_b_edge,t_l_edge,t_r_edge,l_f_edge,r_f_edge,l_b_edge,r_b_edge,b_f_edge,b_b_edge,b_l_edge,b_r_edge]
    corners = [t_f_l_corner,
    t_f_r_corner,
    f_b_l_corner,
    f_b_r_corner,
    b_f_l_corner,
    b_f_r_corner,
    b_b_l_corner,
    b_b_r_corner]
    cubes.extend(edges)
    cubes.extend(corners)
    print(f'{cubes=}')
    return [cube for cube in cubes if cube_num(cube)]
# %%
# slice all on cubes with off cubes if required
def resolve_off(commands):
    only_on_commands = []
    for i,com in enumerate(commands):
        if not com.flip_on:
            for j, com_j in enumerate(commands[i:]):
                if com_j.flip_on:
                    new_cubes = split_cube_from_off(com_j.ranges, com.ranges)
                    if not new_cubes:
                        continue
                    commands.pop(i+j)
                    for cube in new_cubes:
                        commands.insert(i+j,Command(True,cube))
        
    for com in commands:
        if com.flip_on:
            only_on_commands.append(com)
    return only_on_commands
# %%
def resolve_on_commands(input):
    commands = input.copy()
    for i, com in enumerate(commands):
        print(f'{i}')
        for j, com_j in enumerate(commands[i:]):
            overlap_cube = overlap(com.ranges,com_j.ranges)
            print(f'{overlap_cube=}')
            if not overlap_cube:
                continue
            commands.pop(i+j)
            new_cubes = split_cube_from_off(com_j.ranges, overlap_cube)
            print(f'{new_cubes=}')
            if new_cubes:
                for cube in new_cubes:
                    commands.insert(i+j,Command(True,cube))
    return commands
#%%
#tests
test = [Command(True,Range([0,10],(0,10),(0,10))), Command(True,Range((4,6),(4,6),(-2,5)))]
split_cube_from_off(test[0].ranges,test[1].ranges)
# %%
