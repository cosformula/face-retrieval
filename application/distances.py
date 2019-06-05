import json

import falcon
from peewee import JOIN

# from .utils import generate_feature, calculate_distance
from .hook import set_list_query
from .models import Distance, Library, Feature
from .tasks import init_distance


# def get_distances():
#     pass


class Collection(object):

    @falcon.before(set_list_query)
    def on_get(self, req, resp):
        lib_id = req.get_param('libraryID', None)
        if lib_id is not None:
            select = Distance.select(Distance, Library).where(
                Distance.library == lib_id)
        else:
            select = Distance.select(Distance, Library)
        select = select.join(Library, JOIN.LEFT_OUTER).order_by(Distance.id)
        distances = select.paginate(req.query.page, req.query.limit)
        resp.media = {
            'total': select.count(),
            'items': [
                {
                    **distance.to_json(),
                    'library': distance.library.to_json()
                } for distance in distances]
        }
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        library = Library.get_or_none(id=req.media.get('libraryId'))
        feature = Feature.get_or_none(id=req.media.get('featureId'))
        distance, created = Distance.get_or_create(
            name=req.media.get("name")+'.csv', library=library,
            feature=feature,
            from_temp=req.media.get('file'),
            available=False,
            status='initializing',
            algorithm=req.media.get('algorithm'),)

        init_distance(distance)

        resp.status = falcon.HTTP_200
        resp.media = distance.to_json()
        # library = Library.get_or_none(id=req.media.get('libraryId'))
        # library_name = library.name
        # libray_path = os.path.join(const.LIBRARY_PATH, library_name)
        # distance_name = req.media.get("name")
        # photos_list = []
        # if req.media.get('type') == 'import':
        #     file_name = os.path.join(const.TEMP_PATH, req.media.get('file'))

        #     # validate file
        #     with open(file_name, 'r') as f:
        #         photos_list = f.readline()
        #     photos_set = set(photos_list)
        #     library_photos_set = set(library.photos)
        #     if not photos_set.issubset(library_photos_set):
        #         print('该距离文件不是此人脸库的子集')

        #     # copy file
        #     copyfile(file_name, os.path.join(
        #         const.LIBRARY_PATH, 'distances', f'{distance_name}.dat'))
        # else:
        #     dest_path = os.path.join(libray_path, 'distances', distance_name)
        #     get_distances(libray_path, dest_path)
        #     # feature = generate_feature(libray_path)
        #     # distance = calculate_distance(feature)
        #     # with open('eggs.csv', 'wb') as csvfile:
        #     #     spamwriter = csv.writer(csvfile, delimiter=' ',
        #     #                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #     #     spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
        #     #     spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])

        # distance, created = Distance.get_or_create(
        #     name=distance_name, library=library, photos_list=photos_list)

        # resp.status = falcon.HTTP_200
        # resp.media = distance.to_json()


class Item(object):

    def on_get(self, req, resp, id):
        distance = Distance.get_or_none(id=id)
        doc = {
            'id': distance.id,
            'name': distance.name
        }
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200
