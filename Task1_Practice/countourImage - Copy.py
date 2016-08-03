# -*- coding: cp1252 -*-
'''
**************************************************************************
*                  IMAGE PROCESSING (e-Yantra 2014)
*                  ================================
*  This software is intended to teach image processing concepts
*
*  MODULE: Functions
*  Filename: contourImage.py
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
import numpy
import cv2
############################################

############################################
## Read the image
img = cv2.imread('test_images/10.jpg')
############################################

############################################
## Do the processing
# Need a binary Image
stick = 3
whiteball=2
otherball=4

MIN = numpy.array([70, 100, 100],numpy.uint8)
MAX = numpy.array([85, 255, 255],numpy.uint8)
gray = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
height, width = img.shape[:2]
#ret,thresh = cv2.threshold(gray,50,200,cv2.THRESH_TOZERO) #at 130 lowest contours 22
framet = cv2.inRange(gray, MIN, MAX)
#thresh =cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,25)
#edged=cv2.Canny(thresh,30,960)
contours, hierarchy = cv2.findContours(framet,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours=sorted(contours, key = cv2.contourArea, reverse = True)[:5]
cv2.drawContours(img,contours,2,(0,255,0),1) #1 for stick, 2 for white ball, 3 for other ball

print "No. of contours ",len(contours)
print "image res ",width,"X",height
M = cv2.moments(contours[stick])
cx1 = int(M['m10']/M['m00'])
cy1 = int(M['m01']/M['m00'])
print "centre of stick = ", cx1, ", ", cy1
cv2.circle(img,(cx1,cy1), 5, (0,0,255), -1)
##
M = cv2.moments(contours[whiteball])
cx2 = int(M['m10']/M['m00'])
cy2 = int(M['m01']/M['m00'])
print "center of white ball = ", cx2, ", ", cy2
cv2.circle(img,(cx2,cy2), 5, (0,0,255), -1)
##
M = cv2.moments(contours[otherball])
cx3 = int(M['m10']/M['m00'])
cy3 = int(M['m01']/M['m00'])
print "center of ball = ", cx3, ", ", cy3
cv2.circle(img,(cx3,cy3), 5, (0,0,255), -1)
###calculating slope of white ball's and stick's centroids coordinate system
slope=(float)(cy1-cy2)/(cx2-cx1);
print slope
#drawing line
cy4=-(float)(slope)*(cx3-cx1)+cy1
cy4=round(cy4)
cy4=(int)(cy4)
print cy4
ballwidth=height/7
print "ball width ",ballwidth
cv2.line(img,(cx1,cy1),(cx3,cy4),(255,255,255), 1)
##finding colliding ball
ccx=cx3-30
ccy=-(float)(slope)*(ccx-cx1)+cy1
print ccy
pix=60
count=0
while pix<=height:
    count=count+1
    if ccy>=pix-60 and ccy<pix:
        print "Ball ",count
    pix=pix+60    


#print "Centroid = ", cx, ", ", cy
#cv2.circle(img,(cx,cy), 5, (0,0,255), -1)
############################################

############################################
## Show the image
#cv2.imshow('image-gray',framet)
cv2.imshow('image',img)
#cv2.imshow('image',img)

############################################

############################################
## Close and exit
cv2.waitKey(0)
cv2.destroyAllWindows()
############################################
