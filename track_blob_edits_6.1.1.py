#!/usr/bin/env python
import cv2
import numpy as np
import time
from adafruit_motorkit import MotorKit
from picamera.array import PiRGBArray    
from picamera import PiCamera

def nothing(pos):
    pass

cap=cv2.VideoCapture(0)
kit1=MotorKit(address=0x61)#chassis
#_, frame = cap.read()
    
def forward(speed, t):
    """_summary_
    Args:
        speed (double):
        ranges from 0 to +1.0
        indicating the speed of the motors
        t is the time until which motors are ON
    """
    if speed >= 0 and t > 0:
        print('Going forward')
        kit1.motor1.throttle=speed
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

#def backward(speed, t):
    #"""
    #Args:
     #   speed (double):
     #   ranges from 0 to -1.0
     #   indicating the speed of the motors
     #   t (double) is time to which motors drive to
    #"""
    #if speed >= 0 and t > 0:
        # print('Going backward')
        # kit1.motor1.throttle=-speed
        # kit1.motor2.throttle=-speed
        # kit1.motor3.throttle=speed
        # kit1.motor4.throttle=speed
        # time.sleep(t)
        # kit1.motor1.throttle=0
        # kit1.motor2.throttle=0
        # kit1.motor3.throttle=0
        # kit1.motor4.throttle=0
    #else:
        #return "Backward can only be a negative double from 0 to -1.0! Time has to be greater than 0!"

def combined_mask(frame):
    hsv  = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    blue = cv2.inRange(hsv,np.array([80,88,0]),np.array([128,255,255]))
    lit_green  = cv2.inRange(hsv,np.array([50,21,74]),np.array([110,255,255]))
    blue        = cv2.erode(blue, np.ones((5,5)))      #Eroding
    blue        = cv2.dilate(blue,np.ones((8,8)))     #Dilating
    lit_green   = cv2.erode(lit_green, np.ones((5,5)))      #Eroding
    lit_green   = cv2.dilate(lit_green,np.ones((8,8)))
    com_mask   = lit_green + blue
#     com_mask   = cv2.erode(com_mask, np.ones((5,5)))      #Eroding
#     com_mask   = cv2.dilate(com_mask,np.ones((8,8)))     #Dilating
    return com_mask

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 16
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
                
        if area < 15000: 
            message="not found, Area is 15000, "
            print(message)
            rawCapture.truncate(0)
#             print_data(1,0.05, 1, message, area)
            
        elif area < 25000:
            message="Area is 25000 22"
            print(message)
            rawCapture.truncate(0)
#             print_data(1,0.20, 2, message, area)

        elif area < 50000:
            message ="Area is 50000 11"
            print(message)
            rawCapture.truncate(0)
#             print_data(1,0.15, 2, message, area)
            
        elif area < 150000:
            message ="Area is 150000 4-5"
            print(message)
            rawCapture.truncate(0)
#             print_data(1,0.10, 2, message, area)
                
        else :
            #forward(0, 1)
            print(area)
            print("Object Obtained")
#             break


    cv2.imshow("Mask",com_mask)
    #cv2.imshow("Color Tracking",frame)
    
    key = cv2.waitKey(1)
    if key == 27:
        break
cap.release()
cv2.destroyAllWindows()