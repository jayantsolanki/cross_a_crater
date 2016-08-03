# -*- coding: cp1252 -*-
#############################HAPPY HOLIDAYS############################
'''
**************************************************************************
*                  IMAGE PROCESSING (e-Yantra 2014)
*                  ================================
*  This software is intended to teach image processing concepts
*
*  MODULE: Path Planning
*  Filename: task2_code.py
*  Version: 1.0.0  
*  Date: December 25, 2014
*  
*  Author: Jayant Solanki, Uttam Kumar Gupta, Department of Electronics 
*  & Communications, University of Allahabad.
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
import cv2
import heapq
############################################

############################################
## Read the image
grid_map= [ [ 0 for i in range(10) ] for j in range(10) ]
xs=0
ys=0
xe=0
ye=0

img = cv2.imread('test_images/test_image3.png',-1) #showing alpha channel too
############################################
width,height=img.shape[:2]
############################################
## Do the processing

#creating 10x10 matrix space map with black as obstable and other colors as paths.
for x in range(0, 10):
    X=x*40+20
    for y in range(0,10):
        Y=y*40+20
        #print "Pixels ",Y,X," pixel value  b= ",img[Y,X,0]," g= ",img[Y,X,1]," r= ",img[Y,X,2]
        #cv2.circle(img,(Y,X), 5, (0,0,255), -1)
        if img[Y,X,0]==232 and img[Y,X,1]==162 and img[Y,X,2]==0: #start point blue
           
            xs=x+1
            ys=y+1
            #cv2.circle(img,(X,Y), 5, (0,255,0), -1)
        elif img[Y,X,0]==0 and img[Y,X,1]==242 and img[Y,X,2]==255: #end point yellow
            
            xe=x+1
            ye=y+1
            #cv2.circle(img,(X,Y), 5, (0,0,255), -1)
        elif img[Y,X,0]==0 and img[Y,X,1]==0 and img[Y,X,2]==0: #obstacle black
            grid_map[y][x]=1
            #cv2.circle(img,(X,Y), 5, (0,0,255), -1) 
        continue



#####processing for shortest path starts#####
#################
def solve(start, finish, heuristic):
    """Find the shortest path from START to FINISH."""
    heap = []

    link = {} # parent node link
    h = {} # heuristic function 
    g = {} # shortest path to a node

    g[start] = 0
    h[start] = 0
    link[start] = None


    heapq.heappush(heap, (0, start))
    
    while True:
        
        
        f, current = heapq.heappop(heap)
        #print current
        if current == finish:
            route=build_path(start, finish, link)
            print "route_length= ", g[current]
            print "route_path= ",route[1:len(route)]
            #return g[current]
            break
        
        moves = current.get_moves()
        distance = g[current]
        for mv in moves:
            #print mv.x,mv.y
            if grid_map[mv.x][mv.y]==1: #bypass obstacle
                continue
                
            if  (mv not in g or g[mv] > distance + 1):
                g[mv] = distance + 1
                if  mv not in h:
                    h[mv] = heuristic(mv)
                link[mv] = current
                heapq.heappush(heap, (g[mv] + h[mv], mv))
    
    ##Drawing Line
    for i in range(1,len(route)):
        cv2.line(img,(route[i-1].y*40+20,route[i-1].x*40+20),(route[i].y*40+20,route[i].x*40+20),(232,162,0), 3)
    cv2.imshow('image',img)
    

    
def build_path(start, finish, parent):
    """
    Reconstruct the path from start to finish given
    a dict of parent links.

    """
    x = finish
    xs = [x]
    while x != start:
        x = parent[x]
        xs.append(x)
    xs.reverse()
 
    return xs


class GridPoint(object):
    """Represent a position on a grid."""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return "(%d,%d)" % (self.y+1, self.x+1)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def get_moves(self):
        
        
        if self.x>=0 and self.x<=len(grid_map)-1 and self.y>=0 and self.y<=len(grid_map)-1:
            if self.x + 1<len(grid_map):
                yield GridPoint(self.x + 1, self.y)
            if self.y + 1<len(grid_map):  
                yield GridPoint(self.x, self.y + 1)
            if self.x - 1>=-1:
                yield GridPoint(self.x - 1, self.y)
            if self.y - 1>=-1:
                yield GridPoint(self.x, self.y - 1)
                
def no_heuristic(*args):
   """Dummy heuristic"""
   return 0

def grid_test_no_heuristic():
    solve(grid_start, grid_end, no_heuristic)

   
   
grid_start = GridPoint(ys-1,xs-1)
grid_end = GridPoint(ye-1,xe-1)
#print grid_map

grid_test_no_heuristic()


############################################
## Close and exit
cv2.waitKey(0)
cv2.destroyAllWindows()
############################################

