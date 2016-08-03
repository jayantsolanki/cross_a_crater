
'''
**************************************************************************
*                  IMAGE PROCESSING (e-Yantra 2014)
*                  ================================
*  This software is intended to teach image processing concepts
*
*  MODULE: Functions
*  Filename: threshImage.py
*  Version: 1.0.0  
*  Date: November 3, 2014
*  
*  Author: Arun Mukundan, e-Yantra Project, Department of Computer Science
*  and Engineering, Indian Institute of Technology Bombay.
*  
*  Software released under Creative Commons CC BY-NC-SA
*
*  For legal information refer to:
*        http://creativecommons.org/licenses/by-nc-sa/4.0/legalcode 
*     
*
*  This software is made available on an “AS IS WHERE IS BASIS”. 
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using 
*  ICT(NMEICT)
*
**************************************************************************
'''

############################################
## Import OpenCV
import numpy as np
import cv2
import heapq ##priority queue
import serial
import math
from time import sleep
##########################################

#ser=serial.Serial(3)
##########################################
grid_line_x = 18
grid_line_y = 18
grid_start = 0
grid_end = 0
grid_map = [ [ 0 for i in range(grid_line_y-1) ] for j in range(grid_line_x-1) ]
line_widthm=0
line_widthn=0
###########################################
obstacle_position = [[0 for x in range(2)] for x in range(9)]
provision = [[0 for x in range(3)] for x in range(3)]
bed_demand = [[0 for x in range(3)] for x in range(3)]
Bot_position = [[0 for x in range(2)] for x in range(2)]


############################################
def obstacle(hsv):
    lower = np.array([70,100,100])
    upper = np.array([85,255,255])

    mask = cv2.inRange(hsv,lower, upper)
    kernel = np.ones((50,40),np.uint8)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    erosion = cv2.erode(mask,kernel,iterations = 1)
    dilation = cv2.dilate(closing,kernel,iterations = 1)#obstacle = cv2.dilate(closing,kernel,iterations = 1)
    #cv2.imshow('obstacle',dilation)
    #cv2.imwrite('obstacle.jpg',dilation)
    return dilation

#########################################
def draw_obstacle(img):

    contours, hierarchy = cv2.findContours(img,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours, key = cv2.contourArea, reverse = True)[:9]
    cv2.drawContours(orig_img,contours,-1,(255,0,0),1)
    
   #print len(contours)
    for i in range(len(contours)):
        #print "Area = ", cv2.contourArea(contours[i])
        #print "Perimeter = ", cv2.arcLength(contours[i],True)
        M = cv2.moments(contours[i])
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        #print "Centroid = ", cx, ", ", cy
        cv2.circle(orig_img,(cx,cy), 5, (0,0,0), -1)
        obstacle_position[i][0]=cx
        obstacle_position[i][1]=cy
    
    
############################################
def red_provision(hsv):
    lower = np.array([0,100,100])
    upper = np.array([30,255,255])

    mask = cv2.inRange(hsv,lower, upper)
    kernel = np.ones((20,20),np.uint8)
    erosion = cv2.erode(mask,kernel,iterations = 1)
    dilation = cv2.dilate(erosion,kernel,iterations = 1)
    
    contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours, key = cv2.contourArea, reverse = True)[:4]
    cv2.drawContours(orig_img,contours,-1,(255,0,0),1)
    #print len(contours)
    red = [[0 for x in range(0,2)] for x in range(0,len(contours))]
    for i in range(len(contours)):
        #print "Area = ", cv2.contourArea(contours[i])
        #print "Perimeter = ", cv2.arcLength(contours[i],True)
        M = cv2.moments(contours[i])
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        #print "Centroid = ", cx, ", ", cy
        cv2.circle(orig_img,(cx,cy), 5, (255,255,0), -1)
        if cx < 270:  
            provision[cy/160][0]=cx
            provision[cy/160][1]=cy
            provision[cy/160][2]=1
        else:
            bed_demand[cy/160][0]=cx
            bed_demand[cy/160][1]=cy
            bed_demand[cy/160][2]=1
            
