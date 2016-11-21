# -*- coding: utf-8 -*-
"""
**************************************************************************
*                  IMAGE PROCESSING (e-Yantra 2016)
*                  ================================
*  This software is intended to teach image processing concepts
*
*  MODULE: Task1B
*  Filename: cellDetect.py
*  Version: 1.0.0  
*  Date: October 13, 2016
*  
*  Author: Jayant Solanki, e-Yantra Project, Department of Computer Science
*  and Engineering, Indian Institute of Technology Bombay.
*  
*  Software released under Creative Commons CC BY-NC-SA
*
*  For legal information refer to:
*        http://creativecommons.org/licenses/by-nc-sa/4.0/legalcode 
*     
*
*  This software is made available on an “AS IS WHERE IS BASIS”. 
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using 
*  ICT(NMEICT)
*
**************************************************************************
"""
# Read the demo.jpg.
# Go through the below code, it will write the numeral with and without their signs
# on the gridImage
# At the end, output the resultant image as output.jpg and also save it.
#=============================================================
#					Task1B begins	
import cv2
import numpy as np
# Image size is of 600 by 600 pixels. 
# Total gridlines are 7 veticals and 7 Horizontals
grid_line_x = 7
grid_line_y = 7
m=600/(grid_line_x-1)
n=600/(grid_line_y-1)
grid_map = [ [ 0 for i in range(grid_line_y-1) ] for j in range(grid_line_x-1) ]
##########################
# returning grid coordinate from pixels coordinates
#
#
#
#
def getcoor(x,y,m,n):
        X=0
        Y=0
        for i in range(0, grid_line_x): ##drawing lines
                X=X+m
                Y=0
                for j in range(0, grid_line_y): ##drawing lines
                        Y=Y+n
                        # print X,Y,x,y
                        # print i,j
                        if x<=X and y<=Y:
                            return i,j
                            break
##########################
def detectCellVal(img_gray,grid_map):
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
	    # print i,x,y
	    grid_map[y][x]=i;
	    # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
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
	  # print '+',x,y
	  grid_map[y][x]='+';
	  # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)
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
	  # print '-',x,y
	  grid_map[y][x]='-';
	return grid_map
	  # cv2.rectangle(img_rgb, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)##########################
# returning grid coordinate from pixels coordinates
#
#
#
#
def getcoor(x,y,m,n):
        X=0
        Y=0
        for i in range(0, grid_line_x): ##drawing lines
                X=X+m
                Y=0
                for j in range(0, grid_line_y): ##drawing lines
                        Y=Y+n
                        # print X,Y,x,y
                        # print i,j
                        if x<=X and y<=Y:
                            return i,j
                            break
##########################
# Read Image
img_rgb = cv2.imread('demo.jpg')
img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
grid_map= detectCellVal(img_gray,grid_map)
for i in range(0,6):
	for j in range(0,6):
		print grid_map[i][j],' ',
	print '\n'
# Show the image
cv2.imshow('output',img_rgb)
# Write the image
cv2.waitKey()
#=============================================================
# Your Task1B ends here