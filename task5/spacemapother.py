import cv2
import math
import numpy
def space_map(img):
    grid_map= [ [ 0 for i in range(14) ] for j in range(14) ]# initializing zero filled 10x10 matrix 
    for x in range(0, 14):
        X=x*38+19 
        for y in range(0,14):
            Y=y*34+17
            #img[Y,X] is pixel at the centre of each cell
            if cdis(dis(Y,X,cy1,cx1),dis(Y,X,cy2,cx2),dis(Y,X,cy3,cx3),dis(Y,X,cy4,cx4),dis(Y,X,cy5,cx5),dis(Y,X,cy6,cx6),dis(Y,X,cy7,cx7),dis(Y,X,cy8,cx8),dis(Y,X,cy9,cx9))==1:
           # if img[Y,X,0]!=0 and img[Y,X,1]!=0 and img[Y,X,2]!=0: #detecting obstacle, if pixel color is not white then mark it as obstacle
                grid_map[y][x]=1 #marking obstacles with value 1
                cv2.circle(img,(X,Y), 5, (0,0,255), -1) #obstacles marked red
                #print Y,X
                #dis(Y,X,cy4,cx4)
            else:
                cv2.circle(img,(X,Y), 5, (0,255,255), -1)
            continue
    
    cv2.imshow("spacemap",img)
    return grid_map
def dis(x1,y1,x2,y2):
    dist=math.sqrt((x2-x1)*(x2-x1)+(y2-y1)*(y2-y1))
    dist=int(dist)
    #print dist
    return dist
def cdis(d1,d2,d3,d4,d5,d6,d7,d8,d9): ##distance checking
    if(d1<50 or d2<50 or d3<50 or d4<50 or d5<57 or d6<57 or d7<57 or d8<50 or d9<50):
        return 1
    return 0

################################
MIN = numpy.array([75 ,100, 100],numpy.uint8)  #obstacles
MAX = numpy.array([95, 255, 255],numpy.uint8)
img = cv2.imread('images/input.jpg')
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

mask = cv2.inRange(hsv, MIN, MAX)
res = cv2.bitwise_and(img,img, mask= mask)
#cv2.imshow('hsv',res)
ret,thresh = cv2.threshold(mask,127,255,1)
#cv2.imshow('binary',mask)
#cv2.imwrite('binary.jpg',mask)
#cv2.imwrite("wall.jpg",mask)

contours, h = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours=sorted(contours, key = cv2.contourArea, reverse = True)[:12]
cv2.drawContours(res,contours,-1,(0,255,0),2) #6 to 9 are big walls

##drawing centtres of each contours
M = cv2.moments(contours[6])
cx1 = int(M['m10']/M['m00'])
cy1 = int(M['m01']/M['m00'])
#print "centre of stick = ", cx1, ", ", cy1
cv2.circle(res,(cx1,cy1), 5, (255,255,255), -1) #white
##
M = cv2.moments(contours[7])
cx2 = int(M['m10']/M['m00'])
cy2 = int(M['m01']/M['m00'])
#print "center of white ball = ", cx2, ", ", cy2
cv2.circle(res,(cx2,cy2), 5, (0,0,255), -1) #red
##
M = cv2.moments(contours[8])
cx3 = int(M['m10']/M['m00'])
cy3 = int(M['m01']/M['m00'])

cv2.circle(res,(cx3,cy3), 5, (255,0,0), -1)#blue

M = cv2.moments(contours[9])
cx4 = int(M['m10']/M['m00'])
cy4 = int(M['m01']/M['m00'])
print "wall coor",cy4,cx4
cv2.circle(res,(cx4,cy4), 5, (0,255,255), -1)#yellow
#####beds
M = cv2.moments(contours[0])
cx5 = int(M['m10']/M['m00'])
cy5 = int(M['m01']/M['m00'])

cv2.circle(res,(cx5,cy5), 5, (0,0,255), -1)#red

M = cv2.moments(contours[1])
cx6 = int(M['m10']/M['m00'])
cy6 = int(M['m01']/M['m00'])

cv2.circle(res,(cx6,cy6), 5, (0,0,255), -1)#red


M = cv2.moments(contours[2])
cx7 = int(M['m10']/M['m00'])
cy7 = int(M['m01']/M['m00'])

cv2.circle(res,(cx7,cy7), 5, (0,0,255), -1)#red
##side walls small ones on left
M = cv2.moments(contours[10])
cx8 = int(M['m10']/M['m00'])
cy8 = int(M['m01']/M['m00'])

cv2.circle(res,(cx8,cy8), 5, (0,0,255), -1)#red


M = cv2.moments(contours[11])
cx9 = int(M['m10']/M['m00'])
cy9 = int(M['m01']/M['m00'])

cv2.circle(res,(cx9,cy9), 5, (0,0,255), -1)#red
cv2.imshow('maskcontour',res)
######################################
img=cv2.imread("binary1.jpg")
print space_map(img)
############################################
## Close and exit
cv2.waitKey(0)
cv2.destroyAllWindows()
############################################
