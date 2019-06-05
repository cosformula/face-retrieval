# -*- coding: utf-8 -*-
"""
Created on Mon Jul  9 16:26:26 2018

@author: 79136
"""

import os

import dlib
import matplotlib.image as mpimg
import numpy as np


def findeye(srcpath,markpath,predictorpath):
    
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(predictorpath)
        
    if os.path.exists(markpath)==False:
        os.mkdir(markpath)
    
    filename=markpath+'eyePosition.txt'
    file=open(filename,'w')
    for i in os.listdir(srcpath):
        if 'txt' not in i:
            path=srcpath+i
            img=mpimg.imread(path)
            image= np.array(img)
            dets = detector(image, 1)
            for index,face in enumerate(dets):
                shape = predictor(image, face)
                left=[0,0]
                right=[0,0]
                for k in range(36,42):
                    left[0]+=shape.part(k).x
                    left[1]+=shape.part(k).y
                    right[0]+=shape.part(k+6).x
                    right[1]+=shape.part(k+6).y
                left=np.array(left)/6
                right=np.array(right)/6
                file.write(i+" ")
                file.write(str(round(left[0]))+" "+str(round(left[1]))+" "+str(round(right[0]))+" "+str(round(right[1])))
                file.write("\n") 
    file.close()
    
if __name__=="__main__":
    srcpath = 'F:\\study in school\\2018夏季实习\\Normal\\'
    markpath= 'F:\\study in school\\2018夏季实习\\'    
    findeye(srcpath,markpath)
    