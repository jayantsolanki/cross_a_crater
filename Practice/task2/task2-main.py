# -*- coding: utf-8 -*-
"""
**************************************************************************
*                  IMAGE PROCESSING (e-Yantra 2016)
*                  ================================
*  This software is intended to teach image processing concepts
*
*  MODULE: Task2
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
# python task2-main.py N
# where N is the total number of images to be read, 7 in your case
# At the end, show the resultant image and print the resultant grid_map in the console.
#=============================================================
#					Task2C begins							 
#User providing the number of images files to be tested
N_images=int(sys.argv[1])
grid_line_x = 15
grid_line_y = 15
m=700/(grid_line_x-1)
n=700/(grid_line_y-1)
route_length_result=[[0 for i in range(grid_line_y-1)] for j in range(N_images)]
route_path_result=[[]for k in range(N_images)]
grid_map_result = [ [ [0 for i in range(grid_line_y-1)] for j in range(grid_line_x-1) ] for k in range(N_images) ]
######################Test case verification######################
############Do not touch this part of the code####################
def testCases(grid_map_result, route_length_result):
	grid_map_solution = pickle.load( open( "grid_map_solution.p", "rb" ) )
	route_length_solution = pickle.load( open( "route_length_solution.p", "rb" ) )
	# route_path_solution = pickle.load( open( "route_path_solution.p", "rb" ) )
	grid_error=0
	route_length_error=0
	flag=0
	for l in range(0, N_images):
		print 'Testing task2_img_',l+1,'.jpg'
		for i in range(0, grid_line_y-1):
			if(grid_map_solution[l][i]==grid_map_result[l][i]):
				print "Row ",i+1,"is correct"
			else:
				print "Row ",i+1,"is wrong"
				flag=1
				grid_error=grid_error+1
		if(flag==0):
			print "Grid Cells for task2_img_",l+1,".jpg verified successfully, Testing for Route length"
			if(route_length_solution[l]==route_length_result[l]):
				print "Route length for task2_img_",l+1,".jpg is correct"
			else:
				print "Route_length for task2_img_",l+1,".jpg is incorrect"
				route_length_error=route_length_error+1
		else:
			print "Grid cells' values are incorrectly identified, route length will not be verfied unless cells' values are correctly identified"
			flag=0
	print "======================================================================="
	print "Grid Cells verification completed with ",grid_error,"errors"
	print "Route length verification completed with ",route_length_error,"errors"
	if(route_length_error==0 and grid_error==0 and N_images>=7):
		print "Test passed successfully. \n You can upload your submissions now. Good Luck"
######################end of method###############################
for k in range(1,N_images+1):
	grid_map = [ [ 0 for i in range(grid_line_y-1) ] for j in range(grid_line_x-1) ]
	imgpath='task2sets/task2_img_'+str(k)+'.jpg'
	img_rgb = cv2.imread(imgpath)
	img_gray = cv2.cvtColor(img_rgb, cv2.COLOR_BGR2GRAY)
	grid_map=detectCellVal(img_gray,grid_map)
	temp_length=196
	temp_path=[]
	temp_frame=img_rgb
	route_length=0
	route_path=[]
	grid_map_result[k-1]=grid_map
	print grid_map
	for i in range(0,14):#iterate trhugh each and every ones and find the shortest path
		if(grid_map[13][i]==1):
			start=GridPoint(13,i)
			# print "source",13,i
			# print grid_map[13][i]
		else:
			continue
		for j in range(0,14):
			if(grid_map[0][j]==1):
				stop=GridPoint(0,j)
				
				# print "destin",0,j
				# print grid_map[0][j]
				route_length,route_path,frame=solve(start,stop,img_rgb,grid_map)
				route_length=int(len(route_path))
				# print "route path ",route_length
				if(int(route_length)<int(temp_length) and int(route_length)!=0):
					temp_length=int(route_length)
					# print "temp length ",temp_length
					temp_path=route_path
					# temp_frame=frame
			else:
				continue
	# start=GridPoint(13,0)#Source 
	# stop=GridPoint(0,9)#destination 
	# length,route,frame=solve(start,stop,img_rgb,grid_map)
	if(temp_length==196):
		print "No path found"
		route_length_result[k-1]=0
		route_path_result[k-1]=[]
		cv2.imshow('task2_img_'+str(k),temp_frame)
		cv2.imwrite('outputs/task2_img_'+str(k)+'.jpg',temp_frame)
	else:
		route_length_result[k-1]=int(temp_length)-1
		route_path_result[k-1]=temp_path
		print " route length", int(temp_length)-1
		print " route path", temp_path
		for i in range(1,temp_length):
			cv2.line(temp_frame,(temp_path[i-1].y*n+(n/2),temp_path[i-1].x*m+(m/2)),(temp_path[i].y*n+(n/2),temp_path[i].x*m+(m/2)),(255,100,0), 3)
		cv2.imshow('task2_img_'+str(k),temp_frame)
		cv2.imwrite('outputs/task2_img_'+str(k)+'.jpg',temp_frame)
	# grid_map=solveGrid(grid_map)
	# print "resultant grid ",grid_map
	#drawing on the image
	
	cv2.waitKey()#press escape to continue
print "<--------------Starting Test Cases verification-------------->"
testCases(grid_map_result, route_length_result)
# pickle.dump( grid_map_result, open( "grid_map_solution.p", "wb" ) )
# pickle.dump( route_length_result, open( "route_length_solution.p", "wb" ) )
# pickle.dump( route_path_result, open( "route_path_solution.p", "wb" ) )
#=============================================================
# Your task2C ends here