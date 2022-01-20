from operator import truediv
from turtle import distance
import numpy as np
from numpy.linalg import matrix_power as mp
# %%
a = np.array([  [1,0,0],
                [0,0,1],
                [0,-1,0]],dtype=int)
b = np.array([  [0,1,0],
                [-1,0,0],
                [0,0,1]],dtype=int)
elements = [np.identity(3,dtype=int),a,mp(a,2),mp(a,3),b,b.dot(a),b.dot(mp(a,2)),b.dot(mp(a,3)),mp(b,2),mp(b,2).dot(a),mp(b,2).dot(mp(a,2)),mp(b,2).dot(mp(a,3)),mp(b,3),mp(b,3).dot(a),mp(b,3).dot(mp(a,2)),mp(b,3).dot(mp(a,3)),a.dot(b),a.dot(b).dot(a),a.dot(b).dot(mp(a,2)),a.dot(b).dot(mp(a,3)),mp(a,3).dot(b),mp(a,3).dot(b).dot(a),mp(a,3).dot(b).dot(mp(a,2)),mp(a,3).dot(b).dot(mp(a,3))] 

# %%
inp =  [line.strip() for line in open('C:/Users/Stoephu/Documents/Projects/AoC2021/inputs/small_day19.txt')]
scanners = []
beacons = None
for line in inp:
    if '--' == line[:2]:
        scanners.append(beacons)
        beacons = []
        continue
    if len(coords := line.split(',')) == 3:
        coord = np.array([int(coords[0]), int(coords[1]), int(coords[2])],dtype=int)
        beacons.append(coord)
    else:
        continue
scanners.append(beacons)
scanners.pop(0)
scanners = [np.array(l) for l in scanners]
# %%
confirmed_beacons = scanners[0]
# %%
def taxi_metric(coord1, coord2):
    x,y,z = np.abs(coord2 - coord1)
    return x + y + z

def eucl_metric(coord1, coord2):
    x,y,z = coord2 - coord1
    return x*x + y*y + z*z

def farthest_away(scn):
    farthest_beacon = None
    farthest_distance = 0
    for beacon in scn:
        if (dist := taxi_metric(beacon)) > farthest_distance:
            farthest_distance = dist
            farthest_beacon = beacon
    return farthest_beacon


def try_to_fit(scn0, scn1):
    set_scanner = {tuple(x) for x in scn0.tolist()}
    best_score = 0
    matching_coords = None
    rotation_index = 0
    best_offset = None
    for j, rot in enumerate(elements):
        rotated_scanner = rot.dot(scn1.T).T
        for k, a_beacon in enumerate(rotated_scanner):
            for i, beacon in enumerate(scn0):
                offset = beacon - a_beacon
                offset_scanner = rotated_scanner + offset
                set_rotated_scanner = {tuple(x) for x in offset_scanner}
                score = len(set_scanner.intersection(set_rotated_scanner))
                if score > best_score:
                    best_score = score
                    rotation_index = j
                    best_offset = offset
                    matching_coords = offset_scanner.copy()
    return best_score, matching_coords, best_offset, rotation_index

# %%
def get_signature(beacon, beacons):
    signature =[eucl_metric(beacon,x) for x in beacons] 
    signature.sort()
    return frozenset(signature[1:])

def is_signature_inside(signature, signatures):
    for sig in signatures:
        matches = 0
        for dis in sig:
            if dis in signature:
                matches += 1
        if matches >= 12:
            return True
    return False


def unique_signatures():
    signatures = []

    for scanner in scanners:
        for beacon in scanner:
            signature = get_signature(beacon, scanner)
            if not is_signature_inside(signature, signatures):
                signatures.append(signature)

    print(len(signatures))

# %%
def common_beacons(scn1,scn2):
    sigs1 = [get_signature(beacon, scn1) for beacon in scn1]
    print(sigs1)
    sigs2 = [get_signature(beacon, scn2) for beacon in scn2]
    print(sigs2)
    commons = [signature for signature in sigs1 if is_signature_inside(signature,sigs2)]
    return commons
# %%
def rotates_and_translates(scanners):
    todo = scanners[1:].copy()
    all_coords = scanners[0].copy()
    distances = []
    while todo:
        temp = []
        for i, scanner in enumerate(todo):
            matches, matched_coords, offset, rot_index = try_to_fit(all_coords,scanner)
            if matches < 12:
                temp.append(scanner)
            else:
                all_coords = np.append(all_coords,matched_coords, axis=0)
                all_coords = np.unique(all_coords,axis=0)
                distances.append(offset)
                print(f'found match {i} / {len(todo)} / {len(scanners)}')
        todo = temp
    return all_coords,distances
# %%

result, offsets = rotates_and_translates(scanners)
#%%
offsets.append(np.array([0,0,0]))
distances = []
for i, offs in enumerate(offsets):
    for offj in offsets[i:]:
        distances.append(taxi_metric(offs,offj))
print(f'{max(distances)=}')
# %%
