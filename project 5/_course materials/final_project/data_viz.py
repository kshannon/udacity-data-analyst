import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# Making the DataFrame a global variable
DF = None
FEATURE_LIST = [#"poi",
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


#
def dict_to_dataframe(data_dict):
	'''
	takes data in the form of a python dictionary. 
	Returns a Pandas DataFrame.
	'''

	global DF

	DF = pd.DataFrame.from_dict(data_dict, orient='index', dtype=None)

	# Dropping columns of data
	DF.drop('email_address', axis=1, inplace=True)
	
	# replacing NaNs with 0
	# could not get fillna to work, maybe cause NaN was a string?
	#DF.fillna(value=0, inplace=True) 
	DF.replace(to_replace='NaN', value=0, inplace=True) # replace worked for NaN
	
	# function ot print info about data frame
	#print_info()
	
	# function to display heat map.
	#display_corr_matrix()

	display_pairplot()

#
def print_info():
	'''
	Prints useful information about the dataframe.
	'''

	global DF

	#print DF.head() # print first 5 rows
	#print list(DF) # print col names
	#print list(DF.index) # prints row names


def display_corr_matrix():
	'''
	function plots a correlation matrix heat map
	'''
	global DF

	# create a correlation matrix heatmap to look for colinearity
	data = DF
	sns.set(color_codes=True)
	f, ax = plt.subplots(figsize=(9, 9))
	cmap = sns.blend_palette(["#00008B", "#6A5ACD", "#F0F8FF",
	                          "#FFE6F8", "#C71585", "#8B0000"], as_cmap=True)
	sns.corrplot(data, annot=False, sig_stars=False,
	             diag_names=False, cmap=cmap, ax=ax)
	sns.plt.title('Figure 1: Correlation Matrix Heatmap')
	f.tight_layout()
	sns.despine()
	sns.plt.show()


def display_pairplot():
	'''
	'''	

	global DF
	global FEATURE_LIST

	data2 = DF

	pairplot = sns.pairplot(data2[0:50], vars=FEATURE_LIST[0:4], hue="poi", size=0.5)
	sns.plt.title('Figure 2: Pairplot by "poi" hue')
	sns.plt.show()





