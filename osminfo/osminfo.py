import requests
import re
import pickle
import multiprocessing as mp
import pickle
import logging
import bs4

from tqdm import tqdm
from bs4 import BeautifulSoup
from pprint import pprint as pp
from typing import Tuple
from time import sleep
from pathlib import Path

from osminfo.utils import latlon_distance
from osminfo.poi import POI

# Initiate Logger
logger = logging.getLogger(__name__)


class OSMInfo:

    def __init__(self):
        self.nd_latlon = None
        self.error_keys = []
        self.grids = None
        self.nodes = None

    def load_osm_grids_from_pickle(self, path='../pickle_data/TW_grids_full.pickle'):
        path = Path(path)
        self.grids = pickle.load(Path(path).open('rb'))

    def import_nodes(self, nds):
        self.nodes = nds

    def get_err_keys(self):
        return self.error_keys

    def get_nearest_grid(self, lat, lon):
        lat = round(lat, 2)
        lon = round(lon, 2)
        try:
            return self.grids[(lat, lon)]
        except Exception as e:
            logger.error("[Error]\t(get_nearest_grid)\tGrid (%f, %f) is not found.", lat, lon)

    """
    def get_node_latlon(self, node_id: str) -> Tuple[float, float]:
        url = f'https://api.openstreetmap.org/api/0.6/node/{node_id}'
        r = requests.get(url)
        lat = re.findall(r'lat=\"([^\"]*)\"', r.text)[0]
        lon = re.findall(r'lon=\"([^\"]*)\"', r.text)[0]
        return float(lat), float(lon)
    """


    def get_way_length_by_dict(self, way):
        nds = way['node']
        if len(nds) > 1:
            latlon = [ (float(self.nodes[id]['lat']), float(self.nodes[id]['lon'])) for id in nds ]
            result_list = [latlon_distance(latlon[i][0], latlon[i][1], latlon[i+1][0], latlon[i+1][1]) for i in range(len(latlon)-1)]
            return sum(result_list) 
        else:
            return 0.0

    def get_way_length(self, way_bs4):
        nds = way_bs4.find_all('nd')
        nds = [ n['ref'] for n in nds ]
        if len(nds) > 1:
            latlon = [ self.nd_latlon[id] for id in nds ]
            result_list = [latlon_distance(latlon[i][0], latlon[i][1], latlon[i+1][0], latlon[i+1][1]) for i in range(len(latlon)-1)]
            return sum(result_list) 
        else:
            return 0.0


    def get_elements_by_grid(self, lat: float, lon: float, grid_size: float=0.01) -> Tuple[bs4.element.ResultSet]:
        # Validat input
        assert lat <= 90 and lat >= -90 and lon <= 180 and lon >= -180
        url = f'https://api.openstreetmap.org/api/0.6/map?bbox={lon},{lat},{lon+grid_size},{lat+grid_size}'

        try:
            r = requests.get(url)
        except Exception as e:
            logger.error("Error URL: %s \n", url)
            self.error_keys.append((lat, lon))
            sleep(10)
            return [], [], []

        soup = BeautifulSoup(r.text, 'xml')
        nodes = soup.find_all('node')
        ways = soup.find_all('way')
        relations = soup.find_all('relation')
        return (nodes, ways, relations)


    def divide_ways_by_three_classes(self, way_bs4: bs4.element.ResultSet) -> Tuple[float]:
        # Setup three scale of ways from large to small
        class1 = ['motorway', 'trunk', 'motorway_link', 'trunk_link']
        class2 = ['primary', 'secondary', 'tertiary', 'primary_link', 'secondary_link', 'tertiary_link']
        ret1, ret2, ret3 = [], [], []
        for way in way_bs4:
            if way.find('tag'):
                logger.info(way.tag['v'])
                if way.tag['v'] in class1:
                    ret1.append(way)
                elif way.tag['v'] in class2:
                    ret2.append(way)
                else:
                    ret3.append(way)
        return (ret1, ret2, ret3)


    def build_nodes_data(self, node_bs4):
        """
        Build a lookup table that enable further usage
        ex: calculate distance between two nodes while getting length of ways
        """
        ret = {}
        for nd in node_bs4:
            ret[nd['id']] = [ float(nd['lat']), float(nd['lon']) ]
        return ret


    def get_roadnetwork_grid_data(self, lat: float, lon: float, step: float) -> Tuple[float]:
        nodes, ways, relations = self.get_elements_by_grid(lat, lon, step)

        # Setup lookup table of each node
        self.nd_latlon = self.build_nodes_data(nodes)
        freeway, common, others = self.divide_ways_by_three_classes(ways) 

        # freeway
        len_rf, len_rc, len_ro = 0.0, 0.0, 0.0
        for wf in tqdm(freeway):
            len_rf += self.get_way_length(wf)
        for wc in tqdm(common):
            len_rc += self.get_way_length(wc)
        for wo in tqdm(others):
            len_ro += self.get_way_length(wo)
        return (len_rf, len_rc, len_ro)

    def get_nodes_full_data(self, nodes):
        ret = {}
        for n in nodes:
            tmp_node = {'lon': n['lon'], 'lat': n['lat']} 
            tags = n.find_all('tag')
            tag_dict = {} 
            for t in tags:
               tag_dict[t['k']] = t['v'] 
            tmp_node['tag'] = tag_dict
            ret[n['id']] = tmp_node 
        return ret

    def get_ways_full_data(self, ways):
        ret = {}
        for w in ways:
            tag_dict = {}
            for t in w.find_all('tag'):
               tag_dict[t['k']] = t['v'] 
            node_list = [ n['ref'] for n in w.find_all('nd') ]
            ret[w['id']] = {'tag': tag_dict, 'node': node_list}
        return ret

    def get_relation_full_data(self, relations):
        ret = {}
        for r in relations:
            tag_dict = {}
            for t in r.find_all('tag'):
               tag_dict[t['k']] = t['v'] 

            node_list = []
            way_list = []
            relation_list = []
            for m in r.find_all('member'):
                m_type = m['type']
                if m_type == 'node':
                    node_list.append(m['ref'])
                elif m_type == 'way':
                    way_list.append(m['ref'])
                elif m_type == 'relation':
                    relation_list.append(m['ref'])
            ret[r['id']] = {'tag': tag_dict, 'node': node_list, 'way': way_list, 'relation': relation_list}
        return ret

    
    def get_poi_grid_data(self, lat: float, lon: float, step: float) -> Tuple[int]:
        _POI = POI()
        grid = self.get_full_grid_data(lat, lon, step)
        poi_mapping = _POI.trans_poi_class_to_dict()
        poi_feature = [0] * 12

        for _, n in grid['node'].items():
            if 'tag' in n:
                for tk, tv in n['tag'].items():
                    key = (tk, tv)
                    if key in poi_mapping:
                        poi_feature[poi_mapping[key]-1] += 1
        for _, w in grid['way'].items():
            if 'tag' in w:
                for tk, tv in w['tag'].items():
                    key = (tk, tv)
                    if key in poi_mapping:
                        poi_feature[poi_mapping[key]-1] += 1
        for _, r in grid['relation'].items():
            if 'tag' in r:
                for tk, tv in r['tag'].items():
                    key = (tk, tv)
                    if key in poi_mapping:
                        poi_feature[poi_mapping[key]-1] += 1
        return poi_feature
    

    def get_full_grid_data(self, lat, lon, step):
        nodes, ways, relations = self.get_elements_by_grid(lat, lon, step)
        nodes = self.get_nodes_full_data(nodes)
        ways =  self.get_ways_full_data(ways)
        relations = self.get_relation_full_data(relations)
        return {'node': nodes, 'way': ways, 'relation': relations}


if __name__ == '__main__':
    osm = OSMInfo()
    #  d = osm.latlon_distance(50.0359, 5.4253, 58.3838, 3.0412)
    d = osm.get_roadnetwork_grid_data(120.90, 25.00, 0.01)
    # osm.load_osm_grids_from_pickle('../pickle_data/TW_grids_full.pickle')
    # d = osm.get_nearest_grid(lat=23.432342342, lon=121.12112)
    pp(d)
