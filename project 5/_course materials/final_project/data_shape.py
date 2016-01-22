'''
Takes in a data dictionary object and appends new engineered
features to it s a {key : value} pair. 
'''


# Trying to create 6 new features:
# [1] is_director : making 'director' a boolean. if value is >0 or not NaN then = 1
# [2] poi_email_interaction : combining 'from_poi' with 'to_poi'
# [3] poi_email_reciept_interaction : same as above but adding 'shared_reciept_with_poi'
# [4] adj_compensation: I am combining a bunch of financial features and MinMaxing it to 0-1
#	features include: 'salary', 'total_payments', 'exercised_stock_options', 'bonus', 
#					  'long_term_incentive', 'total_stock_value'.


def outlier_cleaning(data_dict):
	'''
	https://www.python.org/dev/peps/pep-0257/    ref here for sprucing this up....
	'''
	### remove TOTAL and THE TRAVEL AGENCY IN THE PARK data as outliers.
	### EUGENE had no data, all are NaN except for {'poi':'False'}. Remove him as well.
	del data_dict['TOTAL']
	del data_dict['THE TRAVEL AGENCY IN THE PARK']
	del data_dict['LOCKHART EUGENE E']



def engineered_features(data_dict):
	'''
	describe: data_dict
	talk about arguments and return types 

	'''

	# creating {key : value} for new features and adding them to data set
	for k,v in data_dict.iteritems():
		v['is_director'] = 0
		v['poi_email_interaction'] = 0
		v['poi_email_reciept_interaction'] = 0
		v['adj_compensation'] = 0
		v['from_poi_to_this_person_fraction'] = 0
		v['from_this_person_to_poi_fraction'] = 0

	# 
	for k,v in data_dict.iteritems():
		for key,value in v.iteritems():
			if key == 'director_fees' and value != 'NaN' and value > 0: 
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

			# creating feature for fractional emails from/to POIs
			if key == 'to_messages' and value != 'NaN' and value > 0:
				v['from_poi_to_this_person_fraction'] = int(v['from_poi_to_this_person'])/float(value)

			if key == 'from_messages' and value != 'NaN' and value > 0:
				v['from_this_person_to_poi_fraction'] = int(v['from_this_person_to_poi'])/float(value)

def data_dict_info(data_dict):
	'''
	'''
	## returning simple info about data set: NaNs features and data points
	num_NaNs = 0
	num_data_points = 0
	for k,v in data_dict.iteritems():
		for key, value in v.iteritems():
			#if key == 'poi' and value == True: print "AHHHHH YEAHHHHH"
			num_data_points += 1
			num_features = len(v)
			if value == 'NaN':
				num_NaNs += 1

	# print ("Number of People under Investigation: %s,\
	# 		Number of Data Points: %s, Number of Features: %s") % (
	# 			len(data_dict), num_data_points, num_features)
	# print "Percentage of data points as NaNs: %s" % (num_NaNs/float(num_data_points))
