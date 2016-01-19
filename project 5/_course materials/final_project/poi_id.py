#!/usr/bin/python

import sys  #sys.exit()
import pickle
sys.path.append("../tools/")
import matplotlib.pyplot as plt

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from sklearn.preprocessing import Imputer

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
features_list = ['poi','salary'] # You will need to use more features

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


### Task 2: Remove outliers
for k,v in data_dict.iteritems():
	if k == "THE TRAVEL AGENCY IN THE PARK": continue #print v['poi']
	if k == "TOTAL": continue #print v
# remove TOTAL and THE TRAVEL AGENCY IN THE PARK data as an outlier. 
del data_dict['TOTAL']
del data_dict['THE TRAVEL AGENCY IN THE PARK']

# returning simple info about data set: NaNs features and data points
num_NaNs = 0
num_data_points = 0
for k,v in data_dict.iteritems():
	if k == 'LOCKHART EUGENE E': print v
	for key, value in v.iteritems():
		num_data_points += 1
		num_features = len(v)
		if value == 'NaN':
			num_NaNs += 1

print ("Number of People under Investigation: %s, \
		Number of Data Points: %s, Number of Features: %s") % (
			len(data_dict), num_data_points, num_features)
print "Percentage of data points as NaNs: %s" % (num_NaNs/float(num_data_points))

# Data Imputation using Mediun vs Mean or linear regression for NaN values
# Use SkLearn Data imputate: 
# http://scikit-learn.org/stable/modules/preprocessing.html#imputation-of-missing-values






### Task 3: Create new feature(s)
### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True)
labels, features = targetFeatureSplit(data)

### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.naive_bayes import GaussianNB
clf = GaussianNB()

### Task 5: Tune your classifier to achieve better than .3 precision and recall 
### using our testing script. Check the tester.py script in the final project
### folder for details on the evaluation method, especially the test_classifier
### function. Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

# Example starting point. Try investigating other evaluation techniques!
from sklearn.cross_validation import train_test_split
features_train, features_test, labels_train, labels_test = \
    train_test_split(features, labels, test_size=0.3, random_state=42)

### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.

# Commented out pickle pickle to make running easier
#dump_classifier_and_data(clf, my_dataset, features_list)

# Bell Sound When Done
print ('\a')



# for point in data:
#     salary = point[0]
#     bonus = point[1]
#     matplotlib.pyplot.scatter( salary, bonus )

# matplotlib.pyplot.xlabel("salary")
# matplotlib.pyplot.ylabel("bonus")
# plt.show()




