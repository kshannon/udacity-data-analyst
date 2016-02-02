#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 1 (Naive Bayes) mini-project. 

    Use a Naive Bayes Classifier to identify emails by their authors
    
    authors and labels:
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess
from sklearn.naive_bayes import GaussianNB


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()


#########################################################
### your code goes here ###
print type(preprocess())
print type(features_train)
print len(features_train)


clf = GaussianNB()

# counting time for fitting model 
t0 = time()
clf.fit(features_train, labels_train)
print "training time:", round(time()-t0, 3), "s"
# training time = 0.921 s

# counting time for prediction
t0 = time()
pred = clf.predict(features_test)
print "predicting time:", round(time()-t0, 3), "s"
# predicting time = 0.185 s

accuracy = clf.score(features_test, labels_test)
print accuracy
# score = .9738


#########################################################

