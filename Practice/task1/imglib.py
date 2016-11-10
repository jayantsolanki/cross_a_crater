import numpy
import cv2
import heapq
from motion import *
grid_line_x = 7
grid_line_y = 7
m=600/(grid_line_x-1)
n=600/(grid_line_y-1)
# m=480/(grid_line_x-1)
# n=540/(grid_line_y-1)
a1=0
b1=0
a2=0
b2=0
a3=0
b3=0
a4=0
b4=0
clipcount=0
###############################
# trims contours accoding to given area
#
#
#
def areacon(contours,area,sub):
        count=0
        #con=0
        for i in range(len(contours)):
                ar = cv2.contourArea(contours[i])
                #print ar,area
                if ar>area-sub and ar<area+sub:#detecting provision marker
                        contours[count]=contours[i]
                        count=count+1
                        #print count
        return contours,count        
                        
# ###############################
# # detects number and sign
# #
# #
# #
# def detectCellVal(outImg,img_rgb,patch,symbol,threshold,grid_map):
#         img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
#         template = cv2.imread(patch)
#         temp_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
#         w, h = temp_gray.shape[::-1]
#         # print w,h
#         res = cv2.matchTemplate(img_gray,temp_gray,cv2.TM_CCOEFF_NORMED)
#         # threshold = 0.616#change this to match
#         loc = numpy.where( res >= threshold)
#         for pt in zip(*loc[::-1]):
#           print pt
#           x,y=getcoor(pt[0]+w/2,pt[1]+h/2,m,n)
#           grid_map[y][x]=symbol
#           cv2.rectangle(outImg, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
#         return outImg,grid_map       
                        
                        
                                                
        

########################################
##############
# Image clipper
#
#
#
#
def imgclip(frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)#where is gray getting used
        # lower = numpy.array([0, 0, 0]) #black color mask
        # upper = numpy.array([120, 120, 120])
        global a1,a2,a3,a4,b1,b2,b3,b4, clipcount #new change 14 sept
        clipcount=clipcount+1
        lower = numpy.array([0, 0, 0]) #black color mask
        upper = numpy.array([179, 56, 45])
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
        if clipcount<=2 or (a1==0 and b1==0 and a2==0 and b2==0 and a3==0 and b3==0 and a4==0 and b4==0):#new change 14 sept

            x1 = approx[0][0][0]
            y1 = approx[0][0][1]
            x2 = approx[1][0][0]
            y2 = approx[1][0][1]
            x3 = approx[3][0][0]
            y3 = approx[3][0][1]
            x4 = approx[2][0][0]
            y4 = approx[2][0][1]
            a1=x1
            a2=x2
            a3=x3
            a4=x4
            b1=y1
            b2=y2
            b3=y3
            b4=y4
        # print x1,y1,x2,y2,x3,y3,x4,y4
        # x1 = 570
        # y1 = 110
        # x2 = 69
        # y2 = 100
        # x3 = 570
        # y3 = 390
        # x4 = 70
        # y4 = 400

        #points remapped from source image from camera
        #to cropped image try to match x1, y1,.... to the respective near values
        # A,B,C,D
        # pts1 = numpy.float32([[x1,y1],[x2,y2],[x3,y3],[x4,y4]]) 
        # pts2 = numpy.float32([[0,0],[0,480],[320,0],[320,480]])
        # pts1 = numpy.float32([[a1,b1],[a2,b2],[a3,b3],[a4,b4]]) 
        # pts2 = numpy.float32([[0,0],[0,480],[320,0],[320,480]])
        pts1 = numpy.float32([[a3,b3],[a1,b1],[a4,b4],[a2,b2]]) 
        pts2 = numpy.float32([[0,0],[0,480],[320,0],[320,480]])
        persM = cv2.getPerspectiveTransform(pts1,pts2)
        img = cv2.warpPerspective(frame,persM,(320,480))
        return img
        ###clipping ends
