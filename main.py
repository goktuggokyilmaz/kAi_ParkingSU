#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parkinglot capacities project

@author: Goktug Gokyilmaz
"""
import cv2
import numpy as np
import json
import os

selected_coordinates = []
paint_select = []
paint_cords = []
coordinate_groups = []
paintmode= False
def createlotspace(camera_angle,filepath):
    global selected_coordinates
    global coordinate_groups
    global paintmode
    # Load the pre-existing image from the file
    image = cv2.imread(filepath)
    jsonname = camera_angle+".json"
    #CORDINATES Are appended SUCH ((AngelName+lotcount),CenterPoints,Booltest,Allpoints)
    # Callback function for mouse click events
    def mouse_callback(event, x, y, flags, param):
        global selected_coordinates
        global paintmode
        global coordinate_groups
        global paint_cords
        global paint_select
    
        if event == cv2.EVENT_LBUTTONDOWN:
            if (paintmode == False):
                selected_coordinates.append((x, y))
                cv2.circle(image, (x, y), 4, (0, 255, 0), -1)
        
                if len(selected_coordinates) == 6:
                    lotname= camera_angle+"-"+str(len(coordinate_groups))
                    booltest = False
                    coordinate_groups.append((lotname,booltest,selected_coordinates.copy()))
                    selected_coordinates = []
                    # Draw green lines connecting the group of four coordinates
                    cv2.polylines(image, [np.array(coordinate_groups[-1][2::])], isClosed=True, color=(0, 255, 0), thickness=2)
                    cv2.putText(image, str(coordinate_groups[-1][0]), ((coordinate_groups[-1][2::][0][1])), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    
                    cv2.imshow(str(camera_angle)+" View", image)
            else:
                paint_select.append((x, y))  
                print(paint_select)
                if len(paint_select) ==2:
                    paint_cords.append(paint_select.copy())
                    paint_select = []
                    cv2.polylines(image, [np.array(paint_cords[-1])], isClosed=True, color=(255, 0, 0), thickness=3)
                    print(paint_cords)
    # Create a window and set the mouse callback function
    cv2.namedWindow(str(camera_angle)+" View")
    cv2.setMouseCallback(str(camera_angle)+" View", mouse_callback)
    
    if os.path.exists(jsonname):
        print(f"The file '{jsonname}' exists.")
        
        with open(jsonname, "r") as file:
            coordinate_groups = json.load(file)
        for x in range(len(coordinate_groups)):
            cv2.polylines(image, [np.array(coordinate_groups[x][2::])], isClosed=True, color=(0, 255, 0), thickness=2)
            cv2.putText(image, str(coordinate_groups[-1][0]), ((coordinate_groups[x][2::][0][1])), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    else:
        print(f"The file '{jsonname}' does not exist.")
    while True:
        cv2.imshow(str(camera_angle)+" View", image)
        
        key = cv2.waitKey(1) & 0xFF
        
        # Press 'q' to exit the program
        if key == ord('q'):
            break
        if key == ord('p'):
            if (paintmode == False):
                paintmode = True
            else:
                paintmode = False
    
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    print(coordinate_groups)
    
    with open(jsonname, "w") as file:
        json.dump(coordinate_groups, file)
    
createlotspace("YM1", "image.png")

