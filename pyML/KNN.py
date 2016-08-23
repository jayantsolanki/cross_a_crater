import numpy as np
import cv2
from matplotlib import pyplot as plt

img = cv2.imread('digits.png')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
img4=cv2.imread('2.jpg')
img4=(255-img4)
gray4 = cv2.cvtColor(img4,cv2.COLOR_BGR2GRAY)
# Now we split the image to 5000 cells, each 20x20 size
cells = [np.hsplit(row,100) for row in np.vsplit(gray,50)]
cellsy= [np.hsplit(row,1) for row in np.vsplit(gray[400:420,0:20],1)]
cellsz= [np.hsplit(row,1) for row in np.vsplit(gray4,1)]
# Make it into a Numpy array. It size will be (50,100,20,20)
x = np.array(cells)
y = np.array(cellsy)
z = np.array(cellsz)
print z
cv2.imshow('ress',gray4)
# cv2.imshow('res',gray[400:420,0:20])
# Now we prepare train_data and test_data.
train = x[:,:50].reshape(-1,400).astype(np.float32) # Size = (2500,400)
test = z[0,0].reshape(-1,400).astype(np.float32) # Size = (2500,400)
# print test
# print x
# cv2.imshow("res",np.array(cells[0]))
# cv2.imshow("res",gray[400:420,0:20])
# Create labels for train and test data
k = np.arange(10)
# print k
train_labels = np.repeat(k,250)[:,np.newaxis]
test_labels = [2]
# print test_labels
# Initiate kNN, train the data, then test it with test data for k=1
knn = cv2.KNearest()
knn.train(train,train_labels)
ret,result,neighbours,dist = knn.find_nearest(test,k=5)
print ret,"\n",result,"\n", neighbours,"\n", dist
# Now we check the accuracy of classification
# For that, compare the result with test_labels and check which are wrong
matches = result==test_labels
correct = np.count_nonzero(matches)
accuracy = correct*100.0/result.size
print "Accuracy is", accuracy
np.savez('knn_data.npz',train=train, train_labels=train_labels)
cv2.waitKey();