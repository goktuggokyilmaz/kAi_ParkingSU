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

def perform_object_detection(filepath):
    try:
        model = YOLO("yolov8m.pt")
        results = model(filepath, device="mps")
        result = results[0]
        bboxes = np.array(result.boxes.xyxy.cpu(),dtype = "int")
        classes = np.array(result.boxes.cls.cpu(),dtype = "int")
        confs = np.array(result.boxes.conf.cpu(),dtype = "float32")

        return zip(bboxes,classes,confs) #returns all detected objects as list 
    
    except Exception as e:
        print(f"Error during object detection: {e}")
        return None
    
def read_json_file(jsonfile):
    try:
        with open(jsonfile, "r") as file:
            coordinate_groups = json.load(file)
        return coordinate_groups
    except FileNotFoundError:
        print(f"Error: File '{jsonfile}' not found.")
        return []
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON format in '{jsonfile}'.")
        return []
    
def detectlot(camera_angle,filepath):
    print("Yolo detection module created")
    #image = cv2.imread(filepath)
    json_name = "cords/"+camera_angle+".json"
    bol_json_name= "bools/bollean"+camera_angle+".json"
    lot_bools={}
    coordinate_groups = read_json_file(json_name)
    
    counter = 0
    for bbox, clss, confs in perform_object_detection(filepath): #we call function return list of all detected objects then we one by one check them
        if clss in [2,7]: #YOLO checks for other classes as well such as person.. so we are interested in trucks and cars only
            (x,y,x2,y2) = bbox #we convert cordidantes of object
            cv2.rectangle(filepath,(x,y),(x2,y2),rgb_purple,2)
            cord1 = [(x, y), (x2, y), (x2, y2), (x, y2)]
            poly1 = Polygon(cord1)
            cv2.putText(filepath,str(clss)+"-"+str(counter),(x,y-5),cv_font ,2,(255,0,0),2)
            #cv2.putText(filepath,str(confs),(x-50,y+50),cv_font, 2,(255,255,0) , 2) #Confidence value 
            counter+= 1
            for testlots in range(len(coordinate_groups)):
                poly2 = Polygon(coordinate_groups[testlots][2::][0])
                if poly1.is_valid and poly2.is_valid:
                    intersec = poly1.intersection(poly2).area
                    union = (poly1.area + poly2.area - intersec)
                    iou = intersec/union
                    if (iou > 0.45):
                        coordinate_groups[testlots][1] = True
                     #if it finds any overlapping no need to check for other lot spaces

    for x in range(len(coordinate_groups)):
        if coordinate_groups[x][1] == False: #Lot is free (no car)
            cv2.polylines(filepath, [np.array(coordinate_groups[x][2::])], isClosed=True, color=rgb_green, thickness=2)
            cv2.putText(filepath, str(coordinate_groups[x][0]), ((coordinate_groups[x][2::][0][1])), cv_font, 2, rgb_green, 2)
        else: #Lot contains car
            cv2.polylines(filepath, [np.array(coordinate_groups[x][2::])], isClosed=True, color=rgb_red, thickness=2)
            cv2.putText(filepath, str(coordinate_groups[x][0]), ((coordinate_groups[x][2::][0][1])), cv_font, 2, rgb_red, 2)

    cv2.imshow(str(camera_angle), filepath)
    cv2.startWindowThread()

    for groups in coordinate_groups:
        lot_bools[groups[0]] = groups[1]
    with open(bol_json_name, "w") as final_file:
        json.dump(lot_bools, final_file)
    print(cv2.waitKey(0))
    cv2.destroyAllWindows()
    for i in range(2):
        cv2.waitKey(1)
        
        
def doublecheckmodel(first,second): 
    bol1_json_name= "bools/bollean"+first+".json"
    bol2_json_name= "bools/bollean"+second+".json"
    if os.path.exists(bol1_json_name) and os.path.exists(bol1_json_name):
        with open(bol1_json_name, "r") as file1:
            first_boolvalues = json.load(file1)
        with open(bol2_json_name, "r") as file1:
            second_boolvalues = json.load(file1)
        for x in second_boolvalues:
            first_boolvalues[x] = second_boolvalues[x]
        with open(bol1_json_name, "w") as final_file:
            json.dump(first_boolvalues, final_file)


#doublecheckmodel("UCB_A","UCB_A_1")

# def doublecheckfromotherangle(first,second):
#     print(first)
#     print(second)
        
#detectlot("YM1", "image.png")