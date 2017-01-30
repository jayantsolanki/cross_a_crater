import cv2
import numpy as np
from matplotlib import pyplot as plt
from imglib import *
from motion import *
grid_line_x = 7
grid_line_y = 7
m=600/(grid_line_x-1)
n=600/(grid_line_y-1)
grid_map = [ [ 0 for i in range(grid_line_y-1) ] for j in range(grid_line_x-1) ]
img_rgb = cv2.imread('task1sets/task1_img_20.jpg')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
img_Out=img_rgb
#number detections
for i in range(1,10):
  # print i
  imgname='digits/'+str(i)+'.jpg'
  template = cv2.imread(imgname)
  temp_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
  w, h = temp_gray.shape[::-1]
  # print w,h
  res = cv2.matchTemplate(img_gray,temp_gray,cv2.TM_CCOEFF_NORMED)
  threshold = 0.616#change this to match
  if i==1:
    threshold=0.5000
  loc = np.where( res >= threshold)
  for pt in zip(*loc[::-1]):
    # print pt
    x,y=getcoor(pt[0]+w/2,pt[1]+h/2,m,n)
    grid_map[y][x]=i;
    cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
# plus sign detection
imgname='digits/'+'plus'+'.jpg'
template = cv2.imread(imgname)
temp_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
w, h = temp_gray.shape[::-1]
# print w,h
res = cv2.matchTemplate(img_gray,temp_gray,cv2.TM_CCOEFF_NORMED)
threshold = 0.616#change this to match
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
  # print pt
  x,y=getcoor(pt[0]+w/2,pt[1]+h/2,m,n)
  grid_map[y][x]='+';
  cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
# minus sign detection
imgname='digits/'+'minus'+'.jpg'
template = cv2.imread(imgname)
temp_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
w, h = temp_gray.shape[::-1]
# print w,h
res = cv2.matchTemplate(img_gray,temp_gray,cv2.TM_CCOEFF_NORMED)
threshold = 0.5#change this to match
loc = np.where( res >= threshold)
for pt in zip(*loc[::-1]):
  # print pt
  x,y=getcoor(pt[0]+w/2,pt[1]+h/2,m,n)
  grid_map[y][x]='-';
  cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
print 'Original grid', grid_map
# solving the expression
grid_map=solveGrid(grid_map)
print "resultant grid ",grid_map
#drawing on the image
for i in range(0,6):
  x,y=gridtopixel(5,i, m,n)
  if grid_map[i][5]/10!=0:
    cv2.putText(img_Out, str(grid_map[i][5]), (x-m/2, y+n/4),cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 4)
  else:
    cv2.putText(img_Out, str(grid_map[i][5]), (x-m/4, y+n/4),cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 4)
cv2.imshow('output',img_Out)
cv2.waitKey()
# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
  
# img_rgb = cv2.imread('task1sets/task1_img_1.jpg')
# img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
# template = cv2.imread('digits/3.jpg')
# temp_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
# # cv2.imshow('inputtemp',temp_gray)
# w, h = temp_gray.shape[::-1]
# # print w,h
# res = cv2.matchTemplate(img_gray,temp_gray,cv2.TM_CCOEFF_NORMED)
# threshold = 0.5#change this to match
# loc = np.where( res >= threshold)
# print "length is ",len(loc)
# coor=zip(*loc[::-1])
# print coor[0][1]
# cv2.circle(img_rgb,(coor[0][0]+w/2,coor[0][1]+h/2), 5, (0,50,200), -1)
# for pt in zip(*loc[::-1]):
#   # print pt[0], pt[1]
#   cv2.rectangle(img_rgb, (400,400), (pt[0] + w, pt[1] + h), (0,0,255), 2)
#   # break
# cv2.imshow('output',img_rgb)
# cv2.waitKey()