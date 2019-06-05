import shutil

import falcon

from .hook import set_list_query
from .models import Library


class Collection(object):

    @falcon.before(set_list_query)
    def on_get(self, req, resp):
        select = Library.select().order_by(Library.id.desc())
        libraries = select.paginate(req.query.page, req.query.limit)
        resp.media = {
            'total': select.count(),
            'items': [{
                'id': library.id,
                'name': library.name,
                'detail': library.detail,
                'isAvailable': library.available,
                'hash': library.hash,
                'count': library.count,
                'status': library.status,
                'cover': '/'.join(['photos', library.name, library.photos[0]]) if library.count > 0 else ''
            } for library in libraries],
        }
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        library_name = req.media.get('name')
        temp_file = req.media.get('file')
        library = Library.create(
            name=library_name, photos=[], count=0, status="extracting",
            from_temp=temp_file, is_available=False)

        # async task
        library.init_library()

        resp.status = falcon.HTTP_200
        resp.media = library.to_json()


class Item(object):

    def on_get(self, req, resp, id):
        library = Library.get_or_none(id=id)
        resp.media = {
            'id': library.id,
            'name': library.name
        }
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, id):
        library = Library.get_or_none(id=id)

        # delete library data
        shutil.rmtree(library.path, ignore_errors=True)

        # delete relate records too
        library.delete_instance(recursive=True)

        resp.status = falcon.HTTP_200
        resp.media = {'success': True}
