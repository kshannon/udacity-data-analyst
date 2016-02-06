#!/usr/bin/python

import sys
import pickle
sys.path.append("../tools/")
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

from data_viz import dict_to_dataframe
from data_shape import engineered_features, outlier_cleaning, data_dict_info
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from dummy_transform import DummyTransform

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.decomposition import PCA
from sklearn.grid_search import GridSearchCV
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.metrics import recall_score, precision_score, f1_score
from sklearn.pipeline import Pipeline

from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn import svm
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier

##################### Task 1: Select what features you'll use. #####################

### 'poi' must be 1st feature in list, comment out features to exclude from classifier
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
				"from_this_person_to_poi",
				"director_fees",
				"deferred_income",
				"long_term_incentive",
				"from_poi_to_this_person",
				#"Engineered Features:"
				"from_poi_to_this_person_fraction",
				"from_this_person_to_poi_fraction",
				"poi_email_interaction",
				"poi_email_reciept_interaction",
				"adj_compensation"]

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


##################### Task 2: Remove outliers #####################

### send data_dict to data_shape.py for cleaning
outlier_cleaning(data_dict)

##################### Task 3: Create new feature(s) #####################

### sends data to data_shape.py to add new features
engineered_features(data_dict)

### prints out useful info about the data set
#data_dict_info(data_dict) 

### creates a PANDAS df to visualize data
#dict_to_dataframe(data_dict)

### store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing

data = featureFormat(my_dataset, features_list, sort_keys = True, remove_NaN = True)
labels, features = targetFeatureSplit(data)

### function that can be used to select features
def feature_select(clf, feature, label):
	'''
	Args:
		1. clf: select a classifier that selects best features.
		2. feature: features from data set.
		3. label: classification labels.

	Function that selects the best features to use and prints all the features 
	with scores and a boolean value if the feature should be used. 
	'''

	features_new = clf.fit(feature, label)
	SKB_scores =  features_new.scores_
	SKB_get_support =  features_new.get_support()


	best_features = []
	for foo in range(0, len(features_list)-1):
		temp_tuple = (features_list[foo + 1], SKB_scores[foo], SKB_get_support[foo])
		best_features.append(temp_tuple)

	sorted_best_features = sorted(best_features, key=lambda tup: tup[1], reverse=True)

	for tup in sorted_best_features:
		print tup

### Use SelectKBest to peek at what the 10 best features are.
#feature_select(SelectKBest(f_classif), features, labels)


##################### Task 4: Try a varity of classifiers #####################

### Several baseline classifiers attempted. DecisionTree was the best.
### baseline classifiers tried: 
### DT out of box
# test_pipeline_dt = Pipeline([	
# 			('select', SelectKBest(k=3)),
# 			('dt', DecisionTreeClassifier()),
# 			])
# clf = test_pipeline_dt



### GussianNB out of box
# test_pipeline_gnb = Pipeline([	
# 			('select', SelectKBest(k=3)),
# 			('gnb', GaussianNB())
# 			])
# clf = test_pipeline_gnb



### AdaBoost out of box
# test_pipeline_adaboost = Pipeline([	
# 			('select', SelectKBest(k=3)),
# 			('adaboost', AdaBoostClassifier())
# 			])
# clf = test_pipeline_adaboost



### Linear SVC out of box
# test_pipeline_Lsvc = Pipeline([	
# 			('select', SelectKBest(k=3)),
# 			('Lsvc', svm.LinearSVC())
# 			])
# clf = test_pipeline_Lsvc



### Random Forest out of box
# test_pipeline_rf = Pipeline([	
# 			('select', SelectKBest(k=3)),
# 			('rf', RandomForestClassifier(n_estimators=10))
# 			])
# clf = test_pipeline_rf


##################### Task 5: Tune your classifier #####################


### constructs a pipeline and can make use of DummyTransform Class,
### to bypass chains in the pipeline, possibly making it easier to test
### different pipeline combinations etc.
def make_pipeline(select=None, scaler=None, pca=None, clf=None):

	'''
	Builds and returns  a pipeline to be passed onto 
	GridSearchCV.
	'''

	dummy = DummyTransform()
	if select == None: select = dummy
	if scaler == None: scaler = dummy
	if pca == None: pca = dummy


	pipeline = Pipeline([	
				('select', select),
				('scaler', scaler),
				('pca', pca),
				('clf', clf)
				])
	return pipeline

### This was the first DT I made when I submitted the Enron Prject, it worked and I
### want to preserve it and pass it to pickle. 
old_pipeline = make_pipeline(pca=PCA(), clf=DecisionTreeClassifier(max_depth=10, min_samples_split=10, min_samples_leaf=3))

### This is the new Decision Tree pipeline I am making to test out an new
### implementation of GridSearchCV using cv=StratifiedShuffeSplit() when passing this 
### pipeline to sss_validate.
clf_dt = DecisionTreeClassifier(max_depth=10, min_samples_split=10, min_samples_leaf=3)
select = SelectKBest(f_classif)

new_pipeline = make_pipeline(select=select, pca=PCA(), clf=clf_dt)

