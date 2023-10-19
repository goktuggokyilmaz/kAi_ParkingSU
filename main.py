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
from yolotest import doublecheckmodel

cord_select = []
paint_select = []
zoom_select = []

zoom_cords = []
paint_cords = []
cord_groups = []
zoom_angle_select = []
paintmode= False


def select_zoom(camera_angle,filepath):
    global zoom_areas
    global zoom_angle_select
    #  zoom areas are the list of camera_angles which contain zoom locations when someone wants to select 2 zoom_cords 
    #  firstly we check if this angle has any zoom on it if so it will create bbox on preselected locations and give user 
    #  to ability to add more locations
    
    json_name = "zoom_areas.json"
    
    if os.path.exists(json_name):
        print("Zoomlarin oldugu dosya bulundu")
        with open(json_name, "r") as file:
            zoom_areas = json.load(file)
    else:
        zoom_areas = {}
    if camera_angle in zoom_areas.keys(): #Shows pre registered zoom areas on cv2
        for x in range(len(zoom_areas[camera_angle])):
            cv2.rectangle(filepath, zoom_areas[camera_angle][x][:2:], zoom_areas[camera_angle][x][2::], (0,255,0), thickness=2)
            
            
    def select_roi(event, x, y, flags, pazram): #add locations if it reachs 4 (which means 2 mause clicks) it adds to real database zoom_areas
        global zoom_angle_select
        global zoom_arena_cords 
        if event == cv2.EVENT_LBUTTONDOWN:
            zoom_angle_select.append(x)
            zoom_angle_select.append(y)
            if len(zoom_angle_select) == 4:
                print(zoom_angle_select)
                print(zoom_areas)
                if camera_angle not in zoom_areas.keys():
                    zoom_areas[camera_angle] = []
                zoom_areas[camera_angle].append(zoom_angle_select)
                print("Zoom areas",zoom_areas)
                cv2.rectangle(filepath, zoom_areas[camera_angle][-1][:2:], zoom_areas[camera_angle][-1][2::], (0,255,0), thickness=2)
                zoom_angle_select = []
                
                
                
                          
    cv2.setMouseCallback(str(camera_angle), select_roi)
    while True:
        cv2.imshow(str(camera_angle), filepath)
        
        key = cv2.waitKey(1) & 0xFF
        
        # Press 'q' to exit the program
        if key == ord('q'):
            break
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    with open(json_name, "w") as file: #finally it saves all changes in database zoom_areas on json file
        json.dump(zoom_areas, file)
    

