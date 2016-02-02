#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import pymongo
import sys, traceback
from pymongo import MongoClient

# creating mongo db and writing to it document by document as I Iiterate 
# through the .osm xml file
client = MongoClient()
db = client.seattle_osm_database
way_node_collection = db.way_node_collection

# regex to help parse out addr: from dataset and to identfy postcodes.
addr_attrib = re.compile(r'(?<=addr:)\w+')
postcode = re.compile(r'\d{5}')

# Globals to use when parsing data. SOURCE_TAGS and CREATED will act as 
# containers organize parsed data. COUNTRY_CODE, CITY_NAME and WA_ZIPCODES
# will be used to check that the data being written into our db is correct.
# MAPPING is a dict that will be called when changing street type.
SOURCE_TAGS = ['node', 'way']
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]
COUNTRY_CODE = 'US'
CITY_NAME = 'Seattle'
#zipcodes sourced from http://zipcode.org/city/WA/SEATTLE
WA_ZIPCODES = ['98101', '98102', '98104', '98105', '98108', '98109', '98112',
'98113', '98114', '98117', '98103', '98106', '98107', '98111', '98115',
'98116', '98118', '98119', '98121', '98125', '98126', '98132', '98133',
'98138', '98139', '98141', '98122', '98124', '98127', '98129', '98131',
'98134', '98136', '98144', '98145', '98148', '98155', '98160', '98161',
'98164', '98165', '98168', '98170', '98146', '98154', '98158', '98166',
'98174', '98175', '98178', '98190', '98191', '98177', '98181', '98185',
'98188', '98189', '98194', '98195', '98199', '98198']
MAPPING = { "st" : "Street",
			"st." : "Street",
			"rd" : "Road",
			"rd." : "Road",
			"ave" : "Avenue",
			"ave." : "Avenue",
			"ln" : "Lane",
			"ln." : "Lane",
			"pl" : "Place",
			"pl." : "Place",
			"la" : "Lane",
			"la." : "Lane",
			"ct" : "Court",
			"ct." : "Court",
			"pkw" : "Parkway",
			"pkw." : "Parkway",
			"pkwy" : "Parkway",
			"pkwy." : "Parkway",
			"pk" : "Park",
			"pk." : "Park",
			"crl" : "Circle",
			"crl." : "Circle",
			"blvd" : "Boulevard",
			"blvd." : "Boulevard",
			"hwy" : "Highway",
			"hwy." : "Highway",
			"dr" : "Drive",
			"dr." : "Drive"}
	
# check if country code is US
def is_valid_country(val):
	return val.lower().strip() == COUNTRY_CODE.lower()

	
# check if city is listed as seattle. For cases of 'Seattle, WA' using .split()
# will return a list so we can .strip(), and .lower() while getting the [0] element
# and comapring that, which will be 'seattle' or another city to our CITY_NAME.
def is_valid_city(val):
	city = val.split(',')
	return city[0].lower().strip() == CITY_NAME.lower()
	

# checking if the postcode is in Seattle's postcodes and not another postcode, 
# or for example Bellvue, WA which is a city just out of seattle.
def is_valid_postcode(val):
	return val in WA_ZIPCODES
	

# function to clean the street name and compare/change street types to MAPPING dict vlaue.
def clean_street(st_name):
	splits = st_name.split(' ')	
	if len(splits) == 1:
		return st_name
	
	buf = []
	is_changed = False
	first = True
	for str in st_name.split(' '):
		if (not first) and str.lower() in MAPPING:
			is_changed = True
			buf.append(MAPPING[str.lower()])
		else:
			buf.append(str)
		first = False
	
	new_str = ' '.join(buf)
	if is_changed:
		print ('%s changed to %s') % (st_name, new_str)
	return new_str


