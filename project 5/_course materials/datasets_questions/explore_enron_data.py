#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle

enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))

print "length of Enron Dict: ", len(enron_data)

# printing a sample of data and number of total samples.
count = True
for k, v in enron_data.iteritems():
	if count:
		print "Sample {Key : Value} pair:" 
		print "key: %s | value: %s" % (k, v)
		print "Number of features: ", len(v)
	count = False

# counting number of people_of_interest using the 'poi' feature.
# This comes from the email addresses file... poi_email_address.py
num_of_poi = 0
for k, dictionary in enron_data.iteritems():
	for k, v in dictionary.iteritems():
		if k == 'poi': 
			if v: num_of_poi += 1
print 'Number of "poi": ', num_of_poi


# accessing James Prentice's stock value
print "Prentice's total stock value: ", (enron_data["PRENTICE JAMES"]
										["total_stock_value"])


# accessing Wesley Colwell num of email messages
print "Colwell's from messages to poi: ", (enron_data["COLWELL WESLEY"]
											["from_this_person_to_poi"])

# accessing Jefferey Skilling's stock options exercised
print "Skillings's total stock options exercised: ",( 
	enron_data["SKILLING JEFFREY K"]['exercised_stock_options'])


# print who took home the most money of the three
print "Skillings's take home: ", enron_data["SKILLING JEFFREY K"]['total_payments']
print "Lay's take home: ", enron_data["LAY KENNETH L"]['total_payments']
print "Fastow's take home: ", enron_data["FASTOW ANDREW S"]['total_payments']


# discover how num of NaN in ['salary'] and ['email_address']
NaN_salary = 0
NaN_email_addy = 0
for k, dictionary in enron_data.iteritems():
	for k, v in dictionary.iteritems():
		if k == 'salary': 
			if v == 'NaN':
				NaN_salary += 1
		elif k == 'email_address':
			if v == 'NaN':
				NaN_email_addy += 1
		else: 
			continue
print "Num of NaN Salaries: %s and Num of NaN Email Addys: %s" % (NaN_salary, NaN_email_addy)


# num of people thta have NaN for total payments in E+F dataset
NaN_total_payments = 0
for k, dictionary in enron_data.iteritems():
	for k, v in dictionary.iteritems():
		if k == 'total_payments': 
			if v == 'NaN': NaN_total_payments += 1

percentage_total_paymts = float(NaN_total_payments)/len(enron_data)*100

print "Num of NaN total payments: %s and percentage of total datset is: %s" % (
									NaN_total_payments, percentage_total_paymts)


# % of POIs have NaN for total payments
NaN_pay_poi = {}
for key, dictionary in enron_data.iteritems():
	for k, v in dictionary.iteritems():
		if k == 'poi':
			if v:
				NaN_pay_poi[key] = enron_data[key]['total_payments']
print len(NaN_pay_poi)


# hardware bell
print ('\a')


