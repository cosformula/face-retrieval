import os
import uuid

import falcon
from peewee import JOIN

from . import const
from .hook import set_list_query
from .models import Retrieval, Library, Distance, User


class Collection(object):

    @falcon.before(set_list_query)
    def on_get(self, req, resp):
        select = Retrieval.select(Retrieval, Library, User)\
            .join(Library, JOIN.LEFT_OUTER)\
            .switch(Retrieval)\
            .join(User, JOIN.LEFT_OUTER)\
            .order_by(Retrieval.id)
        retrieves = select.paginate(req.query.page, req.query.limit)
        resp.media = {
            'items': [retrieve.to_json() for retrieve in retrieves],
            'total': select.count()
        }
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        library = Library.get_by_id(req.media.get('libraryID'))
        user = User.get_by_id(1)
        distance = Distance.get_by_id(req.media.get('distanceID'))
        max_iteration_faces = req.media.get('maxIterationFaces')
        max_iteration = req.media.get('maxIteration')
        strategy = req.media.get('strategy')
        retrieve = Retrieval.create(
            user=user, library=library, strategy=strategy,
            distance=distance, max_iteration_faces=max_iteration_faces)
        os.makedirs(os.path.join(const.LIBRARY_PATH, library.name,
                                 'retrieves', str(retrieve.id), 'targets'))
        retrieve.distance.get_distances()
        resp.media = {'id': retrieve.id.hex}


class Item(object):

    def on_get(self, req, resp, retrieval_id):
        retrieve = Retrieval.get_or_none(id=uuid.UUID(retrieval_id))
        resp.media = {**retrieve.to_json(),
                      'iterations': [iteration.to_json() for iteration in retrieve.iterations],
                      'distance': retrieve.distance.to_json(),
                      'targetUrl': '/'.join(['/api', 'retrieves', retrieval_id, 'targets', retrieve.target]) if retrieve.target else ''
                      }
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, retrieval_id):
        pass