def createlotspace(camera_angle,filepath):
    print("Lot Spaces Now can be created for paint lines press P")
    global cord_select 
    global cord_groups 
    global paintmode
    # Load the pre-existing image from the file
    #image = cv2.imread(filepath)
    cord_select = []
    cord_groups = []
    jsonname = camera_angle+".json"
    #CORDINATES Are appended SUCH ((AngelName+lotcount),CenterPoints,Booltest,Allpoints)
    # Callback function for mouse click events
    def mouse_callback(event, x, y, flags, param):
        global cord_select
        global paintmode
        global cord_groups
        global paint_cords
        global paint_select
    
        if event == cv2.EVENT_LBUTTONDOWN:
            if (paintmode == False):
                cord_select.append((x, y))
                cv2.circle(filepath, (x, y), 4, (0, 255, 0), -1)
        
                if len(cord_select) == 6:
                    lotname= camera_angle+"-"+str(len(cord_groups))
                    booltest = False
                    cord_groups.append((lotname,booltest,cord_select.copy()))
                    cord_select = []
                    # Draw green lines connecting the group of four coordinates
                    cv2.polylines(filepath, [np.array(cord_groups[-1][2::])], isClosed=True, color=(0, 255, 0), thickness=1)
                    cv2.putText(filepath, str(cord_groups[-1][0]), ((cord_groups[-1][2::][0][1])), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
    
                    cv2.imshow(str(camera_angle), filepath)
            else:
                paint_select.append((x, y))  
                print(paint_select)
                if len(paint_select) ==2:
                    paint_cords.append(paint_select.copy())
                    paint_select = []
                    cv2.polylines(filepath, [np.array(paint_cords[-1])], isClosed=True, color=(255, 0, 0), thickness=1)
                    print(paint_cords)
    # Create a window and set the mouse callback function
    cv2.namedWindow(str(camera_angle))
    cv2.setMouseCallback(str(camera_angle), mouse_callback)
    
    if os.path.exists(jsonname):
        print(f"The file '{jsonname}' exists.")
        
        with open(jsonname, "r") as file:
            cord_groups = json.load(file)
        for x in range(len(cord_groups)):
            cv2.polylines(filepath, [np.array(cord_groups[x][2::])], isClosed=True, color=(0, 255, 0), thickness=2)
            cv2.putText(filepath, str(cord_groups[x][0]), ((cord_groups[x][2::][0][1])), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
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
    print(cord_groups)
    
    with open(jsonname, "w") as file:
        json.dump(cord_groups, file)
    
        
def videomain(camera_angle,filepath):  #main code which reads mp4 file
    print("hi")
    cap = cv2.VideoCapture(filepath)
    while True:
        ret, frame = cap.read()
        if not ret: break # break if no next frame
        #print("HERE")
        cv2.imshow(str(camera_angle),frame) # show frame
        key = cv2.waitKey(0) & 0xFF 
        if key == ord('q'): # on press of q break
            break
        if key == ord('e'):
            beforeyolo(camera_angle, frame)
        if key == ord('z'):
            select_zoom(camera_angle, frame)
    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)
    cv2.destroyAllWindows()
    
    
    
def beforeyolo(camera_angle,frame):
    print("BeforYOLO")
    json_name = "zoom_areas.json"
    if os.path.exists(json_name):
        print("Zoomlarin oldugu dosya bulundu")
        with open(json_name, "r") as file:
            zoom_areas = json.load(file)
    else:
        zoom_areas = {}
    key = cv2.waitKey(0) & 0xFF 
    if key == ord("p"):
        createlotspace(camera_angle,frame)
    if key == ord("y"):
        detectlot(camera_angle,frame)
    if camera_angle in zoom_areas.keys(): #Shows pre registered zoom areas on cv2
        for x in range(len(zoom_areas[camera_angle])):
            cv2.rectangle(frame, zoom_areas[camera_angle][x][:2:], zoom_areas[camera_angle][x][2::], (0,255,0), thickness=2)
            current = zoom_areas[camera_angle][x]
            x1, y1, x2, y2 = current
            if x1 < x2:
                x1, x2 = x2, x1
            if y1 < y2:
                y1, y2 = y2, y1
            img_cropped = frame[y1:y2,x1:x2]
            cv2.resize(img_cropped, None, fx=2, fy=2)
            cv2.imshow("cropped", img_cropped)
            key = cv2.waitKey(0) & 0xFF 
            if key == ord("p"):
                createlotspace(camera_angle+"_"+str(x),img_cropped)
            if key == ord("y"):
                detectlot(camera_angle+"_"+str(x),img_cropped)
        
    # release and destroy windows

def zoom_frames(camera_angle,frame):
    frames = []
    frames.append(frame)
    json_name = "zoom_areas.json"
    if os.path.exists(json_name):
        print("Zoomlarin oldugu dosya bulundu")
        with open(json_name, "r") as file:
            zoom_areas = json.load(file)
    else:
        zoom_areas = {}
        
        
    if camera_angle in zoom_areas.keys():
        print(camera_angle,"in keys")
        for x in range(len(zoom_areas[camera_angle])):
            current = zoom_areas[camera_angle][x]
            x1, y1, x2, y2 = current
            #print("TEST ",x1,y2,x2,y2)
            if x1 > x2:
                x1, x2 = x2, x1
            if y1 > y2:
                y1, y2 = y2, y1
            #print("SECTEST ",x1,y2,x2,y2)
            img_cropped = frame[y1:y2,x1:x2]
            img_cropped = cv2.resize(img_cropped, None, fx=2, fy=2)
            frames.append(img_cropped)
    return frames

def videotoframe(camera_angle,filepath):
    cap = cv2.VideoCapture(filepath)
    ret, frame = cap.read()
    if ret:
        cv2.imshow(str(camera_angle),frame) # show frame
        #print("This is your main frame")
        #cv2.imwrite(camera_angle+".jpeg",frame)
        return(frame)
    
def manuel_correction(camera_angle,frame):
    jsonname = camera_angle+".json"
    if os.path.exists(jsonname):
        print(f"The file '{jsonname}' exists.")
        
        with open(jsonname, "r") as file:
            cord_groups = json.load(file)
        for x in range(len(cord_groups)):
            cv2.polylines(frame, [np.array(cord_groups[x][2::])], isClosed=True, color=(0, 255, 0), thickness=2)
            cv2.putText(frame, str(cord_groups[x][0]), ((cord_groups[x][2::][0][1])), cv2.FONT_HERSHEY_PLAIN, 2, (0, 255, 0), 2)
   
    def mouse_callback(event, x, y, flags, param):
        print(camera_angle, x," / ",y)
    cv2.namedWindow(str(camera_angle))
    cv2.setMouseCallback(str(camera_angle), mouse_callback)
    while(True):
        cv2.imshow(str(camera_angle),frame)
        key = cv2.waitKey(0) & 0xFF 
        if key == ord('q'): # on press of q breakq
            break
#videomain("YBF_A", "YBF_A.mov1")

cur_name = "UCB_A"
cur_video = cur_name+".mp4"
cur_frame = videotoframe(cur_name,cur_video)
#select_zoom(cur_name, cur_frame)
frames = (zoom_frames(cur_name, cur_frame))
#manuel_correction(cur_name,cur_frame)

for x in range(len(frames)):
    if x == 0: #Main camera angle
        detectlot(cur_name, frames[x])
        
        #createlotspace(cur_name, frames[x])
    else: #Other zoom frames from main camera_angle
        detectlot(cur_name+"_"+str(x), frames[x])
        doublecheckmodel(cur_name, cur_name+"_"+str(x))
        #createlotspace(cur_name+"_"+str(x), frames[x])
        
        
#createlotspace("YM1", "image.png")

