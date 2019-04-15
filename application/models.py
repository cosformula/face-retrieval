from peewee import *
from playhouse.postgres_ext import *
from datetime import datetime
from . import const
import os
from .utils import db, get_distance_path, get_photo_path
from functools import lru_cache
import uuid
from .tasks import init_library
retrieval_strategies = {
    'random': None,
    'most_similar': None,
    'entropy': None
}


class BaseModel(Model):
    created_at = DateTimeField(default=datetime.now)
    updated_at = DateTimeField(default=datetime.now)

    class Meta:
        database = db


class User(BaseModel):
    username = CharField(unique=True, index=True)
    password = CharField()
    is_admin = BooleanField(default=False, index=True)

    def to_json(self):
        return {
            'userName': self.username,
            'isAdmin': self.is_admin
        }


class Library(BaseModel):
    # id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(unique=True, index=True)
    detail = TextField(default='')
    available = BooleanField(default=True, index=True)
    hash = CharField(null=True)
    status = CharField(default='ok')
    photos = ArrayField(CharField, null=True)
    from_temp = CharField(default='')
    count = IntegerField(default=0)
    # cover =

    def init_library(self):
        init_library(self)

    # def init_folders(self):
    #     folders = ['photos', 'distances', 'retrivieves', 'features']
    #     photo_folder = os.path.join(self.path, 'photos')

    #     # init library data
    #     for folder in folders:
    #         path = os.path.join(self.path, folder)
    #         os.makedirs(os.path.join(path)) if not os.path.isdir(path) else ...

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'detail': self.detail,
            'isAvailable': self.available,
            'hash': self.hash,
            'count': self.count,
            'cover': '/'.join(['photos', self.name, self.photos[0]]) if self.count > 0 else ''
        }

    # def get_photo(self, filename):
    #     pass

    @property
    def path(self):
        return os.path.join(const.LIBRARY_PATH, self.name)

    @property
    def photos_path(self):
        return os.path.join(self.path, 'photos')

    @property
    def features_path(self):
        return os.path.join(self.path, 'features')

    @property
    def distances_path(self):
        return os.path.join(self.path, 'distances')

    def get_photos(self):
        photos = os.listdir(self.get_path(), 'photos')
        return sorted(photos)

        # self.distances_path, feature_name)

    # def import_feature(self, ):
    #     pass

    # def import_distance(self):
    #     pass


# class Algorithm(BaseModel):
#     name = CharField()


class Feature(BaseModel):
    name = CharField(unique=True, index=True)
    # algorithm = ForeignKeyField(Algorithm, backref='features')
    library = ForeignKeyField(Library, backref='features')
    algorithm = CharField(default='')
    parameters = JSONField(null=True)
    available = BooleanField(default=True, index=True)
    from_temp = CharField(default='')
    progress = IntegerField(default=0)
    status = CharField(default='')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'available': self.available,
            'status': self.status
        }

    # def init_feature(self, algorithm, feature_name):
    # self.status = '正在计算...'
    # self.save()
    # names, vectors = algorithm(self.library.photos_path, step)
    # self.status = '计算完成，正在生成文件...'

    # self.status = '整理中...'
    # self.save()
    # , os.path.join(
    # @staticmethod


class Distance(BaseModel):
    # id = UUIDField(primary_key=True, default=uuid.uuid4)
    name = CharField(unique=True, index=True)
    detail = TextField(default='')
    hash = CharField(null=True)
    feature_name = CharField(null=True)
    feature = ForeignKeyField(Feature, backref='distances', null=True)
    library = ForeignKeyField(Library, backref='distances')
    algorithm = CharField(default='')
    # photos_map = JSONField(null=True)
    photos_list = ArrayField(CharField, null=True)
    from_temp = CharField(default='')

    # timestamp = DateTimeField(default=datetime.now)
    available = BooleanField(default=True, index=True)
    status = CharField(default='')

    def to_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'detail': self.detail,
            'hash': self.hash,
            'libraryID': self.library.id,
            'available': self.available
        }

    def fp(self):
        return get_distance_path(self.library.name, self.name)

    @lru_cache(None)
    def get_distances(self):
        distances = []
        with open(self.fp(), 'r') as f:
            for i, line in enumerate(f):
                if i != 0:
                    distances.append(
                        list(map(lambda x: float(x), line.split())))
        return distances

    def get_distance_of_photo_index(self, index):
        with open(self.fp(), 'r') as f:
            for i, line in enumerate(f):
                if i == index:
                    distances = list(map(lambda x: float(x), line.split()))
                    break
        return distances

    def get_distance_of_photo(self, photo_name):
        photos_list = []
        photo_index = 0
        # vectors = np.recfromtxt(feature_file_path, delimiter=",", skip_header=1)
        with open(self.fp(), 'r') as f:
            for i, line in enumerate(f):
                if i == 0:
                    photos_list = f.readline().split()
                    photo_index = photos_list.index(photo_name)
                if i == photo_index:
                    distances = list(map(lambda x: float(x), line.split()))
                    break
        return distances


class Retrieval(BaseModel):
    id = UUIDField(primary_key=True, default=uuid.uuid4)
    user = ForeignKeyField(User, backref='retrieves', index=True)
    remark = TextField(default='')
    library = ForeignKeyField(Library, backref='retrieves')
    distance = ForeignKeyField(Distance, backref='retrieves')
    strategy = CharField(default='random')
    max_iteration = IntegerField(default=8)
    status = CharField(default='pending')
    target = CharField(null=True)
    ended_at = DateTimeField(default=datetime.now)
    # photos = ArrayField(CharField)
    max_iteration_faces = IntegerField(default=16)
    iterator_pointer = IntegerField(default=0)

    def get_next_round(self, selected):
        if len(self.rounds) >= self.max_round:
            return []

    def to_json(self):
        return {
            'id': self.id.hex,
            'user': self.user.to_json(),
            'remark': self.remark,
            'library': self.library.to_json(),
            'strategy': self.strategy,
            'maxIteration': self.max_iteration,
            'status': self.status,
            'maxIterationFaces': self.max_iteration_faces,
            'iteratorPointer': self.iterator_pointer
        }


class Iteration(BaseModel):
    # id = UUIDField(primary_key=True, default=uuid.uuid4)
    retrieval = ForeignKeyField(Retrieval, backref='iterations')
    no = IntegerField()
    distribution = ArrayField(FloatField, default=lambda: [])
    options = ArrayField(IntegerField, default=lambda: [])
    answer = CharField(null=True)

    class Meta:
        primary_key = CompositeKey('retrieval', 'no')

    def to_json(self):
        return {
            'retrievalID': self.retrieval.id,
            'no': self.no,
            'options': self.options,
            'answer': self.answer
        }


def create_tables():
    with db:
        db.create_tables(
            [User, Library, Feature, Distance, Retrieval, Iteration])
