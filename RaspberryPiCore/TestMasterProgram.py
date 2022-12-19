import time
import board
from adafruit_motorkit import MotorKit

kit1=MotorKit(address=0x61)#chassis
kit2=MotorKit(address=0x62)#lifting mechanism

#kit1.motor1.throttle=0.1
#kit1.motor2.throttle=0.1
#kit1.motor3.throttle=-0.1
#kit1.motor4.throttle=-0.1
 
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


def backward(speed, t):
    

    """
   Args:
        speed (double):
        ranges from 0 to -1.0
        indicating the speed of the motors
        t (double) is time to which motors drive to
     """
    if speed <= 0 and t > 0:
        print('Going backward')
        kit2.motor1.throttle=speed
        kit2.motor2.throttle=speed
        kit2.motor3.throttle=-speed
        kit2.motor4.throttle=-speed
        time.sleep(t)
        kit2.motor1.throttle=0
        kit2.motor2.throttle=0
        kit2.motor3.throttle=0
        kit2.motor4.throttle=0


    else:
        return "Backward can only be a negative double from 0 to -1.0! Time has to be greater than 0!"


def extend(lift_speed):
    """_summary_

    Args:
        lift_speed (double): extends the lifting mechanism until the limit has reached
    """
    if lift_speed >=0 and top_limit_sensor == 0 and bot_limit_sensor == 1:
        kit2.motor1.throttle=lift_speed
        kit2.motor2.throttle=lift_speed
        kit2.motor3.throttle=-lift_speed
        kit2.motor4.throttle=-lift_speed
        print('Going up')

    elif top_limit_sensor != 0 and bot_limit_sensor != 0:
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

def retract(lift_speed):
    """_summary_

    Args:
        lift_speed (double): retracts the lifting mechanism until the home position
    """
    if lift_speed >=0 and top_limit_sensor == 1 and bot_limit_sensor == 0:
        kit2.motor1.throttle=-lift_speed
        kit2.motor2.throttle=-lift_speed
        kit2.motor3.throttle=lift_speed
        kit2.motor4.throttle=lift_speed
        print('Going up')

    elif top_limit_sensor != 0 and bot_limit_sensor != 0:
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

def turn_right(angle, phase_speed):
    """_summary_

    Args:
        angle (int): 4 inputs are accepted (90, 180, 270, 360)
        phase_speed (str): can be slow, medium or fast
    """

    return None
