import pickle

from pathlib import Path
from osminfo import OSMInfo
from pprint import pprint as pp

def save_pickle(path, obj):
    path = Path(path)
    if not path.parent.exists():
        path.parent.mkdir()
    path.write_bytes(pickle.dumps(obj))

def load_pickle(path):
    path = Path(path)
    return pickle.load(path.open('rb'))

poi_mapping = load_pickle('../pickle_data/poi_mapping_dict.pickle')

osm = OSMInfo()
osm.load_osm_grids_from_pickle('../pickle_data/TW_grids_full.pickle')

ret = {}

for k, v in osm.grids.items():
    poi_feature = [0] * 12
    for _, n in v['node'].items():
        if 'tag' in n:
            for tk, tv in n['tag'].items():
                key = (tk, tv)
                if key in poi_mapping:
                    poi_feature[poi_mapping[key]-1] += 1
    for _, w in v['way'].items():
        if 'tag' in w:
            for tk, tv in w['tag'].items():
                key = (tk, tv)
                if key in poi_mapping:
                    poi_feature[poi_mapping[key]-1] += 1
    for _, r in v['relation'].items():
        if 'tag' in r:
            for tk, tv in r['tag'].items():
                key = (tk, tv)
                if key in poi_mapping:
                    poi_feature[poi_mapping[key]-1] += 1
    ret[k] = poi_feature

    save_pickle('../input_feature/poi.pickle', ret)
