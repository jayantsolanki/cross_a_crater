# -*- coding: cp1252 -*-
'''
**************************************************************************
*                  IMAGE PROCESSING (e-Yantra 2014)
*                  ================================
*  This software is intended to teach image processing concepts
*
*  MODULE: Fundamentals
*  Filename: camImage.py
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
from time import sleep
#from time import sleep
# Initialize camera
#sleep(5)
cap = cv2.VideoCapture(1)
#cap.set(3,1280)
#cap.set(4,1024)
#sleep(2)
#cap.set(11,50) #set brightness

############################################

############################################
## Read the image

ret, frame = cap.read()
############################################

############################################
## Do the processing

# Nothing

############################################

############################################
## Show the image
cv2.imshow('window',frame)
#cv2.imwrite("test1.jpg",frame)
############################################

############################################
## Close and exit
# close camera
#cv2.WaitKey(10)
cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()
############################################
