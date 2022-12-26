import time
import sys
import os
import math
import datetime
import IMU
import board
import digitalio
from adafruit_motorkit import MotorKit
from adafruit_rgb_display.rgb import color565
from adafruit_rgb_display import st7789
from gpiozero import CPUTemperature

RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      # Complementary filter constant

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

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

magXmin =  0
magYmin =  0
magZmin =  0
magXmax =  0
magYmax =  0
magZmax =  0



'''
Here is an example:
magXmin =  -1748
magYmin =  -1025
magZmin =  -1876
magXmax =  959
magYmax =  1651
magZmax =  708
Dont use the above values, these are just an example.
'''
############### END Calibration offsets #################



gyroXangle = 0.0
gyroYangle = 0.0
gyroZangle = 0.0
CFangleX = 0.0
CFangleY = 0.0


IMU.detectIMU()     #Detect if BerryIMU is connected.
if(IMU.BerryIMUversion == 99):
    print(" No BerryIMU found... exiting ")
    sys.exit()
IMU.initIMU()       #Initialise the accelerometer, gyroscope and compass


a = datetime.datetime.now()


#kit1.motor1.throttle=0.1
#kit1.motor2.throttle=0.1
#kit1.motor3.throttle=-0.1
#kit1.motor4.throttle=-0.1

#Read the accelerometer,gyroscope and magnetometer values
ACCx = IMU.readACCx()
ACCy = IMU.readACCy()
ACCz = IMU.readACCz()
GYRx = IMU.readGYRx()
GYRy = IMU.readGYRy()
GYRz = IMU.readGYRz()
MAGx = IMU.readMAGx()
MAGy = IMU.readMAGy()
MAGz = IMU.readMAGz()
    
##Calculate loop Period(LP). How long between Gyro Reads
b = datetime.datetime.now() - a
a = datetime.datetime.now()
LP = b.microseconds/(1000000*1.0)
outputString = "Loop Time %5.2f " % ( LP )


#Convert Gyro raw to degrees per second
rate_gyr_x =  GYRx * G_GAIN
rate_gyr_y =  GYRy * G_GAIN
rate_gyr_z =  GYRz * G_GAIN


#Calculate the angles from the gyro.
gyroXangle+=rate_gyr_x*LP
gyroYangle+=rate_gyr_y*LP
gyroZangle+=rate_gyr_z*LP


#Convert Accelerometer values to degrees
AccXangle =  (math.atan2(ACCy,ACCz)*RAD_TO_DEG)
AccYangle =  (math.atan2(ACCz,ACCx)+M_PI)*RAD_TO_DEG
    
    
#Complementary filter used to combine the accelerometer and gyro values.
CFangleX=AA*(CFangleX+rate_gyr_x*LP) +(1 - AA) * AccXangle
CFangleY=AA*(CFangleY+rate_gyr_y*LP) +(1 - AA) * AccYangle

       
#convert the values to -180 and +180
if AccYangle > 90:
    AccYangle -= 270.0
elif AccYangle < 90:
    AccYangle += 90.0

#Calculate heading
heading = 180 * math.atan2(MAGy,MAGx)/M_PI

#Only have our heading between 0 and 360
if heading < 0:
    heading += 360

####################################################################
###################Tilt compensated heading#########################
####################################################################
#Normalize accelerometer raw values.
accXnorm = ACCx/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)
accYnorm = ACCy/math.sqrt(ACCx * ACCx + ACCy * ACCy + ACCz * ACCz)


