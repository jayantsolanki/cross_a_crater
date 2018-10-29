# import the necessary packages
import numpy as np
import cv2
ax=0
ay=0
bx=0
by=0
cx=0
cy=0
dx=0
dy=0
jay=0
cap = cv2.VideoCapture(1)
while(True):
    jay=jay+1
    ret, img = cap.read()
    if jay==200:
        break
hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
# lower=np.array([66,207,91])#blue marker 
# upper=np.array([179,255,255])#blue marker
# lower=np.array([0,55,0])#brown marker 
# upper=np.array([20,255,255])#brown marker
# lower=np.array([0,106,66])#brown marker, correct waala 
# upper=np.array([20,255,101])#brown marker
lower = np.array([152, 65, 88]) #pink color mask, 
upper = np.array([178, 227, 255])
# lower = np.array([86, 0, 159]) #light blue color mask,
# upper = np.array([143, 255, 255])
image = cv2.inRange(hsv, lower, upper)

contours,h = cv2.findContours(image,1,2)

for cnt in contours:
    approx = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
    print len(approx)
    # if len(approx)==5:
    #     print "pentagon"
    #     cv2.drawContours(img,[cnt],0,255,-1)
    # elif len(approx)==3:
    #     print "triangle"
    #     cv2.drawContours(img,[cnt],0,(0,255,0),-1)
    # elif len(approx)==4:
    #     print "square"
    #     cv2.drawContours(img,[cnt],0,(0,0,255),-1)
    # elif len(approx) == 9:
    #     print "half-circle"
    #     cv2.drawContours(img,[cnt],0,(255,255,0),-1)
    if len(approx) > 15:
        print "circle"
        cv2.drawContours(img,[cnt],0,(0,255,255),-1)
        M = cv2.moments(cnt)
        B1x = int(M['m10']/M['m00'])
        B1y = int(M['m01']/M['m00'])

cv2.imshow('img',img)
cv2.imshow('image',image)
cv2.waitKey(0)
cv2.destroyAllWindows()