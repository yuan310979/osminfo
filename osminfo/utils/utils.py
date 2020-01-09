import os
import pickle
import logging
import logging.config

from pathlib import Path
from math import sin, cos, sqrt, atan2, radians
from typing import Optional

# Initiate Logger
logger = logging.getLogger(__name__)


def setup_logging(log_path: Optional[str] = None, level: str = "DEBUG"):
    handlers_dict = {
        "console_handler": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
            "level": "DEBUG",
            "stream": "ext://sys.stdout"
        }
    }

    if log_path is not None:
        safe_dir(log_path, with_filename=True)
        handlers_dict["file_handler"] = {
            "class": "logging.FileHandler",
            "formatter": "full",
            "level": "DEBUG",
            "filename": log_path,
            "encoding": "utf8"
        }

    # Configure logging
    config_dict = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "simple": {
                "format": "[ %(asctime)s ] %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
            },
            "full": {
                "format": "[ %(asctime)s ] %(levelname)s - %(name)s:%(funcName)s:%(lineno)d - %(message)s"
            }
        },
        "handlers": handlers_dict,
        "loggers": {
            "osminfo": {
                "level": level,
                "handlers": list(handlers_dict.keys())
            },
            "__main__": {
                "level": level,
                "handlers": list(handlers_dict.keys())
            },
        }
    }

    # Deal with dual log issue
    logging.basicConfig(level=logging.WARNING)
    logging.getLogger().handlers[0].setLevel(logging.WARNING)

    logging.config.dictConfig(config_dict)
    logger.info("Setup Logging!")


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


def safe_dir(path: str, with_filename: bool = False) -> str:
    dir_path = os.path.dirname(path) if with_filename else path
    if not os.path.exists(dir_path):
        logger.info("Dir %s not exist, creating directory!", dir_path)
        os.makedirs(dir_path)
    return os.path.abspath(path)


def save_pickle(path, obj):
    path = Path(path)
    if not path.parent.exists():
        path.parent.mkdir()
    path.write_bytes(pickle.dumps(obj))


def load_pickle(path):
    path = Path(path)
    return pickle.load(path.open('rb'))