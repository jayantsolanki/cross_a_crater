import numpy
import cv2
import serial
import math
from time import sleep
grid_line_x = 9
grid_line_y = 8

####################################Functions#####################################
########################################
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
##############################################
##################
# grid draw
#
#
#
def grid_draw(image,m,n): ##filename is image filename with full file path, n is grid of n lines
    h,k,l=image.shape
    #print h,k
    line_widthm=h/(m-1)
    line_widthn=k/(n-1) ##calculating width between 2 consecutive parallel lines
    for x in range(0, m): ##drawing lines
        X=x*line_widthm

        cv2.line(image,(0,X),(k,X),(0,0,255), 2)#lines is red color, bgr format
    for y in range(0, n): ##drawing lines
        Y=y*line_widthn

        cv2.line(image,(Y,0),(Y,h),(255,0,0), 2)#lines is red color, bgr format
    return (image)

##########################
# returning grid coordinate from pixels coordinates
#
#
#
#
def getcoor(x,y,m,n):
        '''
        cx=x/n#(int)(round(x/m))
        cy=y/n#(int)(round(y/n))
        return cx,cy
        '''
        #img=cv2.imread(filename) ##getting input image
        X=0
        Y=0
        for i in range(0, grid_line_x): ##
                X=X+m
                Y=0
                for j in range(0, grid_line_y): ##
                        Y=Y+n
                        #print X,Y
                        if x<=X and y<=Y:
                                return i,j
                                break
##########################
# converting grid coordinates into pixels
#
#
#
#
def gridtopixel(x,y,m,n):
        X=x*m+m/2
        Y=y*n+n/2
        return X,Y
#############################################################End of Functions########################################
## Read the image
oriImg = cv2.imread('clippedtest2s.jpg')
img2=grid_draw(oriImg,grid_line_x,grid_line_y)
h,k,l=oriImg.shape
m=h/(grid_line_x-1)
n=k/(grid_line_y-1)
print h,k
print "m=",m," n=",n

print "grid cell",getcoor(37,166, m,n)
print "grid cell to pixels",gridtopixel(1,4, m,n)
cv2.circle(oriImg,(int(166),int(37)),3,(0,255,0),-11)
cv2.imshow('clippedImage',img2)
## Close and exit
cv2.waitKey(0)
cv2.destroyAllWindows()
