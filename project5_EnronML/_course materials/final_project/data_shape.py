#!/usr/bin/python

def outlier_cleaning(data_dict):
	'''
	Deletes outliers from the data_dict.
	'''

	del data_dict['TOTAL']
	del data_dict['THE TRAVEL AGENCY IN THE PARK']
	del data_dict['LOCKHART EUGENE E']


def engineered_features(data_dict):
	'''
	Creates new features for the Enron data set and inserts
	them into the data_dict.
	'''

	### creating {key : value} for new features and adding them to data set. This is done
	### so that in the next double for loop I am not altering the data_dict that I am
	### iterating over.
	for k,v in data_dict.iteritems():
		v['poi_email_interaction'] = 0
		v['poi_email_reciept_interaction'] = 0
		v['adj_compensation'] = 0
		v['from_poi_to_this_person_fraction'] = 0
		v['from_this_person_to_poi_fraction'] = 0

	### Main two for loops to extract info from data and add to new features values
	for k,v in data_dict.iteritems():
		for key,value in v.iteritems():		
			
			if (key == 'from_this_person_to_poi' or key == 'from_poi_to_this_person') \
				and value != 'NaN':
				v['poi_email_interaction'] += value
			
			if (key == 'from_this_person_to_poi' or key == 'from_poi_to_this_person' \
				or key == 'shared_receipt_with_poi') and value != 'NaN':
				v['poi_email_reciept_interaction'] += value
				#print "recepit interaction add: ", v['poi_email_reciept_interaction']

			if (key == 'shared_receipt_with_poi') and value != 'NaN':
				v['poi_email_reciept_interaction'] = v['poi_email_reciept_interaction'] * value
				#print "recepit interaction multiply: ", v['poi_email_reciept_interaction']

			if (key == 'salary' or key == 'total_payments' or key == 'exercised_stock_options' \
				or key == 'bonus' or key == 'long_term_incentive' or key == 'total_stock_value') \
				and value != 'NaN':
				v['adj_compensation'] += value

			# creating feature for fractional emails from/to POIs
			if key == 'to_messages' and value != 'NaN' and value > 0:
				v['from_poi_to_this_person_fraction'] = int(v['from_poi_to_this_person'])/float(value)

			if key == 'from_messages' and value != 'NaN' and value > 0:
				v['from_this_person_to_poi_fraction'] = int(v['from_this_person_to_poi'])/float(value)

		# print "poi email interacion", v['poi_email_interaction']
		# print "reciept", v['poi_email_reciept_interaction']


def data_dict_info(data_dict):
	'''
	Prints high level information about Enron Financial data set.
	E.g. num of NaNs, \% of NaNs per feature, num of data points etc.
	'''
	### loop through data set's dict and print out information.
	num_NaNs = 0
	num_data_points = 0
	num_poi = 0
	NaN_dict = {}
	for k,v in data_dict.iteritems():
		for key, value in v.iteritems():
			num_data_points += 1
			num_features = len(v)
			if value == 'NaN':
				num_NaNs += 1
			if key == 'poi' and value == 1:
				num_poi += 1
			if key not in NaN_dict:
				NaN_dict[key] = 0
			if key in NaN_dict and value == "NaN":
				NaN_dict[key] += 1

	# print ("Number of People under Investigation: %s,\
	# 		Number of Data Points: %s, Number of Features: %s") % (
	# 			len(data_dict), num_data_points, num_features)
	# print "Percentage of data points as NaNs: %s" % (num_NaNs/float(num_data_points))
	# print "Num of POIs: ", num_poi

	### turn all values in this dict to percentages. The values are the number of NaNs
	### found in the data set for each feature.
	for k,v in NaN_dict.iteritems():
		NaN_dict[k] = "{0:.2f}".format((v/float(143)*100)) + "%"

	#print NaN_dict