# main function that takes in an xml  
def shape_data(element):
	node = {}
	# flag for writing data. If this is tue at end of function formatted data is returned
	# if not then the data did not meet our specification and nothing is returned so the 
	# iterator can continue to comb through the xml file.
	is_valid = True
	
	# check if xml tag is node or way.
	if element.tag not in SOURCE_TAGS:
		return None
	
	# creating 
	node["type"] = element.tag
	created = {}
	address = {}
	node_refs = []
	pos = [0,0]
	#getting the key/value pairs for the xml item and iterating through it.
	# to populate long/lat POS and the CREATED dict.
	for k, v in element.attrib.iteritems():
		if k in CREATED:
			created[k] = v
		else:
			# adding lat and long to our node element.
			if k == "lat":
				pos[0] = float(v)
			elif k == "lon":
				pos[1] = float(v)
			else:
				#print "root", k, v
				node[k] = v
	node["pos"] = pos
	node["created"] = created
	
	for child in element:
		if not is_valid:
			continue
			#return None
	
		# thid part was a bit tricky because there was a key/value pair within a 
		# key/value pair. E.g.:
		# <tag k="highway" v="traffic_signals" /> we want 'highway' and 'traffic signals'
		# but they are located within their own K/V pairs.
		keyType = child.attrib.keys()[0]
		if keyType == 'k':
			val = child.attrib['v']
			key = child.attrib['k']
			
			# choose to ignore fixme entries as we cannot trust the data within it.
			if key.lower() == 'fixme':
				is_valid = False
				continue
			
			# found some weird double addr:xyz:xyz addresses. Choose to ignore these as well.
			if key.startswith('addr:'):
				if ':' in key[5:]:
					continue
					
				# addr_key is our key
				# e.g. addr_key = 'postcode'
				addr_key = ''.join(addr_attrib.findall(key))
				
				# checking to make sure our data is in Seattle. Caught a lot of Canadian data				
				if addr_key.lower() == 'country':
					is_valid = is_valid_country(val)
					
				if addr_key.lower() == 'city':
					is_valid = is_valid_city(val)
					
				if addr_key.lower() == 'postcode':
					is_valid = is_valid_postcode(val)
				
				if not is_valid:
					continue
				
				# clean up street name
				if addr_key == 'street':
					val = clean_street(val)
					
				address[addr_key] = val
			
			# save this key/value to the node
			node[key] = val
		elif keyType == 'ref':
			node_refs.append(child.attrib['ref'])
		else:
			print 'not k/v: ', keyType
		
		# had to rerun the whole program again.. at first empty addresse {} dicts were
		# being added to nodes. 
		if len(address) > 0:
			node['address'] = address
		# easy to add all refs tags located in way nodes. 
		if element.tag == 'way':
			node['node_refs'] = node_refs
	
	# my laptop ran out of memory without this. apparently eetree iteratively 
	# builds a tree, without this line of code your machine eventually runs
	# out of memory. If the data set is large enough.
	# http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
	element.clear()
	# while element.getprevious() is not None:
		# del element.getparent()[0]
	

	# if no issues were found in auditing the data, then we return node. This is 
	# the other half of the flag created at the beginning of the function. 
	if is_valid:
		return node
		#print node
	
	#print 'Exited out of invalid node'
	return None
	
	# What formatted data: <node>, could look like after the xml has passed through this function:
		# {
		# 	"amenity" : "bicycle_parking",
		# 	"created" : {
		# 		"changeset" : "8421581",
		# 		"user" : "alester",
		# 		"version" : "3",
		# 		"uid" : "307202",
		# 		"timestamp" : "2011-06-13T02:42:07Z"
		# 	},
		# 	"pos" : [
		# 		48.4924963,
		# 		-123.3454852
		# 	],
		# 	"type" : "node",
		# 	"id" : "277636555"
		# }


# this function is what iterates through the .osm xml file data. It passes an element
# to the parsing function and recieves (if the data is apppropriate), a dict like element
# that is written as a document into the collection: way_node_collection 
# which is in oir database. I found this to be more streamlined than writing to a JSON
# file and then iterating through/writing that file to the DB. 
def process_osm(file_in):
	with open(file_in) as file:
		for _, element in ET.iterparse(file):
			el = shape_data(element)
			if el:
				#pprint.pprint(el)
				way_node_collection.insert(el)
	

# This kicks off the process. and because __name__ does equal "--main__" the data file,
# 'seattle_washington.osm' is passed to the process_osm function. I have two other flavors
# of the function. To test I set up a decimated 'sample.osm' file, which takes about 
# 2 min to run. The example.osm file is the even smaller Chicago data used in lecture. 	
if __name__ == "__main__":
    #process_osm('sample.osm')
	#process_osm('example.osm')
	process_osm('seattle_washington.osm')


# Once program is done running bell rings. useful since it takes about 20 min to run.
print ""




