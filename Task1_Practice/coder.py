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
img = cv2.imread('lion.jpg')
############################################

############################################
## Do the processing
# Need a binary Image
i = 2
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray,127,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(img,contours,i,(0,255,0),3)
print len(contours)
print "Area = ", cv2.contourArea(contours[i])
print "Perimeter = ", cv2.arcLength(contours[i],True)
M = cv2.moments(contours[i])
cx = int(M['m10']/M['m00'])
cy = int(M['m01']/M['m00'])
print "Centroid = ", cx, ", ", cy
cv2.circle(img,(cx,cy), 5, (0,0,255), -1)
############################################

############################################
## Show the image
cv2.imshow('image',img)
############################################

############################################
## Close and exit
cv2.waitKey(0)
cv2.destroyAllWindows()
############################################
