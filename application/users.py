import falcon
import json
from .models import User
from . import utils


class Collection(object):

    def on_get(self, req, resp):
        users = User.select()
        # doc = [{
        #     'username': user.username,
        #     'isAdmin': retrieve.is_admin,
        # } for user in users]

        resp.media = {
            'roles': ['admin'],
            'introduction': 'I am a super administrator',
            'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            'name': 'Super Admin'
        }
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp):
        username = req.get_json('username')
        password = req.get_json('password')
        is_admin = req.get_json('isAdmin')
        user = User.create(
            username=username, password=password, is_admin=is_admin)
        resp.json = {'id': user.id}


class Item(object):

    def on_get(self, req, resp, username):
        # user = User.get_or_none(username=username)
        resp.media = {
            'roles': ['admin'],
            'introduction': 'I am a super administrator',
            'avatar': 'https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif',
            'name': 'Super Admin'
            # 'id': retrieve.id,
            # 'userID': retrieve.user.id,
            # 'status': retrieve.status,
            # 'iterations': [iteration.to_json() for iteration in retrieve.iterations]
        }
        resp.status = falcon.HTTP_200

    def on_delete(self, req, resp, retrieval_id):
        pass
