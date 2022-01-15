#%%
from collections import namedtuple

Command = namedtuple('Command', ['flip_on' ,'ranges'])
Range = namedtuple('Range', ['x', 'y', 'z'])
Coord = namedtuple('Coord', ['anchor', 'size'])
#%%
def command(line):
    flip_string, coords_string = line.split()
    flip_on = False
    if flip_string == "on":
        flip_on = True
    coords_string = coords_string.replace('=',',').replace('..',',').split(',')
    x_range = Coord(int(coords_string[1]),int(coords_string[2]) -int(coords_string[1]) +1) #if flip_on else int(coords_string[2])
    y_range = Coord(int(coords_string[4]),int(coords_string[5]) -int(coords_string[4]) +1) #if flip_on else int(coords_string[5])
    z_range = Coord(int(coords_string[7]),int(coords_string[8]) -int(coords_string[7]) +1) #if flip_on else int(coords_string[8])
    return Command(flip_on,Range(x_range,y_range,z_range)) 
#%%
inp =  [line.strip() for line in open('../inputs/day22.txt')]
commands = [command(line) for line in inp]

# %%
def cube_num(ranges):
    x,y,z = ranges
    return (x.size)*(y.size)*(z.size)

def ena(coord: Coord): # end_neighbour_anchor
    return coord.anchor + coord.size

def inside(o_range,i_range) -> bool:
    i_anchor, i_size = i_range
    o_anchor, o_size = o_range
    if ena(i_range) - 1 >= o_anchor and i_anchor - o_anchor <= o_size - 1:
        return True
    return False

def get_overlap_coord(o_range,i_range):
    anchor = i_range.anchor if i_range.anchor >= o_range.anchor else o_range.anchor
    size = ena(i_range) - anchor if ena(i_range) <= ena(o_range) else ena(o_range) - anchor
    new = Coord(anchor, size)
    return new

def overlap(com1:Command,com2:Command) -> list:
    ranges1 = com1.ranges
    ranges2 = com2.ranges
    x1,x2 = ranges1.x,ranges2.x
    y1,y2 = ranges1.y,ranges2.y
    z1,z2 = ranges1.z,ranges2.z
    # exit with None if no overlap
    new_block = []
    if inside(x1,x2):
        new_block.append(get_overlap_coord(x1,x2))
    else:
        return None
    
    if inside(y1,y2):
        new_block.append(get_overlap_coord(y1,y2))
    else:
        return None

    if inside(z1,z2):
        new_block.append(get_overlap_coord(z1,z2))
    else:
        return None
    return Range(*new_block)
    
