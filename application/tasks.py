
from huey import RedisHuey, crontab
import os
from . import const
import zipfile
import mimetypes
import csv
from shutil import copyfile
import numpy as np
import math
from .vgg import vector_resnet50, vector_vggface
huey = RedisHuey('face-retrieval', host='redis')

feature_algo = {
    'resnet50': vector_resnet50,
    'vggface': vector_vggface
}


def scd(vector):
    l = len(vector)
    distances = np.zeros((l, l))
    # i<j
    for i in range(l):
        for j in range(l):
            numerator = abs(vector[i]-vector[j])
            denominator = vector[i]+vector[j]
            distances[i][j] = float(np.sum(numerator/denominator))
            # print((i*l+j+1)/(l*l))

    return distances


def cos(vector):
    l = len(vector)
    distances = np.zeros((l, l))
    # i<j
    for i in range(l):
        for j in range(l):
            # numerator = np.sum(vector[i]*vector[j])
            # denominator = math.sqrt(np.sum(vector[i]*vector[i]))*math.sqrt(np.sum(vector[j]*vector[j]))
            # distances[i][j] = 1 - float(numerator/denominator)
            # print((i*l+j+1)/(l*l))
            distances[i][j] = 1 - np.dot(vector[i], vector[j])/(np.linalg.norm(vector[i])*(np.linalg.norm(vector[j])))
    return distances


distance_algo = {
    'cos': cos,
    'scd': scd
}


@huey.task()
def add(a, b):
    print('add')
    return a+b


@huey.task()
def init_library(library):
    folders = ['photos', 'distances', 'retrieves', 'features']

    # init library data
    for folder in folders:
        path = os.path.join(library.path, folder)
        os.makedirs(os.path.join(path)) if not os.path.isdir(path) else ...

    file_path = os.path.join(const.TEMP_PATH, library.from_temp)
    photo_folder = library.photos_path
    zip_file = zipfile.ZipFile(file_path)

    # extract images from zipfile
    for name in zip_file.namelist():
        is_temp_file = name.startswith('__MACOSX')
        file_type = mimetypes.guess_type(name)[0]
        is_image_file = file_type and file_type.find('image') != -1
        if not is_temp_file and is_image_file:
            zip_file.extract(name, photo_folder)
            # flatten
            os.rename(os.path.join(photo_folder, name), os.path.join(
                photo_folder, name.replace('/', '_')))

    # delete dirs
    dirs = [o for o in os.listdir(photo_folder) if os.path.isdir(
        os.path.join(photo_folder, o))]
    for dir_name in dirs:
        os.rmdir(os.path.join(photo_folder, dir_name))

    # create library object
    photos = os.listdir(photo_folder)

    library.photos = photos
    library.count = len(photos)
    library.status = 'ready'
    library.is_available = True
    library.save()
    return True


@huey.task()
def init_feature(feature):
    library = feature.library
    if feature.from_temp:
        file_name = os.path.join(const.TEMP_PATH, feature.from_temp)

        # validate file
        with open(file_name, 'r') as f:
            photos_list = f.readline()
        photos_set = set(photos_list)
        library_photos_set = set(library.photos)
        if not photos_set.issubset(library_photos_set):
            print('该距离文件不是此人脸库的子集')

        # copy file
        copyfile(file_name, os.path.join(
            const.LIBRARY_PATH, 'features', f'{feature.name}.dat'))
    else:
        try:
            names = list(filter(lambda x: not x.startswith('.'), os.listdir(library.photos_path)))
            names.sort()
            files = map(lambda x: os.path.join(library.photos_path, x), names)
            feature_fun = feature_algo[feature.algorithm]
            vector = feature_fun(files)

            feature_path = os.path.join(
                library.features_path, feature.name)

            array = list(map(lambda x: x[0].detach().numpy(), vector))
            np.savetxt(feature_path, array, header=' '.join(
                names), newline='\r\n', delimiter=' ', fmt='%f', comments='')
        except BaseException as e:
            print(e)
            feature.status = 'error'
            feature.save()
        else:
            feature.available = True
            feature.status = 'ready'
            feature.save()
        # .detach().numpy()
        # with open(feature_path, 'w', newline='') as csvfile:
        #     spamwriter = csv.writer(csvfile, delimiter=',',
        #                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #     spamwriter.writerow(names)
        #     for row in vector:
        #         spamwriter.writerow(row[0].detach().numpy())


@huey.task()
def init_distance(distance):
    library = distance.library
    if distance.from_temp:
        file_name = os.path.join(const.TEMP_PATH, distance.from_temp)

        # validate file
        with open(file_name, 'r') as f:
            photos_list = f.readline()
        photos_set = set(photos_list)
        library_photos_set = set(library.photos)
        if not photos_set.issubset(library_photos_set):
            print('该距离文件不是此人脸库的子集')

        # copy file
        copyfile(file_name, os.path.join(
            const.LIBRARY_PATH, 'distances', f'{distance.name}.dat'))
    else:
        feature_file_path = os.path.join(
            library.features_path, distance.feature.name)
        names = []
        with open(feature_file_path) as f:
            names = f.readline().split()

        vectors = np.recfromtxt(feature_file_path, delimiter=" ", skip_header=1)

        distance_vector = distance_algo[distance.algorithm](vectors)

        distance_path = os.path.join(library.distances_path, distance.name)

        # np.savetxt(feature_path, vector.numpy(), header=' '.join(names),
        #            comments='', newline='\r\n', fmt='%f')
        print(distance_vector)
        np.savetxt(distance_path, distance_vector, header=' '.join(names), newline='\r\n', delimiter=' ', fmt='%f', comments='')

        # with open(distance_path, 'w', newline='') as csvfile:
        #     spamwriter = csv.writer(csvfile, delimiter=' ',
        #                             quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #     print(names)
        #     spamwriter.writerow(names)
        #     for row in distance_vector:
        #         spamwriter.writerow(row)

        distance.available = True
        distance.status = 'ready'
        distance.photos_list = names
        distance.save()
