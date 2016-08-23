"""
================================
Digits Classification Exercise
================================

A tutorial exercise regarding the use of classification techniques on
the Digits dataset.

This exercise is used in the :ref:`clf_tut` part of the
:ref:`supervised_learning_tut` section of the
:ref:`stat_learn_tut_index`.
"""
print(__doc__)

from sklearn import datasets, neighbors, linear_model
import cv2
import numpy as np

digits = datasets.load_digits()
X_digits = digits.data
y_digits = digits.target
img4=cv2.imread('2.jpg')
img4=(255-img4)
gray4 = cv2.cvtColor(img4,cv2.COLOR_BGR2GRAY)
cellsz= [np.hsplit(row,1) for row in np.vsplit(gray4,1)]
z = np.array(X_digits)
# test = z[0,0].reshape(-1,400).astype(np.dtype(np.double)) # Size = (2500,7)

# cv2.imshow('res',z[:,:])
n_samples = len(X_digits)

X_train = X_digits[:.9 * n_samples]
y_train = y_digits[:.9 * n_samples]
X_test = X_digits[.9 * n_samples:]
y_test = y_digits[.9 * n_samples:]
print X_train.shape
print y_train.shape
print X_test.shape
print y_test.shape
knn = neighbors.KNeighborsClassifier()
logistic = linear_model.LogisticRegression()

print('KNN score: %f' % knn.fit(X_train, y_train).score(X_test, y_test))
# print('LogisticRegression score: %f'
#       % logistic.fit(X_train, y_train).score(X_test, y_test))
cv2.waitKey()