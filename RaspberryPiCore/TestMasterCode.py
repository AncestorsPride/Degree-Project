import time
import board
import digitalio
from adafruit_motorkit import MotorKit
from adafruit_rgb_display.rgb import color565
from adafruit_rgb_display import st7789
from gpiozero import CPUTemperature


cpu=CPUTemperature()
cs_pin = digitalio.DigitalInOut(board.CE0)
dc_pin = digitalio.DigitalInOut(board.D25)
reset_pin = None
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

while True:
    if buttonA.value and buttonB.value:
        backlight.value = False  # turn off backlight
    else:
        backlight.value = True  # turn on backlight
    if buttonB.value and not buttonA.value:  # just button A pressed
        display.fill(color565(255, 0, 0))  # red
        forward(0.2, 3.0)
        print(cpu.temperature) #Anything under 50C is acceptable
        
    elif buttonA.value and not buttonB.value:  # just button B pressed
        display.fill(color565(0, 0, 255))  # blue
        backward(0.2, 3.0)
    if not buttonA.value and not buttonB.value:  # none pressed
        display.fill(color565(0, 255, 0))  # green

#if buttonB.value and not buttonA.value:  # just button A pressed
   # display.fill(color565(255, 0, 0))  # red
   # forward(0.6, 3.0)