#####################################   
def blue_provision(hsv):
    lower = np.array([85,69,203])
    upper = np.array([120,255,255])

    mask = cv2.inRange(hsv,lower, upper)
    kernel = np.ones((20,20),np.uint8)
    erosion = cv2.erode(mask,kernel,iterations = 1)
    dilation = cv2.dilate(erosion,kernel,iterations = 1)
    
    contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours, key = cv2.contourArea, reverse = True)[:4]
    cv2.drawContours(orig_img,contours,-1,(255,0,0),1)
    #print len(contours)
    blue = [[0 for x in range(2)] for x in range(len(contours))]
    for i in range(len(contours)):
        #print "Area = ", cv2.contourArea(contours[i])
        #print "Perimeter = ", cv2.arcLength(contours[i],True)
        M = cv2.moments(contours[i])
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        #print "Centroid = ", cx, ", ", cy
        cv2.circle(orig_img,(cx,cy), 5, (255,0,255), -1)
        if cx < 270:  
            provision[cy/160][0]=cx
            provision[cy/160][1]=cy
            provision[cy/160][2]=2
        else:
            bed_demand[cy/160][0]=cx
            bed_demand[cy/160][1]=cy
            bed_demand[cy/160][2]=2
            
#############################
def yellow_provision(hsv):
    lower = np.array([25,100,215])
    upper = np.array([55,255,255])

    mask = cv2.inRange(hsv,lower, upper)
    kernel = np.ones((20,20),np.uint8)
    erosion = cv2.erode(mask,kernel,iterations = 1)
    dilation = cv2.dilate(erosion,kernel,iterations = 1)
    contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours, key = cv2.contourArea, reverse = True)[:4]
    cv2.drawContours(orig_img,contours,-1,(255,0,0),1)
    #print len(contours)
    yellow = [[0 for x in range(2)] for x in range(len(contours))]
    for i in range(len(contours)):
        #print "Area = ", cv2.contourArea(contours[i])
        #print "Perimeter = ", cv2.arcLength(contours[i],True)
        M = cv2.moments(contours[i])
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        #print "Centroid = ", cx, ", ", cy
        cv2.circle(orig_img,(cx,cy), 5, (0,255,255), -1)
        if cx < 270:  
            provision[cy/160][0]=cx
            provision[cy/160][1]=cy
            provision[cy/160][2]=3
        else:
            bed_demand[cy/160][0]=cx
            bed_demand[cy/160][1]=cy
            bed_demand[cy/160][2]=3
            
