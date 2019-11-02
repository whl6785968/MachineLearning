# -*- coding: utf-8 -*-
"""
Created on Fri Sep  6 15:40:00 2019

@author: dell
"""

import cv2
import os
import numpy as np
import sys
import errno


def read_images(path,sz=None):
    c = 0
    X,y = [],[]
    for dirname,dirnames,filenames in os.walk(path):
        for subdirname in dirnames:
            subject_path = os.path.join(dirname,subdirname)
            print(subject_path)
            for filename in os.listdir(subject_path):
                try:
                    if(filename == ".directory"):
                        continue
                    filepath = os.path.join(subject_path,filename)
                    im = cv2.imread(os.path.join(subject_path,filename),cv2.IMREAD_GRAYSCALE)
                    if(im is None):
                        print("image " + filepath + " is none")
                    else:
                        print(im)
                    if(sz is not None):
                        im = cv2.resize(im,(200,200))
                    
                    X.append(np.asarray(im,dtype=np.uint8))
                    y.append(c)
                except (IOError,(errno)):
                    print("I/O error({0})".format(errno))
                except:
                    print("Unexpected error:",sys.exc_info()[0])
                    raise
            print(c)
            c = c + 1
    print(y)
    return [X,y]

def face_rec():
    names = ['焦亚杰的父亲','焦亚杰']
    if len(sys.argv) < 2:
        print("参数长度错误")
        sys.exit()
    print(sys.argv[1])
    [X,y] = read_images(sys.argv[1])
    y = np.asarray(y,dtype=np.int32)
    if(len(sys.argv) == 3):
        out_dir = sys.argv[2]
    model = cv2.face.EigenFaceRecognizer_create()
    model.train(np.asarray(X),np.asarray(y))
    camera = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('C:/Users/dell/Desktop/python/opencv/cascades/haarcascade_frontalface_default.xml')
    while(True):
        read,img = camera.read()
        print("img is " + str(img))
        faces = face_cascade.detectMultiScale(img,1.3,5)
        for (x,y,w,h) in faces:
            img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            print("img is " + str(img))
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            roi = gray[x:x+w,y:y+h]
            try:
                roi = cv2.resize(roi,(200,200),interpolation=cv2.INTER_LINEAR)
                params = model.predic(roi)
                cv2.putText(img,names[params[0]],(x,y-20),cv2.FONT_HERSHEY_SIMPLEX,1,255,2)
            except:
                continue
        cv2.imshow("camera",img)            
        if(cv2.waitKey(int(1000/12)) & 0xff==ord('q')):
            break
    cv2.destroyAllWindows()
       
if __name__ == "__main__":
    face_rec()