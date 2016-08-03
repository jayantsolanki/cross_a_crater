import numpy
import cv2
import math
#MIN = numpy.array([95, 100, 100],numpy.uint8)  #identifies blue marker
#MAX = numpy.array([130, 255, 255],numpy.uint8)

#MIN = numpy.array([0, 100, 100],numpy.uint8)  #for red marker
#MAX = numpy.array([30, 255, 255],numpy.uint8)

#MIN = numpy.array([40 ,100, 100],numpy.uint8)  #for green
#MAX = numpy.array([55, 255, 255],numpy.uint8)

#MIN = numpy.array([75 ,100, 100],numpy.uint8)   #wall detection
#MAX = numpy.array([95, 255, 255],numpy.uint8)
MIN = numpy.array([65 ,100, 100],numpy.uint8)   ##wall
MAX = numpy.array([95, 255, 255],numpy.uint8)
BMIN = numpy.array([0 ,50, 100],numpy.uint8)    #bot when kept on newspaper sheets
BMAX = numpy.array([30, 150, 255],numpy.uint8)
cap = cv2.VideoCapture(1)
while(1):
        
        ret, img = cap.read()
        hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, MIN,MAX)
        bmask = cv2.inRange(hsv, BMIN,BMAX)
        res = cv2.bitwise_and(img,img, mask= mask)
        #cv2.imshow('hsv',res)
        ret,thresh = cv2.threshold(mask,127,255,1)
        bret,bthresh = cv2.threshold(bmask,127,255,1)
        #cv2.imshow('binary',mask)
        #cv2.imwrite("wall.jpg",mask)

        bcontours, bh = cv2.findContours(bmask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        bcontours=sorted(bcontours, key = cv2.contourArea, reverse = True)[:2] ##bot
        contours, h = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
        contours=sorted(contours, key = cv2.contourArea, reverse = True)[:9] ##obstacles
        
        cv2.drawContours(res,contours,-1,(0,255,0),2)
        cv2.drawContours(res,bcontours,0,(255,255,0),2)
        
        ##drawing centtres of each contours
        M = cv2.moments(contours[1])
        cx1 = int(M['m10']/M['m00'])
        cy1 = int(M['m01']/M['m00'])
        #print "centre of stick = ", cx1, ", ", cy1
        cv2.circle(res,(cx1,cy1), 5, (0,0,255), -1)
        ##
        M = cv2.moments(contours[2])
        cx2 = int(M['m10']/M['m00'])
        cy2 = int(M['m01']/M['m00'])
        #print "center of white ball = ", cx2, ", ", cy2
        cv2.circle(res,(cx2,cy2), 5, (0,0,255), -1)
        ##
        M = cv2.moments(contours[6])
        cx3 = int(M['m10']/M['m00'])
        cy3 = int(M['m01']/M['m00'])
        cv2.circle(res,(cx3,cy3), 5, (0,0,255), -1)

        M = cv2.moments(contours[5])
        cx4 = int(M['m10']/M['m00'])
        cy4 = int(M['m01']/M['m00'])
        cv2.circle(res,(cx4,cy4), 5, (0,0,255), -1)

        M = cv2.moments(bcontours[0])
        cx5 = int(M['m10']/M['m00'])
        cy5 = int(M['m01']/M['m00'])
        cv2.circle(res,(cx5,cy5), 5, (0,0,255), -1)

        #db1=math.sqrt((cx5-cx1)*(cx5-cx1)+(cy5-cy1)*(cy5-cy1))
        cv2.line(res,(cx5,cy5),(cx1,cy1),(255,0,0), 2)
        cv2.line(res,(cx5,cy5),(cx2,cy2),(255,0,0), 2)
        cv2.line(res,(cx5,cy5),(cx3,cy3),(255,0,0), 2)
        cv2.line(res,(cx5,cy5),(cx4,cy4),(255,0,0), 2)
##########################
        cv2.imshow('maskcontour',res)
        cv2.imshow('ori',img)
        if cv2.waitKey(1) == 27:  ## 27 - ASCII for escape key
                break
print len(contours)
cv2.destroyAllWindows()
