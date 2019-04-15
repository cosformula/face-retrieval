
from playhouse.db_url import connect
from playhouse.pool import PooledPostgresqlExtDatabase
import os
from . import const
db = connect(const.DB)


def get_feature_path(library_name, feature_name):
    return os.path.join(const.LIBRARY_PATH, library_name, 'features', feature_name)


def get_photo_path(library_name, photo_name):
    return os.path.join(const.LIBRARY_PATH, library_name, 'photos', photoname)


def get_distance_path(library_name, distance_name):
    return os.path.join(const.LIBRARY_PATH, library_name, 'distances', distance_name)


def generate_feature(libarary_path):
    pass


def calculate_distance(feature):
    pass
