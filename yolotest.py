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
from shapely.geometry import Polygon

rgb_red = (0,0,255)
rgb_green = (0,255,0)
rgb_purple = (255,20,147)
cv_font = cv2.FONT_HERSHEY_PLAIN
#TO Check if mps avalible
# import torch
# print(torch.backends.mps.is_available())

def detectlot(camera_angle,filepath):
    image = cv2.imread(filepath)
    json_name = camera_angle+".json"
    bol_json_name= "bollean"+camera_angle+".json"
    lot_bools=[]
    coordinate_groups=[]
    if os.path.exists(json_name):
        print(f"The file '{json_name}' exists.")
        
        with open(json_name, "r") as file:
            coordinate_groups = json.load(file)
        # for x in range(len(coordinate_groups)):
        #     cv2.polylines(image, [np.array(coordinate_groups[x][3::])], isClosed=True, color=(0, 255, 0), thickness=2)
        #     cv2.putText(image, str(coordinate_groups[x][0]), (int(coordinate_groups[x][1][0][0]) ,int(coordinate_groups[x][1][0][1])), cv_font, 2, rgb_green, 2)
    else:
        print(f"The file '{json_name}' does not exist.")
    
    model = YOLO("yolov8m.pt")
    print(coordinate_groups[1])
    # Display the image in a window
    
    results = model(image,device="mps")#WE CAN add device="0"  Nvidia for processing with gpu in MAC its mps
    result = results[0]
    
    bboxes = np.array(result.boxes.xyxy.cpu(),dtype = "int")
    classes = np.array(result.boxes.cls.cpu(),dtype = "int")
    for bbox, clss in zip(bboxes,classes):
        if clss in [2,7]: #YOLO checks for person etc so we are interested in persons only
            (x,y,x2,y2) = bbox
            cv2.rectangle(image,(x,y),(x2,y2),rgb_green,5)
            # cx= int((x2+x)/2)
            # cy= int((y2+y)/2)+20
            # cv2.circle(image, ( cx, cy ), 4, rgb_purple, -1)
            cord1 = [(x, y), (x2, y), (x2, y2), (x, y2)]
            poly1 = Polygon(cord1)
            cv2.putText(image,str(clss),(x,y-5),cv_font ,2,(0,255,0),2)
            for testlots in range(len(coordinate_groups)):
                poly2 = Polygon(coordinate_groups[testlots][2::][0])
                intersec = poly1.intersection(poly2).area
                iou = int((poly1.area + poly2.area + intersec)/10000)
                print(coordinate_groups[testlots][0], iou)
                if (iou > 70):
                    coordinate_groups[testlots][1] = True
                     #if it finds any overlapping no need to check for other lot spaces
    for x in range(len(coordinate_groups)):
        if coordinate_groups[x][1] == False: #Lot is free (no car)
            cv2.polylines(image, [np.array(coordinate_groups[x][2::])], isClosed=True, color=rgb_green, thickness=2)
            cv2.putText(image, str(coordinate_groups[x][0]), ((coordinate_groups[x][2::][0][1])), cv_font, 2, rgb_green, 2)
        else: #Lot contains car
            cv2.polylines(image, [np.array(coordinate_groups[x][2::])], isClosed=True, color=rgb_red, thickness=2)
            cv2.putText(image, str(coordinate_groups[x][0]), ((coordinate_groups[x][2::][0][1])), cv_font, 2, rgb_red, 2)
    cv2.imshow('Img', image)
    #print(bboxes)
    cv2.startWindowThread()
    for groups in coordinate_groups:
        lot_bools.append((groups[0],groups[2]))
    with open(bol_json_name, "w") as final_file:
        json.dump(lot_bools, final_file)
    print(cv2.waitKey(0))
    cv2.destroyAllWindows()
    for i in range(2):
        cv2.waitKey(1)
        
detectlot("YM1", "image.png")