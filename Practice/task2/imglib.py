import numpy
import cv2
import heapq
from motion import *
grid_line_x = 15
grid_line_y = 15
m=700/(grid_line_x-1)
n=700/(grid_line_y-1)
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
count=0

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

##############################
#solvegrid
#
#
#
def solve(start,finish,img,Grid_map): #no heuristics used
    """Find the shortest path from START to FINISH."""
    global grid_map
    global count
    grid_map=Grid_map
    h,k,l=img.shape
    m=h/(grid_line_x-1)
    n=k/(grid_line_y-1)
    heap=[]
    link = {} # parent node link
    g = {} # shortest path to a current node
    count=0
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
            print 'No Path'
            return 0,0
        f, current = heapq.heappop(heap) ##taking current node from heap
        count=count-1
        print count
        # if str(strcurrent[1:2]) == finish and grid_map[int(strcurrent[-2:-1])-1][int(strcurrent[1:2])-1]==1:
        if finish==current:
            finish=current
            # print current[:2]
            name='Shortest Path, image#'
            i=int(100*numpy.random.rand())
            name=name+str(i)
            route=build_path(start, finish, link)
            ####Drawing path , just for pictorial representation######
            for i in range(1,len(route)):
                cv2.line(img,(route[i-1].y*n+(n/2),route[i-1].x*m+(m/2)),(route[i].y*n+(n/2),route[i].x*m+(m/2)),(255,100,0), 3)
            # cv2.imshow('name',img)
            # cv2.imwrite('output.jpg',img)
            ############################
            return g[current], route[1:len(route)],img
            
        
        moves = current.get_moves()
        cost = g[current]
        # print cost
        for mv in moves:
            #print mv.x,mv.y
            distance=numpy.sqrt((M-mv.x)*(M-mv.x)+(N-mv.y)*(N-mv.y))
            #print distance
            cost=distance
            if grid_map[mv.x][mv.y]==0: #bypass obstacles
                continue
                #mv is the neighbour of current cell, in all maximum 4 neighbours will be there
            if  (mv not in g or g[mv] >cost): #check if mv is already visited or if its cost is higher than available cost then update it
                g[mv] = cost
                
                link[mv] = current #storing current node as parent to mv 
                heapq.heappush(heap, (g[mv], mv)) ##adding updated cost and visited node to heap
                # count=count+1
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
        
        global count
        if self.x>=0 and self.x<=len(grid_map)-1 and self.y>=0 and self.y<=len(grid_map)-1:
            if self.x + 1<len(grid_map):
                count=count-1
                yield GridPoint(self.x + 1, self.y)
            if self.y + 1<len(grid_map):  
                yield GridPoint(self.x, self.y + 1)
            if self.x - 1>=-1:
                count=count+1
                yield GridPoint(self.x - 1, self.y)
            if self.y - 1>=-1:
                yield GridPoint(self.x, self.y - 1)
                #############################
              
            if self.x + 1<len(grid_map) and self.y + 1<len(grid_map):
                count=count-1
                yield GridPoint(self.x + 1, self.y+1)
            if self.y + 1<len(grid_map) and  self.x - 1>-1:  
                count=count+1
                yield GridPoint(self.x-1, self.y + 1)    
            if self.x - 1>-1 and self.y - 1>-1:
                count=count+1
                yield GridPoint(self.x - 1, self.y-1)
            if self.y - 1>-1 and self.x + 1<len(grid_map):
                count=count-1
                yield GridPoint(self.x+1, self.y - 1)
             
        

            
                
            
                
            

#############################################################
