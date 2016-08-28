import numpy as np
import cv2
from decimal import *
from matplotlib import pyplot as plt
from sklearn.svm import SVC
from sklearn import cross_validation
from sklearn import datasets, neighbors, linear_model
from sklearn.preprocessing import MinMaxScaler, Normalizer
from sklearn.decomposition import PCA as sklearnPCA, KernelPCA
from sklearn.preprocessing import scale
from sklearn.neighbors import KNeighborsRegressor
# sample=np.zeros((5000,7),dtype=np.dtype(Decimal)) #matrix of 5000x7 , 5000 are digits samples, 7 is humoments for each digits
sample=np.zeros((50,100,28),dtype=np.dtype(np.float64)) #matrix of 5000x7 , 5000 are digits samples, 7 is humoments for each digits
# print sampleTest.shape
# sample=np.reshape(sample,(5000,7))
# print sample.shape
def calHuMoments(src):
	# img = cv2.imread(src)
	# # Convert to grayscale and apply Gaussian filtering
	# hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
	# hsv = cv2.GaussianBlur(hsv, (5, 5), 0)
	# # Threshold the image
	# MIN= np.array([0,0,0],np.uint8)
	# MAX= np.array([355,55,100],np.uint8)
	# mask = cv2.inRange(hsv, MIN,MAX)
	# ret,im_th = cv2.threshold(mask,150,255,cv2.THRESH_BINARY_INV)

	# Find contours in the image
	# ctrs, hier = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	#cv2.drawContours(img, ctrs,35, (255,100,0), 2)
	# print len(ctrs)
	#OPTIMAL 140X140, GAUSSIAN 5,5 AND BLUR, 120,100
	moments=np.zeros((4,7),dtype=np.dtype(np.dtype(Decimal)))
	src = cv2.resize(src, (40, 40))
	m,n=src.shape
	src = cv2.GaussianBlur(src, (5, 5), 0)
	# src = cv2.Canny(src,120,100)
	cv2.imshow('res',src)
	seg=0
	# moments=cv2.HuMoments(cv2.moments(src)).flatten()
	for l in range(0,2):
		for k in range(0,2):
			# cv2.imshow('res',src[l*m/4:l*m/4+m/4-1,k*n/4:k*n/4+n/4-1])
			x = cv2.Canny(src[l*m/2:l*m/2+m/2-1,k*n/2:k*n/2+n/2-1],120,100)
			humoments=cv2.HuMoments(cv2.moments(x)).flatten()
			a1=humoments[0]
			a2=humoments[1]
			a3=humoments[2]
			a4=humoments[3]
			a5=humoments[4]
			a6=humoments[5]
			a7=humoments[6]
			# Amin=np.amin(humoments)
			# Amax=np.amax(humoments)
			# # print Amin, Amax
			# a1=(a1-Amin)/(Amax-Amin)
			# a1=a1*(Amax-Amin)+Amin
			# a2=(a2-Amin)/(Amax-Amin)
			# a2=a2*(Amax-Amin)+Amin
			# a3=(a3-Amin)/(Amax-Amin)
			# a3=a3*(Amax-Amin)+Amin
			# a4=(a4-Amin)/(Amax-Amin)
			# a4=a4*(Amax-Amin)+Amin
			# a5=(a5-Amin)/(Amax-Amin)
			# a5=a5*(Amax-Amin)+Amin
			# a6=(a6-Amin)/(Amax-Amin)
			# a6=a6*(Amax-Amin)+Amin
			# a7=(a7-Amin)/(Amax-Amin)
			# a7=a7*(Amax-Amin)+Amin
			# mean=np.mean(humoments)
			# print np.std(humoments)
			# a1=(a1-mean)
			# a11=pow(a1,2)
			# a2=(a2-mean)
			# a22=pow(a2,2)
			# a3=(a3-mean)
			# a33=pow(a3,2)
			# a4=(a4-mean)
			# a44=pow(a4,2)
			# a5=(a5-mean)
			# a55=pow(a5,2)
			# a6=(a6-mean)
			# a66=pow(a6,2)
			# a7=(a7-mean)
			# a77=pow(a7,2)
			# deviation=np.sqrt(a11+a22+a33+a44+a55+a66+a77)
			# print "deviation",deviation
			# a1=(a1/deviation)
			# a2=(a2/deviation)
			# a3=(a3/deviation)
			# a4=(a4/deviation)
			# a5=(a5/deviation)
			# a6=(a6/deviation)
			# a7=(a7/deviation)
			# print a1,a2,a3,a4,a5,a6
			moments[seg]=[a1,a2,a3,a4,a5,a6,a7]
			# moments=scale(moments)
			# moments[seg]=humoments
			seg=seg+1
	moments=moments[:,:].reshape(-1,28).astype(np.dtype(np.float32))
	# Amin=np.amin(moments)
	# Amax=np.amax(moments)
	# for i in range(0,28):
	# 	moments[0][i]=(moments[0][i]-Amin)/(Amax-Amin)
	# 	moments[0][i]=moments[0][i]*(Amax-Amin)+Amin
	# moments=min_max.fit_transform(moments[0])
	# moments=scale(moments[0])
	# sklearn_pca = sklearnPCA(n_components=7)
	# # moments = sklearn_pca.fit_transform(moments)
	Amean=np.mean(moments)
	Astd=np.std(moments)
	# print "mean", Amean
	# print "Astd",Astd
	# print moments.shape
	for i in range(0,28):
		moments[0][i]=(moments[0][i]-Amean)
		moments[0][i]=moments[0][i]/Astd

	# cv2.imshow('ress',src[0:m/4,0:n/4])	
	# cv2.imshow('rs',src)	
	# moments=cv2.HuMoments(cv2.moments(src)).flatten()
	# a1=moments[0]
	# a2=moments[1]
	# a3=moments[2]
	# a4=moments[3]
	# a5=moments[4]
	# a6=moments[5]
	# a7=moments[6]
	# Amin=np.amin(moments)
	# Amax=np.amax(moments)
	# a1=(a1-Amin)/(Amax-Amin)
	# a2=(a2-Amin)/(Amax-Amin)
	# a3=(a3-Amin)/(Amax-Amin)
	# a4=(a4-Amin)/(Amax-Amin)
	# a5=(a5-Amin)/(Amax-Amin)
	# a6=(a6-Amin)/(Amax-Amin)
	# a7=(a7-Amin)/(Amax-Amin)
	# # print "Original hu moments are ",moments
	# mean=(moments[0]+moments[1]+moments[2]+moments[3]+moments[4]+moments[5]+moments[6])/7
	# # print mean
	# a1=(moments[0]-mean)
	# a11=pow(a1,2)
	# a2=(moments[1]-mean)
	# a22=pow(a2,2)
	# a3=(moments[2]-mean)
	# a33=pow(a3,2)
	# a4=(moments[3]-mean)
	# a44=pow(a4,2)
	# a5=(moments[4]-mean)
	# a55=pow(a5,2)
	# a6=(moments[5]-mean)
	# a66=pow(a6,2)
	# a7=(moments[6]-mean)
	# a77=pow(a7,2)
	# deviation=np.sqrt(a11+a22+a33+a44+a55+a66+a77)
	# a1=(a1/deviation)
	# a2=(a2/deviation)
	# a3=(a3/deviation)
	# a4=(a4/deviation)
	# a5=(a5/deviation)
	# a6=(a6/deviation)
	# a7=(a7/deviation)
	# # nom2Moments={a1,a2,a3,a4,a5,a6,a7}
	# # print "Normalised Hu Moments are", nomMoments
	# a1=np.sign(a1)*np.log10(np.abs(a1))
	# a2=np.sign(a2)*np.log10(np.abs(a2))
	# a3=np.sign(a3)*np.log10(np.abs(a3))
	# a4=np.sign(a4)*np.log10(np.abs(a4))
	# a5=np.sign(a5)*np.log10(np.abs(a5))
	# a6=np.sign(a6)*np.log10(np.abs(a6))
	# a7=np.sign(a7)*np.log10(np.abs(a7))
	# D=abs(a1-logHuMoments[0])+abs(a2-logHuMoments[1])+abs(a3-logHuMoments[2])+abs(a4-logHuMoments[3])+abs(a5-logHuMoments[4])+abs(a6-logHuMoments[5])+abs(a7-logHuMoments[6])
	#print  [a1,a2,a3,a4,a5,a6,a7]
	# moments=[a1,a2,a3,a4,a5,a6,a7]
	return moments
	# return moments
