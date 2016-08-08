# Import the modules
import cv2
from sklearn.externals import joblib
from skimage.feature import hog
import numpy as np
################################
###############################
#
#
#
#
def areacon(contours,area,sub):
        count=0
        for i in range(len(contours)):
                ar = cv2.contourArea(contours[i])
                # print ar,area, sub
                if ar>area-sub and ar<area+sub:#detecting provision marker
                        contours[count]=contours[i]
                        print ar,area, sub, count, i
                        count=count+1
                        #print count
        return contours,count        
##############################
# Load the classifier
clf = joblib.load("digits_cls.pkl")

# Read the input image 
im = cv2.imread("clippedtest2s.jpg")

# Convert to grayscale and apply Gaussian filtering
im_gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
im_gray = cv2.GaussianBlur(im_gray, (5, 5), 0)

# Threshold the image
ret, im_th = cv2.threshold(im_gray, 155, 255, cv2.THRESH_BINARY_INV)

# Find contours in the image
ctrs, hier = cv2.findContours(im_th.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

ctrs, count=areacon(ctrs,110,100)
ctrs=ctrs[:count]
#ctrs=sorted(ctrs, key = cv2.contourArea, reverse = False)[:count] ##bot
# print count
# ctrs=sorted(ctrs, key = cv2.contourArea, reverse = True)[:6] ##bot
#print ctrs
#print ctrs
#cv2.drawContours(im, ctrs, -1, (255,100,0), 2)
# Get rectangles contains each contour
rects = [cv2.boundingRect(ctr) for ctr in ctrs]

# # For each rectangular region, calculate HOG features and predict
# #the digit using Linear SVM.
i=0
# print len(rects)
# for rect in rects:
# 	cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 2) 
for rect in rects:
    # Draw the rectangles
    cv2.rectangle(im, (rect[0], rect[1]), (rect[0] + rect[2], rect[1] + rect[3]), (0, 255, 0), 2) 
    # Make the rectangular region around the digit
    leng = int(rect[3] * 1.6)
    pt1 = int(rect[1] + rect[3] // 2 - leng // 2)
    pt2 = int(rect[0] + rect[2] // 2 - leng // 2)
    roi = im_th[pt1:pt1+leng, pt2:pt2+leng]
    # Resize the imagepython 
    roi = cv2.resize(roi, (28, 28), interpolation=cv2.INTER_AREA)
    roi = cv2.dilate(roi, (3, 3))
    # Calculate the HOG features
    roi_hog_fd = hog(roi, orientations=9, pixels_per_cell=(14, 14), cells_per_block=(1, 1), visualise=False)
    nbr = clf.predict(np.array([roi_hog_fd], 'float64'))
    print nbr
    print "Area", cv2.contourArea(ctrs[i])
    cv2.putText(im, str(int(nbr[0])), (rect[0], rect[1]),cv2.FONT_HERSHEY_DUPLEX, 1, (255, 100, 0), 2)
    i=i+1

# print int(nbr[0])
cv2.imshow("Resulting Image with Rectangular ROIs", im)
cv2.imshow("Thresholded", im_th)
cv2.waitKey()