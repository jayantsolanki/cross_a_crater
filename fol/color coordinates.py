
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
# -*- coding: cp1252 -*-
'''
**************************************************************************
*                  IMAGE PROCESSING (e-Yantra 2014)
*                  ================================
*  This software is intended to teach image processing concepts
*
*  MODULE: Functions
*  Filename: objectDetect.py
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

# Initialize camera 

############################################
img = cv2.imread('output_image_new.jpg')
#####################
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
############################################
def red_provision(hsv):
    lower = np.array([0,100,100])
    upper = np.array([30,255,255])

    mask = cv2.inRange(hsv,lower, upper)
    kernel = np.ones((20,20),np.uint8)
    erosion = cv2.erode(mask,kernel,iterations = 1)
    dilation = cv2.dilate(erosion,kernel,iterations = 1)
    
    contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img,contours,-1,(255,0,0),1)
    #print len(contours)
    red = [[0 for x in range(2)] for x in range(len(contours))]
    for i in range(len(contours)):
        #print "Area = ", cv2.contourArea(contours[i])
        #print "Perimeter = ", cv2.arcLength(contours[i],True)
        M = cv2.moments(contours[i])
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        #print "Centroid = ", cx, ", ", cy
        cv2.circle(img,(cx,cy), 5, (255,255,0), -1)
        red[i][0]=cx
        red[i][1]=cy
    #cv2.imshow('red_provision',img)
    return red
#######   
def blue_provision(hsv):
    lower = np.array([80,100,212])
    upper = np.array([110,255,255])

    mask = cv2.inRange(hsv,lower, upper)
    kernel = np.ones((20,20),np.uint8)
    erosion = cv2.erode(mask,kernel,iterations = 1)
    dilation = cv2.dilate(erosion,kernel,iterations = 1)
    
    contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img,contours,-1,(255,0,0),1)
    #print len(contours)
    blue = [[0 for x in range(2)] for x in range(len(contours))]
    for i in range(len(contours)):
        #print "Area = ", cv2.contourArea(contours[i])
        #print "Perimeter = ", cv2.arcLength(contours[i],True)
        M = cv2.moments(contours[i])
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        #print "Centroid = ", cx, ", ", cy
        cv2.circle(img,(cx,cy), 5, (255,0,255), -1)
        blue[i][0]=cx
        blue[i][1]=cy
    #cv2.imshow('blue_provision',img)
    return blue
########
def yellow_provision(hsv):
    lower = np.array([25,100,215])
    upper = np.array([55,255,255])

    mask = cv2.inRange(hsv,lower, upper)
    kernel = np.ones((20,20),np.uint8)
    erosion = cv2.erode(mask,kernel,iterations = 1)
    dilation = cv2.dilate(erosion,kernel,iterations = 1)
    contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    cv2.drawContours(img,contours,-1,(255,0,0),1)
    #print len(contours)
    yellow = [[0 for x in range(2)] for x in range(len(contours))]
    for i in range(len(contours)):
        #print "Area = ", cv2.contourArea(contours[i])
        #print "Perimeter = ", cv2.arcLength(contours[i],True)
        M = cv2.moments(contours[i])
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        #print "Centroid = ", cx, ", ", cy
        cv2.circle(img,(cx,cy), 5, (0,255,255), -1)
        yellow[i][0]=cx
        yellow[i][1]=cy
    #cv2.imshow('yellow_provision',img)
    return yellow
#######           
def bot_position(hsv):
    lower = np.array([30,90,120])
    upper = np.array([50,255,230])

    mask = cv2.inRange(hsv,lower, upper)
    kernel = np.ones((10,10),np.uint8)
    closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    dilation = cv2.dilate(closing,kernel,iterations = 1)
    contours, hierarchy = cv2.findContours(dilation,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours, key = cv2.contourArea, reverse = True)[:2]
    cv2.drawContours(img,contours,0,(255,0,0),1)
    #print len(contours)
    bot = [0,0]
    
    M = cv2.moments(contours[0])
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    #print "Centroid = ", cx, ", ", cy
    cv2.circle(img,(cx,cy), 5, (0,0,255), -1)
    bot[0]=cx
    bot[1]=cy
    cv2.imshow('bot_position',img)
    cv2.imwrite('Destination.jpg',img)
    return bot
#cv2.imshow('image',img)

    
############################################
red_provision_coordinate = red_provision(hsv)
print  red_provision_coordinate
blue_provision_coordinate = blue_provision(hsv)
print  blue_provision_coordinate
yellow_provision_coordinate = yellow_provision(hsv)
print  yellow_provision_coordinate
bot_position_coordinate = bot_position(hsv)
print  bot_position_coordinate
############################################
## Close and exit
cv2.waitKey(0)
cv2.destroyAllWindows()
#################################################