# %%
def split_cube_from_off(on_cube: Command,off_cube: Command):
    on_range = on_cube.ranges
    off_range = off_cube.ranges
    compact_off = overlap(on_cube,off_cube)
    if not compact_off:
        return None
    top_cube = Range(Coord(ena(compact_off.x),ena(on_range.x)-ena(compact_off.x)),compact_off.y,compact_off.z)
    bottom_cube = Range(Coord(on_range.x.anchor, compact_off.x.anchor - on_range.x.anchor),compact_off.y,compact_off.z)
    front_cube = Range(compact_off.x,Coord(ena(compact_off.y),ena(on_range.y)-ena(compact_off.y)),compact_off.z)
    back_cube = Range(compact_off.x,Coord(on_range.y.anchor, compact_off.y.anchor - on_range.y.anchor),compact_off.z)
    right_cube = Range(compact_off.x,compact_off.y,Coord(ena(compact_off.z),ena(on_range.z)-ena(compact_off.z)))
    left_cube = Range(compact_off.x,compact_off.y,Coord(on_range.z.anchor, compact_off.z.anchor - on_range.z.anchor))
    t_f_edge = Range(Coord(ena(compact_off.x),ena(on_range.x)-ena(compact_off.x)),Coord(ena(compact_off.y),ena(on_range.y)-ena(compact_off.y)),compact_off.z)
    t_b_edge = Range(Coord(ena(compact_off.x),ena(on_range.x)-ena(compact_off.x)),Coord(on_range.y.anchor, compact_off.y.anchor - on_range.y.anchor),compact_off.z)
    t_r_edge = Range(Coord(ena(compact_off.x),ena(on_range.x)-ena(compact_off.x)),compact_off.y,Coord(ena(compact_off.z),ena(on_range.z)-ena(compact_off.z)))
    t_l_edge = Range(Coord(ena(compact_off.x),ena(on_range.x)-ena(compact_off.x)),compact_off.y,Coord(on_range.z.anchor, compact_off.z.anchor - on_range.z.anchor))
    r_f_edge = Range(compact_off.x,Coord(ena(compact_off.y),ena(on_range.y)-ena(compact_off.y)),Coord(ena(compact_off.z),ena(on_range.z)-ena(compact_off.z))) 
    l_f_edge = Range(compact_off.x,Coord(ena(compact_off.y),ena(on_range.y)-ena(compact_off.y)),Coord(on_range.z.anchor, compact_off.z.anchor - on_range.z.anchor))
    r_b_edge = Range(compact_off.x,Coord(on_range.y.anchor, compact_off.y.anchor - on_range.y.anchor),Coord(ena(compact_off.z),ena(on_range.z)-ena(compact_off.z)))
    l_b_edge = Range(compact_off.x,Coord(on_range.y.anchor, compact_off.y.anchor - on_range.y.anchor),Coord(on_range.z.anchor, compact_off.z.anchor - on_range.z.anchor))
    b_f_edge = Range(Coord(on_range.x.anchor, compact_off.x.anchor - on_range.x.anchor),Coord(ena(compact_off.y),ena(on_range.y)-ena(compact_off.y)),compact_off.z)
    b_b_edge = Range(Coord(on_range.x.anchor, compact_off.x.anchor - on_range.x.anchor),Coord(on_range.y.anchor, compact_off.y.anchor - on_range.y.anchor),compact_off.z)
    b_r_edge = Range(Coord(on_range.x.anchor, compact_off.x.anchor - on_range.x.anchor),compact_off.y,Coord(ena(compact_off.z),ena(on_range.z)-ena(compact_off.z)))
    b_l_edge = Range(Coord(on_range.x.anchor, compact_off.x.anchor - on_range.x.anchor),compact_off.y,Coord(on_range.z.anchor, compact_off.z.anchor - on_range.z.anchor))
    t_f_r_corner =  Range(Coord(ena(compact_off.x),ena(on_range.x)-ena(compact_off.x)),Coord(ena(compact_off.y),ena(on_range.y)-ena(compact_off.y)),Coord(ena(compact_off.z),ena(on_range.z)-ena(compact_off.z)))
    t_f_l_corner =  Range(Coord(ena(compact_off.x),ena(on_range.x)-ena(compact_off.x)),Coord(ena(compact_off.y),ena(on_range.y)-ena(compact_off.y)),Coord(on_range.z.anchor, compact_off.z.anchor - on_range.z.anchor))
    t_b_r_corner = Range(Coord(ena(compact_off.x),ena(on_range.x)-ena(compact_off.x)),Coord(on_range.y.anchor, compact_off.y.anchor - on_range.y.anchor),Coord(ena(compact_off.z),ena(on_range.z)-ena(compact_off.z)))
    t_b_l_corner = Range(Coord(ena(compact_off.x),ena(on_range.x)-ena(compact_off.x)),Coord(on_range.y.anchor, compact_off.y.anchor - on_range.y.anchor),Coord(on_range.z.anchor, compact_off.z.anchor - on_range.z.anchor))
    b_f_r_corner =  Range(Coord(on_range.x.anchor, compact_off.x.anchor - on_range.x.anchor),Coord(ena(compact_off.y),ena(on_range.y)-ena(compact_off.y)),Coord(ena(compact_off.z),ena(on_range.z)-ena(compact_off.z)))
    b_f_l_corner =  Range(Coord(on_range.x.anchor, compact_off.x.anchor - on_range.x.anchor),Coord(ena(compact_off.y),ena(on_range.y)-ena(compact_off.y)),Coord(on_range.z.anchor, compact_off.z.anchor - on_range.z.anchor))
    b_b_r_corner = Range(Coord(on_range.x.anchor, compact_off.x.anchor - on_range.x.anchor),Coord(on_range.y.anchor, compact_off.y.anchor - on_range.y.anchor),Coord(ena(compact_off.z),ena(on_range.z)-ena(compact_off.z)))
    b_b_l_corner = Range(Coord(on_range.x.anchor, compact_off.x.anchor - on_range.x.anchor),Coord(on_range.y.anchor, compact_off.y.anchor - on_range.y.anchor),Coord(on_range.z.anchor, compact_off.z.anchor - on_range.z.anchor))
    cubes =  [top_cube,bottom_cube,front_cube,back_cube,left_cube,right_cube]
    edges = [t_f_edge,t_b_edge,t_l_edge,t_r_edge,l_f_edge,r_f_edge,l_b_edge,r_b_edge,b_f_edge,b_b_edge,b_l_edge,b_r_edge]
    corners = [t_f_l_corner,t_f_r_corner,t_b_l_corner,t_b_r_corner,b_f_l_corner,b_f_r_corner,b_b_l_corner,b_b_r_corner]
    cubes.extend(edges)
    cubes.extend(corners)
    non_zero_cubes =  [cube for cube in cubes if cube_num(cube)]
    return non_zero_cubes
# %%
# slice all on cubes with off cubes if required
def resolve(commands):
    on_cubes = []
    todo = commands.copy()
    while todo:
        com: Command = todo.pop(0)
        new_cubes = []
        for com_j in on_cubes:
            if overlap(com_j, com):
                cubes = split_cube_from_off(com_j,com)
                for cube in cubes:
                    new_command = Command(True,cube)
                    new_cubes.append(new_command)
            else:
                new_cubes.append(com_j)
        if com.flip_on:
            new_cubes.append(com)
        on_cubes = new_cubes.copy()
    print(f'{len(on_cubes)=}')
    return on_cubes


# %%
# part 1 
def count_cubes_init(unique_on):
    initialitation_cube = Command(True,Range(Coord(-50,101),Coord(-50,101),Coord(-50,101)))
    num_on_cube = 0
    for com in unique_on:
        o = overlap(initialitation_cube,com)
        num_on_cube += cube_num(o) if o else 0
    print(num_on_cube)
# %%
only_on = resolve(commands)
count_cubes_init(only_on)

# %%
Off = Command(False,Range(Coord(9,3),Coord(9,3),Coord(9,3)))
On_2 = Command(True, Range(Coord(11,3),Coord(11,3),Coord(11,3)))
On_1 = Command(True, Range(Coord(10,3),Coord(10,3),Coord(10,3)))
def test(new_com = None):
    commands = [Off,On_2,On_1] if not new_com else new_com
    return count_cubes_init(resolve(commands))

def list_all_coords(commands):
    l = list()
    for command in commands:
        ranges = command.ranges
        x,y,z = ranges
        for i in range(x.anchor,x.anchor + x.size):
            for j in range(y.anchor,y.anchor + y.size):
                for k in range(z.anchor,z.anchor + z.size):
                    l.append((i,j,k))
    l.sort()
    return l
# %%
#test()
# %%
def count_cubes(commands):
    num_cubes = 0
    for com in commands:
        num_cubes += cube_num(com.ranges)
    print(num_cubes)
count_cubes(only_on)
# %%
