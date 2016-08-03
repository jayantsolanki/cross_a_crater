import numpy
import cv2
#MIN = numpy.array([95, 100, 100],numpy.uint8)  #identifies blue marker
#MAX = numpy.array([130, 255, 255],numpy.uint8)

#MIN = numpy.array([0, 100, 100],numpy.uint8)  #for red marker
#MAX = numpy.array([30, 255, 255],numpy.uint8)

MIN = numpy.array([35 ,60, 100],numpy.uint8)  #for yellow
MAX = numpy.array([60, 255, 255],numpy.uint8)

#MIN = numpy.array([75 ,100, 100],numpy.uint8)   #wall detection
#MAX = numpy.array([95, 255, 255],numpy.uint8)

#MIN = numpy.array([75 ,100, 100],numpy.uint8)  
#MAX = numpy.array([95, 255, 255],numpy.uint8)
cap = cv2.VideoCapture(1)
ret, img = cap.read()
#img = cv2.imread('images/input.jpg')
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

mask = cv2.inRange(hsv, MIN, MAX)
res = cv2.bitwise_and(img,img, mask= mask)
cv2.imshow('hsv',res)
ret,thresh = cv2.threshold(mask,127,255,1)
cv2.imshow('binary',mask)
#cv2.imwrite('binary.jpg',mask)
#cv2.imwrite("wall.jpg",mask)

contours, h = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours=sorted(contours, key = cv2.contourArea, reverse = True)[:12]
print len(contours)
x1,y1 = tuple(contours[0][contours[0][:,:,0].argmin()][0])
#print x1,y1
cv2.circle(res,(x1,y1), 5, (0,0,255), -1)
x2,y2 = tuple(contours[9][contours[9][:,:,0].argmax()][0]) #rightmost
x3,y3 = tuple(contours[9][contours[9][:,:,1].argmin()][0]) #topmost
#print topmost

x4,y4 = tuple(contours[1][contours[1][:,:,1].argmax()][0]) #bottommost
cv2.circle(res,(x2,y2), 5, (0,0,255), -1)
cv2.circle(res,(x3,y3), 5, (0,0,255), -1)
cv2.circle(res,(x4,y4), 5, (0,0,255), -1)
cv2.drawContours(res,contours,-1,(0,255,0),2)
  

cv2.imshow('maskcontour',res)
cv2.waitKey(0)
cv2.destroyAllWindows()
