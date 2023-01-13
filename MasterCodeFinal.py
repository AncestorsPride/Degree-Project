import cv2
import time
import os
import math
import datetime
import board
import digitalio
import numpy as np
import RPi.GPIO as GPIO
from adafruit_motorkit import MotorKit
from adafruit_rgb_display.rgb import color565
from adafruit_rgb_display import st7789
from gpiozero import CPUTemperature
from picamera.array import PiRGBArray    
from picamera import PiCamera

#___________________________________________________________________________________________________________________________________________________________________

cpu=CPUTemperature()
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
BAUDRATE = 64000000  # The pi can be very fast!
# Create the ST7789 display:#
display = st7789.ST7789(
    board.SPI(),
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
    width=135,
    height=240,
    x_offset=53,
    y_offset=40
    )

backlight = digitalio.DigitalInOut(board.D22)
backlight.switch_to_output()
backlight.value = True
buttonA = digitalio.DigitalInOut(board.D23)
buttonB = digitalio.DigitalInOut(board.D24)
buttonA.switch_to_input()
buttonB.switch_to_input()

kit1=MotorKit(address=0x61)#chassis
kit2=MotorKit(address=0x62)#lifting mechanism

top_limit_sensor=6
bottom_limit_sensor=5
GPIO.setup(top_limit_sensor, GPIO.IN)
GPIO.setup(bottom_limit_sensor, GPIO.IN)

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ser = serial.Serial(
     port='/dev/ttyUSB0',
     baudrate=9600,
     parity=serial.PARITY_NONE,
     stopbits=serial.STOPBITS_ONE,
     bytesize=serial.EIGHTBITS,
     timeout=1
     )
counter=0


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------




 
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


def backward(speed, t):     
    """
    Args:
        speed (double):
        ranges from 0 to -1.0
        indicating the speed of the motors
        t (double) is time to which motors drive to
    """
    if speed >= 0 and t > 0:
        print('Going backward')
        kit1.motor1.throttle=speed
        kit1.motor2.throttle=-speed
        kit1.motor3.throttle=speed
        kit1.motor4.throttle=speed
        time.sleep(t)
        kit1.motor1.throttle=0
        kit1.motor2.throttle=0
        kit1.motor3.throttle=0
        kit1.motor4.throttle=0

    else:
        return "Backward can only be a negative double from 0 to -1.0! Time has to be greater than 0!"


def extend(lift_speed):
    
    """_summary_
    Args:
        lift_speed (double): extends the lifting mechanism until the limit has reached
    """
    always=False
    if GPIO.input(top_limit_sensor) == 1:
        always = True
        
        
        if always == True:
            
            kit2.motor1.throttle=-lift_speed
            kit2.motor2.throttle=-lift_speed
            kit2.motor3.throttle=lift_speed
            kit2.motor4.throttle=lift_speed
            time.sleep(3.1)#find)
            print('Going up')
            kit2.motor1.throttle=0.0
            kit2.motor2.throttle=0.0
            kit2.motor3.throttle=0.0
            kit2.motor4.throttle=0.0
            always = False
    else :
        print('Something went wrong')


def retract(lift_speed):
    """_summary_
    Args:
     
     lift_speed (double): retracts the lifting mechanism until the home position
    """
    while GPIO.input(bottom_limit_sensor) != 0:
        kit2.motor1.throttle=lift_speed
        kit2.motor2.throttle=lift_speed
        kit2.motor3.throttle=-lift_speed
        kit2.motor4.throttle=-lift_speed
        print('Going down')

    else :
        time.sleep(1.5)
        kit2.motor1.throttle=0
        kit2.motor2.throttle=0
        kit2.motor3.throttle=0
        kit2.motor4.throttle=0
        print('The bottow has been reached')
        
    
#def turn_on_place(left,right):
#def read_now():
    
#   
# def turn_right(current_angle, angle, phase_speed):
#     """_summary_
#     Args:
#         current_angle (dobule): datum angle = 0 deg 
#         angle (int): 4 inputs are accepted (90, 180, 270, 360)
#         phase_speed (str): can be slow, medium or fast
#     """
#     datum_angle = gyroZangle
#     speed = 0.20
#     
#     while datum_angle != (gyroZangle + 90.0):
#         
#         kit1.motor1.throttle=-0.20
#         kit1.motor2.throttle=-0.20
#         kit1.motor3.throttle=0.20
#         kit1.motor4.throttle=0.20
#         
#     kit1.motor1.throttle=0
#     kit1.motor2.throttle=0
#     kit1.motor3.throttle=0
#     kit1.motor4.throttle=0
#

def combined_mask(frame):
    hsv  = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    blue = cv2.inRange(hsv,np.array([80,88,0]),np.array([128,255,255]))
    lit_green  = cv2.inRange(hsv,np.array([50,21,74]),np.array([110,255,255]))
    com_mask   = lit_green + blue
    com_mask   = cv2.erode(com_mask, np.ones((5,5)))      #Eroding
    com_mask   = cv2.dilate(com_mask,np.ones((10,10)))     #Dilating
    return com_mask

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(640, 480))    
time.sleep(0.1)

while True:
    
    x=ser.readline()# .strip() .readline() 

    
    if buttonA.value and buttonB.value:
        backlight.value = False  # turn off backlight
    else:
        backlight.value = True  # turn on backlight
    if buttonB.value and not buttonA.value:  # just button A pressed
        display.fill(color565(255, 0, 0))  # red
        #forward(0.2, 3.0)
        print(cpu.temperature) #Anything under 50C is acceptable
       # print(float(read_now()))
#         extend(0.35)
        print("B")
        retract(0.35)
        print("A")
        #forward(0.2, 3.0)
        #display.fill(color565(0, 0, 255))  # red

        
    elif x.decode('UTF-8')=='start':  # just button B pressed
        send = ('DEV04 Starting the sequence')
        r=send.encode()
        ser.write(r)
        
        display.fill(color565(0, 0, 255))  # blue
        extend(0.35)
        time.sleep(1)
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
                    print_data(1,0.25, 0.5, message, area)
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
                    print_data(1,0.15, 1, message, area)
                    rawCapture.truncate(0)
                    
                else :
                    #forward(0, 1)
                    print(area)
                    print("Object Obtained")
                    rawCapture.truncate(0)
                    break
                
        
            
            time.sleep(2)        
            backward(0.25,2)
            retract(0.40)
            print('test end')
            send = ('approach')
            r=send.encode()
            #r=bytes(send) 
            ser.write(r)
            
            
       # turn_right(0,0,0)
       # backward(0.2, 3.0)
       # print(cpu.temperature) #Anything under 50C is acceptable
       # print(gyroZangle)
        
    if not buttonA.value and not buttonB.value:  # none pressed
        display.fill(color565(0, 255, 0))  # green
        

#if buttonB.value and not buttonA.value:  # just button A pressed
   # display.fill(color565(255, 0, 0))  # red
   # forward(0.6, 3.0)

