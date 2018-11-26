import requests
import re
import multiprocessing as mp

from tqdm import tqdm
from bs4 import BeautifulSoup
from math import sin, cos, sqrt, atan2, radians
from pprint import pprint as pp
from typing import Tuple

class OSMInfo:

    def __init__(self):
        self.nd_latlon = None

    """
    def get_node_latlon(self, node_id: str) -> Tuple[float, float]:
        url = f'https://api.openstreetmap.org/api/0.6/node/{node_id}'
        r = requests.get(url)
        lat = re.findall(r'lat=\"([^\"]*)\"', r.text)[0]
        lon = re.findall(r'lon=\"([^\"]*)\"', r.text)[0]
        return float(lat), float(lon)
    """

    def get_way_length(self, way_bs4):
        nds = way_bs4.find_all('nd')
        nds = [ n['ref'] for n in nds ]
        if len(nds) > 1:
            latlon = [ self.nd_latlon[id] for id in nds ]
            result_list = [self.latlon_distance(latlon[i][0], latlon[i][1], latlon[i+1][0], latlon[i+1][1]) for i in range(len(latlon)-1)]
            return sum(result_list) 
        else:
            return 0.0

    def get_elements_by_grid(self, lat:float, lon:float, grid_size:float=0.01):
        url = f'https://api.openstreetmap.org/api/0.6/map?bbox={lon},{lat},{lon+grid_size},{lat+grid_size}'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'xml')
        nodes = soup.find_all('node')
        ways = soup.find_all('way')
        return nodes, ways 

    def divide_ways_by_three_classes(self, way_bs4):
        class1 = ['motorway', 'trunk', 'motorway_link', 'trunk_link']
        class2 = ['primary', 'secondary', 'tertiary', 'primary_link', 'secondary_link', 'tertiary_link']
        ret1, ret2, ret3 = [], [], []
        for way in way_bs4:
            if way.find('tag'):
                if way.tag['v'] in class1:
                    ret1.append(way)
                elif way.tag['v'] in class2:
                    ret2.append(way)
                else:
                    ret3.append(way)
        return ret1, ret2, ret3

    def build_nodes_data(self, node_bs4):
        ret = {}
        for nd in node_bs4:
            ret[nd['id']] = [ float(nd['lat']), float(nd['lon']) ]
        return ret

    def get_roadnetwork_grid_data(self, lat, lon, step):
        nodes, ways = self.get_elements_by_grid(lat, lon, 0.01)
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

    @staticmethod
    def latlon_distance(lat1:float, lon1:float, lat2:float, lon2:float) -> float:
        # Ref: https://www.movable-type.co.uk/scripts/latlong.html 
        R = 6371.0
        phi1 = radians(lat1)
        phi2 = radians(lat2)
        phi = radians(lat2-lat1)
        sigma = radians(lon2-lon1)

        a = sin(phi/2)**2 + cos(phi1) * cos(phi2) * sin(sigma/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1-a))

        return R * c

if __name__ == '__main__':
    osm = OSMInfo()
    d = osm.latlon_distance(50.0359, 5.4253, 58.3838, 3.0412)
    d = osm.get_roadnetwork_grid_data(120.90, 25.00, 0.01)
    pp(d)
