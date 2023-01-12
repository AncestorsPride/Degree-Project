import time
import serial
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(23, GPIO.OUT)

ser = serial.Serial(
    port='/dev/ttyUSB0',
    baudrate=9600,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
    )

counter=0

while 1:
    #ser.write(ser.encoder('Write counter: %d \n'%(counter)))
    #time.sleep(1)
    #counter+=1
    x=ser.readline()# .strip() .readline() 
    #print(x)
    if x.decode('utf-8') == 'yes':
        #x[:2]+x[-1]
        #GPIO.output(23, GPIO.HIGH)
        #time.sleep(3)
        print(ser.name)
        print('I hate you!')
        send = ('I am in end03')
        r=send.encode()
        #r=bytes(send) 
        ser.write(r)
        #time.sleep(3)
        toCoord = 'hi'
        z=toCoord.encode()
        ser.write(z)
    elif x.decode('utf-8')=='RightBackAtYou':
        print('2 way is successful')
    else:
        #GPIO.output(23, GPIO.LOW)
        #print(x)
        #print(ser.name) Printing /dev/ttyUSB0
        #time.sleep(0.125)
        print('I love you!')
        print('~~~~~~~~~~~~')
        print(x,len(x),type(x))
        print(type(x.decode('utf-8')))