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
from clf_validate import validate
from feature_format import featureFormat, targetFeatureSplit
from tester import dump_classifier_and_data
from dummy_transform import DummyTransform
from clf_validate import validate

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


def feature_select(clf, feature, label):
	'''
	Uses a classifier to select best features 
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


old_pipeline = make_pipeline(pca=PCA(), clf=DecisionTreeClassifier(max_depth=10, min_samples_split=10, min_samples_leaf=3))


clf = DecisionTreeClassifier(max_depth=10, min_samples_split=10, min_samples_leaf=3)
select = SelectKBest(f_classif)

new_pipeline = make_pipeline(select=select, pca=PCA(), clf=clf)


def sss_validate(estimator, labels_df, features_df, param_dict, folds=None, random_state = None):
    '''
    Validates a classifier using StratifiedShuffleSplit() 
        
    Metrics include: F1-score, recall, and percision
       
    Args:
        estimator: a SkLearn pipeline
        labels_df: PD_dataframe of labels to predict.
        features_df: PD_dataframe of features used to predict labels.
        folds: Number of rfoldsto perform at cv stage
        
    Returns:
        Prints the evaluation average evaluation metrics for F1
            score, recall, and precission.
    '''


    cv = StratifiedShuffleSplit(labels_df, folds, random_state)
    
    clf = GridSearchCV(estimator, param_dict, cv=cv)
    clf.fit(features_df, labels_df)
    clf.predict(features_df)

    print clf.grid_scores_
    print clf.best_estimator_
    print clf.best_score_
    print clf.best_params_

    # make use of .fit and .predict look into tester.py code and use from there what I need.




param_dict = {'pca__n_components' : [2,4,6]}
#param_dict = {'pca__n_components' : [1,2,3,8,9,10]}
#param_dict = {'dt__max_depth' : [2,3,4,5,6,7,8,9,10,11,12]}
# 			  #'dt__min_samples_split' : [2, 4, 8],
# 			  #'dt__min_samples_leaf' : []}

sss_validate(estimator=new_pipeline, labels_df=labels, features_df=features, param_dict=param_dict, folds=1000, random_state = 42)




sys.exit()

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







