import math
import serial
#ser=serial.Serial(4) #COM4, for windows
grid_line_x = 7
grid_line_y = 7
##########################
# returning grid coordinate from pixels coordinates
#
#
#
#
def getcoor(x,y,m,n):
        X=0
        Y=0
        for i in range(0, grid_line_x): ##drawing lines
                X=X+m
                Y=0
                for j in range(0, grid_line_y): ##drawing lines
                        Y=Y+n
                        # print X,Y,x,y
                        # print i,j
                        if x<=X and y<=Y:
                            return i,j
                            break
##########################
# converting grid coordinates into pixels
#
#
#
#
def gridtopixel(x,y,m,n):
        X=x*m+m/2
        Y=y*n+n/2
        return X,Y
########################
