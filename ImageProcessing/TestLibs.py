import time
import math
import IMU
import datetime
import os
import sys

a = datetime.datetime.now()
RAD_TO_DEG = 57.29578
M_PI = 3.14159265358979323846
G_GAIN = 0.070  # [deg/s/LSB]  If you change the dps for gyro, you need to update this value accordingly
AA =  0.40      # Complementary filter constant
gyroZangle = 0.0


IMU.detectIMU()     #Detect if BerryIMU is connected.
if(IMU.BerryIMUversion == 99):
    print(" No BerryIMU found... exiting ")
    sys.exit()
IMU.initIMU()

while True:
    b = datetime.datetime.now() - a
    LP = b.seconds/(1.0)

    
    GYRz = IMU.readGYRz()
    rate_gyr_z =  GYRz * G_GAIN
    gyroZangle+=rate_gyr_z*LP
    print(gyroZangle)

