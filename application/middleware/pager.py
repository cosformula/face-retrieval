import random


class ListqueryMiddleware(object):
    def process_request(self, req, resp):
        req.list_query = {}
        req.list_query['page'] = int(req.params.get('page', 1))
        req.list_query['limit'] = int(req.params.get('limit', 10))
