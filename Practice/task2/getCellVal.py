import cv2
import numpy as np
from matplotlib import pyplot as plt##optional
from imglib import *#optional
from motion import *#optional
# comment here
def detectCellVal(img_gray,grid_map):
	for i in range(0,2):
	  # print i
	  imgname='digits/'+str(i)+'.jpg'
	  template = cv2.imread(imgname)
	  temp_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
	  w, h = temp_gray.shape[::-1]
	  # print w,h
	  res = cv2.matchTemplate(img_gray,temp_gray,cv2.TM_CCOEFF_NORMED)
	  threshold = 0.400#change this to match
	  # if i==1:
	    # threshold=0.3500
	  loc = np.where( res >= threshold)
	  for pt in zip(*loc[::-1]):
	    # print pt
	    x,y=getcoor(pt[0]+w/2,pt[1]+h/2,m,n)
	    grid_map[y][x]=i;
	    cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
	  # cv2.imshow('num',img_gray)
	  # cv2.waitKey()
	# plus sign detection
	return grid_map
