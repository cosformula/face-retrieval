# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 09:42:24 2018

@author: 79136
"""
import os
import matplotlib.image as mpimg
import numpy as np
from scipy import misc
import math
import dlib

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

def reggeo2(nhei,nwid,neye,srcpath,despath,markpath):
    neye=array(neye)
    #create the file path and name and read out source data
    if os.path.exists(despath)==False:
        os.mkdir(despath)
    
    dic={}
    file=open(markpath)
    for i in file.readlines():
        tem=i.strip().split()
        name=tem[0]
        dic[name]=array([[float(tem[2]),float(tem[1])],[float(tem[4]),float(tem[3])]])
    
    
    num=1
    totalnum=len(os.listdir(srcpath))
    for a in os.listdir(srcpath):
        if 'txt' not in a:
            filename = a
            srcfile  = srcpath+filename
            desfile  = despath+filename
            #obtain image data
            srcimg = mpimg.imread(srcfile)
            srcimg = srcimg/256
            
            hei=srcimg.shape[0]
            wid=srcimg.shape[1]
            img = zeros((hei,wid,3))
            img[:,:,0]=srcimg
            img[:,:,1]=srcimg
            img[:,:,2]=srcimg
            
    #        #find feature point
    #        ei=[]
    #        ej=[]
    #        ni=[]
    #        nj=[]
    #        mi=[]
    #        mj=[]
    #        for i in range(len(mrkimg)):
    #            for j in range(len(mrkimg[0])):
    #                if mrkimg[i,j,0]==0 and mrkimg[i,j,1]==0 and mrkimg[i,j,2]==255:
    #                    ei.append(i)
    #                    ej.append(j)
    #                else if mrkimg[i,j,0]==0 and mrkimg[i,j,1]==255 and mrkimg[i,j,2]==0:
    #                    ni.append(i)
    #                    nj.append(j)
    #                else if mrkimg[i,j,0]==255 and mrkimg[i,j,1]==0 and mrkimg[i,j,2]==0:
    #                    mi.append(i)
    #                    mj.append(j)
    #        einum=len(ei)
    #        ejnum=len(ej)
    #        ninum=len(ni)
    #        njnum=len(nj)
    #        minum=len(mi)
    #        mjnum=len(mj)
    #        res=[a,einum,ejnum,ninum,njnum,minum,mjnum]
    #        eye=zeros((2,2))
    #        nose=zeros((1,2))
    #        mouth=zeros((1,2))
    #        
    #        #eye coordinate
    #        k=1
    #        eye[k,0]=eye[k,0]+ei[0]
    #        eye[k,1]=eye[k,1]+ej[1]
    #        count=1
    #        for ii in range(1:ejnum):
    #            ecur=ej[ii]
    #            epre=ej[ii-1]
    #            if (ecur-epre)>1:
    #                eye[k,0] = eye[k,0]/count
    #                eye[k,1] = eye[k,1]/count
    #                count=0
    #                k=k+1
    #            eye[k,0]=eye[k,0]+ei[ii]
    #            eye[k,1]=eye[k,1]+ej[ii]
    #            count=count+1
    #        eye[k,0] = eye[k,0]/count
    #        eye[k,1] = eye[k,1]/count
    #        
    #        #nose coordinate
    #        k=1
    #        nose[k,0]=nose[k,0]+ni[0]
    #        nose[k,1]=nose[k,1]+nj[1]
    #        count=1
    #        for ii in range(1:njnum):
    #            ncur=nj[ii]
    #            npre=nj[ii-1]
    #            if (ncur-npre)>1:
    #                nose[k,0] = nose[k,0]/count
    #                nose[k,1] = nose[k,1]/count
    #                count=0
    #                k=k+1
    #            nose[k,0]=nose[k,0]+ni[ii]
    #            nose[k,1]=nose[k,1]+nj[ii]
    #            count=count+1
    #        nose[k,0] = nose[k,0]/count
    #        nose[k,1] = nose[k,1]/count
    #        
    #        #mouth coordinate 
    #        k=1
    #        mouth[k,0]=mouth[k,0]+mi[0]
    #        mouth[k,1]=mouth[k,1]+mj[1]
    #        count=1
    #        for ii in range(1:mjnum):
    #            mcur=mj[ii]
    #            mpre=mj[ii-1]
    #            if (mcur-mpre)>1:
    #                mouth[k,0] = mouth[k,0]/count
    #                mouth[k,1] = mouth[k,1]/count
    #                count=0
    #                k=k+1
    #            mouth[k,0]=mouth[k,0]+mi[ii]
    #            mouth[k,1]=mouth[k,1]+mj[ii]
    #            count=count+1
    #        mouth[k,0] = mouth[k,0]/count
    #        mouth[k,1] = mouth[k,1]/count
    #        
    #        edis   = norm(eye[0,:]-eye[1,:])
    #        endis  = norm(sum(eye)/2-nose)
    #        emdis  = norm(sum(eye)/2-mouth)
    #        nnose[:,0] = neye[0,0]+ endis*nmdis/emdis
            
            #rotation the image for display
            if dic[filename][0][0]==dic[filename][1][0]:
                angle = 0
            else:
                angle = math.atan((dic[filename][0][1]-dic[filename][1][1])/(dic[filename][0][0]-dic[filename][1][0]))
                if angle>=0:
                    angle=(3.1415926/2-angle)
                else:
                    angle=-(3.1415926/2+angle)  
            #obtain the new coordinates of feature points
            icenter=srcimg.shape[0]
            jcenter=srcimg.shape[1]
            icenter = icenter/2;
            jcenter = jcenter/2;
            #eyes
            for ii in range(2):
                pointy = -(dic[filename][ii][0]-icenter)
                pointx = dic[filename][ii][1]-jcenter
                rou=math.sqrt(pointx*pointx+pointy*pointy)
                theta = math.atan(pointy/pointx)
                if pointx>=0 and pointy<0:
                    theta = 2*3.1415926+theta
                if pointx<0:
                    theta = 3.1415926+theta
                if pointx==0 and pointy==0:
                    theta = 0
                theta=theta+angle
                dic[filename][ii][1] = rou*cos(theta)+jcenter;
                dic[filename][ii][0] = -rou*sin(theta)+icenter;
            
            #rotate the images
            midimg = misc.imrotate(img,angle*180/3.1415926)
            midimg = midimg/256
            #obtain LSM parameter
            edisn      = norm(neye[0,:]-neye[1,:])
            ediso      = norm(dic[filename][0]-dic[filename][1])
            x1         = sum(neye[:,0])/2
            y1         = sum(dic[filename][:,0])/2
            x2         = zeros((2,2))
            x2[:,1]    = 1
            x2[0:2,0]  = neye[:,1]
            y2         = zeros((2,1)) 
            y2[0:2,0]  = dic[filename][:,1]
            beta1      = mat([ediso/edisn,y1-x1*ediso/edisn]).T
            beta2      = inv(x2.T@x2)@x2.T@y2
            #interpolation with bicubic
            desimg = ones((nhei,nwid,3))
            for ii in range(nhei):
                for jj in range(nwid):
                    xi  = array([ii,1])@beta1
                    xj  = array([jj,1])@beta2
    
                    iii = int(fix(float(xi)))
                    jjj = int(fix(float(xj)))
                    
                    #bicubic interpolation
                    if iii-1<0 or jjj-1<0 or iii+3>hei or jjj+3>wid:
                        desimg[ii,jj,0] = 1
                        desimg[ii,jj,1] = 1
                        desimg[ii,jj,2] = 0
                    else:
                        patch = midimg[iii-1:iii+3,jjj-1:jjj+3,0]
                        wx    = abs(array([iii-1,iii,iii+1,iii+2]) - float(xi))
                        wy    = abs(array([jjj-1,jjj,jjj+1,jjj+2]) - float(xj))
                        wx    = func(wx)
                        wy    = func(wy)          
                        temp  = wx*patch*wy.T
                        if temp>1:
                            temp = 1
                        if temp<0:
                            temp = 0
                       
                        desimg[ii,jj,:] = temp
            #imshow(desimg)
            mpimg.imsave(desfile,desimg)
            img=mpimg.imread(desfile)
            print(num/totalnum)
            num+=1
        
        
def func(x):
    [d,dim]=mat(x).shape

    if d!=1:
        print(1,'input error')
    f = zeros((d,dim))
    for i in range(dim):
        if x[i]>=0 and x[i]<1:
            f[0][i] = 1-2*x[i]*x[i]+x[i]*x[i]*x[i]
        elif x[i]>=1 and x[i]<2:
            f[0][i] = 4-8*x[i]+5*x[i]*x[i]-x[i]*x[i]*x[i]
        else:
            f[0][i] = 0
    return mat(f)

def get_normalizepicture(srcpath,despath,predictorpath='hape_predictor_68_face_landmarks.dat'):#src源图片 des标准化后的图片 predictor人脸检测文件
    findeye(srcpath,srcpath,predictorpath)
    nhei=160
    nwid=140
    neye=[[62,42],[62,98]]
    markpath=srcpath+'eyePosition.txt'
    reggeo2(nhei,nwid,neye,srcpath,despath,markpath)
    
    
if __name__=='__main__':
    srcpath = 'F:\\study in school\\2018夏季实习\\Normal\\'
    despath = 'F:\\study in school\\2018夏季实习\\Change2\\'
    predictorpath='D:\\dlib\\shape_predictor_68_face_landmarks.dat'
    get_normalizepicture(srcpath,despath,predictorpath)
