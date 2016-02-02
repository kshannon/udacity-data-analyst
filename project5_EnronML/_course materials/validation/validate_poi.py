#!/usr/bin/python


"""
    Starter code for the validation mini-project.
    The first step toward building your POI identifier!

    Start by loading/formatting the data

    After that, it's not our code anymore--it's yours!
"""

import pickle
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
from sklearn.tree import DecisionTreeClassifier
from sklearn.cross_validation import train_test_split

data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

### first element is our labels, any added elements are predictor
### features. Keep this the same for the mini-project, but you'll
### have a different feature list when you do the final project.
features_list = ["poi", "salary"]

data = featureFormat(data_dict, features_list)
labels, features = targetFeatureSplit(data)


### it's all yours from here forward!  

clf = DecisionTreeClassifier()
clf.fit(features, labels)

pred = clf.predict(features)
score = clf.score(features, labels)
print "accuracy of baseline overfit DT model: ", score


feature_train, feature_test, label_train, label_test = train_test_split(
	features, labels, test_size=0.20, random_state=42)


clf2 = DecisionTreeClassifier()
clf2.fit(feature_train, label_train)

pred = clf2.predict(feature_test)
score = clf2.score(feature_test, label_test)
print "accuracy of corss_validated DT model: ", score

# bell sound when done
print ('\a')


