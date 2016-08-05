import cv2
import numpy as np
from matplotlib import pyplot as plt
img = cv2.imread('test2s.jpg')
imgray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(imgray,100,200)
# ret,thresh = cv2.threshold(imgray,127,255,0)
# image, edges, hierarchy = cv2.findContours(edges,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
# img = cv2.drawContours(img, contours, -1, (0,255,0), 3)
plt.subplot(121),plt.imshow(img,cmap = 'gray')
plt.title('Original Image'), plt.xticks([]), plt.yticks([])
plt.subplot(122),plt.imshow(edges,cmap = 'gray')
plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
plt.show()
