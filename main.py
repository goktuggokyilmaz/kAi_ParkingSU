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
from yolotest import detectlot

selected_coordinates = []
paint_select = []
paint_cords = []
coordinate_groups = []
paintmode= False

def createlotspace(camera_angle,filepath):
    print("Lot Spaces Now can be created for paint lines press P")
    global selected_coordinates
    global coordinate_groups
    global paintmode
    # Load the pre-existing image from the file
    #image = cv2.imread(filepath)
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
                cv2.circle(filepath, (x, y), 4, (0, 255, 0), -1)
        
                if len(selected_coordinates) == 6:
                    lotname= camera_angle+"-"+str(len(coordinate_groups))
                    booltest = False
                    coordinate_groups.append((lotname,booltest,selected_coordinates.copy()))
                    selected_coordinates = []
                    # Draw green lines connecting the group of four coordinates
                    cv2.polylines(filepath, [np.array(coordinate_groups[-1][2::])], isClosed=True, color=(0, 255, 0), thickness=2)
                    cv2.putText(filepath, str(coordinate_groups[-1][0]), ((coordinate_groups[-1][2::][0][1])), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    
                    cv2.imshow(str(camera_angle), filepath)
            else:
                paint_select.append((x, y))  
                print(paint_select)
                if len(paint_select) ==2:
                    paint_cords.append(paint_select.copy())
                    paint_select = []
                    cv2.polylines(filepath, [np.array(paint_cords[-1])], isClosed=True, color=(255, 0, 0), thickness=3)
                    print(paint_cords)
    # Create a window and set the mouse callback function
    cv2.namedWindow(str(camera_angle))
    cv2.setMouseCallback(str(camera_angle), mouse_callback)
    
    if os.path.exists(jsonname):
        print(f"The file '{jsonname}' exists.")
        
        with open(jsonname, "r") as file:
            coordinate_groups = json.load(file)
        for x in range(len(coordinate_groups)):
            cv2.polylines(filepath, [np.array(coordinate_groups[x][2::])], isClosed=True, color=(0, 255, 0), thickness=2)
            cv2.putText(filepath, str(coordinate_groups[-1][0]), ((coordinate_groups[x][2::][0][1])), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    else:
        print(f"The file '{jsonname}' does not exist.")
    while True:
        cv2.imshow(str(camera_angle), filepath)
        
        key = cv2.waitKey(1) & 0xFF
        
        # Press 'q' to exit the program
        if key == ord('q'):
            break
        if key == ord('p'):
            if (paintmode == False):
                paintmode = True
                print("paintmode is now ",paintmode)
            else:
                paintmode = False
                print("paintmode is now ",paintmode)
    
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    print(coordinate_groups)
    
    with open(jsonname, "w") as file:
        json.dump(coordinate_groups, file)
        
def fromvideotoyolo(camera_angle,filepath):
    print("hi")
    cap = cv2.VideoCapture(filepath)
    while True:
        ret, frame = cap.read()
        if not ret: break # break if no next frame
        #print("HERE")
        cv2.imshow(str(camera_angle),frame) # show frame
        
        key = cv2.waitKey(1) & 0xFF 
        if key == ord('q'): # on press of q break
            break
        if key == ord("p"):
            createlotspace(camera_angle,frame)
        if key == ord("y"):
            detectlot(camera_angle,frame)
    # release and destroy windows
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    
fromvideotoyolo("UCB1", "ucbtest.mp4")
#createlotspace("YM1", "image.png")

