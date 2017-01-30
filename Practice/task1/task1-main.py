# -*- coding: utf-8 -*-
"""
**************************************************************************
*                  IMAGE PROCESSING (e-Yantra 2016)
*                  ================================
*  This software is intended to teach image processing concepts
*
*  MODULE: Task1C
*  Filename: task2-main.py
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
import sys
import cv2
import numpy as np
import pickle
from getCellVal import *
from imglib import *
# To compile the file, on the console type 
# python task1-main.py N
# where N is the total number of images to be read, 7 in your case
# At the end, show the resultant image and print the resultant grid_map in the console.
#=============================================================
#					Task2C begins							 
#User providing the number of images files to be tested

N_images=int(sys.argv[1])
grid_line_x = 7
grid_line_y = 7
m=600/(grid_line_x-1)
n=600/(grid_line_y-1)
# grid_map = [ [ 0 for i in range(grid_line_y-1) ] for j in range(grid_line_x-1) ]
grid_map_result = [ [ [0 for i in range(grid_line_y-1)] for j in range(grid_line_x-1) ] for k in range(7) ]
######################Test case verification######################
############Do not touch this part of the code####################
def testCases(grid_map_result):
	grid_map_solution = pickle.load( open( "grid_map_solution.p", "rb" ) )
	error=0
	for l in range(0, N_images):
		print 'Testing task2_img_',l+1,'.jpg'
		for i in range(0, grid_line_y-1):
			if(grid_map_solution[l][i]==grid_map_result[l][i]):
				print "Row ",i+1,"is correct"
			else:
				print "Row ",i+1,"is wrong"
				error=error+1
	if(error>0):
		print "Test Cases verification completed with ",error,"errors"
	else:
		print "Test Cases verification completed successfully. \n You can upload your submissions now"
######################end of method###############################
###################################################################
for k in range(1,N_images+1):
	grid_map = [ [ 0 for i in range(grid_line_y-1) ] for j in range(grid_line_x-1) ]
	imgpath='task2sets/task2_img_'+str(k)+'.jpg'
	img_rgb = cv2.imread(imgpath)
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
	grid_map=detectCellVal(img_gray,grid_map)
	grid_map_result[k-1]=grid_map
	print grid_map
	# grid_map=solveGrid(grid_map)
	# print "resultant grid ",grid_map
	#drawing on the image
	for i in range(0,6):
	  x,y=gridtopixel(5,i, m,n)
	  if grid_map[i][5]/10!=0:
	    cv2.putText(img_rgb, str(grid_map[i][5]), (x-m/2, y+n/4),cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 4)
	  else:
	    cv2.putText(img_rgb, str(grid_map[i][5]), (x-m/4, y+n/4),cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 255), 4)

	cv2.imshow('task2_img_'+str(k),img_rgb)
	cv2.imwrite('output/task2_img_'+str(k)+'.jpg',img_rgb)
	cv2.waitKey()
print "<--------------Starting Test Cases verification-------------->"
# testCases(grid_map_result)
# pickle.dump( grid_map_solution, open( "grid_map_solution.p", "wb" ) )
#=============================================================
# Your task2C ends here