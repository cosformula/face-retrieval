import json

import falcon


# from .models import User


class Login(object):

    # def on_get(self, req, resp):
    #     users = User.select()
    #     doc = [{
    #         'username': user.username,
    #         'isAdmin': retrieve.is_admin,
    #     } for user in users]

    #     resp.body = json.dumps(doc, ensure_ascii=False)
    #     resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        username = req.media.get('username', 'admin')
        password = req.media.get('password', 'test')
        # is_admin = req.media.get('isAdmin')
        # user = User.create(
        #     username=username, password=password, is_admin=is_admin)
        resp.media = {
            'roles': ['admin'],
            'introduction': 'I am a super administrator',
            'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            'name': 'Super Admin'
        }


class Logout(object):

    def on_get(self, req, resp, username):
        user = User.get_or_none(username=username)
        # doc = {
        #     'id': retrieve.id,
        #     'userID': retrieve.user.id,
        #     'status': retrieve.status,
        #     'iterations': [iteration.to_json() for iteration in retrieve.iterations]
        # }
        doc = user.to_json()
        resp.body = json.dumps(doc, ensure_ascii=False)
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, retrieval_id):
        pass
