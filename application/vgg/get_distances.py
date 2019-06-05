# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 09:42:24 2018

@author: 79136
"""

import math

import numpy as np
import torch
import torchvision.models
from PIL import Image
from torchvision import transforms

# vffface
def vector_vggface(files):
    vggface = torchvision.models.vgg19_bn(pretrained=True)
    vggface.classifier = torch.nn.Sequential(
        *list(vggface.classifier.children())[:-3])
    vectors = []
    for filepath in files:
        image = Image.open(filepath)
        image = image.resize((224, 224))

        image_array = np.array(image)

        inp = transforms.ToTensor()(image_array[:, :, :3]).unsqueeze(0)
        vectors.append(vggface(inp))

    return vectors

# resnet50
def vector_resnet50(files):
    resnet50 = torchvision.models.resnet50(pretrained=True)
    resnet50.fc = torch.nn.Sequential(*list(resnet50.fc.children())[:-1])
    vectors = []
    for filepath in files:
        print(filepath)
        image = Image.open(filepath)
        image = image.resize((224, 224))

        image_array = np.array(image)

        inp = transforms.ToTensor()(image_array[:, :, :3]).unsqueeze(0)
        vectors.append(resnet50(inp))

    return vectors


def scd(vector):
    l = len(vector)
    distances = np.zeros((l, l))
    # i<j
    for i in range(l):
        for j in range(l):
            numerator = abs(vector[i][0]-vector[j][0])
            denominator = vector[i][0]+vector[j][0]
            distances[i][j] = float(torch.sum(numerator/denominator))
            print((i*l+j+1)/(l*l))

    return distances


def cos(vector):
    l = len(vector)
    distances = np.zeros((l, l))
    # i<j
    for i in range(l):
        for j in range(l):
            numerator = torch.sum(vector[i][0]*vector[j][0])
            denominator = math.sqrt(torch.sum(
                vector[i][0]*vector[i][0]))*math.sqrt(torch.sum(vector[j][0]*vector[j][0]))
            distances[i][j] = float(numerator/denominator)
            print((i*l+j+1)/(l*l))

    return distances


# src输入文件 des距离矩阵路径 feature特征 dis距离模式
def get_distances(srcpath, despath, feature=vector_resnet50, dis_method=scd):
    names, vectors = feature(srcpath)
    distance = dis_method(vectors)
    path = despath+str(feature).split()[1] + \
        str(dis_method).split()[1]+'distanceResult.txt'
    np.savetxt(path, distance, header=' '.join(names),
               comments='', newline='\r\n', fmt='%f')


if __name__ == "__main__":
    srcpath = 'F:\\study in school\\data mining\\PROJ\\images\\test\\'
    despath = 'F:\\study in school\\data mining\\PROJ\\images\\'

    get_distances(srcpath, despath, feature=vector_resnet50, dis_method=scd)
