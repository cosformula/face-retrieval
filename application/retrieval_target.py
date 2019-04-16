import json
import os
import falcon
import mimetypes
from . import const
from .models import Retrieval
import random


class Collection(object):

    def __init__(self, image_store):
        self._image_store = image_store

    def on_get(self, req, resp, retrieval_id):
        # if not os.path.isdir(path):
        #     resp.status = falcon.HTTP_404
        #     return

        # photos = os.listdir(path)
        # path_prefix = '/'.join(['retrieves', retrieval_id, 'targets'])
        # resp.media = [
        #     {'href': '/'.join([path_prefix, photo])} for photo in photos
        # ]
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp, retrieval_id):
        retrieval = Retrieval.get_or_none(id=retrieval_id)
        library = retrieval.library
        path = os.path.join(library.retrieves_path, retrieval_id, 'targets')
        os.makedirs(path)
        image = req.get_param('file')
        if image is not None:
            name = self._image_store.save(path, image.file, image.type)
        else:
            photos = library.photos
            index = req.media.get('index') or random.randrange(0, len(photos))
            photo_name = photos[index]
            fd = os.open(os.path.join(library.photos_path, photo_name))
            name = self._image_store.save(
                path, fd, mimetypes.guess_type(photo_name)[0])
        retrieval.target = name
        retrieval.save()
        resp.status = falcon.HTTP_200
        resp.media = {
            'targetUrl': '/'.join(['/api', 'retrieves', retrieval_id, 'targets', name])
        }
        # resp.content_type = mimetypes.guess_type(name)[0]
        # resp.stream, resp.stream_len = self._image_store.open(
        #     os.path.join(path, name))


class Item(object):

    def __init__(self, image_store):
        self._image_store = image_store

    def on_get(self, req, resp, retrieval_id, target_name):
        retrieval = Retrieval.get_or_none(id=retrieval_id)
        library = retrieval.library
        path = os.path.join(library.retrieves_path, retrieval_id, 'targets')
        resp.content_type = mimetypes.guess_type(target_name)[0]
        resp.stream, resp.stream_len = self._image_store.open(
            os.path.join(path, target_name))
