import numpy
import cv2
#MIN = numpy.array([95, 100, 100],numpy.uint8)  #identifies blue marker
#MAX = numpy.array([130, 255, 255],numpy.uint8)

#MIN = numpy.array([0, 100, 100],numpy.uint8)  #for red marker
#MAX = numpy.array([30, 255, 255],numpy.uint8)

#MIN = numpy.array([40 ,100, 100],numpy.uint8)  #for yellow
#MAX = numpy.array([55, 255, 255],numpy.uint8)

MIN = numpy.array([75 ,100, 100],numpy.uint8)   #wall detection
MAX = numpy.array([95, 255, 255],numpy.uint8)

#MIN = numpy.array([15 ,0, 100],numpy.uint8)  
#MAX = numpy.array([40, 150, 255],numpy.uint8)
vid = cv2.VideoCapture(1)
#vid.set(11,45) #set brightness
ret, img = vid.read()
hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

mask = cv2.inRange(hsv, MIN, MAX)
res = cv2.bitwise_and(img,img, mask= mask)
cv2.imshow('hsv',res)
ret,thresh = cv2.threshold(mask,127,255,1)
cv2.imshow('binary',mask)
#cv2.imwrite(wall.jpg,mask)

contours, h = cv2.findContours(mask,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
contours=sorted(contours, key = cv2.contourArea, reverse = True)[12]
print len(contours)
#cv2.drawContours(res,contours,-1,(0,255,0),2)
  

cv2.imshow('maskcontour',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
