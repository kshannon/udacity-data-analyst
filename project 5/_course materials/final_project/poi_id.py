#!/usr/bin/python

import sys  #sys.exit()
import pickle
sys.path.append("../tools/")
import matplotlib.pyplot as plt
import numpy as np

from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from sklearn import preprocessing

from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

### Task 1: Select what features you'll use.
### features_list is a list of strings, each of which is a feature name.
### The first feature must be "poi".
### Adding in all features now, will trim later on with PCA etc.
### 143 * 18 = 2574 data points....
features_list = ["poi",
				"salary",
				"to_messages",
				"deferral_payments",
				"total_payments",
				"exercised_stock_options",
				"bonus",
				"restricted_stock",
				"shared_receipt_with_poi",
				"restricted_stock_deferred",
				"total_stock_value",
				"expenses",
				"loan_advances",
				"from_messages",
				#"other",
				"from_this_person_to_poi",
				"director_fees",
				"deferred_income",
				"long_term_incentive",
				"from_poi_to_this_person"]

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


### Task 2: Remove outliers
for k,v in data_dict.iteritems():
	if k == "THE TRAVEL AGENCY IN THE PARK": continue #print v['poi']
	if k == "TOTAL": continue #print v
	if k == 'LOCKHART EUGENE E': continue #print v

### remove TOTAL and THE TRAVEL AGENCY IN THE PARK data as outliers.
### EUGENE had no data, all are NaN except for {'poi':'False'}. Remove him as well.
del data_dict['TOTAL']
del data_dict['THE TRAVEL AGENCY IN THE PARK']
del data_dict['LOCKHART EUGENE E']

### returning simple info about data set: NaNs features and data points
num_NaNs = 0
num_data_points = 0
for k,v in data_dict.iteritems():
	for key, value in v.iteritems():
		#if key == 'poi' and value == True: print "AHHHHH YEAHHHHH"
		num_data_points += 1
		num_features = len(v)
		if value == 'NaN':
			num_NaNs += 1


print ("Number of People under Investigation: %s, \
		Number of Data Points: %s, Number of Features: %s") % (
			len(data_dict), num_data_points, num_features)
print "Percentage of data points as NaNs: %s" % (num_NaNs/float(num_data_points))


### Task 3: Create new feature(s)

### Trying to create 4 new features:

# [1] is_director : making 'director' a boolean. if value is >0 or not NaN then = 1
# [2] poi_email_interaction : combining 'from_poi' with 'to_poi'
# [3] poi_email_reciept_interaction : same as above but adding 'shared_reciept_with_poi'
# [4] adj_compensation: I am combining a bunch of financial features and MinMaxing it to 0-1
#	features include: 'salary', 'total_payments', 'exercised_stock_options', 'bonus', 
#					  'long_term_incentive', 'total_stock_value'.


for k,v in data_dict.iteritems():
	v['is_director'] = 0
	v['poi_email_interaction'] = 0
	v['poi_email_reciept_interaction'] = 0
	v['adj_compensation'] = 0


for k,v in data_dict.iteritems():
	for key,value in v.iteritems():
		if key == 'director_fees' and value != 'NaN' or value > 0: 
			v['is_director'] = 1		
		
		if (key == 'from_this_person_to_poi' or key == 'from_poi_to_this_person') \
			and value != 'NaN':
			v['poi_email_interaction'] += value
		
		if (key == 'from_this_person_to_poi' or key == 'from_poi_to_this_person' \
			or key == 'shared_receipt_with_poi') and value != 'NaN':
			v['poi_email_reciept_interaction'] += value

		if (key == 'salary' or key == 'total_payments' or key == 'exercised_stock_options' \
			or key == 'bonus' or key == 'long_term_incentive' or key == 'total_stock_value') \
			and value != 'NaN':
			v['adj_compensation'] += value



### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True, remove_NaN = True)
labels, features = targetFeatureSplit(data)




### Task 4: Try a varity of classifiers
### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

# Provided to give you a starting point. Try a variety of classifiers.
from sklearn.naive_bayes import GaussianNB
clf2 = GaussianNB()

from sklearn.tree import DecisionTreeClassifier
clf = DecisionTreeClassifier(random_state=0)




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
dump_classifier_and_data(clf, my_dataset, features_list)

# Bell Sound When Done
print ('\a')



# for point in data:
#     salary = point[0]
#     bonus = point[1]
#     matplotlib.pyplot.scatter( salary, bonus )

# matplotlib.pyplot.xlabel("salary")
# matplotlib.pyplot.ylabel("bonus")
# plt.show()




