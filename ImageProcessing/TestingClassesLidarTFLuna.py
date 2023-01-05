import tfluna_test

if ser.isOpen() == False:
    ser.open() # open serial port if not open
while True:
    
      tfluna_test.do_it_once()
#while True:
    
      #distance,strength,temperature = read_tfluna_data() # read values
      #print('Distance: {0:2.2f} m, Strength: {1:2.0f} / 65535 (16-bit), Chip Temperature: {2:2.1f} C'.\
      #format(distance,strength,temperature)) # print sample data
      #print(distance, temperature)
      
ser.close() # close serial por