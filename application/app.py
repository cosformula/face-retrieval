import os
import os

import falcon
from falcon_multipart.middleware import MultipartMiddleware

from . import const, iterations, libraries, photos, retrieves, distances, users, retrieval_target, files, auth, features
from .image_store import ImageStore
from .models import Distance, Library, User, create_tables, Feature
from .utils import db


def refresh_libs():
    lib_dir = const.LIBRARY_PATH
    libs = os.listdir(lib_dir)
    for lib_name in libs:
        if not os.path.isdir(os.path.join(lib_dir, lib_name)):
            continue
        library, created = Library.get_or_create(name=lib_name)
        photos = os.listdir(library.photos_path)
        library.count = len(photos)
        library.photos = photos
        library.save()
        features = os.listdir(library.features_path)
        for feature_name in features:
            if feature_name[0] == '.':
                continue
            fp = os.path.join(library.features_path, feature_name)
            with open(fp, 'r') as f:
                for line in f:
                    photos_list = line.split()
                    break
            print(feature_name)
            feature, created = Feature.get_or_create(
                name=feature_name, library=library)
            feature.save()
        
        distances = os.listdir(library.distances_path)
        for distance_name in distances:
            if distance_name[0] == '.':
                continue
            fp = os.path.join(library.distances_path, distance_name)
            with open(fp, 'r') as f:
                for line in f:
                    photos_list = line.split()
                    break
            print(distance_name)
            distance, created = Distance.get_or_create(
                name=distance_name, library=library)
            distance.photos_list = photos_list
            distance.save()


def init_system():
    admin, created = User.get_or_create(username='admin', password='')

# async def async_task():


create_tables()
refresh_libs()
init_system()
# add(1, 2)


class PeeweeConnectionMiddleware(object):
    def process_request(self, req, resp):
        db.connect(reuse_if_open=True)
        pass

    def process_response(self, req, resp, resource):
        if not db.is_closed():
            db.close()
        pass


# falcon.API(middleware=[MultipartMiddleware()])
api = application = falcon.API(middleware=[
    MultipartMiddleware(),
    # ListqueryMiddleware()
    # PeeweeConnectionMiddleware(),
    # falcon_jsonify.Middleware(help_messages=True),
    # ... other middlewares ...
])


library_image_store = ImageStore(const.LIBRARY_PATH)

# routes = [
#     ['/libraries', libraries.Collection()],
#     ['/libraries/{name}', libraries.Item()],
#     ['/users', users.Collection()],
#     []

# ]

# libraries API
api.add_route('/libraries', libraries.Collection())
api.add_route('/libraries/{id}', libraries.Item())

# users API
api.add_route('/users', users.Collection())
api.add_route('/users/{username}', users.Item())

# auth API
api.add_route('/auth/login', auth.Login())
api.add_route('/auth/logout', auth.Logout())

# distances API
api.add_route('/distances', distances.Collection())
api.add_route('/distances/{id}', distances.Item())

# photos API
api.add_route('/photos/{library}', photos.Collection())
api.add_route('/photos/{library}/{name}', photos.Item(library_image_store))

# iterations API
api.add_route('/retrieves/{retrieval_id}/iterations', iterations.Collection())
api.add_route('/retrieves/{retrieval_id}/iterations/{no}', iterations.Item())

# target API
retrieval_image_store = ImageStore(const.LIBRARY_PATH)
api.add_route('/retrieves/{retrieval_id}/targets',
              retrieval_target.Collection(retrieval_image_store))
api.add_route('/retrieves/{retrieval_id}/targets/{target_name}',
              retrieval_target.Item(retrieval_image_store))

# retrieves API
api.add_route('/retrieves', retrieves.Collection())
api.add_route('/retrieves/{retrieval_id}', retrieves.Item())

# features API
api.add_route('/features', features.Collection())
api.add_route('/features/{feature_id}', features.Item())


# temp files API
temp_files_store = ImageStore(const.TEMP_PATH)

api.add_route('/files', files.Collection(temp_files_store),)
api.add_route('/files/{file_name}', files.Item(temp_files_store))
