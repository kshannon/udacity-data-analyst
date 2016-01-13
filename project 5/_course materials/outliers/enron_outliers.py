#!/usr/bin/python

import pickle
import sys
import matplotlib.pyplot
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit


### read in data dictionary, convert to numpy array
data_dict = pickle.load( open("../final_project/final_project_dataset.pkl", "r") )
features = ["salary", "bonus"]
data = featureFormat(data_dict, features)


def find_jerkoff(data_dict, data):
	
	largest_salary_bonus = sorted(data, key = lambda x: (x[0],x[1]))[-1]

	name_list = []
	for k,v in data_dict.iteritems():
		#if v["salary"] == 26704229 and v['bonus'] == 97343619:
		#	print k
		if v['salary'] == largest_salary_bonus[0] and v['bonus'] == largest_salary_bonus[1]:

			return k

		


def pop_jerkoff(data_dict, features, data):

	k = find_jerkoff(data_dict, data)

	print len(data_dict)
	data_dict.pop(k,0)
	print len(data_dict)

	return data_dict


pop_jerkoff(data_dict, features, data)


# print sorted(data, key = lambda x: (x[0],x[1]))[-1][0]

# print data_dict["salary"][26704229]
data = sorted(data, key = lambda x: (x[0],x[1]))

data.pop()


for point in data:
    salary = point[0]
    bonus = point[1]
    matplotlib.pyplot.scatter( salary, bonus )

matplotlib.pyplot.xlabel("salary")
matplotlib.pyplot.ylabel("bonus")
matplotlib.pyplot.show()

