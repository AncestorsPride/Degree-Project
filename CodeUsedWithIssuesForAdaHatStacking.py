# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""Simple test for using adafruit_motorkit with a DC motor"""
import time
import board
from adafruit_motorkit import MotorKit

# Initialise the first hat on the default address
kit1 = MotorKit(i2c=board.I2C() )
#kit1 = MotorKit(i2c=board.I2C())
# Initialise the second hat on a different address
kit2 = MotorKit(address=0x61)


while True:
    kit1.motor1.throttle = 0.25
    kit1.motor2.throttle = 0.25
    kit1.motor3.throttle = -0.25
    kit1.motor4.throttle = -0.25
    kit2.motor1.throttle = 0.25
    kit2.motor2.throttle = 0.25
    kit2.motor3.throttle = -0.25
    kit2.motor4.throttle = -0.25
    time.sleep(3.0)
    
