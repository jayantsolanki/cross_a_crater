import numpy
import cv2
import serial
import math
from time import sleep
import motion
from imglib import *
from motion import *
#ser=serial.Serial(3) #COM4
grid_line_x = 17
grid_line_y = 17
grid_start = 0
grid_end = 0
grid_map = [ [ 0 for i in range(grid_line_y-1) ] for j in range(grid_line_x-1) ]
marker = [ [ 0 for i in range(3) ] for j in range(8) ]
m=540/grid_line_x-1
n=480/grid_line_y-1
mbs=0
stepper=0
MIN = numpy.array([65 ,110, 50],numpy.uint8)   ##wall
MAX = numpy.array([90, 255, 255],numpy.uint8)

cap = cv2.VideoCapture(1)
rx=0
ry=0
bx=0
by=0
yx=0
yy=0

ret, img = cap.read()
frame=imgclip(img)
marker=markers(frame)
rx=marker[2][0]
ry=marker[2][1]
bx=marker[0][0]
by=marker[0][1]
yx=marker[1][0]
yy=marker[1][1]
print marker
x,y=getcoor(rx,ry,m,n)
#print x,y
start=GridPoint(8,8)
stop=GridPoint(x-1,y-1)
route_length,route_path=solve(start,stop,frame)
print route_path
print route_path[0].y,route_path[0].x

#####################

h,k,l=frame.shape
line_widthm=h/(grid_line_x-1)
line_widthn=k/(grid_line_y-1)



#################
while(1):
        
        ret, frame = cap.read()
        img=imgclip(frame)
        ############ processing starts after clipping
        
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        
        bmask = cv2.inRange(hsv, MIN,MAX)
        
        #bret,bthresh = cv2.threshold(bmask,127,255,1)
        #cv2.imshow('binary',mask)
        #cv2.imwrite("wall.jpg",mask)

        bcontours, bh = cv2.findContours(bmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        bcontours=sorted(bcontours, key = cv2.contourArea, reverse = True)[:15] ##bot
       
        
        #cv2.drawContours(res,contours,-1,(0,255,0),2)
        cv2.drawContours(img,bcontours,13,(255,255,0),2)
        
           
        M = cv2.moments(bcontours[0])
        cx3 = int(M['m10']/M['m00'])
        cy3 = int(M['m01']/M['m00'])
        cv2.circle(img,(cx3,cy3), 5, (0,0,255), -1)
        ##print cx3,cy3
        M = cv2.moments(bcontours[1])
        cx4 = int(M['m10']/M['m00'])
        cy4 = int(M['m01']/M['m00'])
        cv2.circle(img,(cx4,cy4), 5, (0,0,255), -1)
        m1= getslope(cx3,cy3,marker[2][0],marker[2][1])
        m2= getslope(cx3,cy3,cx4,cy4)
        
        bx,by=getcoor(cx3,cy3,m,n)
        print x,y,route_path[route_length-1].y,route_path[route_length-1].x
        '''
        if ax!=route_path(len-1).x and ay!=route_path(len-1).y:
                if motion.orientmove(m1,m2,ax,ay,route_path(i).x),route_path(i).y)==1:
                        i=i+1
                else:
                    move=motion.orientmove(m1,m2,ax,ay,route_path(i).x),route_path(i).y)==1   
                
        '''
        
        
                         
                 
##########################
        #cv2.imshow('maskcontour',bmask)
        cv2.imshow('ori',img)
        if cv2.waitKey(1) == 27:  ## 27 - ASCII for escape key
                break
##############


#print len(contours)
cv2.destroyAllWindows()
