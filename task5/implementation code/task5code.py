import numpy
import cv2
import serial
import math
from time import sleep
import motion
from imglib import *
from motion import *
#ser=serial.Serial(3) #COM4
ser.write("O")
grid_line_x = 13
grid_line_y = 13
m=480/(grid_line_x-1)
n=540/(grid_line_y-1)
grid_start = 0
grid_end = 0
grid_map = [ [ 0 for i in range(grid_line_y-1) ] for j in range(grid_line_x-1) ]
marker = [ [ 0 for i in range(3) ] for j in range(8) ]
tasker=[ [ 0 for i in range(3) ] for j in range(1) ]
flag=1#if flag==0 dont run the navigation task
mbs=0
stepper=0

MIN= numpy.array([122,140,100],numpy.uint8) ##identifying bot
MAX= numpy.array([130,255,255],numpy.uint8)


cap = cv2.VideoCapture(1)

ret, img = cap.read()
frame=imgclip(img)
marker,flag=markers(frame)
rx=marker[2][0]
ry=marker[2][1]
bx=marker[0][0]
by=marker[0][1]
yx=marker[1][0]
yy=marker[1][1]


hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
dilation=obstacle(hsv)#obstacle dilated
grid_mapp,obb=markobstacle(dilation,frame,grid_line_x,grid_line_y)
print "grid_map",grid_mapp
#cv2.imwrite("dilation.jpg",dilation)
#cv2.imwrite("obstacles.jpg",obb)
bmask = cv2.inRange(hsv, MIN,MAX)
bcontours, bh = cv2.findContours(bmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
bcontours=sorted(bcontours, key = cv2.contourArea, reverse = True)[:12] ##bot
#bcontours,lgth=areacon(bcontours,500,300)
#bcontours=sorted(bcontours, key = cv2.contourArea, reverse = True)[:lgth]
print len(bcontours)
M = cv2.moments(bcontours[0])
marker[6][0] = int(M['m10']/M['m00'])
marker[6][1]= int(M['m01']/M['m00'])
cv2.circle(frame,(marker[6][0],marker[6][1]), 5, (0,0,255), -1)
#print cx3,cy3
M = cv2.moments(bcontours[1])
marker[7][0] = int(M['m10']/M['m00'])
marker[7][1] = int(M['m01']/M['m00'])
cv2.circle(frame,(marker[7][0],marker[7][1]), 5, (0,0,255), -1)
cv2.imwrite("bot.jpg",frame)
print "centre area", cv2.contourArea(bcontours[0])
print "other area", cv2.contourArea(bcontours[1])
################
print marker
#################
def execute(route_length,route_path):
        stepper=0 
        while(1):
                
                ret, frame = cap.read()
                img=imgclip(frame)
                ############ processing starts after clipping
                #wap=grid_draw(img,17,17)
                #cv2.imshow("show",wap)
                hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
                
                bmask = cv2.inRange(hsv, MIN,MAX)
                
                #bret,bthresh = cv2.threshold(bmask,127,255,1)
                #cv2.imshow('binary',mask)
                #cv2.imwrite("wall.jpg",mask)

                bcontours, bh = cv2.findContours(bmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
                bcontours=sorted(bcontours, key = cv2.contourArea, reverse = True)[:12] ##bot
                #bcontours,length=areacon(bcontours,500,300)
                #bcontours=sorted(bcontours, key = cv2.contourArea, reverse = True)[:length]
               
                
                #cv2.drawContours(res,contours,-1,(0,255,0),2)
                cv2.drawContours(img,bcontours,-1,(255,255,0),2)
                
                   
                M = cv2.moments(bcontours[0])
                cx3 = int(M['m10']/M['m00'])
                cy3 = int(M['m01']/M['m00'])
                cv2.circle(img,(cx3,cy3), 5, (0,0,255), -1)
                #print cx3,cy3
                M = cv2.moments(bcontours[1])
                cx4 = int(M['m10']/M['m00'])
                cy4 = int(M['m01']/M['m00'])
                cv2.circle(img,(cx4,cy4), 5, (0,100,100), -1)
                #a,b=gridtopixel(x,y,m,n)
                #print route_path[stepper].y+1,route_path[stepper].x+1
                #print y+1,x+1
                #print getcoor(a,b,m,n)
                #cv2.circle(img,(b,a), 5, (211,200,255), -1)
                
                
                
                bx,by=getcoor(cx3,cy3,n,m)
                
                #print route_path[0].y+1,route_path[0].x+1   [(5,6), (4,6), (3,6), (3,5), (3,4), (3,3)]
                #print "starting point",Y,X
                #print "bot center",bx+1,by+1,"route length",route_length
                #print "other bot",cx4,cy4
                if stepper!=route_length:
                        ser.write("9")
                        X,Y=gridtopixel(route_path[stepper].x,route_path[stepper].y,m,n)#X,Y are pixels of next grid coor
                        cv2.circle(img,(Y,X), 5, (255,100,100), -1)
                        #print "hello123"
                        m1= getslope(cx3,cy3,Y,X)
                        d1=dis(cx3,cy3,Y,X)#distance between bot's center and next path coordinates
                        #print "distance between bot's center and next path coordinates", d1
                        m2= getslope(cx3,cy3,cx4,cy4)
                        d2=dis(cx4,cy4,Y,X)#distance between bot's other point and next path coordinates
                        #print "distance between bot's other point and next path coordinates", d2
                        mid1=(cx3+cx4)/2#mid point of bot center and other point
                        mid2=(cy3+cy4)/2#mid point of bot center and other point
                        bx,by=getcoor(mid1,mid2,n,m) #modified bot center
                        
                        if orientmove(m1,m2,bx+1,by+1,route_path[stepper].y+1,route_path[stepper].x+1,d1,d2)==1: #bot reaches next coor
                                      stepper=stepper+1
                                      flag=0
                                      #print "Bot Coor",bx+1,by+1
                                      #print stepper
                                      #ser.write("7")
                                      #z,c=gridtopixel(route_path[stepper].x,route_path[stepper].y,m,n)
          
                else:
                        ser.write("5")
                        #ser.write("9")
                        break
                                
                                
                        
                
                
                
                                 
                         
        ##########################
                        
                #cv2.imshow('maskcontour',bmask)
                cv2.imshow('ori',img)
                if cv2.waitKey(1) == 27:  ## 27 - ASCII for escape key
                        break
        ##############
if flag!=0:
        rx,ry=getcoor(rx,ry,n,m)
        bx,by=getcoor(bx,by,n,m)
        yx,yy=getcoor(yx,yy,n,m)
        bt1,bt2=getcoor(marker[6][0],marker[6][1],n,m)#bot
        
        b1,b2=getcoor(marker[3][0],marker[3][1],n,m)# red table 1
        y1,y2=getcoor(marker[5][0],marker[5][1],n,m)# blue table 2
        r1,r2=getcoor(marker[4][0],marker[4][1],n,m)# red table 3
        ##
        start=GridPoint(bt2,bt1)
        stop=GridPoint(ry,rx)
        length,route=solve(start,stop,frame)# path 1
        execute(length,route)# going for red provision 1
        ser.write("R")#for glowing red led
        ser.write("g")
        ##
        
        #print r1,r2
        start=GridPoint(ry,rx)
        stop=GridPoint(r2+1,r1)
        length,route=solve(start,stop,frame) #path 2
        execute(length,route)# going for red table 3
        ser.write("O")#for glowing off red led
        ##
        ##
        start=GridPoint(r2+1,r1)
        stop=GridPoint(b2+1,b1)
        length,route=solve(start,stop,frame) #path 3
        execute(length,route)# going for red table 1
        ser.write("o")#for glowing red led
        ##

       
        
        start=GridPoint(b2+1,b1)
        stop=GridPoint(by,bx)
        length,route=solve(start,stop,frame)#path 4
        execute(length,route)# going for blue provision
        ser.write("b")#for glowing on blue led
        ##

        start=GridPoint(by,bx)
        stop=GridPoint(y2+1,y1)
        length,route=solve(start,stop,frame) #path 5
        execute(length,route)# going for blue table 2
        ser.write("o")#for glowing off blue led
        ##
        '''
        start=GridPoint(by,bx)
        stop=GridPoint(b2+1,b1)
        length,route=solve(start,stop,frame)#path 6
        execute(length,route)# going for blue demand
        ser.write("o")#for glowing off  blue led
        '''
        ser.write("7") #buzzer on for 5 seconds
        sleep(6)
        ser.write("9")#buzzer off
        ser.close()
        ##
#print route_path[route_length-2].y+1,route_path[route_length-2].x+1
#print x,y

#####################

##############################################


#execute()
#print len(contours)
cv2.destroyAllWindows()
