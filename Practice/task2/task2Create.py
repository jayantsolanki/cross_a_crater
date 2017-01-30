import cv2
import numpy as np
import random
import os
grid_line_x = 15
grid_line_y = 15
m=0
n=0
def grid_draw(img,m,n): ##filename is image filename with full file path, n is grid of n lines
    h,k,l=img.shape
    print h,k
    line_widthm=h/(m-1)
    line_widthn=k/(n-1) ##calculating width between 2 consecutive parallel lines
    for x in range(0, m): ##drawing lines
        X=x*line_widthm

        cv2.line(img,(0,X),(k,X),(0,0,0), 2)#lines is red color, bgr format
    for y in range(0, n): ##drawing lines
        Y=y*line_widthn

        cv2.line(img,(Y,0),(Y,h),(0,0,0), 2)#lines is red color, bgr format
    return (img)  

####################################Functions#####################################
########################################
###########################################
# calculate contours coordinates
#
#
#
#
def ccoor(contour):
        M = cv2.moments(contour)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        return cx,cy
###########################################
##################################
##########################
# returning grid coordinate from pixels coordinates
#
#
#
#
def getcoor(x,y,m,n):
        '''
        cx=x/n#(int)(round(x/m))
        cy=y/n#(int)(round(y/n))
        return cx,cy
        '''
        #img=cv2.imread(filename) ##getting input image
        X=0
        Y=0
        for i in range(0, grid_line_x): ##
                X=X+m
                Y=0
                for j in range(0, grid_line_y): ##
                        Y=Y+n
                        #print X,Y
                        if x<=X and y<=Y:
                                return i,j
                                break
##########################
# converting grid coordinates into pixels
#
#
#
#
def gridtopixel(x,y,m,n):
        X=x*m+m/2
        Y=y*n+n/2
        return X,Y
#########################################
#######################################
#Draw plus sign
#
#
#
def drawPlus(X,Y,a,b):
	cv2.rectangle(img, (X, Y+b/4), (X, Y-b/4),(0,0,0),4)#plus sign
	cv2.rectangle(img, (X-a/4, Y), (X+a/4, Y),(0,0,0),4)#plus sign
#########################################
#########################################
#######################################
#Draw minus sign
#
#
#
def drawMinus(X,Y,a,b):
	cv2.rectangle(img, (X-a/4, y), (X+a/4, Y),(0,0,0),4)#plus sign
#########################################


#print "grid cell to pixels",gridtopixel(1,1, m,n)
#print "grid cell",getcoor(550,150, m,n)
#cv2.circle(img,(int(550),int(150)),3,(0,255,0),-11)
#cv2.putText(img, str(9), (150-m/4, 150+n/4),cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 4)
i=0
j=0
for im in range(1,11):
	newIm=np.zeros((700,700,3), np.uint8) #blank image of 600x600
	newIm[:,:]=(255,255,255)
	img=grid_draw(newIm,grid_line_x,grid_line_y) ##10,14 perfect for path deduction
	h,k,l=img.shape
	m=h/(grid_line_x-1)
	n=k/(grid_line_y-1)
	for i in range(0,14):
		for j in range(0,14):
			x,y=gridtopixel(j,i, m,n)
			# if j%2==0:
			cv2.putText(img, str(random.randrange(0,2)), (x+2-m/4, y+n/4),cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
			# else:
				# if(random.randrange(0,2)%2==0):
					# drawMinus(x,y,m,n)
				# else:
					# drawPlus(x,y,m,n)

	#cv2.imshow("Grid map",img)
	imgName="task2_img_"+str(im)+".jpg"
	# cv2.imwrite(os.path.join("task2sets",imgName),img)
#generating templates for digits and signs
for dig in range(0,2):
	newDig=np.zeros((m,n,3), np.uint8) #blank image of 600x600
	newDig[:,:]=(255,255,255)
	if(dig<=9):
		cv2.putText(newDig, str(dig), (m/2+2-m/4, n/2+n/4),cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)
		digitName=str(dig)+".jpg"
		# cv2.imwrite(os.path.join("digits",digitName),newDig)
	elif(dig==10):
		digitName="plus.jpg"
		cv2.rectangle(newDig, (m/2, n/4), (m/2, n-n/4),(0,0,0),4)#plus sign
		cv2.rectangle(newDig, (m/4, n/2), (m-m/4, n/2),(0,0,0),4)#plus sign
		# cv2.imwrite(os.path.join("digits",digitName),newDig)
	else:
		digitName="minus.jpg"
		cv2.rectangle(newDig, (m/4, n/2), (m-m/4, n/2),(0,0,0),4)#minus sign
		# cv2.imwrite(os.path.join("digits",digitName),newDig)



cv2.waitKey()