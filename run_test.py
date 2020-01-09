import logging

from pprint import pprint

from osminfo.utils import latlon_distance, setup_logging, cur_time
from osminfo import OSMInfo

# Initiate Logger
logger = logging.getLogger(__name__)

if __name__ == '__main__':
    # Init logging
    setup_logging(f'./logs/{cur_time()}.log', "DEBUG")

    # Calculate distance between two node
    # Arguments: lat1, lon1, lat2, lon2
    d = latlon_distance(50.0359, 5.4253, 58.3838, 3.0412)
    print(d)

    o = OSMInfo()
    r = o.get_poi_grid_data(24,121,0.1)
    logger.info(r)
    # d = o.get_roadnetwork_grid_data(24,121,0.01)
    # logger.debug(d)