# import falcon


def validate_image_type(req, resp, resource, params):
    pass
    # if req.content_type not in ALLOWED_IMAGE_TYPES:
    #     msg = 'Image type not allowed. Must be PNG, JPEG, or GIF'
    #     raise falcon.HTTPBadRequest('Bad request', msg)


class ListQuery(object):
    def __init__(self, params):
        self.page = int(params.get('page', 1))
        self.limit = int(params.get('limit', 10))


def set_list_query(req, resp, resource, params):
    req.query = ListQuery(req.params)