# main program
img = cv2.imread('digits.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
# gray = cv2.resize(gray, (4000, 2400))
# gray=(255-gray)
# cv2.imshow("da0",gray)
# Now we split the image to 5000 cells, each 20x20 size
row,col= gray.shape #1000x2000
Dx=20
Dy=20#dimension of each digit
cells = [np.hsplit(row,100) for row in np.vsplit(gray,50)]#1000/50=2000/100=20x20 pixel image
x = np.array(cells)
# print x.shape
# train = x[:,:50].reshape(-1,400).astype(np.float32)
# print x
count=0
min_max=MinMaxScaler()
for i in range(0,50):#getting humoments for all the sample images and storing it in the sample array
	for j in range(0,100):
		# cv2.imshow('ress',x[i,j,:,:])
		sample[i][j]=calHuMoments(x[i,j,:,:])
		count=count+1
	# calHuMoments(x[0,99,:,:],0)
# print sample
# min_max=MinMaxScaler()##feature scaling

train = sample[:,:100].reshape(-1,28).astype(np.dtype(np.float32)) # Size = (3000,7), initializing train
# print train.shape
# # print "Moments ori ",train[0]
# train=min_max.fit_transform(train)
# # print train.shape
# train=scale(train)
# print train.shape

test = sample[:,50:100].reshape(-1,28).astype(np.dtype(np.float32)) # Size = (3000,7)
# test=min_max.fit_transform(test)
# test=scale(test)

# print train[0]
k = np.arange(10)# 10 is for + and 11 is for minus
# k = {0,1,2,3,4,5,6,7,8,9,'+','-'}
# print test[0]
train_labels = np.repeat(k,500)[:,np.newaxis]
test_labels = np.repeat(k,250)[:,np.newaxis]
# Initiate kNN, train the data, then test it with test data for k=1
knn = cv2.KNearest()
#####PCA
train=train.astype(np.float32)
test=test.astype(np.float32)
# sklearn_pca = sklearnPCA(n_components=6)
# sklearn_train = sklearn_pca.fit_transform(train)
# sklearn_test = sklearn_pca.fit_transform(test)
########KPCA
# kpca = KernelPCA(kernel="rbf", fit_inverse_transform=True, gamma=10)
# sklearn_train = kpca.fit_transform(train)
# sklearn_train = kpca.inverse_transform(sklearn_train)
# sklearn_test = kpca.fit_transform(test)
# sklearn_test = kpca.inverse_transform(sklearn_test)
# print sklearn_train[0]
sklearn_train=train
sklearn_test=test
# print sklearn_train[0]
# print train.shape
# print sklearn_train.shape
knn.train(sklearn_train,train_labels)
#test image
# img4=cv2.imread('digits/5.jpg')
# img4 = cv2.resize(img4, (40, 40))
# gray4 = cv2.cvtColor(img4,cv2.COLOR_BGR2GRAY)
# # gray4 = cv2.GaussianBlur(gray4, (5, 5), 0)
# # Threshold the image
# (thresh, gray4) = cv2.threshold(gray4, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
# gray4=(255-gray4)
# # gray4 = cv2.Canny(gray4,200,100)
# # gray4 = cv2.cvtColor(img4,cv2.COLOR_BGR2GRAY)
# # rotating image
# # rows,cols = gray4.shape
# # M = cv2.getRotationMatrix2D((cols/2,rows/2),90,1)
# # gray4 = cv2.warpAffine(gray4,M,(cols,rows))
# #########
# jay=np.zeros((1,1,7),dtype=np.dtype(Decimal))
# jay[0][0]=calHuMoments(gray4)
# print jay
# jay = jay[0,0].reshape(-1,7).astype(np.dtype(np.float32))
# print jay
# print jay.shape
# print test.shape
# test=jay

for k in range(1,6):
	print "k=",k
	ret,result,neighbours,dist = knn.find_nearest(sklearn_test,k=k)
	# print ret,"\n",result,"\n", neighbours,"\n", dist
	# print result, neighbours
	matches = result==test_labels
	correct = np.count_nonzero(matches)
	accuracy = correct*100.0/result.size
	print "Accuracy is", accuracy
# cv2.imshow('ress',gray4)
######################################################3
# using sklearn here
p = np.arange(10)
# p = {0,1,2,3,4,5,6,7,8,9,'+','-'}
train_x = np.repeat(p,500)[:,]
test_y = np.repeat(p,250)[:,]
knn = neighbors.KNeighborsClassifier(n_neighbors=5)
print('KNN score:', knn.fit(sklearn_train, train_x).score(sklearn_test, test_y))
# print 'KNN pred label', knn.predict(sklearn_test[1])
# logistic = linear_model.LogisticRegression()
# print('LogisticRegression score: %f'
#       % logistic.fit(train, train_x).score(test, test_y))
############################
#using SVM
clf = SVC()
p = np.arange(10)
# p = {0,1,2,3,4,5,6,7,8,9,'+','-'}
train_x = np.repeat(p,500)[:,]
test_y = np.repeat(p,250)[:,]
clf.fit(sklearn_train, train_x)
print 'SVM score', clf.score(sklearn_test, test_y)
# print 'SVM pred label', clf.predict(sklearn_test[1])
###########
# neigh = KNeighborsRegressor(n_neighbors=5)
# neigh.fit(sklearn_train, train_x) 
# # KNeighborsRegressor(...)
# print("KNN regression, ",neigh.score(sklearn_test, test_y))
# print neigh.predict(sklearn_test[2499])
# print sklearn_test.shape

#testing
l=x[45,19,:,:]
rows,cols = l.shape
M = cv2.getRotationMatrix2D((cols/2,rows/2),0,1)
l = cv2.warpAffine(l,M,(cols,rows))
cv2.imshow("shw",l)
mom=np.zeros((1,1,28),dtype=np.dtype(np.float64))
mom[0][0]=calHuMoments(l)

sampleCheck = sample[:,:50].reshape(-1,28).astype(np.dtype(np.float64)) # Size = (1,7)
momcheck = mom[0][0].reshape(-1,28).astype(np.dtype(np.float64)) # Size = (1,7)
# print "dsaimension",check.shape
# print "moments sample ",check[0]
# momcheck=min_max1.fit_transform(momcheck)
# sampleCheck=min_max1.fit_transform(sampleCheck)
# # print "momn",momcheck
# # print "original moments, ",sampleCheck
# momcheck=scale(momcheck)
# sampleCheck=scale(sampleCheck)
print "momn",momcheck[0]
# print "original moments, ",sampleCheck[0]
print "original train, ",train[0]
print 'KNN pred label', knn.predict(momcheck[0])
print 'SVM pred label', clf.predict(momcheck[0])
# print "train", train[0]
# jay=jay.astype(np.float32)
# print "min max", jay[0]
# print  train[0]
# sklearn_pca = sklearnPCA(n_components=6)
# check = sklearn_pca.fit_transform(check)
# print check

cv2.waitKey()