##############################          
def bot_position(hsv):
    
    front_end_of_bot_lower = np.array([118,128,159])
    front_end_of_bot_upper = np.array([159,255,255])
    
    back_end_of_bot_lower = np.array([30,75,110])
    back_end_of_bot_upper = np.array([40,255,230])

    
    #####front end masking and centroid
    mask = cv2.inRange(hsv,front_end_of_bot_lower, front_end_of_bot_upper)
    kernel = np.ones((10,10),np.uint8)
    front_closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    front_dilation = cv2.dilate(front_closing,kernel,iterations = 1)
    front_contours, hierarchy = cv2.findContours(front_dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    front_contours=sorted(front_contours, key = cv2.contourArea, reverse = True)[:2]
    cv2.drawContours(orig_img,front_contours,0,(255,0,0),1)

    M = cv2.moments(front_contours[0])
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    #print "Centroid = ", cx, ", ", cy
    cv2.circle(orig_img,(cx,cy), 5, (0,0,0), -1)
    Bot_position[0][0]=cx
    Bot_position[0][1]=cy
    
    #####back end masking and centroid
    mask = cv2.inRange(hsv,back_end_of_bot_lower, back_end_of_bot_upper)
    kernel = np.ones((10,10),np.uint8)
    back_closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    back_dilation = cv2.dilate(back_closing,kernel,iterations = 1)
    back_contours, hierarchy = cv2.findContours(back_dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    back_contours=sorted(back_contours, key = cv2.contourArea, reverse = True)[:2]
    cv2.drawContours(orig_img,back_contours,0,(0,0,0),1)

    M = cv2.moments(back_contours[0])
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    #print "Centroid = ", cx, ", ", cy
    cv2.circle(orig_img,(cx,cy), 5, (0,0,255), -1)
    Bot_position[1][0]=cx
    Bot_position[1][1]=cy
    #cv2.imshow('bot_position',img)
    
############draw line
def line_draw(img,cx1,cy1,cx2,cy2):
    ###calculating slope of white ball's and stick's centroids coordinate system
    slope=(float)(cy1-cy2)/(cx2-cx1);
    cv2.line(orig_img,(cx1,cy1),(cx2,cy2),(255,0,0),5)
    
##############################################
def grid_draw(img,m,n): ##filename is image filename with full file path, n is grid of n lines

    #img=cv2.imread(filename) ##getting input image
    for x in range(0, m): ##drawing lines
        X=x*line_widthm
        cv2.line(img,(0,X),(k,X),(0,0,0), 2)#lines is red color, bgr format
    for y in range(0, n): ##drawing lines
        Y=y*line_widthn
        cv2.line(img,(Y,0),(Y,h),(0,0,0), 2)
    return (img)

############################################
def solve(start,finish,img,orig_img): #no heuristics used
    """Find the shortest path from START to FINISH."""
    
    heap=[]
    link = {} # parent node link
    g = {} # shortest path to a current node
    h = {} # heuristic function
    g[start] = 0 #initial distance to node start is 0
    
    link[start] = None #parent of start node is none
    
    
    heapq.heappush(heap, (0, start))
    
    while True:
        
        f, current = heapq.heappop(heap) ##taking current node from heap
        #print current
        if current == finish:
            name='Shortest Path, image#'
            i=int(100*np.random.rand())
            name=name+str(i)
            route=build_path(start, finish, link)
            ####Drawing path , just for pictorial representation######
            for i in range(1,len(route)):
                cv2.line(orig_img,(route[i-1].y*line_widthn+(line_widthn/2),route[i-1].x*line_widthm+(line_widthm/2)),(route[i].y*line_widthn+(line_widthn/2),route[i].x*line_widthm+(line_widthm/2)),(232,162,0), 3)
            #cv2.imshow('name',img)
            ############################
            return g[current], route[1:len(route)]
            
        
        moves = current.get_moves()
        cost = g[current]
        for mv in moves:
            #print mv.x,mv.y
            if grid_map[mv.x][mv.y]==1: #bypass obstacles
                continue
                #mv is the neighbour of current cell, in all maximum 4 neighbours will be there
            if  (mv not in g or g[mv] > cost + 1): #check if mv is already visited or if its cost is higher than available cost then update it
                g[mv] = cost + 1
                
                link[mv] = current #storing current node as parent to mv 
                heapq.heappush(heap, (g[mv], mv)) ##adding updated cost and visited node to heap
                #cv2.circle(orig_img,(mv.y*line_widthn+line_widthn/2,mv.x*line_widthm+line_widthm/2), 5, (255,144,0), -1)

###########################################################   
def build_path(start, finish, parent):
    
    #create path from start to finish

    x = finish ##back tracking the path from goal to start
    xs = [x]
    while x != start: #going back
        x = parent[x]
        xs.append(x)
    xs.reverse()
 
    return xs

###########################################################
class GridPoint(object):
    """Represent a position on a grid."""
    def __init__(self, x, y): #self referencing x and  y coordinates
        self.x = x
        self.y = y

    def __hash__(self): #returning hash value of the GridPoint object
        return hash((self.x, self.y))

    def __repr__(self):                         #returns values stored in current object, values are x and y coordinates
        return "(%d,%d)" % (self.y+1, self.x+1)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def get_moves(self): ##taking current node coordinates to find neighbours of it
        
        
        if self.x>=0 and self.x<=len(grid_map)-1 and self.y>=0 and self.y<=len(grid_map)-1:
            
            if self.x + 1<len(grid_map):
                yield GridPoint(self.x + 1, self.y)
            if self.y + 1<len(grid_map):  
                yield GridPoint(self.x, self.y + 1)
            if self.x - 1>-1:
                yield GridPoint(self.x - 1, self.y)
            if self.y - 1>-1:
                yield GridPoint(self.x, self.y - 1)
            #############adding diagonal movement too
                
            if self.x + 1<len(grid_map) and self.y + 1<len(grid_map):
                yield GridPoint(self.x + 1, self.y+1)
            if self.y + 1<len(grid_map) and  self.x - 1>-1:  
                yield GridPoint(self.x-1, self.y + 1)    
            if self.x - 1>-1 and self.y - 1>-1:
                yield GridPoint(self.x - 1, self.y-1)
            if self.y - 1>-1 and self.x + 1<len(grid_map):
                yield GridPoint(self.x+1, self.y - 1)
            
                
            
                
            

#############################################################
def play(orig_img,img,m,n):
    '''
    img-- a single test image as input argument
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
                cv2.circle(orig_img,(Y,X), 5, (0,0,255), -1)
            continue
    #print grid_map
    grid_start = GridPoint((Bot_position[1][1]/line_widthm),(Bot_position[1][0]/line_widthn)) ##reversing coordinates so that it can be compatible with coordinate system of matrix
    
    grid_end_provision1 = GridPoint((provision[0][1]/line_widthm),(provision[0][0]/line_widthn))
    grid_end_provision2 = GridPoint((provision[1][1]/line_widthm),(provision[1][0]/line_widthn))
    grid_end_provision3 = GridPoint((provision[2][1]/line_widthm),(provision[2][0]/line_widthn))
    #grid_end_provision1=GridPoint(2,12)
    grid_end_bed_demand1 = GridPoint((bed_demand[0][1]/line_widthm)+1,(bed_demand[0][0]/line_widthn))
    grid_end_bed_demand2 = GridPoint((bed_demand[1][1]/line_widthm)+1,(bed_demand[1][0]/line_widthn))
    grid_end_bed_demand3 = GridPoint((bed_demand[2][1]/line_widthm)+1,(bed_demand[2][0]/line_widthn))
    #print grid_start,grid_end
    route_length_provision1, route_path_provision1=solve(grid_start,grid_end_provision1,img,orig_img)
    
    route_length_provision2, route_path_provision2=solve(grid_start,grid_end_provision2,img,orig_img)
 
    route_length_provision3, route_path_provision3=solve(grid_start,grid_end_provision3,img,orig_img)
    '''
    route_length_bed_demand1, route_path_bed_demand1=solve(grid_start,grid_end_bed_demand1,img,orig_img)
    route_length_bed_demand2, route_path_bed_demand2=solve(grid_start,grid_end_bed_demand2,img,orig_img)
    route_length_bed_demand3, route_path_bed_demand3=solve(grid_start,grid_end_bed_demand3,img,orig_img)
    '''
    grid_map = [[0 for i in range(grid_line_y-1)]for j in range(grid_line_x-1)] #resetting grid map to 0s
    #min(route_length_provision1,route_length_provision2,route_length_provision3)
    return route_length_provision1, route_path_provision1 #return the values calculated
    

##############################################
def co_ordinates(hsv):
    red_provision(hsv)
    blue_provision(hsv)
    yellow_provision(hsv)
    bot_position(hsv)
    #cv2.line(orig_img,(Bot_position[1][0],Bot_position[1][1]),(Bot_position[0][0],Bot_position[0][1]),(0,0,255),2)
    #cv2.line(orig_img,(Bot_position[1][0],Bot_position[1][1]),(provision[0][0],provision[0][1]),(0,0,255),2)
    #cv2.line(orig_img,(Bot_position[1][0],Bot_position[1][1]),(bed_demand[0][0],bed_demand[0][1]),(0,0,255),2)
    #follow_path(Bot_position[1][0],Bot_position[1][1],provision[2][0],provision[2][1],Bot_position[0][0],Bot_position[0][1])
                
'''##############################################
##########
#ser=serial.Serial(3) #COM4
##########
##############################################
def follow_path(cx1,cy1,cx2,cy2,cx3,cy3):
    slope_destination=(float)(cy2-cy1)/(cx2-cx1);
    slope_bot=(float)(cx3-cy1)/(cx3-cx1);
    angle= (slope_destination - slope_bot)/1+(slope_destination*slope_bot)
    while(1):#drawing line
        value =cy3-(float)(slope_destination)*(cx3)-cy3
        if cx1==cx3 and cy1==cy3:
            #ser.write("5")
            print 'stop'
            break
        if (value < 0) and angle > 0:
            #ser.write("4")
            print 'turn left'
            continue
        elif (value < 0) and angle < 0:
            #ser.write("6")
            print 'turn right'
            continue
        elif (value > 0) and angle > 0:
            #ser.write("6")
            print 'turn right'
            continue
        elif (value > 0) and angle < 0:
            #ser.write("4")
            print 'turn left'
            continue
        else :
            #ser.write("8")
            print 'move forward'
        
################################################
def shortest_path_provision1():
    for i in range(1,4):
        if provision1[i-1][2]==1:
            while(1):
                follow_path(Bot_position[1][0],Bot_position[1][1],provision[i-1][0],provision[i-1][1],Bot_position[0][0],Bot_position[0][1])
                break
def shortest_path_provision2():
    for i in range(1,4):
        if provision1[i-1][2]==2:
            while(1):
                follow_path(Bot_position[1][0],Bot_position[1][1],provision[i-1][0],provision[i-1][1],Bot_position[0][0],Bot_position[0][1])
                break
def shortest_path_provision3():
    for i in range(1,4):
        if provision1[i-1][2]==k:
            while(1):
                follow_path(Bot_position[1][0],Bot_position[1][1],provision[i-1][0],provision[i-1][1],Bot_position[0][0],Bot_position[0][1])
                break
def shortest_path_provision(k):
    for i in range(1,4):
        if provision1[i-1][2]==k:
            while(1):
                follow_path(Bot_position[1][0],Bot_position[1][1],provision[i-1][0],provision[i-1][1],Bot_position[0][0],Bot_position[0][1])
                break
            
################################################
def shortest_path():
    for i in range(1,3):
        if bed_demand[i-1][2]==1:
            shortest_path_provision1()
            
        elif bed_demand[i-1][2]==2:
            shortest_path_provision2()

        else:
            shortest_path_provision3()
    while(1):
        follow_path(Bot_position[1][0],Bot_position[1][1],bed_demand[0][0],bed_demand[0][1],Bot_position[0][0],Bot_position[0][1])
        break
    while(1):
        follow_path(Bot_position[1][0],Bot_position[1][1],bed_demand[1][0],bed_demand[1][1],Bot_position[0][0],Bot_position[0][1])
        break
    k=bed_demand[2][2]            
    shortest_path_provision(k)
    while(1):
        follow_path(Bot_position[1][0],Bot_position[1][1],bed_demand[2][0],bed_demand[2][1],Bot_position[0][0],Bot_position[0][1])
        break    
    
North=1
South=0
East=0
West=0
Direction=1

####################################################
ser=serial.Serial(3) #COM4
#print "Enter 8 for forward, 2 for backward, 5 for stop, 4 for left, 6 for right, 0 to quit"
for i in range(0,len(route_path)-1):
    
    print i
    if Direction==North:
        if route_path[i].y+1==route_path[i+1].y+1 and route_path[i].x+1==route_path[i+1].x+2 :
            ser.write("8")
            cv2.waitKey(2000)
            print "N"
        if route_path[i].y+1==route_path[i+1].y+2 and route_path[i].x+1==route_path[i+1].x+1 :
            ser.write("4")
            cv2.waitKey(800)
            East=1
            North=0
            print "hi"
        if route_path[i].y+1==route_path[i+1].y and route_path[i].x+1==route_path[i+1].x+1 :
            ser.write("6")
            cv2.waitKey(800)
            West=1
            North=0
            print "hittt",route_path[i].y+1,route_path[i+1].y+2,route_path[i].x+1,route_path[i+1].x+1
    if Direction==South:
        if route_path[i].y+1==route_path[i+1].y+1 and route_path[i].x+1==route_path[i+1].x :
            ser.write("8")
            cv2.waitKey(2000)
            print "N"
        if route_path[i].y+1==route_path[i+1].y and route_path[i].x+1==route_path[i+1].x+1 :
            ser.write("4")
            cv2.waitKey(800)
            West=1
            South=0
            print "hi"
        if route_path[i].y+1==route_path[i+1].y+2 and route_path[i].x+1==route_path[i+1].x+1 :
            ser.write("6")
            cv2.waitKey(800)
            East=1
            South=0
            print "hittt"
    if Direction==East:
        if route_path[i].y+1==route_path[i+1].y+2 and route_path[i].x+1==route_path[i+1].x+1 :
            ser.write("8")
            cv2.waitKey(2000)
            print "N"
        if route_path[i].y+1==route_path[i+1].y+1 and route_path[i].x+1==route_path[i+1].x :
            ser.write("4")
            cv2.waitKey(800)
            South=1
            East=0
            print "hi"
        if route_path[i].y+1==route_path[i+1].y+1 and route_path[i].x+1==route_path[i+1].x+2 :
            ser.write("6")
            cv2.waitKey(800)
            North=1
            East=0
            print "hittt"
    if Direction==West:
        if route_path[i].y+1==route_path[i+1].y and route_path[i].x+1==route_path[i+1].x+1 :
            ser.write("8")
            cv2.waitKey(2000)
            print "N"
        if route_path[i].y+1==route_path[i+1].y+1 and route_path[i].x+1==route_path[i+1].x+2 :
            ser.write("4")
            cv2.waitKey(800)
            North=1
            West=0
            print "hi"
        if route_path[i].y+1==route_path[i+1].y+1 and route_path[i].x+1==route_path[i+1].x :
            ser.write("6")
            cv2.waitKey(800)
            South=1
            West=0
            print "hittt"
#ser.write("5")
#print "1"
ser.close()'''
####################################################

if __name__ == "__main__":
    orig_img = cv2.imread('output_image7.jpg')
    hsv = cv2.cvtColor(orig_img,cv2.COLOR_BGR2HSV)
    co_ordinates(hsv)
#################################
    h,k,l=orig_img.shape
    line_widthm=h/(grid_line_x-1)
    line_widthn=k/(grid_line_y-1)
    orig_img = grid_draw(orig_img,grid_line_x,grid_line_y)
    obstacle=obstacle(hsv)
    #draw_obstacle(obstacle)
    cv2.imshow('obstacle',obstacle)
    route_length, route_path= play(orig_img,obstacle,grid_line_x,grid_line_y)
    print route_path
    
    #print grid_line_x,grid_line_y
#################################

    print Bot_position
    print provision
    print bed_demand
    print obstacle_position
    cv2.imshow('bot_position',orig_img)
   # cv2.imwrite('Destination.jpg',orig_img)
## Close and exit
cv2.waitKey(0)
cv2.destroyAllWindows()
############################################
