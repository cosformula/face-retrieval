import mimetypes
import os

import falcon

from . import const


class Collection(object):

    def __init__(self, store):
        self._store = store

    def on_get(self, req, resp,):
        path = const.TEMP_PATH
        if not os.path.isdir(path):
            resp.status = falcon.HTTP_404
            return

        files = os.listdir(os.path.join(path))
        resp.media = [
            {'href': '/'.join(['files', file])} for file in files
        ]

        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        # name = self._store.save(req.stream, req.content_type)
        # resp.location = '/images/' + name
        file = req.get_param('file')
        if file is not None:
            name = self._store.save('',file.file, file.type)
        resp.status = falcon.HTTP_201
        resp.media = {
            'file': name
        }

class Item(object):

    def __init__(self, store):
        self._store = store

    def on_get(self, req, resp, file_name):
        resp.content_type = mimetypes.guess_type(file_name)[0]
        resp.stream, resp.stream_len = self._store.open(file_name)
