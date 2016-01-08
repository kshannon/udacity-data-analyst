#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 3 (decision tree) mini-project.

    Use a Decision Tree to identify emails from the Enron corpus by author:    
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess
from sklearn import tree
import numpy as np


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()




#########################################################
### your code goes here ###

print "num of features: ", len(features_train[0]) # num of features
print "rows * cols = ", features_train.size # rows * col
print "(rows, cols): ", features_train.shape # returns num of (rows, cols)

clf = tree.DecisionTreeClassifier(min_samples_split=40) # accu = .9789
clf = clf.fit(features_train, labels_train)
pred = clf.predict(features_test)
score = clf.score(features_test, labels_test)
print "accuracy of DT model: ", score

# bell sound when done
print ('\a')
#########################################################


