# -*- coding: cp1252 -*-
'''
**************************************************************************
*                  IMAGE PROCESSING (e-Yantra 2014)
*                  ================================
*  This software is intended to teach image processing concepts
*
*  MODULE: Sensing
*  Filename: code.py
*  Version: 1.0.0  
*  Date: December 7, 2014
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
import numpy as np
import cv2


def play(img): ##play method is defined below. It will be used for identifying ball number shot by striker
    '''
    img-- a single test image as input argument
    ball_number  -- returns the single integer specifying the target that was 
    hit  eg. 1, 5, etc
    '''
    
## setting up the proper hsv-threshold range for the image
    MIN = np.array([70, 100, 100],np.uint8)  ## lower threshold
    MAX = np.array([85, 255, 255],np.uint8)  ## higher threshold
    
    height, width = img.shape[:2]  #finding and storing the dimension of given color image
    
    hsvimg = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) ##converting color image to HSV format
    framet = cv2.inRange(hsvimg, MIN, MAX) ##thresholding the given HSV image
    contours, hierarchy = cv2.findContours(framet,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE) ##identifying contours in the thresholded image
    contours=sorted(contours, key = cv2.contourArea, reverse = True)[:5] ## sorting contours based on their areas and limiting their total numbers to 5
    stick = 3  ##contour index of cue stick
    whiteball=2 ##contour index of whiteball
    otherball=4 ##contour index of ball among those 7 balls.
    #cv2.drawContours(img,contours,2,(0,255,0),1) 

##calculating the centroids of above three contours
    M1 = cv2.moments(contours[stick])  ##calculating the centroid of lower part of the stick
    cx1 = int(M1['m10']/M1['m00'])
    cy1 = int(M1['m01']/M1['m00'])

##
    M2 = cv2.moments(contours[whiteball]) ##calculating the centroid of striker ball
    cx2 = int(M2['m10']/M2['m00'])
    cy2 = int(M2['m01']/M2['m00'])

##
    M3 = cv2.moments(contours[otherball]) ##calculating the centroid the other ball
    cx3 = int(M3['m10']/M3['m00'])
    cy3 = int(M3['m01']/M3['m00'])

###calculating slope of white ball's and stick's centroids coordinate system
    slope=(float)(cy1-cy2)/(cx2-cx1);

#drawing line through cue and striker.
    cy4=-(float)(slope)*(cx3-cx1)+cy1
    cy4=round(cy4)
    cy4=(int)(cy4)

    ballwidth=height/7 ##finding ball diameter
    cv2.line(img,(cx1,cy1),(cx3,cy4),(255,255,255), 1)
##finding colliding ball
    ccx=cx3
    ccy=-(float)(slope)*(ccx-cx1)+cy1 ##finding the intersected y-ordinate.

    pix=ballwidth ##diameter of each 7 balls
    count=0
    while pix<=height:
        count=count+1
        if ccy>=pix-60 and ccy<pix:
            ball_number=count
        pix=pix+60   
    return ball_number ##returning the ball number identified
##End of method

if __name__ == "__main__":
    #checking output for single image
    img = cv2.imread('test_images/1.jpg')
    ball_number = play(img)
    print ball_number, " number ball at target range"
    #checking output for all images
    num_list = []
    for file_number in range(1,11):
        file_name = "test_images/"+str(file_number)+".jpg"
        pic = cv2.imread(file_name)
        ball_number = play(pic)
        num_list.append(ball_number)
    print num_list ##displaying ball number for each input images
    ##End of program
