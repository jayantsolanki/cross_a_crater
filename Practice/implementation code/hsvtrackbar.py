import cv2
import numpy as np

def nothing(x):
    pass

# Create a black image, a window
cap = cv2.VideoCapture(1)
# img=cv2.imread("output_image.jpg")
# rows,cols,l = img.shape
# M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
# img = cv2.warpAffine(img,M,(cols,rows))
#  hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.namedWindow('image', flags=1)

# create trackbars for color change
cv2.createTrackbar('Mn1','image',0,179,nothing)
cv2.createTrackbar('Mn2','image',0,255,nothing)
cv2.createTrackbar('Mn3','image',0,255,nothing)
cv2.createTrackbar('Mx1','image',0,179,nothing)
cv2.createTrackbar('Mx2','image',0,255,nothing)
cv2.createTrackbar('Mx3','image',0,255,nothing)

# create switch for ON/OFF functionality
switch = '0 : OFF \n1 : ON'
cv2.createTrackbar(switch, 'image',0,1,nothing)

while(1):
    ret, img = cap.read()

    # rotating image
    # rows,cols,l = img.shape
    # M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
    # img = cv2.warpAffine(img,M,(cols,rows))
    hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # hsv=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    k = cv2.waitKey(1) & 0xFF
    if k == 27:
        break

    # get current positions of four trackbars
    Mn1 = cv2.getTrackbarPos('Mn1','image')
    Mn2 = cv2.getTrackbarPos('Mn2','image')
    Mn3 = cv2.getTrackbarPos('Mn3','image')
    Mx1 = cv2.getTrackbarPos('Mx1','image')
    Mx2 = cv2.getTrackbarPos('Mx2','image')
    Mx3 = cv2.getTrackbarPos('Mx3','image')
    s = cv2.getTrackbarPos(switch,'image')

    if s == 0:
        img[:] = img
    else:
        lower=np.array([Mn1,Mn2,Mn3])
        upper=np.array([Mx1,Mx2,Mx3])
        # img=cv2.inRange(hsv,lower,upper)
        # lower = numpy.array([0, 0, 0]) #black color mask
        # upper = numpy.array([120, 120, 120])
        img = cv2.inRange(hsv, lower, upper)
        # img=cv2.bitwise_and(img,img,mask=mask)
    cv2.imshow('images',img)

cv2.destroyAllWindows()