#Calculate pitch and roll
pitch = math.asin(accXnorm)
roll = -math.asin(accYnorm/math.cos(pitch))
 
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
        kit1.motor2.throttle=-speed
        kit1.motor3.throttle=speed
        kit1.motor4.throttle=speed
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
        kit1.motor1.throttle=-speed
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
        lift_speed (double): extends the lifting mechanism until the limit has been reached
                             the max is 1.0, the min is -1.0.
                             Optimal range is -0.25~+0.25
    """
    if lift_speed != 0:#lift_speed >=0 and top_limit_sensor == 0 and bot_limit_sensor == 1:
        print('Going up')
        kit2.motor1.throttle=lift_speed
        kit2.motor2.throttle=lift_speed
        kit2.motor3.throttle=-lift_speed
        kit2.motor4.throttle=-lift_speed
        time.sleep(3.9) #should be 4 sec with 0.35 speed for full extension.
        kit2.motor1.throttle=0
        kit2.motor2.throttle=0
        kit2.motor3.throttle=0
        kit2.motor4.throttle=0
        

    elif lift_speed <= 1.0:#top_limit_sensor != 0 and bot_limit_sensor != 0:
        kit2.motor1.throttle=0
        kit2.motor2.throttle=0
        kit2.motor3.throttle=0
        kit2.motor4.throttle=0
        print('Pleave enter only positive values to go up!')
    
    else:
        kit2.motor1.throttle=0
        kit2.motor2.throttle=0
        kit2.motor3.throttle=0
        kit2.motor4.throttle=0
        return "Extnension speed can only be positive!"

def retract(lift_speed):
    """_summary_
    Args:
        lift_speed (double): retracts the lifting mechanism until the home position
    """
    if lift_speed >=0: #and top_limit_sensor == 1 and bot_limit_sensor == 0:
        kit2.motor1.throttle=-lift_speed
        kit2.motor2.throttle=-lift_speed
        kit2.motor3.throttle=lift_speed
        kit2.motor4.throttle=lift_speed
        print('Going up')

    if lift_speed != 0: #and bot_limit_sensor != 0:
        kit2.motor1.throttle=0
        kit2.motor2.throttle=0
        kit2.motor3.throttle=0
        kit2.motor4.throttle=0
        print('The top has not been reached')
    
    else:
        kit2.motor1.throttle=0
        kit2.motor2.throttle=0
        kit2.motor3.throttle=0
        kit2.motor4.throttle=0
        return "Extnension speed can only be positive!"
    
#def turn_on_place(left,right):
    
def turn_right(current_angle, angle, phase_speed):
    """_summary_
    Args:
        current_angle (dobule): datum angle = 0 deg 
        angle (int): 4 inputs are accepted (90, 180, 270, 360)
        phase_speed (str): can be slow, medium or fast
    """
    datum_angle = gyroZangle
    speed = 0.20
    
    while datum_angle != (gyroZangle + 90.0):
        
        kit1.motor1.throttle=-0.20
        kit1.motor2.throttle=-0.20
        kit1.motor3.throttle=0.20
        kit1.motor4.throttle=0.20
        
    kit1.motor1.throttle=0
    kit1.motor2.throttle=0
    kit1.motor3.throttle=0
    kit1.motor4.throttle=0
    
while True:
    
    if buttonA.value and buttonB.value:
        backlight.value = False  # turn off backlight
    else:
        backlight.value = True  # turn on backlight
        
    if buttonB.value and not buttonA.value:  # just button A pressed
        display.fill(color565(255, 0, 0))  # red
        extend(0.35)
       # forward(0.2, 3.0)
       # print(cpu.temperature) #Anything under 50C is acceptable
       # print(gyroZangle)
        
    if buttonA.value and not buttonB.value:  # just button B pressed
        display.fill(color565(0, 0, 255))  # blue
        #while gyroZangle != (gyroZangle - 90.0):
         #    kit1.motor1.throttle=0.25
          #   kit1.motor2.throttle=0.25
           #  kit1.motor3.throttle=-0.25/2
            # kit1.motor4.throttle=-0.25/2
            # print(gyroZangle)
        #else:
        #     kit1.motor1.throttle=0
        #     kit1.motor2.throttle=0
        #     kit1.motor3.throttle=0
        #     kit1.motor4.throttle=0
       # turn_right(0,0,0)
       # backward(0.2, 3.0)
       # print(cpu.temperature) #Anything under 50C is acceptable
       # print(gyroZangle)
        
    if not buttonA.value and not buttonB.value:  # none pressed
        display.fill(color565(0, 255, 0))  # green
        

#while True:
#    if buttonA.value and buttonB.value:
#        backlight.value = False  # turn off backlight
#    else:
#        backlight.value = True  # turn on backlight
#    if buttonB.value and not buttonA.value:  # just button A pressed
#        display.fill(color565(255, 0, 0))  # red
#    if buttonA.value and not buttonB.value:  # just button B pressed
#        display.fill(color565(0, 0, 255))  # blue
#    if not buttonA.value and not buttonB.value:  # none pressed
#        display.fill(color565(0, 255, 0))  # green
#if buttonB.value and not buttonA.value:  # just button A pressed
   # display.fill(color565(255, 0, 0))  # red
   # forward(0.6, 3.0)


    