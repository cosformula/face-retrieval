import json
import mimetypes
import os

import falcon

from . import const


class Collection(object):

    def on_get(self, req, resp, library):
        path = os.path.join(const.LIBRARY_PATH, library)
        if not os.path.isdir(path):
            resp.status = falcon.HTTP_404
            return

        photos = os.listdir(os.path.join(path, 'photos'))
        doc = [
            {'href': '/'.join(['photos', library, photo])} for photo in photos
        ]

        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200


class Item(object):

    def __init__(self, image_store):
        self._image_store = image_store

    def on_get(self, req, resp, library, name):
        resp.content_type = mimetypes.guess_type(name)[0]
        resp.stream, resp.stream_len = self._image_store.open(
            os.path.join(library, 'photos', name))

    # def on_post(self, req, resp, lib)
