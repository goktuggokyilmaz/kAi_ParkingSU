import requests as req
import json 
import time

def get_image_from_cam1():
    # GET IMAGE FROM CAMERA 1
    img = True #eq.get() 
    return img

def process_image(img):
    # PROCESS IMAGE USING YOLO
    # RETURN RESULT JSON
    result = True
    return result

if __name__ == '__main__':  
  while True:
    img = get_image_from_cam1()
    process_image(img)
    # update database
    time.sleep(10)
   