#!/usr/bin/python

import sys  #sys.exit()
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

from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sklearn.feature_selection import SelectKBest, f_classif
from sklearn.decomposition import PCA
from sklearn.grid_search import GridSearchCV
from sklearn.pipeline import Pipeline

from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

##################### Task 1: Select what features you'll use. #####################

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
				"from_this_person_to_poi",
				"director_fees",
				"deferred_income",
				"long_term_incentive",
				"from_poi_to_this_person",
				# Engineered Features:
				"from_poi_to_this_person_fraction",
				"from_this_person_to_poi_fraction",
				"poi_email_interaction",
				"poi_email_reciept_interaction",
				"adj_compensation"]

### Load the dictionary containing the dataset
with open("final_project_dataset.pkl", "r") as data_file:
    data_dict = pickle.load(data_file)


##################### Task 2: Remove outliers #####################
# cleaning up outlier mess
outlier_cleaning(data_dict)

##################### Task 3: Create new feature(s) #####################

# Function that adds new features to data_dict
engineered_features(data_dict) #from data_shape.py

# prints out useful info about the data set
data_dict_info(data_dict) #from data_shape.py

# creates a PANDAS df to visualize data
dict_to_dataframe(data_dict) #from data_viz.py

sys.exit()


### Store to my_dataset for easy export below.
my_dataset = data_dict

### Extract features and labels from dataset for local testing
data = featureFormat(my_dataset, features_list, sort_keys = True, remove_NaN = True)
labels, features = targetFeatureSplit(data)



##################### Task 4: Try a varity of classifiers #####################
##################### Task 5: Tune your classifier to achieve better than .3 precision and recall #####################

### Please name your classifier clf for easy export below.
### Note that if you want to do PCA or other multi-stage operations,
### you'll need to use Pipelines. For more info:
### http://scikit-learn.org/stable/modules/pipeline.html

###Because of the small size of the dataset, the script uses
### stratified shuffle split cross validation. For more info: 
### http://scikit-learn.org/stable/modules/generated/sklearn.cross_validation.StratifiedShuffleSplit.html

############ -- Gaussian NB [start] -- ############
gaussianNB_pipeline = Pipeline([	
			#('select', SelectKBest(score_func=f_classif)),
			('select', SelectKBest(k=8)),
			#('scaler', MinMaxScaler()),
			('scaler', StandardScaler()),
			('pca', PCA()),
			#('dt', DecisionTreeClassifier()),
			('gNB', GaussianNB())
			])

#param_dict = {'dt__criterion' : ('entropy', 'gini')}
param_dict = {}

clf = GridSearchCV(gaussianNB_pipeline, param_dict)
############ -- Gaussian NB [end] -- ############


############ -- Decision Tree [start] -- ############

############ -- Decision Tree [end] -- ############



############ -- Linear SVC [start] -- ############

#http://scikit-learn.org/stable/modules/generated/sklearn.svm.LinearSVC.html

############ -- Linear SVC [end] -- ############





# # importances = clf.feature_importances_
# # indices = np.argsort(importances)[::-1]
# # for f in range(clf.n_features_):
# # 	print ("%2d) %-*s %f" % ( f + 1, 30, features_list[f + 1], importances[indices[f]]))



### Task 6: Dump your classifier, dataset, and features_list so anyone can
### check your results. You do not need to change anything below, but make sure
### that the version of poi_id.py that you submit can be run on its own and
### generates the necessary .pkl files for validating your results.


# Commented out pickle pickle to make running easier
dump_classifier_and_data(clf, my_dataset, features_list)

# Bell Sound When Done
#print ('\a')










