import numpy
import cv2
import heapq
grid_line_x = 24
grid_line_y = 13
# grid_line_x = 24
# grid_line_y = 9
# m=480/(grid_line_x-1)
# n=540/(grid_line_y-1)
grid_map = [ [ 0 for i in range(grid_line_y-1) ] for j in range(grid_line_x-1) ]
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
##############################
#solvegrid
#
#
#
def solve(start,finish,img): #no heuristics used
    """Find the shortest path from START to FINISH."""
    h,k,l=img.shape
    m=h/(grid_line_x-1)
    n=k/(grid_line_y-1)
    heap=[]
    link = {} # parent node link
    g = {} # shortest path to a current node
    
    g[start] = 0 #initial distance to node start is 0
    M=start.x
    N=start.y
    link[start] = None #parent of start node is none
    
    heapq.heappush(heap, (0, start))
    if(len(heap)==0):#added today at 14 sept, 2016
            print 'No path to follow'
            return 0,0
    
    while True:
        if(len(heap)==0):#added today at 14 sept, 2016
            print 'empty heap'
            return 0,0
        f, current = heapq.heappop(heap) ##taking current node from heap
        #print current
        if current == finish:
            name='Shortest Path, image#'
            i=int(100*numpy.random.rand())
            name=name+str(i)
            route=build_path(start, finish, link)
            ####Drawing path , just for pictorial representation######
            for i in range(1,len(route)):
                cv2.line(img,(route[i-1].y*n+(n/2),route[i-1].x*m+(m/2)),(route[i].y*n+(n/2),route[i].x*m+(m/2)),(232,162,0), 3)
            cv2.imshow('name',img)
            ############################
            return g[current], route[1:len(route)]
            
        
        moves = current.get_moves()
        cost = g[current]
        # print cost
        for mv in moves:
            #print mv.x,mv.y
            distance=numpy.sqrt((M-mv.x)*(M-mv.x)+(N-mv.y)*(N-mv.y))
            #print distance
            cost=distance
            if grid_map[mv.x][mv.y]==1: #bypass obstacles
                continue
                #mv is the neighbour of current cell, in all maximum 4 neighbours will be there
            if  (mv not in g or g[mv] >cost): #check if mv is already visited or if its cost is higher than available cost then update it
                g[mv] = cost
                
                link[mv] = current #storing current node as parent to mv 
                heapq.heappush(heap, (g[mv], mv)) ##adding updated cost and visited node to heap
                # cv2.circle(img,(mv.y*n+n/2,mv.x*m+m/2), 5, (255,144,0), -1)

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
        
        
        if self.x>=0 and self.x<grid_line_x-1 and self.y>=0 and self.y<grid_line_y-1:
            if self.x + 1<grid_line_x-1:
                yield GridPoint(self.x + 1, self.y)
            if self.y + 1<grid_line_y-1:  
                yield GridPoint(self.x, self.y + 1)
            if self.x - 1>=-1:
                yield GridPoint(self.x - 1, self.y)
            if self.y - 1>=-1:
                yield GridPoint(self.x, self.y - 1)
                #############################
              
            if self.x + 1<grid_line_x-1 and self.y + 1<grid_line_y-1:
                yield GridPoint(self.x + 1, self.y+1)
            if self.y + 1<grid_line_y-1 and  self.x - 1>-1:  
                yield GridPoint(self.x-1, self.y + 1)    
            if self.x - 1>-1 and self.y - 1>-1:
                yield GridPoint(self.x - 1, self.y-1)
            if self.y - 1>-1 and self.x + 1<grid_line_x-1:
                yield GridPoint(self.x+1, self.y - 1)
             
        

            
                
            
                
            

