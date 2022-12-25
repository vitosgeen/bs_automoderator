
import base64
import os
import cv2
import pytesseract
import imutils
import numpy as np
import argparse
import shutil, sys
from PIL import Image
from urllib.parse import urlparse
import urllib.request
from urllib.request import urlopen

import requests

class Utils:
        
    def create_dir_images(self):
        mode = 0o777
        dir_exists = os.path.exists('images')
        if dir_exists == True:
            return dir_exists
        os.mkdir('images', mode)

    def remove_dir_images(self):
        shutil.rmtree('images', ignore_errors=True)
    
    def download_image(self, imgurl):
        a = urlparse(imgurl)
        basenameUrl = os.path.basename(a.path)
        print(imgurl)
        full_path = "images/" + basenameUrl
        file_exists = os.path.exists(full_path)
        if file_exists == True:
            return full_path        
        try:
            img_bytes = self.get_request_image(imgurl=imgurl)
        except:
            print('download_image error')  
            return False

        try:
            with open(full_path, "wb") as binary_file:
                binary_file.write(img_bytes)
        except:
            print('download_image save to file error')
            
        
        file_size = os.path.getsize(full_path)
        if file_size == 0:
            os.remove(full_path)
            return False
        return full_path

    def get_request_image(self, imgurl):
        r = requests.get(imgurl, timeout=5)
        return r.content

    def validate_image(self, img_path):
        img = Image.open(img_path)
        if img.format == None:
            print('validate_image file error', img_path)
        return img.format
        

    def detect_text(self, image_path):
        textstr = ""
        try:
            img_cv2 = cv2.imread(image_path)
            text = pytesseract.image_to_string(img_cv2)
            textstr = str(text).strip()
        except:
            print('text image loading error')
        cv2.destroyAllWindows()
        return textstr
        
    def detect_humans(self, image_path):
        HOGCV = cv2.HOGDescriptor()
        person = 0
        HOGCV.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        try:
            image = cv2.imread(image_path)
        except:
            print('person image loading error')
            cv2.destroyAllWindows()
            return person
        # image = imutils.resize(image, width = min(400, image.shape[1])) 
        try:
            bounding_box_cordinates, weights =  HOGCV.detectMultiScale(image, winStride = (8, 8), padding = (32, 32), scale = 1.5, useMeanshiftGrouping=False)
        except:
            print('person detectMultiScale error')
            cv2.destroyAllWindows()
            return person

        for i, (x, y, w, h) in enumerate(bounding_box_cordinates):
            if weights[i] < 0.7 and weights[i] > 0.3:
                person += 1
            if weights[i] > 0.7:
                person += 1
            
        cv2.destroyAllWindows()
        return person
        
    def detect_faces(self, image_path):
        faces_len = 0
        cascPath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)
        try:
            image = cv2.imread(image_path)
        except:
            print('faces image loading error')
            cv2.destroyAllWindows()
            return faces_len
        try:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(80, 80)
            )
        except:
            print('faces detectMultiScale error')
            cv2.destroyAllWindows()
            return faces_len

        faces_len = len(faces)
        cv2.destroyAllWindows()
        return faces_len
        
    def detect_vehicles(self, image_path):
        car = 0
        try:
            image = Image.open(image_path)
            # image = image.resize((450,250))
            image_arr = np.array(image)
            grey = cv2.cvtColor(image_arr,cv2.COLOR_BGR2GRAY)   
            Image.fromarray(grey)
            blur = cv2.GaussianBlur(grey,(5,5),0)
            Image.fromarray(blur)
            dilated = cv2.dilate(blur,np.ones((3,3)))
            Image.fromarray(dilated)
            car_cascade_src = "cars.xml"
            car_cascade = cv2.CascadeClassifier(car_cascade_src)
            cars = car_cascade.detectMultiScale(dilated, 1.1, 1)
            cv2.destroyAllWindows()
            # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
            # closing = cv2.morphologyEx(dilated, cv2.MORPH_CLOSE, kernel) 
            # Image.fromarray(closing)
        except:
            print('vehicle image loading error')
            cv2.destroyAllWindows()
            return car
        
        for (x,y,w,h) in cars:
            car += 1

        cv2.destroyAllWindows()
        return car
        #https://www.analyticsvidhya.com/blog/2021/12/vehicle-detection-and-counting-system-using-opencv