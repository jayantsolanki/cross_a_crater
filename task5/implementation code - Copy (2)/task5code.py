import numpy
import cv2
import serial
import math
from time import sleep
import motion
from imglib import *
from motion import *
#ser=serial.Serial(3) #COM4
grid_line_x = 18
grid_line_y = 18
m=480/(grid_line_x-1)
n=540/(grid_line_y-1)
grid_start = 0
grid_end = 0
grid_map = [ [ 0 for i in range(grid_line_y-1) ] for j in range(grid_line_x-1) ]
marker = [ [ 0 for i in range(3) ] for j in range(8) ]
tasker=[ [ 0 for i in range(3) ] for j in range(1) ]

mbs=0
stepper=0
MIN = numpy.array([65 ,110, 50],numpy.uint8)   ##wall
MAX = numpy.array([90, 255, 255],numpy.uint8)
flag=0
task=0
route_length=[ 0 for i in range(3) ]
route_path_list=[ 0 for i in range(6) ]
carryR=0#task for red
carryB=0#task for B
carryY=0#task for Y
cap = cv2.VideoCapture(1)

ret, img = cap.read()
frame=imgclip(img)
marker=markers(frame)
rx=marker[2][0]
ry=marker[2][1]
bx=marker[0][0]
by=marker[0][1]
yx=marker[1][0]
yy=marker[1][1]


hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
bmask = cv2.inRange(hsv, MIN,MAX)
bcontours, bh = cv2.findContours(bmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
bcontours=sorted(bcontours, key = cv2.contourArea, reverse = True)[:15] ##bot
M = cv2.moments(bcontours[0])
marker[6][0] = int(M['m10']/M['m00'])
marker[6][1]= int(M['m01']/M['m00'])
cv2.circle(frame,(marker[6][0],marker[6][1]), 5, (0,0,255), -1)
#print cx3,cy3
M = cv2.moments(bcontours[1])
marker[7][0] = int(M['m10']/M['m00'])
marker[7][1] = int(M['m01']/M['m00'])
cv2.circle(frame,(marker[7][0],marker[7][1]), 5, (0,0,255), -1)
cv2.imshow("bot",frame)
################
print marker
x,y=getcoor(rx,ry,n,m)
b1,b2=getcoor(marker[6][0],marker[6][1],n,m)
#print b1,b2
#print x,y
start=GridPoint(b2,b1)
stop=GridPoint(y,x)
route_length,route_path=solve(start,stop,frame)
print route_path
#print route_path[route_length-2].y+1,route_path[route_length-2].x+1
#print x,y

#####################

##############################################

#################
def execute():
        stepper=0 
        while(1):
                
                ret, frame = cap.read()
                img=imgclip(frame)
                img = cv2.medianBlur(img,5)
                ############ processing starts after clipping
                #wap=grid_draw(img,17,17)
                #cv2.imshow("show",wap)
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
                #print cx3,cy3
                M = cv2.moments(bcontours[1])
                cx4 = int(M['m10']/M['m00'])
                cy4 = int(M['m01']/M['m00'])
                cv2.circle(img,(cx4,cy4), 5, (0,100,100), -1)
                a,b=gridtopixel(x,y,m,n)
                #print route_path[stepper].y+1,route_path[stepper].x+1
                #print y+1,x+1
                #print getcoor(a,b,m,n)
                #cv2.circle(img,(b,a), 5, (211,200,255), -1)
                
                
                
                bx,by=getcoor(cx3,cy3,n,m)
                
                #print route_path[0].y+1,route_path[0].x+1   [(5,6), (4,6), (3,6), (3,5), (3,4), (3,3)]
                #print "starting point",Y,X
                print "bot center",bx+1,by+1,"route length",route_length
                #print "other bot",cx4,cy4
                if stepper!=route_length:
                        X,Y=gridtopixel(route_path[stepper].x,route_path[stepper].y,m,n)#X,Y are pixels of next grid coor
                        cv2.circle(img,(Y,X), 5, (255,100,100), -1)
                        #print "hello123"
                        m1= getslope(cx3,cy3,Y,X)
                        #print "slope m1", m1
                        m2= getslope(cx3,cy3,cx4,cy4)
                        #print "slope m2", m2
                        if orientmove(m1,m2,bx+1,by+1,route_path[stepper].y+1,route_path[stepper].x+1)==1: #bot reaches next coor
                                      stepper=stepper+1
                                      flag=0
                                      print "Bot Coor",bx+1,by+1
                                      print stepper
                                      ser.write("9")
                                      #z,c=gridtopixel(route_path[stepper].x,route_path[stepper].y,m,n)
          
                else:
                        ser.write("5")
                        ser.write("9")
                        break
                                
                                
                        
                
                
                
                                 
                         
        ##########################
                        
                #cv2.imshow('maskcontour',bmask)
                cv2.imshow('ori',img)
                if cv2.waitKey(1) == 27:  ## 27 - ASCII for escape key
                        break
        ##############

execute()
#print len(contours)
cv2.destroyAllWindows()
