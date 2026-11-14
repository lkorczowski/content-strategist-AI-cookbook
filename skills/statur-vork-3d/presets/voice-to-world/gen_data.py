# Data for the "voice to world" preset: land dots on a Fibonacci sphere (real coastlines from global-land-mask, MIT),
# a growth tree around the speaker, global arcs. Frame: the speaker city on +Y, globe radius 1. Usage: gen_data.py out.json [lat lon]
import json, math, sys, numpy as np
from global_land_mask import globe
rng = np.random.default_rng(7)
LAT0 = math.radians(float(sys.argv[2]) if len(sys.argv) > 3 else 48.86); LON0 = math.radians(float(sys.argv[3]) if len(sys.argv) > 3 else 2.35)
def ll2v(lat, lon):  # earth frame: Y north, X lon 0, Z lon 90E? use right-handed with Z=-sin(lon)
    return np.stack([np.cos(lat)*np.cos(lon), np.sin(lat), -np.cos(lat)*np.sin(lon)], -1)
g = ll2v(LAT0, LON0)
# rotation that maps g -> +Y (Rodrigues)
y = np.array([0, 1, 0.]); ax = np.cross(g, y); s = np.linalg.norm(ax); c = g @ y; ax /= s
K = np.array([[0, -ax[2], ax[1]], [ax[2], 0, -ax[0]], [-ax[1], ax[0], 0]]); Rm = np.eye(3) + s*K + (1-c)*K@K
north = Rm @ y  # earth axis in world frame
# land dots
N = 90000; i = np.arange(N) + .5; phi = np.arccos(1 - 2*i/N); th = math.pi*(1+5**.5)*i
lat = math.pi/2 - phi; lon = (th % (2*math.pi)) - math.pi
land = globe.is_land(np.degrees(lat), np.degrees(lon))
P = (Rm @ ll2v(lat[land], lon[land]).T).T
ang = np.arccos(np.clip(P[:, 1], -1, 1))
print('land dots', len(P))
# growth tree on the cap: angular distance d from 1e-4 to 0.42 rad (globe units)
M = 5200
d = np.exp(rng.uniform(np.log(0.004), np.log(0.42), M)); d.sort()
az = rng.uniform(0, 2*np.pi, M)
nodes = np.stack([np.sin(d)*np.cos(az), np.cos(d), np.sin(d)*np.sin(az)], -1)
parent = np.full(M, -1)
for k in range(M):
    if d[k] < 0.012: continue
    cand = np.arange(k)[d[:k] < d[k]*0.85]
    if len(cand) == 0: continue
    dd = np.linalg.norm(nodes[cand]-nodes[k], axis=1); parent[k] = cand[np.argsort(dd)[:3]][rng.integers(0, min(3, len(cand)))]
# opportunity: a node near d=0.2 whose chain is long
opp = int(np.argmin(np.abs(d-0.21) + (parent < 0)*9))
chain = [opp]
while parent[chain[-1]] >= 0: chain.append(int(parent[chain[-1]]))
# global arcs: from cap edge nodes to land dots far away
arcs = []
src = np.where(d > 0.3)[0]
for k in range(240):
    a = nodes[rng.choice(src)]; b = P[rng.integers(len(P))]
    if np.arccos(np.clip(a@b, -1, 1)) < 0.5: continue
    arcs.append([a.round(5).tolist(), b.round(5).tolist()])
r = lambda x: np.round(x, 5).tolist()
json.dump({'land': r(P.ravel()), 'land_ang': r(ang), 'nodes': r(nodes.ravel()), 'd': r(d), 'parent': parent.tolist(),
           'chain': chain, 'arcs': arcs, 'north': r(north)}, open(sys.argv[1] if len(sys.argv) > 1 else 'data.json', 'w'))
print('nodes', M, 'chain', len(chain), 'arcs', len(arcs), 'north', north.round(3))