############
############
# Obstacle dilation
#
#
#
############################################
def obstacle(hsv):
    lower = numpy.array([53 ,112, 34],numpy.uint8)
    upper = numpy.array([94, 255, 255],numpy.uint8)
    # lower = numpy.array([22 ,57, 208],numpy.uint8)#obstacle green
    # upper = numpy.array([75, 251, 253],numpy.uint8)
    # lower = numpy.array([0 ,0, 0],numpy.uint8)
    # upper = numpy.array([179, 255, 88],numpy.uint8) #different black
    # lower = numpy.array([0, 0, 0]) #black color mask
    # upper = numpy.array([120, 120, 120])
    mask = cv2.inRange(hsv,lower, upper)
    contours, hierarchy = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    contours=sorted(contours, key = cv2.contourArea, reverse = True)[:]
    contours,length=areacon(contours,2500,2000)
    contours=sorted(contours, key = cv2.contourArea, reverse = True)[:length]
    cv2.fillPoly(mask,contours, (255,255,255))
    # cv2.imshow('maksed',mask)
    #kernel = numpy.ones((50,40),numpy.uint8)
    kernel = numpy.ones((33,33),numpy.uint8)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    #erosion = cv2.erode(mask,kernel,iterations = 1)
    dilation = cv2.dilate(closing,kernel,iterations = 1)#obstacle = cv2.dilate(closing,kernel,iterations = 1)
    cv2.imshow('Obstacle dilation',dilation)
    return mask, dilation
#################################
#################################
#draw grid with obstacles marked
#
#
#
def markobstacle(obb,imgg,m,n):
        h,k,l=imgg.shape
        widm=h/(m-1)
        widn=k/(n-1)
        '''
        img-- a single test image as inumpyut argument
        route_length  -- returns the single integer specifying the route length
        '''
        global grid_map

        #cv2.imshow("walls in grid map",obb)
        for x in range(0,m-1):
                X=x*widm+(widm/2)
                for y in range(0,n-1):
                        Y=y*widn+(widn/2)
                        # print 
                        if obb[X,Y]>=200 or x==0 or x==m-2 or y==0 or y==n-2:#and frame[X,Y,1]>=70 and frame[X,Y,2]>=70: #obstacle black ,bgr value(0,0,0)
                                grid_map[x][y]=1
                                cv2.circle(imgg,(Y,X), 5, (0,50,200), -1)
                        continue
        #print grid_map
        return grid_map,imgg
        

##############################################
##################
# grid draw
#
#
#
def grid_draw(image,mm,nn): ##filename is image filename with full file path, n is grid of n lines

    #img=cv2.imread(filename) ##getting input image
    h,k,l=image.shape
    widm=h/(mm-1)
    widn=k/(nn-1)
    for x in range(0, mm): ##drawing lines
        X=x*widm
        cv2.line(image,(0,X),(k,X),(0,0,0), 2)#lines is red color, bgr format
    for y in range(0, nn): ##drawing lines
        Y=y*widn
        cv2.line(image,(Y,0),(Y,h),(0,0,0), 2)
    return (image)
###################


###########################################
# calculate contours coordinates
#
#
#
#
def ccoor(contour):
        M = cv2.moments(contour)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        return cx,cy
###############################
# detects number and sign
#
#
#
def solveGrid(grid_map):
        operator='+'
        for i in range(0,6):
            operator='+'
            for j in range(0,5):
                # print grid_map[i][j]
                if str(grid_map[i][j])=='+' and j%2==1:
                    operator='+'
                    # grid_map[i][5]=grid_map[i][5]+grid_map[i][j]
                elif str(grid_map[i][j])=='-' and j%2==1:
                    operator='-'
                    # grid_map[i][5]=grid_map[i][5]-grid_map[i][j]
                elif j%2==0:
                    if operator=='+':
                        grid_map[i][5]=grid_map[i][5]+grid_map[i][j]
                    else:
                        grid_map[i][5]=grid_map[i][5]-grid_map[i][j]
        return grid_map  
