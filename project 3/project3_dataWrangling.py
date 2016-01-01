#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import pymongo
import sys, traceback
from pymongo import MongoClient

client = MongoClient()
db = client.seattle_osm_database

way_node_collection = db.way_node_collection
addr_attrib = re.compile(r'(?<=addr:)\w+')
postcode = re.compile(r'\d{5}')
SOURCE_TAGS = ['node', 'way']
CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

#zipcodes sourced from http://zipcode.org/city/WA/SEATTLE
COUNTRY_CODE = 'US'
CITY_NAME = 'Seattle'
WA_ZIPCODES = ['98101', '98102', '98104', '98105', '98108', '98109', '98112',
'98113', '98114', '98117', '98103', '98106', '98107', '98111', '98115',
'98116', '98118', '98119', '98121', '98125', '98126', '98132', '98133',
'98138', '98139', '98141', '98122', '98124', '98127', '98129', '98131',
'98134', '98136', '98144', '98145', '98148', '98155', '98160', '98161',
'98164', '98165', '98168', '98170', '98146', '98154', '98158', '98166',
'98174', '98175', '98178', '98190', '98191', '98177', '98181', '98185',
'98188', '98189', '98194', '98195', '98199', '98198']

mapping = { "st" : "Street",
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
	
def is_valid_country(val):
	return val.lower().strip() == COUNTRY_CODE.lower()
	
def is_valid_city(val):
	# split on ',' to grab the actual city name
	# or, we can hardcode for Seattle, WA
	city = val.split(',')
	return city[0].lower().strip() == CITY_NAME.lower()
	
def is_valid_postcode(val):
	return val in WA_ZIPCODES
	
def clean_street(st_name):
	splits = st_name.split(' ')	
	if len(splits) == 1:
		return st_name
	
	buf = []
	is_changed = False
	first = True
	for str in st_name.split(' '):
		if (not first) and str.lower() in mapping:
			is_changed = True
			buf.append(mapping[str.lower()])
		else:
			buf.append(str)
		first = False
	
	new_str = ' '.join(buf)
	if is_changed:
		print ('%s changed to %s') % (st_name, new_str)
	#return ' '.join(buf)
	return new_str

def shape_data(element):
	node = {}
	is_valid = True
	
	if element.tag not in SOURCE_TAGS:
		return None
	
	node["type"] = element.tag
	created = {}
	address = {}
	node_refs = []
	pos = [0,0]
	for k, v in element.attrib.iteritems():
		if k in CREATED:
			created[k] = v
		else:
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
	
		keyType = child.attrib.keys()[0]
		if keyType == 'k':
			val = child.attrib['v']
			key = child.attrib['k']
			
			if key.lower() == 'fixme':
				is_valid = False
				continue
			
			if key.startswith('addr:'):
				if ':' in key[5:]:
					continue
					
				# addr_key is our key
				# e.g. addr_key = 'postcode'
				addr_key = ''.join(addr_attrib.findall(key))
								
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
		
		if len(address) > 0:
			node['address'] = address
		if element.tag == 'way':
			node['node_refs'] = node_refs
	
	# http://www.ibm.com/developerworks/xml/library/x-hiperfparse/
	element.clear()
	# while element.getprevious() is not None:
		# del element.getparent()[0]
	
	if is_valid:
		return node
		#print node
	
	#print 'Exited out of invalid node'
	return None

def process_osm(file_in):
	with open(file_in) as file:
		for _, element in ET.iterparse(file):
			el = shape_data(element)
			if el:
				#pprint.pprint(el)
				way_node_collection.insert(el)
	
	
if __name__ == "__main__":
    #process_osm('sample.osm')
	#process_osm('example.osm')
	process_osm('seattle_washington.osm')

print ""

# def parse_zip(data):    
#     return ''.join(postcode.findall(data))
    
# for zip in zip_strs:
#     print 'input: %s, postcode: %s' % (zip, parse_zip(zip))



