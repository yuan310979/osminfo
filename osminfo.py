import requests
import re
import multiprocessing as mp

from tqdm import tqdm
from bs4 import BeautifulSoup
from math import sin, cos, sqrt, atan2, radians
from pprint import pprint as pp
from typing import Tuple

class OSMInfo:

    #  def __init__(self):

    def get_node_latlon(self, node_id: str) -> Tuple[float, float]:
        url = f'https://api.openstreetmap.org/api/0.6/node/{node_id}'
        r = requests.get(url)
        lat = re.findall(r'lat=\"([^\"]*)\"', r.text)[0]
        lon = re.findall(r'lon=\"([^\"]*)\"', r.text)[0]
        return float(lat), float(lon)

    def get_way_length(self, way_bs4):
        length = 0.0
        nds = way_bs4.find_all('nd')
        nds = [ n['ref'] for n in nds ]
        latlon = [ self.get_node_latlon(nd) for nd in nds ]

        # multiprocessing
        arg_index = [[*(latlon[index]), *(latlon[index+1])] for index in range(len(latlon) - 1)]
        p = mp.Pool(8)
        result_list = p.starmap(self.latlon_distance, arg_index) 
        p.close()
        p.join()
        return sum(result_list) 

    def get_ways_by_grid(self, lon:float, lat:float, grid_size:float=0.01):
        url = f'https://api.openstreetmap.org/api/0.6/map?bbox={lon},{lat},{lon+grid_size},{lat+grid_size}'
        r = requests.get(url)
        soup = BeautifulSoup(r.text, 'xml')
        return soup.find_all('way')

    @staticmethod
    def latlon_distance(lon1:float, lat1:float, lon2:float, lat2:float) -> float:
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
    ways = osm.get_ways_by_grid(120.98, 24.81, 0.01)
    for w in tqdm(ways):
        d = osm.get_way_length(w)
        print(d)
