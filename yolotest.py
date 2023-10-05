#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parkinglot capacities project
YOLO TEST COD

@author: Goktug Gokyilmaz
"""
import cv2
from ultralytics import YOLO
import numpy as np
import os
import json

#TO Check if mps avalible
# import torch
# print(torch.backends.mps.is_available())


image = cv2.imread('image.png')
jsonname = "YM1"+".json"
if os.path.exists(jsonname):
    print(f"The file '{jsonname}' exists.")
    
    with open(jsonname, "r") as file:
        coordinate_groups = json.load(file)
    for x in range(len(coordinate_groups)):
        cv2.polylines(image, [np.array(coordinate_groups[x][2::])], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.putText(image, str(coordinate_groups[x][0]), (int(coordinate_groups[x][1][0][0]) ,int(coordinate_groups[x][1][0][1])), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
else:
    print(f"The file '{jsonname}' does not exist.")

model = YOLO("yolov8m.pt")

# Display the image in a window

results = model(image,device="mps")#WE CAN add device="0"  Nvidia for processing with gpu in MAC its mps
result = results[0]

bboxes = np.array(result.boxes.xyxy.cpu(),dtype = "int")
classes = np.array(result.boxes.cls.cpu(),dtype = "int")
for bbox, clss in zip(bboxes,classes):
    (x,y,x2,y2) = bbox
    #print("x=",x,y,x2,y2)
    #cv2.rectangle(image,(x,y),(x2,y2),(0,255,0),5)
    cv2.circle(image, ( x, y ), 4, (0, 255, 0), -1)
    cv2.putText(image,str(clss),(x,y-5),cv2.FONT_HERSHEY_PLAIN,2,(0,255,0),2)
cv2.imshow('Img', image)
print(bboxes)
cv2.startWindowThread()
print(cv2.waitKey(0))
cv2.destroyAllWindows()
for i in range(2):
    cv2.waitKey(1)