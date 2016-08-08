import numpy as np
import cv2
img = cv2.imread('test3s.jpg')
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
equ = cv2.equalizeHist(img)
res = np.hstack((img,equ)) #stacking images side-by-side
# create a CLAHE object (Arguments are optional).
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
cl1 = clahe.apply(img)
cv2.imshow('clahe',cl1)
cv2.imshow('histo',res)
cv2.waitKey(0)
cv2.destroyAllWindows()