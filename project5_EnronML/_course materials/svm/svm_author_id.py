#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 2 (SVM) mini-project.

    Use a SVM to identify emails from the Enron corpus by their authors:    
    Sara has label 0
    Chris has label 1
"""
    
import sys
from time import time
sys.path.append("../tools/")
from email_preprocess import preprocess


### features_train and features_test are the features for the training
### and testing datasets, respectively
### labels_train and labels_test are the corresponding item labels
features_train, features_test, labels_train, labels_test = preprocess()


# these allow us to train the data using only 1% of data.
features_train = features_train[:len(features_train)/100] 
labels_train = labels_train[:len(labels_train)/100] 

#########################################################
### your code goes here ###
from sklearn import svm
from sklearn.metrics import accuracy_score

#clf = svm.SVC(kernel='linear')
clf = svm.SVC(kernel='rbf', C=10000)


t0 = time()
clf.fit(features_train, labels_train)
print "training time:", round(time()-t0, 3), "s"


t0 = time()
pred = clf.predict(features_test)
print "predicting time:", round(time()-t0, 3), "s"


print "C at 10000.0: accuracy_score = ", accuracy_score(labels_test, pred)

# getting predictions for specific indexes
answer_10 = pred[10]
answer_26 = pred[26]
answer_50 = pred[50]
print "answer for 10: %s, for 26: %s, for 50: %s" % (answer_10, answer_26, answer_50)

# getting classified count for predicitions
chris = 0
sara = 0
for prediction in pred:
	if prediction == 1:
		chris += 1
	sara += 1
print "number of predictions for chris: %s, sara: %s and total: %s" % (chris, sara, len(pred))

#########################################################

# play hardware bell sound
print('\a')