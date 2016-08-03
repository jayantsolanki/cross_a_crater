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
img = cv2.imread('test_images/6.jpg')
############################################

############################################
## Do the processing
# Need a binary Image

stick = 2
whiteball=3
otherball=1

height, width = img.shape[:2]
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray,100,200,cv2.THRESH_TOZERO) #at 130 lowest contours 22
#thresh =cv2.adaptiveThreshold(gray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,25)
#edged=cv2.Canny(gray,11,800)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours=sorted(contours, key = cv2.contourArea, reverse = True)[:7]
cv2.drawContours(img,contours,3,(0,255,0),2) #9 for stick part, 14 is white ball
print len(contours)

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
cv2.line(img,(cx3-30,0),(cx3-30,height),(0,255,255), 1)
#cv2.circle(img,(cx3,cy4), 5, (0,0,255), -1)
##
cv2.circle(img,(cx3-30,height-60), 5, (0,0,255), -1)
cv2.circle(img,(cx3-30,height-120), 5, (0,0,255), -1)
cv2.circle(img,(cx3-30,height-180), 5, (0,0,255), -1)
cv2.circle(img,(cx3-30,height-240), 5, (0,0,255), -1)
cv2.circle(img,(cx3-30,height-300), 5, (0,0,255), -1)
cv2.circle(img,(cx3-30,height-360), 5, (0,0,255), -1)
############################################
print "Area of whiteball = ", cv2.contourArea(contours[3])
print "Perimeter of whiteball  = ", cv2.arcLength(contours[3],True)
rw=cv2.arcLength(contours[3],True)/(2*3.14)
print "whiteball radius ",rw
print "Area of otherball = ", cv2.contourArea(contours[1])
print "Perimeter of otherball = ", cv2.arcLength(contours[1],True)
ro=cv2.arcLength(contours[1],True)/(2*3.14)
print "otherball radius ",ro
############################################
## Show the image
#cv2.imshow('image-gray',thresh)
cv2.imshow('image',img)

############################################

############################################
## Close and exit
cv2.waitKey(0)
cv2.destroyAllWindows()
############################################
