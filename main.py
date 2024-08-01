import cv2
import numpy as np
import math
import ultralytics
from ultralytics import YOLO
import  cvzone

from sort import Sort

model =YOLO("assets/yolov8n.pt")
cap = cv2.VideoCapture('assets/bot1.mp4')
with open("assets/classes.txt","r") as f:
    classnames =f.read().splitlines()
tracker = Sort(max_age=20,min_hits=5)
line = [1100,0,1100,900]
counter = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
    detections = np.empty((0,5))
    result = model(frame,stream=True)
    for info in result:
        parametrs = info.boxes
        for details in parametrs:
            x1,y1,x2,y2 = details.xyxy[0]
            conf = details.conf[0]
            conf = math.ceil(conf*100)
            class_detect = details.cls[0]
            class_detect = int(class_detect)
            class_detect = classnames[class_detect]
            # if conf > 30 :
            # and  class_detect == "bottle":
            #    x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
            #    current_detection = np.array([x1,y1,x2,y2,conf])
            #    detections = np.vstack((detections,current_detection))
            x1,y1,x2,y2 = int(x1),int(y1),int(x2),int(y2)
            current_detection = np.array([x1,y1,x2,y2,conf])
            detections = np.vstack((detections,current_detection))
       
    track_result = tracker.update(detections)  
    cv2.line(frame,(line[0],line[1]),(line[2],line[3]),(255,0,255),5)
    for info in track_result:
        print(info)
        info =  ~np.isnan(info)
        x1,y1,x2,y2,id =  info    
        x1,y1,x2,y2,id = int(x1),int(y1),int(x2),int(y2),int(id)
        w,h = x2-x1,y2-y1
        cx,cy=x1+w//2,y1+h//2
        # cv2.circle(frame,(cx,cy),12,(255,0,255),1)
        # cv2.rectangle(frame,(x1,y1),(x2,y2),(255,0,255),5)
        cvzone.putTextRect(frame,f'{id}',[x1+8,y1-12],scale=2,thickness=2)
        cvzone.cornerRect(frame,[x1,y1,w,h],rt=5)
        if line[1] <cy < line[3] and line[2]-10 <cx<line[2]+10:
            cv2.line(frame,(line[0],line[1]),(line[2],line[3]),(0,0,255),10)
            if counter.count(id) == 0:
                 counter.append(id)
    cvzone.putTextRect(frame,f'Total drinks = {len(counter)}',[500,34],scale=2.5,thickness=4, border=2)
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break