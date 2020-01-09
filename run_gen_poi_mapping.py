"""
gen_poi_mapping.py
===================================================
Generate POI mapping dict and save it as pickle file.
(tag_key, tag_val): [0..12]
Ex: ("amenity", "fuel"): 0
which means it is class 1 of 12 POI feature classes.
"""

import pickle

from pathlib import Path
from osminfo.poi import POI

def save_pickle(path, obj):
    """
    save obj as picke file in path.
    """
    path = Path(path)
    if not path.parent.exists():
        path.parent.mkdir()
    path.write_bytes(pickle.dumps(obj))

PICKLE_PATH = '../pickle_data/poi_mapping_dict.pickle'

# POI divided standard is written in poi.py
POI_ = POI()

# Translate POI classes to dict
D = POI_.trans_poi_class_to_dict()

# Save the dict as pickle file
save_pickle(PICKLE_PATH, D)
