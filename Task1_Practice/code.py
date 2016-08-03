# -*- coding: cp1252 -*-
import numpy as np
import cv2

img = cv2.imread('test_images/1.jpg')

#Teams can add other helper functions which can be \
#added here

def play(img):
    '''
    img-- a single test image as input argument
    ball_number  -- returns the single integer specifying the target that was 
    hit  eg. 1, 5, etc
    '''
    stick = 3
    whiteball=2
    otherball=4

    MIN = np.array([70, 100, 100],np.uint8)
    MAX = np.array([85, 255, 255],np.uint8)

    hsvimg = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    height, width = img.shape[:2]
    framet = cv2.inRange(hsvimg, MIN, MAX)
    contours, hierarchy = cv2.findContours(framet,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours, key = cv2.contourArea, reverse = True)[:5]
#cv2.drawContours(img,contours,2,(0,255,0),1) #1 for stick, 2 for white ball, 3 for other ball

##
    M1 = cv2.moments(contours[stick])
    cx1 = int(M1['m10']/M1['m00'])
    cy1 = int(M1['m01']/M1['m00'])

##
    M2 = cv2.moments(contours[whiteball])
    cx2 = int(M2['m10']/M2['m00'])
    cy2 = int(M2['m01']/M2['m00'])

##
    M3 = cv2.moments(contours[otherball])
    cx3 = int(M3['m10']/M3['m00'])
    cy3 = int(M3['m01']/M3['m00'])

###calculating slope of white ball's and stick's centroids coordinate system
    slope=(float)(cy1-cy2)/(cx2-cx1);

#drawing line
    cy4=-(float)(slope)*(cx3-cx1)+cy1
    cy4=round(cy4)
    cy4=(int)(cy4)

    ballwidth=height/7
    cv2.line(img,(cx1,cy1),(cx3,cy4),(255,255,255), 1)
##finding colliding ball
    ccx=cx3-30
    ccy=-(float)(slope)*(ccx-cx1)+cy1

    pix=60
    count=0
    while pix<=height:
        count=count+1
        if ccy>=pix-60 and ccy<pix:
            ball_number=count
        pix=pix+60   
    return ball_number
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
    print num_list
