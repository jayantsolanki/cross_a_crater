############################################
## Import OpenCV
import numpy as np
import cv2
def get_perspective_image(frame):
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # lower = np.array([0, 0, 0]) #black color mask
    # upper = np.array([120, 120, 120])
    # lower = np.array([152, 79, 88]) #pink color mask
    # upper = np.array([178, 227, 255])
    MIN1 = np.array([152, 79, 88]) #pink color mask, for bot localisation
    MAX1 = np.array([178, 227, 255])
    MIN2 = np.array([99, 25, 147]) # for blueblack bot localisation
    MAX2 = np.array([143, 191, 255])
    bmask1 = cv2.inRange(hsv, MIN1,MAX1)
    bmask2 = cv2.inRange(hsv, MIN2,MAX2)
    
    #bret,bthresh = cv2.threshold(bmask,127,255,1)
    #cv2.imshow('binary',mask)
    #cv2.imwrite("wall.jpg",mask)

    bcontours1, bh = cv2.findContours(bmask1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    bcontours1=sorted(bcontours1, key = cv2.contourArea, reverse = True)[:12] ##bot
    # bcontours2, bh = cv2.findContours(bmask1,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    # bcontours2=sorted(bcontours2, key = cv2.contourArea, reverse = True)[:12] ##bot
    # print len(bcontours)
    M = cv2.moments(bcontours1[0])
    Cx = int(M['m10']/M['m00'])
    Cy= int(M['m01']/M['m00'])
    cv2.circle(frame,(Cx,Cy), 5, (0,0,255), -1)
    #print cx3,cy3
    M = cv2.moments(bcontours1[1])
    cx = int(M['m10']/M['m00'])
    cy = int(M['m01']/M['m00'])
    cv2.circle(frame,(cx,cy), 5, (0,0,255), -1)
    cv2.drawContours(frame,bcontours1,-1,(0,255,0),3)
    # cv2.drawContours(frame,bcontours2,-1,(0,255,0),3)
    # cv2.imshow('src', frame)

    return frame



cap = cv2.VideoCapture(1)
ret, img_src = cap.read()
cv2.imwrite("output_image.jpg", img_src)
# img_src=get_perspective_image(img_src)
# cv2.imshow('dst', img_src)
# cv2.waitKey(0)
while True:
    ret, src = cap.read()
    src=get_perspective_image(src)
    cv2.imshow('src', src)
    if cv2.waitKey(1) == 27:  ## 27 - ASCII for escape key
        break
#cv2.imwrite("input_image.jpg", src)

##getting the perspective image
#img_src= get_perspective_image(src)
#cv2.waitKey(0)

## Close and exit
cap.release()
cv2.destroyAllWindows()
############################################
