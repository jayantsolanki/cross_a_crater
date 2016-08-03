import numpy
import cv2
import serial
import math
from time import sleep
ser=serial.Serial(3) #COM4
grid_line_x = 17
grid_line_y = 17
grid_start = 0
grid_end = 0
grid_map = [ [ 0 for i in range(grid_line_y-1) ] for j in range(grid_line_x-1) ]
line_widthm=540/16
line_widthn=480/16
mbs=0
#MIN = numpy.array([95, 100, 100],numpy.uint8)  #identifies blue marker
#MAX = numpy.array([130, 255, 255],numpy.uint8)

RMIN = numpy.array([0, 100, 100],numpy.uint8)  #for red marker
RMAX = numpy.array([30, 255, 255],numpy.uint8)

#MIN = numpy.array([40 ,100, 100],numpy.uint8)  #for green
#MAX = numpy.array([55, 255, 255],numpy.uint8)

#MIN = numpy.array([75 ,100, 100],numpy.uint8)   #wall detection
#MAX = numpy.array([95, 255, 255],numpy.uint8)
MIN = numpy.array([65 ,110, 50],numpy.uint8)   ##wall
MAX = numpy.array([90, 255, 255],numpy.uint8)
#BMIN = numpy.array([0 ,50, 100],numpy.uint8)    #bot when kept on newspaper sheets
#BMAX = numpy.array([30, 150, 255],numpy.uint8)
##############
def imgclip(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        lower = numpy.array([0, 0, 0]) #black color mask
        upper = numpy.array([120, 120, 120])
        mask = cv2.inRange(frame, lower, upper)

        ret,thresh1 = cv2.threshold(mask,127,255,cv2.THRESH_BINARY)
        contours, hierarchy = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #cv2.drawContours(frame,contours,-1,(0,255,0),3)
        biggest = 0
        max_area = 0
        min_size = thresh1.size/4
        index1 = 0
        for i in contours:
                area = cv2.contourArea(i)
                if area > 10000:
                    peri = cv2.arcLength(i,True)
                if area > max_area: 
                    biggest = index1
                    max_area = area
                index1 = index1 + 1
        approx = cv2.approxPolyDP(contours[biggest],0.05*peri,True)
        #drawing the biggest polyline
        cv2.polylines(frame, [approx], True, (0,255,0), 3)
        x1 = approx[0][0][0]
        y1 = approx[0][0][1]
        x2 = approx[1][0][0]
        y2 = approx[1][0][1]
        x3 = approx[3][0][0]
        y3 = approx[3][0][1]
        x4 = approx[2][0][0]
        y4 = approx[2][0][1]
        #print x1,y1,x2,y2,x3,y3,x4,y4
        

        #points remapped from source image from camera
        #to cropped image try to match x1, y1,.... to the respective near values
        pts1 = numpy.float32([[x1,y1],[x2,y2],[x3,y3],[x4,y4]]) 
        pts2 = numpy.float32([[0,0],[0,480],[540,0],[540,480]])
        persM = cv2.getPerspectiveTransform(pts1,pts2)
        img = cv2.warpPerspective(frame,persM,(540,480))
        return img
        ###clipping ends
############
cap = cv2.VideoCapture(1)
rx=0
ry=0
bx=0
by=0
yx=0
yy=0

ret, img = cap.read()
frame=imgclip(img)
hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
#####getting red coor
mask = cv2.inRange(hsv, RMIN,RMAX)
res = cv2.bitwise_and(frame,frame, mask= mask)
#cv2.imshow('hsv',res)
#cv2.imwrite("hola.jpg",hsv)
ret,thresh = cv2.threshold(mask,127,255,1)
contours, h = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours=sorted(contours, key = cv2.contourArea, reverse = True)[:3] ##obstacles
M = cv2.moments(contours[1])
cx1 = int(M['m10']/M['m00'])
cy1 = int(M['m01']/M['m00'])
print cx1,cy1
cv2.circle(res,(cx1,cy1), 5, (0,0,255), -1)
##
M = cv2.moments(contours[2])
cx2 = int(M['m10']/M['m00'])
cy2 = int(M['m01']/M['m00'])
print cx2,cy2
#cv2.circle(res,(cx2,cy2), 5, (0,0,255), -1)
##
if(cx1<269):
        rx=cx1
        ry=cy1
else:   
        rx=cx2
        ry=cy2
print rx,ry

#####################
############################################
def obstacle(hsv):
    lower = numpy.array([70,100,100])
    upper = numpy.array([85,255,255])

    mask = cv2.inRange(hsv,lower, upper)
    kernel = numpy.ones((50,40),numpy.uint8)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    erosion = cv2.erode(mask,kernel,iterations = 1)
    dilation = cv2.dilate(closing,kernel,iterations = 1)#obstacle = cv2.dilate(closing,kernel,iterations = 1)
    #cv2.imshow('obstacle',dilation)
    #cv2.imwrite('obstacle.jpg',dilation)
    return dilation
#################################
h,k,l=frame.shape
line_widthm=h/(grid_line_x-1)
line_widthn=k/(grid_line_y-1)
#img = grid_draw(frame,grid_line_x,grid_line_y)
obstacle=obstacle(hsv)
#draw_obstacle(obstacle)
#cv2.imshow('obstacle',obstacle)
def drawgrid(img,m,n):
    '''
    img-- a single test image as inumpyut argument
    route_length  -- returns the single integer specifying the route length
    '''
    global grid_map
    xs=0 #start coordinates, depicting  horizontal rows in grid_map, vertical column for image
    ys=0 #start coordinates, depicting  vertical column in grid_map, horizontal row for image
    xe=0 #end coordinates
    ye=0
    
    #creating mxn matrix space map with black as obstable and other colors as paths.
    for x in range(0,m-1):
        X=x*line_widthm+(line_widthm/2)
        for y in range(0,n-1):
            Y=y*line_widthn+(line_widthn/2)
            if img[X,Y]>=70 or x==0 or y==0 or y==n-2 or x==m-2:#and img[X,Y,1]>=70 and img[X,Y,2]>=70: #obstacle black ,bgr value(0,0,0)
                grid_map[x][y]=1
                cv2.circle(img,(Y,X), 5, (0,0,255), -1)
            continue
    #print grid_map
    
    return 0
    

##############################################
def getcoor(x,y):
        cx=x/line_widthm
        cy=y/line_widthn
        return cx,cy
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
        bcontours=sorted(bcontours, key = cv2.contourArea, reverse = True)[:2] ##bot
       
        
        #cv2.drawContours(res,contours,-1,(0,255,0),2)
        cv2.drawContours(bmask,bcontours,-1,(255,255,0),2)
        
        ##drawing centtres of each contours
        
        '''
        M = cv2.moments(contours[6])
        cx3 = int(M['m10']/M['m00'])
        cy3 = int(M['m01']/M['m00'])
        cv2.circle(res,(cx3,cy3), 5, (0,0,255), -1)

        M = cv2.moments(contours[5])
        cx4 = int(M['m10']/M['m00'])
        cy4 = int(M['m01']/M['m00'])
        cv2.circle(res,(cx4,cy4), 5, (0,0,255), -1)
        '''
        M = cv2.moments(bcontours[0])
        cx3 = int(M['m10']/M['m00'])
        cy3 = int(M['m01']/M['m00'])
        cv2.circle(img,(cx3,cy3), 5, (0,0,255), -1)
        print cx3,cy3
        M = cv2.moments(bcontours[1])
        cx4 = int(M['m10']/M['m00'])
        cy4 = int(M['m01']/M['m00'])
        cv2.circle(img,(cx4,cy4), 5, (0,0,255), -1)

        #db1=math.sqrt((cx5-cx1)*(cx5-cx1)+(cy5-cy1)*(cy5-cy1))
        '''
        cv2.line(res,(cx5,cy5),(cx1,cy1),(255,0,0), 2)
        cv2.line(res,(cx5,cy5),(cx2,cy2),(255,0,0), 2)
        cv2.line(res,(cx5,cy5),(cx3,cy3),(255,0,0), 2)
        cv2.line(res,(cx5,cy5),(cx4,cy4),(255,0,0), 2)
        '''
        ax,ay=getcoor(rx,ry)
        bx,by=getcoor(cx3,cy3)
        if ax==bx and ay==by:
                ser.write("5")
        print bx,by
        print ax,ay
        mbs=-(float)(cy3-ry)/(cx3-rx)
        #print mbs
        if cx4-cx3!=0:
                mbb=-(float)(cy4-cy3)/(cx4-cx3)
        else:
                ser.write("4")
                ser.write("5")
        #print mbb
        
        if mbs*mbb!=-1:
                theta=math.atan((mbs-mbb)/(1+mbs*mbb))
                print theta
                if theta<-0.2 or theta>0.2:
                        #com=1
                        if theta<-0.1:
                               ser.write("6")  #right turn
                        else:
                               ser.write("4")   #left turn
                        #com = raw_input()
                        
                        #ser.write(com) #send command
                
                else:
                         ser.write("5")
                         ser.write("8")
                         
                 
##########################
        #cv2.imshow('maskcontour',bmask)
        cv2.imshow('ori',img)
        if cv2.waitKey(1) == 27:  ## 27 - ASCII for escape key
                break
##############


#print len(contours)
cv2.destroyAllWindows()
