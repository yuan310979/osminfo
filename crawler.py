import pickle
import numpy as np
import multiprocessing as mp

from pathlib import Path
from tqdm import tqdm
from pprint import pprint as pp
from itertools import product
from osminfo import OSMInfo

start_lon = 120.00
start_lat = 21.80
lon_range = 2
lat_range = 3.5
step = 0.01

"""
start_lon = 121.50
start_lat = 25.00
lon_range = 0.1
lat_range = 0.1
step = 0.01
"""

road_data = {}
#grids = None

osm = OSMInfo()

keys = product(np.arange(0, lat_range,step) + start_lat, np.arange(0, lon_range, step) + start_lon)
keys = [(round(key[0], 2), round(key[1], 2)) for key in keys]
#args = [(round(key[0], 2), round(key[1], 2), step) for key in keys]

"""
with mp.Pool(16) as p:
    grids = p.starmap(osm.get_roadnetwork_grid_data, args)
    p.close()
    p.join()

for key, data in zip(keys, grids):
    pp(key, data)
    road_data[key] = data
"""

for key in tqdm(keys):
    road_data[key] = osm.get_roadnetwork_grid_data(key[0], key[1], step)
    
data_path = Path('./data/')
road_data_path = data_path / 'road_network.pickle'

if not data_path.exists():
    data_path.mkdir()

road_data_path.write_bytes(pickle.dumps(road_data))

"""
d = pickle.load(road_data_path.open('rb'))
pp(d)
"""
