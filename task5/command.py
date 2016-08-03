import serial
from time import sleep
ser=serial.Serial(3) #COM4
print "Enter 8 for forward, 2 for backward, 5 for stop, 4 for left, 6 for right, 0 to quit"
com=1
while com!="0":
    com = raw_input()
    ser.write("O") 
    ser.write(com) #send command

ser.close()