#############################################################


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
###########################################
##################################
#idetifying markers and returning their array coordinates
#
#
#
#
def markers(img):
        marker = [ [ 0 for i in range(3) ] for j in range(8) ]
        count=0
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        #Starting with red markers
        MIN= numpy.array([0,100,100],numpy.uint8)
        MAX= numpy.array([30,255,255],numpy.uint8)
        mask = cv2.inRange(hsv, MIN,MAX)
        ret,thresh = cv2.threshold(mask,127,255,1)
        Rcontours, h = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        Rcontours=sorted(Rcontours, key = cv2.contourArea, reverse = True)[:5]
        Rcontours,length=areacon(Rcontours,1500,600)
        Rcontours=sorted(Rcontours, key = cv2.contourArea, reverse = True)[:length]
        cv2.drawContours(img,Rcontours,-1,(255,0,0),3)
        #print len(Rcontours)
        
        # blue markers
        MIN= numpy.array([95,100,100],numpy.uint8)
        MAX= numpy.array([130,255,255],numpy.uint8)
        mask = cv2.inRange(hsv, MIN,MAX)
        ret,thresh = cv2.threshold(mask,127,255,1)
        Bcontours, h = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        Bcontours=sorted(Bcontours, key = cv2.contourArea, reverse = True)[:5]
        Bcontours,length=areacon(Bcontours,1500,600)
        Bcontours=sorted(Bcontours, key = cv2.contourArea, reverse = True)[:length]
        
        #print "Blue markers",length
        cv2.drawContours(img,Bcontours,-1,(255,0,0),3)
        #yellow markers
        # blue markers
        MIN= numpy.array([40,100,100],numpy.uint8)
        MAX= numpy.array([60,255,255],numpy.uint8)
        mask = cv2.inRange(hsv, MIN,MAX)
        ret,thresh = cv2.threshold(mask,127,255,1)
        Ycontours, h = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        Ycontours=sorted(Ycontours, key = cv2.contourArea, reverse = True)[:5]
        #cv2.drawContours(img,Ycontours,-1,(255,0,0),3)
        Ycontours,length=areacon(Ycontours,1500,600)
        Ycontours=sorted(Ycontours, key = cv2.contourArea, reverse = True)[:length]
        cv2.drawContours(img,Ycontours,-1,(255,0,0),3)
        cv2.imshow("Rcon",img)
        #####returning coordiantes of marker with maximum demands
        
        if len(Rcontours)>=len(Bcontours):
                if(len(Rcontours)>=len(Ycontours)):
                        ##code here for R
                        count=0
                        for i in range(len(Rcontours)):
                                cx,cy=ccoor(Rcontours[i])
                                #cv2.circle(orig_img,(cx,cy), 5, (255,255,0), -1)
                                if cx < 270:#detecting provision marker
                                        #count=count+1
                                        marker[2][0]=cx
                                        marker[2][1]=cy
                                        marker[2][2]=2
                                
                                else:#detecting demand markers
                                        marker[3+count][0]=cx
                                        marker[3+count][1]=cy
                                        marker[3+count][2]=2 #2 means red demand
                                        count=count+1
                        #code here for yellow
                        for i in range(len(Ycontours)):
                                cx,cy=ccoor(Ycontours[i])
                                #cv2.circle(orig_img,(cx,cy), 5, (255,255,0), -1)
                                if cx < 270:#detecting provision marker
                                        
                                        marker[1][0]=cx
                                        marker[1][1]=cy
                                        marker[1][2]=1
                                
                                else:#detecting demand markers
                                        
                                        marker[3+count][0]=cx
                                        marker[3+count][1]=cy
                                        marker[3+count][2]=1 #1 means yellow demand
                                        count=count+1
                        #code for blue
                        for i in range(len(Bcontours)):
                                cx,cy=ccoor(Bcontours[i])
                                #cv2.circle(orig_img,(cx,cy), 5, (255,255,0), -1)
                                if cx < 270:#detecting provision marker
                                        
                                        marker[0][0]=cx
                                        marker[0][1]=cy
                                        marker[0][2]=0
                                        
                                else:#detecting demand markers
                                        
                                        marker[3+count][0]=cx
                                        marker[3+count][1]=cy
                                        marker[3+count][2]=0 #0 means blue demand
                                        count=count+1

                        
                else:
                        #code here for yellow
                        count=0
                        
                        for i in range(len(Ycontours)):
                                cx,cy=ccoor(Ycontours[i])
                                print cx,cy
                                
                                #cv2.circle(orig_img,(cx,cy), 5, (255,255,0), -1)
                                if cx < 270:#detecting provision marker
                                        
                                        marker[1][0]=cx
                                        marker[1][1]=cy
                                        marker[1][2]=1
                                
                                else:#detecting demand markers
                                        
                                        marker[3+count][0]=cx
                                        marker[3+count][1]=cy
                                        marker[3+count][2]=1 #1 means yellow demand
                                        count=count+1
                        #code for blue
                        for i in range(len(Bcontours)):
                                cx,cy=ccoor(Bcontours[i])
                                #cv2.circle(orig_img,(cx,cy), 5, (255,255,0), -1)
                                if cx < 270:#detecting provision marker
                                        
                                        marker[0][0]=cx
                                        marker[0][1]=cy
                                        marker[0][2]=0
                                        
                                else:#detecting demand markers
                                        
                                        marker[3+count][0]=cx
                                        marker[3+count][1]=cy
                                        marker[3+count][2]=0 #0 means blue demand
                                        count=count+1
                        #code for R
                        for i in range(len(Rcontours)):
                                cx,cy=ccoor(Rcontours[i])
                                #cv2.circle(orig_img,(cx,cy), 5, (255,255,0), -1)
                                if cx < 270:#detecting provision marker
                                        #count=count+1
                                        marker[2][0]=cx
                                        marker[2][1]=cy
                                        marker[2][2]=2
                                
                                else:#detecting demand markers
                                        marker[3+count][0]=cx
                                        marker[3+count][1]=cy
                                        marker[3+count][2]=2 #2 means red demand
                                        count=count+1
                        
        else:
                if(len(Bcontours)>=len(Ycontours)):
                        #code for B
                        count=0
                        for i in range(len(Bcontours)):
                                cx,cy=ccoor(Bcontours[i])
                                #cv2.circle(orig_img,(cx,cy), 5, (255,255,0), -1)
                                if cx < 270:#detecting provision marker
                                        
                                        marker[0][0]=cx
                                        marker[0][1]=cy
                                        marker[0][2]=0
                                        
                                else:#detecting demand markers
                                        
                                        marker[3+count][0]=cx
                                        marker[3+count][1]=cy
                                        marker[3+count][2]=0 #0 means blue demand
                                        count=count+1
                        #code for R
                        for i in range(len(Rcontours)):
                                cx,cy=ccoor(Rcontours[i])
                                #cv2.circle(orig_img,(cx,cy), 5, (255,255,0), -1)
                                if cx < 270:#detecting provision marker
                                        #count=count+1
                                        marker[2][0]=cx
                                        marker[2][1]=cy
                                        marker[2][2]=2
                                
                                else:#detecting demand markers
                                        marker[3+count][0]=cx
                                        marker[3+count][1]=cy
                                        marker[3+count][2]=2 #2 means red demand
                                        count=count+1
                        #code here for yellow
                        
                        for i in range(len(Ycontours)):
                                cx,cy=ccoor(Ycontours[i])
                                #cv2.circle(orig_img,(cx,cy), 5, (255,255,0), -1)
                                if cx < 270:#detecting provision marker
                                        
                                        marker[1][0]=cx
                                        marker[1][1]=cy
                                        marker[1][2]=1
                                
                                else:#detecting demand markers
                                        
                                        marker[3+count][0]=cx
                                        marker[3+count][1]=cy
                                        marker[3+count][2]=1 #1 means yellow demand
                                        count=count+1
                else:
                        #code for Y
                        #code here for yellow
                        count=0
                        for i in range(len(Ycontours)):
                                cx,cy=ccoor(Ycontours[i])
                                #cv2.circle(orig_img,(cx,cy), 5, (255,255,0), -1)
                                if cx < 270:#detecting provision marker
                                        
                                        marker[1][0]=cx
                                        marker[1][1]=cy
                                        marker[1][2]=1
                                
                                else:#detecting demand markers
                                        
                                        marker[3+count][0]=cx
                                        marker[3+count][1]=cy
                                        marker[3+count][2]=1 #1 means yellow demand
                                        count=count+1
                        #code for R
                        for i in range(len(Rcontours)):
                                cx,cy=ccoor(Rcontours[i])
                                #cv2.circle(orig_img,(cx,cy), 5, (255,255,0), -1)
                                if cx < 270:#detecting provision marker
                                        #count=count+1
                                        marker[2][0]=cx
                                        marker[2][1]=cy
                                        marker[2][2]=2
                                
                                else:#detecting demand markers
                                        marker[3+count][0]=cx
                                        marker[3+count][1]=cy
                                        marker[3+count][2]=2 #2 means red demand
                                        count=count+1
                        #code for B
                        
                        for i in range(len(Bcontours)):
                                cx,cy=ccoor(Bcontours[i])
                                #cv2.circle(orig_img,(cx,cy), 5, (255,255,0), -1)
                                if cx < 270:#detecting provision marker
                                        
                                        marker[0][0]=cx
                                        marker[0][1]=cy
                                        marker[0][2]=0
                                        
                                else:#detecting demand markers
                                        
                                        marker[3+count][0]=cx
                                        marker[3+count][1]=cy
                                        marker[3+count][2]=0 #0 means blue demand
                                        count=count+1
        
        
        return marker
###########################################

