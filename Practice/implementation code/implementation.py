import cv2
import numpy as np
import random
import os
import serial
import math
from time import sleep
import motion
from imglib import *
from motion import *
grid_line_x = 18
grid_line_y = 12
grid_map = [ [ 0 for i in range(grid_line_y-1) ] for j in range(grid_line_x-1) ]
##################

#########################################
img=cv2.imread("demo.jpg")
frame=imgclip(img)
h,k,l=img.shape
m=h/(grid_line_x-1)
n=k/(grid_line_y-1)
print m,n
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
dilation, obs=obstacle(hsv)#obstacle dilated
img=grid_draw(img,grid_line_x,grid_line_y)
grid_mapp,obb=markobstacle(obs,img,grid_line_x,grid_line_y)
# print grid_mapp
print getcoor(40,80,n,m)
print gridtopixel(1,2,n,m)
x,y=gridtopixel(1,2, n,m)
print "grid cell to pixels",x,y
cv2.circle(img,(int(y),int(x)),3,(0,255,0),-11)
start=GridPoint(1,2)
stop=GridPoint(10,6)
length,route=solve(start,stop,img)
print length, route
# dilation=obstacle(hsv)#obstacle dilated
# cv2.imshow("obstacles",dilation)
cv2.imshow("grid",frame)
cv2.imshow("res",img)
cv2.waitKey()