PERF_FORMAT_STRING = "\
\tAccuracy: {:>0.{display_precision}f}\tPrecision: {:>0.{display_precision}f}\t\
Recall: {:>0.{display_precision}f}\tF1: {:>0.{display_precision}f}\tF2: {:>0.{display_precision}f}"
RESULTS_FORMAT_STRING = "\tTotal predictions: {:4d}\tTrue positives: {:4d}\tFalse positives: {:4d}\
\tFalse negatives: {:4d}\tTrue negatives: {:4d}"

### takes my pipeline along with a param dict and runs it through a GridSearch and CV to 
### return the best model and scores along with Recall, Precision and F1
def sss_validate(estimator, labels_df, features_df, param_dict, folds=None, random_state = None):
    '''
    Validates a classifier using StratifiedShuffleSplit() 
        
    Metrics include: F1-score, recall, and percision
       
    Args:
        estimator: a SkLearn pipeline
        labels_df: PD_dataframe of labels to predict.
        features_df: PD_dataframe of features used to predict labels.
        folds: Number of folds to perform at cv stage.
        random_state: random shuffle state to use during shuffle split
    Returns:
        Prints the evaluation average evaluation metrics for F1
            score, recall, and precission.
    '''

    ### inside GridSearchCV() use StratifiedShuffleSplit for CV instead of k3fold
    cv = StratifiedShuffleSplit(labels_df, folds, random_state)
    clf = GridSearchCV(estimator, param_dict, cv=cv)
    
    ### ------ code from UDACITY tester.py file ------ ###
    true_negatives = 0
    false_negatives = 0
    true_positives = 0
    false_positives = 0

    for train_idx, test_idx in cv: 
        features_train = []
        features_test  = []
        labels_train   = []
        labels_test    = []
        for ii in train_idx:
            features_train.append( features_df[ii] )
            labels_train.append( labels_df[ii] )
        for jj in test_idx:
            features_test.append( features_df[jj] )
            labels_test.append( labels_df[jj] )

        print len(train_idx)
        print len(test_idx)

        print "features train", len(features_train)
        print "labels train", len(labels_train)
        print "features test", len(features_test)
        print "labels test", len(labels_test)

        # index error here, not sure why.
        clf.fit(features_train, labels_train)

        sys.exit()

        
        predictions = clf.predict(features_test)
        for prediction, truth in zip(predictions, labels_test):
        	if prediction == 0 and truth == 0:
        		true_negatives += 1
        	elif prediction == 0 and truth == 1:
        		false_negatives += 1
        	elif prediction == 1 and truth == 0:
        		false_positives += 1
        	elif prediction == 1 and truth == 1:
        		true_positives += 1
        	else:
        		print "Warning: Found a predicted label not == 0 or 1."
        		print "All predictions should take value 0 or 1."
        		print "Evaluating performance for processed predictions:"
        		break
    try:
        total_predictions = true_negatives + false_negatives + false_positives + true_positives
        accuracy = 1.0*(true_positives + true_negatives)/total_predictions
        precision = 1.0*true_positives/(true_positives+false_positives)
        recall = 1.0*true_positives/(true_positives+false_negatives)
        f1 = 2.0 * true_positives/(2*true_positives + false_positives+false_negatives)
        f2 = (1+2.0*2.0) * precision*recall/(4*precision + recall)
        print clf
        print PERF_FORMAT_STRING.format(accuracy, precision, recall, f1, f2, display_precision = 5)
        print RESULTS_FORMAT_STRING.format(total_predictions, true_positives, false_positives, false_negatives, true_negatives)
        print ""
    except:
        print "Got a divide by zero when trying out:", clf
        print "Precision or recall may be undefined due to a lack of true positive predicitons."


    ### this will tell me what grids were attempted and what the mean and variance was for
    ### each attmept. Further it will provide mewith the best model.
    ### does it have to be mean and variance? or can I see if it can use reall?
    print clf.grid_scores_
    print clf.best_estimator_
    print clf.best_score_
    print clf.best_params_

    # make use of .fit and .predict look into tester.py code and use from there what I need.


### create a param dict for to go along with pipeline. These will be passed in sss_validate
param_dict = {'pca__n_components' : [2,4,6]}

### validate function to test on new decision tree pipeline.
#sss_validate(estimator=new_pipeline, labels_df=labels, features_df=features, param_dict=param_dict, folds=1000, random_state = 42)


##################### Task 6: Dump your classifier #####################

features_list2 = ["poi", 
				"salary",
				#"to_messages",
				#"deferral_payments",
				"total_payments",
				"exercised_stock_options",
				#"bonus",
				"restricted_stock",
				#"shared_receipt_with_poi",
				#"restricted_stock_deferred",
				#"total_stock_value",
				"expenses",
				#"loan_advances",
				#"from_messages",
				#"from_this_person_to_poi",
				"director_fees",
				"deferred_income",
				#"long_term_incentive",
				#"from_poi_to_this_person",
				# Engineered Features:
				"from_poi_to_this_person_fraction",
				"from_this_person_to_poi_fraction",
				#"poi_email_interaction",
				"poi_email_reciept_interaction"]
				#"adj_compensation"]
clf = old_pipeline

### create pickle files for tester.py
dump_classifier_and_data(clf, my_dataset, features_list2)







