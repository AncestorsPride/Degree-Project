#!/usr/bin/env python
import cv2
import numpy as np
import time
from adafruit_motorkit import MotorKit
from picamera.array import PiRGBArray    
from picamera import PiCamera

def nothing(pos):
    pass
speed =0
t=0
#cap=cv2.VideoCapture(0)
kit1=MotorKit(address=0x61)#chassis
#_, frame = cap.read()
    
def forward(speed, t):
    if speed >= 0 and t > 0:
        print('Going forward 2')
        kit1.motor1.throttle=-speed
        kit1.motor2.throttle=speed
        kit1.motor3.throttle=-speed
        kit1.motor4.throttle=-speed
        time.sleep(t)
        kit1.motor1.throttle=0
        kit1.motor2.throttle=0
        kit1.motor3.throttle=0
        kit1.motor4.throttle=0
    else:
        return "Forward can only be a positive double from 0 to +1.0! Time has to be greater than 0!"
def combined_mask(frame):
    hsv  = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    blue = cv2.inRange(hsv,np.array([85,112,0]),np.array([128,255,255]))
    lit_green  = cv2.inRange(hsv,np.array([50,21,88]),np.array([110,255,255]))
    com_mask   = lit_green + blue
    com_mask   = cv2.erode(com_mask, np.ones((5,5)))      #Eroding
    com_mask   = cv2.dilate(com_mask,np.ones((10,10)))     #Dilating
    return com_mask

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(640, 480))
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    
    def print_data(w,speed, t, message, area):
        #time.sleep(w)
        forward(speed, t) 
        print(message)
        print(area)

    frame = frame.array
    com_mask = combined_mask(frame)
    (contours,hierarchy)=cv2.findContours(com_mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    rawCapture.truncate(0)

    if len(contours)>0:
        contour= max(contours,key=cv2.contourArea)
        area = cv2.contourArea(contour)
        time.sleep(1)        
        if area < 15000: 
            time.sleep(1)
            message="not found, Area is 15000, "
            print_data(1,0.05, 1, message, area)
            rawCapture.truncate(0)
            
        elif area < 25000:
            message="Area is 25000 22"
            print_data(1,0.20, 2, message, area)
            rawCapture.truncate(0)

        elif area < 50000:
            message ="Area is 50000 11"
            print_data(1,0.15, 2, message, area)
            rawCapture.truncate(0)
            
        elif area < 150000:
            message ="Area is 150000 4-5"
            print_data(1,0.10, 2, message, area)
            rawCapture.truncate(0)
                
        else :
            #forward(0, 1)
            print(area)
            print("Object Obtained")
            rawCapture.truncate(0)
            break

        cv2.imshow("Mask",com_mask)
    
#     key = cv2.waitKey(1)
#     if key == 27:
#         break
print("end")    
# cap.release()
cv2.destroyAllWindows()
