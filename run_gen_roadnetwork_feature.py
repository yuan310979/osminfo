import pickle
import os

from pathlib import Path
from osminfo import OSMInfo
from pprint import pprint as pp
from tqdm import tqdm



def divide_ways_by_classes(cs, ways):
    ret = [ [] for _ in range(len(cs)+1) ]
    for way_id, way_val in ways.items():
        if 'highway' in way_val['tag']:
            for idx, c in enumerate(cs):
                for _c in c:
                    if _c == way_val['tag']['highway']:
                        ret[idx].append(way_val)
        else:
            ret[-1].append(way_val)
    return ret
                
osm = OSMInfo()
osm.load_osm_grids_from_pickle('../pickle_data/BJ_grids_full.pickle')

class1 = ['motorway', 'trunk', 'motorway_link', 'trunk_link']
class2 = ['primary', 'secondary', 'tertiary', 'primary_link', 'secondary_link', 'tertiary_link']

ret = {}

for k, v in tqdm(osm.grids.items()):
    len_rf, len_rc, len_ro = 0.0, 0.0, 0.0
    freeway, common, others = divide_ways_by_classes([class1, class2], v['way']) 

    osm.import_nodes(v['node'])

    for wf in tqdm(freeway):
        len_rf += osm.get_way_length_by_dict(wf)
    for wc in tqdm(common):
        len_rc += osm.get_way_length_by_dict(wc)
    for wo in tqdm(others):
        len_ro += osm.get_way_length_by_dict(wo)

    ret[k] = {}
    ret[k]['count'] = (len(freeway), len(common), len(others))
    ret[k]['length'] = (len_rf, len_rc, len_ro)

save_pickle('../input_feature/road_network.pickle', ret)
