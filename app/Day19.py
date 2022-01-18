import numpy as np
from numpy.linalg import matrix_power as mp
# %%
a = np.array([  [1,0,0],
                [0,0,1],
                [0,-1,0]])
b = np.array([  [0,1,0],
                [-1,0,0],
                [0,0,1]])
elements = [np.identity(3),a,mp(a,2),mp(a,3),b,b.dot(a),b.dot(mp(a,2)),b.dot(mp(a,3)),mp(b,2),mp(b,2).dot(a),mp(b,2).dot(mp(a,2)),mp(b,2).dot(mp(a,3)),mp(b,3),mp(b,3).dot(a),mp(b,3).dot(mp(a,2)),mp(b,3).dot(mp(a,3)),a.dot(b),a.dot(b).dot(a),a.dot(b).dot(mp(a,2)),a.dot(b).dot(mp(a,3)),mp(a,3).dot(b),mp(a,3).dot(b).dot(a),mp(a,3).dot(b).dot(mp(a,2)),mp(a,3).dot(b).dot(mp(a,3))] 

# %%
inp =  [line.strip() for line in open('../inputs/small_day19.txt')]
scanners = []
beacons = None
for line in inp:
    if '--' == line[:2]:
        scanners.append(beacons)
        beacons = []
        continue
    if len(coords := line.split(',')) == 3:
        coord = np.array([int(coords[0]), int(coords[1]), int(coords[2])])
        beacons.append(coord)
    else:
        continue
scanners.pop(0)
scanners = [np.array(l) for l in scanners]
# %%
confirmed_beacons = scanners[0]
# %%
def taxi_metric(coord):
    x,y,z = np.abs(coord)
    return x + y + z

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
    anchor_beacon = None
    best_score = 0
    scn0_beacon = None
    best_rotation = None
    for j, rot in enumerate(elements):
        
        rotated_scanner = np.array([rot.dot(vec) for vec in scn1])#np.einsum('ij,kj->ik',rot,scn1)#rot.dot(scn1)
        for k, a_beacon in enumerate(rotated_scanner):
            for i, beacon in enumerate(scn0):
                offset = beacon - a_beacon
                offset_scanner = scn1 + offset
                set_rotated_scanner = {tuple(x) for x in offset_scanner}
                score = len(x :=set_scanner.intersection(set_rotated_scanner))
                if score > best_score:
                    best_score = score
                    scn0_beacon = beacon
                    best_rotation = j
                    anchor_beacon = a_beacon
    return best_score, anchor_beacon, scn0_beacon, best_rotation
# %%
try_to_fit(scanners[0], scanners[1])
# %%
for scanner in scanners[1:]:
    print(try_to_fit(scanners[0], scanner))
# %%
