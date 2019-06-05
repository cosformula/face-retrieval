import falcon
from peewee import JOIN

from .hook import set_list_query
from .models import Library, Feature
# from .utils import generate_feature, calculate_distance
from .tasks import init_feature


# def get_distances():
#     pass

# def serializer():


class Collection(object):

    @falcon.before(set_list_query)
    def on_get(self, req, resp):
        lib_id = req.get_param('libraryID', None)
        if lib_id is not None:
            select = Feature.select(Feature, Library).order_by(Feature.created_at.desc()).where(
                Feature.library == lib_id)
        else:
            select = Feature.select(Feature, Library).order_by(
                Feature.created_at.desc())
        select = select.join(Library, JOIN.LEFT_OUTER).order_by(Feature.id)
        features = select.paginate(req.query.page, req.query.limit)
        resp.media = {
            'total': select.count(),
            'items': [
                {
                    **feature.to_json(),
                    'library': feature.library.to_json()
                } for feature in features]
        }
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        library = Library.get_or_none(id=req.media.get('libraryId'))

        feature, created = Feature.get_or_create(
            name=req.media.get("name")+'.csv', library=library,
            from_temp=req.media.get('file'),
            available=False,
            status='initializing',
            algorithm=req.media.get('algorithm'),)

        init_feature(feature)

        resp.status = falcon.HTTP_200
        resp.media = {
            **feature.to_json(), 'library': feature.library.to_json()}


class Item(object):

    def on_get(self, req, resp, id):
        feature = Feature.get_or_none(id=id)
        resp.body = feature.to_json()
        resp.status = falcon.HTTP_200
