import falcon
import json
from .models import Retrieval, Iteration, User
from .algorithms import update_probability_distribution, get_next_iteration_random, get_next_iteration_similarity, get_next_iteration_entropy
from . import const, utils
import os


class Collection(object):

    def on_get(self, req, resp):
        retrieves = Retrieval.select(Retrieval, User).join(User)
        resp.media = [{
            'id': retrieve.id,
            'user': retrieve.user,
            'status': retrieve.status
        } for retrieve in retrieves]
        resp.status = falcon.HTTP_200

    def on_post(self, req, resp, retrieval_id):
        no = req.media.get('no')
        answer = req.media.get('answer')
        retrieval = Retrieval.get_by_id(retrieval_id)
        library = retrieval.library
        distance = retrieval.distance
        last_distribution = None
        if no == 0:
            photos = distance.photos_list
            photos_length = len(photos)
            avaerage_distribution = 1 / photos_length
            distribution = [
                avaerage_distribution for i in range(photos_length)]
            last_distribution = distribution
        else:
            answer = distance.photos_list.index(answer)
            last_iteration = Iteration.get(retrieval=retrieval, no=no-1)
            last_distribution = last_iteration.distribution
            options = last_iteration.options
            # print(last_distribution,options,answer)
            distribution = update_probability_distribution(
                distance.get_distances(), last_distribution.copy(), options, answer)
        if retrieval.strategy == 'random':
            options = get_next_iteration_random(
                no, distribution, retrieval.max_iteration_faces)
        elif retrieval.strategy == 'similarity':
            options = get_next_iteration_similarity(
                no, distribution, retrieval.max_iteration_faces
            )
        elif retrieval.strategy == 'entropy':
            options = get_next_iteration_entropy(
                no, distribution, retrieval.max_iteration_faces, distance.get_distances()
            )
        option_indexes = [option[1] for option in options]
        iteration = Iteration.get_or_create(
            retrieval=retrieval, no=no)[0]
        iteration.distribution = distribution
        iteration.options = option_indexes
        iteration.answer = answer
        iteration.save()
        retrieval.iterator_pointer = no
        retrieval.save()
        resp.media = [
            {
                'url': '/'.join(['/api', 'photos', library.name,
                                 distance.photos_list[index]]),
                'status': {
                    'prob': distribution[index],
                    'lastProb': last_distribution[index]
                },
                'name': distance.photos_list[index]
            } for index in option_indexes
        ]


class Item(object):

    def on_get(self, req, resp, id):
        retrieve = Retrieval.get_or_none(id=id)
        resp.media = {
            'id': retrieve.id,
            'user': retrieve.user,
            'status': retrieve.status,
            'rounds': retrieve.rounds
        }
        resp.status = falcon.HTTP_200

    def on_patch(self, req, resp, id):
        pass

    def on_delete(self, req, resp, id):
        pass
