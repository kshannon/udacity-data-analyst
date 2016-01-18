#!/usr/bin/python


"""
    Starter code for the evaluation mini-project.
    Start by copying your trained/tested POI identifier from
    that which you built in the validation mini-project.

    This is the second step toward building your POI identifier!

    Start by loading/formatting the data...
"""

import pickle
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import precision_score, recall_score, accuracy_score, confusion_matrix

data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

### add more features to features_list!
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)



# DT baseline ... sucked here
clf = DecisionTreeClassifier()
clf.fit(features, labels)
pred = clf.predict(features)
score = clf.score(features, labels)
print "accuracy of baseline overfit DT model: ", score

# split data
feature_train, feature_test, label_train, label_test = train_test_split(
	features, labels, test_size=0.30, random_state=42)

# build, fit, predict on split data
dt = DecisionTreeClassifier()
dt.fit(feature_train, label_train)
pred2 = dt.predict(feature_test)
score2 = dt.score(feature_test, label_test)
print "accuracy of corss_validated DT model: ", score2


# print number of POIs in test batch
poi = 0
people = 0
for num in label_test:
	if num == 1.0: poi += 1
	else: people += 1
print poi
print people

# look for true positives In this case, we define a true positive as a case 
# where both the actual label and the predicted label are 1
# loop or use: sklearn.metrics.accuracy_score( actual, predicted)
match = 0
for pred, actual in zip(pred2, label_test):
    if pred == 1 and actual == 1: match += 1
print 'MATCH.com(ed): ', match

# compute precision from sklearn.metrics

print "precision: ", precision_score(label_test, pred2)
print "recall: ", recall_score(label_test, pred2)

# counting tp, fn, fp, tn
fake_preds = [0, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0, 1] 
fake_true_labels = [0, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 1, 0, 1, 1, 1, 0, 1, 0, 0]

# TN|FP    9|3
# FN|TP    2|6
print"confusion_matrix: ", confusion_matrix(fake_true_labels, fake_preds)
print "precision: ", precision_score(fake_true_labels, fake_preds)
print "recall: ", recall_score(fake_true_labels, fake_preds)

# “My identifier doesn’t have great PRECISION, but it does have good RECALL. 
# That means that, nearly every time a POI shows up in my test set, I am able to 
# identify him or her. The cost of this is that I sometimes get some false positives, 
# where non-POIs get flagged.”

# “My identifier doesn’t have great RECALL, but it does have good PRECISION. 
# That means that whenever a POI gets flagged in my test set, I know with a 
# lot of confidence that it’s very likely to be a real POI and not a false alarm.
# On the other hand, the price I pay for this is that I sometimes miss real POIs, 
# since I’m effectively reluctant to pull the trigger on edge cases.”

# “My identifier has a really great F1-SCORE.
# This is the best of both worlds. Both my false positive and false negative rates 
# are LOW, which means that I can identify POI’s reliably and accurately. If my 
# identifier finds a POI then the person is almost certainly a POI, and if the identifier 
# does not flag someone, then they are almost certainly not a POI.”

# There’s usually a tradeoff between precision and recall--which one do you think is more 
# important in your POI identifier? There’s no right or wrong answer, there are good arguments 
# either way, but you should be able to interpret both metrics and articulate which one you find 
# most important and why. -- Better to pull the trigger on finding innocent people, to further investigate.


	# function to calculate confusion matrix
# def perf_measure(y_actual, y_hat):
#     TP = 0
#     FP = 0
#     TN = 0
#     FN = 0

#     for i in range(len(y_hat)): 
#         if y_actual[i]==y_hat[i]==1:
#            TP += 1
#     for i in range(len(y_hat)): 
#         if y_actual[i]==1 and y_actual!=y_hat[i]:
#            FP += 1
#     for i in range(len(y_hat)): 
#         if y_actual[i]==y_hat[i]==0:
#            TN += 1
#     for i in range(len(y_hat)): 
#         if y_actual[i]==0 and y_actual!=y_hat[i]:
#            FN += 1
# return(TP, FP, TN, FN)


# bell sound when done
print ('\a')

