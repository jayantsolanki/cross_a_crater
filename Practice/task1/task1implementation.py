import cv2
import numpy as np
def calHuMoments(src, logHuMoments, num):
	img = cv2.imread(src)
	# Convert to grayscale and apply Gaussian filtering
	hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
	# Threshold the image
	MIN= np.array([0,0,0],np.uint8)
	MAX= np.array([355,55,100],np.uint8)
	mask = cv2.inRange(hsv, MIN,MAX)
	# ret,im_th = cv2.threshold(mask,160,255,cv2.THRESH_BINARY_INV)

	# Find contours in the image
	# ctrs, hier = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	#cv2.drawContours(img, ctrs,35, (255,100,0), 2)
	# print len(ctrs)
	moments=cv2.HuMoments(cv2.moments(mask)).flatten()
	# print "Original hu moments are ",moments
	mean=(moments[0]+moments[1]+moments[2]+moments[3]+moments[4]+moments[5]+moments[6])/7
	# print mean
	a1=(moments[0]-mean)
	a11=pow(a1,2)
	a2=(moments[1]-mean)
	a22=pow(a2,2)
	a3=(moments[2]-mean)
	a33=pow(a3,2)
	a4=(moments[3]-mean)
	a44=pow(a4,2)
	a5=(moments[4]-mean)
	a55=pow(a5,2)
	a6=(moments[5]-mean)
	a66=pow(a6,2)
	a7=(moments[6]-mean)
	a77=pow(a7,2)
	deviation=np.sqrt(a11+a22+a33+a44+a55+a66+a77)
	a1=a1/deviation
	a2=a2/deviation
	a3=a3/deviation
	a4=a4/deviation
	a5=a5/deviation
	a6=a6/deviation
	a7=a7/deviation
	# nom2Moments={a1,a2,a3,a4,a5,a6,a7}
	# print "Normalised Hu Moments are", nomMoments
	a1=a1*np.log(abs(a1))/abs(a1)
	a2=a2*np.log(abs(a2))/abs(a2)
	a3=a3*np.log(abs(a3))/abs(a3)
	a4=a4*np.log(abs(a4))/abs(a4)
	a5=a5*np.log(abs(a5))/abs(a5)
	a6=a6*np.log(abs(a6))/abs(a6)
	a7=a7*np.log(abs(a7))/abs(a7)
	D=abs(a1-logHuMoments[0])+abs(a2-logHuMoments[1])+abs(a3-logHuMoments[2])+abs(a4-logHuMoments[3])+abs(a5-logHuMoments[4])+abs(a6-logHuMoments[5])+abs(a7-logHuMoments[6])
	print D

# blue=np.uint8([[[0,0,0]]])
# hsv_blue=cv2.cvtColor(blue, cv2.COLOR_BGR2HSV)
# print hsv_blue
# cv2.imshow('contours',mask)
# cv2.imshow('original',img)
image='digits/4.jpg'
img = cv2.imread(image)
# Convert to grayscale and apply Gaussian filtering
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
# Threshold the image
MIN= np.array([0,0,0],np.uint8)
MAX= np.array([355,55,100],np.uint8)
mask = cv2.inRange(hsv, MIN,MAX)
cv2.imwrite("444.jpg",mask)
# ret,im_th = cv2.threshold(mask,160,255,cv2.THRESH_BINARY_INV)

# Find contours in the image
# ctrs, hier = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#cv2.drawContours(img, ctrs,35, (255,100,0), 2)
# print len(ctrs)
moments=cv2.HuMoments(cv2.moments(mask)).flatten()
# print "Original hu moments are ",moments
mean=(moments[0]+moments[1]+moments[2]+moments[3]+moments[4]+moments[5]+moments[6])/7
# print mean
a1=(moments[0]-mean)
a11=pow(a1,2)
a2=(moments[1]-mean)
a22=pow(a2,2)
a3=(moments[2]-mean)
a33=pow(a3,2)
a4=(moments[3]-mean)
a44=pow(a4,2)
a5=(moments[4]-mean)
a55=pow(a5,2)
a6=(moments[5]-mean)
a66=pow(a6,2)
a7=(moments[6]-mean)
a77=pow(a7,2)
deviation=np.sqrt(a11+a22+a33+a44+a55+a66+a77)
a1=a1/deviation
a2=a2/deviation
a3=a3/deviation
a4=a4/deviation
a5=a5/deviation
a6=a6/deviation
a7=a7/deviation
nomMoments=[a1,a2,a3,a4,a5,a6,a7]
# print "Normalised Hu Moments are", nomMoments
a1=a1*np.log(abs(a1))/abs(a1)
a2=a2*np.log(abs(a2))/abs(a2)
a3=a3*np.log(abs(a3))/abs(a3)
a4=a4*np.log(abs(a4))/abs(a4)
a5=a5*np.log(abs(a5))/abs(a5)
a6=a6*np.log(abs(a6))/abs(a6)
a7=a7*np.log(abs(a7))/abs(a7)
logMoments=[a1,a2,a3,a4,a5,a6,a7]
print "Digit >> 1"
for i in range(0,10):
	image="digits/"+str(i)+".jpg"
	calHuMoments(image,logMoments, i)
cv2.waitKey()